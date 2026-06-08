#!/usr/bin/env python3
"""Summarize expanded hard READ v2 downstream internal rubric review rows."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
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

FLAG_KEYS = [
    "missing_required_fact",
    "irrelevant_contamination",
    "stale_or_contradictory_contamination",
    "hallucinated_memory",
    "citation_issue",
    "generic_no_memory",
    "strong_answer",
]

STRATEGY_ORDER = [
    "no_memory",
    "all_candidates",
    "budgeted_candidate_order",
    "keyword_top_k",
    "random_k",
    "oracle_selected",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 4) if values else 0.0


def validate_review(rows: list[dict[str, Any]]) -> None:
    if len(rows) != 48:
        raise ValueError(f"expected 48 review rows, found {len(rows)}")
    seen: set[str] = set()
    for row in rows:
        prompt_id = row.get("prompt_id")
        if not prompt_id:
            raise ValueError("review row missing prompt_id")
        if prompt_id in seen:
            raise ValueError(f"duplicate prompt_id: {prompt_id}")
        seen.add(prompt_id)

        for field in [
            "case_id",
            "strategy",
            "response_text",
            "injected_memory_ids",
            "cited_memory_ids",
            "auto_metrics",
            "manual_scores",
            "manual_utility",
            "review_flags",
            "review_notes",
        ]:
            if field not in row:
                raise ValueError(f"{prompt_id}: missing field {field}")

        scores = row["manual_scores"]
        if not isinstance(scores, dict):
            raise ValueError(f"{prompt_id}: manual_scores must be an object")
        for key in SCORE_KEYS:
            value = scores.get(key)
            if value not in (0, 1, 2):
                raise ValueError(f"{prompt_id}: {key} must be 0, 1, or 2; found {value!r}")
        expected_utility = sum(scores[key] for key in SCORE_KEYS)
        if row["manual_utility"] != expected_utility:
            raise ValueError(
                f"{prompt_id}: manual_utility={row['manual_utility']} "
                f"does not match score sum {expected_utility}"
            )

        flags = row["review_flags"]
        if not isinstance(flags, dict):
            raise ValueError(f"{prompt_id}: review_flags must be an object")
        for key in FLAG_KEYS:
            if not isinstance(flags.get(key), bool):
                raise ValueError(f"{prompt_id}: review flag {key} must be boolean")


def aggregate_rows(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(row)

    output: dict[str, Any] = {}
    for name in sorted(grouped):
        items = grouped[name]
        score_avgs = {
            f"avg_{score_key}": mean([float(row["manual_scores"][score_key]) for row in items])
            for score_key in SCORE_KEYS
        }
        flag_counts = {
            flag_key: sum(1 for row in items if row["review_flags"].get(flag_key))
            for flag_key in FLAG_KEYS
        }
        output[name] = {
            "count": len(items),
            "avg_manual_utility": mean([float(row["manual_utility"]) for row in items]),
            **score_avgs,
            "review_flag_counts": flag_counts,
        }
    return output


def attach_auto_metrics(
    strategy_summary: dict[str, Any], auto_scores: dict[str, Any]
) -> dict[str, Any]:
    auto_by_strategy = auto_scores.get("by_strategy", {})
    for strategy, summary in strategy_summary.items():
        if strategy in auto_by_strategy:
            summary["automatic_citation_metrics"] = auto_by_strategy[strategy]
    return strategy_summary


def select_examples(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any] | None]:
    def first(predicate: Any) -> dict[str, Any] | None:
        for row in rows:
            if predicate(row):
                return row
        return None

    def lowest_utility(predicate: Any) -> dict[str, Any] | None:
        matches = [row for row in rows if predicate(row)]
        if not matches:
            return None
        return sorted(matches, key=lambda row: (row["manual_utility"], row["prompt_id"]))[0]

    return {
        "strong_oracle_selected": first(
            lambda row: row["strategy"] == "oracle_selected"
            and row["review_flags"].get("strong_answer")
        ),
        "generic_no_memory": first(
            lambda row: row["strategy"] == "no_memory"
            and row["review_flags"].get("generic_no_memory")
        ),
        "all_candidates_contamination": lowest_utility(
            lambda row: row["strategy"] == "all_candidates"
            and (
                row["review_flags"].get("irrelevant_contamination")
                or row["review_flags"].get("stale_or_contradictory_contamination")
                or row["review_flags"].get("citation_issue")
            )
        ),
        "keyword_top_k_failure": lowest_utility(
            lambda row: row["strategy"] == "keyword_top_k"
            and (
                row["review_flags"].get("missing_required_fact")
                or row["review_flags"].get("stale_or_contradictory_contamination")
            )
        ),
        "random_k_failure": lowest_utility(
            lambda row: row["strategy"] == "random_k"
            and (
                row["review_flags"].get("missing_required_fact")
                or row["review_flags"].get("irrelevant_contamination")
                or row["review_flags"].get("stale_or_contradictory_contamination")
            )
        ),
        "budgeted_candidate_order_failure": lowest_utility(
            lambda row: row["strategy"] == "budgeted_candidate_order"
            and (
                row["review_flags"].get("missing_required_fact")
                or row["review_flags"].get("irrelevant_contamination")
                or row["review_flags"].get("stale_or_contradictory_contamination")
            )
        ),
    }


def fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" if i == 0 else "---:" for i in range(len(headers))) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(value) for value in row) + " |")
    return lines


def row_summary(row: dict[str, Any] | None) -> list[str]:
    if row is None:
        return ["No matching example found."]
    text = row["response_text"].strip().replace("\n", " ")
    if len(text) > 700:
        text = text[:697].rstrip() + "..."
    return [
        f"- Prompt: `{row['prompt_id']}`",
        f"- Utility: {row['manual_utility']}",
        f"- Notes: {row['review_notes']}",
        "",
        "```text",
        text,
        "```",
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    strategy_summary: dict[str, Any],
    case_summary: dict[str, Any],
    auto_scores: dict[str, Any],
    selection_metrics: dict[str, Any],
    examples: dict[str, dict[str, Any] | None],
) -> None:
    strategy_rows = []
    for strategy in STRATEGY_ORDER:
        if strategy not in strategy_summary:
            continue
        item = strategy_summary[strategy]
        flags = item["review_flag_counts"]
        auto = item.get("automatic_citation_metrics", {})
        strategy_rows.append(
            [
                f"`{strategy}`",
                item["count"],
                item["avg_manual_utility"],
                item["avg_required_fact_coverage"],
                item["avg_irrelevant_memory_contamination"],
                item["avg_stale_or_contradictory_use"],
                item["avg_task_response_quality"],
                item["avg_citation_compliance"],
                auto.get("e2e_required_citation_recall", ""),
                auto.get("avg_avoid_citations", ""),
                auto.get("avg_stale_citations", ""),
                auto.get("avg_contradictory_citations", ""),
                flags["strong_answer"],
                flags["missing_required_fact"],
                flags["irrelevant_contamination"],
                flags["stale_or_contradictory_contamination"],
            ]
        )

    case_rows = []
    for case_id in sorted(case_summary):
        item = case_summary[case_id]
        flags = item["review_flag_counts"]
        case_rows.append(
            [
                f"`{case_id}`",
                item["count"],
                item["avg_manual_utility"],
                item["avg_required_fact_coverage"],
                item["avg_irrelevant_memory_contamination"],
                item["avg_stale_or_contradictory_use"],
                item["avg_task_response_quality"],
                flags["strong_answer"],
                flags["missing_required_fact"],
            ]
        )

    selection = selection_metrics.get("aggregates", {})
    selection_rows = []
    for strategy in STRATEGY_ORDER:
        if strategy not in selection or strategy not in strategy_summary:
            continue
        sel = selection[strategy]
        man = strategy_summary[strategy]
        auto = man.get("automatic_citation_metrics", {})
        selection_rows.append(
            [
                f"`{strategy}`",
                sel.get("mean_post_required_recall", ""),
                sel.get("total_post_avoid_injected_count", ""),
                sel.get("total_post_stale_injected_count", ""),
                sel.get("total_post_contradictory_injected_count", ""),
                auto.get("e2e_required_citation_recall", ""),
                auto.get("avg_avoid_citations", ""),
                man["avg_manual_utility"],
            ]
        )

    lines = [
        "# Hard READ v2 Expanded Downstream Internal Rubric Review",
        "",
        "## Review Method",
        "",
        "This is an internal rubric review of 48 expanded v2 hard READ downstream DeepSeek V4 Flash responses. It is diagnostic only and should not be described as a human benchmark unless independently audited by the user.",
        "",
        "Each response was scored on six 0/1/2 fields: required fact coverage, irrelevant-memory contamination, stale or contradictory use, hallucinated memory use, task response quality, and citation compliance. `manual_utility` is the sum of those fields with a maximum of 12.",
        "",
        "## Strategy Aggregate",
        "",
        *table(
            [
                "Strategy",
                "Count",
                "Utility",
                "Req facts",
                "Irrelevant clean",
                "Stale/contrad clean",
                "Quality",
                "Citation",
                "Auto req recall",
                "Auto avoid avg",
                "Auto stale avg",
                "Auto contradictory avg",
                "Strong",
                "Missing req",
                "Irrelevant flags",
                "Stale/contrad flags",
            ],
            strategy_rows,
        ),
        "",
        "## Case Aggregate",
        "",
        *table(
            [
                "Case",
                "Count",
                "Utility",
                "Req facts",
                "Irrelevant clean",
                "Stale/contrad clean",
                "Quality",
                "Strong",
                "Missing req",
            ],
            case_rows,
        ),
        "",
        "## Selection-vs-Response Comparison",
        "",
        *table(
            [
                "Strategy",
                "Selection req recall",
                "Selection avoid injected",
                "Selection stale injected",
                "Selection contradictory injected",
                "Response req citation recall",
                "Response avoid citation avg",
                "Manual utility",
            ],
            selection_rows,
        ),
        "",
        "- The expanded fixture keeps the candidate-order artifact reduced at selection time: `budgeted_candidate_order` has low required recall while still injecting hard negatives.",
        "- The response review shows `no_memory` avoids contamination but repeatedly misses memory-only thresholds, validation commands, and blocking constraints.",
        "- `oracle_selected` is the clean upper-bound reference for this diagnostic: it has complete required-fact coverage and no hard-negative use in the reviewed subset.",
        "- `all_candidates` often recovers required facts, but it sometimes blends them with stale, contradictory, or unrelated instructions.",
        "- `keyword_top_k` and `random_k` expose hard-negative behavior; individual rows remain useful only when the selected set happens to include enough required evidence.",
        "",
        "## Automatic Citation Metrics Summary",
        "",
        f"- Prompt count: {auto_scores.get('prompt_count', 0)}.",
        f"- Response count: {auto_scores.get('response_count', 0)}.",
        f"- No-response count: {auto_scores.get('no_response_count', 0)}.",
        "- Citation formatting remained clean: hallucinated memory citations, current-unit citations, and bare memory references all averaged 0.00 across strategies.",
        "- Automatic metrics are citation diagnostics only; they do not judge whether the answer used the cited facts correctly.",
        "",
        "## Notable Examples",
        "",
        "### Strong oracle_selected response",
        "",
        *row_summary(examples["strong_oracle_selected"]),
        "",
        "### Generic or under-specified no_memory response",
        "",
        *row_summary(examples["generic_no_memory"]),
        "",
        "### all_candidates contamination example",
        "",
        *row_summary(examples["all_candidates_contamination"]),
        "",
        "### keyword_top_k failure example",
        "",
        *row_summary(examples["keyword_top_k_failure"]),
        "",
        "### random_k failure example",
        "",
        *row_summary(examples["random_k_failure"]),
        "",
        "### budgeted_candidate_order failure example",
        "",
        *row_summary(examples["budgeted_candidate_order_failure"]),
        "",
        "## Limitations",
        "",
        "- This is an internal rubric review, not a formal human benchmark.",
        "- The review covers a 48-response subset drawn from eight expanded v2 hard READ cases.",
        "- The review does not prove downstream utility.",
        "- The review does not evaluate learned router/live LoRA behavior.",
        "- The review does not establish production memory-system behavior.",
        "- The review does not support a claim that any routing approach is better than alternatives.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> dict[str, Any]:
    rows = load_jsonl(Path(args.review))
    validate_review(rows)
    auto_scores = load_json(Path(args.auto_scores))
    selection_metrics = load_json(Path(args.selection_metrics))

    strategy_summary = attach_auto_metrics(aggregate_rows(rows, "strategy"), auto_scores)
    case_summary = aggregate_rows(rows, "case_id")
    examples = select_examples(rows)

    output = {
        "review_method": "internal rubric review; diagnostic only; not a human benchmark unless independently audited",
        "row_count": len(rows),
        "score_keys": SCORE_KEYS,
        "flag_keys": FLAG_KEYS,
        "by_strategy": strategy_summary,
        "by_case": case_summary,
        "automatic_citation_metrics": {
            "prompt_count": auto_scores.get("prompt_count", 0),
            "response_count": auto_scores.get("response_count", 0),
            "no_response_count": auto_scores.get("no_response_count", 0),
            "by_strategy": auto_scores.get("by_strategy", {}),
        },
        "selection_metrics": selection_metrics,
        "notable_examples": {
            name: (row["prompt_id"] if row is not None else None)
            for name, row in examples.items()
        },
        "claim_boundary": (
            "Micro-pilot rubric diagnostics only; no downstream utility proof, "
            "no learned router/live LoRA behavior, no production memory-system claim."
        ),
    }

    Path(args.out_json).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(
        Path(args.out_md),
        rows,
        strategy_summary,
        case_summary,
        auto_scores,
        selection_metrics,
        examples,
    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", required=True)
    parser.add_argument("--auto-scores", required=True)
    parser.add_argument("--selection-metrics", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()
    output = run(args)
    print(json.dumps({"row_count": output["row_count"], "strategies": sorted(output["by_strategy"])}, sort_keys=True))


if __name__ == "__main__":
    main()
