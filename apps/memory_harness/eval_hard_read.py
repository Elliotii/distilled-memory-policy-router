#!/usr/bin/env python3
"""Selection-only hard READ evaluation runner.

This runner evaluates deterministic READ selection strategies over labeled
hard-candidate fixtures. It does not run downstream answer generation.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Dict, Iterable, List

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from apps.memory_harness.backends.read_selectors import run_read_selector
from apps.memory_harness.cli import scenario_query
from apps.memory_harness.context_builder import build_context
from apps.memory_harness.memory_store import load_memory_pool
from apps.memory_harness.schemas import JsonDict, validate_memory_record


LABEL_KEYS = [
    "required_memory_ids",
    "helpful_memory_ids",
    "avoid_memory_ids",
    "stale_or_harmful_memory_ids",
    "contradictory_memory_ids",
    "wrong_scope_memory_ids",
]

CASE_REQUIRED_KEYS = [
    "case_id",
    "user_input",
    "runtime_context",
    "current_units",
    "candidate_memory_ids",
    "labels",
]


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


def load_replay_predictions(path: str | None) -> Dict[str, JsonDict]:
    if not path:
        return {}
    predictions: Dict[str, JsonDict] = {}
    for row in load_jsonl(path):
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{path}: replay prediction row missing case_id")
        if case_id in predictions:
            raise ValueError(f"{path}: duplicate replay prediction case_id {case_id}")
        predictions[case_id] = row
    return predictions


def _require_keys(row: JsonDict, keys: Iterable[str], label: str) -> None:
    missing = [key for key in keys if key not in row]
    if missing:
        raise ValueError(f"{label} missing required keys: {', '.join(missing)}")


def validate_no_global_relevance(memory_rows: List[JsonDict]) -> None:
    for memory in memory_rows:
        validate_memory_record(memory)


def validate_case(case: JsonDict, memory_ids: set[str]) -> None:
    _require_keys(case, CASE_REQUIRED_KEYS, "hard READ case")
    case_id = case["case_id"]
    candidate_ids = set(case["candidate_memory_ids"])
    if len(candidate_ids) != len(case["candidate_memory_ids"]):
        raise ValueError(f"{case_id}: duplicate candidate_memory_ids")
    if not 8 <= len(candidate_ids) <= 15:
        raise ValueError(f"{case_id}: candidate count must be 8-15")
    missing = sorted(candidate_ids - memory_ids)
    if missing:
        raise ValueError(f"{case_id}: candidate ids missing from pool: {', '.join(missing)}")

    labels = case["labels"]
    for key in LABEL_KEYS:
        label_ids = set(labels.get(key, []))
        if not label_ids <= candidate_ids:
            raise ValueError(f"{case_id}: {key} contains non-candidate ids")

    if len(labels.get("required_memory_ids", [])) < 2:
        raise ValueError(f"{case_id}: needs at least 2 required memories")
    if len(labels.get("helpful_memory_ids", [])) < 1:
        raise ValueError(f"{case_id}: needs at least 1 helpful memory")
    if len(labels.get("avoid_memory_ids", [])) < 3:
        raise ValueError(f"{case_id}: needs at least 3 avoid memories")
    if len(labels.get("stale_or_harmful_memory_ids", [])) < 1:
        raise ValueError(f"{case_id}: needs at least 1 stale_or_harmful memory")
    if not labels.get("wrong_scope_memory_ids") and not labels.get("contradictory_memory_ids"):
        raise ValueError(f"{case_id}: needs wrong_scope or contradictory memory")

    candidate_labels = labels.get("candidate_labels", {})
    if set(candidate_labels) != candidate_ids:
        raise ValueError(f"{case_id}: candidate_labels must cover all candidate ids")
    hard_negative_types = {item.get("hard_negative_type") for item in candidate_labels.values()}
    if "same_entity_irrelevant" not in hard_negative_types and "near_duplicate" not in hard_negative_types:
        raise ValueError(f"{case_id}: needs same_entity_irrelevant or near_duplicate hard negative")


def selected_flags(selected_memories: List[JsonDict], flag: str) -> int:
    return sum(1 for memory in selected_memories if flag in memory.get("flags", []))


def count_intersection(selected_ids: Iterable[str], label_ids: Iterable[str]) -> int:
    return len(set(selected_ids) & set(label_ids))


def pre_budget_metrics(
    case: JsonDict,
    selected_memories: List[JsonDict],
    selected_ids: List[str],
) -> JsonDict:
    labels = case["labels"]
    required_ids = labels.get("required_memory_ids", [])
    required_selected = count_intersection(selected_ids, required_ids)
    required_total = len(required_ids)
    return {
        "selected_count": len(selected_ids),
        "required_selected_count": required_selected,
        "required_total": required_total,
        "required_selected_recall": round(required_selected / required_total, 6) if required_total else 0.0,
        "helpful_selected_count": count_intersection(selected_ids, labels.get("helpful_memory_ids", [])),
        "avoid_selected_count": count_intersection(selected_ids, labels.get("avoid_memory_ids", [])),
        "stale_selected_count": count_intersection(selected_ids, labels.get("stale_or_harmful_memory_ids", [])),
        "contradictory_selected_count": count_intersection(selected_ids, labels.get("contradictory_memory_ids", [])),
        "wrong_scope_selected_count": count_intersection(selected_ids, labels.get("wrong_scope_memory_ids", [])),
        "sensitive_boundary_selected_count": selected_flags(selected_memories, "sensitive_boundary"),
    }


def post_budget_metrics(
    case: JsonDict,
    context: JsonDict,
    injected_memories: List[JsonDict],
) -> JsonDict:
    injected_ids = context["selected_memory_ids"]
    labels = case["labels"]
    required_ids = labels.get("required_memory_ids", [])
    required_injected = count_intersection(injected_ids, required_ids)
    required_total = len(required_ids)
    return {
        "injected_count": len(injected_ids),
        "context_chars": context["context_chars"],
        "required_injected_count": required_injected,
        "required_total": required_total,
        "required_injected_recall": round(required_injected / required_total, 6) if required_total else 0.0,
        "helpful_injected_count": count_intersection(injected_ids, labels.get("helpful_memory_ids", [])),
        "avoid_injected_count": count_intersection(injected_ids, labels.get("avoid_memory_ids", [])),
        "stale_injected_count": count_intersection(injected_ids, labels.get("stale_or_harmful_memory_ids", [])),
        "contradictory_injected_count": count_intersection(injected_ids, labels.get("contradictory_memory_ids", [])),
        "wrong_scope_injected_count": count_intersection(injected_ids, labels.get("wrong_scope_memory_ids", [])),
        "sensitive_boundary_injected_count": selected_flags(injected_memories, "sensitive_boundary"),
        "over_budget_omitted_count": len(context["omitted_memory_ids"]),
    }


def mean(values: List[float]) -> float:
    return round(statistics.fmean(values), 6) if values else 0.0


def aggregate_rows(rows: List[JsonDict]) -> JsonDict:
    output: Dict[str, JsonDict] = {}
    for strategy in sorted({row["strategy"] for row in rows}):
        strategy_rows = [row for row in rows if row["strategy"] == strategy]
        pre_metrics = [row["pre_budget_selection"] for row in strategy_rows]
        post_metrics = [row["post_budget_context"] for row in strategy_rows]
        output[strategy] = {
            "case_count": len(strategy_rows),
            "mean_pre_selected_count": mean([m["selected_count"] for m in pre_metrics]),
            "mean_post_injected_count": mean([m["injected_count"] for m in post_metrics]),
            "mean_pre_required_recall": mean([m["required_selected_recall"] for m in pre_metrics]),
            "mean_post_required_recall": mean([m["required_injected_recall"] for m in post_metrics]),
            "total_pre_avoid_selected_count": sum(m["avoid_selected_count"] for m in pre_metrics),
            "total_post_avoid_injected_count": sum(m["avoid_injected_count"] for m in post_metrics),
            "total_pre_stale_selected_count": sum(m["stale_selected_count"] for m in pre_metrics),
            "total_post_stale_injected_count": sum(m["stale_injected_count"] for m in post_metrics),
            "total_pre_contradictory_selected_count": sum(m["contradictory_selected_count"] for m in pre_metrics),
            "total_post_contradictory_injected_count": sum(m["contradictory_injected_count"] for m in post_metrics),
            "total_pre_wrong_scope_selected_count": sum(m["wrong_scope_selected_count"] for m in pre_metrics),
            "total_post_wrong_scope_injected_count": sum(m["wrong_scope_injected_count"] for m in post_metrics),
            "total_pre_sensitive_boundary_selected_count": sum(m["sensitive_boundary_selected_count"] for m in pre_metrics),
            "total_post_sensitive_boundary_injected_count": sum(m["sensitive_boundary_injected_count"] for m in post_metrics),
            "mean_context_chars": mean([m["context_chars"] for m in post_metrics]),
        }
    return output


def write_jsonl(path: Path, rows: List[JsonDict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def observation_rows(rows: List[JsonDict], strategy: str) -> List[JsonDict]:
    return [row for row in rows if row["strategy"] == strategy]


def top_observations(by_case_rows: List[JsonDict]) -> List[str]:
    observations: List[str] = []
    all_rows = observation_rows(by_case_rows, "all_candidates")
    if all_rows:
        worst_all = max(all_rows, key=lambda row: row["pre_budget_selection"]["avoid_selected_count"])
        observations.append(
            f"{worst_all['case_id']}: all_candidates selector selects "
            f"{worst_all['pre_budget_selection']['avoid_selected_count']} avoid memories pre-budget; "
            f"{worst_all['post_budget_context']['avoid_injected_count']} reach the all-candidates context after character budgeting."
        )
    order_rows = observation_rows(by_case_rows, "budgeted_candidate_order")
    if order_rows:
        sample_order = max(order_rows, key=lambda row: row["post_budget_context"]["required_injected_recall"])
        observations.append(
            f"{sample_order['case_id']}: budgeted_candidate_order is order-sensitive and reaches "
            f"{sample_order['post_budget_context']['required_injected_recall']:.2f} required recall on this candidate order."
        )
    keyword_rows = observation_rows(by_case_rows, "keyword_top_k")
    keyword_misses = [
        row for row in keyword_rows
        if row["pre_budget_selection"]["required_selected_recall"] < 1.0
    ]
    if keyword_misses:
        worst_keyword = min(keyword_misses, key=lambda row: row["pre_budget_selection"]["required_selected_recall"])
        observations.append(
            f"{worst_keyword['case_id']}: keyword_top_k required recall is "
            f"{worst_keyword['pre_budget_selection']['required_selected_recall']:.2f} pre-budget, so lexical selection misses required memory."
        )
    risky_keyword = [
        row for row in keyword_rows
        if (
            row["pre_budget_selection"]["stale_selected_count"]
            + row["pre_budget_selection"]["wrong_scope_selected_count"]
            + row["pre_budget_selection"]["contradictory_selected_count"]
        ) > 0
    ]
    if risky_keyword:
        risky = max(
            risky_keyword,
            key=lambda row: (
                row["pre_budget_selection"]["stale_selected_count"]
                + row["pre_budget_selection"]["wrong_scope_selected_count"]
                + row["pre_budget_selection"]["contradictory_selected_count"]
            ),
        )
        observations.append(
            f"{risky['case_id']}: keyword_top_k selects stale, contradictory, or wrong-scope memory pre-budget."
        )
    return observations[:3]


def contamination_examples(by_case_rows: List[JsonDict], strategy: str, limit: int = 3) -> List[str]:
    rows = [
        row for row in observation_rows(by_case_rows, strategy)
        if row["pre_budget_selection"]["avoid_selected_count"] > 0
    ]
    rows.sort(key=lambda row: (-row["pre_budget_selection"]["avoid_selected_count"], row["case_id"]))
    return [
        f"{row['case_id']}: selected {row['pre_budget_selection']['avoid_selected_count']} avoid memories "
        f"pre-budget; injected {row['post_budget_context']['avoid_injected_count']} after context budgeting."
        for row in rows[:limit]
    ]


def keyword_failure_examples(by_case_rows: List[JsonDict], limit: int = 3) -> List[str]:
    rows = []
    for row in observation_rows(by_case_rows, "keyword_top_k"):
        metrics = row["pre_budget_selection"]
        risk_count = (
            metrics["stale_selected_count"]
            + metrics["contradictory_selected_count"]
            + metrics["wrong_scope_selected_count"]
        )
        if metrics["required_selected_recall"] < 1.0 or risk_count:
            rows.append((risk_count, row))
    rows.sort(key=lambda item: (-item[0], item[1]["pre_budget_selection"]["required_selected_recall"], item[1]["case_id"]))
    examples = []
    for risk_count, row in rows[:limit]:
        pre = row["pre_budget_selection"]
        post = row["post_budget_context"]
        examples.append(
            f"{row['case_id']}: pre required recall {pre['required_selected_recall']:.2f}, "
            f"post required recall {post['required_injected_recall']:.2f}; "
            f"pre selected stale={pre['stale_selected_count']}, "
            f"contradictory={pre['contradictory_selected_count']}, "
            f"wrong_scope={pre['wrong_scope_selected_count']}."
        )
    return examples


def write_report(
    path: Path,
    *,
    case_count: int,
    memory_count: int,
    strategies: List[str],
    aggregates: JsonDict,
    observations: List[str],
    by_case_rows: List[JsonDict],
    is_v2_design: bool = False,
) -> None:
    lines = [
        "# Hard READ Selection Pilot Report",
        "",
        "Context: hard READ pilot fixture selection-only evaluation.",
        "",
        "This report evaluates memory selection only. It does not run a downstream answerer, call an API, load Qwen or LoRA, or evaluate learned router/live LoRA behavior.",
        "",
        "Learned router/live LoRA is not evaluated because no real backend output is available for these hard-read cases.",
        "",
        "## Run Summary",
        "",
        f"- Case count: {case_count}",
        f"- Memory pool count: {memory_count}",
        f"- Strategies evaluated: {', '.join(strategies)}",
    ]
    if is_v2_design:
        lines.extend([
            "",
            "## v2 Design Intent Compared With v1",
            "",
            "- Candidate memory order is fixed-seed shuffled rather than label-ordered, so `budgeted_candidate_order` is a stress test for order bias rather than a favorable pseudo-oracle.",
            "- Current task notes are deliberately less answerable without memory: they define the task but omit exact commands, thresholds, deadlines, and implementation constraints that live only in memory.",
            "- v2 is designed to reduce no_memory answerability by under-specifying task notes, but this is not verified by the selection-only eval; it must be checked in a later downstream response pilot.",
            "- This remains an 8-case pilot fixture repair, not the final 30-40 case hard READ evaluation.",
            "- This is selection-only and does not measure downstream answer quality.",
        ])
    lines.extend([
        "",
        "## Metric Semantics",
        "",
        "`pre_budget_selection` measures what the selector chose before the context budget is applied. `post_budget_context` measures what actually reaches the injected memory context after `max_memories` and `max_context_chars` are enforced.",
        "",
        "`all_candidates` now means a true all-candidates context: it selects every candidate and bypasses the `top-k`/`max_memories` cap. The `max_context_chars` cap is still retained as a safety bound.",
        "",
        "`budgeted_candidate_order` is the first-k candidate-order baseline. It is order-sensitive, not a learned selector, and is vulnerable to fixture ordering.",
        "",
        "## Aggregate Strategy Metrics",
        "",
        "| Strategy | Mean pre selected | Mean post injected | Pre req recall | Post req recall | Pre avoid | Post avoid | Pre stale | Post stale | Pre contradictory | Post contradictory | Pre wrong-scope | Post wrong-scope | Pre sensitive | Post sensitive | Mean context chars |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for strategy in sorted(aggregates):
        row = aggregates[strategy]
        lines.append(
            f"| {strategy} | {row['mean_pre_selected_count']:.2f} | {row['mean_post_injected_count']:.2f} | "
            f"{row['mean_pre_required_recall']:.2f} | {row['mean_post_required_recall']:.2f} | "
            f"{row['total_pre_avoid_selected_count']} | {row['total_post_avoid_injected_count']} | "
            f"{row['total_pre_stale_selected_count']} | {row['total_post_stale_injected_count']} | "
            f"{row['total_pre_contradictory_selected_count']} | {row['total_post_contradictory_injected_count']} | "
            f"{row['total_pre_wrong_scope_selected_count']} | {row['total_post_wrong_scope_injected_count']} | "
            f"{row['total_pre_sensitive_boundary_selected_count']} | {row['total_post_sensitive_boundary_injected_count']} | "
            f"{row['mean_context_chars']:.2f} |"
        )

    lines.extend([
        "",
        "## Top Case-Level Observations",
        "",
    ])
    lines.extend([f"- {item}" for item in observations])
    lines.extend([
        "",
        "## All-Candidates Contamination Examples",
        "",
        "The all_candidates selector selects every avoid memory pre-budget. Because this strategy bypasses `top-k`, the post-budget counts below show how many avoid memories reach the injected context unless the character cap omits them.",
        "",
    ])
    lines.extend([f"- {item}" for item in contamination_examples(by_case_rows, "all_candidates")])
    lines.extend([
        "",
        "## Keyword Top-K Failure Examples",
        "",
        "Keyword top-k can miss required memory when a hard negative shares stronger lexical overlap with the task text. It can also select stale, contradictory, or wrong-scope memories when those candidates repeat the same service and task terms.",
        "",
    ])
    lines.extend([f"- {item}" for item in keyword_failure_examples(by_case_rows)])
    lines.extend([
        "",
        "## Candidate-Order Baseline Note",
        "",
        "`budgeted_candidate_order` represents the naive first-k candidate-order baseline. It is order-sensitive and should not be treated as a realistic retriever ranking.",
        "",
        "## Limitations",
        "",
        "- Selection metrics are diagnostic and do not measure downstream answer quality.",
        "- This pilot is intentionally small and fixture-like to validate hard-candidate schema and selection metrics; it is not the final 30-40 case hard READ evaluation.",
        "- Candidate ordering is a fixture property and should not be interpreted as realistic retrieval rank quality.",
        "- Keyword retrieval is a deterministic lexical stub, not evidence about deployed retrieval behavior.",
        "- Oracle selection uses labels and is a reference ceiling for fixture inspection only.",
        "- No learned router, live LoRA, or saved router output is evaluated in this context.",
        "- These results should not be used to claim downstream utility or that any learned selector outperforms baselines.",
        "",
        "## Next Context Recommendation",
        "",
        "Recommended next context: Context 7.4-E — v2 downstream prompt-pack scaffold and manual prompt inspection.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def evaluate(args: argparse.Namespace) -> JsonDict:
    cases = load_jsonl(args.cases)
    memory_rows = load_jsonl(args.memory_pool)
    validate_no_global_relevance(memory_rows)
    memory_ids = {row["memory_id"] for row in memory_rows}
    for case in cases:
        validate_case(case, memory_ids)

    store = load_memory_pool(args.memory_pool)
    strategies = [item.strip() for item in args.strategies.split(",") if item.strip()]
    replay_predictions = load_replay_predictions(args.replay_predictions)
    if "replay_learned_router" in strategies and not replay_predictions:
        raise ValueError("--replay-predictions is required for replay_learned_router")
    by_case_rows: List[JsonDict] = []
    trace_rows: List[JsonDict] = []

    for case in cases:
        candidates = store.get_by_ids(case["candidate_memory_ids"])
        query = scenario_query(case)
        selector_case = {**case, "scenario_id": case["case_id"]}
        for strategy in strategies:
            selection = run_read_selector(
                strategy,
                selector_case,
                candidates,
                query=query,
                k=args.top_k,
                replay_predictions=replay_predictions,
            )
            selected_ids = selection["selected_memory_ids"]
            selected_memories = store.get_by_ids(selected_ids)
            context_max_memories = len(selected_memories) if strategy == "all_candidates" else args.top_k
            context = build_context(
                selected_memories,
                max_memories=context_max_memories,
                max_context_chars=args.max_context_chars,
            )
            injected_ids = context["selected_memory_ids"]
            injected_memories = store.get_by_ids(injected_ids)
            omitted_candidate_ids = [
                memory_id
                for memory_id in case["candidate_memory_ids"]
                if memory_id not in selected_ids
            ]
            pre_metrics = pre_budget_metrics(case, selected_memories, selected_ids)
            post_metrics = post_budget_metrics(case, context, injected_memories)
            compact = {
                "case_id": case["case_id"],
                "strategy": strategy,
                "read_selector_backend": selection["backend"],
                "selected_memory_ids_pre_budget": selected_ids,
                "injected_memory_ids_post_budget": injected_ids,
                "omitted_candidate_ids": omitted_candidate_ids,
                "required_memory_ids": case["labels"].get("required_memory_ids", []),
                "avoid_memory_ids": case["labels"].get("avoid_memory_ids", []),
                "pre_budget_selection": pre_metrics,
                "post_budget_context": post_metrics,
                "selector_diagnostics": selection.get("diagnostics", {}),
                "metrics": {
                    "pre_budget_selection": pre_metrics,
                    "post_budget_context": post_metrics,
                },
            }
            by_case_rows.append(compact)
            trace_rows.append({
                **compact,
                "runtime_context": case.get("runtime_context", {}),
                "diagnostics": selection.get("diagnostics", {}),
                "context_builder": context,
                "note": "selection-only trace row; no downstream answer generated",
            })

    aggregates = aggregate_rows(by_case_rows)
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_json = {
        "case_count": len(cases),
        "memory_pool_count": len(memory_rows),
        "strategies": strategies,
        "replay_predictions": {
            "path": args.replay_predictions,
            "count": len(replay_predictions),
            "used": "replay_learned_router" in strategies,
            "claim_boundary": "Saved predictions are replayed only; eval_hard_read does not load a model.",
        },
        "aggregates": aggregates,
        "claim_boundary": "Selection-only pilot; no downstream answer quality or learned-router result.",
    }
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics_json, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_jsonl(output_dir / "by_case.jsonl", by_case_rows)
    write_jsonl(output_dir / "traces.jsonl", trace_rows)
    write_report(
        output_dir / "report.md",
        case_count=len(cases),
        memory_count=len(memory_rows),
        strategies=strategies,
        aggregates=aggregates,
        observations=top_observations(by_case_rows),
        by_case_rows=by_case_rows,
        is_v2_design=any(str(case.get("case_id", "")).startswith("hard_read_v2_") for case in cases),
    )
    return metrics_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Selection-only hard READ pilot evaluator")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--memory-pool", required=True)
    parser.add_argument("--strategies", required=True)
    parser.add_argument("--top-k", type=int, default=4)
    parser.add_argument("--max-context-chars", type=int, default=1600)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--replay-predictions")
    args = parser.parse_args()
    metrics = evaluate(args)
    print(json.dumps({
        "case_count": metrics["case_count"],
        "memory_pool_count": metrics["memory_pool_count"],
        "strategies": metrics["strategies"],
        "out_dir": args.out_dir,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
