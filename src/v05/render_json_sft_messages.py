"""Render Unit JSON SFT messages from v0.5 train/dev cases for v0.5b LoRA.

Reads existing v0.5 case JSONL files (unchanged) and writes chat-style SFT
messages with assistant content in strict Unit JSON format.

Usage:
  python src/v05/render_json_sft_messages.py \
    --cases data/v05/train/subsets/v05_train_125_cases.jsonl \
    --out data/v05b/json_sft/v05b_train_125_json_sft_messages.jsonl \
    --source v05b_train_125
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v05.render_sft_messages import render_user_input


JSON_SYSTEM_PROMPT = (
    "You are a memory policy router for coding-agent contexts.\n\n"
    "Task:\n"
    "Given RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:\n"
    "- which candidate memories to READ;\n"
    "- which current unit IDs to STORE and to which target;\n"
    "- which current unit IDs to SKIP.\n\n"
    "Output only valid JSON. Do not include markdown fences, comments, prose, "
    "or explanations.\n\n"
    "Format:\n"
    '{\n'
    '  "read": ["m1", "m3"],\n'
    '  "store": [\n'
    '    {"target": "service_memory", "unit_id": "u1"},\n'
    '    {"target": "task_state", "unit_id": "u2"}\n'
    '  ],\n'
    '  "skip": ["u3"]\n'
    '}\n\n'
    "Legal STORE targets:\n"
    "user_profile, project_memory, repo_memory, service_memory, task_state\n\n"
    "Rules:\n"
    "- READ useful memories only; skip merely related or stale ones.\n"
    "- STORE durable, reusable information with correct target.\n"
    "- SKIP sensitive, temporary, one-off, or out-of-scope content.\n"
    "- Every current unit must appear exactly once in store or skip.\n"
    "- Do not invent IDs, targets, or content."
)

LEGAL_TARGETS = frozenset({
    "user_profile",
    "project_memory",
    "repo_memory",
    "service_memory",
    "task_state",
})


def build_json_assistant(case: dict[str, Any]) -> str:
    """Build the canonical Unit JSON assistant string from case gold."""
    gold = case["gold"]
    read = sorted(gold.get("read", []))  # canonical order: sorted for determinism
    store = gold.get("store", [])
    skip = sorted(gold.get("skip", []))

    # Build store entries with target and unit_id in case-consistent order
    unit_order = {u["unit_id"]: i for i, u in enumerate(case["current_units"])}
    store_entries = [
        {"target": s["target"], "unit_id": s["unit_id"]}
        for s in sorted(store, key=lambda s: unit_order.get(s["unit_id"], 999))
    ]

    payload = {
        "read": read,
        "store": store_entries,
        "skip": skip,
    }
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))


def build_json_sft_message(
    case: dict[str, Any],
    source: str,
) -> dict[str, Any]:
    """Build one SFT message with Unit JSON assistant."""
    gold = case["gold"]
    gold_store = gold.get("store", [])
    has_read = bool(gold.get("read", []))
    has_store = bool(gold_store)

    if has_read and has_store:
        shape = "READ + STORE joint"
    elif has_read:
        shape = "READ-only"
    elif has_store:
        shape = "STORE/SKIP-only"
    else:
        shape = "no READ and no STORE"

    return {
        "messages": [
            {"role": "system", "content": JSON_SYSTEM_PROMPT},
            {"role": "user", "content": render_user_input(case)},
            {"role": "assistant", "content": build_json_assistant(case)},
        ],
        "case_id": case["case_id"],
        "source": source,
        "metadata": {
            "tags": case.get("tags", []),
            "num_candidate_memories": len(case.get("candidate_memories", [])),
            "num_current_units": len(case.get("current_units", [])),
            "gold_shape": shape,
            "store_targets": [s["target"] for s in gold_store],
            "is_final_train_data": False,
        },
    }


def validate_json_sft_message(
    case: dict[str, Any],
    msg: dict[str, Any],
    case_index: int,
) -> list[str]:
    """Validate a single JSON SFT message. Returns list of error strings."""
    errors: list[str] = []
    case_id = case.get("case_id", f"index {case_index}")

    # 1. Assistant parses as JSON
    assistant = msg["messages"][2]["content"]
    try:
        parsed = json.loads(assistant)
    except json.JSONDecodeError as e:
        errors.append(f"{case_id}: assistant is not valid JSON: {e}")
        return errors

    # 2. No markdown/prose in assistant
    if "```" in assistant:
        errors.append(f"{case_id}: assistant contains markdown fence")

    # 3. Check required keys
    for key in ("read", "store", "skip"):
        if key not in parsed:
            errors.append(f"{case_id}: assistant missing key '{key}'")
    if errors:
        return errors

    # 4. read must be array of strings
    if not isinstance(parsed["read"], list):
        errors.append(f"{case_id}: 'read' must be a list")
    else:
        valid_mem_ids = {m["memory_id"] for m in case.get("candidate_memories", [])}
        for i, rid in enumerate(parsed["read"]):
            if not isinstance(rid, str):
                errors.append(f"{case_id}: read[{i}] must be a string")
            elif rid not in valid_mem_ids:
                errors.append(f"{case_id}: read[{i}]='{rid}' not in candidate_memories")

    # 5. store must be array of objects with valid target/unit_id
    if not isinstance(parsed["store"], list):
        errors.append(f"{case_id}: 'store' must be a list")
    else:
        valid_unit_ids = {u["unit_id"] for u in case.get("current_units", [])}
        seen_units: set[str] = set()
        for i, item in enumerate(parsed["store"]):
            if not isinstance(item, dict):
                errors.append(f"{case_id}: store[{i}] must be an object")
                continue
            target = item.get("target")
            unit_id = item.get("unit_id")
            if target not in LEGAL_TARGETS:
                errors.append(f"{case_id}: store[{i}].target='{target}' is illegal")
            if not isinstance(unit_id, str) or not unit_id:
                errors.append(f"{case_id}: store[{i}].unit_id must be non-empty string")
            elif unit_id not in valid_unit_ids:
                errors.append(f"{case_id}: store[{i}].unit_id='{unit_id}' not in current_units")
            elif unit_id in seen_units:
                errors.append(f"{case_id}: duplicate store unit_id '{unit_id}'")
            else:
                seen_units.add(unit_id)

    # 6. skip must be array of strings
    if not isinstance(parsed["skip"], list):
        errors.append(f"{case_id}: 'skip' must be a list")
    else:
        valid_unit_ids = {u["unit_id"] for u in case.get("current_units", [])}
        seen_skip: set[str] = set()
        for i, uid in enumerate(parsed["skip"]):
            if not isinstance(uid, str):
                errors.append(f"{case_id}: skip[{i}] must be a string")
            elif uid not in valid_unit_ids:
                errors.append(f"{case_id}: skip[{i}]='{uid}' not in current_units")
            elif uid in seen_skip:
                errors.append(f"{case_id}: duplicate skip unit_id '{uid}'")
            else:
                seen_skip.add(uid)

    # 7. Unit coverage: every unit exactly once in store or skip
    if not errors:
        store_ids = {s.get("unit_id") for s in parsed["store"] if isinstance(s, dict)}
        skip_ids = set(parsed["skip"]) if isinstance(parsed["skip"], list) else set()
        all_units = {u["unit_id"] for u in case.get("current_units", [])}
        assigned = store_ids | skip_ids
        missing = all_units - assigned
        overlap = store_ids & skip_ids
        if missing:
            errors.append(f"{case_id}: missing unit assignment: {sorted(missing)}")
        if overlap:
            errors.append(f"{case_id}: unit in both store and skip: {sorted(overlap)}")

    # 8. Canonical consistency: parsed JSON must equal structured gold
    gold = case["gold"]
    gold_read = set(gold.get("read", []))
    gold_store = {(s["target"], s["unit_id"]) for s in gold.get("store", [])}
    gold_skip = set(gold.get("skip", []))

    parsed_read = set(parsed.get("read", []) if isinstance(parsed.get("read"), list) else [])
    parsed_store = {
        (s["target"], s["unit_id"])
        for s in (parsed.get("store") if isinstance(parsed.get("store"), list) else [])
        if isinstance(s, dict)
    }
    parsed_skip = set(parsed.get("skip", []) if isinstance(parsed.get("skip"), list) else [])

    if parsed_read != gold_read:
        errors.append(f"{case_id}: read mismatch: parsed={sorted(parsed_read)} gold={sorted(gold_read)}")
    if parsed_store != gold_store:
        errors.append(f"{case_id}: store mismatch")
    if parsed_skip != gold_skip:
        errors.append(f"{case_id}: skip mismatch: parsed={sorted(parsed_skip)} gold={sorted(gold_skip)}")

    return errors


def render_json_sft(cases_path: str, out_path: str, source: str) -> int:
    """Read cases from JSONL, build JSON SFT messages, validate, write."""
    with open(cases_path, encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]
    print(f"Loaded {len(cases)} cases from {cases_path}")

    messages = []
    all_errors: list[str] = []
    for case in cases:
        msg = build_json_sft_message(case, source)
        messages.append(msg)

    # Validate all messages
    for i, (case, msg) in enumerate(zip(cases, messages)):
        errs = validate_json_sft_message(case, msg, i)
        all_errors.extend(errs)

    if all_errors:
        print(f"\nVALIDATION FAILED: {len(all_errors)} error(s)")
        for e in all_errors[:20]:
            print(f"  {e}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more")
        return 1

    # Write output
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(messages)} JSON SFT messages to {out_path}")
    print("All validations passed")
    return 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Render Unit JSON SFT messages from v0.5 case files."
    )
    ap.add_argument("--cases", required=True, help="Path to input cases JSONL")
    ap.add_argument("--out", required=True, help="Output path for JSON SFT messages JSONL")
    ap.add_argument("--source", default="v05b_json_sft", help="Source tag for metadata")
    args = ap.parse_args()

    return render_json_sft(args.cases, args.out, args.source)


if __name__ == "__main__":
    sys.exit(main())
