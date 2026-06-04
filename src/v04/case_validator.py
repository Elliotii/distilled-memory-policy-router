"""Minimal structural validator for v0.4 case records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.v04.parser import LEGAL_TARGETS, parse_policy_dsl


REQUIRED_TOP_LEVEL_FIELDS = (
    "case_id",
    "runtime_context",
    "candidate_memories",
    "current_units",
    "gold",
    "tags",
    "notes",
)
REQUIRED_RUNTIME_CONTEXT_FIELDS = ("project", "repo", "service", "task")
LEGAL_TARGET_SET = set(LEGAL_TARGETS)
ALLOWED_GOLD_FIELDS = {"read", "store", "skip", "dsl"}
FORBIDDEN_GOLD_FIELDS = {
    "fact",
    "decision",
    "preference",
    "sop",
    "type",
    "subtype",
    "reason",
    "entity",
    "confidence",
    "needs_review",
    "ADD",
    "UPDATE",
    "DELETE",
    "MERGE",
}


def validate_case(record: dict[str, Any]) -> dict[str, Any]:
    """Validate one v0.4 case record without semantic repair."""

    errors: list[str] = []
    if not isinstance(record, dict):
        return {"valid": False, "errors": ["record must be an object"]}

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in record:
            errors.append(f"missing required field: {field}")

    case_id = record.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        errors.append("case_id is required")

    runtime_context = record.get("runtime_context")
    if not isinstance(runtime_context, dict):
        errors.append("runtime_context must be an object")
    else:
        for field in REQUIRED_RUNTIME_CONTEXT_FIELDS:
            value = runtime_context.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"missing runtime_context field: {field}")

    candidate_memory_ids = _validate_candidate_memories(record.get("candidate_memories"), errors)
    current_unit_ids = _validate_current_units(record.get("current_units"), errors)

    gold = record.get("gold")
    if not isinstance(gold, dict):
        errors.append("gold must be an object")
        gold = {}
    else:
        for field in gold:
            if field not in ALLOWED_GOLD_FIELDS:
                errors.append(f"unsupported gold field: {field}")
            if field in FORBIDDEN_GOLD_FIELDS:
                errors.append(f"forbidden gold field: {field}")

    if "read" not in gold:
        errors.append("missing gold field: read")
    if "store" not in gold:
        errors.append("missing gold field: store")
    if "skip" not in gold:
        errors.append("missing gold field: skip")

    gold_read = _validate_gold_read(gold.get("read"), set(candidate_memory_ids), errors)
    gold_store = _validate_gold_store(gold.get("store"), set(current_unit_ids), errors)
    gold_skip = _validate_gold_skip(gold.get("skip"), set(current_unit_ids), errors)
    _validate_unit_assignment(current_unit_ids, gold_store, gold_skip, errors)
    _validate_gold_dsl(gold.get("dsl"), candidate_memory_ids, current_unit_ids, gold_read, gold_store, gold_skip, errors)

    tags = record.get("tags")
    if not isinstance(tags, list) or not all(isinstance(tag, str) and tag for tag in tags):
        errors.append("tags must be a list of non-empty strings")

    notes = record.get("notes")
    if not isinstance(notes, str):
        errors.append("notes must be a string")

    return {"valid": not errors, "errors": errors}


def validate_jsonl_file(path: str | Path) -> dict[str, Any]:
    """Validate a JSONL file containing v0.4 case records."""

    path = Path(path)
    errors: list[str] = []
    record_count = 0

    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            record_count += 1
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
                continue

            result = validate_case(record)
            for error in result["errors"]:
                errors.append(f"line {line_number}: {error}")

    return {"valid": not errors, "errors": errors, "record_count": record_count}


def _validate_candidate_memories(value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append("candidate_memories must be a list")
        return []

    memory_ids: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"candidate_memories[{index}] must be an object")
            continue

        memory_id = item.get("memory_id")
        target = item.get("target")
        content = item.get("content") or item.get("text", "")

        if not isinstance(memory_id, str) or not memory_id.strip():
            errors.append(f"candidate_memories[{index}].memory_id is required")
        elif memory_id in seen:
            errors.append(f"duplicate candidate memory_id: {memory_id}")
        else:
            seen.add(memory_id)
            memory_ids.append(memory_id)

        if target not in LEGAL_TARGET_SET:
            label = memory_id if isinstance(memory_id, str) and memory_id else f"index {index}"
            errors.append(f"invalid candidate memory target for {label}: {target}")
        if not isinstance(content, str) or not content.strip():
            label = memory_id if isinstance(memory_id, str) and memory_id else f"index {index}"
            errors.append(f"candidate memory content is required for {label}")

    return memory_ids


def _validate_current_units(value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append("current_units must be a list")
        return []

    unit_ids: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"current_units[{index}] must be an object")
            continue

        unit_id = item.get("unit_id")
        text = item.get("text")

        if not isinstance(unit_id, str) or not unit_id.strip():
            errors.append(f"current_units[{index}].unit_id is required")
        elif unit_id in seen:
            errors.append(f"duplicate current unit_id: {unit_id}")
        else:
            seen.add(unit_id)
            unit_ids.append(unit_id)

        if not isinstance(text, str) or not text.strip():
            label = unit_id if isinstance(unit_id, str) and unit_id else f"index {index}"
            errors.append(f"current unit text is required for {label}")

    return unit_ids


def _validate_gold_read(value: Any, candidate_memory_ids: set[str], errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append("gold.read must be a list")
        return []

    read_ids: list[str] = []
    seen: set[str] = set()
    for memory_id in value:
        if not isinstance(memory_id, str) or not memory_id.strip():
            errors.append("gold.read entries must be non-empty strings")
            continue
        if memory_id not in candidate_memory_ids:
            errors.append(f"gold.read unknown memory_id: {memory_id}")
        if memory_id in seen:
            errors.append(f"duplicate gold.read memory_id: {memory_id}")
            continue
        seen.add(memory_id)
        read_ids.append(memory_id)

    return read_ids


def _validate_gold_store(value: Any, current_unit_ids: set[str], errors: list[str]) -> list[dict[str, str]]:
    if not isinstance(value, list):
        errors.append("gold.store must be a list")
        return []

    store_entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"gold.store[{index}] must be an object")
            continue

        for field in item:
            if field not in {"target", "unit_id"}:
                errors.append(f"unsupported gold.store field: {field}")
            if field in FORBIDDEN_GOLD_FIELDS:
                errors.append(f"forbidden gold.store field: {field}")

        target = item.get("target")
        unit_id = item.get("unit_id")
        if target not in LEGAL_TARGET_SET:
            label = unit_id if isinstance(unit_id, str) and unit_id else f"index {index}"
            errors.append(f"gold.store invalid target for {label}: {target}")
        if not isinstance(unit_id, str) or not unit_id.strip():
            errors.append(f"gold.store[{index}].unit_id is required")
            continue
        if unit_id not in current_unit_ids:
            errors.append(f"gold.store unknown unit_id: {unit_id}")
        if unit_id in seen:
            errors.append(f"duplicate gold.store unit_id: {unit_id}")
            continue
        seen.add(unit_id)
        store_entries.append({"target": target, "unit_id": unit_id})

    return store_entries


def _validate_gold_skip(value: Any, current_unit_ids: set[str], errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append("gold.skip must be a list")
        return []

    skip_ids: list[str] = []
    seen: set[str] = set()
    for unit_id in value:
        if not isinstance(unit_id, str) or not unit_id.strip():
            errors.append("gold.skip entries must be non-empty strings")
            continue
        if unit_id not in current_unit_ids:
            errors.append(f"gold.skip unknown unit_id: {unit_id}")
        if unit_id in seen:
            errors.append(f"duplicate gold.skip unit_id: {unit_id}")
            continue
        seen.add(unit_id)
        skip_ids.append(unit_id)

    return skip_ids


def _validate_unit_assignment(
    current_unit_ids: list[str],
    gold_store: list[dict[str, str]],
    gold_skip: list[str],
    errors: list[str],
) -> None:
    store_ids = {entry["unit_id"] for entry in gold_store}
    skip_ids = set(gold_skip)
    for unit_id in current_unit_ids:
        in_store = unit_id in store_ids
        in_skip = unit_id in skip_ids
        if in_store and in_skip:
            errors.append(f"unit appears in both gold.store and gold.skip: {unit_id}")
        elif not in_store and not in_skip:
            errors.append(f"unit missing from gold.store/gold.skip: {unit_id}")


def _validate_gold_dsl(
    dsl: Any,
    candidate_memory_ids: list[str],
    current_unit_ids: list[str],
    gold_read: list[str],
    gold_store: list[dict[str, str]],
    gold_skip: list[str],
    errors: list[str],
) -> None:
    if dsl is None:
        return
    if not isinstance(dsl, str) or not dsl.strip():
        # Accept empty DSL when structured fields (read/store/skip) are present
        return

    parsed = parse_policy_dsl(dsl, candidate_memory_ids, current_unit_ids, LEGAL_TARGETS)
    if not parsed["validation"]["valid"]:
        for error in parsed["validation"]["errors"]:
            errors.append(f"gold.dsl invalid: {error}")
        return

    parsed_read = {item["memory_id"] for item in parsed["read"]}
    parsed_store = {item["unit_id"]: item["target"] for item in parsed["store"]}
    parsed_skip = {item["unit_id"] for item in parsed["skip"]}
    expected_read = set(gold_read)
    expected_store = {item["unit_id"]: item["target"] for item in gold_store}
    expected_skip = set(gold_skip)

    if parsed_read != expected_read:
        errors.append("gold.dsl read does not match gold.read")
    if parsed_store != expected_store:
        errors.append("gold.dsl store does not match gold.store")
    if parsed_skip != expected_skip:
        errors.append("gold.dsl skip does not match gold.skip")
