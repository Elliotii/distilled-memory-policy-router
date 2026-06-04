"""Build gold_v2_003 v2 — robust STORE allocation, per-case unique unit texts.
Strategy: generate unique unit texts per case using domain vocab + varied phrasings.
"""
from __future__ import annotations
import hashlib, json, random, sys, re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
random.seed(77)

TARGETS = ["task_state","service_memory","repo_memory","project_memory","user_profile"]

# 8 domains with domain-specific vocabulary
DOMAINS = [
    {"project":"clinical-trials","repo":"trialops","service":"patient-matcher",
     "vocab":["enrollment","cohort","protocol","amendment","eligibility","adverse event","consent","IRB","arm","placebo","screening","informed consent","endpoint","monitoring","HIPAA","de-identification","pseudonym","inclusion criteria","exclusion","dosing schedule"]},
    {"project":"fraud-detection","repo":"riskwall","service":"transaction-analyzer",
     "vocab":["transaction score","chargeback","risk rule","merchant category","velocity check","ML model","feature vector","false positive","false negative","rules engine","threshold","alert","Suspicious Activity Report","KYC","AML","sanctions screening","device fingerprint","behavioral analytics"]},
    {"project":"smart-building","repo":"buildingos","service":"hvac-controller",
     "vocab":["thermostat","occupancy sensor","airflow","chiller","energy schedule","zone","setpoint","BACnet","AHU","VAV","demand response","peak load","temperature","humidity","CO2 sensor","preventive maintenance","fault detection","commissioning","economizer","damper"]},
    {"project":"observability-platform","repo":"observekit","service":"log-aggregator",
     "vocab":["trace","span","metric","log retention","alert routing","dashboard","SLO","error budget","burn rate","pager","on-call","runbook","incident","postmortem","query","index","sampling","cardinality","label","Prometheus","Grafana","exemplar"]},
    {"project":"document-workflow","repo":"paperless","service":"approval-engine",
     "vocab":["review queue","redaction","approval policy","retention","document","signature","workflow step","escalation","compliance","audit","version","watermark","template","clause","contract","NDA","legal hold","disposition","reviewer","deadline"]},
    {"project":"ml-feature-store","repo":"feastkit","service":"feature-server",
     "vocab":["feature freshness","offline/online parity","embedding","backfill","training set","inference","entity","feature view","point-in-time","TTL","registry","transformation","batch","streaming","materialization","drift detection","feature importance","serving layer"]},
    {"project":"education-platform","repo":"learnhub","service":"assessment-engine",
     "vocab":["course enrollment","grading rubric","roster sync","assessment policy","quiz","submission","plagiarism","proctoring","certificate","learning objective","prerequisite","syllabus","office hours","TA","gradebook","rubric","academic integrity","final exam","retake policy"]},
    {"project":"data-pipeline","repo":"datapipe","service":"ingestion-gateway",
     "vocab":["schema drift","partition","backfill","watermark","lineage","ETL","CDC","batch window","data quality","validation rule","dead letter","retry policy","checkpoint","idempotency","deduplication","late arrival","out-of-order","throughput","lag"]},
]

# ── Unit text generators ──
TASK_PHRASES = [
    "Investigate why {svc} is {problem} for {context}.",
    "Debug the {svc} {issue} that started after the {trigger}.",
    "Add {feature} to the {svc} to support {context}.",
    "Roll back the {svc} to {version} because the latest release introduced a {bug}.",
    "The {svc} {metric} dropped to {value} after the {change} — investigate.",
    "Update the {svc} to handle {context} correctly when {condition}.",
    "Refactor the {svc} {component} to use {pattern} instead of {old_pattern}.",
    "Profile the {svc} {component} — the {bottleneck} is causing {symptom}.",
]

SVC_PHRASES = [
    "The {svc} {guarantees} {sla} uptime with a maximum response latency of {latency}ms at p{percentile}.",
    "All {svc} responses include a `{header}` header for {purpose}.",
    "The {svc} performs {operation} — {detail}.",
    "{data} from the {svc} is published every {interval} seconds to the `{topic}` Kafka topic partitioned by {key}.",
    "The {svc} requires all downstream calls to include {auth} for {reason}.",
    "The {svc} caches {what} in {where} with a {ttl} TTL.",
    "The {svc} circuit-breaker opens after {n} consecutive failures and resets after {reset}s.",
    "Each {svc} instance maintains a local {cache_type} cache of the {size} most recent {what}.",
]

REPO_PHRASES = [
    "All changes to the {repo} repo that touch the {svc} must include {what} in the PR description.",
    "Run `{cmd}` in the {repo} repo to {action} the {svc} with {data}.",
    "The {repo} CI pipeline enforces that no PR is merged if it {condition}.",
    "Configuration for the {svc} lives under `{path}` in {repo}, with separate files for {envs}.",
    "The {repo} repo uses `{runner}` as its task runner; `{cmd}` runs {what} on the {svc} codebase.",
    "{what} for the {svc} in {repo} use {tool} to {action}.",
]

PROJ_PHRASES = [
    "The {proj} project requires that any service handling {what} undergo a {frequency} {review_type} review.",
    "All {proj} microservices must report their {metric} to the centralized `{dashboard}` dashboard every {interval}.",
    "The {proj} project uses {tool} for {purpose} — services must {requirement}.",
    "Architecture Decision Records for {proj} are stored in `{path}` in the main monorepo.",
    "The {proj} project enforces a {target} availability target for all {scope} services.",
    "All {proj} services must support {capability} — if {dependency} fails, fall back to {fallback}.",
]

USER_PHRASES = [
    "I prefer the {svc} dashboard to show a {viz} of {what} rather than {alt}.",
    "Flag any {svc} {what} that {condition} as '{label}' in the dashboard.",
    "I want {svc} {reports} sent as a {frequency} {format} rather than {alt}.",
    "Configure the {svc} alerts so that I only get paged for issues affecting more than {n} {what}.",
    "Sort the {svc} {list} by {field} rather than by {alt_field}.",
    "Show {svc} {metric} in {unit} rather than {alt_unit} for our {context}.",
]

SENSITIVE_POOL = [
    ("My personal mobile for on-call testing is +1-555-0192.","phone"),
    ("Use recovery phone +1-555-0148 to reset the admin console MFA.","phone"),
    ("Send deployment summaries to dev.alex@gmail.com instead of the team alias.","email"),
    ("My work email for audit notifications is compliance.lead@clinical.org.","email"),
    ("The staging DB password was reset to Tr0ub4dor&3 after the security incident.","credential"),
    ("The integration test uses a live API key: ak_prod_z9x8y7w6v5u4 — rotate this before next deploy.","credential"),
    ("My home address for W-2 delivery is 742 Evergreen Terrace, Springfield, IL 62701.","address"),
    ("Ship the hardware token to 451 Briarwood Lane, Apt 3B, Austin, TX 78701.","address"),
    ("Use Amex 3782-822463-10005 exp 09/27 for the sandbox AWS billing.","payment"),
    ("My debit card 4000-1234-5678-9010 exp 03/28 CVV 442 is linked to the test payment gateway.","payment"),
    ("The test record uses SSN 987-65-4320 for HIPAA masking verification.","id"),
    ("My employee badge EMP-88291 grants server room access — deactivate it before leave starts.","id"),
    ("The load-test script uses OAuth secret gs_sec_4f8a2c1e9b3d7h6j — regenerate quarterly.","credential"),
    ("My personal GitHub token ghp_x9y8z7w6v5u4t3s2 is accidentally in the deploy script.","credential"),
    ("Send monthly compliance reports to jane.review@outlook.com instead of the shared mailbox.","email"),
    ("Use +1-555-0277 as the SMS recovery number for the admin console two-factor setup.","phone"),
]

STALE_POOL = [
    "The legacy system used SOAP APIs until retirement in 2023.",
    "A Rails monolith handled everything before the 2022 microservice migration.",
    "RabbitMQ was the event bus before the 2024 Kafka migration.",
    "The original dashboard was a static HTML page from an hourly cron job.",
    "Manual 12-step deployment runbooks were used before CI/CD was adopted.",
    "The old alerting system sent thousands of false-positive emails daily.",
    "Debugging required SSH access to individual production servers before observability tools.",
    "Flask and SQLite powered the prototype before migration to FastAPI and PostgreSQL.",
    "Deployment logs were tracked in a shared Google Doc before proper tooling.",
    "A static weekly on-call schedule with no timezone awareness was the previous rotation.",
    "Polling for status updates was required before webhooks were implemented.",
    "Bash scripts from 2021 served as the abandoned load-testing framework.",
    "Every UI change required a full deployment before feature flags were adopted.",
    "Nagios with a 3000-line Perl script configured the old monitoring stack.",
    "Incident postmortems were unsearchable PDFs in a shared drive.",
    "XML-RPC with a custom parser that broke on Unicode was the old API protocol.",
    "A dedicated QA silo existed before embedded QA engineers joined each squad.",
    "Scheduled 4-hour downtime windows were required for all platform upgrades.",
    "Custom cron-based orchestration managed workflows before the job scheduler.",
    "Manual spreadsheet tracking of service dependencies preceded the service catalog.",
]

FILLER_WORDS = {
    "problem": ["returning 503 errors","dropping messages","showing stale data","timing out","producing duplicates","leaking memory","throwing NullPointerException","failing schema validation"],
    "context": ["peak traffic hours","deployments on Fridays","large payloads","concurrent users above 100","mobile clients","the EU region only","requests with Unicode","batch operations"],
    "issue": ["race condition","memory leak","connection pool exhaustion","cache invalidation bug","deadlock","infinite retry loop"],
    "trigger": ["config push at 3PM","database migration","Kafka partition change","TLS certificate rotation","load-balancer failover"],
    "feature": ["rate limiting","circuit breaking","request deduplication","graceful degradation","dark launch support","canary deployment support"],
    "version": ["v2.3.1","v3.0.2","v1.8.7","v4.2.0","v2.9.4"],
    "bug": ["regression in concurrent processing","off-by-one error in pagination","N+1 query problem","serialization bug with timestamps","hash collision in the partitioner"],
    "metric": ["p99 latency","error rate","throughput","CPU utilization","memory usage","request queue depth"],
    "value": ["spiked to 95%","dropped to 12%","tripled overnight","fluctuated by ±40%","plateaued at 200ms"],
    "change": ["latest deployment","config update","DNS change","certificate renewal","upstream API deprecation"],
    "condition": ["the upstream returns 429s","the cache is cold","the payload exceeds 1MB","the client disconnects mid-request","multiple regions are active"],
    "component": ["request handler","worker pool","cache layer","authentication middleware","serialization module"],
    "pattern": ["async/await","circuit breaker","bulkhead isolation","event sourcing","CQRS"],
    "old_pattern": ["synchronous calls","unbounded retries","shared thread pool","direct database access","monolithic handler"],
    "bottleneck": ["database connection pool","external API call","synchronous I/O","large object allocation","lock contention"],
    "symptom": ["p99 latency spikes to 3 seconds","OOM after 6 hours of uptime","request queue growing unboundedly","50% of requests timing out"],
    "guarantees": ["guarantees","enforces","maintains","provides"],
    "sla": ["99.5%","99.9%","99.95%","99.99%"],
    "latency": ["200","500","100","800","50"],
    "percentile": ["95","99","99.9"],
    "header": ["X-Trace-Id","X-Request-Id","X-Correlation-Id","X-Tenant-Id"],
    "purpose": ["distributed tracing","request correlation","multi-tenant isolation","rate-limit tracking"],
    "operation": ["idempotent request processing","consistent hashing for workload distribution","optimistic concurrency control"],
    "detail": ["submitting the same request twice produces one result with the same ID","requests with identical keys always route to the same worker","conflicts are detected via version vectors and resolved by the client"],
    "data": ["Health check results","Performance metrics","Audit log entries","Usage statistics"],
    "interval": ["15","30","60","10","5"],
    "topic": ["svc.health","svc.metrics","svc.events","svc.audit"],
    "key": ["service_id","tenant_id","request_id","user_id"],
    "auth": ["a client certificate for mutual TLS","an OAuth2 bearer token with audience validation","a signed JWT with a 5-minute expiry","an API key with SHA-256 HMAC signing"],
    "reason": ["authentication","rate limiting","billing attribution","request tracing"],
    "what": ["frequently accessed reference data","user session tokens","rate-limit counters","computed aggregation results"],
    "where": ["Redis","Memcached","an in-memory LRU cache","a local SQLite database"],
    "ttl": ["30-minute","2-hour","15-second","24-hour"],
    "n": ["3","5","7","10"],
    "reset": ["30","60","120","15"],
    "cache_type": ["LRU","TTL-based","least-frequently-used"],
    "size": ["1000","5000","100","2000"],
    "cmd": ["just test-svc","make bench-svc","just lint-svc"],
    "action": ["execute the standard benchmark suite against","run integration tests for","type-check"],
    "data": ["production-like traffic","a simulated Redis instance","sample payloads from S3"],
    "path": ["svc/config/","config/svc/","deploy/svc/"],
    "envs": ["dev, staging, and production","dev and production","staging and canary"],
    "runner": ["just","make","task"],
    "tool": ["Docker Compose","Testcontainers","localstack"],
    "frequency": ["quarterly","monthly","bi-weekly"],
    "review_type": ["security","architecture","compliance"],
    "dashboard": ["slo-tracker","health-dashboard","compliance-monitor"],
    "requirement": ["propagate trace context via W3C headers","report SLO compliance every 5 minutes","log all access with the requesting user ID"],
    "target": ["99.9%","99.5%","99.99%"],
    "scope": ["customer-facing","internal","all"],
    "capability": ["graceful degradation","circuit breaking","feature toggles"],
    "dependency": ["the upstream service","the database","the cache","the message broker"],
    "fallback": ["static defaults","cached responses","a degraded mode","manual processing"],
    "viz": ["heatmap","candlestick chart","time-series graph","gauge panel"],
    "alt": ["individual markers","a table view","a list","email notifications"],
    "label": ["stale","critical","warning","degraded"],
    "reports": ["optimization reports","audit logs","performance summaries"],
    "format": ["digest email","Slack message","dashboard widget"],
    "list": ["vehicle list","candidate shortlist","document queue","alert list"],
    "field": ["next-estimated-arrival time","interview availability","submission timestamp","priority"],
    "alt_field": ["vehicle ID","score","claim amount","alphabetical order"],
    "unit": ["liters-per-100-km","miles-per-gallon","percentage points","basis points"],
    "alt_unit": ["MPG","kilometers-per-liter","raw counts","dollars"],
}


def gen_unit(domain, target, seed_val):
    """Generate a unique unit text for a domain+target combo."""
    random.seed(seed_val)
    dk = domain["project"]
    s, r, p = domain["service"], domain["repo"], domain["project"]
    vocab = domain["vocab"]
    
    def pick(key):
        options = FILLER_WORDS.get(key, [key])
        return random.choice(options)
    
    if target == "task_state":
        tmpl = random.choice(TASK_PHRASES)
        text = tmpl.format(
            svc=s, problem=pick("problem"), context=pick("context"),
            issue=pick("issue"), trigger=pick("trigger"),
            feature=pick("feature"), version=pick("version"), bug=pick("bug"),
            metric=pick("metric"), value=pick("value"), change=pick("change"),
            condition=pick("condition"), component=pick("component"),
            pattern=pick("pattern"), old_pattern=pick("old_pattern"),
            bottleneck=pick("bottleneck"), symptom=pick("symptom"),
        )
    elif target == "service_memory":
        tmpl = random.choice(SVC_PHRASES)
        text = tmpl.format(
            svc=s, guarantees=pick("guarantees"), sla=pick("sla"),
            latency=pick("latency"), percentile=pick("percentile"),
            header=pick("header"), purpose=pick("purpose"),
            operation=pick("operation"), detail=pick("detail"),
            data=pick("data"), interval=pick("interval"), topic=pick("topic"),
            key=pick("key"), auth=pick("auth"), reason=pick("reason"),
            what=pick("what"), where=pick("where"), ttl=pick("ttl"),
            n=pick("n"), reset=pick("reset"),
            cache_type=pick("cache_type"), size=pick("size"),
        )
    elif target == "repo_memory":
        tmpl = random.choice(REPO_PHRASES)
        text = tmpl.format(
            svc=s, repo=r, what=random.choice(vocab),
            cmd=pick("cmd"), action=pick("action"), data=pick("data"),
            condition=pick("condition"), path=pick("path"), envs=pick("envs"),
            runner=pick("runner"), tool=pick("tool"),
        )
    elif target == "project_memory":
        tmpl = random.choice(PROJ_PHRASES)
        text = tmpl.format(
            proj=p, svc=s, what=random.choice(vocab),
            review_type=pick("review_type"), frequency=pick("frequency"),
            metric=random.choice(vocab), dashboard=pick("dashboard"),
            interval=pick("interval"), tool=random.choice(["OpenTelemetry","Prometheus","Grafana"]),
            purpose=random.choice(vocab), requirement=pick("requirement"),
            target=pick("target"), scope=pick("scope"),
            capability=pick("capability"), dependency=pick("dependency"),
            fallback=pick("fallback"), path="docs/architecture/decisions/",
        )
    else:  # user_profile
        tmpl = random.choice(USER_PHRASES)
        text = tmpl.format(
            svc=s, viz=pick("viz"), what=random.choice(vocab),
            alt=pick("alt"), condition=pick("condition"), label=pick("label"),
            reports=pick("reports"), format=pick("format"), frequency="daily",
            n=pick("n"), list=pick("list"), field=pick("field"),
            alt_field=pick("alt_field"), metric=random.choice(vocab),
            unit=pick("unit"), alt_unit=pick("alt_unit"), context="our team",
        )
    
    # Add domain-specific vocabulary word for uniqueness
    extra_vocab = random.choice(vocab)
    if extra_vocab.lower() not in text.lower():
        text += f" This relates to the {extra_vocab} functionality."
    
    return text


def build():
    random.seed(77)
    cases = []
    _seed = [1000]  # mutable counter for unique seeds
    
    shapes_180 = ["read_only"]*32 + ["store_skip_only"]*70 + ["read_store_joint"]*78
    random.shuffle(shapes_180)
    sens_180 = [True]*28 + [False]*152; random.shuffle(sens_180)
    bnd_180 = [True]*46 + [False]*134; random.shuffle(bnd_180)
    
    domain_list = list(DOMAINS)
    sens_idx = 0
    
    for i in range(180):
        d = domain_list[i % 8]
        dk = d["project"]
        s, r, p = d["service"], d["repo"], d["project"]
        vocab = d["vocab"]
        shape = shapes_180[i]
        is_sens = sens_180[i]
        is_bnd = bnd_180[i]
        
        # ── Memories ──
        nm = random.randint(2, min(5, 5))
        if shape == "read_only": nm = random.randint(2, 4)
        
        mems_raw = []
        _seed[0] += 1; svc_text = gen_unit(d, "service_memory", _seed[0])
        mems_raw.append({"target":"service_memory","text":svc_text,"tags":[]})
        
        if nm >= 2 and random.random() < 0.7:
            _seed[0] += 1; mems_raw.append({"target":"repo_memory","text":gen_unit(d,"repo_memory",_seed[0]),"tags":[]})
        if nm >= 3 and random.random() < 0.5:
            _seed[0] += 1; mems_raw.append({"target":"project_memory","text":gen_unit(d,"project_memory",_seed[0]),"tags":[]})
        if nm >= 4 and random.random() < 0.4:
            _seed[0] += 1; mems_raw.append({"target":"user_profile","text":gen_unit(d,"user_profile",_seed[0]),"tags":[]})
        
        while len(mems_raw) < nm:
            mems_raw.append({"target":"service_memory","text":random.choice(STALE_POOL),"tags":["stale"]})
        
        random.shuffle(mems_raw)
        memories = []
        for j, mr in enumerate(mems_raw):
            memories.append({"memory_id":f"m{j+1}","target":mr["target"],
                           "text":mr["text"],"tags":mr.get("tags",[])})
        
        # ── Units ──
        units, g_read, g_store, g_skip, tags = [], [], [], [], []
        
        if shape == "read_only":
            _seed[0] += 1
            u1_text = gen_unit(d, "task_state", _seed[0])
            units.append({"unit_id":"u1","text":u1_text,"tags":["task_progress","read_only"]})
            g_skip.append("u1")
            non_stale = [m["memory_id"] for m in memories if "stale" not in m.get("tags",[])]
            n_read = min(random.randint(1, min(3, len(non_stale))), len(non_stale))
            g_read = random.sample(non_stale, n_read)
            tags = ["read_only"]
        
        elif shape == "store_skip_only":
            # 2-3 units: 2 STORE + 1 SKIP/sensitive
            target1 = random.choices(TARGETS, weights=[33,32,17,12,6])[0]
            _seed[0] += 1
            u1_text = gen_unit(d, target1, _seed[0])
            u1_tags = ["store_skip_only", f"target_{target1}"]
            if is_bnd: u1_tags.append("target_boundary")
            units.append({"unit_id":"u1","text":u1_text,"tags":u1_tags})
            g_store.append({"unit_id":"u1","target":target1})
            
            target2 = random.choices(TARGETS, weights=[33,32,17,12,6])[0]
            _seed[0] += 1
            u2_text = gen_unit(d, target2, _seed[0])
            u2_tags = ["store_skip_only", f"target_{target2}"]
            if is_bnd: u2_tags.append("target_boundary")
            units.append({"unit_id":"u2","text":u2_text,"tags":u2_tags})
            g_store.append({"unit_id":"u2","target":target2})
            
            if is_sens:
                sens_text, stype = SENSITIVE_POOL[sens_idx % len(SENSITIVE_POOL)]
                sens_idx += 1
                units.append({"unit_id":"u3","text":sens_text,
                             "tags":[f"sensitive_{stype}","sensitive_boundary","store_skip_only"]})
                g_skip.append("u3")
                tags.append("sensitive_boundary")
            else:
                _seed[0] += 1
                u3_text = gen_unit(d, "task_state", _seed[0])
                units.append({"unit_id":"u3","text":u3_text,"tags":["task_progress","store_skip_only"]})
                g_skip.append("u3")
            tags.append("store_skip_only")
        
        else:  # read_store_joint
            # Unit 1: task→SKIP
            _seed[0] += 1
            u1_text = gen_unit(d, "task_state", _seed[0])
            units.append({"unit_id":"u1","text":u1_text,"tags":["task_progress","read_store_joint"]})
            g_skip.append("u1")
            
            # Unit 2: STORE (always — sensitive gets u3 instead)
            if is_sens:
                # u2 is STORE, u3 is sensitive SKIP (extra unit)
                target = random.choices(TARGETS, weights=[33,32,17,12,6])[0]
                _seed[0] += 1
                u2_text = gen_unit(d, target, _seed[0])
                u2_tags = ["read_store_joint", f"target_{target}"]
                if is_bnd: u2_tags.append("target_boundary")
                units.append({"unit_id":"u2","text":u2_text,"tags":u2_tags})
                g_store.append({"unit_id":"u2","target":target})
                
                sens_text, stype = SENSITIVE_POOL[sens_idx % len(SENSITIVE_POOL)]
                sens_idx += 1
                units.append({"unit_id":"u3","text":sens_text,
                             "tags":[f"sensitive_{stype}","sensitive_boundary","read_store_joint"]})
                g_skip.append("u3")
                tags.append("sensitive_boundary")
            else:
                # 2 STORE units (u2, u3) when not sensitive
                target2 = random.choices(TARGETS, weights=[33,32,17,12,6])[0]
                _seed[0] += 1
                u2_text = gen_unit(d, target2, _seed[0])
                u2_tags = ["read_store_joint", f"target_{target2}"]
                if is_bnd: u2_tags.append("target_boundary")
                units.append({"unit_id":"u2","text":u2_text,"tags":u2_tags})
                g_store.append({"unit_id":"u2","target":target2})
                
                target3 = random.choices(TARGETS, weights=[33,32,17,12,6])[0]
                _seed[0] += 1
                u3_text = gen_unit(d, target3, _seed[0])
                u3_tags = ["read_store_joint", f"target_{target3}"]
                if is_bnd: u3_tags.append("target_boundary")
                units.append({"unit_id":"u3","text":u3_text,"tags":u3_tags})
                g_store.append({"unit_id":"u3","target":target3})
            
            non_stale = [m["memory_id"] for m in memories if "stale" not in m.get("tags",[])]
            n_read = min(random.randint(1, min(3, len(non_stale))), len(non_stale))
            g_read = random.sample(non_stale, n_read)
            tags.append("read_store_joint")
        
        runtime = {"project":p,"repo":r,"service":s,"task":f"Working on the {s} service in the {p} project"}
        if is_bnd: tags.append("target_boundary")
        if is_sens: tags.append("sensitive_boundary")
        tags = list(set(tags))
        
        cases.append({"case_id":f"v05e_gold_{i+1:04d}","runtime_context":runtime,
                      "candidate_memories":memories,"current_units":units,
                      "gold":{"read":sorted(g_read),"store":g_store,"skip":sorted(g_skip),"dsl":""},
                      "tags":tags,"notes":f"gold_v2_003. shape={shape}"})
    
    random.shuffle(cases)
    active, holdout = cases[:150], cases[150:180]
    for i,c in enumerate(active): c["case_id"]=f"v05e_gold_active_{i+1:04d}"
    for i,c in enumerate(holdout): c["case_id"]=f"v05e_gold_holdout_{i+1:04d}"
    return active, holdout


def compute_hash(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_jsonl(path, cases):
    with open(path,"w") as f:
        for c in cases: f.write(json.dumps(c,ensure_ascii=False)+"\n")

def main():
    active, holdout = build()
    base = Path("data/v05e/gold_v2")
    base.mkdir(parents=True, exist_ok=True)
    ap = base / "v05e_gold_v2_003_active_cases.jsonl"
    hp = base / "v05e_gold_v2_003_holdout_cases.jsonl"
    write_jsonl(ap, active); write_jsonl(hp, holdout)
    
    print(f"Active: {len(active)} | Holdout: {len(holdout)}")
    shapes, sens, bnd, total_store = {}, 0, 0, 0
    targets = {t:0 for t in TARGETS}
    all_units, exact_set = [], set()
    exact_conflicts = 0
    
    for c in active:
        s = ("read_only" if "read_only" in c["tags"] else
             "store_skip_only" if "store_skip_only" in c["tags"] else "read_store_joint")
        shapes[s] = shapes.get(s,0)+1
        if "sensitive_boundary" in c["tags"]: sens += 1
        if "target_boundary" in c["tags"]: bnd += 1
        for st in c["gold"]["store"]: targets[st["target"]] += 1; total_store += 1
        for u in c["current_units"]:
            t = u["text"].strip().lower()
            all_units.append(t)
            if t in exact_set: exact_conflicts += 1
            exact_set.add(t)
    
    print(f"\nShapes: { {k: f'{v} ({100*v/150:.0f}%)' for k,v in shapes.items()} }")
    print(f"Targets ({total_store}): { {t: f'{n} ({100*n/max(1,total_store):.1f}%)' for t,n in sorted(targets.items())} }")
    print(f"Stress: sensitive={sens}, boundary={bnd}")
    
    uu = len(exact_set)
    ALL_NAMES = [d['project'] for d in DOMAINS] + [d['repo'] for d in DOMAINS] + [d['service'] for d in DOMAINS]
    def norm(text):
        t = text.lower()
        for n in ALL_NAMES: t = t.replace(n, 'SVC')
        t = re.sub(r'v?\d+\.\d+(\.\d+)?','VER',t)
        t = re.sub(r'\d+','N',t)
        return ' '.join(t.split()[:10])
    us = Counter(norm(u['text']) for c in active for u in c['current_units'])
    
    print(f"\nDiversity: {len(all_units)} unit instances, {uu} unique ({100*uu/len(all_units):.1f}%)")
    print(f"  Exact text conflicts: {exact_conflicts}")
    print(f"  Max norm skeleton repeat: {max(us.values())}")
    print(f"  Skeletons >5: {sum(1 for v in us.values() if v>5)}")
    
    h = {"active":compute_hash(ap),"holdout":compute_hash(hp)}
    print(f"\nHashes: active={h['active'][:16]}... holdout={h['holdout'][:16]}...")
    return 0

if __name__=="__main__":
    sys.exit(main())
