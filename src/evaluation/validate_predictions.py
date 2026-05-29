"""Validate parsed prediction JSONL files against the evaluation contract."""

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

from src.schemas import RouterTarget
from src.validation.validate_cases import load_records


ALLOWED_OPTIONAL_KEYS = {"run_id", "model_id", "raw_output", "parse_error"}
REQUIRED_KEYS = {"case_id", "target"}


@dataclass
class PredictionDiagnostics:
    invalid_json: list[str] = field(default_factory=list)
    invalid_shape: list[str] = field(default_factory=list)
    invalid_target_schema: list[str] = field(default_factory=list)
    unknown_case_ids: list[str] = field(default_factory=list)
    duplicate_case_ids: list[str] = field(default_factory=list)
    missing_case_ids: list[str] = field(default_factory=list)
    invalid_read_hints: list[str] = field(default_factory=list)
    invalid_spans: list[str] = field(default_factory=list)

    def all_errors(self) -> list[str]:
        return [
            *self.invalid_json,
            *self.invalid_shape,
            *self.invalid_target_schema,
            *self.unknown_case_ids,
            *self.duplicate_case_ids,
            *self.missing_case_ids,
            *self.invalid_read_hints,
            *self.invalid_spans,
        ]


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
                errors.append(f"line {line_number}: prediction must be a JSON object")
                continue
            rows.append(row)
    return rows, errors


def load_gold_cases(path: Path) -> dict[str, dict[str, Any]]:
    records, invalid_json = load_records(path)
    if invalid_json:
        raise ValueError(f"gold file has invalid JSON records: {invalid_json[:3]}")
    cases: dict[str, dict[str, Any]] = {}
    for record in records:
        case_id = record.payload.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"gold record on line {record.line_number} is missing case_id")
        if case_id in cases:
            raise ValueError(f"gold file contains duplicate case_id: {case_id}")
        cases[case_id] = record.payload
    return cases


def validate_predictions(
    prediction_rows: list[dict[str, Any]],
    gold_cases: dict[str, dict[str, Any]],
    *,
    require_complete: bool,
    strict_case_constraints: bool,
) -> PredictionDiagnostics:
    diagnostics = PredictionDiagnostics()

    case_ids: list[str] = []
    for row_index, row in enumerate(prediction_rows, start=1):
        keys = set(row)
        missing_keys = REQUIRED_KEYS - keys
        extra_keys = keys - REQUIRED_KEYS - ALLOWED_OPTIONAL_KEYS
        if missing_keys:
            diagnostics.invalid_shape.append(
                f"row {row_index}: missing required keys {sorted(missing_keys)}"
            )
            continue
        if extra_keys:
            diagnostics.invalid_shape.append(
                f"row {row_index}: unexpected keys {sorted(extra_keys)}"
            )

        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            diagnostics.invalid_shape.append(f"row {row_index}: case_id must be a non-empty string")
            continue
        case_ids.append(case_id)

        gold_case = gold_cases.get(case_id)
        if gold_case is None:
            diagnostics.unknown_case_ids.append(f"row {row_index}: unknown case_id {case_id!r}")

        target = row.get("target")
        if not isinstance(target, dict):
            diagnostics.invalid_shape.append(f"{case_id}: target must be an object")
            continue
        try:
            RouterTarget.model_validate(target)
        except ValidationError as exc:
            diagnostics.invalid_target_schema.append(f"{case_id}: target schema failed: {exc}")
            continue

        if strict_case_constraints and gold_case is not None:
            candidate_ids = {
                memory.get("id")
                for memory in gold_case.get("candidate_memories", [])
                if isinstance(memory, dict)
            }
            for memory_id in target.get("read_hints", []):
                if memory_id not in candidate_ids:
                    diagnostics.invalid_read_hints.append(
                        f"{case_id}: read_hints reference missing candidate {memory_id!r}"
                    )

            current_user_input = gold_case.get("current_user_input", "")
            for index, write_span in enumerate(target.get("write_spans", [])):
                span = write_span.get("span") if isinstance(write_span, dict) else None
                if not isinstance(span, str) or span not in current_user_input:
                    diagnostics.invalid_spans.append(
                        f"{case_id}: write_spans[{index}].span is not an exact input substring: {span!r}"
                    )
            for index, span in enumerate(target.get("ignore_spans", [])):
                if not isinstance(span, str) or span not in current_user_input:
                    diagnostics.invalid_spans.append(
                        f"{case_id}: ignore_spans[{index}] is not an exact input substring: {span!r}"
                    )

    duplicate_case_ids = sorted(
        case_id for case_id, count in Counter(case_ids).items() if count > 1
    )
    diagnostics.duplicate_case_ids = [
        f"duplicate prediction case_id: {case_id}" for case_id in duplicate_case_ids
    ]

    if require_complete:
        predicted = set(case_ids)
        missing = sorted(set(gold_cases) - predicted)
        diagnostics.missing_case_ids = [
            f"missing prediction for case_id: {case_id}" for case_id in missing
        ]

    return diagnostics


def format_report(
    *,
    gold_path: Path,
    prediction_path: Path,
    gold_count: int,
    prediction_count: int,
    diagnostics: PredictionDiagnostics,
) -> str:
    lines = [
        f"Prediction validation report for {prediction_path}",
        f"gold file: {gold_path}",
        f"gold cases: {gold_count}",
        f"prediction rows: {prediction_count}",
        f"invalid JSON records: {len(diagnostics.invalid_json)}",
        f"invalid shape: {len(diagnostics.invalid_shape)}",
        f"invalid target schema: {len(diagnostics.invalid_target_schema)}",
        f"unknown case_id: {len(diagnostics.unknown_case_ids)}",
        f"duplicate case_id: {len(diagnostics.duplicate_case_ids)}",
        f"missing case_id: {len(diagnostics.missing_case_ids)}",
        f"invalid read_hints: {len(diagnostics.invalid_read_hints)}",
        f"invalid spans: {len(diagnostics.invalid_spans)}",
    ]
    for error in diagnostics.all_errors():
        lines.append(f"  - {error}")
    if not diagnostics.all_errors():
        lines.append("All checks passed.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Do not require predictions for every gold case.",
    )
    parser.add_argument(
        "--no-strict-case-constraints",
        action="store_true",
        help="Skip read_hint and span checks against the selected gold/dev cases.",
    )
    args = parser.parse_args()

    gold_cases = load_gold_cases(args.gold)
    prediction_rows, invalid_json = load_jsonl(args.predictions)
    diagnostics = validate_predictions(
        prediction_rows,
        gold_cases,
        require_complete=not args.allow_partial,
        strict_case_constraints=not args.no_strict_case_constraints,
    )
    diagnostics.invalid_json = invalid_json

    report = format_report(
        gold_path=args.gold,
        prediction_path=args.predictions,
        gold_count=len(gold_cases),
        prediction_count=len(prediction_rows),
        diagnostics=diagnostics,
    )
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    print(report, end="")
    return 1 if diagnostics.all_errors() else 0


if __name__ == "__main__":
    raise SystemExit(main())
