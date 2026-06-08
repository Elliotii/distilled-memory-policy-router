#!/usr/bin/env python3
"""Summarize hard READ downstream internal rubric review rows."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List


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

JsonDict = Dict[str, object]


def load_jsonl(path: str) -> List[JsonDict]:
    rows: List[JsonDict] = []
    for line_no, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL") from exc
    return rows


def load_json(path: str) -> JsonDict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return round(statistics.fmean(values), 6) if values else 0.0


def validate_review(rows: List[JsonDict]) -> None:
    if len(rows) != 24:
        raise ValueError(f"expected 24 review rows, found {len(rows)}")
    seen = set()
    for row in rows:
        prompt_id = str(row.get("prompt_id"))
        if prompt_id in seen:
            raise ValueError(f"duplicate prompt_id: {prompt_id}")
        seen.add(prompt_id)
        scores = row.get("manual_scores")
        if not isinstance(scores, dict):
            raise ValueError(f"{prompt_id}: missing manual_scores object")
        for key in SCORE_KEYS:
            value = scores.get(key)
            if value not in [0, 1, 2]:
                raise ValueError(f"{prompt_id}: invalid {key}={value!r}")
        expected_utility = sum(int(scores[key]) for key in SCORE_KEYS)
        if row.get("manual_utility") != expected_utility:
            raise ValueError(f"{prompt_id}: manual_utility mismatch")
        flags = row.get("review_flags")
        if not isinstance(flags, dict):
            raise ValueError(f"{prompt_id}: missing review_flags object")
        for key in FLAG_KEYS:
            if flags.get(key) not in [True, False]:
                raise ValueError(f"{prompt_id}: invalid flag {key}={flags.get(key)!r}")


def aggregate_rows(rows: List[JsonDict], group_key: str) -> Dict[str, JsonDict]:
    grouped: Dict[str, List[JsonDict]] = defaultdict(list)
    for row in rows:
        grouped[str(row[group_key])].append(row)

    output: Dict[str, JsonDict] = {}
    for key in sorted(grouped):
        subset = grouped[key]
        flag_counts = Counter()
        for row in subset:
            flags = row["review_flags"]
            for flag in FLAG_KEYS:
                if flags.get(flag):
                    flag_counts[flag] += 1
        output[key] = {
            "count": len(subset),
            "avg_manual_utility": mean(float(row["manual_utility"]) for row in subset),
            **{
                f"avg_{score_key}": mean(
                    float(row["manual_scores"][score_key]) for row in subset
                )
                for score_key in SCORE_KEYS
            },
            "flag_counts": {flag: int(flag_counts[flag]) for flag in FLAG_KEYS},
        }
    return output


def pick_example(
    rows: List[JsonDict],
    *,
    strategy: str,
    flag: str | None = None,
    prefer_low_utility: bool = False,
) -> JsonDict | None:
    candidates = [row for row in rows if row["strategy"] == strategy]
    if flag is not None:
        candidates = [row for row in candidates if row["review_flags"].get(flag)]
    if not candidates:
        return None
    if prefer_low_utility:
        return sorted(candidates, key=lambda row: (int(row["manual_utility"]), str(row["prompt_id"])))[0]
    return sorted(candidates, key=lambda row: (-int(row["manual_utility"]), str(row["prompt_id"])))[0]


def quote_block(text: str) -> List[str]:
    return ["```text", text.strip(), "```"]


def write_markdown(path: str, summary: JsonDict, rows: List[JsonDict]) -> None:
    by_strategy = summary["by_strategy"]
    by_case = summary["by_case"]
    auto_by_strategy = summary["auto_by_strategy"]

    lines = [
        "# Hard READ Downstream Internal Rubric Review",
        "",
        "## Review Method",
        "",
        "This is an internal rubric review of the 24 DeepSeek responses collected for the hard READ downstream micro-pilot. It is useful for diagnosis, but it is not a formal benchmark and should not be described as a human evaluation.",
        "",
        "Each response was scored on six 0/1/2 dimensions: required fact coverage, irrelevant-memory contamination, stale or contradictory use, hallucinated memory use, task response quality, and citation compliance. `manual_utility` is the sum of those six fields.",
        "",
        "## Strategy Aggregates",
        "",
        "| Strategy | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Halluc clean | Quality | Citation | Auto req recall | Auto avoid avg | Auto stale avg | Auto contradictory avg | Strong | Missing req | Irrelevant flags | Stale/contrad flags |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for strategy, row in by_strategy.items():
        auto = auto_by_strategy.get(strategy, {})
        flags = row["flag_counts"]
        lines.append(
            f"| `{strategy}` | {row['count']} | {row['avg_manual_utility']:.2f} | "
            f"{row['avg_required_fact_coverage']:.2f} | "
            f"{row['avg_irrelevant_memory_contamination']:.2f} | "
            f"{row['avg_stale_or_contradictory_use']:.2f} | "
            f"{row['avg_hallucinated_memory_use']:.2f} | "
            f"{row['avg_task_response_quality']:.2f} | "
            f"{row['avg_citation_compliance']:.2f} | "
            f"{float(auto.get('e2e_required_citation_recall', 0.0)):.2f} | "
            f"{float(auto.get('avg_avoid_citations', 0.0)):.2f} | "
            f"{float(auto.get('avg_stale_citations', 0.0)):.2f} | "
            f"{float(auto.get('avg_contradictory_citations', 0.0)):.2f} | "
            f"{flags['strong_answer']} | {flags['missing_required_fact']} | "
            f"{flags['irrelevant_contamination']} | "
            f"{flags['stale_or_contradictory_contamination']} |"
        )

    lines.extend([
        "",
        "## Case Aggregates",
        "",
        "| Case | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Quality | Strong | Missing req |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for case_id, row in by_case.items():
        flags = row["flag_counts"]
        lines.append(
            f"| `{case_id}` | {row['count']} | {row['avg_manual_utility']:.2f} | "
            f"{row['avg_required_fact_coverage']:.2f} | "
            f"{row['avg_irrelevant_memory_contamination']:.2f} | "
            f"{row['avg_stale_or_contradictory_use']:.2f} | "
            f"{row['avg_task_response_quality']:.2f} | "
            f"{flags['strong_answer']} | {flags['missing_required_fact']} |"
        )

    lines.extend([
        "",
        "## Notable Observations",
        "",
        "- `oracle_selected` is the cleanest reference condition in this micro-pilot: it has full rubric utility and no contamination flags.",
        "- `budgeted_candidate_order` is strong on these four selected cases, but the selection report notes that candidate order is structured and should not be treated as a realistic retriever ranking.",
        "- `all_candidates` recovers required facts but exposes contamination risk by giving the answerer stale, contradictory, and irrelevant memories.",
        "- `keyword_top_k` shows the hard-negative failure mode most clearly: lexical overlap can retrieve stale or contradictory memories while missing required ones.",
        "- `no_memory` responses are usually clean but under-specified when important details live only in prior memory context.",
        "",
        "## Examples",
        "",
    ])
    examples = [
        ("Strong oracle_selected response", pick_example(rows, strategy="oracle_selected", flag="strong_answer")),
        (
            "All-candidates contamination example",
            pick_example(
                rows,
                strategy="all_candidates",
                flag="irrelevant_contamination",
                prefer_low_utility=True,
            ),
        ),
        (
            "Keyword top-k failure example",
            pick_example(
                rows,
                strategy="keyword_top_k",
                flag="missing_required_fact",
                prefer_low_utility=True,
            ),
        ),
        ("No-memory under-specified example", pick_example(rows, strategy="no_memory", flag="generic_no_memory")),
    ]
    for title, row in examples:
        if row is None:
            continue
        lines.extend([
            f"### {title}",
            "",
            f"- Prompt: `{row['prompt_id']}`",
            f"- Utility: {row['manual_utility']}",
            f"- Notes: {row['review_notes']}",
            "",
            *quote_block(str(row["response_text"])),
            "",
        ])

    lines.extend([
        "## Limitations",
        "",
        "- This is an internal rubric review, not a formal benchmark.",
        "- The review covers only 24 responses from four hard READ cases and six strategies.",
        "- The response review does not evaluate learned router/live LoRA behavior.",
        "- The review does not prove downstream utility or production safety.",
        "- The automatic citation metrics and internal rubric scores should be used as diagnostic evidence only.",
    ])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def summarize(review_path: str, auto_scores_path: str) -> JsonDict:
    rows = load_jsonl(review_path)
    validate_review(rows)
    auto_scores = load_json(auto_scores_path)
    return {
        "review_method": "internal rubric review; diagnostic, not a formal benchmark",
        "row_count": len(rows),
        "score_keys": SCORE_KEYS,
        "flag_keys": FLAG_KEYS,
        "by_strategy": aggregate_rows(rows, "strategy"),
        "by_case": aggregate_rows(rows, "case_id"),
        "auto_by_strategy": auto_scores.get("by_strategy", {}),
        "claim_boundary": "Internal rubric review only; no downstream utility proof or learned-router result.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize hard READ downstream review")
    parser.add_argument("--review", required=True)
    parser.add_argument("--auto-scores", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    summary = summarize(args.review, args.auto_scores)
    rows = load_jsonl(args.review)
    Path(args.out_json).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(args.out_md, summary, rows)
    print(json.dumps({
        "row_count": summary["row_count"],
        "strategy_count": len(summary["by_strategy"]),
        "case_count": len(summary["by_case"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
