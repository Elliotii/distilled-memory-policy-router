#!/usr/bin/env python3
"""Summarize learned_router manual review rows for hard READ v2 expanded subset."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path
from typing import Any


SCORE_KEYS = [
    "required_fact_coverage",
    "irrelevant_memory_contamination",
    "stale_or_contradictory_use",
    "hallucinated_memory_use",
    "task_response_quality",
    "citation_compliance",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def mean(values: list[float]) -> float:
    return round(statistics.fmean(values), 6) if values else 0.0


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(rows) != 8:
        raise ValueError(f"expected 8 learned_router review rows, got {len(rows)}")
    for row in rows:
        if row.get("strategy") != "learned_router":
            raise ValueError(f"unexpected strategy for {row.get('prompt_id')}: {row.get('strategy')}")
        expected_total = sum(int(row[key]) for key in SCORE_KEYS)
        if row.get("total_utility_score") != expected_total:
            raise ValueError(f"total mismatch for {row.get('prompt_id')}: {row.get('total_utility_score')} != {expected_total}")

    by_case = {
        row["case_id"]: {
            "prompt_id": row["prompt_id"],
            "total_utility_score": row["total_utility_score"],
            **{f"score_{key}": row[key] for key in SCORE_KEYS},
            "empty_response": bool(row.get("empty_response")),
            "usable_response": bool(row.get("usable_response")),
            "cited_memory_ids": row.get("cited_memory_ids", []),
            "rationale": row.get("brief_rationale", ""),
        }
        for row in rows
    }
    review_flag_counts = {
        "missing_required_fact": sum(1 for row in rows if row["required_fact_coverage"] < 2),
        "material_contamination": sum(1 for row in rows if row["irrelevant_memory_contamination"] == 0),
        "stale_or_contradictory_material_use": sum(1 for row in rows if row["stale_or_contradictory_use"] == 0),
        "hallucinated_memory": sum(1 for row in rows if row["hallucinated_memory_use"] < 2),
        "citation_issue": sum(1 for row in rows if row["citation_compliance"] < 2),
        "strong_answer": sum(1 for row in rows if row["total_utility_score"] == 12),
        "no_response": sum(1 for row in rows if row.get("empty_response") or not row.get("usable_response")),
    }
    by_strategy = {
        "learned_router": {
            "count": len(rows),
            "avg_manual_utility": mean([float(row["total_utility_score"]) for row in rows]),
            "avg_required_fact_coverage": mean([float(row["required_fact_coverage"]) for row in rows]),
            "avg_irrelevant_memory_contamination": mean([float(row["irrelevant_memory_contamination"]) for row in rows]),
            "avg_stale_or_contradictory_use": mean([float(row["stale_or_contradictory_use"]) for row in rows]),
            "avg_hallucinated_memory_use": mean([float(row["hallucinated_memory_use"]) for row in rows]),
            "avg_task_response_quality": mean([float(row["task_response_quality"]) for row in rows]),
            "avg_citation_compliance": mean([float(row["citation_compliance"]) for row in rows]),
            "missing_required_count": review_flag_counts["missing_required_fact"],
            "material_contamination_count": review_flag_counts["material_contamination"],
            "stale_or_contradictory_material_use_count": review_flag_counts["stale_or_contradictory_material_use"],
            "no_response_count": review_flag_counts["no_response"],
            "review_flag_counts": review_flag_counts,
        }
    }
    return {
        "review_method": "Internal manual rubric review of 8 learned_router downstream responses.",
        "row_count": len(rows),
        "score_keys": SCORE_KEYS,
        "by_strategy": by_strategy,
        "by_case": by_case,
        "claim_boundary": "Eight-case manual rubric diagnostic only; not general downstream utility proof.",
    }


def write_report(path: Path, summary: dict[str, Any]) -> None:
    strat = summary["by_strategy"]["learned_router"]
    lines = [
        "# Learned-Router Manual Review Report",
        "",
        "This is an internal rubric review of the 8 learned_router downstream responses. It uses the same 0/1/2 rubric dimensions as the existing expanded downstream subset review.",
        "",
        "## Aggregate",
        "",
        "| Strategy | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Hallucination clean | Quality | Citation | Missing req | Material contamination | Stale/contrad material | No response |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| `learned_router` | {strat['count']} | {strat['avg_manual_utility']:.2f} | "
            f"{strat['avg_required_fact_coverage']:.2f} | {strat['avg_irrelevant_memory_contamination']:.2f} | "
            f"{strat['avg_stale_or_contradictory_use']:.2f} | {strat['avg_hallucinated_memory_use']:.2f} | "
            f"{strat['avg_task_response_quality']:.2f} | {strat['avg_citation_compliance']:.2f} | "
            f"{strat['missing_required_count']} | {strat['material_contamination_count']} | "
            f"{strat['stale_or_contradictory_material_use_count']} | {strat['no_response_count']} |"
        ),
        "",
        "## Case Notes",
        "",
        "| Case | Utility | Empty | Rationale |",
        "| --- | ---: | --- | --- |",
    ]
    for case_id, row in summary["by_case"].items():
        lines.append(
            f"| `{case_id}` | {row['total_utility_score']} | {str(row['empty_response']).lower()} | {row['rationale']} |"
        )
    lines.extend([
        "",
        "## Boundary",
        "",
        "This report does not call APIs, rerun responses, or prove general downstream utility. It is a small diagnostic rubric review.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-jsonl", required=True)
    parser.add_argument("--out-summary", required=True)
    parser.add_argument("--out-report", required=True)
    args = parser.parse_args()

    rows = load_jsonl(Path(args.review_jsonl))
    summary = summarize(rows)
    Path(args.out_summary).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(Path(args.out_report), summary)
    print(json.dumps({"rows": summary["row_count"], "utility": summary["by_strategy"]["learned_router"]["avg_manual_utility"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
