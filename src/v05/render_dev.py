"""Canonical v0.5 dev set writer and validator.

Reads the canonical dev cases JSONL, validates them, and generates SFT messages.

IMPORTANT: The canonical dev set lives in data/v05/dev/v05_dev_cases.jsonl.
This script does NOT generate dev cases from scratch. It reads the frozen
canonical JSONL. The original generation was done in Context 5.3-B and the
distribution was post-processed to match target ranges.

Usage:
  # Validate and write SFT messages (safe with --write flag)
  PYTHONDONTWRITEBYTECODE=1 python src/v05/render_dev.py --write

  # Validate only (no file writes)
  PYTHONDONTWRITEBYTECODE=1 python src/v05/render_dev.py

  # Write SFT messages only (does not touch cases)
  PYTHONDONTWRITEBYTECODE=1 python src/v05/render_dev.py --sft-only
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v04.case_validator import validate_case, validate_jsonl_file
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

# ── Paths ──────────────────────────────────────────────────────
CANONICAL_CASES = ROOT / "data/v05/dev/v05_dev_cases.jsonl"
CANONICAL_SFT = ROOT / "data/v05/dev/v05_dev_sft_messages.jsonl"
HASH_MANIFEST = ROOT / "reports/v05/v05_dev_hash_manifest.md"

SYSTEM_PROMPT = (
    "You are a memory policy router for coding-agent contexts.\n\n"
    "Task:\n"
    "Given RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:\n"
    "- which candidate memories to READ;\n"
    "- which current unit IDs to STORE and to which target;\n"
    "- which current unit IDs to SKIP.\n\n"
    "Output only the DSL. Do not include comments, prose, explanations, or JSON.\n\n"
    "Allowed DSL lines:\n"
    "READ <memory_id_list|NONE>\n"
    "STORE <target> <unit_id>\n"
    "STORE NONE\n"
    "SKIP <unit_id_list|NONE>\n\n"
    "Legal STORE targets:\n"
    "user_profile, project_memory, repo_memory, service_memory, task_state\n\n"
    "Rules:\n"
    "- READ useful memories only; skip merely related or stale ones.\n"
    "- STORE durable, reusable information with correct target.\n"
    "- SKIP sensitive, temporary, one-off, or out-of-scope content.\n"
    "- Every current unit must appear exactly once in STORE or SKIP.\n"
    "- Do not invent IDs, targets, or content."
)


def load_canonical() -> list[dict[str, Any]]:
    """Load canonical dev cases."""
    if not CANONICAL_CASES.exists():
        raise FileNotFoundError(
            f"Canonical dev cases not found at {CANONICAL_CASES}. "
            "This script reads the frozen canonical dev set; it does not generate cases."
        )
    with open(CANONICAL_CASES, encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]
    return cases


def compute_hash(path: Path) -> str:
    """SHA-256 hex digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_cases(cases: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    """Run full structural validation on all cases."""
    all_ok = True
    errors: list[str] = []

    # Case count
    if len(cases) != 100:
        all_ok = False
        errors.append(f"Expected 100 cases, got {len(cases)}")

    # Case IDs
    ids = [c["case_id"] for c in cases]
    expected = [f"v05_dev_{i:04d}" for i in range(1, 101)]
    if ids != expected:
        all_ok = False
        errors.append("Case ID sequence mismatch")

    # Per-case validation
    for case in cases:
        cid = case["case_id"]

        # Structural
        result = validate_case(case)
        if not result["valid"]:
            all_ok = False
            for e in result["errors"]:
                errors.append(f"{cid}: {e}")

        # DSL parse
        dsl = case["gold"]["dsl"]
        mem_ids = [m["memory_id"] for m in case["candidate_memories"]]
        unit_ids = [u["unit_id"] for u in case["current_units"]]
        parsed = parse_policy_dsl(dsl, mem_ids, unit_ids, LEGAL_TARGETS)
        if not parsed["validation"]["valid"]:
            all_ok = False
            for e in parsed["validation"]["errors"]:
                errors.append(f"{cid} DSL: {e}")

        # Canonical consistency
        parsed_read = {item["memory_id"] for item in parsed["read"]}
        parsed_store = {item["unit_id"]: item["target"] for item in parsed["store"]}
        parsed_skip = {item["unit_id"] for item in parsed["skip"]}
        gold_read = set(case["gold"]["read"])
        gold_store = {s["unit_id"]: s["target"] for s in case["gold"]["store"]}
        gold_skip = set(case["gold"]["skip"])

        if parsed_read != gold_read:
            all_ok = False
            errors.append(f"{cid} READ mismatch")
        if parsed_store != gold_store:
            all_ok = False
            errors.append(f"{cid} STORE mismatch")
        if parsed_skip != gold_skip:
            all_ok = False
            errors.append(f"{cid} SKIP mismatch")

        # Unit coverage
        store_units = {s["unit_id"] for s in case["gold"]["store"]}
        skip_units = set(case["gold"]["skip"])
        all_units = {u["unit_id"] for u in case["current_units"]}
        covered = store_units | skip_units
        both = store_units & skip_units
        missing = all_units - covered
        if both:
            all_ok = False
            errors.append(f"{cid} unit in both STORE and SKIP: {both}")
        if missing:
            all_ok = False
            errors.append(f"{cid} unit missing: {missing}")

        # READ IDs exist
        read_set = set(case["gold"]["read"])
        mem_set = {m["memory_id"] for m in case["candidate_memories"]}
        invalid_reads = read_set - mem_set
        if invalid_reads:
            all_ok = False
            errors.append(f"{cid} invalid READ IDs: {invalid_reads}")

        # STORE targets valid
        for s in case["gold"]["store"]:
            if s["target"] not in LEGAL_TARGETS:
                all_ok = False
                errors.append(f"{cid} invalid target: {s['target']}")
            if s["unit_id"] not in all_units:
                all_ok = False
                errors.append(f"{cid} invalid STORE unit_id: {s['unit_id']}")

        # Sensitive check
        sensitive_patterns = [
            "my password is", "my api key", "my phone number is", "my address is",
            "my passport", "my credit card", "my recovery code", "my backup email",
            "my personal email", "my mother's maiden", "webhook url is http",
        ]
        for s in case["gold"]["store"]:
            uid = s["unit_id"]
            for u in case["current_units"]:
                if u["unit_id"] == uid:
                    text = u["text"].lower()
                    for pat in sensitive_patterns:
                        if pat in text:
                            all_ok = False
                            errors.append(f"{cid} SENSITIVE STORE: {uid} contains '{pat}'")

    return all_ok, errors


def compute_distributions(cases: list[dict[str, Any]]) -> dict:
    """Compute distribution statistics."""
    total = len(cases)
    ro = sum(1 for c in cases if c["gold"]["read"] and not c["gold"]["store"])
    so = sum(1 for c in cases if not c["gold"]["read"] and c["gold"]["store"])
    rj = sum(1 for c in cases if c["gold"]["read"] and c["gold"]["store"])

    targets = [s["target"] for c in cases for s in c["gold"]["store"]]
    tc = Counter(targets)
    total_store_units = sum(tc.values())

    return {
        "total_cases": total,
        "read_only": ro,
        "store_skip_only": so,
        "read_store_joint": rj,
        "total_store_units": total_store_units,
        "total_skip_units": sum(len(c["gold"]["skip"]) for c in cases),
        "target_counts": dict(tc),
        "target_pcts": {t: c / total_store_units * 100 for t, c in tc.items()} if total_store_units else {},
    }


def build_sft_messages(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build SFT messages from cases."""

    def render_user_input(case: dict[str, Any]) -> str:
        rc = case["runtime_context"]
        context_lines = [
            "RUNTIME_CONTEXT",
            f"project: {rc['project']}",
            f"repo: {rc['repo']}",
            f"service: {rc['service']}",
            f"task: {rc['task']}",
        ]
        mems = case["candidate_memories"]
        if mems:
            mem_lines = ["CANDIDATE_MEMORIES"]
            for m in mems:
                mem_lines.append(f"{m['memory_id']} [{m['target']}]: {m['content']}")
        else:
            mem_lines = ["CANDIDATE_MEMORIES", "NONE"]
        units = case["current_units"]
        unit_lines = ["CURRENT_UNITS"]
        for u in units:
            unit_lines.append(f"{u['unit_id']}: {u['text']}")
        return "\n".join(context_lines + [""] + mem_lines + [""] + unit_lines)

    messages = []
    for case in cases:
        dsl = case["gold"]["dsl"]
        gold_store = case["gold"]["store"]
        has_read = bool(case["gold"]["read"])
        has_store = bool(gold_store)
        if has_read and has_store:
            shape = "READ + STORE joint"
        elif has_read:
            shape = "READ-only"
        elif has_store:
            shape = "STORE/SKIP-only"
        else:
            shape = "no READ and no STORE"

        msg = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": render_user_input(case)},
                {"role": "assistant", "content": dsl},
            ],
            "case_id": case["case_id"],
            "source": "v05_dev_dry_run",
            "metadata": {
                "tags": case["tags"],
                "num_candidate_memories": len(case["candidate_memories"]),
                "num_current_units": len(case["current_units"]),
                "gold_shape": shape,
                "store_targets": [s["target"] for s in gold_store],
                "is_final_train_data": False,
                "split": "dev",
            },
        }
        messages.append(msg)
    return messages


def validate_sft(cases: list[dict[str, Any]], messages: list[dict[str, Any]]) -> bool:
    """Validate SFT messages against cases."""
    ok = True
    for case, msg in zip(cases, messages):
        assistant = msg["messages"][2]["content"]
        if assistant != case["gold"]["dsl"]:
            print(f"  ❌ SFT ASSISTANT MISMATCH: {case['case_id']}")
            ok = False
        if "```" in assistant:
            print(f"  ❌ SFT MARKDOWN: {case['case_id']}")
            ok = False
        if assistant.strip().startswith("{"):
            print(f"  ❌ SFT JSON: {case['case_id']}")
            ok = False
        if msg["metadata"]["is_final_train_data"]:
            print(f"  ❌ is_final_train_data: {case['case_id']}")
            ok = False
        if msg["source"] != "v05_dev_dry_run":
            print(f"  ❌ source: {case['case_id']}")
            ok = False
        if msg["metadata"].get("split") != "dev":
            print(f"  ❌ split: {case['case_id']}")
            ok = False
    return ok


def write_hash_manifest(cases: list[dict[str, Any]]) -> None:
    """Write a hash manifest for the canonical dev set."""
    if CANONICAL_CASES.exists():
        cases_hash = compute_hash(CANONICAL_CASES)
    else:
        cases_hash = "N/A"

    lines = [
        "# V0.5 Dev Set Hash Manifest",
        "",
        f"**Date:** 2026-06-02",
        f"**Context:** 5.3-B2 — reproducibility cleanup",
        "",
        "## Canonical Files",
        "",
        "| File | SHA-256 |",
        "|------|---------|",
        f"| `data/v05/dev/v05_dev_cases.jsonl` | `{cases_hash}` |",
        "",
        "## Metadata",
        "",
        f"- Cases: {len(cases)}",
        f"- Case ID range: v05_dev_0001 – v05_dev_0100",
        f"- Source: Independently composed, post-processed for distribution balance",
        f"- render_dev.py: Frozen-data writer (reads canonical JSONL, validates, writes SFT)",
        "",
        "## Reproduction",
        "",
        "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python src/v05/render_dev.py --write",
        "```",
        "",
        "This reads the canonical `v05_dev_cases.jsonl`, validates all 100 cases,",
        "and writes `v05_dev_sft_messages.jsonl`.",
        "",
        "---",
        "",
        "*End of V0.5 Dev Hash Manifest.*",
    ]
    HASH_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    HASH_MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Hash manifest written to {HASH_MANIFEST}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Canonical v0.5 dev set writer and validator."
    )
    ap.add_argument(
        "--write", action="store_true",
        help="Write dev cases JSONL (normally not needed — canonical is frozen)"
    )
    ap.add_argument(
        "--sft-only", action="store_true",
        help="Write only SFT messages, do not touch cases"
    )
    args = ap.parse_args()

    print("Loading canonical dev cases...")
    cases = load_canonical()
    print(f"Loaded {len(cases)} cases from {CANONICAL_CASES}")

    # Validate
    print("\nValidating...")
    ok, errors = validate_cases(cases)
    if errors:
        for e in errors[:20]:
            print(f"  ❌ {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
    if not ok:
        print(f"\n❌ {len(errors)} validation errors — cannot proceed")
        return 1

    # JSONL file validation
    jsonl_ok = validate_jsonl_file(str(CANONICAL_CASES))
    if not jsonl_ok["valid"]:
        print(f"❌ JSONL file validation failed: {jsonl_ok['errors']}")
        return 1

    print("✅ All validations passed")

    # Distributions
    dist = compute_distributions(cases)
    print(f"\nDistribution: {dist['total_cases']} cases")
    print(f"  READ-only: {dist['read_only']} ({dist['read_only']/dist['total_cases']*100:.0f}%)")
    print(f"  STORE/SKIP-only: {dist['store_skip_only']} ({dist['store_skip_only']/dist['total_cases']*100:.0f}%)")
    print(f"  READ+STORE: {dist['read_store_joint']} ({dist['read_store_joint']/dist['total_cases']*100:.0f}%)")
    print(f"  STORE units: {dist['total_store_units']}")
    for t in ["service_memory", "task_state", "repo_memory", "project_memory", "user_profile"]:
        cnt = dist["target_counts"].get(t, 0)
        pct = dist["target_pcts"].get(t, 0)
        print(f"    {t}: {cnt} ({pct:.1f}%)")

    # Write cases only if --write
    if args.write:
        print(f"\nWriting cases to {CANONICAL_CASES}...")
        with open(CANONICAL_CASES, "w", encoding="utf-8") as f:
            for case in cases:
                f.write(json.dumps(case, ensure_ascii=False) + "\n")
        print("Done (canonical cases written).")
    elif args.sft_only:
        print("\nSkipping cases write (--sft-only mode).")
    else:
        print("\nSkipping cases write (use --write to overwrite).")

    # Always write SFT messages
    print(f"\nBuilding SFT messages...")
    messages = build_sft_messages(cases)
    with open(CANONICAL_SFT, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(messages)} SFT messages to {CANONICAL_SFT}")

    # Validate SFT
    print("Validating SFT messages...")
    if validate_sft(cases, messages):
        print("✅ SFT validation passed")
    else:
        print("❌ SFT validation failed")
        return 1

    # Hash manifest
    write_hash_manifest(cases)

    print("\n=== DEV SET REPRODUCIBILITY CHECK COMPLETE ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
