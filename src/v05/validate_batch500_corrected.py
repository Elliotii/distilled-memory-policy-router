"""Validate corrected batch500 comprehensively.

Covers: structural, DSL parse, canonical consistency, SFT quality,
distribution, fix presence, no-label-drift, sensitive check.
"""

from __future__ import annotations

import json, sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.v04.case_validator import validate_jsonl_file
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS


def main():
    cases_path = ROOT / "data/v05/batches/v05_batch500_corrected_cases.jsonl"
    sft_path = ROOT / "data/v05/batches/v05_batch500_corrected_sft_messages.jsonl"
    reb_path = ROOT / "data/v05/batches/v05_batch500_rebalanced_cases.jsonl"

    with cases_path.open(encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]
    print(f"Corrected cases: {len(cases)}")

    # 1. Structural
    res = validate_jsonl_file(str(cases_path))
    print(f"[1] Structural: {'PASS' if res['valid'] else 'FAIL'}")
    if not res["valid"]:
        for e in res.get("errors", []):
            print(f"  {e}")

    # 2. DSL parse + canonical
    dsl_errors = []
    canon_errors = []
    for c in cases:
        dsl = c["gold"]["dsl"]
        mids = [m["memory_id"] for m in c["candidate_memories"]]
        uids = [u["unit_id"] for u in c["current_units"]]
        p = parse_policy_dsl(dsl, mids, uids, LEGAL_TARGETS)
        if not p["validation"]["valid"]:
            dsl_errors.append(c["case_id"])
            continue
        pr = {i["memory_id"] for i in p["read"]}
        ps = {i["unit_id"]: i["target"] for i in p["store"]}
        pk = {i["unit_id"] for i in p["skip"]}
        gr = set(c["gold"]["read"])
        gs = {s["unit_id"]: s["target"] for s in c["gold"]["store"]}
        gk = set(c["gold"]["skip"])
        if pr != gr or ps != gs or pk != gk:
            canon_errors.append(c["case_id"])
    print(f"[2] DSL parse: {len(cases) - len(dsl_errors)}/{len(cases)}")
    print(f"[3] Canonical: {len(cases) - len(canon_errors)}/{len(cases)}")

    # 3. SFT
    if sft_path.exists():
        with sft_path.open(encoding="utf-8") as f:
            sft = [json.loads(line) for line in f if line.strip()]
        print(f"[4] SFT rows: {len(sft)}")
        sft_err = 0
        for c, m in zip(cases, sft):
            if m["messages"][2]["content"] != c["gold"]["dsl"]:
                sft_err += 1
            if "```" in m["messages"][2]["content"]:
                sft_err += 1
            if m["metadata"]["is_final_train_data"]:
                sft_err += 1
        print(f"[5] SFT errors: {sft_err}")
    else:
        print("[4] SFT file not found (will regenerate)")

    # 4. Distribution
    targets = Counter()
    for c in cases:
        for s in c["gold"]["store"]:
            targets[s["target"]] += 1
    total_store = sum(targets.values())

    joint = sum(1 for c in cases if c["gold"]["read"] and c["gold"]["store"])
    store_only = sum(1 for c in cases if not c["gold"]["read"] and c["gold"]["store"])
    read_only = sum(1 for c in cases if c["gold"]["read"] and not c["gold"]["store"])

    print(f"\n[6] Target distribution:")
    for t in ["service_memory", "task_state", "repo_memory", "project_memory", "user_profile"]:
        v = targets.get(t, 0)
        pct = round(v / total_store * 100, 1) if total_store else 0
        print(f"  {t}: {v} ({pct}%)")
    print(f"  Total STORE: {total_store}")
    skip_count = sum(len(c["gold"]["skip"]) for c in cases)
    print(f"  Total SKIP: {skip_count}")

    print(f"\n[7] Shape distribution:")
    print(f"  READ+STORE joint: {joint} ({round(joint/len(cases)*100,1)}%)")
    print(f"  STORE/SKIP-only: {store_only} ({round(store_only/len(cases)*100,1)}%)")
    print(f"  READ-only: {read_only} ({round(read_only/len(cases)*100,1)}%)")

    # 5. Fix presence
    fix_ids = {"v05_batch100_0039", "v05_batch50_0014", "v05_batch500_0096", "v05_batch500_0097"}
    fix_checks = {}
    for c in cases:
        cid = c["case_id"]
        if cid == "v05_batch100_0039":
            u1_target = next((s["target"] for s in c["gold"]["store"] if s["unit_id"] == "u1"), None)
            fix_checks[cid] = u1_target == "task_state"
        elif cid == "v05_batch50_0014":
            u3_target = next((s["target"] for s in c["gold"]["store"] if s["unit_id"] == "u3"), None)
            fix_checks[cid] = u3_target == "task_state"
        elif cid == "v05_batch500_0096":
            u3_in_store = any(s["unit_id"] == "u3" for s in c["gold"]["store"])
            u3_in_skip = "u3" in c["gold"]["skip"]
            fix_checks[cid] = u3_in_store and not u3_in_skip
        elif cid == "v05_batch500_0097":
            u3_in_store = any(s["unit_id"] == "u3" for s in c["gold"]["store"])
            u3_in_skip = "u3" in c["gold"]["skip"]
            fix_checks[cid] = u3_in_store and not u3_in_skip
    print(f"\n[8] Fix presence: {fix_checks}")
    all_fixes_ok = all(fix_checks.values())

    # 6. No other labels changed
    with reb_path.open(encoding="utf-8") as f:
        reb = [json.loads(line) for line in f if line.strip()]
    reb_map = {c["case_id"]: c for c in reb}
    changed = []
    for c in cases:
        cid = c["case_id"]
        if cid in fix_ids:
            continue
        if cid in reb_map:
            if c["gold"]["dsl"] != reb_map[cid]["gold"]["dsl"]:
                changed.append(cid)
    print(f"\n[9] Other cases with DSL changes: {len(changed)}")
    if changed:
        print(f"  IDs: {changed[:10]}")

    # 7. Sensitive check
    sensitive = []
    for c in cases:
        for s in c["gold"]["store"]:
            uid = s["unit_id"]
            unit = next(u for u in c["current_units"] if u["unit_id"] == uid)
            t = unit["text"].lower()
            for kw in ["password", "secret", "token", "api key", "credit card",
                       "webhook", "SSN", "private key", "phone number", "recovery code"]:
                if kw in t:
                    rule_indicators = ["must ", "should ", "never ", "requires ", "enforce",
                                       "policy", "convention", "stored in", "config", "path",
                                       "validate", "tokenize", "JWT", "mask"]
                    if not any(p in t for p in rule_indicators):
                        sensitive.append(f"{c['case_id']} {uid}: {t[:100]}")
    print(f"\n[10] Actual sensitive stored: {len(sensitive)}")
    if sensitive:
        for s in sensitive:
            print(f"  {s}")

    # 8. Template / duplication check
    dup_texts = Counter()
    for c in cases:
        for u in c["current_units"]:
            dup_texts[u["text"]] += 1
    repeated = {t: n for t, n in dup_texts.items() if n > 1}
    print(f"\n[11] Repeated unit texts: {len(repeated)}")

    # Summary
    all_ok = (
        res["valid"]
        and len(dsl_errors) == 0
        and len(canon_errors) == 0
        and (not sft_path.exists() or sft_err == 0)
        and all_fixes_ok
        and len(changed) == 0
        and len(sensitive) == 0
        and len(cases) == 500
        and (not sft_path.exists() or len(sft) == 500)
    )
    print(f"\n=== SUMMARY: {'ALL PASS' if all_ok else 'ISSUES FOUND'} ===")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
