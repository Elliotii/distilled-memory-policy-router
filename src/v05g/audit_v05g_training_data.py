"""Audit v0.5g training data for leakage, quality, and readiness.

Checks:
- Exact text overlap vs dev, old gold, gold_v2_009
- Namespace (project/repo/service) overlap
- Placeholder residue
- Sensitive content audit
- Distribution verification against targets
- SFT format validation
"""
from __future__ import annotations
import json, hashlib, re, sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

V05G_DIR = ROOT / "data/v05g"

PROTECTED_FILES = {
    "dev": ROOT / "data/dev/dev_250.jsonl",
    "old_gold": ROOT / "data/gold/gold_eval_300.jsonl",
    "gold_v2_009": ROOT / "data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl",
    "gold_v2_holdout": ROOT / "data/v05e/gold_v2/v05e_gold_v2_holdout_cases.jsonl",
}

V05G_FILES = {
    "500_control_cases": V05G_DIR / "cases/v05g_train_500_control_cases.jsonl",
    "500_control_sft": V05G_DIR / "json_sft/v05g_train_500_control_json_sft_messages.jsonl",
    "add_500_cases": V05G_DIR / "cases/v05g_train_additional_500_targeted_cases.jsonl",
    "add_500_sft": V05G_DIR / "json_sft/v05g_train_additional_500_targeted_json_sft_messages.jsonl",
    "1000_cases": V05G_DIR / "cases/v05g_train_1000_targeted_cases.jsonl",
    "1000_sft": V05G_DIR / "json_sft/v05g_train_1000_targeted_json_sft_messages.jsonl",
}

# Banned namespaces from gold_v2 construction
BANNED_PROJECTS = {
    'accessibility-compliance', 'cybersecurity-audit', 'game-analytics',
    'genomics-pipeline', 'media-transcoding', 'quantitative-research',
    'real-estate-valuation', 'supply-chain-optimizer',
    'ecommerce-platform', 'iot-monitoring', 'legal-doc-review',
    'inventory-mgmt', 'support-ticketing', 'edu-platform',
    'flowcraft', 'demand-forecaster', 'education-platform',
}
BANNED_SERVICES = {
    'audit-crawler', 'backtest-engine', 'comp-engine', 'encoding-orchestrator',
    'inventory-planner', 'session-analyzer', 'variant-caller', 'vuln-scanner',
    'alert-manager', 'auto-router', 'cart-service', 'clause-extractor',
    'quiz-grader', 'reorder-engine',
}
BANNED_REPOS = {
    'a11ykit', 'alphapack', 'pentestkit', 'pixelpipe', 'playmetrics',
    'seqflow', 'stockplan', 'valuestack',
    'docanalyzer', 'learnhub', 'sensornet', 'shopengine', 'stockpile',
    'ticketflow',
}


def load_jsonl(path):
    cases = []
    with open(path) as f:
        for line in f:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def extract_texts(cases):
    """Extract all text from cases for overlap checking."""
    texts = []
    for c in cases:
        # Current user input / units
        for u in c.get("current_units", []):
            texts.append(u.get("text", u.get("content", "")))
        # Candidate memories
        for m in c.get("candidate_memories", []):
            texts.append(m.get("text", m.get("content", "")))
        # Also check current_user_input if present
        if "current_user_input" in c:
            texts.append(c["current_user_input"])
        # Runtime context task
        ctx = c.get("runtime_context", {})
        if isinstance(ctx, dict) and "task" in ctx:
            texts.append(ctx["task"])
    return texts


def extract_namespaces(cases):
    """Extract project/repo/service names."""
    projects = set()
    services = set()
    repos = set()
    for c in cases:
        ctx = c.get("runtime_context", {})
        if isinstance(ctx, dict):
            p = ctx.get("project", "")
            s = ctx.get("service", "")
            r = ctx.get("repo", "")
            if p: projects.add(p.lower())
            if s: services.add(s.lower())
            if r: repos.add(r.lower())
    return projects, services, repos


def check_exact_overlap(new_texts, protected_texts, protected_label):
    """Check for exact text substring overlap of length >= 30 chars."""
    # Only check substrings >= 30 chars to avoid false positives on common phrases
    results = []
    for pt in protected_texts:
        if len(pt) < 30:
            continue
        pt_lower = pt.lower().strip()
        for i, nt in enumerate(new_texts):
            if len(nt) < 30:
                continue
            if pt_lower == nt.lower().strip():
                results.append(f"  EXACT match with {protected_label}: '{pt[:80]}...'")
                break
    return results


def check_span_overlap(new_texts, protected_texts, protected_label):
    """Check if any protected text span >= 20 chars appears inside new text."""
    results = []
    for pt in protected_texts:
        if len(pt) < 20:
            continue
        pt_lower = pt.lower().strip()
        for i, nt in enumerate(new_texts):
            if len(nt) < 20:
                continue
            if pt_lower in nt.lower():
                results.append(f"  SPAN overlap with {protected_label}: '{pt[:60]}...' in new")
                break
    return results


def check_sensitive_stores(cases):
    """Audit that no sensitive content is in STORE."""
    violations = []
    for c in cases:
        cid = c.get("case_id", "unknown")
        gold = c["gold"]
        store_ids = {s["unit_id"] for s in gold.get("store", [])}
        for u in c.get("current_units", []):
            if any("sensitive" in t for t in u.get("tags", [])):
                if u["unit_id"] in store_ids:
                    violations.append(f"  {cid}: sensitive unit {u['unit_id']} in STORE: {u.get('text','')[:60]}")
    return violations


def check_duplicate_assignment(cases):
    """Check for duplicate unit assignments."""
    violations = []
    for c in cases:
        cid = c.get("case_id", "unknown")
        store_uids = [s["unit_id"] for s in c["gold"].get("store", [])]
        if len(store_uids) != len(set(store_uids)):
            violations.append(f"  {cid}: duplicate store unit_id")
        store_set = set(store_uids)
        skip_set = set(c["gold"].get("skip", []))
        if store_set & skip_set:
            violations.append(f"  {cid}: unit in both store and skip: {store_set & skip_set}")
    return violations


def check_invalid_targets(cases):
    """Check for invalid STORE targets."""
    legal = {"task_state", "service_memory", "repo_memory", "project_memory", "user_profile"}
    violations = []
    for c in cases:
        cid = c.get("case_id", "unknown")
        for s in c["gold"].get("store", []):
            if s.get("target") not in legal:
                violations.append(f"  {cid}: invalid target '{s.get('target')}'")
    return violations


def check_placeholder_residue(cases, filler_keys):
    """Check for unresolved filler keys in generated cases."""
    violations = []
    for c in cases:
        cid = c.get("case_id", "unknown")
        for u in c.get("current_units", []):
            ut = u.get("text", u.get("content", ""))
            if re.search(r'\{vocab_item\}', ut):
                violations.append(f"  {cid}: '{{vocab_item}}' in unit {u['unit_id']}")
            unresolved = re.findall(r'\{([a-z]+_[a-z_]+)\}', ut)
            for ph in unresolved:
                if ph in filler_keys:
                    violations.append(f"  {cid}: unresolved '{{{ph}}}' in unit {u['unit_id']}")
        for m in c.get("candidate_memories", []):
            mt = m.get("text", m.get("content", ""))
            if re.search(r'\{vocab_item\}', mt):
                violations.append(f"  {cid}: '{{vocab_item}}' in memory {m['memory_id']}")
            unresolved = re.findall(r'\{([a-z]+_[a-z_]+)\}', mt)
            for ph in unresolved:
                if ph in filler_keys:
                    violations.append(f"  {cid}: unresolved '{{{ph}}}' in memory {m['memory_id']}")
    return violations


def validate_sft_format(sft_path, cases_path):
    """Validate SFT messages format."""
    errors = []
    sft_cases = load_jsonl(sft_path)
    ref_cases = load_jsonl(cases_path)
    
    if len(sft_cases) != len(ref_cases):
        errors.append(f"  Count mismatch: SFT={len(sft_cases)} cases={len(ref_cases)}")
        return errors
    
    legal_targets = {"task_state", "service_memory", "repo_memory", "project_memory", "user_profile"}
    
    for i, (sft, ref) in enumerate(zip(sft_cases, ref_cases)):
        cid = sft.get("case_id", f"idx_{i}")
        msgs = sft.get("messages", [])
        
        if len(msgs) != 3:
            errors.append(f"  {cid}: expected 3 messages, got {len(msgs)}")
            continue
        
        assistant = msgs[2].get("content", "")
        
        # Parse JSON
        try:
            parsed = json.loads(assistant)
        except json.JSONDecodeError:
            errors.append(f"  {cid}: JSON parse failed")
            continue
        
        # No markdown
        if "```" in assistant:
            errors.append(f"  {cid}: markdown fence detected")
        
        # Required keys
        for key in ("read", "store", "skip"):
            if key not in parsed:
                errors.append(f"  {cid}: missing '{key}' in assistant")
        
        if "read" not in parsed or "store" not in parsed or "skip" not in parsed:
            continue
        
        # Validate reads
        mem_ids = {m["memory_id"] for m in ref.get("candidate_memories", [])}
        for rid in parsed["read"]:
            if rid not in mem_ids:
                errors.append(f"  {cid}: read '{rid}' not in candidate_memories")
        
        # Validate stores
        unit_ids = {u["unit_id"] for u in ref.get("current_units", [])}
        seen_store = set()
        for item in parsed["store"]:
            if not isinstance(item, dict):
                errors.append(f"  {cid}: store item not dict")
                continue
            t = item.get("target")
            uid = item.get("unit_id")
            if t not in legal_targets:
                errors.append(f"  {cid}: invalid target '{t}'")
            if uid not in unit_ids:
                errors.append(f"  {cid}: store unit_id '{uid}' not in units")
            if uid in seen_store:
                errors.append(f"  {cid}: duplicate store unit_id '{uid}'")
            seen_store.add(uid)
        
        # Validate skips
        seen_skip = set()
        for uid in parsed["skip"]:
            if uid not in unit_ids:
                errors.append(f"  {cid}: skip unit_id '{uid}' not in units")
            if uid in seen_skip:
                errors.append(f"  {cid}: duplicate skip unit_id '{uid}'")
            seen_skip.add(uid)
        
        # Unit coverage
        if unit_ids != (seen_store | seen_skip):
            missing = unit_ids - (seen_store | seen_skip)
            if missing:
                errors.append(f"  {cid}: unassigned units: {missing}")
        
        # Canonical consistency
        gold_read = set(ref["gold"]["read"])
        sft_read = set(parsed["read"])
        if gold_read != sft_read:
            errors.append(f"  {cid}: read mismatch")
        
        gold_store = {(s["target"], s["unit_id"]) for s in ref["gold"]["store"]}
        sft_store = {(s["target"], s["unit_id"]) for s in parsed["store"] if isinstance(s, dict)}
        if gold_store != sft_store:
            errors.append(f"  {cid}: store mismatch")
        
        gold_skip = set(ref["gold"]["skip"])
        sft_skip = set(parsed["skip"])
        if gold_skip != sft_skip:
            errors.append(f"  {cid}: skip mismatch")
    
    return errors


def compute_dist(cases):
    """Compute distribution stats."""
    total = len(cases)
    shapes = Counter()
    targets = Counter()
    total_store = 0
    tags = Counter()
    
    for c in cases:
        g = c["gold"]
        hr = bool(g.get("read", []))
        hs = bool(g.get("store", []))
        if hr and hs: shapes["READ+STORE"] += 1
        elif hr: shapes["READ-only"] += 1
        elif hs: shapes["STORE/SKIP-only"] += 1
        else: shapes["SKIP-only"] += 1
        
        for s in g.get("store", []):
            targets[s["target"]] += 1
            total_store += 1
        
        for t in c.get("tags", []):
            tags[t] += 1
    
    return {
        "total": total, "store_units": total_store,
        "shapes": dict(shapes),
        "shape_pct": {k: round(100*v/total, 1) for k, v in shapes.items()},
        "targets": dict(targets),
        "target_pct": {k: round(100*v/max(1,total_store), 1) for k, v in targets.items()},
        "tags": dict(tags),
    }


def main():
    print("=" * 70)
    print("v05g Training Data Audit")
    print("=" * 70)
    
    all_ok = True
    
    # ── 1. Load data ──
    print("\n[1] Loading data...")
    v05g_data = {}
    for name, path in V05G_FILES.items():
        if path.exists():
            v05g_data[name] = load_jsonl(path)
            print(f"  {name}: {len(v05g_data[name])} records")
        else:
            print(f"  {name}: MISSING!")
            all_ok = False
    
    protected_data = {}
    for name, path in PROTECTED_FILES.items():
        if path.exists():
            protected_data[name] = load_jsonl(path)
            print(f"  Protected {name}: {len(protected_data[name])} records")
        else:
            print(f"  Protected {name}: not found (skipping)")
    
    if not all_ok:
        print("\n❌ Missing v05g files. Aborting.")
        return 1
    
    # ── 2. Namespace leakage ──
    print("\n[2] Namespace leakage check...")
    add_cases = v05g_data["add_500_cases"]
    add_projects, add_services, add_repos = extract_namespaces(add_cases)
    
    proj_overlap = add_projects & BANNED_PROJECTS
    svc_overlap = add_services & BANNED_SERVICES
    repo_overlap = add_repos & BANNED_REPOS
    
    if proj_overlap:
        print(f"  ❌ Project overlap: {proj_overlap}")
        all_ok = False
    else:
        print(f"  ✅ No project overlap with banned namespaces")
    
    if svc_overlap:
        print(f"  ❌ Service overlap: {svc_overlap}")
        all_ok = False
    else:
        print(f"  ✅ No service overlap with banned namespaces")
    
    if repo_overlap:
        print(f"  ❌ Repo overlap: {repo_overlap}")
        all_ok = False
    else:
        print(f"  ✅ No repo overlap with banned namespaces")
    
    # Also check against protected files
    for name, pdata in protected_data.items():
        p_projects, p_services, p_repos = extract_namespaces(pdata)
        if not p_projects and not p_services and not p_repos:
            continue
        p_overlap = add_projects & p_projects
        s_overlap = add_services & p_services
        r_overlap = add_repos & p_repos
        if p_overlap or s_overlap or r_overlap:
            print(f"  ❌ Namespace overlap with {name}")
            if p_overlap: print(f"    Projects: {p_overlap}")
            if s_overlap: print(f"    Services: {s_overlap}")
            if r_overlap: print(f"    Repos: {r_overlap}")
            all_ok = False
        else:
            print(f"  ✅ No namespace overlap with {name}")
    
    # ── 3. Exact text leakage (additional 500 vs protected) ──
    print("\n[3] Text leakage check (additional 500 vs protected)...")
    add_texts = extract_texts(add_cases)
    total_exact = 0
    total_span = 0
    
    for name, pdata in protected_data.items():
        p_texts = extract_texts(pdata)
        exact_matches = check_exact_overlap(add_texts, p_texts, name)
        span_matches = check_span_overlap(add_texts, p_texts, name)
        
        if exact_matches:
            print(f"  ❌ Exact overlaps with {name}:")
            for m in exact_matches[:10]:
                print(m)
            total_exact += len(exact_matches)
            all_ok = False
        else:
            print(f"  ✅ No exact text overlap with {name}")
        
        if span_matches:
            # Filter out span matches that are very short or common phrases
            real_spans = [s for s in span_matches if len(s.split("'")[1]) > 40 if len(s.split("'")) > 1]
            if real_spans:
                print(f"  ❌ Significant span overlaps with {name}:")
                for m in real_spans[:10]:
                    print(m)
                total_span += len(real_spans)
                all_ok = False
            else:
                print(f"  ✅ No significant span overlap with {name}")
        else:
            print(f"  ✅ No span overlap with {name}")
    
    # ── 4. Quality gates ──
    print("\n[4] Quality gates...")
    
    # Sensitive stores
    sens_violations = check_sensitive_stores(add_cases)
    if sens_violations:
        print(f"  ❌ Sensitive STORE violations in additional 500: {len(sens_violations)}")
        for v in sens_violations[:10]: print(v)
        all_ok = False
    else:
        print(f"  ✅ No sensitive units in STORE")
    
    # Also check combined 1000
    combined_cases = v05g_data["1000_cases"]
    sens_violations_all = check_sensitive_stores(combined_cases)
    if sens_violations_all:
        print(f"  ❌ Sensitive STORE violations in combined 1000: {len(sens_violations_all)}")
        for v in sens_violations_all[:10]: print(v)
        all_ok = False
    else:
        print(f"  ✅ No sensitive units in STORE (combined 1000)")
    
    # Duplicate assignments
    dup_violations = check_duplicate_assignment(combined_cases)
    if dup_violations:
        print(f"  ❌ Duplicate assignment: {len(dup_violations)}")
        all_ok = False
    else:
        print(f"  ✅ No duplicate unit assignments")
    
    # Invalid targets
    tgt_violations = check_invalid_targets(combined_cases)
    if tgt_violations:
        print(f"  ❌ Invalid targets: {len(tgt_violations)}")
        all_ok = False
    else:
        print(f"  ✅ No invalid targets")
    
    # Placeholder residue (additional 500 only)
    filler_keys = {"problem","context","issue","trigger","feature","version","bug","metric",
                   "symptom","owner","deadline","sla","latency","percentile","header","purpose",
                   "where","ttl","n","reset","system","cmd","action","what","path","frequency",
                   "review_type","dashboard","interval","behavior","pattern","progress","quarter",
                   "phase","blocker","component","data","topic","key","condition","tool",
                   "operation","detail","vocab_item"}
    ph_violations = check_placeholder_residue(add_cases, filler_keys)
    if ph_violations:
        print(f"  ❌ Placeholder residue: {len(ph_violations)}")
        for v in ph_violations[:10]: print(v)
        all_ok = False
    else:
        print(f"  ✅ No placeholder residue in additional 500")
    
    # ── 5. SFT format validation ──
    print("\n[5] SFT format validation...")
    sft_errors_1000 = validate_sft_format(
        str(V05G_FILES["1000_sft"]),
        str(V05G_FILES["1000_cases"])
    )
    if sft_errors_1000:
        print(f"  ❌ SFT validation errors in 1000 combined: {len(sft_errors_1000)}")
        for e in sft_errors_1000[:20]: print(e)
        all_ok = False
    else:
        print(f"  ✅ Combined 1000 SFT: 100% valid")
    
    sft_errors_add = validate_sft_format(
        str(V05G_FILES["add_500_sft"]),
        str(V05G_FILES["add_500_cases"])
    )
    if sft_errors_add:
        print(f"  ❌ SFT validation errors in additional 500: {len(sft_errors_add)}")
        all_ok = False
    else:
        print(f"  ✅ Additional 500 SFT: 100% valid")
    
    # ── 6. Distribution check ──
    print("\n[6] Distribution against targets...")
    dist = compute_dist(combined_cases)
    
    target_ranges = {
        "task_state": (25, 32),
        "service_memory": (24, 32),
        "repo_memory": (16, 22),
        "project_memory": (12, 20),
        "user_profile": (6, 12),
    }
    
    print(f"  Combined 1000: {dist['total']} cases, {dist['store_units']} store units")
    print(f"  Shapes: READ-only={dist['shape_pct'].get('READ-only',0)}% "
          f"STORE/SKIP={dist['shape_pct'].get('STORE/SKIP-only',0)}% "
          f"READ+STORE={dist['shape_pct'].get('READ+STORE',0)}%")
    
    for t, (lo, hi) in target_ranges.items():
        pct = dist['target_pct'].get(t, 0)
        in_range = lo <= pct <= hi
        status = "✅" if in_range else "❌"
        print(f"  {status} {t}: {pct}% (target {lo}-{hi}%)")
        if not in_range:
            all_ok = False
    
    # Shape targets
    shape_ranges = {
        "READ-only": (10, 20),
        "STORE/SKIP-only": (35, 45),
        "READ+STORE": (40, 50),
    }
    for s, (lo, hi) in shape_ranges.items():
        pct = dist['shape_pct'].get(s, 0)
        in_range = lo <= pct <= hi
        status = "✅" if in_range else "❌"
        print(f"  {status} Shape {s}: {pct}% (target {lo}-{hi}%)")
        if not in_range:
            all_ok = False
    
    # ── 7. Stress coverage in additional 500 ──
    print("\n[7] Stress coverage in additional 500...")
    add_dist = compute_dist(add_cases)
    add_tags = add_dist["tags"]
    
    sens_cases = sum(1 for c in add_cases if any("sensitive" in t for t in c.get("tags", [])))
    bnd_cases = add_tags.get("target_boundary", 0)
    read_only = add_dist["shapes"].get("READ-only", 0)
    store_skip_only = add_dist["shapes"].get("STORE/SKIP-only", 0)
    read_store = add_dist["shapes"].get("READ+STORE", 0)
    
    # Hard SKIP cases: store_skip_only cases + read_only cases where unit is hard skip
    hard_skip = sum(1 for c in add_cases if "hard_skip" in c.get("tags", []))
    # READ distractor: cases with stale memories
    read_distractor = sum(1 for c in add_cases 
                         if any("stale" in m.get("tags", []) for m in c.get("candidate_memories", [])))
    
    sens_pct = round(100 * sens_cases / 500, 1)
    bnd_pct = round(100 * bnd_cases / 500, 1)
    hskip_pct = round(100 * hard_skip / 500, 1)
    rdist_pct = round(100 * read_distractor / 500, 1)
    
    print(f"  Sensitive/private cases: {sens_cases} ({sens_pct}%) target 15-25%: {'✅' if 15<=sens_pct<=25 else '⚠️' if sens_pct>25 else '❌'}")
    print(f"  Target-boundary cases: {bnd_cases} ({bnd_pct}%) target 25-35%: {'✅' if 25<=bnd_pct<=35 else '⚠️' if bnd_pct>35 else '❌'}")
    print(f"  Hard SKIP cases: {hard_skip} ({hskip_pct}%) target min 25%: {'✅' if hskip_pct>=25 else '❌'}")
    print(f"  READ distractor/stale cases: {read_distractor} ({rdist_pct}%) target min 30%: {'✅' if rdist_pct>=30 else '❌'}")
    
    # ── 8. Verify hashes ──
    print("\n[8] Hash verification...")
    lock_path = V05G_DIR / "v05g_training_data_lock.json"
    if lock_path.exists():
        lock = json.loads(open(lock_path).read())
        for name, info in lock.get("files", {}).items():
            path = Path(info["path"])
            if path.exists():
                current_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                locked_hash = info["sha256"]
                match = current_hash == locked_hash
                print(f"  {'✅' if match else '❌'} {name}: {current_hash[:16]}...")
                if not match:
                    all_ok = False
    
    # ── Summary ──
    print("\n" + "=" * 70)
    if all_ok:
        print("✅ ALL AUDIT CHECKS PASSED")
    else:
        print("❌ SOME AUDIT CHECKS FAILED")
    print("=" * 70)
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
