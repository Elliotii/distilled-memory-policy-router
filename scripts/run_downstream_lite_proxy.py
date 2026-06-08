#!/usr/bin/env python3
"""Run a no-inference downstream-lite context-efficiency proxy benchmark.

This script replays locked gold cases and saved prediction raw outputs. It does
not load a model, call an API, train, retrieve, or modify input artifacts.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


STRATEGY_ORDER = [
    "all_candidates",
    "router_selected",
    "oracle_selected",
    "no_memory",
    "top_k_naive",
]


@dataclass(frozen=True)
class CaseRecord:
    case_id: str
    candidate_ids: list[str]
    memory_text_by_id: dict[str, str]
    gold_read_ids: set[str]
    router_read_ids: set[str]


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    rows: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    with path.open(encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                row = json.loads(text)
            except json.JSONDecodeError as exc:
                skipped.append(
                    {
                        "case_id": f"{path}:{line_number}",
                        "reason": f"invalid JSONL row: {exc}",
                    }
                )
                continue
            if not isinstance(row, dict):
                skipped.append(
                    {
                        "case_id": f"{path}:{line_number}",
                        "reason": "JSONL row is not an object",
                    }
                )
                continue
            rows.append(row)
    return rows, skipped


def stable_unique_strings(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if isinstance(value, str) and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def extract_policy_read_ids(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return []
    if "read" in policy:
        return stable_unique_strings(policy.get("read"))
    if "read_hints" in policy:
        hints = policy.get("read_hints")
        if isinstance(hints, list):
            ids: list[str] = []
            for hint in hints:
                if isinstance(hint, str):
                    ids.append(hint)
                elif isinstance(hint, dict):
                    value = hint.get("id") or hint.get("memory_id")
                    if isinstance(value, str):
                        ids.append(value)
            return stable_unique_strings(ids)
    return []


def parse_raw_output(raw_output: Any) -> dict[str, Any]:
    if not isinstance(raw_output, str) or not raw_output.strip():
        raise ValueError("missing raw_output string")
    text = raw_output.strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise
        parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("raw_output JSON is not an object")
    return parsed


def candidate_memory_id(memory: Any) -> str | None:
    if not isinstance(memory, dict):
        return None
    value = memory.get("memory_id") or memory.get("id")
    return value if isinstance(value, str) else None


def candidate_memory_text(memory: Any) -> str:
    if not isinstance(memory, dict):
        return ""
    value = memory.get("text") or memory.get("content") or memory.get("memory")
    return value if isinstance(value, str) else ""


def build_case_records(
    gold_rows: list[dict[str, Any]],
    prediction_rows: list[dict[str, Any]],
    initial_skipped: list[dict[str, str]],
) -> tuple[list[CaseRecord], list[dict[str, str]]]:
    skipped = list(initial_skipped)
    predictions_by_case: dict[str, dict[str, Any]] = {}
    duplicate_prediction_ids: set[str] = set()

    for row in prediction_rows:
        case_id = row.get("case_id")
        if not isinstance(case_id, str):
            skipped.append({"case_id": "unknown", "reason": "prediction row missing string case_id"})
            continue
        if case_id in predictions_by_case:
            duplicate_prediction_ids.add(case_id)
        predictions_by_case[case_id] = row

    for case_id in sorted(duplicate_prediction_ids):
        skipped.append({"case_id": case_id, "reason": "duplicate prediction row; last row used"})

    records: list[CaseRecord] = []
    for gold_row in gold_rows:
        case_id = gold_row.get("case_id")
        if not isinstance(case_id, str):
            skipped.append({"case_id": "unknown", "reason": "gold row missing string case_id"})
            continue

        candidate_memories = gold_row.get("candidate_memories")
        if not isinstance(candidate_memories, list):
            skipped.append({"case_id": case_id, "reason": "candidate_memories is not a list"})
            continue

        candidate_ids: list[str] = []
        memory_text_by_id: dict[str, str] = {}
        for memory in candidate_memories:
            memory_id = candidate_memory_id(memory)
            if memory_id is None:
                continue
            if memory_id not in memory_text_by_id:
                candidate_ids.append(memory_id)
            memory_text_by_id[memory_id] = candidate_memory_text(memory)

        gold_policy = gold_row.get("gold") or gold_row.get("target")
        gold_read_ids = set(extract_policy_read_ids(gold_policy))

        prediction_row = predictions_by_case.get(case_id)
        if prediction_row is None:
            skipped.append({"case_id": case_id, "reason": "missing prediction row"})
            continue

        try:
            predicted_policy = parse_raw_output(prediction_row.get("raw_output"))
        except (json.JSONDecodeError, ValueError) as exc:
            skipped.append({"case_id": case_id, "reason": f"could not parse prediction raw_output: {exc}"})
            continue

        router_read_ids = set(extract_policy_read_ids(predicted_policy))
        records.append(
            CaseRecord(
                case_id=case_id,
                candidate_ids=candidate_ids,
                memory_text_by_id=memory_text_by_id,
                gold_read_ids=gold_read_ids,
                router_read_ids=router_read_ids,
            )
        )

    return records, skipped


def safe_ratio(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def safe_reduction(selected: int, baseline: int) -> float | None:
    if baseline == 0:
        return None
    return 1.0 - (selected / baseline)


def selected_ids_for_strategy(record: CaseRecord, strategy: str, top_k: int) -> set[str]:
    if strategy == "all_candidates":
        return set(record.candidate_ids)
    if strategy == "router_selected":
        return set(record.router_read_ids)
    if strategy == "oracle_selected":
        return set(record.gold_read_ids)
    if strategy == "no_memory":
        return set()
    if strategy == "top_k_naive":
        return set(record.candidate_ids[:top_k])
    raise ValueError(f"unknown strategy: {strategy}")


def compute_strategy_metrics(
    records: list[CaseRecord],
    strategy: str,
    top_k: int,
    skipped_case_count: int,
) -> dict[str, Any]:
    total_selected = 0
    total_selected_chars = 0
    total_all_candidates = 0
    total_gold_read = 0
    total_selected_gold = 0
    total_irrelevant_selected = 0
    total_irrelevant_all = 0
    exact_matches = 0

    for record in records:
        selected_ids = selected_ids_for_strategy(record, strategy, top_k)
        selected_existing_ids = selected_ids.intersection(record.memory_text_by_id)
        gold_ids = set(record.gold_read_ids)
        candidate_ids = set(record.candidate_ids)
        irrelevant_all = candidate_ids - gold_ids
        irrelevant_selected = selected_ids - gold_ids

        total_selected += len(selected_ids)
        total_selected_chars += sum(len(record.memory_text_by_id[memory_id]) for memory_id in selected_existing_ids)
        total_all_candidates += len(record.candidate_ids)
        total_gold_read += len(gold_ids)
        total_selected_gold += len(selected_ids.intersection(gold_ids))
        total_irrelevant_selected += len(irrelevant_selected)
        total_irrelevant_all += len(irrelevant_all)
        if selected_ids == gold_ids:
            exact_matches += 1

    cases = len(records)
    return {
        "cases": cases,
        "avg_selected_memory_count": safe_ratio(total_selected, cases),
        "avg_selected_memory_chars": safe_ratio(total_selected_chars, cases),
        "selected_memory_reduction_vs_all": safe_reduction(total_selected, total_all_candidates),
        "gold_read_recall": safe_ratio(total_selected_gold, total_gold_read),
        "irrelevant_memory_count": total_irrelevant_selected,
        "avg_irrelevant_memory_count": safe_ratio(total_irrelevant_selected, cases),
        "irrelevant_memory_reduction_vs_all": safe_reduction(total_irrelevant_selected, total_irrelevant_all),
        "exact_read_set_match": safe_ratio(exact_matches, cases),
        "exact_read_set_match_count": exact_matches,
        "skipped_cases": skipped_case_count,
    }


def fmt_float(value: Any, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def fmt_percent(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def build_markdown_report(metrics: dict[str, Any], command: str) -> str:
    strategies = metrics["strategies"]
    top_k = metrics["top_k_naive_k"]
    lines = [
        "# Downstream-Lite Proxy Report",
        "",
        "This report is a no-inference context-efficiency proxy over locked `gold_v2_009` gold cases and saved BF16 r16 1000_4090 prediction raw outputs. It is not a real downstream LLM evaluation.",
        "",
        "## Command",
        "",
        "```bash",
        command,
        "```",
        "",
        "## Strategy Comparison",
        "",
        f"`top_k_naive` uses k={top_k}, the rounded average number of router-selected memories per parsed case.",
        "",
        "| Strategy | Cases | Avg selected memories | Avg selected chars | Selected reduction vs all | Gold READ recall | Irrelevant memories | Avg irrelevant | Irrelevant reduction vs all | Exact READ set match | Skipped cases |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for strategy in STRATEGY_ORDER:
        item = strategies[strategy]
        lines.append(
            "| {strategy} | {cases} | {avg_count} | {avg_chars} | {selected_reduction} | {recall} | {irrelevant_count} | {avg_irrelevant} | {irrelevant_reduction} | {exact} | {skipped} |".format(
                strategy=strategy,
                cases=item["cases"],
                avg_count=fmt_float(item["avg_selected_memory_count"], 2),
                avg_chars=fmt_float(item["avg_selected_memory_chars"], 1),
                selected_reduction=fmt_percent(item["selected_memory_reduction_vs_all"]),
                recall=fmt_percent(item["gold_read_recall"]),
                irrelevant_count=item["irrelevant_memory_count"],
                avg_irrelevant=fmt_float(item["avg_irrelevant_memory_count"], 2),
                irrelevant_reduction=fmt_percent(item["irrelevant_memory_reduction_vs_all"]),
                exact=fmt_percent(item["exact_read_set_match"]),
                skipped=item["skipped_cases"],
            )
        )

    router = strategies["router_selected"]
    all_candidates = strategies["all_candidates"]
    oracle = strategies["oracle_selected"]
    no_memory = strategies["no_memory"]
    lines.extend(
        [
            "",
            "## Main Findings",
            "",
            f"- `router_selected` selected {fmt_float(router['avg_selected_memory_count'], 2)} memories per case on average versus {fmt_float(all_candidates['avg_selected_memory_count'], 2)} for `all_candidates`.",
            f"- `router_selected` reduced selected-memory count by {fmt_percent(router['selected_memory_reduction_vs_all'])} versus injecting all candidates, using approximate context chars rather than real token cost.",
            f"- `router_selected` retained {fmt_percent(router['gold_read_recall'])} gold READ recall, while `oracle_selected` is {fmt_percent(oracle['gold_read_recall'])} by construction and `no_memory` is {fmt_percent(no_memory['gold_read_recall'])}.",
            f"- `router_selected` selected {router['irrelevant_memory_count']} irrelevant memories across parsed cases, a {fmt_percent(router['irrelevant_memory_reduction_vs_all'])} reduction versus `all_candidates`.",
            f"- `router_selected` exact READ set match is {fmt_percent(router['exact_read_set_match'])}; this should be interpreted as saved prediction replay over locked `gold_v2_009`, not as live inference.",
            "",
            "## Limitations",
            "",
            "- No LLM answer evaluation is performed.",
            "- No retriever is implemented or evaluated.",
            "- No model inference, training, Qwen loading, or external API call is performed.",
            "- No real latency or cost measurement is performed.",
            "- Character count is only an approximate context-size proxy, not a token-cost measurement.",
            "- The benchmark is controlled and uses fixed candidate memories from locked artifacts.",
            "- The proxy uses saved prediction raw outputs, not live model responses.",
            "",
            "## Claim Boundaries",
            "",
            "This report can support only a narrow context-efficiency proxy claim: under locked `gold_v2_009` artifacts, saved router predictions select fewer candidate memories than injecting all candidates while preserving most labeled READ memories. It does not prove downstream answer quality, real deployment savings, production safety, retriever behavior, or full-agent behavior.",
        ]
    )

    skipped_cases = metrics.get("skipped_case_details", [])
    lines.extend(["", "## Skipped Cases", ""])
    if skipped_cases:
        for item in skipped_cases:
            lines.append(f"- `{item['case_id']}`: {item['reason']}")
    else:
        lines.append("No cases were skipped.")

    lines.append("")
    return "\n".join(lines)


def build_command(args: argparse.Namespace) -> str:
    return (
        "python3 scripts/run_downstream_lite_proxy.py \\\n"
        f"  --gold {args.gold} \\\n"
        f"  --predictions {args.predictions} \\\n"
        f"  --out-json {args.out_json} \\\n"
        f"  --out-md {args.out_md}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, required=True, help="Locked gold JSONL file.")
    parser.add_argument("--predictions", type=Path, required=True, help="Saved prediction JSONL file.")
    parser.add_argument("--out-json", type=Path, required=True, help="Output metrics JSON path.")
    parser.add_argument("--out-md", type=Path, required=True, help="Output markdown report path.")
    args = parser.parse_args()

    gold_rows, gold_skipped = load_jsonl(args.gold)
    prediction_rows, prediction_skipped = load_jsonl(args.predictions)
    records, skipped_cases = build_case_records(gold_rows, prediction_rows, gold_skipped + prediction_skipped)

    if records:
        avg_router_selected = sum(len(record.router_read_ids) for record in records) / len(records)
        top_k = int(math.floor(avg_router_selected + 0.5))
    else:
        avg_router_selected = 0.0
        top_k = 0

    skipped_case_count = len(skipped_cases)
    strategies = {
        strategy: compute_strategy_metrics(records, strategy, top_k, skipped_case_count)
        for strategy in STRATEGY_ORDER
    }
    metrics = {
        "benchmark": "downstream_lite_context_efficiency_proxy",
        "mode": "no_inference_saved_prediction_replay",
        "gold_path": str(args.gold),
        "predictions_path": str(args.predictions),
        "gold_rows": len(gold_rows),
        "prediction_rows": len(prediction_rows),
        "parsed_cases": len(records),
        "skipped_case_count": skipped_case_count,
        "skipped_case_details": skipped_cases,
        "top_k_naive_k": top_k,
        "router_avg_selected_memory_count_for_top_k": avg_router_selected,
        "metric_notes": {
            "gold_relevant_memory": "memory id in the gold READ set",
            "irrelevant_selected_memory": "selected memory id not in the gold READ set",
            "gold_read_recall": "selected gold READ ids divided by total gold READ ids",
            "selected_memory_chars": "approximate context chars from selected candidate memory text, not tokens",
            "selected_memory_reduction_vs_all": "1 - selected_count / all_candidate_count",
            "irrelevant_memory_reduction_vs_all": "1 - irrelevant_selected_count / irrelevant_all_count, or null when no irrelevant candidates exist",
        },
        "strategies": strategies,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text(build_markdown_report(metrics, build_command(args)), encoding="utf-8")

    print(f"Parsed cases: {len(records)}")
    print(f"Skipped cases: {skipped_case_count}")
    print(f"top_k_naive k: {top_k}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote report: {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
