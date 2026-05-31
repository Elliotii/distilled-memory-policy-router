"""Strict parser for the v0.4 READ / STORE / SKIP DSL."""

from __future__ import annotations

from collections.abc import Iterable


SCHEMA_VERSION = "memory_policy.v0.4"
LEGAL_TARGETS = (
    "user_profile",
    "project_memory",
    "repo_memory",
    "service_memory",
    "task_state",
)


def parse_policy_dsl(
    raw_dsl: str,
    candidate_memory_ids: Iterable[str],
    current_unit_ids: Iterable[str],
    legal_targets: Iterable[str] = LEGAL_TARGETS,
) -> dict:
    """Parse v0.4 DSL into canonical JSON-like output.

    Ordering is deterministic and follows first valid occurrence in the raw DSL.
    READ duplicates are mechanically deduplicated. STORE/SKIP duplicates and
    conflicts are validation errors, not repairs.
    """

    candidate_ids = list(candidate_memory_ids)
    unit_ids = list(current_unit_ids)
    candidate_id_set = set(candidate_ids)
    unit_id_set = set(unit_ids)
    legal_target_set = set(legal_targets)

    read_ids: list[str] = []
    read_seen: set[str] = set()
    store_entries: list[dict[str, str]] = []
    store_seen: set[str] = set()
    skip_ids: list[str] = []
    skip_seen: set[str] = set()
    errors: list[str] = []

    read_line_count = 0
    skip_line_count = 0
    store_none_seen = False

    lines = [line.strip() for line in raw_dsl.splitlines() if line.strip()]
    if not lines:
        return _result([], [], [], ["empty output"])

    for line in lines:
        keyword, _, rest = line.partition(" ")
        rest = rest.strip()

        if keyword == "READ":
            read_line_count += 1
            if read_line_count > 1:
                errors.append("duplicate READ line")
                continue
            if not rest:
                errors.append(f"malformed READ line: {line}")
                continue
            if rest == "NONE":
                continue

            memory_ids, list_errors = _parse_id_list(rest, "READ")
            errors.extend(list_errors)
            for memory_id in memory_ids:
                if memory_id not in candidate_id_set:
                    errors.append(f"unknown memory_id: {memory_id}")
                    continue
                if memory_id not in read_seen:
                    read_seen.add(memory_id)
                    read_ids.append(memory_id)

        elif keyword == "STORE":
            if not rest:
                errors.append(f"malformed STORE line: {line}")
                continue
            if rest == "NONE":
                if store_none_seen:
                    errors.append("duplicate STORE NONE")
                store_none_seen = True
                continue

            parts = rest.split()
            if len(parts) != 2:
                errors.append(f"malformed STORE line: {line}")
                continue

            target, unit_id = parts
            if target not in legal_target_set:
                errors.append(f"invalid target: {target}")
            if unit_id not in unit_id_set:
                errors.append(f"unknown unit_id in STORE: {unit_id}")
                continue
            if unit_id in store_seen:
                errors.append(f"duplicate STORE unit_id: {unit_id}")
                continue

            store_seen.add(unit_id)
            store_entries.append({"target": target, "unit_id": unit_id})

        elif keyword == "SKIP":
            skip_line_count += 1
            if skip_line_count > 1:
                errors.append("duplicate SKIP line")
                continue
            if not rest:
                errors.append(f"malformed SKIP line: {line}")
                continue
            if rest == "NONE":
                continue

            unit_ids_from_line, list_errors = _parse_id_list(rest, "SKIP")
            errors.extend(list_errors)
            for unit_id in unit_ids_from_line:
                if unit_id not in unit_id_set:
                    errors.append(f"unknown unit_id in SKIP: {unit_id}")
                    continue
                if unit_id in skip_seen:
                    errors.append(f"duplicate SKIP unit_id: {unit_id}")
                    continue
                skip_seen.add(unit_id)
                skip_ids.append(unit_id)

        else:
            errors.append(f"unknown line type: {keyword}")

    if store_none_seen and store_entries:
        errors.append("STORE NONE cannot be combined with STORE assignments")

    for unit_id in unit_ids:
        in_store = unit_id in store_seen
        in_skip = unit_id in skip_seen
        if in_store and in_skip:
            errors.append(f"unit appears in both STORE and SKIP: {unit_id}")
        elif not in_store and not in_skip:
            errors.append(f"missing unit assignment: {unit_id}")

    if errors:
        return _result([], [], [], errors)

    return _result(
        [{"memory_id": memory_id} for memory_id in read_ids],
        store_entries,
        [{"unit_id": unit_id} for unit_id in skip_ids],
        [],
    )


def _parse_id_list(raw_value: str, line_type: str) -> tuple[list[str], list[str]]:
    values = [value.strip() for value in raw_value.split(",")]
    if any(value == "" for value in values):
        return [], [f"malformed {line_type} list: {raw_value}"]
    return values, []


def _result(read: list[dict], store: list[dict], skip: list[dict], errors: list[str]) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "read": read,
        "store": store,
        "skip": skip,
        "validation": {
            "valid": not errors,
            "errors": errors,
        },
    }
