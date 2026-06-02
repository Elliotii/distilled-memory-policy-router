"""Apply 4 independent-review fixes to batch500 rebalanced cases.

Fixes:
1. v05_batch100_0039 u1: service_memory → task_state (action-verb rule)
2. v05_batch50_0014 u3: repo_memory → task_state (implementation action)
3. v05_batch500_0096 u3: SKIP → repo_memory (explicit file path)
4. v05_batch500_0097 u3: SKIP → repo_memory (explicit file path)

Produces corrected cases JSONL. Does not modify input files.
"""

from __future__ import annotations

import json, sys
from pathlib import Path
from collections import Counter, OrderedDict

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.v04.case_validator import validate_case, validate_jsonl_file
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

INPUT_CASES = ROOT / "data/v05/batches/v05_batch500_rebalanced_cases.jsonl"
OUTPUT_CASES = ROOT / "data/v05/batches/v05_batch500_corrected_cases.jsonl"


# ── FIX DEFINITIONS ──────────────────────────────────────────────

FIXES = [
    # Fix 1: v05_batch100_0039 u1
    {
        "case_id": "v05_batch100_0039",
        "description": "Change u1 from service_memory to task_state (action-verb 'Add a grade appeal workflow...' per V05_LABEL_POLICY §7)",
        "apply": lambda case: _fix_1(case),
    },
    # Fix 2: v05_batch50_0014 u3
    {
        "case_id": "v05_batch50_0014",
        "description": "Change u3 from repo_memory to task_state (implementation action 'Add a priority field...')",
        "apply": lambda case: _fix_2(case),
    },
    # Fix 3: v05_batch500_0096 u3
    {
        "case_id": "v05_batch500_0096",
        "description": "Change u3 from SKIP to repo_memory (explicit file path docs/v05/scope_exclusions.md)",
        "apply": lambda case: _fix_3(case),
    },
    # Fix 4: v05_batch500_0097 u3
    {
        "case_id": "v05_batch500_0097",
        "description": "Change u3 from SKIP to repo_memory (explicit file path docs/planning/roadmap_2026_Q3.md)",
        "apply": lambda case: _fix_4(case),
    },
]


def _fix_1(case: dict) -> dict:
    """v05_batch100_0039: u1 service_memory -> task_state"""
    gold = case["gold"]
    # Update store
    for s in gold["store"]:
        if s["unit_id"] == "u1":
            s["target"] = "task_state"
    # Update DSL
    gold["dsl"] = (
        "READ m1,m2\n"
        "STORE task_state u1\n"
        "STORE service_memory u2\n"
        "STORE service_memory u3\n"
        "SKIP NONE"
    )
    # Update notes
    case["notes"] = (
        "READ+STORE joint. Reads m1 (current grading) and m2 (audit requirement). "
        "u1: 'Add a grade appeal workflow...' — action-verb per §7 → task_state. "
        "u2: appeals review rule — durable service behavior → service_memory. "
        "u3: grade audit logging — durable service behavior → service_memory."
    )
    return case


def _fix_2(case: dict) -> dict:
    """v05_batch50_0014: u3 repo_memory -> task_state"""
    gold = case["gold"]
    # Update store
    for s in gold["store"]:
        if s["unit_id"] == "u3":
            s["target"] = "task_state"
    # Update DSL
    gold["dsl"] = (
        "READ m1,m2\n"
        "STORE service_memory u1\n"
        "STORE task_state u3\n"
        "SKIP u2"
    )
    # Update notes
    case["notes"] = (
        "READ+STORE joint with user_profile memory and sensitive boundary. "
        "Reads m1 (notification behavior) and m2 (user preference). "
        "u1: durable CRITICAL priority bypass behavior → service_memory. "
        "u2: home address — personal/sensitive → SKIP. "
        "u3: 'Add a priority field...' — implementation action per §7 → task_state."
    )
    return case


def _fix_3(case: dict) -> dict:
    """v05_batch500_0096: u3 SKIP -> repo_memory"""
    gold = case["gold"]
    # Remove u3 from skip
    gold["skip"] = [u for u in gold["skip"] if u != "u3"]
    # Add u3 to store as repo_memory
    gold["store"].append({"target": "repo_memory", "unit_id": "u3"})
    # Update DSL
    gold["dsl"] = (
        "READ NONE\n"
        "STORE project_memory u1\n"
        "STORE repo_memory u3\n"
        "SKIP u2"
    )
    # Update notes
    case["notes"] = (
        "u1: project scope exclusion → project_memory. "
        "u2: proposes out-of-scope skill system → SKIP. "
        "u3: 'The documentation ... lives under docs/v05/scope_exclusions.md' — "
        "explicit file path → repo_memory."
    )
    return case


def _fix_4(case: dict) -> dict:
    """v05_batch500_0097: u3 SKIP -> repo_memory"""
    gold = case["gold"]
    # Remove u3 from skip
    gold["skip"] = [u for u in gold["skip"] if u != "u3"]
    # Add u3 to store as repo_memory
    gold["store"].append({"target": "repo_memory", "unit_id": "u3"})
    # Update DSL
    gold["dsl"] = (
        "READ NONE\n"
        "STORE task_state u2\n"
        "STORE repo_memory u3\n"
        "SKIP u1"
    )
    # Update notes
    case["notes"] = (
        "u1: speculative 'Maybe we should' → SKIP. "
        "u2: current state description → task_state. "
        "u3: 'The roadmap document is tracked in docs/planning/roadmap_2026_Q3.md' — "
        "explicit file path → repo_memory."
    )
    return case


# ── MAIN ─────────────────────────────────────────────────────────

def apply_fixes() -> tuple[list[dict], list[dict]]:
    """Load, fix, write, validate. Returns (all_cases, fix_log)."""
    # Load original
    with INPUT_CASES.open(encoding="utf-8") as f:
        original_cases = [json.loads(line) for line in f if line.strip()]
    print(f"Loaded {len(original_cases)} cases from rebalanced batch500")

    # Build lookup
    case_map = {c["case_id"]: c for c in original_cases}

    fix_log = []
    fixed_cases = list(original_cases)

    for fix_def in FIXES:
        cid = fix_def["case_id"]
        if cid not in case_map:
            print(f"ERROR: {cid} not found!")
            sys.exit(1)

        idx = next(i for i, c in enumerate(fixed_cases) if c["case_id"] == cid)
        before_dsl = fixed_cases[idx]["gold"]["dsl"]
        before_store = [f"{s['target']} {s['unit_id']}" for s in fixed_cases[idx]["gold"]["store"]]
        before_skip = fixed_cases[idx]["gold"]["skip"][:]

        # Deep copy and apply
        import copy
        case_copy = copy.deepcopy(fixed_cases[idx])
        fixed = fix_def["apply"](case_copy)
        fixed_cases[idx] = fixed

        after_dsl = fixed["gold"]["dsl"]
        after_store = [f"{s['target']} {s['unit_id']}" for s in fixed["gold"]["store"]]
        after_skip = fixed["gold"]["skip"][:]

        log_entry = {
            "case_id": cid,
            "description": fix_def["description"],
            "before": {"dsl": before_dsl, "store": before_store, "skip": before_skip},
            "after": {"dsl": after_dsl, "store": after_store, "skip": after_skip},
        }
        fix_log.append(log_entry)
        print(f"Fixed {cid}: {fix_def['description']}")

    # Write corrected cases
    with OUTPUT_CASES.open("w", encoding="utf-8") as f:
        for case in fixed_cases:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"Wrote {len(fixed_cases)} corrected cases to {OUTPUT_CASES}")

    return fixed_cases, fix_log


def validate_corrected(cases: list[dict]) -> dict:
    """Run comprehensive validation. Returns results dict."""
    results = {
        "structural": None,
        "dsl_parse": None,
        "canonical": None,
        "sensitive": None,
        "distribution": None,
        "fix_presence": None,
        "other_unchanged": None,
        "details": {},
    }

    # 1. Structural validation
    res = validate_jsonl_file(str(OUTPUT_CASES))
    results["structural"] = {"valid": res["valid"], "errors": res.get("errors", [])[:10]}
    print(f"Structural: {'PASS' if res['valid'] else 'FAIL'}")

    # 2. DSL parse + canonical consistency
    parse_errors = []
    canonical_errors = []
    for c in cases:
        dsl = c["gold"]["dsl"]
        mids = [m["memory_id"] for m in c["candidate_memories"]]
        uids = [u["unit_id"] for u in c["current_units"]]
        p = parse_policy_dsl(dsl, mids, uids, LEGAL_TARGETS)
        if not p["validation"]["valid"]:
            parse_errors.append(c["case_id"])
            continue
        pr = {i["memory_id"] for i in p["read"]}
        ps = {i["unit_id"]: i["target"] for i in p["store"]}
        pk = {i["unit_id"] for i in p["skip"]}
        gr = set(c["gold"]["read"])
        gs = {s["unit_id"]: s["target"] for s in c["gold"]["store"]}
        gk = set(c["gold"]["skip"])
        if pr != gr or ps != gs or pk != gk:
            canonical_errors.append(c["case_id"])
    results["dsl_parse"] = {"errors": parse_errors, "total": len(cases) - len(parse_errors)}
    results["canonical"] = {"errors": canonical_errors, "total": len(cases) - len(canonical_errors)}
    print(f"DSL parse: {results['dsl_parse']['total']}/{len(cases)}")
    print(f"Canonical: {results['canonical']['total']}/{len(cases)}")

    # 3. Target distribution
    targets = Counter()
    for c in cases:
        for s in c["gold"]["store"]:
            targets[s["target"]] += 1
    skip_count = sum(len(c["gold"]["skip"]) for c in cases)
    read_count = sum(len(c["gold"]["read"]) for c in cases)

    total_store = sum(targets.values())
    results["distribution"] = {
        "targets": dict(targets),
        "total_store": total_store,
        "total_read_entries": read_count,
        "total_skip_entries": skip_count,
    }

    # Shape distribution
    joint = sum(1 for c in cases if c["gold"]["read"] and c["gold"]["store"])
    store_only = sum(1 for c in cases if not c["gold"]["read"] and c["gold"]["store"])
    read_only = sum(1 for c in cases if c["gold"]["read"] and not c["gold"]["store"])
    results["distribution"]["shapes"] = {
        "READ+STORE joint": joint,
        "STORE/SKIP-only": store_only,
        "READ-only": read_only,
    }
    print(f"Target distribution: {dict(targets)}")
    print(f"Shape distribution: joint={joint}, store-only={store_only}, read-only={read_only}")

    # 4. Sensitive check
    sensitive_hits = []
    for c in cases:
        for s in c["gold"]["store"]:
            uid = s["unit_id"]
            unit = next(u for u in c["current_units"] if u["unit_id"] == uid)
            t = unit["text"].lower()
            for kw in ["password", "secret", "token", "api key", "credit card",
                       "webhook", "SSN", "private key", "phone number", "email", "recovery code"]:
                if kw in t:
                    # Check if it's a rule about the keyword
                    rule_indicators = ["must ", "should ", "never ", "requires ", "enforce",
                                       "policy", "convention", "stored in", "config", "path",
                                       "validate", "tokenize"]
                    if not any(p in t for p in rule_indicators):
                        sensitive_hits.append({"case_id": c["case_id"], "unit": uid, "text_preview": t[:100]})
    results["sensitive"] = {"hits": sensitive_hits, "count": len(sensitive_hits)}
    print(f"Sensitive stored: {len(sensitive_hits)}")

    # 5. Fix presence verification
    fix_ids = {"v05_batch100_0039", "v05_batch50_0014", "v05_batch500_0096", "v05_batch500_0097"}
    fix_found = {cid: False for cid in fix_ids}
    for c in cases:
        if c["case_id"] in fix_ids:
            fix_found[c["case_id"]] = True
    results["fix_presence"] = {"all_present": all(fix_found.values()), "details": fix_found}
    print(f"Fix presence: {fix_found}")

    # 6. Verify no other labels changed (compare against rebalanced)
    # We compare all cases except the 4 fixed ones
    with INPUT_CASES.open(encoding="utf-8") as f:
        original = [json.loads(line) for line in f if line.strip()]
    orig_map = {c["case_id"]: c for c in original}
    changed_others = []
    for c in cases:
        cid = c["case_id"]
        if cid in fix_ids:
            continue  # skip fixed ones
        orig = orig_map[cid]
        if c["gold"]["dsl"] != orig["gold"]["dsl"]:
            changed_others.append(cid)
    results["other_unchanged"] = {
        "count": len(changed_others),
        "case_ids": changed_others[:20],
    }
    print(f"Other cases with changed DSL: {len(changed_others)}")

    # 7. Verify the 4 fixes match expected
    expected_fixes = {
        "v05_batch100_0039": {
            "u1_target": "task_state",
            "has_u3_in_store": True,  # u3 should still be store
        },
        "v05_batch50_0014": {
            "u3_target": "task_state",
        },
        "v05_batch500_0096": {
            "u3_target": "repo_memory",
            "u3_not_in_skip": True,
        },
        "v05_batch500_0097": {
            "u3_target": "repo_memory",
            "u3_not_in_skip": True,
        },
    }
    fix_verify_errors = []
    for c in cases:
        cid = c["case_id"]
        if cid not in fix_ids:
            continue
        exp = expected_fixes[cid]
        store_by_unit = {s["unit_id"]: s["target"] for s in c["gold"]["store"]}
        skip_set = set(c["gold"]["skip"])

        if "u1_target" in exp:
            if store_by_unit.get("u1") != exp["u1_target"]:
                fix_verify_errors.append(f"{cid}: u1 target mismatch")
        if "u3_target" in exp:
            if store_by_unit.get("u3") != exp["u3_target"]:
                fix_verify_errors.append(f"{cid}: u3 target mismatch")
        if "u3_not_in_skip" in exp:
            if "u3" in skip_set:
                fix_verify_errors.append(f"{cid}: u3 still in skip")
    results["fix_verification"] = {"errors": fix_verify_errors}
    print(f"Fix verification errors: {len(fix_verify_errors)}")

    return results


# ── DISTRIBUTION COMPARISON ──────────────────────────────────────

def distribution_summary(cases: list[dict]) -> dict:
    """Compute full distribution summary."""
    targets = Counter()
    shapes = Counter()
    for c in cases:
        for s in c["gold"]["store"]:
            targets[s["target"]] += 1
        has_read = bool(c["gold"]["read"])
        has_store = bool(c["gold"]["store"])
        if has_read and has_store:
            shape = "joint"
        elif has_read:
            shape = "read-only"
        else:
            shape = "store-only"
        shapes[shape] += 1
    total_store = sum(targets.values())
    total_cases = len(cases)
    return {
        "cases": total_cases,
        "targets": dict(targets),
        "target_pct": {k: round(v / total_store * 100, 1) for k, v in targets.items()},
        "shapes": dict(shapes),
        "shape_pct": {k: round(v / total_cases * 100, 1) for k, v in shapes.items()},
        "total_store": total_store,
        "total_skip": sum(len(c["gold"]["skip"]) for c in cases),
        "total_read": sum(len(c["gold"]["read"]) for c in cases),
    }


if __name__ == "__main__":
    all_cases, fix_log = apply_fixes()
    results = validate_corrected(all_cases)

    # Print before/after distribution
    print("\n=== BEFORE (rebalanced) ===")
    with INPUT_CASES.open(encoding="utf-8") as f:
        orig = [json.loads(line) for line in f if line.strip()]
    before = distribution_summary(orig)
    for t in ["service_memory", "task_state", "repo_memory", "project_memory", "user_profile"]:
        print(f"  {t}: {before['targets'].get(t, 0)} ({before['target_pct'].get(t, 0)}%)")
    print(f"  SKIP units: {before['total_skip']}")

    print("\n=== AFTER (corrected) ===")
    after = distribution_summary(all_cases)
    for t in ["service_memory", "task_state", "repo_memory", "project_memory", "user_profile"]:
        print(f"  {t}: {after['targets'].get(t, 0)} ({after['target_pct'].get(t, 0)}%)")
    print(f"  SKIP units: {after['total_skip']}")

    print("\n=== NET CHANGES ===")
    for t in ["service_memory", "task_state", "repo_memory", "project_memory", "user_profile"]:
        before_v = before["targets"].get(t, 0)
        after_v = after["targets"].get(t, 0)
        delta = after_v - before_v
        print(f"  {t}: {before_v} → {after_v} ({delta:+d})")
    print(f"  SKIP units: {before['total_skip']} → {after['total_skip']} ({after['total_skip'] - before['total_skip']:+d})")

    # Overall pass/fail
    all_ok = (
        results["structural"]["valid"]
        and len(results["dsl_parse"]["errors"]) == 0
        and len(results["canonical"]["errors"]) == 0
        and results["sensitive"]["count"] == 0
        and results["fix_presence"]["all_present"]
        and results["other_unchanged"]["count"] == 0
        and len(results["fix_verification"]["errors"]) == 0
    )
    print(f"\n=== OVERALL: {'PASS' if all_ok else 'ISSUES FOUND'} ===")

    # Write fix log
    fix_log_path = ROOT / "data/v05/batches/v05_batch500_independent_review_fixes.jsonl"
    with fix_log_path.open("w", encoding="utf-8") as f:
        for entry in fix_log:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Fix log written to {fix_log_path}")
