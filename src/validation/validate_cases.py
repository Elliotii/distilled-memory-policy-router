"""Validate memory policy router JSONL decision cases."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pydantic import ValidationError

from src.schemas import REQUIRED_CATEGORIES, Category, DecisionCase


def load_cases(path: Path) -> tuple[list[DecisionCase], list[str]]:
    cases: list[DecisionCase] = []
    errors: list[str] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue

            try:
                payload: Any = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc}")
                continue

            try:
                cases.append(DecisionCase.model_validate(payload))
            except ValidationError as exc:
                errors.append(f"line {line_number}: schema validation failed: {exc}")

    return cases, errors


def validate_dataset(cases: list[DecisionCase], min_per_category: int) -> list[str]:
    errors: list[str] = []

    case_ids = [case.case_id for case in cases]
    duplicate_case_ids = sorted(
        case_id for case_id, count in Counter(case_ids).items() if count > 1
    )
    if duplicate_case_ids:
        errors.append(f"duplicate case_id values: {duplicate_case_ids}")

    inputs = [case.current_user_input for case in cases]
    duplicate_inputs = sorted(text for text, count in Counter(inputs).items() if count > 1)
    if duplicate_inputs:
        errors.append(f"duplicate current_user_input values: {duplicate_inputs}")

    if min_per_category > 0:
        category_counts = Counter(case.category for case in cases)
        for category in REQUIRED_CATEGORIES:
            count = category_counts.get(category, 0)
            if count < min_per_category:
                errors.append(
                    f"category {category.value!r} has {count} cases; "
                    f"expected at least {min_per_category}"
                )

    return errors


def print_summary(cases: list[DecisionCase], path: Path) -> None:
    print(f"Validated {len(cases)} cases from {path}")
    print("Category coverage:")
    for category in Category:
        count = sum(1 for case in cases if case.category == category)
        print(f"  {category.value}: {count}")

    read_count = sum(len(case.expected_output.read_hints) for case in cases)
    write_count = sum(len(case.expected_output.write_spans) for case in cases)
    ignore_count = sum(len(case.expected_output.ignore_spans) for case in cases)
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

    cases, errors = load_cases(path)
    errors.extend(validate_dataset(cases, min_per_category=args.min_per_category))

    if errors:
        print(f"Validation failed for {path}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print_summary(cases, path)
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
