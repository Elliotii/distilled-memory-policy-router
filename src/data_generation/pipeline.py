"""Offline generation pipeline utilities.

The pipeline is intentionally model-provider agnostic. Real API code should eventually
produce raw records, then reuse this module for path conventions, validation, invalid
sample isolation, metadata, and distribution reporting.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from src.schemas import Category, DecisionCase, MemoryType
from src.validation.validate_cases import format_report, validate_all


@dataclass(frozen=True)
class GenerationRunPaths:
    """Canonical output paths for one synthetic generation run."""

    run_dir: Path
    raw_cases: Path
    valid_cases: Path
    invalid_samples: Path
    metadata: Path
    validation_report: Path
    distribution_report: Path


@dataclass(frozen=True)
class GenerationRunResult:
    """Result summary for one offline generation run."""

    run_id: str
    paths: GenerationRunPaths
    requested_count: int
    raw_count: int
    valid_count: int
    invalid_count: int
    validation_passed: bool


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve_run_paths(output_root: Path, run_id: str) -> GenerationRunPaths:
    run_dir = output_root / run_id
    return GenerationRunPaths(
        run_dir=run_dir,
        raw_cases=run_dir / "raw_cases.jsonl",
        valid_cases=run_dir / "cases.jsonl",
        invalid_samples=run_dir / "invalid_samples.jsonl",
        metadata=run_dir / "metadata.json",
        validation_report=run_dir / "validation_report.txt",
        distribution_report=run_dir / "distribution_report.md",
    )


def write_jsonl(records: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(record, ensure_ascii=True) + "\n" for record in records)
    path.write_text(body, encoding="utf-8")


def write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def isolate_invalid_records(
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid_records: list[dict[str, Any]] = []
    invalid_records: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()
    seen_current_inputs: set[str] = set()

    for index, record in enumerate(records, start=1):
        try:
            case = DecisionCase.model_validate(record)
        except ValidationError as exc:
            invalid_records.append(
                {
                    "source_index": index,
                    "error_type": "schema_validation",
                    "error": str(exc),
                    "record": record,
                }
            )
            continue

        if case.case_id in seen_case_ids:
            invalid_records.append(
                {
                    "source_index": index,
                    "error_type": "duplicate_case_id",
                    "error": f"duplicate case_id: {case.case_id}",
                    "record": record,
                }
            )
            continue

        if case.current_user_input in seen_current_inputs:
            invalid_records.append(
                {
                    "source_index": index,
                    "error_type": "duplicate_current_user_input",
                    "error": "duplicate current_user_input",
                    "record": record,
                }
            )
            continue

        seen_case_ids.add(case.case_id)
        seen_current_inputs.add(case.current_user_input)
        valid_records.append(record)

    return valid_records, invalid_records


def _markdown_table(headers: list[str], rows: list[list[str | int | float]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def format_distribution_report(
    *,
    cases: list[DecisionCase],
    run_id: str,
    valid_cases_path: Path,
    invalid_count: int,
) -> str:
    category_counts = Counter(case.category for case in cases)
    candidate_type_counts = Counter(
        memory.type for case in cases for memory in case.candidate_memories
    )
    write_type_counts = Counter(
        write_span.type for case in cases for write_span in case.target.write_spans
    )
    read_total = sum(len(case.target.read_hints) for case in cases)
    write_total = sum(len(case.target.write_spans) for case in cases)
    ignore_total = sum(len(case.target.ignore_spans) for case in cases)
    cases_with_context = sum(1 for case in cases if case.recent_context)
    cases_with_candidates = sum(1 for case in cases if case.candidate_memories)

    lines = [
        f"# Distribution Report: {run_id}",
        "",
        f"Generated file: `{valid_cases_path}`",
        "",
        "Structural validation checks JSON shape, schema constraints, candidate ID references, exact span substrings, and duplicates. It does not prove semantic quality.",
        "",
        "## Summary",
        "",
    ]
    lines.extend(
        _markdown_table(
            ["metric", "value"],
            [
                ["valid_cases", len(cases)],
                ["invalid_samples", invalid_count],
                ["cases_with_recent_context", cases_with_context],
                ["cases_with_candidate_memories", cases_with_candidates],
                ["target.read_hints", read_total],
                ["target.write_spans", write_total],
                ["target.ignore_spans", ignore_total],
            ],
        )
    )
    lines.extend(["", "## Category Counts", ""])
    lines.extend(
        _markdown_table(
            ["category", "count"],
            [[category.value, category_counts.get(category, 0)] for category in Category],
        )
    )
    lines.extend(["", "## Candidate Memory Type Counts", ""])
    lines.extend(
        _markdown_table(
            ["memory_type", "count"],
            [[memory_type.value, candidate_type_counts.get(memory_type, 0)] for memory_type in MemoryType],
        )
    )
    lines.extend(["", "## Target Write Type Counts", ""])
    lines.extend(
        _markdown_table(
            ["memory_type", "count"],
            [[memory_type.value, write_type_counts.get(memory_type, 0)] for memory_type in MemoryType],
        )
    )
    lines.append("")
    return "\n".join(lines)


def run_generation_pipeline(
    *,
    records: list[dict[str, Any]],
    output_root: Path,
    run_id: str,
    metadata: dict[str, Any],
    min_per_category: int = 0,
) -> GenerationRunResult:
    paths = resolve_run_paths(output_root, run_id)
    paths.run_dir.mkdir(parents=True, exist_ok=True)

    valid_records, invalid_records = isolate_invalid_records(records)

    write_jsonl(records, paths.raw_cases)
    write_jsonl(valid_records, paths.valid_cases)
    write_jsonl(invalid_records, paths.invalid_samples)

    cases, total_records, diagnostics = validate_all(
        paths.valid_cases,
        min_per_category=min_per_category,
    )
    validation_text = format_report(cases, paths.valid_cases, total_records, diagnostics)
    paths.validation_report.write_text(validation_text, encoding="utf-8")

    distribution_text = format_distribution_report(
        cases=cases,
        run_id=run_id,
        valid_cases_path=paths.valid_cases,
        invalid_count=len(invalid_records),
    )
    paths.distribution_report.write_text(distribution_text, encoding="utf-8")

    validation_passed = not diagnostics.all_errors()
    final_metadata = {
        **metadata,
        "run_id": run_id,
        "generated_at_utc": utc_now_iso(),
        "requested_count": metadata.get("requested_count", len(records)),
        "raw_count": len(records),
        "valid_count": len(valid_records),
        "invalid_count": len(invalid_records),
        "validation_passed": validation_passed,
        "validation_scope": "structural_only",
        "semantic_quality_checked": False,
        "output_paths": {
            "raw_cases": str(paths.raw_cases),
            "valid_cases": str(paths.valid_cases),
            "invalid_samples": str(paths.invalid_samples),
            "validation_report": str(paths.validation_report),
            "distribution_report": str(paths.distribution_report),
        },
    }
    write_json(final_metadata, paths.metadata)

    return GenerationRunResult(
        run_id=run_id,
        paths=paths,
        requested_count=int(final_metadata["requested_count"]),
        raw_count=len(records),
        valid_count=len(valid_records),
        invalid_count=len(invalid_records),
        validation_passed=validation_passed,
    )
