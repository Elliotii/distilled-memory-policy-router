"""DeepSeek independent audit of v05g repaired training data.
Read-only audit - does not modify any data files.
"""
import json, hashlib, re, sys, random
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path('/home/abc16/distilled-memory-policy-router')

def load(path):
    return [json.loads(l) for l in open(path) if l.strip()]

def hdr(title):
    print()
    print('=' * 70)
    print(title)
    print('=' * 70)

add_cases = load(ROOT / 'data/v05g/cases/v05g_train_additional_500_targeted_cases.jsonl')
ctl_cases = load(ROOT / 'data/v05g/cases/v05g_train_500_control_cases.jsonl')
c1000_cases = load(ROOT / 'data/v05g/cases/v05g_train_1000_targeted_cases.jsonl')

# ===================================================================
# 3. READ REPAIR AUDIT
# ===================================================================
hdr('3. READ REPAIR AUDIT')

stale_reads = 0
distractor_reads = 0
non_stale_not_read_no_reason = 0
non_recoverable_reads = 0
total_read_events = 0
read_by_type = defaultdict(lambda: {'total': 0, 'read': 0})

for c in add_cases:
    ctx = c.get('runtime_context', {})
    service = ctx.get('service', '').lower()
    repo = ctx.get('repo', '').lower()

    gold_read = set(c['gold'].get('read', []))
    store_targets = [s['target'] for s in c['gold'].get('store', [])]
    has_user_stores = 'user_profile' in store_targets

    for m in c.get('candidate_memories', []):
        mid = m['memory_id']
        text = m.get('text', m.get('content', ''))
        text_lower = text.lower()
        m_tags = m.get('tags', [])
        m_type = m.get('target', '')

        read_by_type[m_type]['total'] += 1

        is_stale = ('stale' in m_tags)

        mid_is_read = mid in gold_read
        if mid_is_read:
            total_read_events += 1
            read_by_type[m_type]['read'] += 1

        if is_stale and mid_is_read:
            stale_reads += 1
            print('  STALE READ: {} {} mtype={}: {}'.format(c['case_id'], mid, m_type, text[:100]))

        # Determine if this memory is a distractor based on visible semantics
        mentions_service = service and service in text_lower
        mentions_repo = repo and repo in text_lower

        is_distractor = (
            'distractor' in m_tags or
            m_type == 'project_memory' or
            (m_type == 'service_memory' and service and not mentions_service) or
            (m_type == 'repo_memory' and repo and not mentions_repo)
        )

        if is_distractor and mid_is_read:
            distractor_reads += 1
            print('  DISTRACTOR READ: {} {} mtype={}: {}'.format(c['case_id'], mid, m_type, text[:100]))

        # Rule: eligible for READ = non-stale AND (mentions current service/repo OR is user_profile with user stores)
        eligible_for_read = (
            not is_stale and (
                mentions_service or mentions_repo or
                (m_type == 'user_profile' and has_user_stores)
            )
        )

        if not is_stale and not mid_is_read and eligible_for_read:
            non_stale_not_read_no_reason += 1
            print('  NO-REASON NOT-READ: {} {} mtype={}'.format(c['case_id'], mid, m_type))
            print('    svc={} repo={} has_user={} mentions_svc={} mentions_repo={}'.format(
                service, repo, has_user_stores, mentions_service, mentions_repo))
            print('    text: {}'.format(text[:120]))

        if mid_is_read and not eligible_for_read:
            if not is_stale:
                non_recoverable_reads += 1
                print('  UNRECOVERABLE READ: {} {} mtype={}'.format(c['case_id'], mid, m_type))
                print('    svc={} repo={} has_user={} mentions_svc={} mentions_repo={}'.format(
                    service, repo, has_user_stores, mentions_service, mentions_repo))
                print('    text: {}'.format(text[:120]))

print()
print('--- READ Hard Gates ---')
print('Total READ events: {}'.format(total_read_events))
print('Stale reads: {} (must be 0)'.format(stale_reads))
print('Distractor reads: {} (must be 0)'.format(distractor_reads))
print('Non-stale not-read no reason: {} (must be 0)'.format(non_stale_not_read_no_reason))
print('Non-recoverable reads: {} (must be 0)'.format(non_recoverable_reads))

print()
print('--- READ Rates by Memory Type ---')
for mtype in sorted(read_by_type.keys()):
    d = read_by_type[mtype]
    rate = 100 * d['read'] / max(1, d['total'])
    print('  {}: {}/{} READ ({:.1f}%)'.format(mtype, d['read'], d['total'], rate))

print()
print('--- READ Rule Mechanical Assessment ---')
pm = read_by_type.get('project_memory', {'total': 1, 'read': 0})
print('project_memory READ rate: {:.1f}% (cross-domain distractor - READ=0% by design)'.format(100 * pm['read'] / pm['total']))
up = read_by_type.get('user_profile', {'total': 1, 'read': 0})
print('user_profile READ rate: {:.1f}% ({}/{})'.format(100 * up['read'] / up['total'], up['read'], up['total']))

read_ok = (stale_reads == 0 and distractor_reads == 0 and
           non_stale_not_read_no_reason == 0 and non_recoverable_reads == 0)
print('READ repair verdict: {}'.format('ALL PASS' if read_ok else 'FAIL'))

# ===================================================================
# 4. PREFIX SHORTCUT AUDIT
# ===================================================================
hdr('4. PREFIX SHORTCUT AUDIT')

def first_n_words(text, n=3):
    words = text.split()
    return ' '.join(words[:n]).lower()

prefix_binary = defaultdict(set)
prefix_multiclass = defaultdict(set)
prefix_examples = defaultdict(list)

for c in add_cases:
    store_uids = {s['unit_id'] for s in c['gold'].get('store', [])}
    skip_uids = set(c['gold'].get('skip', []))
    store_targets = {s['unit_id']: s['target'] for s in c['gold'].get('store', [])}

    for u in c.get('current_units', []):
        uid = u['unit_id']
        text = u.get('text', u.get('content', ''))
        prefix = first_n_words(text, 3)
        if uid in store_uids:
            target = store_targets[uid]
            prefix_binary[prefix].add('STORE')
            prefix_multiclass[prefix].add('STORE({})'.format(target))
        elif uid in skip_uids:
            prefix_binary[prefix].add('SKIP')
            prefix_multiclass[prefix].add('SKIP')
        else:
            prefix_binary[prefix].add('UNASSIGNED')
            prefix_multiclass[prefix].add('UNASSIGNED')
        prefix_examples[prefix].append({
            'case_id': c['case_id'], 'unit_id': uid,
            'text': text[:120],
            'label': 'STORE({})'.format(store_targets[uid]) if uid in store_uids else 'SKIP'
        })

total_units = sum(len(v) for v in prefix_examples.values())
total_prefixes = len(prefix_binary)
ambiguous_binary = sum(1 for labels in prefix_binary.values() if len(labels) > 1)
ambiguous_multi = sum(1 for labels in prefix_multiclass.values() if len(labels) > 1)

correct_binary = sum(len(prefix_examples[p]) for p, labels in prefix_binary.items() if len(labels) == 1)
correct_multi = sum(len(prefix_examples[p]) for p, labels in prefix_multiclass.items() if len(labels) == 1)

binary_pct = 100 * correct_binary / max(1, total_units)
multi_pct = 100 * correct_multi / max(1, total_units)

print('Total units: {}'.format(total_units))
print('Unique 3-word prefixes: {}'.format(total_prefixes))
print('Ambiguous prefixes (binary STORE/SKIP): {}'.format(ambiguous_binary))
print('Ambiguous prefixes (multi-class): {}'.format(ambiguous_multi))
print('Binary 3-word-prefix accuracy: {:.1f}%'.format(binary_pct))
print('Multi-class 3-word-prefix accuracy: {:.1f}%'.format(multi_pct))

print()
print('--- Ambiguous Binary Prefixes ({}) ---'.format(ambiguous_binary))
for prefix in sorted(prefix_binary.keys()):
    labels = prefix_binary[prefix]
    if len(labels) > 1:
        examples = prefix_examples[prefix]
        lc = Counter(ex['label'] for ex in examples)
        print('  [{}]: {} units, labels={}'.format(prefix, len(examples), dict(lc)))
        for ex in examples[:3]:
            print('    {}: {}...'.format(ex['label'], ex['text'][:100]))

body_dependent_cases = set()
for prefix, labels in prefix_binary.items():
    if len(labels) > 1:
        for ex in prefix_examples[prefix]:
            body_dependent_cases.add(ex['case_id'])

print()
print('Body-dependent cases: {}/500 ({:.1f}%)'.format(len(body_dependent_cases), 100*len(body_dependent_cases)/500))

# ===================================================================
# 5. SENSITIVE LITERAL AUDIT
# ===================================================================
hdr('5. SENSITIVE LITERAL AUDIT')

sensitive_texts = []
sensitive_in_store = 0
all_sensitive = 0

for c in add_cases:
    store_uids = {s['unit_id'] for s in c['gold'].get('store', [])}
    for u in c.get('current_units', []):
        tags = u.get('tags', [])
        if any('sensitive' in t for t in tags):
            all_sensitive += 1
            text = u.get('text', u.get('content', ''))
            sensitive_texts.append(text)
            if u['unit_id'] in store_uids:
                sensitive_in_store += 1

tc = Counter(sensitive_texts)
unique_texts = len(tc)
max_repeated = max(tc.values()) if tc else 0
repeated_2x = sum(1 for v in tc.values() if v == 2)
repeated_1x = sum(1 for v in tc.values() if v == 1)

print('Total sensitive units: {}'.format(all_sensitive))
print('Unique sensitive texts: {}'.format(unique_texts))
print('Max repeated: {}x'.format(max_repeated))
print('Texts at 1x: {}, at 2x: {}'.format(repeated_1x, repeated_2x))
print('Sensitive in STORE (add 500): {} (must be 0)'.format(sensitive_in_store))

if max_repeated > 2:
    print('Texts repeated >2x:')
    for text, count in tc.most_common():
        if count > 2:
            print('  {}x: {}...'.format(count, text[:80]))

sensitive_store_c1000 = 0
for c in c1000_cases:
    store_uids = {s['unit_id'] for s in c['gold'].get('store', [])}
    for u in c.get('current_units', []):
        if any('sensitive' in t for t in u.get('tags', [])):
            if u['unit_id'] in store_uids:
                sensitive_store_c1000 += 1
print('Sensitive in STORE (c1000): {} (must be 0)'.format(sensitive_store_c1000))

sensitive_ok = (sensitive_in_store == 0 and max_repeated <= 2)

# ===================================================================
# 6. QUALITY GATES
# ===================================================================
hdr('6. QUALITY GATES (RECOMPUTED)')

legal_targets = {'task_state', 'service_memory', 'repo_memory', 'project_memory', 'user_profile'}
gates = {}

# SFT parse
sft_errors = 0
for fn in ['json_sft/v05g_train_additional_500_targeted_json_sft_messages.jsonl',
           'json_sft/v05g_train_1000_targeted_json_sft_messages.jsonl']:
    for row in load(ROOT / 'data/v05g' / fn):
        msgs = row.get('messages', [])
        if len(msgs) != 3:
            sft_errors += 1
            continue
        try:
            json.loads(msgs[2]['content'])
        except:
            sft_errors += 1
gates['SFT JSON parse=100%'] = (sft_errors == 0, sft_errors)

# Unit coverage
unassigned = 0
for c in c1000_cases:
    all_uids = {u['unit_id'] for u in c.get('current_units', [])}
    assigned = {s['unit_id'] for s in c['gold'].get('store', [])} | set(c['gold'].get('skip', []))
    if all_uids != assigned:
        unassigned += 1
gates['unit coverage=100%'] = (unassigned == 0, unassigned)

# Mutually exclusive
both = 0
for c in c1000_cases:
    s = {s['unit_id'] for s in c['gold'].get('store', [])}
    k = set(c['gold'].get('skip', []))
    if s & k:
        both += 1
gates['store/skip exclusive'] = (both == 0, both)

# Sensitive STORE
gates['sensitive STORE=0'] = (sensitive_store_c1000 == 0, sensitive_store_c1000)

# No target:skip
ts = 0
for c in c1000_cases:
    for s in c['gold'].get('store', []):
        if s.get('target') == 'skip':
            ts += 1
gates['no target:skip'] = (ts == 0, ts)

# No duplicate
dup = 0
for c in c1000_cases:
    uids = [s['unit_id'] for s in c['gold'].get('store', [])]
    if len(uids) != len(set(uids)):
        dup += 1
gates['no dup assignment'] = (dup == 0, dup)

# Valid targets
it = 0
for c in c1000_cases:
    for s in c['gold'].get('store', []):
        if s.get('target') not in legal_targets:
            it += 1
gates['valid targets'] = (it == 0, it)

# Valid IDs
bad_ids = 0
for c in c1000_cases:
    mids = {m['memory_id'] for m in c.get('candidate_memories', [])}
    uids = {u['unit_id'] for u in c.get('current_units', [])}
    for rid in c['gold'].get('read', []):
        if rid not in mids:
            bad_ids += 1
    for s in c['gold'].get('store', []):
        if s['unit_id'] not in uids:
            bad_ids += 1
    for sid in c['gold'].get('skip', []):
        if sid not in uids:
            bad_ids += 1
gates['valid IDs'] = (bad_ids == 0, bad_ids)

# Placeholders
ph = 0
for c in add_cases:
    for u in c.get('current_units', []):
        if re.search(r'\{vocab_item\}', u.get('text', u.get('content', ''))):
            ph += 1
    for m in c.get('candidate_memories', []):
        if re.search(r'\{vocab_item\}', m.get('text', m.get('content', ''))):
            ph += 1
gates['no placeholders'] = (ph == 0, ph)

for gname in sorted(gates.keys()):
    result, count = gates[gname]
    status = 'PASS' if result else 'FAIL'
    print('  {}: {} ({})'.format(gname, status, count))

all_gates = all(v[0] for v in gates.values())
print('Quality gates combined: {}'.format('ALL PASS' if all_gates else 'FAIL'))

# ===================================================================
# 7. SEMANTIC SPOT-CHECK
# ===================================================================
hdr('7. SEMANTIC SPOT-CHECK (100-case sample)')

random.seed(42)
sample = random.sample(add_cases, min(100, len(add_cases)))

target_mismatches = 0
hard_skip_issues = 0

tkw_map = {
    'task_state': ['issue', 'blocker', 'debug', 'investigat', 'error', 'deploy',
                   'rollout', 'incident', 'outage', 'fix', 'active', 'broken', 'failing', 'down'],
    'service_memory': ['guarantees', 'uptime', 'architecture', 'design', 'protocol',
                       'api', 'endpoint', 'service', 'threshold', 'latency', 'throughput', 'sla'],
    'repo_memory': ['run', 'make', 'build', 'test', 'ci', 'pr', 'commit', 'branch',
                    'lint', 'deploy script', 'bench', 'dockerfile'],
    'project_memory': ['security review', 'audit', 'quarterly', 'compliance',
                       'review cycle', 'standup', 'sprint', 'bi-weekly', 'retrospective'],
    'user_profile': ['prefer', 'pronoun', 'timezone', 'notif', 'contact', 'setting',
                     'profile', 'preference', 'theme', 'dark mode', 'language'],
}

for c in sample:
    for s in c['gold'].get('store', []):
        target = s['target']
        uid = s['unit_id']
        unit_text = ''
        for u in c.get('current_units', []):
            if u['unit_id'] == uid:
                unit_text = u.get('text', u.get('content', '')).lower()
                break
        if target in tkw_map:
            has_kw = any(kw in unit_text for kw in tkw_map[target])
            if not has_kw:
                target_mismatches += 1

    for uid in c['gold'].get('skip', []):
        unit_text = ''
        unit_tags = []
        for u in c.get('current_units', []):
            if u['unit_id'] == uid:
                unit_text = u.get('text', u.get('content', '')).lower()
                unit_tags = u.get('tags', [])
                break
        is_sensitive = any('sensitive' in t for t in unit_tags)
        has_resolved = any(kw in unit_text for kw in [
            'resolved', 'rollback', 'reverted', 'closed', 'wontfix',
            'wont fix', 'obsolete', 'no longer', 'completed', 'fully resolved',
            'traced to a now-resolved'])
        has_stale = any(kw in unit_text for kw in [
            'deprecated', 'archived', 'legacy', 'discontinued', 'sunset', 'retired'])
        has_private = any(kw in unit_text for kw in [
            '@', 'phone', 'password', 'token', 'key', 'secret', 'ssn',
            'credit card', 'api key'])
        if not (is_sensitive or has_resolved or has_stale or has_private):
            hard_skip_issues += 1

print('Target-text alignment issues: {} (out of store units in sample)'.format(target_mismatches))
print('Hard SKIP plausibility issues: {} (out of skip units in sample)'.format(hard_skip_issues))

# Show 3 sample cases
print()
print('--- 3 Sample Cases for Manual Review ---')
for c in random.sample(sample, min(3, len(sample))):
    print()
    print('Case: {}'.format(c['case_id']))
    ctx = c.get('runtime_context', {})
    print('  Context: project={} svc={} repo={}'.format(
        ctx.get('project', ''), ctx.get('service', ''), ctx.get('repo', '')))
    print('  Tags: {}'.format(c.get('tags', [])))
    print('  READ: {}'.format(c['gold'].get('read', [])))
    print('  STORE: {}'.format([(s['target'], s['unit_id']) for s in c['gold'].get('store', [])]))
    print('  SKIP: {}'.format(c['gold'].get('skip', [])))
    print('  Memories:')
    for m in c.get('candidate_memories', []):
        rd = 'R' if m['memory_id'] in c['gold'].get('read', []) else '-'
        print('    [{}] {} ({}): {}'.format(rd, m['memory_id'], m.get('memory_type', '?'),
              m.get('text', '')[:120]))
    print('  Units:')
    for u in c.get('current_units', []):
        uid = u['unit_id']
        in_store = uid in {s['unit_id'] for s in c['gold'].get('store', [])}
        target = next((s['target'] for s in c['gold'].get('store', []) if s['unit_id'] == uid), 'skip')
        label = 'STORE({})'.format(target) if in_store else 'SKIP'
        print('    [{}] {} tags={}: {}'.format(label, uid, u.get('tags', []),
              u.get('text', '')[:120]))

# ===================================================================
# 8. DOCUMENTATION AUDIT
# ===================================================================
hdr('8. DOCUMENTATION AUDIT')

doc_issues = []
for d in [ROOT / 'reports/v05g', ROOT / 'docs/v05g']:
    if d.exists():
        for rf in d.glob('*.md'):
            text = rf.read_text()
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if 'unevaluated' in line.lower() and 'gold_v2_009' in line.lower():
                    doc_issues.append('{}:{}: still says gold_v2_009 unevaluated'.format(rf.name, i+1))

if doc_issues:
    for issue in doc_issues:
        print('  DOC ISSUE: {}'.format(issue))
else:
    print('No documentation issues found')

# ===================================================================
# 9. LOCK/HASH AUDIT
# ===================================================================
hdr('9. LOCK/HASH AUDIT')

lock_path = ROOT / 'data/v05g/v05g_training_data_lock.json'
lock = json.loads(lock_path.read_text())
hash_issues = []
for name, info in lock.get('files', {}).items():
    path = Path(info['path'])
    if not path.exists():
        hash_issues.append('MISSING: {}'.format(path))
        continue
    curr = hashlib.sha256(path.read_bytes()).hexdigest()
    locked = info['sha256']
    if curr != locked:
        hash_issues.append('MISMATCH: {}'.format(name))
        print('  {}: curr={} lock={} MISMATCH'.format(name, curr[:16], locked[:16]))
    else:
        print('  {}: {}... MATCH'.format(name, curr[:16]))

if not hash_issues:
    print('All file hashes match lock file')

# ===================================================================
# 10. NAMESPACE LEAKAGE
# ===================================================================
hdr('10. NAMESPACE LEAKAGE (additional 500)')

banned_projects = {
    'accessibility-compliance', 'cybersecurity-audit', 'game-analytics',
    'genomics-pipeline', 'media-transcoding', 'quantitative-research',
    'real-estate-valuation', 'supply-chain-optimizer',
    'ecommerce-platform', 'iot-monitoring', 'legal-doc-review',
    'inventory-mgmt', 'support-ticketing', 'edu-platform',
    'flowcraft', 'demand-forecaster', 'education-platform',
}
banned_services = {
    'audit-crawler', 'backtest-engine', 'comp-engine', 'encoding-orchestrator',
    'inventory-planner', 'session-analyzer', 'variant-caller', 'vuln-scanner',
    'alert-manager', 'auto-router', 'cart-service', 'clause-extractor',
    'quiz-grader', 'reorder-engine',
}
banned_repos = {
    'a11ykit', 'alphapack', 'pentestkit', 'pixelpipe', 'playmetrics',
    'seqflow', 'stockplan', 'valuestack',
    'docanalyzer', 'learnhub', 'sensornet', 'shopengine', 'stockpile', 'ticketflow',
}

add_projects = set()
add_services = set()
add_repos = set()
for c in add_cases:
    ctx = c.get('runtime_context', {})
    if isinstance(ctx, dict):
        p = ctx.get('project', '').lower()
        s = ctx.get('service', '').lower()
        r = ctx.get('repo', '').lower()
        if p: add_projects.add(p)
        if s: add_services.add(s)
        if r: add_repos.add(r)

proj_overlap = add_projects & banned_projects
svc_overlap = add_services & banned_services
repo_overlap = add_repos & banned_repos

print('Banned project overlap: {}'.format(proj_overlap if proj_overlap else 'NONE'))
print('Banned service overlap: {}'.format(svc_overlap if svc_overlap else 'NONE'))
print('Banned repo overlap: {}'.format(repo_overlap if repo_overlap else 'NONE'))

# Check against gold_v2_009
g009_cases = load(ROOT / 'data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl')
g009_projects = set()
g009_services = set()
g009_repos = set()
for c in g009_cases:
    ctx = c.get('runtime_context', {})
    if isinstance(ctx, dict):
        if ctx.get('project'): g009_projects.add(ctx['project'].lower())
        if ctx.get('service'): g009_services.add(ctx['service'].lower())
        if ctx.get('repo'): g009_repos.add(ctx['repo'].lower())

p_overlap = add_projects & g009_projects
s_overlap = add_services & g009_services
r_overlap = add_repos & g009_repos

print('gold_v2_009 project overlap: {}'.format(p_overlap if p_overlap else 'NONE'))
print('gold_v2_009 service overlap: {}'.format(s_overlap if s_overlap else 'NONE'))
print('gold_v2_009 repo overlap: {}'.format(r_overlap if r_overlap else 'NONE'))

ns_ok = not (proj_overlap or svc_overlap or repo_overlap or p_overlap or s_overlap or r_overlap)
print('Namespace leakage verdict: {}'.format('PASS' if ns_ok else 'FAIL'))

# ===================================================================
# SUMMARY
# ===================================================================
hdr('AUDIT SUMMARY')
print('READ repair:         {}'.format('PASS' if read_ok else 'FAIL'))
print('9 quality gates:     {}'.format('PASS' if all_gates else 'FAIL'))
print('Sensitive literal:   {}'.format('PASS' if sensitive_ok else 'FAIL'))
print('Namespace leakage:   {}'.format('PASS' if ns_ok else 'FAIL'))
print('Documentation:       {}'.format('PASS' if not doc_issues else 'FAIL'))
print('Hash/lock:           {}'.format('PASS' if not hash_issues else 'FAIL'))
print('Binary prefix acc:   {:.1f}% (report: 90.9%)'.format(binary_pct))
print('Multi-class prefix:  {:.1f}%'.format(multi_pct))
print('Body-dep cases:      {}/500 ({:.1f}%)'.format(len(body_dependent_cases), 100*len(body_dependent_cases)/500))
print('Target-text issues:  {} (sample={})'.format(target_mismatches, len(sample)))
print('Hard SKIP issues:    {} (sample={})'.format(hard_skip_issues, len(sample)))
print('Stale reads:         {}'.format(stale_reads))
print('Non-recoverable:     {}'.format(non_recoverable_reads))
print('Max sensitive rpt:   {}x'.format(max_repeated))
print('Ambiguous prefixes:  {}'.format(ambiguous_binary))
