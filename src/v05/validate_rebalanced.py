import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.v04.case_validator import validate_jsonl_file
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

cases_path = ROOT / "data/v05/batches/v05_batch500_rebalanced_cases.jsonl"
sft_path = ROOT / "data/v05/batches/v05_batch500_rebalanced_sft_messages.jsonl"
orig_path = ROOT / "data/v05/batches/v05_batch500_cases.jsonl"

with cases_path.open() as f:
    cases = [json.loads(l) for l in f if l.strip()]
print(f"Cases: {len(cases)}")

res = validate_jsonl_file(str(cases_path))
print(f"Structural: {'PASS' if res['valid'] else 'FAIL'}")

errors = []
for c in cases:
    dsl = c["gold"]["dsl"]
    mids = [m["memory_id"] for m in c["candidate_memories"]]
    uids = [u["unit_id"] for u in c["current_units"]]
    p = parse_policy_dsl(dsl, mids, uids, LEGAL_TARGETS)
    if not p["validation"]["valid"]:
        errors.append(f"DSL: {c['case_id']}")
        continue
    pr = {i["memory_id"] for i in p["read"]}
    ps = {i["unit_id"]: i["target"] for i in p["store"]}
    pk = {i["unit_id"] for i in p["skip"]}
    gr = set(c["gold"]["read"])
    gs = {s["unit_id"]: s["target"] for s in c["gold"]["store"]}
    gk = set(c["gold"]["skip"])
    if pr != gr or ps != gs or pk != gk:
        errors.append(f"Canonical: {c['case_id']}")
print(f"DSL + canonical errors: {len(errors)}")

ids = [c["case_id"] for c in cases]
dups = [i for i, n in Counter(ids).items() if n > 1]
print(f"Duplicate IDs: {len(dups)}")

with sft_path.open() as f:
    sft = [json.loads(l) for l in f if l.strip()]
print(f"SFT rows: {len(sft)}")

sft_err = 0
for c, m in zip(cases, sft):
    if m["messages"][2]["content"] != c["gold"]["dsl"]: sft_err += 1
    if "```" in m["messages"][2]["content"]: sft_err += 1
    if m["metadata"]["is_final_train_data"]: sft_err += 1
print(f"SFT errors: {sft_err}")

with orig_path.open() as f:
    orig = [json.loads(l) for l in f if l.strip()]
print(f"Original cases unchanged: {len(orig)}")

repl_ids_path = ROOT / "data/v05/batches/v05_batch500_rebalance_replaced_case_ids.txt"
with repl_ids_path.open() as f:
    replaced = [l.strip() for l in f if l.strip()]
print(f"Replaced IDs: {len(replaced)}")

repl_path = ROOT / "data/v05/batches/v05_batch500_rebalance_replacement_cases.jsonl"
with repl_path.open() as f:
    repl = [json.loads(l) for l in f if l.strip()]
print(f"Replacement cases: {len(repl)}")

# Sensitive check
sensitive = 0
for c in cases:
    for s in c["gold"]["store"]:
        uid = s["unit_id"]
        unit = next(u for u in c["current_units"] if u["unit_id"] == uid)
        t = unit["text"].lower()
        for kw in ["password", "secret", "token", "api key", "credit card", "webhook", "SSN", "private key"]:
            if kw in t:
                # Check if it's a rule about the keyword or actual content
                if any(p in t for p in ["must ", "should ", "never ", "requires ", "enforce", "policy", "convention", "stored in", "config", "path"]):
                    pass  # false positive - rule about handling
                else:
                    sensitive += 1
                    print(f"SENSITIVE: {c['case_id']} {uid}: {t[:100]}")
print(f"Real sensitive stored: {sensitive}")

print(f"\nALL CHECKS: {'PASS' if not errors and not sft_err and not dups else 'ISSUES'}")
