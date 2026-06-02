"""Comprehensive validation script for batch500."""
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.v04.case_validator import validate_case, validate_jsonl_file
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

FILES = {
    'batch300': 'data/v05/batches/v05_batch300_cases.jsonl',
    'new200': 'data/v05/batches/v05_batch500_new200_cases.jsonl',
    'batch500': 'data/v05/batches/v05_batch500_cases.jsonl',
    'sft': 'data/v05/batches/v05_batch500_sft_messages.jsonl',
}

errors = []

# 1. Structural validation
for name, path in FILES.items():
    if name == 'sft':
        continue
    res = validate_jsonl_file(str(ROOT / path))
    status = 'PASS' if res['valid'] else 'FAIL'
    print(f'{name}: {status} ({res.get("record_count", "?")} cases)')
    if not res['valid']:
        for e in res['errors'][:5]:
            print(f'  ERROR: {e}')
            errors.append(f'{name}: {e}')

# 2. Load all data
with open(ROOT / FILES['batch300']) as f:
    batch300 = [json.loads(l) for l in f if l.strip()]
with open(ROOT / FILES['new200']) as f:
    new200 = [json.loads(l) for l in f if l.strip()]
with open(ROOT / FILES['batch500']) as f:
    batch500 = [json.loads(l) for l in f if l.strip()]
with open(ROOT / FILES['sft']) as f:
    sft = [json.loads(l) for l in f if l.strip()]

print(f'\nbatch300: {len(batch300)} cases')
print(f'new200: {len(new200)} cases')
print(f'batch500: {len(batch500)} cases')
print(f'SFT messages: {len(sft)}')

assert len(batch300) == 300, f'batch300 should be 300, got {len(batch300)}'
assert len(new200) == 200, f'new200 should be 200, got {len(new200)}'
assert len(batch500) == 500, f'batch500 should be 500, got {len(batch500)}'
assert len(sft) == 500, f'SFT should be 500, got {len(sft)}'

# 3. SFT integrity
for case, msg in zip(batch500, sft):
    assistant = msg['messages'][2]['content']
    if assistant != case['gold']['dsl']:
        errors.append(f'SFT assistant mismatch: {case["case_id"]}')
    if '```' in assistant:
        errors.append(f'SFT markdown: {case["case_id"]}')
    if assistant.strip().startswith('{'):
        errors.append(f'SFT JSON: {case["case_id"]}')
    if msg['metadata']['is_final_train_data']:
        errors.append(f'SFT is_final_train_data: {case["case_id"]}')

# 4. DSL parse + canonical consistency
for c in batch500:
    dsl = c['gold']['dsl']
    mem_ids = [m['memory_id'] for m in c['candidate_memories']]
    unit_ids = [u['unit_id'] for u in c['current_units']]
    parsed = parse_policy_dsl(dsl, mem_ids, unit_ids, LEGAL_TARGETS)
    if not parsed['validation']['valid']:
        errors.append(f'DSL parse fail: {c["case_id"]}')
        continue
    pr = {item['memory_id'] for item in parsed['read']}
    ps = {item['unit_id']: item['target'] for item in parsed['store']}
    pk = {item['unit_id'] for item in parsed['skip']}
    gr = set(c['gold']['read'])
    gs = {s['unit_id']: s['target'] for s in c['gold']['store']}
    gk = set(c['gold']['skip'])
    if pr != gr:
        errors.append(f'READ mismatch: {c["case_id"]}')
    if ps != gs:
        errors.append(f'STORE mismatch: {c["case_id"]}')
    if pk != gk:
        errors.append(f'SKIP mismatch: {c["case_id"]}')

# 5. ID uniqueness
all_ids = [c['case_id'] for c in batch500]
dup_ids = [i for i, n in Counter(all_ids).items() if n > 1]
if dup_ids:
    errors.append(f'Duplicate case_ids: {dup_ids}')

# 6. Unit text duplicates
unit_texts = [u['text'] for c in batch500 for u in c['current_units']]
dup_units = {t: n for t, n in Counter(unit_texts).items() if n > 1}
if dup_units:
    errors.append(f'Duplicate unit texts: {len(dup_units)}')

# 7. Memory text duplicates
mem_texts = [m['content'] for c in batch500 for m in c['candidate_memories']]
dup_mems = {t: n for t, n in Counter(mem_texts).items() if n > 1}
if dup_mems:
    print(f'Note: {len(dup_mems)} duplicate memory texts (may be benign)')

# 8. Sensitive content check
sensitive_patterns = ['password', 'secret', 'token', 'api key', 'private key', 'SSN', 'credit card', 'webhook']
sensitive_stored = []
for c in batch500:
    for s in c['gold']['store']:
        uid = s['unit_id']
        unit = next(u for u in c['current_units'] if u['unit_id'] == uid)
        text_lower = unit['text'].lower()
        for pat in sensitive_patterns:
            if pat in text_lower:
                sensitive_stored.append((c['case_id'], uid, pat))
if sensitive_stored:
    errors.append(f'Sensitive units STOREd: {len(sensitive_stored)}')
    for item in sensitive_stored:
        print(f'  SENSITIVE STORED: {item[0]} {item[1]}: "{item[2]}"')

# 9. Generic placeholder check
generic_rc = 0
for c in batch500:
    rc = c['runtime_context']
    for v in rc.values():
        if v in ['service', 'repo', 'project', 'task', '']:
            generic_rc += 1
if generic_rc:
    errors.append(f'Generic runtime_context values: {generic_rc}')

# 10. Subset50 / few-shot overlap
subset50_path = ROOT / 'data/v04/model_predictions/p5_subset50_case_ids.txt'
if subset50_path.exists():
    sub50_ids = set(subset50_path.read_text().strip().splitlines())
    overlap = set(all_ids) & sub50_ids
    if overlap:
        errors.append(f'Subset50 overlap: {overlap}')

fewshot_path = ROOT / 'data/v04/model_predictions/qwen3_4b_unit_dsl_fewshot_examples.jsonl'
if fewshot_path.exists():
    with fewshot_path.open() as f:
        fs_ids = {json.loads(l)['case_id'] for l in f if l.strip()}
    overlap = set(all_ids) & fs_ids
    if overlap:
        errors.append(f'Few-shot overlap: {overlap}')

# 11. Distribution summary
from collections import Counter as Ctr
targets = Ctr()
shapes = Ctr()
for c in batch500:
    for s in c['gold']['store']:
        targets[s['target']] += 1
    hr = bool(c['gold']['read'])
    hs = bool(c['gold']['store'])
    if hr and hs: shapes['read_store_joint'] += 1
    elif hr: shapes['read_only'] += 1
    else: shapes['store_skip_only'] += 1

print(f'\n=== BATCH500 FINAL DISTRIBUTION ===')
total_units = sum(targets.values())
for t, c in targets.most_common():
    print(f'  {t}: {c} ({c/total_units*100:.1f}%)')
print(f'  Total STORE units: {total_units}')
print(f'Shapes: {dict(shapes)}')
print(f'  read_store_joint: {shapes.get("read_store_joint",0)/500*100:.1f}%')
print(f'  store_skip_only: {shapes.get("store_skip_only",0)/500*100:.1f}%')
print(f'  read_only: {shapes.get("read_only",0)/500*100:.1f}%')

# 12. Final result
print(f'\n=== VALIDATION RESULT ===')
if errors:
    print(f'FAILED: {len(errors)} errors found')
    for e in errors[:20]:
        print(f'  {e}')
else:
    print('ALL CHECKS PASSED')
