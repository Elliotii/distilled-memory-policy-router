"""Validate MVP multi-turn memory-policy trace JSONL files."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED_WRITE_TYPES = {"fact", "decision", "sop", "task_state"}
ALLOWED_ROLES = {"user", "assistant", "system", "tool"}
TARGET_KEYS = {"read_hints", "write_spans", "ignore_spans"}


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(row, dict):
                errors.append(f"line {line_number}: trace record must be an object")
                continue
            rows.append(row)
    return rows, errors


def validate_target(
    trace_id: str,
    turn_id: str,
    current_user_input: str,
    candidate_memories: list[dict[str, Any]],
    target: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if set(target) != TARGET_KEYS:
        errors.append(f"{trace_id}/{turn_id}: target keys must be {sorted(TARGET_KEYS)}")
        return errors

    memory_ids = [
        memory.get("id")
        for memory in candidate_memories
        if isinstance(memory, dict) and isinstance(memory.get("id"), str)
    ]
    memory_id_set = set(memory_ids)

    read_hints = target.get("read_hints")
    if not isinstance(read_hints, list):
        errors.append(f"{trace_id}/{turn_id}: read_hints must be a list")
    else:
        if len(read_hints) != len(set(read_hints)):
            errors.append(f"{trace_id}/{turn_id}: read_hints contain duplicates")
        for memory_id in read_hints:
            if memory_id not in memory_id_set:
                errors.append(f"{trace_id}/{turn_id}: read_hints missing candidate {memory_id!r}")

    write_spans = target.get("write_spans")
    if not isinstance(write_spans, list):
        errors.append(f"{trace_id}/{turn_id}: write_spans must be a list")
    else:
        seen_write_spans: set[str] = set()
        for index, write_span in enumerate(write_spans):
            if not isinstance(write_span, dict):
                errors.append(f"{trace_id}/{turn_id}: write_spans[{index}] must be an object")
                continue
            span = write_span.get("span")
            memory_type = write_span.get("type")
            if not isinstance(span, str) or not span:
                errors.append(f"{trace_id}/{turn_id}: write_spans[{index}].span is invalid")
                continue
            if span in seen_write_spans:
                errors.append(f"{trace_id}/{turn_id}: duplicate write span {span!r}")
            seen_write_spans.add(span)
            if span not in current_user_input:
                errors.append(f"{trace_id}/{turn_id}: write span is not an exact input substring: {span!r}")
            if memory_type not in ALLOWED_WRITE_TYPES:
                errors.append(f"{trace_id}/{turn_id}: invalid write type {memory_type!r}")

    ignore_spans = target.get("ignore_spans")
    if not isinstance(ignore_spans, list):
        errors.append(f"{trace_id}/{turn_id}: ignore_spans must be a list")
    else:
        if len(ignore_spans) != len(set(ignore_spans)):
            errors.append(f"{trace_id}/{turn_id}: ignore_spans contain duplicates")
        for index, span in enumerate(ignore_spans):
            if not isinstance(span, str) or not span:
                errors.append(f"{trace_id}/{turn_id}: ignore_spans[{index}] is invalid")
                continue
            if span not in current_user_input:
                errors.append(f"{trace_id}/{turn_id}: ignore span is not an exact input substring: {span!r}")

    return errors


def validate_trace(row: dict[str, Any]) -> tuple[list[str], Counter[str]]:
    errors: list[str] = []
    metrics: Counter[str] = Counter()

    trace_id = row.get("trace_id")
    if not isinstance(trace_id, str) or not trace_id:
        return ["trace record is missing trace_id"], metrics
    if not json.dumps(row, ensure_ascii=True).isascii():
        errors.append(f"{trace_id}: trace must be ASCII")

    turns = row.get("turns")
    if not isinstance(turns, list) or not (2 <= len(turns) <= 5):
        errors.append(f"{trace_id}: turns must contain 2-5 items")
        return errors, metrics

    turn_ids: list[str] = []
    for turn in turns:
        if not isinstance(turn, dict):
            errors.append(f"{trace_id}: turn must be an object")
            continue
        turn_id = turn.get("turn_id")
        if not isinstance(turn_id, str) or not turn_id:
            errors.append(f"{trace_id}: turn missing turn_id")
            turn_id = "<missing>"
        turn_ids.append(turn_id)

        current_user_input = turn.get("current_user_input")
        if not isinstance(current_user_input, str) or not current_user_input:
            errors.append(f"{trace_id}/{turn_id}: current_user_input is required")
            current_user_input = ""

        recent_context = turn.get("recent_context")
        if not isinstance(recent_context, list) or len(recent_context) > 4:
            errors.append(f"{trace_id}/{turn_id}: recent_context must be a list of 0-4 turns")
            recent_context = []
        for index, context_turn in enumerate(recent_context):
            if not isinstance(context_turn, dict):
                errors.append(f"{trace_id}/{turn_id}: recent_context[{index}] must be an object")
                continue
            if context_turn.get("role") not in ALLOWED_ROLES:
                errors.append(f"{trace_id}/{turn_id}: invalid recent_context role {context_turn.get('role')!r}")
            if not isinstance(context_turn.get("content"), str) or not context_turn.get("content"):
                errors.append(f"{trace_id}/{turn_id}: recent_context[{index}].content is required")

        candidate_memories = turn.get("candidate_memories")
        if not isinstance(candidate_memories, list) or len(candidate_memories) > 8:
            errors.append(f"{trace_id}/{turn_id}: candidate_memories must be a list of 0-8 items")
            candidate_memories = []
        memory_ids: list[str] = []
        for index, memory in enumerate(candidate_memories):
            if not isinstance(memory, dict):
                errors.append(f"{trace_id}/{turn_id}: candidate_memories[{index}] must be an object")
                continue
            memory_id = memory.get("id")
            if not isinstance(memory_id, str) or not memory_id:
                errors.append(f"{trace_id}/{turn_id}: candidate_memories[{index}].id is required")
            else:
                memory_ids.append(memory_id)
            if memory.get("type") not in ALLOWED_WRITE_TYPES:
                errors.append(f"{trace_id}/{turn_id}: invalid candidate memory type {memory.get('type')!r}")
            if not isinstance(memory.get("content"), str) or not memory.get("content"):
                errors.append(f"{trace_id}/{turn_id}: candidate_memories[{index}].content is required")
        if len(memory_ids) != len(set(memory_ids)):
            errors.append(f"{trace_id}/{turn_id}: candidate memory IDs are not unique")

        target = turn.get("target")
        if not isinstance(target, dict):
            errors.append(f"{trace_id}/{turn_id}: target must be an object")
            continue
        errors.extend(validate_target(trace_id, turn_id, current_user_input, candidate_memories, target))

        metrics["turns"] += 1
        metrics["read_hints"] += len(target.get("read_hints", []))
        metrics["write_spans"] += len(target.get("write_spans", []))
        metrics["ignore_spans"] += len(target.get("ignore_spans", []))
        if candidate_memories:
            metrics["turns_with_candidate_memories"] += 1
        if recent_context:
            metrics["turns_with_recent_context"] += 1

    if len(turn_ids) != len(set(turn_ids)):
        errors.append(f"{trace_id}: turn_ids are not unique")

    return errors, metrics


def format_report(path: Path, rows: list[dict[str, Any]], errors: list[str], metrics: Counter[str]) -> str:
    lines = [
        f"Trace validation report for {path}",
        f"total traces: {len(rows)}",
        f"total turns: {metrics['turns']}",
        f"turns_with_candidate_memories: {metrics['turns_with_candidate_memories']}",
        f"turns_with_recent_context: {metrics['turns_with_recent_context']}",
        f"target.read_hints: {metrics['read_hints']}",
        f"target.write_spans: {metrics['write_spans']}",
        f"target.ignore_spans: {metrics['ignore_spans']}",
        f"errors: {len(errors)}",
    ]
    lines.extend(f"  - {error}" for error in errors)
    if not errors:
        lines.append("All checks passed.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    rows, errors = load_jsonl(args.path)
    trace_ids = [row.get("trace_id") for row in rows]
    for trace_id, count in Counter(trace_ids).items():
        if count > 1:
            errors.append(f"duplicate trace_id: {trace_id}")

    metrics: Counter[str] = Counter()
    for row in rows:
        trace_errors, trace_metrics = validate_trace(row)
        errors.extend(trace_errors)
        metrics.update(trace_metrics)

    report = format_report(args.path, rows, errors, metrics)
    if args.report:
        args.report.write_text(report, encoding="utf-8")
    print(report, end="")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
