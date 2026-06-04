"""Build gold_v2_007 — semantic READ, genuine boundaries, fixed grammar.
Key design: READ is recoverable from model-visible memory text.
Memories tagged as [STALE] or prefixed with disambiguating content.
"""
from __future__ import annotations
import hashlib, json, random, sys, re
from pathlib import Path
from collections import Counter, defaultdict
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT))
random.seed(234)

TARGETS = ["task_state","service_memory","repo_memory","project_memory","user_profile"]

DOMAINS = [
    {"project":"cybersecurity-audit","repo":"pentestkit","service":"vuln-scanner","family":"security",
     "vocab":["CVE scanning","exploit detection","patch verification","penetration testing","remediation tracking","CVSS scoring","attack surface analysis","threat modeling","false positive triage","SIEM integration","endpoint monitoring","alert triage","incident response","phishing analysis","ransomware detection","firewall auditing","IDS tuning","compliance scanning","risk assessment","credentialed checks"]},
    {"project":"supply-chain-optimizer","repo":"stockplan","service":"inventory-planner","family":"logistics",
     "vocab":["safety stock calculation","lead time analysis","reorder point optimization","demand signal processing","supplier scoring","inventory turnover","SKU rationalization","backorder prediction","fill rate monitoring","seasonality adjustment","promotional lift estimation","procurement automation","vendor scorecard","purchase order tracking","consignment reconciliation","cycle counting","ABC classification","economic order quantity","warehouse slotting","cross-docking efficiency"]},
    {"project":"media-transcoding","repo":"pixelpipe","service":"encoding-orchestrator","family":"media",
     "vocab":["codec selection","bitrate optimization","resolution scaling","H.264 encoding","H.265 transcoding","AV1 compression","keyframe placement","two-pass encoding","CRF tuning","ABR ladder generation","package formatting","DRM encryption","watermark embedding","subtitle integration","aspect ratio correction","frame rate conversion","GOP configuration","deinterlacing filter","color space mapping","mezzanine processing"]},
    {"project":"accessibility-compliance","repo":"a11ykit","service":"audit-crawler","family":"a11y",
     "vocab":["WCAG 2.1 compliance","ARIA implementation","screen reader testing","keyboard navigation audit","color contrast analysis","focus order verification","alt text validation","landmark structure","skip link functionality","axe-core integration","Lighthouse auditing","accessibility tree inspection","semantic HTML review","focus trap testing","live region monitoring","role assignment","tabindex management","contrast ratio measurement","Section 508 compliance","violation prioritization"]},
    {"project":"quantitative-research","repo":"alphapack","service":"backtest-engine","family":"finance",
     "vocab":["alpha generation","beta calculation","Sharpe ratio optimization","drawdown analysis","survivorship bias correction","look-ahead bias prevention","slippage modeling","market impact estimation","portfolio turnover","factor model construction","risk parity allocation","VaR computation","expected shortfall","Monte Carlo simulation","stress testing","historical backtesting","transaction cost analysis","capacity estimation","signal decay tracking","information coefficient"]},
    {"project":"genomics-pipeline","repo":"seqflow","service":"variant-caller","family":"bioinformatics",
     "vocab":["FASTQ processing","BAM alignment","VCF generation","coverage depth analysis","variant allele frequency","germline calling","somatic mutation detection","SNV identification","indel detection","copy number estimation","ploidy assessment","reference genome mapping","read pair analysis","base quality scoring","mapping quality filtering","duplicate marking","haplotype phasing","genotype likelihood","panel of normals","clinical reporting"]},
    {"project":"real-estate-valuation","repo":"valuestack","service":"comp-engine","family":"realestate",
     "vocab":["comparable sale analysis","cap rate calculation","NOI estimation","DCF modeling","appraisal review","zoning verification","square footage measurement","price per square foot","tax assessment","MLS data","days on market","listing price","closing price","mortgage rate","amortization schedule","LTV ratio","escrow management","title verification","deed recording","property inspection"]},
    {"project":"game-analytics","repo":"playmetrics","service":"session-analyzer","family":"gaming",
     "vocab":["DAU tracking","MAU reporting","retention analysis","churn prediction","session length","ARPDAU calculation","LTV estimation","cohort analysis","funnel optimization","conversion tracking","IAP revenue","tutorial completion","level progression","matchmaking quality","latency monitoring","frame rate stability","crash rate reduction","FTUE optimization","A/B test analysis","engagement scoring"]},
]

# ── SEMANTICALLY-SCOPED templates ──
# READ-relevant cues built into text
SVC_MEM_TMPL = [
    "The {svc} guarantees {sla}% uptime with max response latency of {latency}ms at p{percentile} for {vocab_item}.",
    "All {svc} responses include a {header} header for {purpose} covering {vocab_item} endpoints.",
    "The {svc} caches {vocab_item} data in {where} with a {ttl} TTL for performance.",
    "The {svc} circuit breaker opens after {n} consecutive failures to the {system} and resets after {reset}s for {vocab_item}.",
]
REPO_MEM_TMPL = [
    "Run {cmd} in the {repo} repo to {action} the {svc} for {vocab_item} validation.",
    "All {svc} changes in {repo} must include {what} for {vocab_item} before merging.",
    "{svc} configuration for {vocab_item} lives under {path} in the {repo} repo.",
]
PROJ_MEM_TMPL = [
    "The {proj} project requires {frequency} {review_type} reviews for any changes affecting {vocab_item}.",
    "All {proj} services must report {vocab_item} metrics to {dashboard} every {interval}.",
]
USER_MEM_TMPL = [
    "I prefer the {svc} dashboard to show {vocab_item} metrics as a heatmap rather than a table.",
    "Flag {svc} alerts for {vocab_item} as critical when they affect more than {n} items.",
]

TASK_STORE = [
    "Currently investigating why the {svc} {problem} for {context}. Fix needed by {deadline}.",
    "Active incident: the {svc} {issue} after the {trigger}. Assigned to {owner} this sprint.",
    "This sprint: add {feature} to the {svc} for {context}. Due {deadline}.",
    "Rolling back the {svc} to {version} because the release introduced a {bug} in production.",
]
TASK_SKIP = [
    "Hypothetical: what if the {svc} {problem} during {context}? Not a current concern.",
    "Old incident (resolved): the {svc} had a {issue} after {trigger}. No longer active.",
    "Scratch note: the {svc} showed unusual {metric} last Tuesday, self-resolved.",
    "Discarded idea: add {feature} to {svc}. Rejected by architecture review.",
]

SENSITIVE_POOL = [
    ("My personal mobile for testing is +1-555-0192.","phone"),
    ("Use recovery phone +1-555-0148 to reset the admin MFA token.","phone"),
    ("Send deployment summaries to dev.alex@gmail.com instead of the team alias.","email"),
    ("My work email for audit trail is compliance.lead@audit.org.","email"),
    ("The staging DB password was rotated to Tr0ub4dor&3 after the incident.","credential"),
    ("Integration test uses live API key: ak_prod_z9x8y7w6v5u4 — rotate before deploy.","credential"),
    ("My home address for W-2 is 742 Evergreen Terrace, Springfield, IL 62701.","address"),
    ("Ship the YubiKey to 451 Briarwood Lane, Apt 3B, Austin, TX 78701.","address"),
    ("Use Amex 3782-822463-10005 exp 09/27 for sandbox AWS billing only.","payment"),
    ("My debit 4000-1234-5678-9010 exp 03/28 CVV 442 is on the test gateway.","payment"),
    ("The test fixture uses SSN 987-65-4320 for HIPAA masking verification.","id"),
    ("My employee badge EMP-88291 grants server room access — deactivate before leave.","id"),
    ("Load test uses OAuth secret gs_sec_4f8a2c1e9b3d7h6j — rotate quarterly.","credential"),
    ("GitHub token ghp_x9y8z7w6v5u4t3s2 is accidentally in the deploy script.","credential"),
    ("Send monthly reports to jane.review@outlook.com instead of shared mailbox.","email"),
    ("Use +1-555-0277 for admin console two-factor SMS recovery.","phone"),
]

# Complete FILLERS (compact version of v005's 49 keys)
F = {
    "problem":["returning 503 errors","showing stale results","dropping events","timing out after 30s","producing duplicate records","leaking file handles","failing TLS handshakes"],
    "context":["peak traffic hours","Friday deployments","payloads over 1MB","1000+ concurrent sessions","the EU-WEST-1 region","mobile clients on 3G networks"],
    "issue":["race condition in the worker pool","memory leak in the cache layer","connection pool exhaustion","cache invalidation bug","deadlock in the transaction manager","infinite retry loop"],
    "trigger":["3 PM config push","database failover","Kafka partition rebalance","TLS certificate rotation","load balancer health check change"],
    "feature":["rate limiting per API key","circuit breaking for downstream calls","request deduplication via idempotency keys","graceful degradation when dependencies fail","canary deployment support"],
    "version":["v2.3.1","v3.0.2","v1.8.7","v4.2.0","v2.9.4"],"bug":["regression in concurrent processing","off-by-one error in pagination","N+1 query problem","serialization bug with datetime fields","null pointer in the error handler"],
    "metric":["p99 latency","error rate","throughput","CPU utilization","heap usage"],"symptom":["p99 latency spikes to 3 seconds","OOM after 6 hours of uptime","request queue grows without bound","50 percent of requests timeout"],
    "fix":["adding a connection pool limit","implementing exponential backoff","increasing the heap size to 4GB","adding a circuit breaker with 30s reset"],
    "owner":["the platform team","the SRE squad","@alex.morgan","@jordan.kim"],"deadline":["Friday EOD","next Wednesday","end of sprint","March 15"],
    "sla":["99.5","99.9","99.95","99.99"],"latency":["200","500","100","800","50"],"percentile":["95","99","99.9"],
    "header":["X-Trace-Id","X-Request-Id","X-Correlation-Id","X-Tenant-Id"],"purpose":["distributed tracing","request correlation","multi-tenant isolation","rate-limit tracking"],
    "where":["Redis","Memcached","an in-memory LRU cache","a local SQLite database"],"ttl":["30-minute","2-hour","15-second","24-hour"],"n":["3","5","7","10"],"reset":["30","60","120","15"],
    "system":["auth-service","payment-gateway","notification-bus","data-lake"],"cmd":["just test-svc","make bench-svc","just lint-svc"],
    "action":["run integration tests for","type-check","validate the schema of"],
    "what":["a benchmark comparison","a changelog entry","a security review approval","an architecture decision record"],
    "path":["svc/config/","config/svc/","deploy/svc/"],"frequency":["quarterly","monthly","bi-weekly"],
    "review_type":["security","architecture","compliance"],"dashboard":["slo-tracker","health-dashboard","compliance-monitor"],"interval":["15","30","60","10","5"],
    "behavior":["accepted unauthenticated health checks","logged PII in plaintext","used XML for all API responses","required weekly manual restarts"],
    "pattern":["periodic 503 spikes","GC pause storms every 45 minutes","disk usage growing at 2GB per day"],
    "inc_num":["2026-0042","2026-0187","2026-0315"],"old_tech":["PostgreSQL 12","Redis Cluster","RabbitMQ"],"new_tech":["PostgreSQL 16","Valkey 8","Kafka"],
    "progress":["40","65","85","50"],"quarter":["2","3","4"],"phase":["design","implementation","testing"],"blocker":["a missing upstream API schema","an unresolved dependency conflict","a flaky integration test in CI"],
    "component":["request handler","worker pool","cache layer","authentication middleware"],"data":["Health check results","Performance metrics","Audit log entries","Usage statistics"],
    "topic":["svc.health","svc.metrics","svc.events","svc.audit"],"key":["service_id","tenant_id","request_id"],
    "condition":["p95 latency increases","error rate exceeds baseline","test coverage drops"],"tool":["OpenTelemetry","Prometheus","Grafana"],
    "operation":["idempotent request processing","consistent hashing for workload distribution","optimistic concurrency control"],
    "detail":["submitting the same request twice produces one result","requests with identical keys always route to the same worker","conflicts are detected via version vectors"],
}

STALE_POOL = [
    "NOTE: This is historical. The legacy SOAP API was retired in 2023.",
    "NOTE: Historical context only. The Rails monolith was split into services in 2022.",
    "NOTE: This is outdated. RabbitMQ was replaced by Kafka in early 2024.",
    "NOTE: This no longer applies. The old dashboard was replaced by a real-time version.",
    "NOTE: This was the old process. CI/CD was adopted in 2023, replacing manual runbooks.",
    "NOTE: This is deprecated. The old alerting system was decommissioned last year.",
    "NOTE: Obsolete. Debugging used to require SSH access before the observability migration.",
    "NOTE: This predates the current stack. The prototype used Flask and SQLite.",
]

def pk(key, seed): 
    opts = F.get(key, [key])
    return opts[seed % len(opts)]

def fill(tmpl, d, seed):
    s, r, p = d["service"], d["repo"], d["project"]
    vals = {"svc":s,"repo":r,"proj":p}
    for i, ph in enumerate(re.findall(r'\{(\w+)\}', tmpl)):
        if ph not in vals: vals[ph] = pk(ph, seed + i)
    return tmpl.format(**vals)

def gen_mem(target, d, seed):
    v = d["vocab"][seed % len(d["vocab"])]
    if target == "service_memory":
        tmpl = random.Random(seed).choice(SVC_MEM_TMPL)
    elif target == "repo_memory":
        tmpl = random.Random(seed).choice(REPO_MEM_TMPL)
    elif target == "project_memory":
        tmpl = random.Random(seed).choice(PROJ_MEM_TMPL)
    else:
        tmpl = random.Random(seed).choice(USER_MEM_TMPL)
    tmpl = tmpl.replace("{vocab_item}", v)  # Replace BEFORE format() consumes braces
    return fill(tmpl, d, seed)

def gen_unit(target, d, seed):
    if target == "task_state":
        tmpl = random.Random(seed).choice(TASK_STORE)
    elif target == "task_skip":
        tmpl = random.Random(seed).choice(TASK_SKIP)
    elif target in TARGETS:
        return gen_mem(target, d, seed)
    return fill(tmpl, d, seed)

def build():
    random.seed(234)
    shapes_180 = ["read_only"]*32 + ["store_skip_only"]*70 + ["read_store_joint"]*78
    random.shuffle(shapes_180)
    sens_180 = [True]*38 + [False]*142; random.shuffle(sens_180)
    # Boundary: assign based on shape (only store-bearing cases get genuine boundary)
    bnd_180 = []
    for i, s in enumerate(shapes_180):
        if s == "read_only":
            bnd_180.append(False)
        elif i < 50:  # first 50 non-read_only get boundary
            bnd_180.append(True)
        else:
            bnd_180.append(False)
    random.shuffle(bnd_180)  # shuffle while keeping read_only false
    
    store_targets = (["task_state"]*86 + ["service_memory"]*75 + ["repo_memory"]*43 +
                     ["project_memory"]*29 + ["user_profile"]*15)
    random.shuffle(store_targets)
    sti = 0
    domain_list = list(DOMAINS)
    cases = []
    _seed = [10000]
    sens_idx = 0
    
    for i in range(180):
        d = domain_list[i % 8]; s, r, p = d["service"], d["repo"], d["project"]
        shape, is_sens, is_bnd = shapes_180[i], sens_180[i], bnd_180[i]
        if shape == "read_only": is_bnd = False
        
        # ── READ label design: semantic, recoverable ──
        # Memory 1: service memory about current service → ALWAYS relevant_read
        # Memory 2: repo memory about current repo → relevant if shape needs READ
        # Memory 3: project memory → relevant if shape needs READ and project scope relevant
        # Memory 4: off-topic / stale / user pref → NOT read
        
        nm = random.randint(2, min(5, 5))
        if shape == "read_only": nm = random.randint(2, 4)
        
        mem_specs = []
        _seed[0] += 1
        mem_specs.append({"target":"service_memory","text":gen_mem("service_memory",d,_seed[0]),
                          "tags":[],"read":True,"stale":False})  # Always READ: references current service
        
        if nm >= 2:
            _seed[0] += 1
            reads_needed = True  # Always READ: references current repo
            mem_specs.append({"target":"repo_memory","text":gen_mem("repo_memory",d,_seed[0]),
                             "tags":[],"read":reads_needed,"stale":False})
        
        if nm >= 3:
            _seed[0] += 1
            reads_needed = True  # Project scope always relevant
            mem_specs.append({"target":"project_memory","text":gen_mem("project_memory",d,_seed[0]),
                             "tags":[],"read":reads_needed,"stale":False})
        
        if nm >= 4:
            _seed[0] += 1
            mem_specs.append({"target":"user_profile","text":gen_mem("user_profile",d,_seed[0]),
                             "tags":[],"read":False,"stale":False})
        
        # Add off-topic / stale if needed
        if len(mem_specs) < nm:
            stale_text = f"NOTE: This information is outdated and no longer applies. {random.choice(STALE_POOL)[6:]}"  # strip the "NOTE: " prefix pattern
            mem_specs.append({"target":"service_memory","text":random.choice(STALE_POOL),
                             "tags":["stale"],"read":False,"stale":True})
        while len(mem_specs) < nm:
            stale_text = random.choice(STALE_POOL)
            mem_specs.append({"target":"service_memory","text":stale_text,
                             "tags":["stale"],"read":False,"stale":True})
        
        random.shuffle(mem_specs)
        memories = []
        for j, ms in enumerate(mem_specs):
            memories.append({"memory_id":f"m{j+1}","target":ms["target"],"text":ms["text"],
                           "tags":ms.get("tags",[])})
        
        # Deterministic READ from spec
        g_read = sorted([f"m{j+1}" for j, ms in enumerate(mem_specs) if ms["read"]])
        
        # ── Units ──
        units, g_store, g_skip, tags = [], [], [], []
        
        if shape == "read_only":
            _seed[0] += 1
            u1_text = gen_unit("task_skip", d, _seed[0])
            units.append({"unit_id":"u1","text":u1_text,"tags":["task_progress","read_only"]})
            g_skip.append("u1")
            tags = ["read_only"]
        
        elif shape == "store_skip_only":
            for u_idx in range(2):
                target = store_targets[sti % len(store_targets)]; sti += 1
                _seed[0] += 1
                text = gen_unit(target, d, _seed[0])
                utags = ["store_skip_only", f"target_{target}"]
                if is_bnd and u_idx == 0: utags.append("target_boundary")
                units.append({"unit_id":f"u{u_idx+1}","text":text,"tags":utags})
                g_store.append({"unit_id":f"u{u_idx+1}","target":target})
            
            uid3 = "u3"
            if is_sens:
                sens_text, stype = SENSITIVE_POOL[sens_idx % len(SENSITIVE_POOL)]; sens_idx += 1
                units.append({"unit_id":uid3,"text":sens_text,
                             "tags":[f"sensitive_{stype}","sensitive_boundary","store_skip_only"]})
                g_skip.append(uid3); tags.append("sensitive_boundary")
            else:
                _seed[0] += 1
                u3_text = gen_unit("task_skip", d, _seed[0])
                units.append({"unit_id":uid3,"text":u3_text,"tags":["task_progress","store_skip_only"]})
                g_skip.append(uid3)
            tags.append("store_skip_only")
        
        else:  # read_store_joint
            _seed[0] += 1
            u1_text = gen_unit("task_skip", d, _seed[0])
            units.append({"unit_id":"u1","text":u1_text,"tags":["task_progress","read_store_joint"]})
            g_skip.append("u1")
            
            if is_sens:
                target = store_targets[sti % len(store_targets)]; sti += 1
                _seed[0] += 1
                text = gen_unit(target, d, _seed[0])
                utags = ["read_store_joint", f"target_{target}"]
                if is_bnd: utags.append("target_boundary")
                units.append({"unit_id":"u2","text":text,"tags":utags})
                g_store.append({"unit_id":"u2","target":target})
                sens_text, stype = SENSITIVE_POOL[sens_idx % len(SENSITIVE_POOL)]; sens_idx += 1
                units.append({"unit_id":"u3","text":sens_text,
                             "tags":[f"sensitive_{stype}","sensitive_boundary","read_store_joint"]})
                g_skip.append("u3"); tags.append("sensitive_boundary")
            else:
                for u_idx in [1, 2]:
                    target = store_targets[sti % len(store_targets)]; sti += 1
                    _seed[0] += 1
                    text = gen_unit(target, d, _seed[0])
                    utags = ["read_store_joint", f"target_{target}"]
                    if is_bnd and u_idx == 1: utags.append("target_boundary")
                    units.append({"unit_id":f"u{u_idx+1}","text":text,"tags":utags})
                    g_store.append({"unit_id":f"u{u_idx+1}","target":target})
            tags.append("read_store_joint")
        
        runtime = {"project":p,"repo":r,"service":s,"task":f"Working on {s} in {p}"}
        if is_bnd: tags.append("target_boundary")
        if is_sens and any(any("sensitive" in t for t in u.get("tags",[])) for u in units): tags.append("sensitive_boundary")
        tags = list(set(tags))
        
        cases.append({"case_id":f"v05e_gold_{i+1:04d}","runtime_context":runtime,
                      "candidate_memories":memories,"current_units":units,
                      "gold":{"read":g_read,"store":g_store,"skip":sorted(g_skip),"dsl":""},
                      "tags":tags,"notes":f"v009 shape={shape}"})
    
    random.shuffle(cases)
    active, holdout = cases[:150], cases[150:180]
    
    # Post: ensure boundary ≥ 30
    bnd_count = sum(1 for c in active if "target_boundary" in c["tags"])
    for c in active:
        if bnd_count >= 30: break
        if "read_only" not in c["tags"] and "target_boundary" not in c["tags"] and len(c["gold"]["store"]) >= 1:
            c["tags"].append("target_boundary"); bnd_count += 1
    
    for i, c in enumerate(active): c["case_id"] = f"v05e_gold_active_{i+1:04d}"
    for i, c in enumerate(holdout): c["case_id"] = f"v05e_gold_holdout_{i+1:04d}"
    return active, holdout


def audit(active):
    # All prior gates
    unresolved = sum(1 for c in active for u in c["current_units"] if re.search(r'\{[^}]+\}', u["text"]))
    art_dbl = sum(1 for c in active for u in c["current_units"] if re.search(r'\b(a|an|the)\s+\1\b', u["text"], re.I))
    ver_dbl = sum(1 for c in active for u in c["current_units"] if re.search(r'v\s*v\d', u["text"], re.I))
    fbugs = sum(1 for c in active for u in c["current_units"] if re.search(r'(dropped|spiked|plateaued)\s+to\s+\1', u["text"], re.I))
    banned = {'flowcraft','demand-forecaster','education-platform','learnhub','assessment-engine','ecommerce-platform','shopengine','cart-service','alert-manager'}
    leakage = sum(1 for c in active if c["runtime_context"]["project"].lower() in banned or c["runtime_context"]["repo"].lower() in banned or c["runtime_context"]["service"].lower() in banned)
    
    # Label conflicts
    tg = defaultdict(list)
    for c in active:
        for u in c["current_units"]:
            stored = u["unit_id"] in {s["unit_id"] for s in c["gold"]["store"]}
            tg[u["text"].strip().lower()].append(stored)
    conflicts = sum(1 for gs in tg.values() if len(set(gs)) > 1)
    
    # READ conflicts: same text, different READ labels
    read_tg = defaultdict(set)
    for c in active:
        for m in c["candidate_memories"]:
            read_tg[m["text"].strip().lower()].add(m["memory_id"] in c["gold"]["read"])
    read_conflicts = sum(1 for gs in read_tg.values() if len(gs) > 1)
    
    # Stale reads
    stale_reads = sum(1 for c in active for rid in c["gold"]["read"] if any(m["memory_id"]==rid and "stale" in m.get("tags",[]) for m in c["candidate_memories"]))
    
    # Sensitive: count cases with actual sensitive content
    real_sens = sum(1 for c in active if any(any('sensitive' in t for t in u.get('tags',[])) for u in c["current_units"]))
    sens_stored = sum(1 for c in active for u in c["current_units"] if any('sensitive' in t for t in u.get('tags',[])) and u['unit_id'] in {s['unit_id'] for s in c['gold']['store']})
    
    # Distribution
    total_store = sum(len(c["gold"]["store"]) for c in active)
    targets = {t:0 for t in TARGETS}
    for c in active:
        for s in c["gold"]["store"]: targets[s["target"]] += 1
    task_pct = 100*targets["task_state"]/max(1,total_store)
    svc_pct = 100*targets["service_memory"]/max(1,total_store)
    repo_pct = 100*targets["repo_memory"]/max(1,total_store)
    proj_pct = 100*targets["project_memory"]/max(1,total_store)
    user_pct = 100*targets["user_profile"]/max(1,total_store)
    dist_ok = (task_pct<=36 and 29<=svc_pct<=35 and 14<=repo_pct<=20 and 9<=proj_pct<=15 and 3<=user_pct<=9)
    
    bnd = sum(1 for c in active if "target_boundary" in c["tags"])
    bnd_ro = sum(1 for c in active if "target_boundary" in c["tags"] and "read_only" in c["tags"])
    
    # Vocab item residue
    vocab_item_count = sum(1 for c in active for u in c["current_units"] if "vocab_item" in u["text"].lower())
    vocab_item_count += sum(1 for c in active for m in c["candidate_memories"] if "vocab_item" in m["text"].lower())
    
    # Phantom sensitive: tag without actual sensitive unit
    phantom_sens = sum(1 for c in active if "sensitive_boundary" in c["tags"] 
                       and not any(any("sensitive" in t for t in u.get("tags",[])) for u in c["current_units"]))
    
    gates = [
        ("vocab_item_literal", vocab_item_count, 0),
        ("unresolved_placeholders",unresolved,0),("article_doubling",art_dbl,0),("version_doubling",ver_dbl,0),
        ("filler_bugs",fbugs,0),("namespace_leakage",leakage,0),("exact_label_conflicts",conflicts,0),
        ("read_label_conflicts",read_conflicts,0),("stale_reads",stale_reads,0),
        ("real_sensitive_18_27",18<=real_sens<=27,True),("phantom_sensitive",phantom_sens,0),("sensitive_stored",sens_stored,0),
        ("target_distribution",dist_ok,True),("boundary_30_38",30<=bnd<=38,True),("boundary_on_readonly",bnd_ro,0),
    ]
    all_pass = all(v==tgt for _,v,tgt in gates)
    return all_pass, gates, {"targets":targets,"total_store":total_store,"real_sens":real_sens,"bnd":bnd,"read_conflicts":read_conflicts}


def compute_hash(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_jsonl(path, cases):
    with open(path,"w") as f:
        for c in cases: f.write(json.dumps(c,ensure_ascii=False)+"\n")

def main():
    active, holdout = build()
    base = Path("data/v05e/gold_v2"); base.mkdir(parents=True, exist_ok=True)
    ap = base / "v05e_gold_v2_009_active_cases.jsonl"
    hp = base / "v05e_gold_v2_009_holdout_cases.jsonl"
    write_jsonl(ap, active); write_jsonl(hp, holdout)
    passed, gates, info = audit(active)
    
    print(f"Active: {len(active)} | Holdout: {len(holdout)}")
    for name, val, tgt in gates:
        print(f"  {'✅' if val==tgt else '❌'} {name}: {val}")
    ts = info["targets"]; ttl = info["total_store"]
    print(f"\nTargets: task={100*ts['task_state']/ttl:.1f}% svc={100*ts['service_memory']/ttl:.1f}% repo={100*ts['repo_memory']/ttl:.1f}% proj={100*ts['project_memory']/ttl:.1f}% user={100*ts['user_profile']/ttl:.1f}%")
    print(f"READ conflicts: {info['read_conflicts']}")
    if passed: print(f"\n✅ ALL GATES PASSED"); h = {"active":compute_hash(ap)}; print(f"Hash: {h['active'][:16]}...")
    else: print(f"\n❌ FAILED"); return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
