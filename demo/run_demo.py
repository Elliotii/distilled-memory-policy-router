#!/usr/bin/env python3
"""Replay Memory Policy Router fixture cases.

This demo reads static JSON fixtures derived from locked gold and saved
prediction artifacts. It does not load models, call APIs, train, retrieve, or
write memory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INDEX = ROOT / "cases" / "index.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def policy_sets(policy: dict[str, Any]) -> tuple[set[str], set[tuple[str, str]], set[str]]:
    read = set(policy.get("read", []))
    store = {
        (item["unit_id"], item["target"])
        for item in policy.get("store", [])
        if "unit_id" in item and "target" in item
    }
    skip = set(policy.get("skip", []))
    return read, store, skip


def compare_policies(gold: dict[str, Any], predicted: dict[str, Any]) -> dict[str, Any]:
    gold_read, gold_store, gold_skip = policy_sets(gold)
    pred_read, pred_store, pred_skip = policy_sets(predicted)
    read_match = gold_read == pred_read
    store_match = gold_store == pred_store
    skip_match = gold_skip == pred_skip
    return {
        "read_exact_set_match": read_match,
        "store_unit_target_exact_set_match": store_match,
        "skip_exact_set_match": skip_match,
        "full_exact": read_match and store_match and skip_match,
        "read_missing": sorted(gold_read - pred_read),
        "read_extra": sorted(pred_read - gold_read),
        "store_missing": sorted([{"unit_id": u, "target": t} for u, t in gold_store - pred_store], key=lambda x: (x["unit_id"], x["target"])),
        "store_extra": sorted([{"unit_id": u, "target": t} for u, t in pred_store - gold_store], key=lambda x: (x["unit_id"], x["target"])),
        "skip_missing": sorted(gold_skip - pred_skip),
        "skip_extra": sorted(pred_skip - gold_skip),
    }


def fmt_bool(value: bool) -> str:
    return "yes" if value else "no"


def print_policy(label: str, policy: dict[str, Any]) -> None:
    print(f"{label}:")
    print(f"  READ:  {policy.get('read', [])}")
    store = policy.get("store", [])
    print("  STORE:")
    if store:
        for item in store:
            print(f"    - {item['unit_id']} -> {item['target']}")
    else:
        print("    - none")
    print(f"  SKIP:  {policy.get('skip', [])}")


def print_case(case: dict[str, Any]) -> dict[str, Any]:
    title = case.get("title", "Untitled case")
    case_id = case.get("case_id", "unknown")
    print(f"# {title}")
    print(f"case_id: {case_id}")
    print("mode: no-inference artifact replay")
    print()

    print("Candidate memories:")
    memories = case.get("candidate_memories", [])
    for memory in memories:
        print(f"  - {memory['memory_id']} [{memory.get('target', 'unknown')}]: {memory.get('text', '')}")
    print()

    print("Current units:")
    for unit in case.get("current_units", []):
        print(f"  - {unit['unit_id']}: {unit.get('text', '')}")
    print()

    gold = case.get("gold_policy", {})
    predicted = case.get("predicted_policy", {})
    print_policy("Gold policy", gold)
    print()
    print_policy("Predicted policy", predicted)
    print()

    comparison = compare_policies(gold, predicted)
    total_memories = len(memories)
    selected = len(set(predicted.get("read", [])))
    comparison["selected_memory_count"] = selected
    comparison["total_memory_count"] = total_memories

    print("Comparison:")
    print(f"  read exact set match:          {fmt_bool(comparison['read_exact_set_match'])}")
    print(f"  store unit+target exact match: {fmt_bool(comparison['store_unit_target_exact_set_match'])}")
    print(f"  skip exact set match:          {fmt_bool(comparison['skip_exact_set_match'])}")
    print(f"  full exact:                    {fmt_bool(comparison['full_exact'])}")
    print(f"  selected memories:             {selected}/{total_memories}")
    if comparison["read_missing"]:
        print(f"  missing READ ids:              {comparison['read_missing']}")
    if comparison["read_extra"]:
        print(f"  extra READ ids:                {comparison['read_extra']}")
    if comparison["store_missing"]:
        print(f"  missing STORE decisions:       {comparison['store_missing']}")
    if comparison["store_extra"]:
        print(f"  extra STORE decisions:         {comparison['store_extra']}")
    if comparison["skip_missing"]:
        print(f"  missing SKIP ids:              {comparison['skip_missing']}")
    if comparison["skip_extra"]:
        print(f"  extra SKIP ids:                {comparison['skip_extra']}")
    print()

    notes = case.get("notes", {})
    if notes:
        print("Notes:")
        for key in ("illustrates", "limitations"):
            if key in notes:
                print(f"  {key}: {notes[key]}")
    return comparison


def list_cases(index_path: Path = DEFAULT_INDEX) -> None:
    if not index_path.exists():
        raise FileNotFoundError(f"Missing index: {index_path}")
    index = load_json(index_path)
    cases = index.get("cases", [])
    print("Available demo cases:")
    for item in cases:
        print(f"  - {item['path']}: {item['title']} ({item['case_id']})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List available demo cases.")
    parser.add_argument("--case", type=Path, help="Path to a demo case JSON file.")
    parser.add_argument("--json-out", type=Path, help="Optional path to write comparison metrics JSON.")
    args = parser.parse_args()

    if args.list:
        list_cases()
        return 0
    if not args.case:
        parser.error("provide --list or --case")

    case = load_json(args.case)
    comparison = print_case(case)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(comparison, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote comparison JSON: {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

