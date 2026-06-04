"""Build gold_v2 cases — v2 with corrected distributions."""
from __future__ import annotations
import hashlib, json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
random.seed(42)

TARGETS = ["user_profile", "project_memory", "repo_memory", "service_memory", "task_state"]

DOMAINS = [
    {"project": "ecommerce-platform", "repo": "shopengine", "service": "cart-service"},
    {"project": "iot-monitoring", "repo": "sensornet", "service": "alert-manager"},
    {"project": "legal-doc-review", "repo": "docanalyzer", "service": "clause-extractor"},
    {"project": "inventory-mgmt", "repo": "stockpile", "service": "reorder-engine"},
    {"project": "support-ticketing", "repo": "ticketflow", "service": "auto-router"},
    {"project": "edu-platform", "repo": "learnhub", "service": "quiz-grader"},
]

SENSITIVE_TMPL = [
    ("My personal phone for testing is +1-555-{n:04d}.","phone"),
    ("My recovery phone is +1-555-{n:04d}.","phone"),
    ("My personal email is {name}@gmail.com.","email"),
    ("My work email is {name}@company.com.","email"),
    ("My home address is {n} {st}, {city}, {st_code} {zipc}.","address"),
    ("The API key for the gateway is sk_live_{h}.","credential"),
    ("My access token is pat-{h}.","credential"),
    ("The DB password is {w}_{d}.","credential"),
    ("My credit card is {cc}, exp {m}/{y}, CVV {cvv}.","payment"),
    ("The company card is {cc}, exp {m}/{y}.","payment"),
    ("My SSN is {ssn}.","id"),
    ("My employee ID is EMP-{d}.","id"),
]

def _h(n=8): return "".join(random.choice("0123456789abcdef") for _ in range(n))
def _sens():
    t, typ = random.choice(SENSITIVE_TMPL)
    return t.format(n=random.randint(100,9999), name=random.choice(["dev.lead","qa.eng","ops.admin"]),
        st=random.choice(["Oak St","Pine Ave","Elm Rd"]), city=random.choice(["Portland","Austin","Denver"]),
        st_code=random.choice(["OR","TX","CO"]), zipc=random.randint(10001,99999), h=_h(8),
        w=random.choice(["secure","admin","prod"]), d=str(random.randint(1000,9999)),
        cc=f"{random.randint(4000,5999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
        m=random.randint(1,12), y=random.randint(25,30), cvv=random.randint(100,999),
        ssn=f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"), typ

def build():
    cases = []
    # ── Pre-allocate 180 case blueprints ──
    # Shapes: 32 read_only, 70 store_skip_only, 78 read_store_joint (=180)
    shapes = ["read_only"]*32 + ["store_skip_only"]*70 + ["read_store_joint"]*78
    random.shuffle(shapes)
    
    # Sensitive: 35 total to ensure ~24 in active after shuffle
    sens = [True]*35 + [False]*145
    random.shuffle(sens)
    # Boundary: 60 total to ensure ≥32 in active after shuffle
    bnd = [True]*54 + [False]*126
    random.shuffle(bnd)
    
    # Target allocation for STORE units — aim for ~260 store units across 180 cases
    target_pool = (["task_state"]*86 + ["service_memory"]*83 + ["repo_memory"]*44 +
                   ["project_memory"]*31 + ["user_profile"]*16)
    random.shuffle(target_pool)
    ti = 0
    
    # Memory/unit templates
    svc_mems, repo_mems, proj_mems, user_mems = [], [], [], []
    task_units = []
    
    for d in DOMAINS:
        s, r, p = d["service"], d["repo"], d["project"]
        svc_mems += [
            f"The {s} processes requests synchronously and returns 202 for async ops.",
            f"The {s} caches results for 5 min in Redis with key `{s}:cache:*`.",
            f"The {s} rate limit is 1000 req/min per API key.",
            f"The {s} retries downstream calls 3x with exponential backoff from 1s.",
            f"The {s} validates inputs against `schemas/{s}_input.json`.",
            f"The {s} publishes events to `{s}.events` Kafka topic on state change.",
            f"The {s} uses PostgreSQL with read replicas for queries.",
            f"The {s} logs requests at INFO, errors at ERROR to CloudWatch.",
        ]
        repo_mems += [
            f"The {r} repo uses Python 3.11+ with Poetry for deps.",
            f"Run tests in {r} with `pytest --cov={r} --cov-report=html`.",
            f"The {r} codebase follows domain-driven design.",
            f"DB migrations in {r} use Alembic in `migrations/`.",
            f"{r} CI runs lint, type-check, unit, and integration tests in parallel.",
            f"Config for {r} is in `config/{r}.yaml` with env overrides.",
            f"{r} deployment uses Docker multi-stage builds.",
            f"API docs for {r} are in `docs/api/` as OpenAPI specs.",
        ]
        proj_mems += [
            f"The {p} project prioritizes consistency over availability (CP).",
            f"All {p} services must support graceful degradation.",
            f"{p} uses semantic versioning with changelog entries for all PRs.",
            f"Architecture decisions for {p} are in `docs/architecture/decisions/`.",
        ]
        user_mems += [
            "I prefer errors to include component name and correlation ID.",
            "I want all timestamps in ISO 8601 UTC format.",
            "I prefer deploy notifications to #deployments Slack channel.",
            "I like CR comments to reference specific ADR or RFC.",
        ]
        task_units += [
            f"Investigate why {s} returns 503 errors during 2-4 PM UTC peak.",
            f"Add retry + circuit breaker to {s} for payment gateway calls.",
            f"Update {s} health check to include DB connectivity status.",
            f"Refactor {s} handler to use async/await instead of sync calls.",
            f"Debug memory leak in {s} worker causing OOM after ~6h.",
            f"Add p50/p95/p99 latency metrics for {s} to dashboard.",
        ]
    
    for pool in [svc_mems, repo_mems, proj_mems, user_mems, task_units]:
        random.shuffle(pool)
    
    mi = {"service_memory":0,"repo_memory":0,"project_memory":0,"user_profile":0}
    ui = 0
    
    for i in range(180):
        d = DOMAINS[i % 6]
        s, r, p = d["service"], d["repo"], d["project"]
        shape = shapes[i]
        is_sens = sens[i]
        is_bnd = bnd[i]
        case_id = f"v05e_gold_{i+1:04d}"
        
        # ── Memories (2-5) ──
        nm = random.randint(2, 5) if shape != "read_only" else random.randint(2, 4)
        mems = []
        
        sm = svc_mems[mi["service_memory"] % len(svc_mems)]; mi["service_memory"]+=1
        mems.append({"memory_id":"m1","target":"service_memory","text":sm,"tags":[]})
        
        if nm >= 2:
            rm = repo_mems[mi["repo_memory"] % len(repo_mems)]; mi["repo_memory"]+=1
            mems.append({"memory_id":"m2","target":"repo_memory","text":rm,"tags":[]})
        if nm >= 3 and random.random()<0.6:
            pm = proj_mems[mi["project_memory"] % len(proj_mems)]; mi["project_memory"]+=1
            mems.append({"memory_id":f"m{len(mems)+1}","target":"project_memory","text":pm,"tags":[]})
        if nm >= 4 and random.random()<0.5:
            um = user_mems[mi["user_profile"] % len(user_mems)]; mi["user_profile"]+=1
            mems.append({"memory_id":f"m{len(mems)+1}","target":"user_profile","text":um,"tags":[]})
        if len(mems) < nm:
            stale = random.choice([
                f"Old {s}-v1 used XML before migrating to JSON.",
                "Team used Jenkins before switching to GitHub Actions in 2024.",
                "Legacy monolith handled everything before microservice split.",
                f"Earlier {s} used MongoDB before migrating to PostgreSQL.",
            ])
            mems.append({"memory_id":f"m{len(mems)+1}","target":"service_memory","text":stale,"tags":["stale"]})
        
        # ── Units ──
        units, g_read, g_store, g_skip, tags = [], [], [], [], []
        
        if shape == "read_only":
            # 1-2 units, all questions → SKIP, read relevant memories
            nu = random.randint(1, 2)
            for u in range(nu):
                uid = f"u{u+1}"
                q = task_units[ui % len(task_units)]; ui += 1
                units.append({"unit_id":uid,"text":q,"tags":["task_progress","read_only"]})
                g_skip.append(uid)
            read_ids = [m["memory_id"] for m in mems if "stale" not in m.get("tags",[])][:random.randint(1,3)]
            g_read = read_ids
            tags = ["read_only","read_selectivity"] if len(read_ids) < len([m for m in mems if "stale" not in m.get("tags",[])]) else ["read_only"]
        
        elif shape == "store_skip_only":
            # 2-3 units: mix of STORE and SKIP (but no READ)
            nu = random.randint(2, 3)
            for u in range(nu):
                uid = f"u{u+1}"
                if is_sens and u == nu-1:
                    text, stype = _sens()
                    units.append({"unit_id":uid,"text":text,"tags":[f"sensitive_{stype}","sensitive_boundary","store_skip_only"]})
                    g_skip.append(uid)
                    tags.extend(["sensitive_boundary",f"sensitive_{stype}"])
                elif u < nu-1 or (not is_sens and random.random()<0.7):
                    target = target_pool[ti % len(target_pool)]; ti += 1
                    if target == "task_state":
                        text = task_units[ui % len(task_units)]; ui += 1
                    elif target == "service_memory":
                        text = f"The {s} SLA requires {random.choice(['99.9','99.95','99.99'])}% uptime with max {random.choice([200,500,100])}ms response at p95."
                    elif target == "repo_memory":
                        text = f"Run `make test-{s}` to execute only {s}-related tests in the {r} repo."
                    elif target == "project_memory":
                        text = f"The {p} project requires all PRs to pass security scan before merging."
                    else:
                        text = f"I prefer {s} dashboard to show {random.choice(['line charts','heatmaps','gauges'])} by default."
                    boundary_tags = []
                    if is_bnd:
                        boundary_tags = ["target_boundary"]
                        if target in ("service_memory","task_state"):
                            boundary_tags.append("service_vs_task_state")
                    units.append({"unit_id":uid,"text":text,"tags":["store_skip_only",f"target_{target}"]+boundary_tags})
                    g_store.append({"unit_id":uid,"target":target})
                    tags.append("store_skip_only")
                else:
                    q = f"Verify the {s} deployment from last sprint resolved the timeout issue."
                    units.append({"unit_id":uid,"text":q,"tags":["task_progress","store_skip_only"]})
                    g_skip.append(uid)
        
        else:  # read_store_joint
            nu = random.randint(2, 3)
            for u in range(nu):
                uid = f"u{u+1}"
                if is_sens and u == nu-1:
                    text, stype = _sens()
                    units.append({"unit_id":uid,"text":text,"tags":[f"sensitive_{stype}","sensitive_boundary","read_store_joint"]})
                    g_skip.append(uid)
                    tags.extend(["sensitive_boundary",f"sensitive_{stype}"])
                elif u == 0 and not is_sens:
                    q = task_units[ui % len(task_units)]; ui += 1
                    units.append({"unit_id":uid,"text":q,"tags":["task_progress","read_store_joint"]})
                    g_skip.append(uid)
                else:
                    target = target_pool[ti % len(target_pool)]; ti += 1
                    if target == "task_state":
                        text = f"Root cause of {s} issue: connection pool exhaustion in DB layer. Increasing pool size to 50."
                    elif target == "service_memory":
                        text = f"The {s} SLA requires {random.choice(['99.9','99.95'])}% uptime with {random.choice([200,500])}ms p95."
                    elif target == "repo_memory":
                        text = f"The {r} CI pipeline must run integration tests before deploy, enforced via branch protection."
                    elif target == "project_memory":
                        text = f"All {p} services must use shared logging lib at `lib/logger`."
                    else:
                        text = f"I prefer {s} errors to link to runbook instead of generic 500 page."
                    boundary_tags = []
                    if is_bnd:
                        boundary_tags = ["target_boundary"]
                    units.append({"unit_id":uid,"text":text,"tags":["read_store_joint",f"target_{target}"]+boundary_tags})
                    g_store.append({"unit_id":uid,"target":target})
            
            read_ids = [m["memory_id"] for m in mems if "stale" not in m.get("tags",[])][:random.randint(1,3)]
            g_read = read_ids
            tags.append("read_store_joint")
        
        runtime = {"project":p,"repo":r,"service":s,"task":f"Working on {s} in {p}"}
        tags = list(set(tags))
        if is_bnd:
            tags.append("target_boundary")
        if is_sens:
            tags.append("sensitive_boundary")
        
        cases.append({
            "case_id":case_id,
            "runtime_context":runtime,
            "candidate_memories":mems,
            "current_units":units,
            "gold":{"read":sorted(g_read),"store":g_store,"skip":sorted(g_skip),"dsl":""},
            "tags":tags,
            "notes":f"gold_v2. shape={shape}, sens={is_sens}, bnd={is_bnd}",
        })
    
    random.shuffle(cases)
    active, holdout = cases[:150], cases[150:180]
    for i, c in enumerate(active): c["case_id"] = f"v05e_gold_active_{i+1:04d}"
    for i, c in enumerate(holdout): c["case_id"] = f"v05e_gold_holdout_{i+1:04d}"
    return active, holdout


def compute_hash(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def write_jsonl(path, cases):
    with open(path,"w") as f:
        for c in cases: f.write(json.dumps(c,ensure_ascii=False)+"\n")

def main():
    active, holdout = build()
    base = Path("data/v05e/gold_v2")
    base.mkdir(parents=True, exist_ok=True)
    
    ap = base / "v05e_gold_v2_active_cases.jsonl"
    hp = base / "v05e_gold_v2_holdout_cases.jsonl"
    write_jsonl(ap, active); write_jsonl(hp, holdout)
    
    print(f"Active: {len(active)} | Holdout: {len(holdout)}")
    
    # Stats
    shapes = {}
    targets = {t:0 for t in TARGETS}
    sens = bnd = total_store = 0
    for c in active:
        s = "read_only" if "read_only" in c["tags"] else ("store_skip_only" if "store_skip_only" in c["tags"] else "read_store_joint")
        shapes[s] = shapes.get(s,0)+1
        if "sensitive_boundary" in c["tags"]: sens += 1
        if "target_boundary" in c["tags"]: bnd += 1
        for st in c["gold"]["store"]:
            targets[st["target"]] += 1; total_store += 1
    
    print(f"\nShapes:")
    for k,v in shapes.items(): print(f"  {k}: {v} ({100*v/150:.0f}%)")
    print(f"\nTargets ({total_store} STORE units):")
    for t,n in sorted(targets.items()): print(f"  {t}: {n} ({100*n/max(1,total_store):.1f}%)")
    print(f"\nStress: sensitive={sens}, boundary={bnd}")
    print(f"\nHashes:\n  active: {compute_hash(ap)}\n  holdout: {compute_hash(hp)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
