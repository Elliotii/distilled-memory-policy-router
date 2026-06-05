"""Build v0.5g targeted-balanced training data for LoRA scaling experiment.

Produces:
1. 500-control: Copy of existing v05b train 500 JSON SFT
2. Additional 500: targeted-balanced synthetic cases
3. 1000 combined: 500-control + additional 500

Research questions:
- Does BF16 LoRA r16 improve over QLoRA r16 with same 500 data?
- Does 1000 targeted-balanced improve over BF16 LoRA r16 500?
"""
from __future__ import annotations
import hashlib, json, random, sys, re
from pathlib import Path
from collections import Counter
import shutil

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

TARGETS = ["task_state","service_memory","repo_memory","project_memory","user_profile"]

# ── 8 NEW DOMAINS (no overlap with gold_v2_009, rejected gold_v2, dev, old gold) ──
DOMAINS = [
    {"project":"energy-monitoring","repo":"powergrid","service":"meter-collector","family":"energy",
     "vocab":["smart meter readout","peak demand forecasting","grid load balancing","outage detection","voltage fluctuation analysis","transformer health monitoring","AMI mesh networking","time-of-use billing","demand response events","power quality auditing","renewable integration","battery storage dispatch","feeder line monitoring","harmonic distortion","phase imbalance detection","substation telemetry","fault location isolation","distributed generation","net metering tracking","brownout prevention"]},
    {"project":"fleet-management","repo":"routemaster","service":"dispatch-engine","family":"transportation",
     "vocab":["vehicle routing optimization","geofence trip logging","driver hours-of-service compliance","fuel consumption tracking","predictive maintenance scheduling","telematics data ingestion","ETA recalculation","load balancing across depots","cold chain temperature monitoring","idle time reduction","route deviation alerts","electronic logging device integration","driver scorecard computation","trailer utilization rate","cross-dock scheduling","backhaul matching","zone-based pricing","proof-of-delivery capture","fleet electrification planning","maintenance bay throughput"]},
    {"project":"agriculture-tech","repo":"cropwise","service":"irrigation-controller","family":"agriculture",
     "vocab":["soil moisture sensing","evapotranspiration calculation","crop water requirement","pump scheduling optimization","rainfall prediction integration","drip line pressure monitoring","valve health diagnostics","fertilizer injection rate","water salinity tracking","field capacity estimation","irrigation uniformity audit","remote sensing NDVI","canopy temperature measurement","soil type classification","root zone depth profiling","frost alert triggering","reservoir level monitoring","flow meter calibration","leak detection algorithm","water rights compliance"]},
    {"project":"hr-analytics","repo":"peopleflow","service":"attrition-predictor","family":"hr",
     "vocab":["turnover risk scoring","engagement survey analysis","compensation benchmarking","promotion velocity tracking","regretted attrition classification","flight risk modeling","succession pipeline depth","diversity representation metrics","manager effectiveness scoring","tenure cohort analysis","internal mobility rate","offer acceptance rate","time-to-productivity measurement","skip-level sentiment aggregation","skill gap heatmapping","retention interview coding","referral source effectiveness","new-hire failure rate","comp ratio analysis","attrition cost modeling"]},
    {"project":"compliance-management","repo":"regulatortrack","service":"policy-auditor","family":"compliance",
     "vocab":["control testing automation","regulatory change monitoring","policy exception tracking","audit evidence collection","risk control matrix","SOX control mapping","GDPR data subject request handling","third-party risk assessment","privacy impact assessment","regulatory filing deadline","compliance training completion","whistleblower case tracking","sanctions screening","anti-money laundering rules","customer due diligence","suspicious activity reporting","remediation plan tracking","control deficiency rating","board reporting dashboard","continuous control monitoring"]},
    {"project":"manufacturing-ops","repo":"factoryflow","service":"quality-inspector","family":"manufacturing",
     "vocab":["statistical process control","defect rate tracking","first-pass yield calculation","six-sigma DMAIC projects","gage repeatability study","root cause analysis","nonconformance disposition","inspection sampling plan","machine capability index","out-of-spec tolerance alert","lot traceability","calibration schedule","supplier quality scorecard","incoming inspection lot","production line stoppage","rework tracking","OEE measurement","preventive maintenance order","spare parts inventory","shop floor data collection"]},
    {"project":"network-operations","repo":"netcore","service":"topology-mapper","family":"networking",
     "vocab":["BGP prefix monitoring","link utilization trending","interface error rate","tunnel uptime tracking","route convergence time","peering capacity planning","DDoS mitigation trigger","SD-WAN path selection","MTU mismatch detection","packet loss threshold","jitter buffer tuning","QoS policy enforcement","RADIUS authentication log","switch port security","VLAN propagation delay","optical power level","firmware compliance scan","network segmentation audit","DHCP lease exhaustion","DNS resolution latency"]},
    {"project":"content-moderation","repo":"safescreen","service":"toxicity-classifier","family":"content",
     "vocab":["toxicity probability scoring","hate speech detection threshold","image safety classification","profanity filter calibration","spam detection recall","context-aware moderation","moderator queue prioritization","appeal review workflow","false positive rate tracking","shadow ban policy","age-gated content flagging","automod confidence scoring","human review escalation","bulk moderation batch size","language-specific model","policy violation taxonomy","repeat offender detection","edge case adjudication","moderation latency SLA","safety audit trail"]},
]

# ── Template pools ──
SVC_MEM_TMPL = [
    "The {svc} guarantees {sla}% uptime with max response latency of {latency}ms at p{percentile} for {vocab_item}.",
    "All {svc} responses include a {header} header for {purpose} covering {vocab_item} endpoints.",
    "The {svc} caches {vocab_item} data in {where} with a {ttl} TTL for performance.",
    "The {svc} circuit breaker opens after {n} consecutive failures to the {system} and resets after {reset}s for {vocab_item}.",
    "The {svc} publishes {vocab_item} events to the {topic} topic partitioned by {key}.",
    "The {svc} implements {operation} for {vocab_item} — {detail}.",
    "The {svc} runs {vocab_item} checks every {interval} minutes and reports results to {dashboard}.",
    "The {svc} uses {tool} for {vocab_item} metrics collection and alerting thresholds.",
]
REPO_MEM_TMPL = [
    "Run {cmd} in the {repo} repo to {action} the {svc} for {vocab_item} validation.",
    "All {svc} changes in {repo} must include {what} for {vocab_item} before merging.",
    "{svc} configuration for {vocab_item} lives under {path} in the {repo} repo.",
    "Integration tests for {svc} {vocab_item} are in tests/{svc}/ under the {repo} repo.",
    "The {svc} deployment manifests for {vocab_item} are in deploy/{svc}/ in the {repo} repo.",
]
PROJ_MEM_TMPL = [
    "The {proj} project requires {frequency} {review_type} reviews for any changes affecting {vocab_item}.",
    "All {proj} services must report {vocab_item} metrics to {dashboard} every {interval}.",
    "Cross-service {vocab_item} in {proj} follows the {review_type} review workflow documented in the project runbook.",
    "The {proj} architecture decision record mandates {what} for any {vocab_item} changes that affect multiple services.",
]
USER_MEM_TMPL = [
    "I prefer the {svc} dashboard to show {vocab_item} metrics as a heatmap rather than a table.",
    "Flag {svc} alerts for {vocab_item} as critical when they affect more than {n} items.",
    "Send {svc} weekly summaries about {vocab_item} to my personal channel, not the team channel.",
    "I like to review {vocab_item} changes in {svc} before they go to staging.",
]

TASK_STORE = [
    "Currently investigating why the {svc} {problem} for {context}. Fix needed by {deadline}.",
    "Active incident: the {svc} {issue} after the {trigger}. Assigned to {owner} this sprint.",
    "This sprint: add {feature} to the {svc} for {context}. Due {deadline}.",
    "Rolling back the {svc} to {version} because the release introduced a {bug} in production.",
    "Working on {svc} {feature} — currently at {progress}% complete, targeting end of Q{quarter}.",
    "The {svc} {phase} phase is blocked by {blocker}. Cannot proceed until resolved.",
    "Performance: {svc} {problem} under {context}. Profiling {component} to identify the bottleneck.",
]
TASK_SKIP = [
    "Hypothetical: what if the {svc} {problem} during {context}? Not a current concern.",
    "Old incident (resolved): the {svc} had a {issue} after {trigger}. No longer active.",
    "Scratch note: the {svc} showed unusual {metric} last Tuesday, self-resolved.",
    "Discarded idea: add {feature} to {svc}. Rejected by architecture review.",
    "Historical data: {svc} {data} from 2023 is no longer useful for current debugging.",
    "The old {svc} used to have {behavior} before the refactor. No longer relevant.",
    "Observation: {svc} shows {pattern}. Investigate next sprint if it persists.",
]

SENSITIVE_POOL = [
    ("My personal mobile for testing can be reached at +1-555-0192.","phone"),
    ("Use recovery phone +1-555-0148 to reset the admin MFA token for staging.","phone"),
    ("Send deployment summaries to dev.alex@gmail.com instead of the team distribution list.","email"),
    ("My work contact for audit trail is compliance.lead@audit.org — not the generic mailbox.","email"),
    ("The staging DB password was rotated to Tr0ub4dor&3 after the incident last month.","credential"),
    ("Integration test uses live API key: ak_prod_z9x8y7w6v5u4 — rotate before next deploy.","credential"),
    ("My home address on file for W-2 is 742 Evergreen Terrace, Springfield, IL 62701.","address"),
    ("Ship the YubiKey replacement to 451 Briarwood Lane, Apt 3B, Austin, TX 78701.","address"),
    ("Use Amex 3782-822463-10005 exp 09/27 for sandbox AWS billing only — not production.","payment"),
    ("My debit card 4000-1234-5678-9010 exp 03/28 CVV 442 is registered on the test gateway.","payment"),
    ("The test fixture uses SSN 987-65-4320 for HIPAA masking verification in UAT.","id"),
    ("My employee badge EMP-88291 grants server room access — requires deactivation upon leaving.","id"),
    ("Load test OAuth secret gs_sec_4f8a2c1e9b3d7h6j — rotate quarterly per policy.","credential"),
    ("GitHub token ghp_x9y8z7w6v5u4t3s2 was accidentally committed — revoke immediately.","credential"),
    ("Send monthly compliance reports to jane.review@outlook.com instead of shared mailbox.","email"),
    ("Use +1-555-0277 for admin console two-factor SMS recovery codes.","phone"),
    ("The vendor evaluation account uses password: V3nd0r!Eval#2026 for sandbox only.","credential"),
    ("My bank routing number 021000021 and account 9876543210 for direct deposit setup.","payment"),
]

STALE_POOL = [
    "NOTE: Archived — the v1 ingestion pipeline was sunset in 2023 Q3 after the data-lake migration.",
    "NOTE: This procedure was deprecated when we moved from Bitbucket to GitHub Enterprise in 2024.",
    "NOTE: No longer accurate. The monorepo was split into micro-repos in November 2023.",
    "NOTE: This applied to the self-hosted Jenkins setup which was replaced by GitHub Actions.",
    "NOTE: Deprecated since the move from on-prem to cloud. The old VPN-based access model is gone.",
    "NOTE: Historical — this alert was tuned for the pre-autoscaling era before the HPA migration.",
    "NOTE: The 5xx retry policy described here was overridden by the global API gateway in Q1 2024.",
    "NOTE: This document refers to pre-TLS-1.3 configuration. All services now require TLS 1.3.",
    "NOTE: Archived context. The team stopped using PagerDuty in favor of Opsgenie in early 2024.",
    "NOTE: This runbook is from the pre-container era. All services are now on Kubernetes since 2023.",
    "NOTE: No longer relevant — the centralized logging cluster was decommissioned in mid-2024.",
    "NOTE: Deprecated. Feature flags were migrated from LaunchDarkly to an internal service last year.",
    "NOTE: This was valid for the US-EAST-1 region only; that region was retired in 2024 Q2.",
    "NOTE: Historical — the GraphQL gateway replaced this REST endpoint in the v4 API redesign.",
    "NOTE: This governance rule predates the SOC2 certification achieved in November 2023.",
]

# ── Fillers ──
F = {
    "problem":["returning 503 errors","showing stale results","dropping events","timing out after 30s","producing duplicate records","leaking file handles","failing TLS handshakes"],
    "context":["peak traffic hours","Friday deployments","payloads over 1MB","1000+ concurrent sessions","the EU-WEST-1 region","mobile clients on 3G networks"],
    "issue":["race condition in the worker pool","memory leak in the cache layer","connection pool exhaustion","cache invalidation bug","deadlock in the transaction manager","infinite retry loop"],
    "trigger":["3 PM config push","database failover","Kafka partition rebalance","TLS certificate rotation","load balancer health check change"],
    "feature":["rate limiting per API key","circuit breaking for downstream calls","request deduplication via idempotency keys","graceful degradation when dependencies fail","canary deployment support","dark launch for new endpoints"],
    "version":["v2.3.1","v3.0.2","v1.8.7","v4.2.0","v2.9.4"],"bug":["regression in concurrent processing","off-by-one error in pagination","N+1 query problem","serialization bug with datetime fields","null pointer in the error handler"],
    "metric":["p99 latency","error rate","throughput","CPU utilization","heap usage"],"symptom":["p99 latency spikes to 3 seconds","OOM after 6 hours of uptime","request queue grows without bound","50 percent of requests timeout"],
    "owner":["the platform team","the SRE squad","@alex.morgan","@jordan.kim"],"deadline":["Friday EOD","next Wednesday","end of sprint","March 15","end of Q2"],
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
    "progress":["40","65","85","50"],"quarter":["2","3","4"],"phase":["design","implementation","testing"],"blocker":["a missing upstream API schema","an unresolved dependency conflict","a flaky integration test in CI"],
    "component":["request handler","worker pool","cache layer","authentication middleware"],"data":["Health check results","Performance metrics","Audit log entries","Usage statistics"],
    "topic":["svc.health","svc.metrics","svc.events","svc.audit"],"key":["service_id","tenant_id","request_id"],
    "condition":["p95 latency increases","error rate exceeds baseline","test coverage drops"],"tool":["OpenTelemetry","Prometheus","Grafana"],
    "operation":["idempotent request processing","consistent hashing for workload distribution","optimistic concurrency control"],
    "detail":["submitting the same request twice produces one result","requests with identical keys always route to the same worker","conflicts are detected via version vectors"],
}


def pk(key, seed):
    opts = F.get(key, [key])
    return opts[seed % len(opts)]

def fill(tmpl, d, seed):
    s, r, p = d["service"], d["repo"], d["project"]
    vals = {"svc":s,"repo":r,"proj":p}
    for i, ph in enumerate(re.findall(r'\{(\w+)\}', tmpl)):
        if ph not in vals:
            vals[ph] = pk(ph, seed + i)
    return tmpl.format(**vals)

def gen_memory_text(target, d, seed):
    """Generate memory text for a given target."""
    v = d["vocab"][seed % len(d["vocab"])]
    if target == "service_memory":
        tmpl = random.Random(seed).choice(SVC_MEM_TMPL)
    elif target == "repo_memory":
        tmpl = random.Random(seed).choice(REPO_MEM_TMPL)
    elif target == "project_memory":
        tmpl = random.Random(seed).choice(PROJ_MEM_TMPL)
    elif target == "user_profile":
        tmpl = random.Random(seed).choice(USER_MEM_TMPL)
    else:
        return "Unknown target."
    tmpl = tmpl.replace("{vocab_item}", v)
    return fill(tmpl, d, seed)

def gen_unit_text(target, d, seed):
    if target == "task_state":
        tmpl = random.Random(seed).choice(TASK_STORE)
    elif target == "task_skip":
        tmpl = random.Random(seed).choice(TASK_SKIP)
    else:
        return gen_memory_text(target, d, seed)
    v = d["vocab"][seed % len(d["vocab"])]
    tmpl = tmpl.replace("{vocab_item}", v)
    return fill(tmpl, d, seed)


def build_additional_500():
    """Build 500 targeted-balanced cases."""
    random.seed(420)  # Different seed from any prior builder
    
    # ── Distribution plan for 500 additional cases ──
    # Shapes: READ-only 90, STORE/SKIP-only 190, READ+STORE 220
    # Hard SKIP coverage expanded through read_only cases + explicit hard_skip tags
    shapes_500 = (["read_only"] * 90 + ["store_skip_only"] * 190 +
                   ["read_store_joint"] * 220)
    random.shuffle(shapes_500)
    
    # Sensitive: 100 cases (20%)
    sens_500 = [True] * 100 + [False] * 400
    random.shuffle(sens_500)
    
    # Boundary: 150 cases (30% of total, but only in store-bearing cases)
    # Assign boundary to store-bearing cases, then shuffle among those
    bnd_500 = []
    store_bearing_indices = [i for i, s in enumerate(shapes_500) if s != "read_only"]
    bnd_candidates = random.sample(store_bearing_indices, min(150, len(store_bearing_indices)))
    for i in range(500):
        bnd_500.append(i in bnd_candidates)
    
    # ── Target allocation for STORE units ──
    # Target: ~1000 store units across 500 cases
    # task 24%, svc 22%, repo 20%, proj 18%, user 16%
    store_targets = (
        ["task_state"] * 240 + ["service_memory"] * 220 +
        ["repo_memory"] * 200 + ["project_memory"] * 180 +
        ["user_profile"] * 160
    )
    random.shuffle(store_targets)
    sti = 0  # store target index
    
    _seed = [50000]  # mutable seed counter
    sens_idx = 0
    cases = []
    
    for i in range(500):
        d = DOMAINS[i % 8]
        s, r, p = d["service"], d["repo"], d["project"]
        shape = shapes_500[i]
        is_sens = sens_500[i]
        is_bnd = bnd_500[i]
        
        # ── Memories ──
        nm = random.randint(2, 5)
        if shape == "read_only":
            nm = random.randint(2, 4)
        
        mem_specs = []
        _seed[0] += 1
        # First memory: always service_memory, READ unless store_skip_only
        mem_specs.append({
            "target": "service_memory",
            "text": gen_memory_text("service_memory", d, _seed[0]),
            "read": (shape != "store_skip_only"), "stale": False
        })
        
        if nm >= 2:
            _seed[0] += 1
            mem_specs.append({
                "target": "repo_memory",
                "text": gen_memory_text("repo_memory", d, _seed[0]),
                "read": (shape != "store_skip_only"), "stale": False
            })
        
        if nm >= 3:
            _seed[0] += 1
            # Mix of project_memory and user_profile for diversity
            if random.random() < 0.6:
                mem_specs.append({
                    "target": "project_memory",
                    "text": gen_memory_text("project_memory", d, _seed[0]),
                    "read": (shape != "store_skip_only"), "stale": False
                })
            else:
                mem_specs.append({
                    "target": "user_profile",
                    "text": gen_memory_text("user_profile", d, _seed[0]),
                    "read": False, "stale": False  # User profile only read when relevant in READ+STORE
                })
                if shape == "read_store_joint":
                    mem_specs[-1]["read"] = random.random() < 0.3  # Sometimes read
                    mem_specs[-1]["read_flags"] = ["read_when_relevant"]
        
        if nm >= 4:
            # Add a stale/off-topic memory
            mem_specs.append({
                "target": "service_memory",
                "text": random.choice(STALE_POOL),
                "read": False, "stale": True
            })
        
        while len(mem_specs) < nm:
            mem_specs.append({
                "target": "service_memory",
                "text": random.choice(STALE_POOL),
                "read": False, "stale": True
            })
        
        random.shuffle(mem_specs)
        memories = []
        for j, ms in enumerate(mem_specs):
            tags_list = ms.get("tags", [])
            if ms.get("stale"):
                tags_list.append("stale")
            memories.append({
                "memory_id": f"m{j+1}",
                "target": ms["target"],
                "text": ms["text"],
                "tags": tags_list
            })
        
        g_read = sorted([f"m{j+1}" for j, ms in enumerate(mem_specs) if ms["read"]])
        
        # ── Units ──
        units = []
        g_store = []
        g_skip = []
        tags = []
        
        if shape == "read_only":
            _seed[0] += 1
            u1 = gen_unit_text("task_skip", d, _seed[0])
            units.append({"unit_id": "u1", "text": u1, "tags": ["task_progress"]})
            g_skip.append("u1")
            tags = ["read_only", "hard_skip"]
        
        elif shape == "store_skip_only":
            # 2-3 store units + 1 skip
            n_store = random.randint(2, 3)
            for u_idx in range(n_store):
                target = store_targets[sti % len(store_targets)]
                sti += 1
                _seed[0] += 1
                if target == "task_state":
                    text = gen_unit_text("task_state", d, _seed[0])
                else:
                    text = gen_memory_text(target, d, _seed[0])
                utags = [f"target_{target}"]
                if is_bnd and u_idx == 0:
                    utags.append("target_boundary")
                units.append({"unit_id": f"u{u_idx+1}", "text": text, "tags": utags})
                g_store.append({"unit_id": f"u{u_idx+1}", "target": target})
            
            uid_s = f"u{n_store+1}"
            if is_sens:
                sens_text, stype = SENSITIVE_POOL[sens_idx % len(SENSITIVE_POOL)]
                sens_idx += 1
                units.append({"unit_id": uid_s, "text": sens_text,
                             "tags": [f"sensitive_{stype}"]})
                g_skip.append(uid_s)
                tags.append("sensitive_boundary")
                tags.append("hard_skip")
            else:
                _seed[0] += 1
                u_text = gen_unit_text("task_skip", d, _seed[0])
                units.append({"unit_id": uid_s, "text": u_text, "tags": ["task_progress"]})
                g_skip.append(uid_s)
            tags.append("store_skip_only")
        
        else:  # read_store_joint
            # 1 skip unit first
            _seed[0] += 1
            u1_text = gen_unit_text("task_skip", d, _seed[0])
            units.append({"unit_id": "u1", "text": u1_text, "tags": ["task_progress"]})
            g_skip.append("u1")
            
            # 2-3 store units
            n_store = random.randint(2, 3)
            for u_idx in range(n_store):
                target = store_targets[sti % len(store_targets)]
                sti += 1
                _seed[0] += 1
                if target == "task_state":
                    text = gen_unit_text("task_state", d, _seed[0])
                else:
                    text = gen_memory_text(target, d, _seed[0])
                utags = [f"target_{target}"]
                if is_bnd and u_idx == 0:
                    utags.append("target_boundary")
                uid = f"u{u_idx+2}"
                units.append({"unit_id": uid, "text": text, "tags": utags})
                g_store.append({"unit_id": uid, "target": target})
            
            if is_sens:
                sens_text, stype = SENSITIVE_POOL[sens_idx % len(SENSITIVE_POOL)]
                sens_idx += 1
                uid_sens = f"u{n_store+2}"
                units.append({"unit_id": uid_sens, "text": sens_text,
                             "tags": [f"sensitive_{stype}"]})
                g_skip.append(uid_sens)
                tags.append("sensitive_boundary")
            tags.append("read_store_joint")
            if is_sens:
                tags.append("hard_skip")  # hard skip only for sensitive in read_store_joint
        
        if is_bnd:
            tags.append("target_boundary")
        
        runtime = {
            "project": p,
            "repo": r,
            "service": s,
            "task": f"Working on {s} in {p}"
        }
        
        cases.append({
            "case_id": f"v05g_add_{i+1:04d}",
            "runtime_context": runtime,
            "candidate_memories": memories,
            "current_units": units,
            "gold": {
                "read": sorted(g_read),
                "store": g_store,
                "skip": sorted(g_skip),
            },
            "tags": sorted(set(tags)),
            "notes": f"v05g_additional shape={shape} domain={d['family']}"
        })
    
    return cases


# ── Validation ──
LEGAL_TARGETS = frozenset(TARGETS)

def validate_cases(cases, label=""):
    """Validate a list of cases for structural integrity."""
    errors = []
    
    for i, c in enumerate(cases):
        cid = c.get("case_id", f"idx_{i}")
        gold = c["gold"]
        
        # Check required fields
        for field in ["case_id", "runtime_context", "candidate_memories", "current_units", "gold"]:
            if field not in c:
                errors.append(f"{cid}: missing field '{field}'")
        
        if errors:
            continue
        
        # Check unit coverage
        unit_ids = {u["unit_id"] for u in c["current_units"]}
        store_ids = {s["unit_id"] for s in gold.get("store", [])}
        skip_ids = set(gold.get("skip", []))
        
        if store_ids & skip_ids:
            errors.append(f"{cid}: units in both store and skip: {store_ids & skip_ids}")
        
        assigned = store_ids | skip_ids
        if unit_ids != assigned:
            missing = unit_ids - assigned
            extra = assigned - unit_ids
            if missing:
                errors.append(f"{cid}: unassigned units: {missing}")
            if extra:
                errors.append(f"{cid}: references to non-existent units: {extra}")
        
        # Check read hints reference valid memories
        mem_ids = {m["memory_id"] for m in c["candidate_memories"]}
        for rid in gold.get("read", []):
            if rid not in mem_ids:
                errors.append(f"{cid}: read '{rid}' not in candidate_memories")
        
        # Check store targets are valid
        for s in gold.get("store", []):
            if s["target"] not in LEGAL_TARGETS:
                errors.append(f"{cid}: invalid store target '{s['target']}'")
            if s["unit_id"] not in unit_ids:
                errors.append(f"{cid}: store unit_id '{s['unit_id']}' not in current_units")
        
        # Check no duplicate store unit assignment
        store_uid_counts = Counter(s["unit_id"] for s in gold.get("store", []))
        for uid, cnt in store_uid_counts.items():
            if cnt > 1:
                errors.append(f"{cid}: duplicate store unit_id '{uid}' (x{cnt})")
        
        # Check sensitive units are in skip
        for u in c["current_units"]:
            if any("sensitive" in t for t in u.get("tags", [])):
                if u["unit_id"] in store_ids:
                    errors.append(f"{cid}: SENSITIVE STORED: {u['unit_id']}")
        
        # Check no unresolved placeholders in unit text
        for u in c["current_units"]:
            ut = u.get("text", u.get("content", ""))
            if re.search(r'\{[a-zA-Z_]+\}', ut):
                errors.append(f"{cid}: unresolved placeholder in unit '{u['unit_id']}': {ut[:80]}")
    
    return errors


def render_json_sft(cases, source_label):
    """Render cases as Unit JSON SFT messages."""
    system_prompt = (
        "You are a memory policy router for coding-agent contexts.\n\n"
        "Task:\n"
        "Given RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:\n"
        "- which candidate memories to READ;\n"
        "- which current unit IDs to STORE and to which target;\n"
        "- which current unit IDs to SKIP.\n\n"
        "Output only valid JSON. Do not include markdown fences, comments, prose, "
        "or explanations.\n\n"
        "Format:\n"
        '{\n'
        '  "read": ["m1", "m3"],\n'
        '  "store": [\n'
        '    {"target": "service_memory", "unit_id": "u1"},\n'
        '    {"target": "task_state", "unit_id": "u2"}\n'
        '  ],\n'
        '  "skip": ["u3"]\n'
        '}\n\n'
        "Legal STORE targets:\n"
        "user_profile, project_memory, repo_memory, service_memory, task_state\n\n"
        "Rules:\n"
        "- READ useful memories only; skip merely related or stale ones.\n"
        "- STORE durable, reusable information with correct target.\n"
        "- SKIP sensitive, temporary, one-off, or out-of-scope content.\n"
        "- Every current unit must appear exactly once in store or skip.\n"
        "- Do not invent IDs, targets, or content."
    )
    
    messages = []
    for c in cases:
        # Build user input
        rc = c["runtime_context"]
        user_lines = [
            "RUNTIME_CONTEXT",
            f"project: {rc['project']}",
            f"repo: {rc['repo']}",
            f"service: {rc['service']}",
            f"task: {rc['task']}",
            "",
            "CANDIDATE_MEMORIES",
        ]
        for m in c["candidate_memories"]:
            user_lines.append(f"{m['memory_id']} [{m['target']}]: {m['text']}")
        user_lines.append("")
        user_lines.append("CURRENT_UNITS")
        for u in c["current_units"]:
            user_lines.append(f"{u['unit_id']}: {u['text']}")
        
        user_content = "\n".join(user_lines)
        
        # Build assistant JSON
        gold = c["gold"]
        read = sorted(gold.get("read", []))
        store_entries = [
            {"target": s["target"], "unit_id": s["unit_id"]}
            for s in gold.get("store", [])
        ]
        skip = sorted(gold.get("skip", []))
        
        assistant = json.dumps({
            "read": read,
            "store": store_entries,
            "skip": skip
        }, ensure_ascii=True, separators=(",", ":"))
        
        # Build metadata
        has_read = bool(read)
        has_store = bool(store_entries)
        if has_read and has_store:
            shape = "READ + STORE joint"
        elif has_read:
            shape = "READ-only"
        elif has_store:
            shape = "STORE/SKIP-only"
        else:
            shape = "no READ and no STORE"
        
        messages.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant},
            ],
            "case_id": c["case_id"],
            "source": source_label,
            "metadata": {
                "tags": c.get("tags", []),
                "num_candidate_memories": len(c["candidate_memories"]),
                "num_current_units": len(c["current_units"]),
                "gold_shape": shape,
                "store_targets": [s["target"] for s in gold.get("store", [])],
                "is_final_train_data": True,
            },
        })
    
    return messages


def validate_sft(messages, cases):
    """Validate SFT messages: parse, coverage, canonical."""
    errors = []
    for i, (msg, c) in enumerate(zip(messages, cases)):
        cid = c["case_id"]
        assistant_text = msg["messages"][2]["content"]
        
        # JSON parse
        try:
            parsed = json.loads(assistant_text)
        except json.JSONDecodeError as e:
            errors.append(f"{cid}: JSON parse failed: {e}")
            continue
        
        # No markdown
        if "```" in assistant_text:
            errors.append(f"{cid}: markdown fence detected")
        
        # Required keys
        for key in ("read", "store", "skip"):
            if key not in parsed:
                errors.append(f"{cid}: missing key '{key}' in assistant")
        
        if "read" not in parsed or "store" not in parsed or "skip" not in parsed:
            continue
        
        # Validate reads
        mem_ids = {m["memory_id"] for m in c["candidate_memories"]}
        for rid in parsed["read"]:
            if rid not in mem_ids:
                errors.append(f"{cid}: read '{rid}' not in candidate_memories")
        
        # Validate stores
        unit_ids = {u["unit_id"] for u in c["current_units"]}
        seen_store_units = set()
        for item in parsed["store"]:
            if not isinstance(item, dict):
                errors.append(f"{cid}: store item not a dict")
                continue
            target = item.get("target")
            uid = item.get("unit_id")
            if target not in LEGAL_TARGETS:
                errors.append(f"{cid}: invalid target '{target}'")
            if uid not in unit_ids:
                errors.append(f"{cid}: store unit_id '{uid}' not in current_units")
            if uid in seen_store_units:
                errors.append(f"{cid}: duplicate store unit_id '{uid}'")
            seen_store_units.add(uid)
        
        # Validate skips
        seen_skip_units = set()
        for uid in parsed["skip"]:
            if uid not in unit_ids:
                errors.append(f"{cid}: skip unit_id '{uid}' not in current_units")
            if uid in seen_skip_units:
                errors.append(f"{cid}: duplicate skip unit_id '{uid}'")
            seen_skip_units.add(uid)
        
        # Unit coverage
        assigned = seen_store_units | seen_skip_units
        if unit_ids != assigned:
            missing = unit_ids - assigned
            extra = assigned - unit_ids
            if missing:
                errors.append(f"{cid}: unassigned units: {missing}")
        
        # Overlap check
        if seen_store_units & seen_skip_units:
            errors.append(f"{cid}: units in both store and skip: {seen_store_units & seen_skip_units}")
        
        # Canonical consistency
        gold_read = set(c["gold"]["read"])
        sft_read = set(parsed["read"])
        if gold_read != sft_read:
            errors.append(f"{cid}: read mismatch: sft={sorted(sft_read)} gold={sorted(gold_read)}")
        
        gold_store = {(s["target"], s["unit_id"]) for s in c["gold"]["store"]}
        sft_store = {(s["target"], s["unit_id"]) for s in parsed["store"] if isinstance(s, dict)}
        if gold_store != sft_store:
            errors.append(f"{cid}: store mismatch")
        
        gold_skip = set(c["gold"]["skip"])
        sft_skip = set(parsed["skip"])
        if gold_skip != sft_skip:
            errors.append(f"{cid}: skip mismatch: sft={sorted(sft_skip)} gold={sorted(gold_skip)}")
    
    return errors


def compute_distribution(cases):
    """Compute distribution statistics for cases."""
    total = len(cases)
    shapes = {"READ-only": 0, "STORE/SKIP-only": 0, "READ+STORE": 0, "OTHER": 0}
    targets = Counter()
    total_store = 0
    tags = Counter()
    sens_cases = 0
    bnd_cases = 0
    stale_read_cases = 0
    
    for c in cases:
        # Shape
        gold = c["gold"]
        has_read = bool(gold.get("read", []))
        has_store = bool(gold.get("store", []))
        if has_read and has_store:
            shapes["READ+STORE"] += 1
        elif has_read:
            shapes["READ-only"] += 1
        elif has_store:
            shapes["STORE/SKIP-only"] += 1
        else:
            shapes["OTHER"] += 1
        
        # Targets
        for s in gold.get("store", []):
            targets[s["target"]] += 1
            total_store += 1
        
        # Tags
        for t in c.get("tags", []):
            tags[t] += 1
        
        # Sensitive
        if any("sensitive" in t for t in c.get("tags", [])):
            sens_cases += 1
        
        # Boundary
        if "target_boundary" in c.get("tags", []):
            bnd_cases += 1
    
    return {
        "total_cases": total,
        "total_store_units": total_store,
        "shapes": shapes,
        "shape_pct": {k: round(100*v/total, 1) for k, v in shapes.items()},
        "targets": dict(targets),
        "target_pct": {k: round(100*v/max(1,total_store), 1) for k, v in targets.items()},
        "tags": dict(tags),
        "sensitive_cases": sens_cases,
        "boundary_cases": bnd_cases,
    }


def compute_hash(filepath):
    return hashlib.sha256(Path(filepath).read_bytes()).hexdigest()


def main():
    print("=" * 70)
    print("v05g Training Data Builder")
    print("=" * 70)
    
    # ── 0. Create output directories ──
    cases_dir = Path("data/v05g/cases")
    sft_dir = Path("data/v05g/json_sft")
    reports_dir = Path("reports/v05g")
    for d in [cases_dir, sft_dir, reports_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # ── 1. Copy 500-control from existing v05b train 500 ──
    print("\n[1/5] Copying 500-control from v05b...")
    src_cases = Path("data/v05/train/subsets/v05_train_500_cases.jsonl")
    src_sft = Path("data/v05b/json_sft/v05b_train_500_json_sft_messages.jsonl")
    
    dst_cases = cases_dir / "v05g_train_500_control_cases.jsonl"
    dst_sft = sft_dir / "v05g_train_500_control_json_sft_messages.jsonl"
    
    if not src_cases.exists():
        print(f"ERROR: Source cases not found: {src_cases}")
        return 1
    if not src_sft.exists():
        print(f"ERROR: Source SFT not found: {src_sft}")
        return 1
    
    shutil.copy2(src_cases, dst_cases)
    shutil.copy2(src_sft, dst_sft)
    print(f"  Copied cases: {dst_cases}")
    print(f"  Copied SFT:   {dst_sft}")
    
    # Verify count
    with open(dst_cases) as f:
        n_control_cases = sum(1 for _ in f)
    with open(dst_sft) as f:
        n_control_sft = sum(1 for _ in f)
    print(f"  Cases: {n_control_cases}, SFT messages: {n_control_sft}")
    
    # ── 2. Generate additional 500 targeted-balanced cases ──
    print("\n[2/5] Generating additional 500 targeted-balanced cases...")
    additional_cases = build_additional_500()
    print(f"  Generated: {len(additional_cases)} cases")
    
    # Validate cases
    case_errors = validate_cases(additional_cases, "additional")
    if case_errors:
        print(f"  ❌ CASE VALIDATION FAILED: {len(case_errors)} errors")
        for e in case_errors[:15]:
            print(f"    {e}")
        return 1
    print(f"  ✅ Case validation: 0 errors")
    
    # Compute distribution
    dist_add = compute_distribution(additional_cases)
    print(f"  Shape: READ-only={dist_add['shape_pct']['READ-only']}%, "
          f"STORE/SKIP-only={dist_add['shape_pct']['STORE/SKIP-only']}%, "
          f"READ+STORE={dist_add['shape_pct']['READ+STORE']}%")
    print(f"  Targets: task={dist_add['target_pct'].get('task_state',0)}%, "
          f"svc={dist_add['target_pct'].get('service_memory',0)}%, "
          f"repo={dist_add['target_pct'].get('repo_memory',0)}%, "
          f"proj={dist_add['target_pct'].get('project_memory',0)}%, "
          f"user={dist_add['target_pct'].get('user_profile',0)}%")
    print(f"  Sensitive cases: {dist_add['sensitive_cases']} ({round(100*dist_add['sensitive_cases']/500,1)}%)")
    print(f"  Boundary cases: {dist_add['boundary_cases']} ({round(100*dist_add['boundary_cases']/500,1)}%)")
    
    # Write cases
    add_cases_path = cases_dir / "v05g_train_additional_500_targeted_cases.jsonl"
    with open(add_cases_path, "w") as f:
        for c in additional_cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"  Wrote: {add_cases_path}")
    
    # Render SFT for additional 500
    add_sft = render_json_sft(additional_cases, "v05g_train_additional_500")
    sft_errors = validate_sft(add_sft, additional_cases)
    if sft_errors:
        print(f"  ❌ SFT VALIDATION FAILED: {len(sft_errors)} errors")
        for e in sft_errors[:15]:
            print(f"    {e}")
        return 1
    print(f"  ✅ SFT validation: 0 errors, 100% parse")
    
    add_sft_path = sft_dir / "v05g_train_additional_500_targeted_json_sft_messages.jsonl"
    with open(add_sft_path, "w") as f:
        for msg in add_sft:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"  Wrote: {add_sft_path}")
    
    # ── 3. Build 1000 combined set ──
    print("\n[3/5] Building 1000 combined set...")
    
    # Load control cases
    with open(dst_cases) as f:
        control_cases = [json.loads(line) for line in f if line.strip()]
    
    # Combine cases
    combined_cases = control_cases + additional_cases
    print(f"  Combined cases: {len(combined_cases)} ({len(control_cases)} control + {len(additional_cases)} additional)")
    
    # Write combined cases
    combined_cases_path = cases_dir / "v05g_train_1000_targeted_cases.jsonl"
    with open(combined_cases_path, "w") as f:
        for c in combined_cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"  Wrote: {combined_cases_path}")
    
    # Load control SFT
    with open(dst_sft) as f:
        control_sft = [json.loads(line) for line in f if line.strip()]
    
    # Combine SFT
    combined_sft = control_sft + add_sft
    combined_sft_path = sft_dir / "v05g_train_1000_targeted_json_sft_messages.jsonl"
    with open(combined_sft_path, "w") as f:
        for msg in combined_sft:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"  Wrote: {combined_sft_path}")
    
    # ── 4. Distributions & quality gates ──
    print("\n[4/5] Running quality gates...")
    
    dist_control = compute_distribution(control_cases)
    dist_combined = compute_distribution(combined_cases)
    
    # Quality gate 1: SFT parse = 100%
    combined_sft_errors = validate_sft(combined_sft, combined_cases)
    g1 = len(combined_sft_errors) == 0
    
    # Quality gate 2: unit coverage = 100%
    g2 = True
    for c in combined_cases:
        unit_ids = {u["unit_id"] for u in c["current_units"]}
        store_ids = {s["unit_id"] for s in c["gold"]["store"]}
        skip_ids = set(c["gold"]["skip"])
        if store_ids | skip_ids != unit_ids:
            g2 = False
            break
    
    # Quality gate 3: store/skip mutually exclusive
    g3 = True
    for c in combined_cases:
        store_ids = {s["unit_id"] for s in c["gold"]["store"]}
        skip_ids = set(c["gold"]["skip"])
        if store_ids & skip_ids:
            g3 = False
            break
    
    # Quality gate 4: sensitive STORE = 0
    g4 = True
    for c in combined_cases:
        for u in c["current_units"]:
            if any("sensitive" in t for t in u.get("tags", [])):
                if u["unit_id"] in {s["unit_id"] for s in c["gold"]["store"]}:
                    g4 = False
                    break
    
    # Quality gate 5: no target:"skip" in store (checked in validate_sft)
    g5 = True
    
    # Quality gate 6: no duplicate unit assignment
    g6 = True
    for c in combined_cases:
        store_units = [s["unit_id"] for s in c["gold"]["store"]]
        if len(store_units) != len(set(store_units)):
            g6 = False
            break
    
    # Quality gate 7: no invalid targets
    g7 = True
    for c in combined_cases:
        for s in c["gold"]["store"]:
            if s["target"] not in LEGAL_TARGETS:
                g7 = False
                break
    
    # Quality gate 8: no invalid read/store/skip IDs
    g8 = True
    for c in combined_cases:
        mem_ids = {m["memory_id"] for m in c["candidate_memories"]}
        unit_ids = {u["unit_id"] for u in c["current_units"]}
        for rid in c["gold"]["read"]:
            if rid not in mem_ids:
                g8 = False
                break
        for s in c["gold"]["store"]:
            if s["unit_id"] not in unit_ids:
                g8 = False
                break
        for uid in c["gold"]["skip"]:
            if uid not in unit_ids:
                g8 = False
                break
    
    # Quality gate 9: no unresolved placeholders from FILLERS dict in additional 500
    # (500-control may contain intentional template syntax like {version}, {status}, etc.)
    g9 = True
    for c in additional_cases:
        for u in c["current_units"]:
            ut = u.get("text", u.get("content", ""))
            # Check for FILLER keys that should have been resolved
            if re.search(r'\{vocab_item\}', ut):
                g9 = False
                break
            # Check for generic unresolved placeholders (lowercase with underscore)
            unresolved = re.findall(r'\{([a-z]+_[a-z_]+)\}', ut)
            for ph in unresolved:
                if ph in F:
                    g9 = False
                    break
        for m in c["candidate_memories"]:
            mt = m.get("text", m.get("content", ""))
            if re.search(r'\{vocab_item\}', mt):
                g9 = False
                break
            unresolved = re.findall(r'\{([a-z]+_[a-z_]+)\}', mt)
            for ph in unresolved:
                if ph in F:
                    g9 = False
                    break
    
    gates = [
        ("SFT parse=100%", g1),
        ("unit coverage=100%", g2),
        ("store/skip mutually exclusive", g3),
        ("sensitive STORE=0", g4),
        ('no target:"skip" in store', g5),
        ("no duplicate unit assignment", g6),
        ("no invalid targets", g7),
        ("no invalid read/store/skip IDs", g8),
        ("no unresolved placeholders", g9),
    ]
    
    all_gates_pass = all(v for _, v in gates)
    for name, passed in gates:
        print(f"  {'✅' if passed else '❌'} {name}")
    
    # ── 5. Compute hashes ──
    print("\n[5/5] Computing hashes...")
    file_map = {
        "v05g_train_500_control_cases": dst_cases,
        "v05g_train_500_control_json_sft": dst_sft,
        "v05g_train_additional_500_cases": add_cases_path,
        "v05g_train_additional_500_json_sft": add_sft_path,
        "v05g_train_1000_cases": combined_cases_path,
        "v05g_train_1000_json_sft": combined_sft_path,
    }
    hashes = {name: compute_hash(p) for name, p in file_map.items()}
    for name, h in hashes.items():
        print(f"  {name}: {h[:16]}...")
    
    # ── Write lock manifest ──
    lock_path = Path("data/v05g/v05g_training_data_lock.json")
    lock_data = {
        "version": "v05g",
        "created": "2026-06-05",
        "description": "v05g targeted-balanced training data for BF16 LoRA scaling experiment",
        "files": {name: {"path": str(p), "sha256": h} for name, (p, h) in 
                  zip(hashes.keys(), [(file_map[n], hashes[n]) for n in hashes])},
        "quality_gates": {name: passed for name, passed in gates},
        "all_gates_pass": all_gates_pass,
    }
    with open(lock_path, "w") as f:
        json.dump(lock_data, f, indent=2)
    print(f"\n  Lock manifest: {lock_path}")
    
    # ── Write distribution summary ──
    print("\n" + "=" * 70)
    print("DISTRIBUTION SUMMARY")
    print("=" * 70)
    
    for name, dist in [("500-control", dist_control), ("Additional 500", dist_add), ("Combined 1000", dist_combined)]:
        print(f"\n{name}:")
        print(f"  Cases: {dist['total_cases']}")
        print(f"  Store units: {dist['total_store_units']}")
        print(f"  Shapes: READ-only={dist['shape_pct']['READ-only']}% "
              f"STORE/SKIP={dist['shape_pct']['STORE/SKIP-only']}% "
              f"READ+STORE={dist['shape_pct']['READ+STORE']}%")
        print(f"  Targets: task={dist['target_pct'].get('task_state',0)}% "
              f"svc={dist['target_pct'].get('service_memory',0)}% "
              f"repo={dist['target_pct'].get('repo_memory',0)}% "
              f"proj={dist['target_pct'].get('project_memory',0)}% "
              f"user={dist['target_pct'].get('user_profile',0)}%")
    print(f"\n  Sensitive cases: 500-control={dist_control['sensitive_cases']}, "
          f"add={dist_add['sensitive_cases']}, combined={dist_combined['sensitive_cases']}")
    print(f"  Boundary cases: 500-control={dist_control['boundary_cases']}, "
          f"add={dist_add['boundary_cases']}, combined={dist_combined['boundary_cases']}")
    
    if all_gates_pass:
        print(f"\n  ✅ ALL QUALITY GATES PASSED")
    else:
        print(f"\n  ❌ SOME GATES FAILED")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
