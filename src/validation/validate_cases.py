"""Validate memory policy router JSONL decision cases."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pydantic import ValidationError

from src.schemas import REQUIRED_CATEGORIES, Category, DecisionCase, MemoryType


@dataclass
class JsonRecord:
    """A parsed JSONL record with source line metadata."""

    line_number: int
    payload: dict[str, Any]


@dataclass
class DatasetDiagnostics:
    """Validation details that are useful even when schema validation fails."""

    invalid_json: list[str] = field(default_factory=list)
    schema_errors: list[str] = field(default_factory=list)
    invalid_read_hints: list[str] = field(default_factory=list)
    invalid_spans: list[str] = field(default_factory=list)
    duplicate_case_ids: list[str] = field(default_factory=list)
    duplicate_current_user_inputs: list[str] = field(default_factory=list)
    category_minimum_errors: list[str] = field(default_factory=list)

    def all_errors(self) -> list[str]:
        return [
            *self.invalid_json,
            *self.schema_errors,
            *self.invalid_read_hints,
            *self.invalid_spans,
            *self.duplicate_case_ids,
            *self.duplicate_current_user_inputs,
            *self.category_minimum_errors,
        ]


def load_records(path: Path) -> tuple[list[JsonRecord], list[str]]:
    records: list[JsonRecord] = []
    errors: list[str] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue

            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc}")
                continue

            if not isinstance(payload, dict):
                errors.append(f"line {line_number}: JSONL record must be an object")
                continue

            records.append(JsonRecord(line_number=line_number, payload=payload))

    return records, errors


def load_cases(records: list[JsonRecord]) -> tuple[list[DecisionCase], list[str]]:
    cases: list[DecisionCase] = []
    errors: list[str] = []

    for record in records:
        try:
            cases.append(DecisionCase.model_validate(record.payload))
        except ValidationError as exc:
            errors.append(f"line {record.line_number}: schema validation failed: {exc}")

    return cases, errors


def _target_for(record: JsonRecord) -> dict[str, Any] | None:
    target = record.payload.get("target")
    if isinstance(target, dict):
        return target
    return None


def collect_invalid_read_hints(records: list[JsonRecord]) -> list[str]:
    errors: list[str] = []

    for record in records:
        target = _target_for(record)
        if target is None:
            continue

        candidate_memories = record.payload.get("candidate_memories", [])
        if not isinstance(candidate_memories, list):
            continue

        candidate_ids = {
            memory.get("id")
            for memory in candidate_memories
            if isinstance(memory, dict) and isinstance(memory.get("id"), str)
        }

        read_hints = target.get("read_hints", [])
        if not isinstance(read_hints, list):
            continue

        missing_ids = [
            memory_id
            for memory_id in read_hints
            if isinstance(memory_id, str) and memory_id not in candidate_ids
        ]
        if missing_ids:
            case_id = record.payload.get("case_id", f"line {record.line_number}")
            errors.append(f"{case_id}: read_hints reference missing IDs: {missing_ids}")

    return errors


def collect_invalid_spans(records: list[JsonRecord]) -> list[str]:
    errors: list[str] = []

    for record in records:
        target = _target_for(record)
        current_user_input = record.payload.get("current_user_input")
        if target is None or not isinstance(current_user_input, str):
            continue

        case_id = record.payload.get("case_id", f"line {record.line_number}")
        write_spans = target.get("write_spans", [])
        if isinstance(write_spans, list):
            for index, write_span in enumerate(write_spans):
                if not isinstance(write_span, dict):
                    continue
                span = write_span.get("span")
                if not isinstance(span, str) or not span or span not in current_user_input:
                    errors.append(
                        f"{case_id}: invalid write_spans[{index}].span: {span!r}"
                    )

        ignore_spans = target.get("ignore_spans", [])
        if isinstance(ignore_spans, list):
            for index, span in enumerate(ignore_spans):
                if not isinstance(span, str) or not span or span not in current_user_input:
                    errors.append(f"{case_id}: invalid ignore_spans[{index}]: {span!r}")

    return errors


def validate_dataset(cases: list[DecisionCase], min_per_category: int) -> DatasetDiagnostics:
    diagnostics = DatasetDiagnostics()

    case_ids = [case.case_id for case in cases]
    duplicate_case_ids = sorted(case_id for case_id, count in Counter(case_ids).items() if count > 1)
    diagnostics.duplicate_case_ids = [
        f"duplicate case_id value: {case_id}" for case_id in duplicate_case_ids
    ]

    inputs = [case.current_user_input for case in cases]
    duplicate_inputs = sorted(text for text, count in Counter(inputs).items() if count > 1)
    diagnostics.duplicate_current_user_inputs = [
        f"duplicate current_user_input value: {text}" for text in duplicate_inputs
    ]

    if min_per_category > 0:
        category_counts = Counter(case.category for case in cases)
        for category in REQUIRED_CATEGORIES:
            count = category_counts.get(category, 0)
            if count < min_per_category:
                diagnostics.category_minimum_errors.append(
                    f"category {category.value!r} has {count} cases; "
                    f"expected at least {min_per_category}"
                )

    return diagnostics


def count_memory_types(cases: list[DecisionCase]) -> tuple[Counter[MemoryType], Counter[MemoryType]]:
    candidate_counts: Counter[MemoryType] = Counter()
    write_counts: Counter[MemoryType] = Counter()

    for case in cases:
        candidate_counts.update(memory.type for memory in case.candidate_memories)
        write_counts.update(write_span.type for write_span in case.target.write_spans)

    return candidate_counts, write_counts


def print_count_section(title: str, counts: Counter[Any], ordered_values: list[Any]) -> None:
    print(f"{title}:")
    for value in ordered_values:
        key = value.value if hasattr(value, "value") else str(value)
        print(f"  {key}: {counts.get(value, 0)}")


def format_count_section(title: str, counts: Counter[Any], ordered_values: list[Any]) -> list[str]:
    lines = [f"{title}:"]
    for value in ordered_values:
        key = value.value if hasattr(value, "value") else str(value)
        lines.append(f"  {key}: {counts.get(value, 0)}")
    return lines


def format_report_lines(
    cases: list[DecisionCase],
    path: Path,
    total_records: int,
    diagnostics: DatasetDiagnostics,
) -> list[str]:
    lines = [f"Validation report for {path}", f"total cases: {total_records}"]

    category_counts = Counter(case.category for case in cases)
    lines.extend(format_count_section("category counts", category_counts, list(Category)))

    candidate_type_counts, write_type_counts = count_memory_types(cases)
    lines.extend(
        format_count_section(
            "memory type counts - candidate_memories",
            candidate_type_counts,
            list(MemoryType),
        )
    )
    lines.extend(
        format_count_section(
            "memory type counts - target.write_spans",
            write_type_counts,
            list(MemoryType),
        )
    )

    read_count = sum(len(case.target.read_hints) for case in cases)
    write_count = sum(len(case.target.write_spans) for case in cases)
    ignore_count = sum(len(case.target.ignore_spans) for case in cases)
    lines.append("target totals:")
    lines.append(f"  read_hints: {read_count}")
    lines.append(f"  write_spans: {write_count}")
    lines.append(f"  ignore_spans: {ignore_count}")

    lines.append(f"invalid read_hints: {len(diagnostics.invalid_read_hints)}")
    for error in diagnostics.invalid_read_hints:
        lines.append(f"  - {error}")

    lines.append(f"invalid spans: {len(diagnostics.invalid_spans)}")
    for error in diagnostics.invalid_spans:
        lines.append(f"  - {error}")

    lines.append(f"duplicate case_id: {len(diagnostics.duplicate_case_ids)}")
    for error in diagnostics.duplicate_case_ids:
        lines.append(f"  - {error}")

    lines.append(f"duplicate current_user_input: {len(diagnostics.duplicate_current_user_inputs)}")
    for error in diagnostics.duplicate_current_user_inputs:
        lines.append(f"  - {error}")

    lines.append(f"schema errors: {len(diagnostics.schema_errors)}")
    for error in diagnostics.schema_errors:
        lines.append(f"  - {error}")

    lines.append(f"invalid JSON records: {len(diagnostics.invalid_json)}")
    for error in diagnostics.invalid_json:
        lines.append(f"  - {error}")

    lines.append(f"category minimum errors: {len(diagnostics.category_minimum_errors)}")
    for error in diagnostics.category_minimum_errors:
        lines.append(f"  - {error}")

    return lines


def format_report(
    cases: list[DecisionCase],
    path: Path,
    total_records: int,
    diagnostics: DatasetDiagnostics,
) -> str:
    return "\n".join(format_report_lines(cases, path, total_records, diagnostics)) + "\n"


def print_report(
    cases: list[DecisionCase],
    path: Path,
    total_records: int,
    diagnostics: DatasetDiagnostics,
) -> None:
    print(format_report(cases, path, total_records, diagnostics), end="")


def validate_all(path: Path, min_per_category: int) -> tuple[list[DecisionCase], int, DatasetDiagnostics]:
    records, invalid_json = load_records(path)
    cases, schema_errors = load_cases(records)
    diagnostics = validate_dataset(cases, min_per_category=min_per_category)
    diagnostics.invalid_json = invalid_json
    diagnostics.schema_errors = schema_errors
    diagnostics.invalid_read_hints = collect_invalid_read_hints(records)
    diagnostics.invalid_spans = collect_invalid_spans(records)

    return cases, len(records) + len(invalid_json), diagnostics


def print_summary(cases: list[DecisionCase], path: Path) -> None:
    # Kept for compatibility with callers that imported this function during Day 1.
    print(f"Validated {len(cases)} cases from {path}")
    print("Category coverage:")
    for category in Category:
        count = sum(1 for case in cases if case.category == category)
        print(f"  {category.value}: {count}")

    read_count = sum(len(case.target.read_hints) for case in cases)
    write_count = sum(len(case.target.write_spans) for case in cases)
    ignore_count = sum(len(case.target.ignore_spans) for case in cases)
    print("Target totals:")
    print(f"  read_hints: {read_count}")
    print(f"  write_spans: {write_count}")
    print(f"  ignore_spans: {ignore_count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default="data/seed_examples.jsonl",
        help="JSONL decision-case file to validate.",
    )
    parser.add_argument(
        "--min-per-category",
        type=int,
        default=2,
        help="Minimum examples required per MVP category. Use 0 to disable.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    cases, total_records, diagnostics = validate_all(path, min_per_category=args.min_per_category)
    print_report(cases, path, total_records, diagnostics)

    errors = diagnostics.all_errors()
    if errors:
        print(f"Validation failed for {path}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
