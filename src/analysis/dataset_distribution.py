"""Generate structural distribution and gap reports for decision-case JSONL files."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.schemas import Category, DecisionCase, MemoryType
from src.validation.validate_cases import validate_all


CATEGORY_TARGET_PCT: dict[Category, float] = {
    Category.SIMPLE_WRITE: 0.10,
    Category.MULTI_WRITE: 0.12,
    Category.READ_RELEVANT_MEMORY: 0.12,
    Category.IGNORE_NOISE: 0.12,
    Category.CORRECTION_OR_REVISION: 0.12,
    Category.CONTEXT_DEPENDENT_REFERENCE: 0.10,
    Category.CONFLICTING_MEMORY: 0.10,
    Category.MIXED_WRITE_AND_IGNORE: 0.08,
    Category.NO_ACTION_NEEDED: 0.08,
    Category.DISTRACTOR_MEMORY_SELECTION: 0.06,
}

WRITE_TYPE_TARGET_RANGES: dict[MemoryType, tuple[float, float]] = {
    MemoryType.SOP: (0.10, 0.15),
    MemoryType.FACT: (0.25, 0.30),
    MemoryType.DECISION: (0.30, 0.35),
    MemoryType.TASK_STATE: (0.20, 0.25),
}

CASE_RATE_TARGET_RANGES: dict[str, tuple[float, float]] = {
    "cases_with_ignore_spans": (0.25, 0.35),
    "cases_with_candidate_memories": (0.50, 0.70),
    "cases_with_recent_context": (0.25, 0.40),
    "cases_with_5_to_8_candidate_memories": (0.15, 0.25),
}


@dataclass(frozen=True)
class DatasetSpec:
    label: str
    path: Path


@dataclass(frozen=True)
class DatasetSummary:
    label: str
    path: Path
    cases: list[DecisionCase]
    category_counts: Counter[Category]
    candidate_type_counts: Counter[MemoryType]
    write_type_counts: Counter[MemoryType]
    read_hints_total: int
    write_spans_total: int
    ignore_spans_total: int
    cases_with_ignore_spans: int
    cases_with_candidate_memories: int
    cases_with_recent_context: int
    cases_with_5_to_8_candidate_memories: int


def parse_dataset_spec(raw: str) -> DatasetSpec:
    if ":" not in raw:
        raise ValueError("--dataset must use label:path format")
    label, path = raw.split(":", 1)
    label = label.strip()
    if not label:
        raise ValueError("dataset label must not be empty")
    return DatasetSpec(label=label, path=Path(path))


def summarize_dataset(spec: DatasetSpec, min_per_category: int) -> DatasetSummary:
    cases, total_records, diagnostics = validate_all(
        spec.path,
        min_per_category=min_per_category,
    )
    errors = diagnostics.all_errors()
    if errors:
        error_text = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"{spec.path} failed structural validation:\n{error_text}")
    if total_records != len(cases):
        raise ValueError(f"{spec.path} has {total_records} records but {len(cases)} valid cases")

    return DatasetSummary(
        label=spec.label,
        path=spec.path,
        cases=cases,
        category_counts=Counter(case.category for case in cases),
        candidate_type_counts=Counter(
            memory.type for case in cases for memory in case.candidate_memories
        ),
        write_type_counts=Counter(
            write_span.type for case in cases for write_span in case.target.write_spans
        ),
        read_hints_total=sum(len(case.target.read_hints) for case in cases),
        write_spans_total=sum(len(case.target.write_spans) for case in cases),
        ignore_spans_total=sum(len(case.target.ignore_spans) for case in cases),
        cases_with_ignore_spans=sum(1 for case in cases if case.target.ignore_spans),
        cases_with_candidate_memories=sum(1 for case in cases if case.candidate_memories),
        cases_with_recent_context=sum(1 for case in cases if case.recent_context),
        cases_with_5_to_8_candidate_memories=sum(
            1 for case in cases if 5 <= len(case.candidate_memories) <= 8
        ),
    )


def pct(value: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{(value / total) * 100:.1f}%"


def range_status(value: float, lower: float, upper: float) -> str:
    if value < lower:
        return "below_target"
    if value > upper:
        return "above_target"
    return "in_range"


def markdown_table(headers: list[str], rows: list[list[str | int]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def add_summary_section(lines: list[str], summary: DatasetSummary) -> None:
    total_cases = len(summary.cases)
    total_candidate_memories = sum(summary.candidate_type_counts.values())
    total_write_spans = sum(summary.write_type_counts.values())
    category_rows: list[list[str | int]] = []
    for category in Category:
        actual_count = summary.category_counts.get(category, 0)
        target_count = CATEGORY_TARGET_PCT[category] * total_cases
        category_rows.append(
            [
                category.value,
                actual_count,
                pct(actual_count, total_cases),
                f"{CATEGORY_TARGET_PCT[category] * 100:.1f}%",
                f"{actual_count - target_count:+.1f}",
            ]
        )

    lines.extend(
        [
            f"## Dataset: {summary.label}",
            "",
            f"File: `{summary.path}`",
            "",
            "### Summary",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            ["metric", "count", "rate"],
            [
                ["total_cases", total_cases, "100.0%"],
                [
                    "cases_with_candidate_memories",
                    summary.cases_with_candidate_memories,
                    pct(summary.cases_with_candidate_memories, total_cases),
                ],
                [
                    "cases_with_recent_context",
                    summary.cases_with_recent_context,
                    pct(summary.cases_with_recent_context, total_cases),
                ],
                [
                    "cases_with_ignore_spans",
                    summary.cases_with_ignore_spans,
                    pct(summary.cases_with_ignore_spans, total_cases),
                ],
                [
                    "cases_with_5_to_8_candidate_memories",
                    summary.cases_with_5_to_8_candidate_memories,
                    pct(summary.cases_with_5_to_8_candidate_memories, total_cases),
                ],
                ["target.read_hints", summary.read_hints_total, ""],
                ["target.write_spans", summary.write_spans_total, ""],
                ["target.ignore_spans", summary.ignore_spans_total, ""],
            ],
        )
    )

    lines.extend(["", "### Category Distribution", ""])
    lines.extend(
        markdown_table(
            ["category", "count", "actual_rate", "mvp_target_rate", "delta_vs_target_count"],
            category_rows,
        )
    )

    lines.extend(["", "### Candidate Memory Type Distribution", ""])
    candidate_type_rows: list[list[str | int]] = []
    for memory_type in MemoryType:
        count = summary.candidate_type_counts.get(memory_type, 0)
        candidate_type_rows.append(
            [
                memory_type.value,
                count,
                pct(count, total_candidate_memories),
            ]
        )
    lines.extend(
        markdown_table(
            ["memory_type", "count", "rate"],
            candidate_type_rows,
        )
    )

    lines.extend(["", "### Target Write Type Distribution", ""])
    lines.extend(
        markdown_table(
            ["memory_type", "count", "actual_rate", "target_range", "status"],
            [
                write_type_row(summary, memory_type, total_write_spans)
                for memory_type in MemoryType
            ],
        )
    )

    lines.extend(["", "### Case-Rate Targets", ""])
    lines.extend(
        markdown_table(
            ["metric", "count", "actual_rate", "target_range", "status"],
            [
                case_rate_row(summary, "cases_with_ignore_spans", total_cases),
                case_rate_row(summary, "cases_with_candidate_memories", total_cases),
                case_rate_row(summary, "cases_with_recent_context", total_cases),
                case_rate_row(summary, "cases_with_5_to_8_candidate_memories", total_cases),
            ],
        )
    )
    lines.append("")


def write_type_row(
    summary: DatasetSummary,
    memory_type: MemoryType,
    total_write_spans: int,
) -> list[str | int]:
    count = summary.write_type_counts.get(memory_type, 0)
    lower, upper = WRITE_TYPE_TARGET_RANGES[memory_type]
    actual = count / total_write_spans if total_write_spans else 0.0
    return [
        memory_type.value,
        count,
        pct(count, total_write_spans),
        f"{lower * 100:.0f}-{upper * 100:.0f}%",
        range_status(actual, lower, upper),
    ]


def case_rate_row(
    summary: DatasetSummary,
    metric: str,
    total_cases: int,
) -> list[str | int]:
    count = getattr(summary, metric)
    lower, upper = CASE_RATE_TARGET_RANGES[metric]
    actual = count / total_cases if total_cases else 0.0
    return [
        metric,
        count,
        pct(count, total_cases),
        f"{lower * 100:.0f}-{upper * 100:.0f}%",
        range_status(actual, lower, upper),
    ]


def add_combined_recommendations(lines: list[str], summaries: list[DatasetSummary]) -> None:
    lines.extend(["## Recommended Next Generation Bias", ""])
    lines.extend(
        [
            "- Keep category sampling close to the MVP distribution from the project spec.",
            "- Increase `task_state` writes and task-state candidate memories.",
            (
                "- Increase `fact` writes in seed-like human examples; avoid drifting "
                "back to SOP-heavy data."
            ),
            (
                "- Keep `sop` valid but rare unless the user explicitly states a "
                "durable workflow rule."
            ),
            (
                "- Generate more recent-context cases, especially context-dependent "
                "references and corrections."
            ),
            "- Generate more cases with 5-8 candidate memories to stress read selection.",
            "- Raise ignore-span coverage, but keep ignores selective rather than exhaustive.",
            (
                "- Treat mock data as pipeline smoke-test material only; do not train "
                "or evaluate on it."
            ),
            "",
        ]
    )

    if summaries:
        lines.extend(["### Dataset-Specific Notes", ""])
        for summary in summaries:
            total_write_spans = sum(summary.write_type_counts.values())
            task_state_writes = summary.write_type_counts.get(MemoryType.TASK_STATE, 0)
            sop_writes = summary.write_type_counts.get(MemoryType.SOP, 0)
            recent_context_rate = summary.cases_with_recent_context / len(summary.cases)
            heavy_candidate_rate = (
                summary.cases_with_5_to_8_candidate_memories / len(summary.cases)
            )

            notes: list[str] = []
            if total_write_spans and task_state_writes / total_write_spans < 0.20:
                notes.append("add more task_state write targets")
            if total_write_spans and sop_writes / total_write_spans > 0.15:
                notes.append("reduce generic sop write targets")
            if recent_context_rate < 0.25:
                notes.append("add more recent_context cases")
            if heavy_candidate_rate < 0.15:
                notes.append("add more 5-8 candidate-memory cases")
            if not notes:
                notes.append("distribution is within the current structural targets")
            lines.append(f"- `{summary.label}`: " + "; ".join(notes) + ".")
        lines.append("")


def format_report(summaries: list[DatasetSummary]) -> str:
    lines = [
        "# Day 3 Dataset Distribution Gap Report",
        "",
        (
            "This report is structural analysis only. It checks validated JSONL "
            "records, category balance, memory-type distribution, context/candidate "
            "coverage, and target-field counts. It does not prove semantic label quality."
        ),
        "",
        (
            "The target ranges come from the project spec and the Day 2 generation "
            "strategy. They are planning targets for the next synthetic generation "
            "round, not hard validator rules."
        ),
        "",
    ]

    for summary in summaries:
        add_summary_section(lines, summary)

    add_combined_recommendations(lines, summaries)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        action="append",
        required=True,
        help="Dataset in label:path format. May be supplied multiple times.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional Markdown report output path. Prints to stdout when omitted.",
    )
    parser.add_argument(
        "--min-per-category",
        type=int,
        default=0,
        help="Minimum per category for structural validation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    specs = [parse_dataset_spec(raw) for raw in args.dataset]
    summaries = [
        summarize_dataset(spec, min_per_category=args.min_per_category)
        for spec in specs
    ]
    report = format_report(summaries)

    if args.output is None:
        print(report)
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote distribution gap report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
