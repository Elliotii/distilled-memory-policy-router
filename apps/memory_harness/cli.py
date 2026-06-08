#!/usr/bin/env python3
"""CLI for the Applied Memory Harness skeleton."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from apps.memory_harness.audit_trace import build_trace, write_trace
from apps.memory_harness.backends.read_selectors import run_read_selector
from apps.memory_harness.backends.write_policies import run_write_policy
from apps.memory_harness.context_builder import build_context
from apps.memory_harness.memory_store import load_memory_pool
from apps.memory_harness.retrievers import retrieve_top_k
from apps.memory_harness.schemas import JsonDict, normalize_current_unit, validate_scenario
from apps.memory_harness.unitizer import unitize_text
from apps.memory_harness.write_preview import build_write_preview


def load_scenarios(path: str) -> List[JsonDict]:
    rows: List[JsonDict] = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL") from exc
        validate_scenario(row)
        rows.append(row)
    return rows


def find_scenario(scenarios: List[JsonDict], scenario_id: str) -> JsonDict:
    for scenario in scenarios:
        if scenario["scenario_id"] == scenario_id:
            return scenario
    raise KeyError(f"scenario not found: {scenario_id}")


def scenario_query(scenario: JsonDict) -> str:
    context = scenario.get("runtime_context", {})
    context_text = " ".join(str(context.get(key, "")) for key in ("project", "repo", "service", "task"))
    return f"{scenario.get('user_input', '')} {context_text}".strip()


def scenario_units(scenario: JsonDict) -> List[JsonDict]:
    units = scenario.get("current_units") or unitize_text(scenario["user_input"])
    return [normalize_current_unit(dict(unit), index) for index, unit in enumerate(units, 1)]


def build_retrieval_block(query: str, candidate_memories: List[JsonDict]) -> JsonDict:
    retrieved = retrieve_top_k(query, candidate_memories, len(candidate_memories))
    return {
        "backend": "keyword_bm25_lite_stub",
        "query": query,
        "candidate_count": len(candidate_memories),
        "candidates": [
            {
                "memory_id": item["memory_id"],
                "score": item["score"],
                "matched_tokens": item["matched_tokens"],
                "target": item["memory"].get("target", ""),
                "text": item["memory"].get("text", ""),
                "project": item["memory"].get("project", ""),
                "repo": item["memory"].get("repo", ""),
                "service": item["memory"].get("service", ""),
                "flags": item["memory"].get("flags", []),
                "source": item["memory"].get("source", ""),
            }
            for item in retrieved
        ],
        "note": "deterministic keyword/BM25-lite retriever stub",
    }


def run_once(args: argparse.Namespace, scenario: JsonDict, selector_name: str) -> JsonDict:
    store = load_memory_pool(args.memory_pool)
    candidate_memories = store.get_by_ids(scenario["candidate_memory_ids"])
    query = scenario_query(scenario)
    current_units = scenario_units(scenario)
    k = max(args.max_memories, 0)

    retrieval = build_retrieval_block(query, candidate_memories)
    read_selection = run_read_selector(
        selector_name,
        scenario,
        candidate_memories,
        query=query,
        k=k,
    )
    write_policy = run_write_policy(args.write_policy, scenario, current_units)
    selected_memories = store.get_by_ids(read_selection["selected_memory_ids"])
    context = build_context(
        selected_memories,
        max_memories=args.max_memories,
        max_context_chars=args.max_context_chars,
    )
    preview = build_write_preview(
        current_units,
        write_policy.get("store_units", []),
        write_policy.get("skip_unit_ids", []),
    )
    return build_trace(
        scenario=scenario,
        current_units=current_units,
        retrieval=retrieval,
        read_selection=read_selection,
        write_policy=write_policy,
        context_builder=context,
        write_preview=preview,
    )


def compare_selectors(scenario: JsonDict) -> List[str]:
    selectors = [
        "no_memory",
        "all_candidates",
        "keyword_top_k",
        "random_k",
        "oracle_selected",
    ]
    if scenario.get("fixture_router_read_ids"):
        selectors.append("replay_router_selected")
    return selectors


def main() -> int:
    parser = argparse.ArgumentParser(description="Applied Memory Harness skeleton")
    parser.add_argument("--scenario-file", required=True)
    parser.add_argument("--memory-pool")
    parser.add_argument("--scenario-id")
    parser.add_argument("--read-selector", default="keyword_top_k")
    parser.add_argument("--write-policy", default="disabled", choices=["disabled", "fixture"])
    parser.add_argument("--max-memories", type=int, default=4)
    parser.add_argument("--max-context-chars", type=int, default=1600)
    parser.add_argument("--trace-out")
    parser.add_argument("--list-scenarios", action="store_true")
    parser.add_argument("--compare-all", action="store_true")
    args = parser.parse_args()

    scenarios = load_scenarios(args.scenario_file)
    if args.list_scenarios:
        for scenario in scenarios:
            print(f"{scenario['scenario_id']}\t{scenario.get('runtime_context', {}).get('task', '')}")
        return 0

    if not args.memory_pool:
        parser.error("--memory-pool is required unless --list-scenarios is used")

    if not args.scenario_id:
        parser.error("--scenario-id is required unless --list-scenarios is used")

    scenario = find_scenario(scenarios, args.scenario_id)

    if args.compare_all:
        runs = [run_once(args, scenario, selector) for selector in compare_selectors(scenario)]
        output = {"scenario_id": scenario["scenario_id"], "runs": runs}
        if not args.trace_out:
            print(json.dumps(output, indent=2, sort_keys=True))
        else:
            write_trace(args.trace_out, output)
        return 0

    trace = run_once(args, scenario, args.read_selector)
    if not args.trace_out:
        print(json.dumps(trace, indent=2, sort_keys=True))
    else:
        write_trace(args.trace_out, trace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
