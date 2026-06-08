#!/usr/bin/env python3
"""Score hard READ downstream pilot responses for citation scaffolding.

The scorer is intentionally limited to automatic citation checks. It does not
judge answer quality or memory usefulness.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path
from typing import Dict, Iterable, List


MEMORY_CITATION_RE = re.compile(r"\[(m\d{3})\]")
CURRENT_UNIT_CITATION_RE = re.compile(r"\[u\d+\]")
BARE_MEMORY_RE = re.compile(r"(?<![\[\w])(m\d{3})(?![\]\w])")

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


def unique_ordered(items: Iterable[str]) -> List[str]:
    seen = set()
    output = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        output.append(item)
    return output


def citation_metrics(prompt: JsonDict, response: JsonDict) -> JsonDict:
    text = str(response.get("response_text") or "")
    injected_ids = set(prompt.get("injected_memory_ids", []))
    required_ids = set(prompt.get("required_memory_ids", []))
    helpful_ids = set(prompt.get("helpful_memory_ids", []))
    avoid_ids = set(prompt.get("avoid_memory_ids", []))
    stale_ids = set(prompt.get("stale_or_harmful_memory_ids", []))
    contradictory_ids = set(prompt.get("contradictory_memory_ids", []))
    wrong_scope_ids = set(prompt.get("wrong_scope_memory_ids", []))

    cited_ids = unique_ordered(MEMORY_CITATION_RE.findall(text))
    cited_set = set(cited_ids)
    bracket_spans = [match.span() for match in MEMORY_CITATION_RE.finditer(text)]
    bare_refs = []
    for match in BARE_MEMORY_RE.finditer(text):
        if any(start <= match.start() and match.end() <= end for start, end in bracket_spans):
            continue
        bare_refs.append(match.group(1))

    required_cited = sorted(required_ids & cited_set)
    required_injected = required_ids & injected_ids
    required_total = len(required_ids)
    required_injected_total = len(required_injected)

    return {
        "prompt_id": prompt["prompt_id"],
        "case_id": prompt["case_id"],
        "strategy": prompt["strategy"],
        "has_response": bool(text.strip()),
        "valid_memory_citations": cited_ids,
        "hallucinated_memory_citations": sorted(cited_set - injected_ids),
        "required_citations": required_cited,
        "helpful_citations": sorted(helpful_ids & cited_set),
        "avoid_citations": sorted(avoid_ids & cited_set),
        "stale_citations": sorted(stale_ids & cited_set),
        "contradictory_citations": sorted(contradictory_ids & cited_set),
        "wrong_scope_citations": sorted(wrong_scope_ids & cited_set),
        "required_citation_recall": round(len(required_cited) / required_total, 6) if required_total else 0.0,
        "conditional_required_citation_recall": (
            round(len(required_injected & cited_set) / required_injected_total, 6)
            if required_injected_total
            else 0.0
        ),
        "bare_memory_refs": unique_ordered(bare_refs),
        "current_unit_citations": unique_ordered(CURRENT_UNIT_CITATION_RE.findall(text)),
    }


def mean(values: List[float]) -> float:
    return round(statistics.fmean(values), 6) if values else 0.0


def aggregate(rows: List[JsonDict]) -> JsonDict:
    output: Dict[str, JsonDict] = {}
    for strategy in sorted({str(row["strategy"]) for row in rows}):
        subset = [row for row in rows if row["strategy"] == strategy]
        prompt_count = len(subset)
        response_count = sum(1 for row in subset if row["has_response"])
        output[strategy] = {
            "prompt_count": prompt_count,
            "response_coverage": round(response_count / prompt_count, 6) if prompt_count else 0.0,
            "e2e_required_citation_recall": mean([float(row["required_citation_recall"]) for row in subset]),
            "conditional_required_citation_recall": mean([
                float(row["conditional_required_citation_recall"]) for row in subset
            ]),
            "avg_avoid_citations": mean([len(row["avoid_citations"]) for row in subset]),
            "avg_stale_citations": mean([len(row["stale_citations"]) for row in subset]),
            "avg_contradictory_citations": mean([len(row["contradictory_citations"]) for row in subset]),
            "avg_wrong_scope_citations": mean([len(row["wrong_scope_citations"]) for row in subset]),
            "avg_hallucinated_memory_citations": mean([
                len(row["hallucinated_memory_citations"]) for row in subset
            ]),
            "avg_bare_memory_refs": mean([len(row["bare_memory_refs"]) for row in subset]),
            "avg_current_unit_citations": mean([len(row["current_unit_citations"]) for row in subset]),
            "no_response_count": prompt_count - response_count,
        }
    return output


def write_markdown(path: str, score_doc: JsonDict) -> None:
    lines = [
        "# Hard READ Downstream Pilot Citation Scores",
        "",
        "These are partial automatic citation metrics for scaffold validation. They are not answer-quality proof.",
        "",
        f"- Prompt count: {score_doc['prompt_count']}",
        f"- Response count: {score_doc['response_count']}",
        f"- No-response count: {score_doc['no_response_count']}",
        "",
        "## Strategy Aggregates",
        "",
        "| Strategy | Prompts | Coverage | E2E required recall | Conditional required recall | Avoid avg | Stale avg | Contradictory avg | Wrong-scope avg | Hallucinated avg | Bare refs avg | Current-unit citations avg | No response |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for strategy, row in score_doc["by_strategy"].items():
        lines.append(
            f"| {strategy} | {row['prompt_count']} | {row['response_coverage']:.2f} | "
            f"{row['e2e_required_citation_recall']:.2f} | "
            f"{row['conditional_required_citation_recall']:.2f} | "
            f"{row['avg_avoid_citations']:.2f} | {row['avg_stale_citations']:.2f} | "
            f"{row['avg_contradictory_citations']:.2f} | {row['avg_wrong_scope_citations']:.2f} | "
            f"{row['avg_hallucinated_memory_citations']:.2f} | {row['avg_bare_memory_refs']:.2f} | "
            f"{row['avg_current_unit_citations']:.2f} | {row['no_response_count']} |"
        )
    lines.extend([
        "",
        "## Boundary",
        "",
        "Empty or missing responses should produce zero citation recall and full no-response counts. Manual or rubric-based review is still required for fact coverage, contamination, stale use, hallucination, task quality, and citation compliance.",
    ])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def score(prompts_path: str, responses_path: str) -> JsonDict:
    prompts = load_jsonl(prompts_path)
    responses = load_jsonl(responses_path)
    prompt_by_id = {str(row["prompt_id"]): row for row in prompts}
    response_by_id = {str(row["prompt_id"]): row for row in responses}
    missing = sorted(set(prompt_by_id) - set(response_by_id))
    if missing:
        raise ValueError("responses missing prompt_ids: " + ", ".join(missing))

    rows = [citation_metrics(prompt, response_by_id[prompt_id]) for prompt_id, prompt in prompt_by_id.items()]
    response_count = sum(1 for row in rows if row["has_response"])
    return {
        "prompt_count": len(rows),
        "response_count": response_count,
        "no_response_count": len(rows) - response_count,
        "by_strategy": aggregate(rows),
        "by_prompt": rows,
        "claim_boundary": "Automatic citation scaffold only; not answer-quality evaluation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score hard READ downstream pilot response citations")
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--responses", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    score_doc = score(args.prompts, args.responses)
    Path(args.out_json).write_text(json.dumps(score_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(args.out_md, score_doc)
    print(json.dumps({
        "prompt_count": score_doc["prompt_count"],
        "response_count": score_doc["response_count"],
        "no_response_count": score_doc["no_response_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
