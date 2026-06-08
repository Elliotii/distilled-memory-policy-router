#!/usr/bin/env python3
"""Score citation traces for LLM downstream-lite responses.

This script computes partial automatic citation metrics only. It does not judge
task response quality, answer usefulness, or uncited hallucinations.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


MEMORY_CITATION_RE = re.compile(r"\[(m\d+)\]", re.IGNORECASE)
CURRENT_UNIT_CITATION_RE = re.compile(r"\[(u\d+)\]", re.IGNORECASE)
BARE_MEMORY_RE = re.compile(r"(?<![\[\w])(m\d+)(?![\]\w])", re.IGNORECASE)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number} is not a JSON object")
            rows.append(row)
    return rows


def stable_strings(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if isinstance(value, str):
            normalized = value.lower()
            if normalized not in seen:
                seen.add(normalized)
                result.append(normalized)
    return result


def extract_citations(text: Any) -> list[str]:
    if not isinstance(text, str):
        return []
    seen: set[str] = set()
    citations: list[str] = []
    for match in MEMORY_CITATION_RE.findall(text):
        memory_id = match.lower()
        if memory_id not in seen:
            seen.add(memory_id)
            citations.append(memory_id)
    return citations


def extract_current_unit_citations(text: Any) -> list[str]:
    if not isinstance(text, str):
        return []
    seen: set[str] = set()
    citations: list[str] = []
    for match in CURRENT_UNIT_CITATION_RE.findall(text):
        unit_id = match.lower()
        if unit_id not in seen:
            seen.add(unit_id)
            citations.append(unit_id)
    return citations


def extract_bare_memory_references(text: Any) -> list[str]:
    if not isinstance(text, str):
        return []
    seen: set[str] = set()
    references: list[str] = []
    for match in BARE_MEMORY_RE.findall(text):
        memory_id = match.lower()
        if memory_id not in seen:
            seen.add(memory_id)
            references.append(memory_id)
    return references


def safe_recall(count: int, total: int) -> float | None:
    if total == 0:
        return None
    return count / total


def average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def score_response(prompt: dict[str, Any], response: dict[str, Any] | None) -> dict[str, Any]:
    response_text = response.get("response_text", "") if response else ""
    cited = extract_citations(response_text)
    invalid_current_units = extract_current_unit_citations(response_text)
    bare_memory_refs = extract_bare_memory_references(response_text)
    cited_set = set(cited)
    required = set(stable_strings(prompt.get("expected_required_memory_ids")))
    avoid = set(stable_strings(prompt.get("expected_avoid_memory_ids")))
    injected = set(stable_strings(prompt.get("injected_memory_ids")))
    injected_required = required.intersection(injected)
    required_cited = required.intersection(cited_set)
    injected_required_cited = injected_required.intersection(cited_set)
    hallucinated = cited_set - injected
    irrelevant = cited_set.intersection(avoid)
    no_response = not isinstance(response_text, str) or not response_text.strip()

    return {
        "prompt_id": prompt["prompt_id"],
        "case_id": prompt["case_id"],
        "strategy": prompt["strategy"],
        "cited_memory_ids": cited,
        "invalid_current_unit_citations": invalid_current_units,
        "bare_memory_references": bare_memory_refs,
        "required_cited_count": len(required_cited),
        "required_total_count": len(required),
        "end_to_end_required_citation_recall": safe_recall(len(required_cited), len(required)),
        "conditional_required_citation_recall": safe_recall(len(injected_required_cited), len(injected_required)),
        "conditional_required_total_count": len(injected_required),
        "irrelevant_citation_count": len(irrelevant),
        "hallucinated_citation_count": len(hallucinated),
        "invalid_current_unit_citation_count": len(invalid_current_units),
        "bare_memory_reference_count": len(bare_memory_refs),
        "citation_format_violation_count": len(invalid_current_units) + len(bare_memory_refs),
        "irrelevant_citations": sorted(irrelevant),
        "hallucinated_citations": sorted(hallucinated),
        "missing_required_citations": sorted(required - cited_set),
        "no_response_count": 1 if no_response else 0,
    }


def aggregate_by_strategy(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["strategy"]].append(row)

    aggregates: dict[str, dict[str, Any]] = {}
    for strategy, items in sorted(grouped.items()):
        end_to_end_values = [
            item["end_to_end_required_citation_recall"]
            for item in items
            if item["end_to_end_required_citation_recall"] is not None
        ]
        conditional_values = [
            item["conditional_required_citation_recall"]
            for item in items
            if item["conditional_required_citation_recall"] is not None
        ]
        no_response_count = sum(item["no_response_count"] for item in items)
        prompts = len(items)
        aggregates[strategy] = {
            "prompts": prompts,
            "avg_end_to_end_required_citation_recall": average(end_to_end_values),
            "avg_conditional_required_citation_recall": average(conditional_values),
            "avg_irrelevant_citation_count": average([item["irrelevant_citation_count"] for item in items]),
            "avg_hallucinated_citation_count": average([item["hallucinated_citation_count"] for item in items]),
            "avg_invalid_current_unit_citation_count": average([item["invalid_current_unit_citation_count"] for item in items]),
            "avg_bare_memory_reference_count": average([item["bare_memory_reference_count"] for item in items]),
            "avg_citation_format_violation_count": average([item["citation_format_violation_count"] for item in items]),
            "no_response_count": no_response_count,
            "response_coverage": 0.0 if prompts == 0 else (prompts - no_response_count) / prompts,
        }
    return aggregates


def format_float(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def build_markdown(results: dict[str, Any]) -> str:
    lines = [
        "# LLM Downstream-Lite Pilot Scores",
        "",
        "These are partial automatic citation metrics. They do not judge task response quality, answer usefulness, contradiction handling, or uncited hallucinations.",
        "",
        "## Summary",
        "",
        f"- Prompt rows: {results['prompt_count']}",
        f"- Response rows: {results['response_count']}",
        f"- No-response rows: {results['no_response_count']}",
        "",
        "## Strategy Aggregates",
        "",
        "| Strategy | Prompts | Response coverage | End-to-end required citation recall | Conditional required citation recall | Avg irrelevant citations | Avg hallucinated citations | Avg current-unit citations | Avg bare memory refs | Avg format violations | No responses |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for strategy, item in sorted(results["strategy_aggregates"].items()):
        lines.append(
            "| {strategy} | {prompts} | {coverage} | {e2e} | {conditional} | {irrelevant} | {hallucinated} | {current_units} | {bare_refs} | {format_violations} | {no_response} |".format(
                strategy=strategy,
                prompts=item["prompts"],
                coverage=format_float(item["response_coverage"]),
                e2e=format_float(item["avg_end_to_end_required_citation_recall"]),
                conditional=format_float(item["avg_conditional_required_citation_recall"]),
                irrelevant=format_float(item["avg_irrelevant_citation_count"]),
                hallucinated=format_float(item["avg_hallucinated_citation_count"]),
                current_units=format_float(item["avg_invalid_current_unit_citation_count"]),
                bare_refs=format_float(item["avg_bare_memory_reference_count"]),
                format_violations=format_float(item["avg_citation_format_violation_count"]),
                no_response=item["no_response_count"],
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "Citation recall is a proxy for whether a response cites required memory IDs. Bare references like `m2` do not count as citations. Bracketed current-unit references like `[u2]` are diagnosed as invalid current-unit citations, not memory citations. These metrics are not full memory-fact coverage, and a response can be useful or flawed in ways this script cannot detect.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    args = parser.parse_args()

    prompts = load_jsonl(args.prompts)
    responses = load_jsonl(args.responses)
    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    response_by_id = {row.get("prompt_id"): row for row in responses if isinstance(row.get("prompt_id"), str)}
    duplicate_response_ids = sorted(
        prompt_id
        for prompt_id in response_by_id
        if sum(1 for row in responses if row.get("prompt_id") == prompt_id) > 1
    )

    scored_rows = [score_response(prompt, response_by_id.get(prompt["prompt_id"])) for prompt in prompts]
    results = {
        "metric_scope": "partial automatic citation metrics only; not full answer-quality judging",
        "prompt_path": str(args.prompts),
        "response_path": str(args.responses),
        "prompt_count": len(prompts),
        "response_count": len(responses),
        "missing_response_prompt_ids": sorted(set(prompt_by_id) - set(response_by_id)),
        "extra_response_prompt_ids": sorted(set(response_by_id) - set(prompt_by_id)),
        "duplicate_response_ids": duplicate_response_ids,
        "no_response_count": sum(row["no_response_count"] for row in scored_rows),
        "strategy_aggregates": aggregate_by_strategy(scored_rows),
        "prompt_scores": scored_rows,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text(build_markdown(results), encoding="utf-8")
    print(f"Scored prompts: {len(scored_rows)}")
    print(f"No-response rows: {results['no_response_count']}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote Markdown: {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
