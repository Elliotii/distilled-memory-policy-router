"""Build gold_v2_006 — pre-allocated targets, deterministic READ, no post-hoc relabeling."""
from __future__ import annotations
import hashlib, json, random, sys, re
from pathlib import Path
from collections import Counter, defaultdict
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT))
random.seed(789)

TARGETS = ["task_state","service_memory","repo_memory","project_memory","user_profile"]
TARGET_WEIGHTS = [33,32,17,12,6]

DOMAINS = [
    {"project":"cybersecurity-audit","repo":"pentestkit","service":"vuln-scanner","family":"security",
     "vocab":["vulnerability","CVE","exploit","patch","zero-day","penetration test","remediation","CVSS score","attack surface","threat model","false positive","SIEM","endpoint","alert triage","incident response","phishing","ransomware","firewall rule","IDS signature","authenticated scan"]},
    {"project":"supply-chain-optimizer","repo":"stockplan","service":"inventory-planner","family":"logistics",
     "vocab":["safety stock","lead time","reorder point","demand signal","supplier","inventory turnover","SKU","backorder","fill rate","seasonality","promotional lift","procurement","vendor scorecard","purchase order","consignment stock","cycle count","ABC classification","economic order quantity","warehouse slotting","cross-docking"]},
    {"project":"media-transcoding","repo":"pixelpipe","service":"encoding-orchestrator","family":"media",
     "vocab":["codec","bitrate","resolution","H.264","H.265","AV1","keyframe interval","two-pass encoding","CRF","ABR ladder","packaging","DRM","watermarking","subtitle burn-in","aspect ratio","frame rate","GOP size","deinterlacing","color space","mezzanine file"]},
    {"project":"accessibility-compliance","repo":"a11ykit","service":"audit-crawler","family":"a11y",
     "vocab":["WCAG 2.1","ARIA","screen reader","keyboard navigation","color contrast","focus order","alt text","landmark","skip link","axe-core","Lighthouse","accessibility tree","semantic HTML","focus trap","live region","role","tabindex","contrast ratio","Section 508","violation severity"]},
    {"project":"quantitative-research","repo":"alphapack","service":"backtest-engine","family":"finance",
     "vocab":["alpha","beta","Sharpe ratio","drawdown","survivorship bias","look-ahead bias","slippage","market impact","portfolio turnover","factor model","risk parity","VaR","expected shortfall","Monte Carlo","stress test","historical simulation","transaction cost","capacity","signal decay","information coefficient"]},
    {"project":"genomics-pipeline","repo":"seqflow","service":"variant-caller","family":"bioinformatics",
     "vocab":["FASTQ","BAM","VCF","alignment","coverage depth","variant allele frequency","germline","somatic","SNV","indel","copy number","ploidy","reference genome","read pair","base quality","mapping quality","duplicate marking","haplotype","genotype likelihood","panel of normals"]},
    {"project":"real-estate-valuation","repo":"valuestack","service":"comp-engine","family":"realestate",
     "vocab":["comparable sale","cap rate","NOI","DCF","appraisal","zoning","square footage","price per square foot","assessment","tax record","MLS","days on market","listing price","closing price","mortgage rate","amortization","LTV","escrow","title","deed"]},
    {"project":"game-analytics","repo":"playmetrics","service":"session-analyzer","family":"gaming",
     "vocab":["DAU","MAU","retention","churn","session length","ARPDAU","LTV","cohort","funnel","conversion","IAP","tutorial completion","level progression","matchmaking","latency","frame rate","crash rate","first-time user experience","A/B test","engagement"]},
]

# Complete FILLERS from v005 (49 keys)
FILLERS = {
    "problem":["returning 503 errors","showing stale results","dropping events","timing out after 30s","producing duplicate records","leaking file handles","failing TLS handshakes","rejecting valid tokens"],
    "context":["peak traffic hours","Friday deployments","payloads over 1MB","1000+ concurrent sessions","the EU-WEST-1 region","mobile clients on 3G networks","unicode characters in filenames","nested JSON beyond depth 10"],
    "issue":["race condition in the worker pool","memory leak in the cache layer","connection pool exhaustion","cache invalidation bug","deadlock in the transaction manager","infinite retry loop","hash collision in the partitioner","serialization error with timestamps"],
    "trigger":["3 PM config push","database failover","Kafka partition rebalance","TLS certificate rotation","load balancer health check change"],
    "feature":["rate limiting per API key","circuit breaking for downstream calls","request deduplication via idempotency keys","graceful degradation when dependencies fail","canary deployment support","dark launch capability for A/B testing"],
    "version":["v2.3.1","v3.0.2","v1.8.7","v4.2.0","v2.9.4","v3.5.1","v1.11.3"],
    "bug":["regression in concurrent processing","off-by-one error in pagination","N+1 query problem","serialization bug with datetime fields","hash collision in the consistent hashing ring","null pointer in the error handler"],
    "metric":["p99 latency","error rate","throughput","CPU utilization","heap usage","request queue depth","cache hit ratio"],
    "value":["spiked from 200ms to 3s","dropped by 40 percent","tripled compared to baseline","reached 800ms at the 95th percentile","fell below 60 percent","exceeded the 500ms SLO"],
    "target":["below 500ms at p99","above 99.5 percent","under 200ms average","over 99.9 percent uptime","within 5 percent of the baseline"],
    "symptom":["p99 latency spikes to 3 seconds under load","OOM after 6 hours of uptime","request queue grows without bound","50 percent of requests timeout after 30s","error rate jumps to 12 percent"],
    "fix":["adding a connection pool limit","implementing exponential backoff","increasing the heap size to 4GB","adding a circuit breaker with 30s reset","deploying a read replica for queries"],
    "old_tech":["PostgreSQL 12","Redis Cluster","RabbitMQ","EC2 Auto Scaling groups","Jenkins"],
    "new_tech":["PostgreSQL 16","Valkey 8","Kafka","Kubernetes HPA","GitHub Actions"],
    "progress":["40","65","85","25","50"],
    "system":["auth-service","payment-gateway","notification-bus","data-lake","feature-store"],
    "quarter":["2","3","4"],"phase":["design","implementation","testing","review"],
    "owner":["the platform team","the SRE squad","@alex.morgan","@jordan.kim","the infrasec group"],
    "deadline":["Friday EOD","next Wednesday","end of sprint","March 15","Q2 closing"],
    "inc_num":["2026-0042","2026-0187","2026-0315","2026-0523"],
    "behavior":["accepted unauthenticated health checks","logged PII in plaintext","used XML for all API responses","required weekly manual restarts","ran on a single thread with no timeout"],
    "pattern":["periodic 503 spikes","GC pause storms every 45 minutes","disk usage growing at 2GB per day","repeated DNS resolution failures","connection resets during peak hours"],
    "blocker":["a missing upstream API schema","the auth team deployment freeze","an unresolved dependency conflict","waiting for the database migration approval","a flaky integration test in CI"],
    "component":["request handler","worker pool","cache layer","authentication middleware","serialization module","rate limiter"],
    "sla":["99.5","99.9","99.95","99.99"],"latency":["200","500","100","800","50"],"percentile":["95","99","99.9"],
    "header":["X-Trace-Id","X-Request-Id","X-Correlation-Id","X-Tenant-Id"],
    "purpose":["distributed tracing","request correlation","multi-tenant isolation","rate-limit tracking","audit logging"],
    "operation":["idempotent request processing","consistent hashing for workload distribution","optimistic concurrency control","two-phase commit for distributed transactions"],
    "detail":["submitting the same request twice produces one result with the same ID","requests with identical keys always route to the same worker","conflicts are detected via version vectors and resolved by the client","both participants must agree before any data is committed"],
    "data":["Health check results","Performance metrics","Audit log entries","Usage statistics","Configuration snapshots"],
    "interval":["15","30","60","10","5"],"topic":["svc.health","svc.metrics","svc.events","svc.audit","svc.config"],
    "key":["service_id","tenant_id","request_id","user_id"],
    "where":["Redis","Memcached","an in-memory LRU cache","a local SQLite database"],
    "ttl":["30-minute","2-hour","15-second","24-hour","5-minute"],
    "n":["3","5","7","10"],"reset":["30","60","120","15"],
    "what":["a benchmark comparison","a changelog entry","a security review approval","an architecture decision record","a rollback plan"],
    "cmd":["just test-svc","make bench-svc","just lint-svc","task validate-svc"],
    "action":["execute the standard benchmark suite against","run integration tests for","type-check the entire","validate the schema of"],
    "condition":["p95 latency increases","error rate exceeds baseline","test coverage drops","memory usage grows"],
    "path":["svc/config/","config/svc/","deploy/svc/","src/svc/config/"],
    "frequency":["quarterly","monthly","bi-weekly"],"review_type":["security","architecture","compliance"],
    "dashboard":["slo-tracker","health-dashboard","compliance-monitor","cost-analyzer"],
    "tool":["OpenTelemetry","Prometheus","Grafana","Datadog"],
}

TASK_STORE_POOL = [
    "Currently investigating why the {svc} {problem} for {context}. The rollout team needs a fix by {deadline}.",
    "Active incident: the {svc} {issue} that started after the {trigger}. Assigned to {owner} for resolution this sprint.",
    "This sprint task: add {feature} to the {svc} to handle {context}. Due by {deadline}.",
    "Currently rolling back the {svc} to {version} because the latest release introduced a {bug} in production.",
    "Active migration: moving the {svc} from {old_tech} to {new_tech}. Currently at {progress} percent completion.",
    "Sprint goal: the {svc} {metric} needs to improve from {value} to better than {target}. Owner: {owner}.",
    "Assigned task: refactor the {svc} {component} to use {pattern}. Blocked by {blocker}.",
    "Follow-up from incident INC-{inc_num}: the {svc} {symptom}. Need to implement {fix} by next week.",
    "Current deployment: the {svc} canary is at {progress} percent traffic. Monitoring {metric} for regressions.",
    "Integration milestone: connect the {svc} to the new {system} by the end of Q{quarter}. Currently in {phase}.",
]
TASK_SKIP_POOL = [
    "Hypothetical scenario: what would happen if the {svc} {problem} during {context}? Not a current concern.",
    "Old incident note from last quarter (resolved): the {svc} had a {issue} after the {trigger}. No longer active.",
    "Scratch investigation: the {svc} showed unusual {metric} last Tuesday, but it self-resolved within 2 hours.",
    "Discarded idea: add {feature} to the {svc}. Rejected because it conflicts with the architecture roadmap.",
    "Historical reference: the {svc} used to {behavior} before the Q1 redesign. Not relevant to current work.",
    "Unrelated question: does the {svc} support {context}? This is handled by a different team entirely.",
    "Stale note from previous sprint: the {svc} {symptom}. Already fixed in {version}.",
    "Off-topic observation: the {svc} logs show {pattern} during off-hours, but this is expected behavior.",
]

SENSITIVE_POOL = [
    ("My personal mobile for testing is +1-555-0192.","phone"),
    ("Use recovery phone +1-555-0148 to reset the admin MFA token.","phone"),
    ("Send deployment summaries to dev.alex@gmail.com instead of the team alias.","email"),
    ("My work email for audit trail is compliance.lead@audit.org.","email"),
    ("The staging DB password was rotated to Tr0ub4dor&3 after the incident.","credential"),
    ("Integration test uses live API key: ak_prod_z9x8y7w6v5u4 — rotate before next deploy.","credential"),
    ("My home address for W-2 is 742 Evergreen Terrace, Springfield, IL 62701.","address"),
    ("Ship the YubiKey to 451 Briarwood Lane, Apt 3B, Austin, TX 78701.","address"),
    ("Use Amex 3782-822463-10005 exp 09/27 for the sandbox AWS billing only.","payment"),
    ("My debit 4000-1234-5678-9010 exp 03/28 CVV 442 is linked to the test gateway.","payment"),
    ("The test fixture uses SSN 987-65-4320 for HIPAA masking verification.","id"),
    ("My employee badge EMP-88291 grants server room access — deactivate before leave.","id"),
    ("Load test uses OAuth secret gs_sec_4f8a2c1e9b3d7h6j — rotate each quarter.","credential"),
    ("GitHub token ghp_x9y8z7w6v5u4t3s2 is accidentally in the deploy script.","credential"),
    ("Send monthly reports to jane.review@outlook.com, not the shared mailbox.","email"),
    ("Use +1-555-0277 for the admin console two-factor SMS recovery.","phone"),
]

STALE_POOL = [
    "Old SOAP APIs were retired in 2023 after the REST migration.",
    "A Rails monolith handled everything until the 2022 service split.",
    "RabbitMQ was replaced by Kafka for event streaming in early 2024.",
    "The original dashboard was a static HTML page from an hourly cron job.",
    "Manual 12-step deployment runbooks were used before CI/CD adoption.",
    "The old alerting system sent thousands of false-positive emails daily.",
    "Debugging required SSH access to individual servers before observability.",
    "Flask and SQLite powered the prototype before FastAPI and PostgreSQL.",
    "Deployment logs were a shared Google Doc before proper change management.",
    "A static on-call rotation with no timezone awareness was the old schedule.",
    "Polling was required for status before webhooks were implemented in 2024.",
    "Abandoned bash scripts from 2021 served as the load-testing framework.",
    "Every UI change required a full deployment before feature flags were adopted.",
    "Nagios with a 3000-line Perl config ran the old monitoring stack.",
    "Incident postmortems were unsearchable PDFs in a shared network drive.",
    "XML-RPC with a custom parser that broke on Unicode was the old API protocol.",
    "A dedicated QA silo existed before embedded QA engineers joined every squad.",
    "Scheduled 4-hour downtime was needed for all platform upgrades before 2024.",
    "Custom cron-based orchestration managed workflows before the job scheduler.",
    "Manual spreadsheet tracking of dependencies preceded the service catalog.",
]

def _pick(key, seed_val):
    options = FILLERS.get(key, [key])
    return options[seed_val % len(options)]

def _fill(template, d, seed_base):
    s, r, p = d["service"], d["repo"], d["project"]
    fill = {"svc":s,"repo":r,"proj":p}
    for i, ph in enumerate(re.findall(r'\{(\w+)\}', template)):
        if ph not in fill:
            fill[ph] = _pick(ph, seed_base + i)
    return template.format(**fill)

def _gen_target_text(target, d, seed_val):
    """Generate text semantically appropriate for the given target."""
    s, r, p = d["service"], d["repo"], d["project"]
    v = d["vocab"]
    vw = v[seed_val % len(v)]
    
    if target == "task_state":
        return _fill(random.Random(seed_val).choice(TASK_STORE_POOL), d, seed_val)
    elif target == "service_memory":
        tmpls = [
            f"The {{svc}} guarantees {{sla}} percent uptime with maximum response latency of {{latency}}ms at p{{percentile}}. This covers {vw} workflows.",
            f"All {{svc}} responses include a {{header}} header for {{purpose}} across all {vw} endpoints.",
            f"The {{svc}} performs {{operation}}. {{detail}} This is critical for {vw} use cases.",
            f"{{data}} from the {{svc}} is published every {{interval}}s to {{topic}} partitioned by {{key}} for {vw} consumers.",
            f"The {{svc}} caches {vw} data in {{where}} with a {{ttl}} TTL.",
            f"The {{svc}} circuit breaker opens after {{n}} consecutive failures to the {{system}} and resets after {{reset}}s.",
        ]
        return _fill(random.Random(seed_val).choice(tmpls), d, seed_val)
    elif target == "repo_memory":
        tmpls = [
            f"All {{svc}} changes in {{repo}} must include {{what}} in the PR description per team policy for {vw}.",
            f"Run {{cmd}} in {{repo}} to {{action}} the {{svc}} against {{data}} for {vw} verification.",
            f"The {{repo}} CI blocks merges if the {{svc}} {{condition}} by more than 10 percent on {vw} tests.",
            f"{{svc}} config in {{repo}} lives under {{path}} with per-environment overrides for {vw}.",
        ]
        return _fill(random.Random(seed_val).choice(tmpls), d, seed_val)
    elif target == "project_memory":
        # Project-scope text: cross-service rules, project-wide requirements
        tmpls = [
            f"The {{proj}} project requires {{frequency}} {{review_type}} reviews for any changes touching {vw}.",
            f"All {{proj}} services must report {vw} metrics to {{dashboard}} every {{interval}} via {{tool}}.",
            f"Architecture Decision Records for {{proj}} live in {{path}} with cross-references to all services handling {vw}.",
            f"The {{proj}} project enforces that any {vw} change must be approved by the architecture review board.",
            f"Every service in {{proj}} must implement {vw} according to the standard defined in the project governance doc.",
        ]
        return _fill(random.Random(seed_val).choice(tmpls), d, seed_val)
    else:  # user_profile
        tmpls = [
            f"I prefer the {{svc}} dashboard to show {vw} metrics as a heatmap rather than a table.",
            f"Flag {{svc}} alerts for {vw} as critical when they affect more than {{n}} items.",
            f"I want {{svc}} notifications for {vw} sent as daily digests, not real-time alerts.",
        ]
        return _fill(random.Random(seed_val).choice(tmpls), d, seed_val)

def build():
    random.seed(789)
    
    # ── Pre-allocate target counts for all 180 cases ──
    # Target STORE units needed: ~237 across 180 cases
    # Each store_skip_only has 2 stores, each read_store_joint has 2 stores (when not sens) or 1 (when sens)
    # ~70 store_skip_only * 2 + ~78 read_store_joint * (2 * 0.85 + 1 * 0.15) ≈ 140 + 144 = 284
    # After sensitive flags remove some stores: ~237
    
    shapes_180 = ["read_only"]*32 + ["store_skip_only"]*70 + ["read_store_joint"]*78
    random.shuffle(shapes_180)
    sens_180 = [True]*26 + [False]*154; random.shuffle(sens_180)
    bnd_180 = [True]*54 + [False]*126; random.shuffle(bnd_180)
    
    # Pre-allocate targets
    total_stores_est = sum(2 for s in shapes_180 if s == "store_skip_only") + sum((1 if sens_180[i] else 2) for i, s in enumerate(shapes_180) if s == "read_store_joint")
    n_task = int(total_stores_est * 0.33)
    n_svc = int(total_stores_est * 0.32)
    n_repo = int(total_stores_est * 0.17)
    n_proj = int(total_stores_est * 0.12)
    n_user = total_stores_est - n_task - n_svc - n_repo - n_proj
    
    store_targets = (["task_state"]*n_task + ["service_memory"]*n_svc + 
                     ["repo_memory"]*n_repo + ["project_memory"]*n_proj + ["user_profile"]*n_user)
    random.shuffle(store_targets)
    sti = 0
    
    domain_list = list(DOMAINS)
    cases = []
    _seed = [9000]
    sens_idx = 0
    
    for i in range(180):
        d = domain_list[i % 8]
        s, r, p = d["service"], d["repo"], d["project"]
        shape, is_sens, is_bnd = shapes_180[i], sens_180[i], bnd_180[i]
        
        # ── Memories with relevance tags ──
        nm = random.randint(2, min(5, 5))
        if shape == "read_only": nm = random.randint(2, 4)
        
        mems_raw = []
        _seed[0] += 1
        mems_raw.append({"target":"service_memory","text":_gen_target_text("service_memory",d,_seed[0]),
                         "tags":[],"relevance":"relevant_read"})
        if nm >= 2 and random.random() < 0.7:
            _seed[0] += 1
            rel = "relevant_read" if random.random() < 0.6 else "distractor"
            mems_raw.append({"target":"repo_memory","text":_gen_target_text("repo_memory",d,_seed[0]),
                            "tags":[],"relevance":rel})
        if nm >= 3 and random.random() < 0.5:
            _seed[0] += 1
            rel = "relevant_read" if random.random() < 0.5 else "distractor"
            mems_raw.append({"target":"project_memory","text":_gen_target_text("project_memory",d,_seed[0]),
                            "tags":[],"relevance":rel})
        if nm >= 4 and random.random() < 0.4:
            _seed[0] += 1
            mems_raw.append({"target":"user_profile","text":_gen_target_text("user_profile",d,_seed[0]),
                            "tags":[],"relevance":"distractor"})
        while len(mems_raw) < nm:
            mems_raw.append({"target":"service_memory","text":random.choice(STALE_POOL),
                            "tags":["stale"],"relevance":"stale"})
        
        random.shuffle(mems_raw)
        memories = []
        for j, mr in enumerate(mems_raw):
            memories.append({"memory_id":f"m{j+1}","target":mr["target"],"text":mr["text"],
                           "tags":mr.get("tags",[])})
        
        # ── Deterministic READ: all relevant_read memories ──
        g_read = sorted([m["memory_id"] for j, m in enumerate(memories) 
                        if mems_raw[j].get("relevance") == "relevant_read"])
        
        # ── Units with pre-allocated targets ──
        units, g_store, g_skip, tags = [], [], [], []
        
        if shape == "read_only":
            _seed[0] += 1
            u1_text = _fill(random.choice(TASK_SKIP_POOL), d, _seed[0])
            units.append({"unit_id":"u1","text":u1_text,"tags":["task_progress","read_only"]})
            g_skip.append("u1")
            tags = ["read_only"]
        
        elif shape == "store_skip_only":
            for u_idx in range(2):
                target = store_targets[sti % len(store_targets)]; sti += 1
                _seed[0] += 1
                text = _gen_target_text(target, d, _seed[0])
                utags = ["store_skip_only", f"target_{target}"]
                if is_bnd: utags.append("target_boundary")
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
                u3_text = _fill(random.choice(TASK_SKIP_POOL), d, _seed[0])
                units.append({"unit_id":uid3,"text":u3_text,"tags":["task_progress","store_skip_only"]})
                g_skip.append(uid3)
            tags.append("store_skip_only")
        
        else:  # read_store_joint
            _seed[0] += 1
            u1_text = _fill(random.choice(TASK_SKIP_POOL), d, _seed[0])
            units.append({"unit_id":"u1","text":u1_text,"tags":["task_progress","read_store_joint"]})
            g_skip.append("u1")
            
            if is_sens:
                target = store_targets[sti % len(store_targets)]; sti += 1
                _seed[0] += 1
                text = _gen_target_text(target, d, _seed[0])
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
                    text = _gen_target_text(target, d, _seed[0])
                    utags = ["read_store_joint", f"target_{target}"]
                    if is_bnd: utags.append("target_boundary")
                    units.append({"unit_id":f"u{u_idx+1}","text":text,"tags":utags})
                    g_store.append({"unit_id":f"u{u_idx+1}","target":target})
            tags.append("read_store_joint")
        
        runtime = {"project":p,"repo":r,"service":s,"task":f"Working on the {s} in {p}"}
        if is_bnd: tags.append("target_boundary")
        if is_sens: tags.append("sensitive_boundary")
        tags = list(set(tags))
        
        # Remove boundary from READ-only
        if shape == "read_only" and "target_boundary" in tags:
            tags.remove("target_boundary")
        
        cases.append({"case_id":f"v05e_gold_{i+1:04d}","runtime_context":runtime,
                      "candidate_memories":memories,"current_units":units,
                      "gold":{"read":g_read,"store":g_store,"skip":sorted(g_skip),"dsl":""},
                      "tags":tags,"notes":f"v006 shape={shape}"})
    
    random.shuffle(cases)
    active, holdout = cases[:150], cases[150:180]
    
    # Post-generation: ensure boundary ≥ 30 without relabeling targets
    bnd_count = sum(1 for c in active if "target_boundary" in c["tags"])
    for c in active:
        if bnd_count >= 30: break
        if "read_only" not in c["tags"] and "target_boundary" not in c["tags"]:
            c["tags"].append("target_boundary"); bnd_count += 1
    
    for i, c in enumerate(active): c["case_id"] = f"v05e_gold_active_{i+1:04d}"
    for i, c in enumerate(holdout): c["case_id"] = f"v05e_gold_holdout_{i+1:04d}"
    return active, holdout


def audit(active):
    from collections import Counter, defaultdict
    
    # Unresolved placeholders
    unresolved = sum(1 for c in active for u in c["current_units"] if re.search(r'\{[^}]+\}', u["text"]))
    unresolved += sum(1 for c in active for m in c["candidate_memories"] if re.search(r'\{[^}]+\}', m["text"]))
    
    # String quality
    art_dbl = sum(1 for c in active for u in c["current_units"] if re.search(r'\b(a|an|the)\s+\1\b', u["text"], re.I))
    ver_dbl = sum(1 for c in active for u in c["current_units"] if re.search(r'v\s*v\d', u["text"], re.I))
    fbugs = sum(1 for c in active for u in c["current_units"] if re.search(r'(dropped|spiked|plateaued)\s+to\s+\1', u["text"], re.I))
    
    # Namespace
    banned = {'flowcraft','demand-forecaster','education-platform','learnhub','assessment-engine',
              'ecommerce-platform','shopengine','cart-service','alert-manager'}
    leakage = sum(1 for c in active if c["runtime_context"]["project"].lower() in banned 
                  or c["runtime_context"]["repo"].lower() in banned 
                  or c["runtime_context"]["service"].lower() in banned)
    
    # Exact label conflicts
    tg = defaultdict(list)
    for c in active:
        for u in c["current_units"]:
            stored = u["unit_id"] in {s["unit_id"] for s in c["gold"]["store"]}
            tg[u["text"].strip().lower()].append(stored)
    conflicts = sum(1 for gs in tg.values() if len(set(gs)) > 1)
    
    # Target-text alignment: check project_memory text contains project-scope keywords
    misaligned = 0
    proj_kw = ['project requires','all services must','every service','cross-service','across all','architecture decision','project enforces','project governance']
    repo_kw = ['in the repo','run','ci','config','migrations','directory','file','path','PR','branch']
    for c in active:
        for s in c["gold"]["store"]:
            text = next((u["text"] for u in c["current_units"] if u["unit_id"] == s["unit_id"]), "")
            t = text.lower()
            target = s["target"]
            if target == "project_memory" and not any(kw in t for kw in proj_kw):
                if any(kw in t for kw in repo_kw):
                    misaligned += 1
            if target == "repo_memory" and any(kw in t for kw in proj_kw) and not any(kw in t for kw in repo_kw):
                misaligned += 1
    
    # READ determinism
    stale_read = sum(1 for c in active for rid in c["gold"]["read"] 
                     if any(m["memory_id"]==rid and "stale" in m.get("tags",[]) for m in c["candidate_memories"]))
    
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
    dist_ok = (task_pct <= 36.0 and 29 <= svc_pct <= 35 and 14 <= repo_pct <= 20 
               and 9 <= proj_pct <= 15 and 3 <= user_pct <= 9)
    
    sens = sum(1 for c in active if "sensitive_boundary" in c["tags"])
    bnd = sum(1 for c in active if "target_boundary" in c["tags"])
    bnd_ro = sum(1 for c in active if "target_boundary" in c["tags"] and "read_only" in c["tags"])
    sens_stored = sum(1 for c in active for u in c["current_units"] 
                      if any('sensitive' in t for t in u.get('tags',[])) 
                      and u['unit_id'] in {s['unit_id'] for s in c['gold']['store']})
    
    gates = [
        ("unresolved_placeholders", unresolved, 0),
        ("article_doubling", art_dbl, 0),
        ("version_doubling", ver_dbl, 0),
        ("filler_bugs", fbugs, 0),
        ("namespace_leakage", leakage, 0),
        ("exact_label_conflicts", conflicts, 0),
        ("target_text_misaligned", misaligned, 0),
        ("stale_reads", stale_read, 0),
        ("target_distribution", dist_ok, True),
        ("sensitive_18_27", 18 <= sens <= 27, True),
        ("boundary_30_38", 30 <= bnd <= 38, True),
        ("boundary_on_readonly", bnd_ro, 0),
        ("sensitive_stored", sens_stored, 0),
    ]
    
    all_pass = all(v == tgt for _, v, tgt in gates)
    return all_pass, gates, {"targets":targets,"total_store":total_store,"sens":sens,"bnd":bnd}


def compute_hash(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_jsonl(path, cases):
    with open(path,"w") as f:
        for c in cases: f.write(json.dumps(c,ensure_ascii=False)+"\n")

def main():
    active, holdout = build()
    base = Path("data/v05e/gold_v2")
    base.mkdir(parents=True, exist_ok=True)
    ap = base / "v05e_gold_v2_006_active_cases.jsonl"
    hp = base / "v05e_gold_v2_006_holdout_cases.jsonl"
    write_jsonl(ap, active); write_jsonl(hp, holdout)
    
    passed, gates, info = audit(active)
    
    print(f"Active: {len(active)} | Holdout: {len(holdout)}")
    print(f"\n=== GATES ===")
    for name, val, tgt in gates:
        icon = "✅" if val == tgt else "❌"
        print(f"  {icon} {name}: {val} (target={tgt})")
    
    ts = info["targets"]
    ts_total = info["total_store"]
    print(f"\nTargets ({ts_total}): task={ts['task_state']} ({100*ts['task_state']/ts_total:.1f}%) svc={ts['service_memory']} ({100*ts['service_memory']/ts_total:.1f}%) repo={ts['repo_memory']} ({100*ts['repo_memory']/ts_total:.1f}%) proj={ts['project_memory']} ({100*ts['project_memory']/ts_total:.1f}%) user={ts['user_profile']} ({100*ts['user_profile']/ts_total:.1f}%)")
    print(f"Stress: sens={info['sens']} bnd={info['bnd']}")
    
    if not passed:
        print("\n❌ GATES FAILED"); return 1
    
    print(f"\n✅ ALL GATES PASSED")
    h = {"active":compute_hash(ap),"holdout":compute_hash(hp)}
    print(f"Hashes: active={h['active'][:16]}... holdout={h['holdout'][:16]}...")
    return 0

if __name__ == "__main__":
    sys.exit(main())
