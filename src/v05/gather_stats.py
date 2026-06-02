"""Quick stats gathering for report generation."""
import json
from collections import Counter

with open("data/v05/batches/v05_batch300_cases.jsonl") as f:
    cases = [json.loads(l) for l in f if l.strip()]
with open("data/v05/batches/v05_batch300_sft_messages.jsonl") as f:
    sfts = [json.loads(l) for l in f if l.strip()]
with open("data/v05/batches/v05_batch300_replacement51_cases.jsonl") as f:
    r51 = [json.loads(l) for l in f if l.strip()]

print(f"Cases: {len(cases)}, SFT: {len(sfts)}, R51: {len(r51)}")

targets = Counter()
total_skip = 0; total_read = 0
for c in cases:
    for s in c["gold"]["store"]: targets[s["target"]] += 1
    total_skip += len(c["gold"]["skip"])
    total_read += len(c["gold"]["read"])
total = sum(targets.values())

print(f"\n=== TARGETS ===")
for t in ["service_memory","task_state","repo_memory","project_memory","user_profile"]:
    v = targets.get(t,0)
    print(f"  {t}: {v} ({v/total*100:.1f}%)")
print(f"  Total STORE: {total}")
print(f"  Total SKIP: {total_skip}")
svc = targets.get("service_memory",0); task = targets.get("task_state",0)
print(f"  svc:task gap: {abs(svc/total - task/total)*100:.1f}pp")

shapes = Counter()
for c in cases:
    hr, hs = bool(c["gold"]["read"]), bool(c["gold"]["store"])
    shapes["READ+STORE" if (hr and hs) else ("READ-only" if hr else "STORE/SKIP")] += 1
print(f"\n=== SHAPES ===")
for k,v in shapes.most_common():
    print(f"  {k}: {v} ({v/300*100:.1f}%)")

all_tags = Counter()
for c in cases:
    for t in c["tags"]: all_tags[t] += 1
print(f"\n=== TAGS (top 20) ===")
for t,v in all_tags.most_common(20):
    print(f"  {t}: {v}")

domains = Counter()
for c in cases: domains[c["runtime_context"]["project"]] += 1
print(f"\n=== DOMAINS ===")
for d,v in domains.most_common():
    print(f"  {d}: {v}")

unit_texts = []; mem_texts = []
for c in cases:
    for u in c["current_units"]: unit_texts.append(u["text"])
    for m in c["candidate_memories"]: mem_texts.append(m["content"])
print(f"\n=== DUPLICATES ===")
print(f"  Duplicate unit texts: {len(unit_texts) - len(set(unit_texts))}")
print(f"  Duplicate memory texts: {len(mem_texts) - len(set(mem_texts))}")

generic_count = sum(1 for c in cases if c["runtime_context"].get("service") == "service")
print(f"  Generic placeholder 'service': {generic_count}")

ids = [c["case_id"] for c in cases]
print(f"  Duplicate case_ids: {len(ids) - len(set(ids))}")

# R51 analysis
r51_targets = Counter()
for c in r51:
    for s in c["gold"]["store"]: r51_targets[s["target"]] += 1
r51_total = sum(r51_targets.values())
print(f"\n=== R51 TARGETS ===")
print(f"  svc={r51_targets.get('service_memory',0)} task={r51_targets.get('task_state',0)} repo={r51_targets.get('repo_memory',0)} proj={r51_targets.get('project_memory',0)} user={r51_targets.get('user_profile',0)}")

r51_shapes = Counter()
for c in r51:
    hr, hs = bool(c["gold"]["read"]), bool(c["gold"]["store"])
    r51_shapes["READ+STORE" if (hr and hs) else ("READ-only" if hr else "STORE/SKIP")] += 1
print(f"\n=== R51 SHAPES ===")
print(f"  {dict(r51_shapes)}")

# SFT checks
sft_ok = all(s["messages"][2]["content"] == c["gold"]["dsl"] for s,c in zip(sfts, cases))
sft_no_md = all("```" not in s["messages"][2]["content"] for s in sfts)
sft_no_json = all(not s["messages"][2]["content"].strip().startswith("{") for s in sfts)
sft_not_final = all(not s["metadata"]["is_final_train_data"] for s in sfts)
print(f"\n=== SFT CHECKS ===")
print(f"  assistant==dsl: {'OK' if sft_ok else 'FAIL'}")
print(f"  no markdown: {'OK' if sft_no_md else 'FAIL'}")
print(f"  no JSON: {'OK' if sft_no_json else 'FAIL'}")
print(f"  is_final_train_data=false: {'OK' if sft_not_final else 'FAIL'}")

# Sensitive check
sensitive_kw = ["password","token","key","secret","phone","email","credit","ssn","passport","pin","recovery","webhook"]
sensitive_in_store = 0
for c in cases:
    for s in c["gold"]["store"]:
        uid = s["unit_id"]
        text = next(u["text"] for u in c["current_units"] if u["unit_id"] == uid)
        for kw in sensitive_kw:
            if kw in text.lower():
                is_false_pos = any(x in text.lower() for x in ["must use","does not store","policy","mask","centralized","credential","tokenized","tokenization","tokenize","identifier","alias",".md","yaml","config","reference","documentation","document","schema"])
                if is_false_pos: break
                print(f"  WARNING: sensitive in STORE: {c['case_id']} {uid}: {text[:100]}")
                sensitive_in_store += 1
                break
print(f"\n  Sensitive-looking units in STORE: {sensitive_in_store} (should be 0)")
