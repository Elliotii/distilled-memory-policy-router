"""Generate 200 new cases for batch500, merge with batch300, validate, and produce SFT messages.

Context 5.2-A: batch500 draft generation and validation.
Not final train/dev/gold. Not locked. 200 hand-crafted non-template cases.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ── SFT rendering (same as render_sft_messages.py) ──────────────────────────

SYSTEM_PROMPT = (
    "You are a memory policy router for coding-agent contexts.\n\n"
    "Task:\n"
    "Given RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:\n"
    "- which candidate memories to READ;\n"
    "- which current unit IDs to STORE and to which target;\n"
    "- which current unit IDs to SKIP.\n\n"
    "Output only the DSL. Do not include comments, prose, explanations, or JSON.\n\n"
    "Allowed DSL lines:\n"
    "READ <memory_id_list|NONE>\n"
    "STORE <target> <unit_id>\n"
    "STORE NONE\n"
    "SKIP <unit_id_list|NONE>\n\n"
    "Legal STORE targets:\n"
    "user_profile, project_memory, repo_memory, service_memory, task_state\n\n"
    "Rules:\n"
    "- READ useful memories only; skip merely related or stale ones.\n"
    "- STORE durable, reusable information with correct target.\n"
    "- SKIP sensitive, temporary, one-off, or out-of-scope content.\n"
    "- Every current unit must appear exactly once in STORE or SKIP.\n"
    "- Do not invent IDs, targets, or content."
)

def render_user_input(case: dict[str, Any]) -> str:
    rc = case["runtime_context"]
    lines = [
        "RUNTIME_CONTEXT",
        f"project: {rc['project']}",
        f"repo: {rc['repo']}",
        f"service: {rc['service']}",
        f"task: {rc['task']}",
        "",
    ]
    mems = case["candidate_memories"]
    if mems:
        lines.append("CANDIDATE_MEMORIES")
        for m in mems:
            lines.append(f"{m['memory_id']} [{m['target']}]: {m['content']}")
    else:
        lines.append("CANDIDATE_MEMORIES\nNONE")
    lines.append("")
    lines.append("CURRENT_UNITS")
    for u in case["current_units"]:
        lines.append(f"{u['unit_id']}: {u['text']}")
    return "\n".join(lines)

def build_sft_message(case: dict[str, Any], source: str) -> dict[str, Any]:
    gold_store = case["gold"]["store"]
    has_read = bool(case["gold"]["read"])
    has_store = bool(gold_store)
    if has_read and has_store:
        shape = "READ + STORE joint"
    elif has_read:
        shape = "READ-only"
    elif has_store:
        shape = "STORE/SKIP-only"
    else:
        shape = "no READ and no STORE"
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": render_user_input(case)},
            {"role": "assistant", "content": case["gold"]["dsl"]},
        ],
        "case_id": case["case_id"],
        "source": source,
        "metadata": {
            "tags": case["tags"],
            "num_candidate_memories": len(case["candidate_memories"]),
            "num_current_units": len(case["current_units"]),
            "gold_shape": shape,
            "store_targets": [s["target"] for s in gold_store],
            "is_final_train_data": False,
        },
    }

# ── Abbreviations for case definition ──────────────────────────────────────
# To keep case definitions compact:
# rc = runtime_context, cm = candidate_memories, cu = current_units
# mid = memory_id, uid = unit_id, tgt = target

def m(mid: str, tgt: str, content: str) -> dict:
    return {"memory_id": mid, "target": tgt, "content": content}

def u(uid: str, text: str) -> dict:
    return {"unit_id": uid, "text": text}

def st(tgt: str, uid: str) -> dict:
    return {"target": tgt, "unit_id": uid}

def make_case(cid: str, rc: dict, cms: list, cus: list, read: list, store: list, skip: list, tags: list, notes: str) -> dict:
    dsl_lines = []
    if read:
        dsl_lines.append(f"READ {','.join(read)}")
    else:
        dsl_lines.append("READ NONE")
    for s in store:
        dsl_lines.append(f"STORE {s['target']} {s['unit_id']}")
    if not store:
        dsl_lines.append("STORE NONE")
    if skip:
        dsl_lines.append(f"SKIP {','.join(skip)}")
    else:
        dsl_lines.append("SKIP NONE")
    return {
        "case_id": cid,
        "runtime_context": rc,
        "candidate_memories": cms,
        "current_units": cus,
        "gold": {"read": read, "store": store, "skip": skip, "dsl": "\n".join(dsl_lines)},
        "tags": tags,
        "notes": notes,
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 200 NEW CASES FOR BATCH500
# Organized by shape group for distribution tracking.
# Each case is hand-crafted with unique semantic content.
# ═══════════════════════════════════════════════════════════════════════════════

NEW200: list[dict[str, Any]] = []

# ── READ+STORE JOINT (70 cases) ─────────────────────────────────────────────

# === Group A: service_memory + task_state combos (svc_vs_task boundary) ===

NEW200.append(make_case("v05_batch500_0001",
    rc={"project":"customer-support","repo":"helpdesk","service":"ticket-router","task":"define ticket routing algorithm"},
    cms=[m("m1","service_memory","The ticket router assigns incoming tickets to agents based on skill tags and current queue depth."),
         m("m2","task_state","The current routing uses round-robin assignment without considering agent expertise.")],
    cus=[u("u1","The ticket router must route billing-related tickets to agents with the billing_certified skill tag, ignoring queue-balance for these tickets."),
         u("u2","Update the agent skill matrix to include the new billing_certified tag for 5 agents.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines durable routing rule (mandatory skill-based routing for billing) -> service_memory. u2 is current config update task -> task_state."))

NEW200.append(make_case("v05_batch500_0002",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"query-engine","task":"add query result caching policy"},
    cms=[m("m1","service_memory","The query engine executes SQL against a ClickHouse cluster and returns results as JSON arrays."),
         m("m2","repo_memory","Query engine cache configuration lives in config/query_engine/cache.yaml with TTL per query type.")],
    cus=[u("u1","The query engine must cache aggregate query results for 15 minutes when the underlying table has not received new rows."),
         u("u2","Add a cache-busting mechanism that invalidates cached results when the source table's modification timestamp advances.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("service_memory","u2")], skip=[],
    tags=["read_store_joint","service_invariant","repo_convention"],
    notes="u1 defines caching policy (durable behavior) -> service_memory. u2 defines cache invalidation mechanism (also durable behavior) -> service_memory. Both are architectural decisions."))

NEW200.append(make_case("v05_batch500_0003",
    rc={"project":"healthcare-admin","repo":"medflow","service":"patient-portal","task":"add appointment conflict detection"},
    cms=[m("m1","service_memory","The patient portal currently allows booking appointments in 15-minute slots without checking provider availability."),
         m("m2","project_memory","The medflow project must comply with HIPAA data handling requirements for all patient-facing services.")],
    cus=[u("u1","The appointment scheduler must reject bookings that overlap with an existing confirmed appointment for the same provider."),
         u("u2","Add a provider availability cache that refreshes every 30 seconds from the scheduling database.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="New domain: healthcare-admin. u1 is a durable business rule -> service_memory. u2 is an implementation detail -> task_state."))

NEW200.append(make_case("v05_batch500_0004",
    rc={"project":"supply-chain","repo":"logistix","service":"inventory-sync","task":"add low-stock alert thresholds"},
    cms=[m("m1","service_memory","The inventory sync service polls warehouse databases every 5 minutes and updates the central inventory table."),
         m("m2","repo_memory","Alert threshold configuration per SKU is stored in config/inventory/alert_thresholds.yaml.")],
    cus=[u("u1","The inventory sync service must trigger a low-stock alert when any SKU quantity falls below its configured reorder point for more than 2 consecutive polling cycles."),
         u("u2","Set the reorder point for SKU BX-4491 to 50 units and update the alert threshold config.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="New domain: supply-chain. u1 defines durable alert behavior (2-cycle hysteresis) -> service_memory. u2 is a specific config update -> task_state."))

NEW200.append(make_case("v05_batch500_0005",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"contract-parser","task":"add clause extraction rules"},
    cms=[m("m1","service_memory","The contract parser extracts clauses by section number and categorizes them as obligation, liability, or termination."),
         m("m2","project_memory","The clausekeeper project does not provide legal advice; it only structures and indexes contract text.")],
    cus=[u("u1","The contract parser must flag any clause containing the phrase 'indemnify and hold harmless' for manual attorney review, regardless of its automatic category."),
         u("u2","Add the indemnification flag to the clause metadata schema in the parser output.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="New domain: legal-docs. u1 is a durable parsing rule (mandatory human review for indemnification) -> service_memory. u2 is schema extension -> task_state."))

NEW200.append(make_case("v05_batch500_0006",
    rc={"project":"creator-tools","repo":"artisan","service":"render-farm","task":"add job priority queue"},
    cms=[m("m1","service_memory","The render farm processes jobs in FIFO order across a pool of 8 GPU workers with per-job timeout of 4 hours."),
         m("m2","repo_memory","Render job configurations including frame ranges and output formats are defined in jobs/<job_id>/render_config.json.")],
    cus=[u("u1","The render farm must support a priority queue where jobs tagged 'client_review' are scheduled before regular jobs, preserving FIFO within each priority tier."),
         u("u2","Add the priority field to the job submission API and update the scheduler to read it.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="New domain: creator-tools. u1 defines priority scheduling behavior -> service_memory. u2 is API update task -> task_state."))

# --- Tag-rich: related_but_useless + stale_memory ---

NEW200.append(make_case("v05_batch500_0007",
    rc={"project":"data-platform","repo":"data-jobs","service":"ingestion","task":"fix CSV parsing error on currency fields"},
    cms=[m("m1","service_memory","The ingestion service parses CSV files using a schema defined in the data catalog and rejects rows with mismatched column counts."),
         m("m2","service_memory","The old v1 ingestion used a fixed-width parser that could not handle quoted fields."),
         m("m3","task_state","Last month's ingestion bug was caused by a UTF-8 BOM in the header row of the finance department CSV.")],
    cus=[u("u1","The ingestion service must strip euro currency symbols from amount fields before casting to numeric, because the European branch exports amounts as '€1,234.56'."),
         u("u2","Add a currency symbol stripping step to the CSV preprocessing stage before schema validation.")],
    read=["m1"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","stale_memory","related_but_useless"],
    notes="m2 is stale legacy parsing. m3 is related (previous bug) but about a different issue (UTF-8 BOM vs currency symbols). Both correctly not read. u1 defines durable preprocessing rule -> service_memory. u2 is implementation task -> task_state."))

NEW200.append(make_case("v05_batch500_0008",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"catalog-search","task":"improve search relevance for multi-word queries"},
    cms=[m("m1","service_memory","The catalog search uses Elasticsearch with BM25 scoring and a synonym filter for common product name variations."),
         m("m2","service_memory","The previous search ranking experiment used learning-to-rank with user click data but was rolled back due to cold-start problems."),
         m("m3","repo_memory","Search index mappings are defined in elasticsearch/mappings/catalog_v3.json.")],
    cus=[u("u1","The catalog search must boost exact phrase matches by a factor of 3.0 over individual term matches when the query contains quoted strings."),
         u("u2","Run an A/B test comparing the new phrase boost against the current BM25-only baseline on 10% of traffic.")],
    read=["m1","m3"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","stale_memory","related_but_useless","service_vs_task_state"],
    notes="m2 is stale (rolled-back experiment, different approach). m1 and m3 provide current search config context. u1 defines durable ranking behavior -> service_memory. u2 is current experiment plan -> task_state."))

NEW200.append(make_case("v05_batch500_0009",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"sft-renderer","task":"add system prompt templating"},
    cms=[m("m1","service_memory","The SFT message renderer converts case JSON records into chat-format messages with system, user, and assistant roles."),
         m("m2","project_memory","The v0.4 interface pilot compared three interfaces; v0.5 uses only Unit DSL for training."),
         m("m3","service_memory","The old v0.3 prompt builder used a single monolithic prompt without role separation.")],
    cus=[u("u1","The SFT renderer must support a configurable system prompt template that can be swapped per experiment without modifying the renderer code."),
         u("u2","Extract the system prompt into a separate template file under prompts/v05/system_prompt.txt.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","stale_memory","related_but_useless"],
    notes="m3 is stale v0.3 reference. m2 is project-level but used as context. u1 defines durable renderer capability -> service_memory. u2 is current refactoring task -> task_state."))

# --- Tag-rich: sensitive_boundary ---

NEW200.append(make_case("v05_batch500_0010",
    rc={"project":"finance-dashboard","repo":"finboard","service":"report-generator","task":"add scheduled PDF report delivery"},
    cms=[m("m1","service_memory","The report generator renders dashboard widgets as PDF files using headless Chromium and stores them in the reports bucket."),
         m("m2","repo_memory","Report delivery schedules are configured in config/reports/schedules.yaml per recipient.")],
    cus=[u("u1","The report generator must deliver scheduled reports via email with the PDF attached and a summary in the email body."),
         u("u2","Add the CFO's email address cfo@company-internal.example.com to the report delivery list."),
         u("u3","My SMTP relay password for the staging environment is smtp_stage_2026_pass.")],
    read=["m1","m2"], store=[st("service_memory","u1")], skip=["u2","u3"],
    tags=["read_store_joint","service_invariant","sensitive_boundary"],
    notes="u1 is durable delivery behavior -> service_memory. u2 is an internal email (borderline but SKIP as it's a specific contact detail that could be considered PII). u3 is a password -> must SKIP."))

NEW200.append(make_case("v05_batch500_0011",
    rc={"project":"customer-support","repo":"helpdesk","service":"chat-router","task":"add live chat handoff to human agents"},
    cms=[m("m1","service_memory","The chat router classifies incoming messages by intent and either responds automatically or queues for human agent."),
         m("m2","task_state","The current handoff threshold routes to human when confidence is below 0.7; this was set last quarter.")],
    cus=[u("u1","The chat router must redact credit card numbers from chat transcripts before they are stored, matching the regex pattern for 13-16 digit sequences."),
         u("u2","A customer just pasted their full credit card number 4532-1234-5678-9012 into the chat window."),
         u("u3","Add a PCI compliance audit log for the redaction process.")],
    read=["m1"], store=[st("service_memory","u1"),st("task_state","u3")], skip=["u2"],
    tags=["read_store_joint","service_invariant","task_progress","sensitive_boundary","stale_memory"],
    notes="u1 defines durable redaction behavior -> service_memory. u2 contains a credit card number (even though synthetic) -> must SKIP. u3 is current task -> task_state. m2 is stale threshold from last quarter."))

NEW200.append(make_case("v05_batch500_0012",
    rc={"project":"mobile-field","repo":"field-app","service":"location-tracker","task":"add geofence entry alerts"},
    cms=[m("m1","service_memory","The location tracker samples GPS coordinates every 60 seconds and evaluates geofence membership using polygon containment."),
         m("m2","user_profile","The user prefers location-based alerts to be delivered as silent notifications that appear in the notification tray only.")],
    cus=[u("u1","The location tracker must trigger a geofence entry alert when the device enters any customer site polygon, with a 90-second debounce to avoid false triggers."),
         u("u2","The user's home address is 5678 Oak Lane, Springfield, IL 62701 — use this to create a home geofence."),
         u("u3","Add geofence alert logging to the analytics pipeline for measuring alert accuracy.")],
    read=["m1"], store=[st("service_memory","u1"),st("task_state","u3")], skip=["u2"],
    tags=["read_store_joint","service_invariant","task_progress","sensitive_boundary","related_but_useless"],
    notes="u1 defines durable geofence behavior -> service_memory. u2 contains a home address -> must SKIP (even though user provided it for a feature). u3 is current task -> task_state. m2 is related (notification preference) but about a different aspect."))

# --- More READ+STORE joint cases across domains ---

NEW200.append(make_case("v05_batch500_0013",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"version-manager","task":"add documentation version diffing"},
    cms=[m("m1","service_memory","The version manager tracks documentation versions by git commit hash and stores rendered HTML snapshots in the docstore bucket."),
         m("m2","repo_memory","Versioned documentation is accessible at /docs/v<major>.<minor>/ and the latest alias always points to the most recent stable version.")],
    cus=[u("u1","The version manager must compute a semantic diff between two documentation versions, highlighting added, removed, and modified sections with visual indicators."),
         u("u2","Add a diff endpoint to the version manager API that accepts two version tags and returns a structured diff JSON.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines durable diff behavior -> service_memory. u2 is API implementation task -> task_state."))

NEW200.append(make_case("v05_batch500_0014",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"step-executor","task":"add conditional branching support"},
    cms=[m("m1","service_memory","The step executor runs workflow steps sequentially and passes output context as JSON between steps."),
         m("m2","repo_memory","Workflow definitions are stored as YAML files in workflows/ with a schema validated at load time.")],
    cus=[u("u1","The step executor must support conditional branching where a step's output field is compared against a configured value, and the next step is chosen from a branch map."),
         u("u2","Add branch condition evaluation to the step executor's transition logic before the next workflow release.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines durable branching behavior -> service_memory. u2 is implementation plan -> task_state."))

NEW200.append(make_case("v05_batch500_0015",
    rc={"project":"travel-planner","repo":"voyager","service":"itinerary-builder","task":"add multi-city stopover optimization"},
    cms=[m("m1","service_memory","The itinerary builder constructs travel plans by chaining flights, hotels, and activities into a time-ordered schedule."),
         m("m2","service_memory","The pricing service caches flight prices with a 5-minute TTL and does not re-query within the cache window.")],
    cus=[u("u1","The itinerary builder must optimize multi-city itineraries by evaluating all permutations of stopover cities and selecting the route with the lowest total travel time under 72 hours."),
         u("u2","The pricing service must refresh its cache when the itinerary builder requests prices for a multi-city route that spans more than 3 days.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("service_memory","u2")], skip=[],
    tags=["read_store_joint","service_invariant","repo_vs_service"],
    notes="u1 defines itinerary optimization algorithm -> service_memory. u2 defines pricing cache refresh behavior for multi-city routes -> service_memory. Both are durable service behaviors."))

NEW200.append(make_case("v05_batch500_0016",
    rc={"project":"education-platform","repo":"learnhub","service":"assessment-engine","task":"add adaptive question difficulty"},
    cms=[m("m1","service_memory","The assessment engine selects questions from a pool tagged by difficulty level and topic, using a fixed 3-4-3 ratio for easy-medium-hard."),
         m("m2","task_state","The current question pool has 2400 questions across 12 topics, with medium-difficulty questions comprising 45%.")],
    cus=[u("u1","The assessment engine must adjust question difficulty dynamically based on the learner's running accuracy: increase difficulty when accuracy exceeds 80% over the last 5 questions, decrease when it falls below 40%."),
         u("u2","Add the dynamic difficulty adjustment module as a middleware between question selection and presentation.")],
    read=["m1"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state","stale_memory"],
    notes="u1 defines adaptive difficulty algorithm with specific thresholds -> service_memory. u2 is implementation task -> task_state. m2 is stale pool statistics."))

NEW200.append(make_case("v05_batch500_0017",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"physics-engine","task":"add destructible environment support"},
    cms=[m("m1","service_memory","The physics engine simulates rigid-body collisions at 60Hz using the Bullet physics SDK with a fixed timestep of 1/120s."),
         m("m2","repo_memory","Physics collision meshes are stored under assets/physics/collision/ in the Wavefront OBJ format.")],
    cus=[u("u1","The physics engine must support destructible objects by replacing a rigid body with a cluster of smaller rigid bodies when accumulated damage exceeds the object's integrity threshold."),
         u("u2","Add the damage accumulation property to the physics material definition schema.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines durable destruction physics behavior -> service_memory. u2 is schema extension task -> task_state."))

NEW200.append(make_case("v05_batch500_0018",
    rc={"project":"data-platform","repo":"data-jobs","service":"quality-checker","task":"add anomaly detection for pipeline output"},
    cms=[m("m1","service_memory","The quality checker validates pipeline output tables against schema constraints and row-count expectations before marking a batch as complete."),
         m("m2","project_memory","The data-platform quality SLA requires that all data anomalies are detected within 30 minutes of pipeline completion.")],
    cus=[u("u1","The quality checker must run a Z-score anomaly detection on numeric columns, flagging any value more than 3 standard deviations from the column mean as anomalous."),
         u("u2","Add the Z-score anomaly detector as a new check type in the quality checker's check registry.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines durable anomaly detection algorithm (3-sigma rule) -> service_memory. u2 is implementation task -> task_state."))

NEW200.append(make_case("v05_batch500_0019",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"data-importer","task":"add CSV import with column mapping"},
    cms=[m("m1","service_memory","The data importer accepts CSV and JSON files, validates them against target table schemas, and inserts rows in batches of 1000."),
         m("m2","repo_memory","Import configurations including column mappings are stored in config/imports/<dataset_name>.yaml.")],
    cus=[u("u1","The data importer must support fuzzy column name matching when the CSV header does not exactly match the target schema, using Levenshtein distance with a maximum edit distance of 2."),
         u("u2","Build the fuzzy matching UI in the import wizard so users can review and confirm suggested mappings.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","repo_vs_service"],
    notes="u1 defines durable fuzzy matching behavior -> service_memory. u2 is UI task -> task_state."))

NEW200.append(make_case("v05_batch500_0020",
    rc={"project":"learning-assistant","repo":"tutorai","service":"quiz-generator","task":"add distractors to multiple-choice questions"},
    cms=[m("m1","service_memory","The quiz generator creates multiple-choice questions from study material by extracting key facts and generating 4 answer options."),
         m("m2","task_state","The current distractors are random sentences from unrelated topics, which learners find too easy to eliminate.")],
    cus=[u("u1","The quiz generator must produce plausible distractors by selecting sentences from the same topic that share keywords with the correct answer but contain a factual error."),
         u("u2","Replace the random-distractor logic with the new semantic-distractor generator in the quiz pipeline.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines durable distractor generation algorithm -> service_memory. u2 is replacement task -> task_state."))

# --- boundary cases: project_memory vs task_state ---

NEW200.append(make_case("v05_batch500_0021",
    rc={"project":"supply-chain","repo":"logistix","service":"route-optimizer","task":"add real-time traffic rerouting"},
    cms=[m("m1","service_memory","The route optimizer computes delivery routes using the Google OR-Tools constraint solver with time windows and vehicle capacity constraints."),
         m("m2","project_memory","The logistix project must keep all delivery route computation on-premise; no third-party cloud routing APIs are permitted.")],
    cus=[u("u1","The route optimizer must incorporate real-time traffic data from the internal traffic feed to dynamically reroute vehicles when a road segment's travel time increases by more than 50%."),
         u("u2","Add the traffic feed integration module to the route optimizer's data ingestion pipeline.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is a project-level constraint (on-premise only) -> project_memory context. u1 defines durable rerouting behavior -> service_memory. u2 is implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0022",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"obligation-tracker","task":"add obligation deadline reminders"},
    cms=[m("m1","service_memory","The obligation tracker extracts dated commitments from contract clauses and stores them with their due dates and responsible parties."),
         m("m2","project_memory","The clausekeeper project does not send legal notices or act as a registered agent; all communications are internal notifications only.")],
    cus=[u("u1","The obligation tracker must send reminder notifications 30, 14, and 3 days before each obligation deadline to the responsible party's email."),
         u("u2","Add the reminder schedule configuration to the obligation tracker's notification settings.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is a project-level scope limitation (no legal notices) -> project_memory. u1 defines durable reminder schedule -> service_memory. u2 is config task -> task_state."))

NEW200.append(make_case("v05_batch500_0023",
    rc={"project":"healthcare-admin","repo":"medflow","service":"appointment-scheduler","task":"add telehealth session support"},
    cms=[m("m1","service_memory","The appointment scheduler manages provider calendars with 15-minute slots and enforces a maximum of 24 patients per provider per day."),
         m("m2","project_memory","The medflow project requires all telehealth sessions to use the approved video platform MedLink; no external video conferencing tools are permitted.")],
    cus=[u("u1","The appointment scheduler must support a telehealth appointment type that reserves a video session slot on MedLink and sends the join link to the patient 15 minutes before the appointment."),
         u("u2","Add the telehealth appointment type to the scheduler's booking API and validate MedLink provider availability before confirming.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is a project-level platform constraint -> project_memory. u1 is durable telehealth scheduling behavior -> service_memory. u2 is implementation -> task_state."))

# --- boundary: repo_memory vs service_memory ---

NEW200.append(make_case("v05_batch500_0024",
    rc={"project":"creator-tools","repo":"artisan","service":"asset-compiler","task":"add texture atlas generation"},
    cms=[m("m1","service_memory","The asset compiler bundles individual texture files into texture atlases using a max-rectangle bin-packing algorithm."),
         m("m2","repo_memory","Texture source files live under assets/textures/ and compiled atlases are output to build/atlases/ with a manifest.json index.")],
    cus=[u("u1","The asset compiler must generate mipmap chains for each texture atlas level, downscaling by factors of 2 until the smallest dimension reaches 4 pixels."),
         u("u2","Store the mipmap generation parameters in config/asset_compiler/mipmap.yaml so they can be tuned per target platform.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("repo_memory","u2")], skip=[],
    tags=["read_store_joint","service_invariant","repo_convention","repo_vs_service"],
    notes="u1 defines mipmap generation algorithm -> service_memory (what it does). u2 defines config path -> repo_memory (where config lives). Clean repo_vs_service distinction."))

NEW200.append(make_case("v05_batch500_0025",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"payment-gateway","task":"add support for Buy Now Pay Later"},
    cms=[m("m1","service_memory","The payment gateway tokenizes credit card data via Stripe and stores only the payment token and last 4 digits."),
         m("m2","repo_memory","Payment provider adapters live under src/payment/adapters/ and each implements the PaymentProvider interface.")],
    cus=[u("u1","The payment gateway must support the Klarna BNPL provider by implementing the installment plan selection flow: present available plans, capture user choice, and create the order with the selected plan ID."),
         u("u2","Add the Klarna adapter class in src/payment/adapters/klarna_adapter.py implementing the PaymentProvider interface.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("repo_memory","u2")], skip=[],
    tags=["read_store_joint","service_invariant","repo_convention","repo_vs_service"],
    notes="u1 defines BNPL integration behavior -> service_memory. u2 defines repo file location -> repo_memory."))

NEW200.append(make_case("v05_batch500_0026",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"trigger-manager","task":"add webhook trigger type"},
    cms=[m("m1","service_memory","The trigger manager currently supports cron schedules and message queue triggers for starting workflows."),
         m("m2","repo_memory","Trigger configurations are defined in workflows/<name>/triggers.yaml and support multiple trigger types per workflow.")],
    cus=[u("u1","The trigger manager must accept incoming webhook POST requests, validate the HMAC-SHA256 signature against a configured secret, and start the associated workflow with the webhook body as input context."),
         u("u2","Add the webhook secret configuration to config/triggers/secrets.yaml with per-workflow secret keys.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("repo_memory","u2")], skip=[],
    tags=["read_store_joint","service_invariant","repo_convention","repo_vs_service"],
    notes="u1 defines webhook trigger behavior (validation + workflow start) -> service_memory. u2 defines config storage path -> repo_memory."))

# --- More diverse READ+STORE joint cases ---

NEW200.append(make_case("v05_batch500_0027",
    rc={"project":"finance-dashboard","repo":"finboard","service":"portfolio-tracker","task":"add real-time stock price streaming"},
    cms=[m("m1","service_memory","The portfolio tracker calculates total portfolio value by aggregating positions across accounts and multiplying by the latest cached price."),
         m("m2","repo_memory","Price data is cached in Redis under keys pricedata:<ticker> with the cache TTL defined in config/portfolio/cache.yaml.")],
    cus=[u("u1","The portfolio tracker must subscribe to the exchange's WebSocket price feed and update cached prices within 500ms of receiving a new quote."),
         u("u2","Add the WebSocket price feed client as a new data source adapter in the portfolio tracker's data layer.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines real-time update behavior with latency SLA -> service_memory. u2 is implementation task -> task_state."))

NEW200.append(make_case("v05_batch500_0028",
    rc={"project":"travel-planner","repo":"voyager","service":"loyalty-engine","task":"add tier-based reward multipliers"},
    cms=[m("m1","service_memory","The loyalty engine awards points for completed bookings at a base rate of 1 point per dollar spent."),
         m("m2","project_memory","The voyager loyalty program has three tiers: Silver, Gold, and Platinum, with increasing benefits at each tier.")],
    cus=[u("u1","The loyalty engine must apply a points multiplier based on the member tier: Silver 1.0x, Gold 1.5x, Platinum 2.0x, calculated on the pre-tax booking amount."),
         u("u2","The loyalty program must never allow point redemption for cash equivalents such as gift cards or statement credits.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("project_memory","u2")], skip=[],
    tags=["read_store_joint","service_invariant","project_vs_repo","target_boundary"],
    notes="u1 defines service-level multiplier rule -> service_memory. u2 defines a cross-tier program rule ('never allow') -> project_memory. Shows project_memory vs service_memory on same domain: u1 is per-transaction engine behavior, u2 is a program-wide prohibition."))

NEW200.append(make_case("v05_batch500_0029",
    rc={"project":"customer-support","repo":"helpdesk","service":"sentiment-analyzer","task":"add urgency detection from chat text"},
    cms=[m("m1","service_memory","The sentiment analyzer scores each customer message on a -1.0 to 1.0 sentiment scale and tags messages with detected emotion labels."),
         m("m2","repo_memory","Sentiment model weights are loaded from models/sentiment/bert_finetuned_v2.pt and updated monthly.")],
    cus=[u("u1","The sentiment analyzer must also detect urgency signals: phrases like 'urgent', 'as soon as possible', 'immediately', and all-caps words in messages longer than 10 characters."),
         u("u2","Add an urgency_score field to the sentiment output JSON and expose it in the agent dashboard.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines urgency detection behavior with specific heuristics -> service_memory. u2 is dashboard integration task -> task_state."))

NEW200.append(make_case("v05_batch500_0030",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"code-linker","task":"add bidirectional code-to-docs linking"},
    cms=[m("m1","service_memory","The code linker parses source code comments for @doc annotations and creates hyperlinks from documentation to the referenced code files."),
         m("m2","repo_memory","Code-to-doc mappings are stored in a SQLite database at data/code_links.db with schema version 3.")],
    cus=[u("u1","The code linker must also parse documentation files for @code annotations that reference source files and line ranges, creating bidirectional links."),
         u("u2","Update the link database schema to add a link_direction column with values 'code_to_doc' and 'doc_to_code'.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","repo_convention","repo_vs_service"],
    notes="u1 defines bidirectional linking behavior -> service_memory. u2 is schema update task -> task_state."))

NEW200.append(make_case("v05_batch500_0031",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"case-generator","task":"add batch500 diversity checks"},
    cms=[m("m1","service_memory","The case generator produces JSONL case records following the v0.4 case schema with structural validation."),
         m("m2","project_memory","The v0.5 generation policy requires no templates, no fill-in-the-blank patterns, and unique semantic content per case.")],
    cus=[u("u1","The case generator must reject any generated case whose current_unit text is an exact duplicate of any existing case in the dataset."),
         u("u2","Add a semantic similarity check that flags cases whose unit texts have a cosine similarity above 0.85 with any existing case.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines a hard deduplication rule -> service_memory. u2 defines a fuzzy check (threshold-based) but is an implementation task -> task_state. The distinction: u1 is a definite rule, u2 is a proposed threshold-based check."))

# --- More joint cases to reach 70 target ---

NEW200.append(make_case("v05_batch500_0032",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"chart-renderer","task":"add drill-down from aggregate to detail view"},
    cms=[m("m1","service_memory","The chart renderer generates SVG charts from aggregated query results and supports bar, line, pie, and scatter plot types."),
         m("m2","repo_memory","Chart templates and color palettes are defined in config/charts/ and use a JSON schema validated at render time.")],
    cus=[u("u1","The chart renderer must support drill-down interactions: when a user clicks on an aggregate bar segment, the renderer issues a detail query filtered to that segment's dimensions and renders a sub-chart."),
         u("u2","Add the drill-down query template parameterization so each chart type can define its own detail query pattern.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines drill-down behavior -> service_memory. u2 is template parameterization task -> task_state."))

NEW200.append(make_case("v05_batch500_0033",
    rc={"project":"finance-dashboard","repo":"finboard","service":"risk-analyzer","task":"add Value at Risk calculation"},
    cms=[m("m1","service_memory","The risk analyzer computes position-level risk metrics including beta, Sharpe ratio, and maximum drawdown from daily price history."),
         m("m2","project_memory","The finboard risk module must use the historical simulation method for VaR, not parametric or Monte Carlo, to ensure consistency with the compliance team's methodology.")],
    cus=[u("u1","The risk analyzer must compute 1-day 95% Value at Risk for each portfolio using the historical simulation method on a rolling 252-day window."),
         u("u2","Add the VaR calculation to the daily risk report that is emailed to portfolio managers.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is a project-level methodology constraint -> project_memory. u1 defines VaR computation -> service_memory. u2 is report integration task -> task_state."))

NEW200.append(make_case("v05_batch500_0034",
    rc={"project":"education-platform","repo":"learnhub","service":"plagiarism-checker","task":"add cross-submission similarity detection"},
    cms=[m("m1","service_memory","The plagiarism checker compares each submission against a library of known sources using n-gram fingerprinting with n=5."),
         m("m2","task_state","The current plagiarism check runs only against the public web index, not against other student submissions in the same course.")],
    cus=[u("u1","The plagiarism checker must also compare new submissions against all previous submissions in the same course section using MinHash with 128 permutations and a similarity threshold of 0.6."),
         u("u2","Add the cross-submission index to the plagiarism pipeline and schedule it to run nightly.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines cross-submission detection algorithm with specific parameters -> service_memory. u2 is scheduling task -> task_state."))

NEW200.append(make_case("v05_batch500_0035",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"dialogue-system","task":"add emotion-driven response selection"},
    cms=[m("m1","service_memory","The dialogue system selects NPC responses from a dialogue tree based on player choices and faction reputation scores."),
         m("m2","repo_memory","Dialogue trees are authored in YAML files under content/dialogue/<character_id>/ and support branching, conditions, and variable setting.")],
    cus=[u("u1","The dialogue system must incorporate an NPC emotion model where each NPC has an emotional state vector (anger, fear, joy, trust) that influences which response variant is selected from the dialogue node."),
         u("u2","Add emotion state fields to the NPC character schema and initialize them from the character definition YAML.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines emotion-driven selection algorithm -> service_memory. u2 is schema init task -> task_state."))

NEW200.append(make_case("v05_batch500_0036",
    rc={"project":"mobile-field","repo":"field-app","service":"offline-storage","task":"add conflict-free replicated data type support"},
    cms=[m("m1","service_memory","The offline storage module persists user edits in a local SQLite database and syncs them to the server when connectivity is restored."),
         m("m2","service_memory","The current sync uses last-write-wins conflict resolution, which can silently discard concurrent edits from different devices.")],
    cus=[u("u1","The offline storage module must support a counter CRDT for numeric fields, merging concurrent increments by summing the delta from the last known synchronized value."),
         u("u2","Implement the counter CRDT merge function and add it to the sync conflict resolver as the default strategy for inventory count fields.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines CRDT merge algorithm -> service_memory. u2 is implementation task -> task_state."))

NEW200.append(make_case("v05_batch500_0037",
    rc={"project":"data-platform","repo":"data-jobs","service":"schema-registry","task":"add schema evolution compatibility checks"},
    cms=[m("m1","service_memory","The schema registry stores Avro schemas for all pipeline topics and enforces unique schema IDs per topic."),
         m("m2","project_memory","The data-platform requires BACKWARD compatibility for all schema changes to production topics; FORWARD compatibility is optional for staging.")],
    cus=[u("u1","The schema registry must validate that new schema versions are backward-compatible before accepting them: all fields present in the previous version must exist in the new version with the same or a compatible type."),
         u("u2","Add the compatibility check step to the schema registration API and reject registrations that fail the check with a descriptive error.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is project-level compatibility policy -> project_memory. u1 defines the validation rules -> service_memory. u2 is API implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0038",
    rc={"project":"healthcare-admin","repo":"medflow","service":"prescription-validator","task":"add drug interaction checking"},
    cms=[m("m1","service_memory","The prescription validator checks that prescribed medications have valid NDC codes and that the dosage falls within the recommended range for the patient's age group."),
         m("m2","repo_memory","Drug interaction data is loaded from a monthly updated CSV at data/drug_interactions/ddis_v2026.csv.")],
    cus=[u("u1","The prescription validator must cross-reference new prescriptions against the patient's active medications and flag any interactions with severity 'major' or 'contraindicated' for pharmacist review."),
         u("u2","Add the drug-drug interaction check as a prerequisite step before the prescription is sent to the pharmacy system.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines interaction checking behavior -> service_memory. u2 is workflow integration task -> task_state."))

NEW200.append(make_case("v05_batch500_0039",
    rc={"project":"supply-chain","repo":"logistix","service":"demand-forecaster","task":"add seasonal trend decomposition"},
    cms=[m("m1","service_memory","The demand forecaster predicts daily SKU demand using a moving average of the last 28 days with exponential smoothing (alpha=0.3)."),
         m("m2","repo_memory","Forecast model parameters are stored in config/forecasting/models.yaml and can be overridden per warehouse.")],
    cus=[u("u1","The demand forecaster must decompose the demand signal into trend, seasonal, and residual components using STL decomposition with a seasonal period of 7 days, and forecast using the recomposed trend + seasonal components."),
         u("u2","Add the STL decomposition module and replace the current moving average predictor.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines STL-based forecasting algorithm -> service_memory. u2 is replacement task -> task_state."))

NEW200.append(make_case("v05_batch500_0040",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"redaction-engine","task":"add automatic PII redaction for shared documents"},
    cms=[m("m1","service_memory","The redaction engine applies manual redaction marks defined by attorneys and renders redacted PDFs with black-box overlays."),
         m("m2","project_memory","The clausekeeper project must never automatically delete or modify the original document; redactions are always overlay layers on copies.")],
    cus=[u("u1","The redaction engine must automatically detect and redact Social Security Numbers, dates of birth, and financial account numbers using regex patterns before presenting documents for attorney review."),
         u("u2","Add an auto-redaction review step where detected PII is highlighted and requires attorney confirmation before final redaction.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","sensitive_boundary","project_vs_repo"],
    notes="u1 defines auto-redaction patterns -> service_memory. u2 is review workflow task -> task_state. m2 is project-level policy (no original modification)."))

NEW200.append(make_case("v05_batch500_0041",
    rc={"project":"creator-tools","repo":"artisan","service":"version-control","task":"add branching for collaborative projects"},
    cms=[m("m1","service_memory","The version control system stores project revisions as immutable snapshots referenced by SHA-256 hashes with parent pointers forming a DAG."),
         m("m2","repo_memory","Version history is stored under .artisan/versions/ and the current HEAD pointer is in .artisan/HEAD.")],
    cus=[u("u1","The version control system must support named branches where each branch is a mutable pointer to a revision, and merging a branch creates a new revision with two parent pointers."),
         u("u2","Add branch create, merge, and delete commands to the artisan CLI tool.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines branching/merging semantics -> service_memory. u2 is CLI implementation task -> task_state."))

NEW200.append(make_case("v05_batch500_0042",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"inventory-manager","task":"add warehouse transfer logic"},
    cms=[m("m1","service_memory","The inventory manager tracks stock levels per SKU per warehouse and reserves quantities when orders are placed."),
         m("m2","repo_memory","Warehouse definitions are stored in config/warehouses/ with capacity, address, and operating hours.")],
    cus=[u("u1","The inventory manager must support warehouse-to-warehouse transfers: when a transfer is requested, the source warehouse quantity is decremented immediately and the destination warehouse quantity is incremented only after the transfer is confirmed by warehouse staff."),
         u("u2","Add the transfer status state machine with states: requested, in_transit, received, cancelled.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("service_memory","u2")], skip=[],
    tags=["read_store_joint","service_invariant","repo_vs_service"],
    notes="u1 defines transfer behavior (immediate decrement, confirmed increment) -> service_memory. u2 defines state machine -> service_memory (durable workflow definition)."))

NEW200.append(make_case("v05_batch500_0043",
    rc={"project":"learning-assistant","repo":"tutorai","service":"progress-tracker","task":"add skill mastery estimation"},
    cms=[m("m1","service_memory","The progress tracker logs lesson completions, quiz scores, and time spent per topic to compute a completion percentage."),
         m("m2","task_state","The current progress metric is a simple lesson-completion ratio that does not account for quiz performance or retention.")],
    cus=[u("u1","The progress tracker must estimate skill mastery using a Bayesian Knowledge Tracing model that updates the probability of mastery after each quiz attempt based on correctness and response time."),
         u("u2","Implement the BKT model with the standard 4-parameter variant (guess, slip, initial, transit) using the learner's last 20 quiz attempts per skill.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines BKT-based mastery estimation -> service_memory. u2 is model implementation task -> task_state."))

NEW200.append(make_case("v05_batch500_0044",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"error-handler","task":"add retry with exponential backoff for transient failures"},
    cms=[m("m1","service_memory","The error handler catches step execution failures and either marks the workflow as failed or routes to a compensation handler."),
         m("m2","task_state","The current retry logic is a simple fixed 3-retry loop with no backoff, causing thundering-herd problems when an upstream API is rate-limited.")],
    cus=[u("u1","The error handler must retry failed steps with exponential backoff: 1s, 2s, 4s, 8s, 16s, up to a maximum of 5 retries, with jitter of ±25% to avoid synchronization."),
         u("u2","Add a retry policy configuration per workflow step so that different steps can have different retry strategies.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines retry algorithm -> service_memory. u2 is config task -> task_state."))

NEW200.append(make_case("v05_batch500_0045",
    rc={"project":"customer-support","repo":"helpdesk","service":"macros-engine","task":"add conditional logic to support macros"},
    cms=[m("m1","service_memory","The macros engine lets agents define reusable response templates with variable substitution for customer name, ticket ID, and product."),
         m("m2","repo_memory","Macros are stored as YAML files in config/macros/ and can reference other macros by name.")],
    cus=[u("u1","The macros engine must support if/else conditions based on ticket fields: for example, if ticket.priority == 'critical' include the escalation notice, else include the standard closing."),
         u("u2","Add the conditional block syntax to the macro YAML schema and update the macro renderer to evaluate conditions.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines conditional macro logic -> service_memory. u2 is schema/implementation task -> task_state."))

NEW200.append(make_case("v05_batch500_0046",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"search-index","task":"add faceted search filters"},
    cms=[m("m1","service_memory","The search index builds a full-text index over documentation content and returns results ranked by TF-IDF relevance."),
         m("m2","repo_memory","Index settings including tokenizer, stop words, and boost fields are in config/search/index_settings.json.")],
    cus=[u("u1","The search index must support faceted filtering on document metadata: language, version, product, and content type, where each facet aggregates document counts for the current result set."),
         u("u2","Add the facet aggregation pipeline to the search query handler and expose facet counts in the search API response.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines faceted search behavior -> service_memory. u2 is API implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0047",
    rc={"project":"travel-planner","repo":"voyager","service":"fraud-detector","task":"add booking velocity checks"},
    cms=[m("m1","service_memory","The fraud detector scores each booking attempt on a 0-100 risk scale using rules for IP-geolocation mismatch, unusual device fingerprint, and high-value one-way tickets."),
         m("m2","repo_memory","Fraud rules are configured in config/fraud/rules.yaml with per-rule weight and action (flag, block, review).")],
    cus=[u("u1","The fraud detector must track booking velocity per user account: if an account attempts more than 5 bookings within a 10-minute window, automatically flag all subsequent bookings for manual review."),
         u("u2","Add the velocity tracking counter to the fraud detector's Redis cache with a 10-minute TTL per user.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines velocity check rule -> service_memory. u2 is implementation detail -> task_state."))

# Continue with more READ+STORE joint cases...

NEW200.append(make_case("v05_batch500_0048",
    rc={"project":"finance-dashboard","repo":"finboard","service":"data-validator","task":"add cross-source reconciliation checks"},
    cms=[m("m1","service_memory","The data validator checks that imported data matches the target schema and that numeric columns fall within configured min-max bounds."),
         m("m2","project_memory","The finboard project requires daily reconciliation between the trading system and the accounting ledger before reports are published.")],
    cus=[u("u1","The data validator must perform a cross-source reconciliation by comparing total positions per account from the trading system against the corresponding ledger entries, flagging any discrepancies greater than 0.01%."),
         u("u2","Add the reconciliation check as a scheduled job that runs at 06:00 UTC before the daily report generation.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is a project-level reconciliation requirement -> project_memory. u1 defines reconciliation logic -> service_memory. u2 is scheduling task -> task_state."))

NEW200.append(make_case("v05_batch500_0049",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"label-auditor","task":"add automated target-boundary checks"},
    cms=[m("m1","service_memory","The label auditor runs structural validation on case records and reports any schema violations."),
         m("m2","project_memory","v0.5 data policy requires that all 'Add/Implement/Build' phrasing defaults to task_state unless durable behavior dominates.")],
    cus=[u("u1","The label auditor must flag cases where a unit begins with 'Add', 'Implement', or 'Build' but is labeled service_memory, for human review of the label."),
         u("u2","Add the action-verb detection regex to the label auditor's rule set and generate a warning report for each flagged case.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines flagging rule -> service_memory. u2 is implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0050",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"dashboard-builder","task":"add custom metric formulas"},
    cms=[m("m1","service_memory","The dashboard builder renders widgets from saved queries and supports drag-and-drop layout with resizable panels."),
         m("m2","repo_memory","Dashboard definitions are stored as JSON in dashboards/<dashboard_id>.json with widget and layout sections.")],
    cus=[u("u1","The dashboard builder must support custom metric formulas where a widget's value is computed as an arithmetic expression over other widget values on the same dashboard, such as (widget_a - widget_b) / widget_c."),
         u("u2","Add the formula parser that evaluates expressions with widget ID references and standard arithmetic operators.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines formula widget capability -> service_memory. u2 is parser implementation -> task_state."))

# READ+STORE joint 51-70: More diverse tag coverage

NEW200.append(make_case("v05_batch500_0051",
    rc={"project":"education-platform","repo":"learnhub","service":"course-builder","task":"add prerequisite chaining validation"},
    cms=[m("m1","service_memory","The course builder allows instructors to define course modules, lessons, and quizzes with ordering constraints."),
         m("m2","task_state","The current prerequisite system only supports direct prerequisites, not transitive chains.")],
    cus=[u("u1","The course builder must validate the prerequisite graph for cycles before publishing a course, rejecting any configuration where course A requires B which requires A."),
         u("u2","Add cycle detection using depth-first search to the course validation pipeline.")],
    read=["m1"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state","stale_memory"],
    notes="u1 defines cycle detection rule -> service_memory. u2 is implementation -> task_state. m2 is stale limitation context."))

NEW200.append(make_case("v05_batch500_0052",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"animation-blender","task":"add inverse kinematics for character feet"},
    cms=[m("m1","service_memory","The animation blender interpolates between animation clips using blend trees parameterized by character speed and direction."),
         m("m2","repo_memory","Animation clip data is stored under assets/animations/ in the studio's custom .ganim format.")],
    cus=[u("u1","The animation blender must apply two-bone inverse kinematics to character feet during locomotion animations, keeping the feet planted on the ground when the character moves over uneven terrain."),
         u("u2","Add the IK solver as a post-processing step in the animation pipeline after the blend tree evaluation.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines IK behavior -> service_memory. u2 is pipeline integration -> task_state."))

NEW200.append(make_case("v05_batch500_0053",
    rc={"project":"customer-support","repo":"helpdesk","service":"sla-monitor","task":"add breach prediction alerts"},
    cms=[m("m1","service_memory","The SLA monitor tracks ticket response and resolution times against configured SLA targets and sends breach alerts when a target is exceeded."),
         m("m2","repo_memory","SLA definitions per priority and customer tier are in config/sla/targets.yaml.")],
    cus=[u("u1","The SLA monitor must predict SLA breaches 30 minutes before they occur by extrapolating the current ticket handling rate against the remaining time, and alert the team lead."),
         u("u2","Add the predictive alert module that uses linear regression on the last hour of response times to estimate the breach time.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines predictive SLA monitoring -> service_memory. u2 is implementation method -> task_state."))

NEW200.append(make_case("v05_batch500_0054",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"recommendation-engine","task":"add collaborative filtering model"},
    cms=[m("m1","service_memory","The recommendation engine currently uses content-based filtering by comparing product attributes (category, price range, tags) to user purchase history."),
         m("m2","repo_memory","Recommendation model weights are stored in models/recommendations/ and loaded at service startup.")],
    cus=[u("u1","The recommendation engine must add collaborative filtering using matrix factorization with 50 latent factors, trained on the user-item purchase matrix with alternating least squares."),
         u("u2","Train the collaborative filtering model on the last 12 months of purchase data and evaluate with RMSE on a 10% holdout set.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines recommendation algorithm -> service_memory. u2 is training/evaluation task -> task_state."))

NEW200.append(make_case("v05_batch500_0055",
    rc={"project":"data-platform","repo":"data-jobs","service":"partition-manager","task":"add automatic partition archival"},
    cms=[m("m1","service_memory","The partition manager creates date-partitioned tables and manages retention by dropping partitions older than the retention period."),
         m("m2","project_memory","The data-platform requires that archived data be stored in cold storage for 7 years before permanent deletion for compliance.")],
    cus=[u("u1","The partition manager must archive partitions to cold storage before dropping them, by exporting the partition data to compressed Parquet files in the archive bucket with the naming pattern <table>/<partition>/data.parquet."),
         u("u2","Add the archive-before-drop step to the partition retention job and verify archive integrity before dropping.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is compliance retention policy -> project_memory. u1 defines archival behavior -> service_memory. u2 is implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0056",
    rc={"project":"mobile-field","repo":"field-app","service":"push-notifier","task":"add notification grouping by topic"},
    cms=[m("m1","service_memory","The push notifier sends individual notifications to devices and tracks delivery status with receipts."),
         m("m2","repo_memory","Notification templates and channel configurations are in config/notifications/channels.yaml.")],
    cus=[u("u1","The push notifier must group notifications by topic within a 30-minute window: instead of sending 5 separate alerts for the same project update, it sends one summary notification with a count badge."),
         u("u2","Add the notification grouping buffer that accumulates notifications per topic and flushes when the window expires or the buffer reaches 10 messages.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines grouping behavior -> service_memory. u2 is buffer implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0057",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"task-dispatcher","task":"add priority-based task assignment"},
    cms=[m("m1","service_memory","The task dispatcher assigns workflow tasks to workers from a shared queue using round-robin distribution."),
         m("m2","task_state","The current task queue has no concept of priority; all tasks are treated equally regardless of the workflow's SLA tier.")],
    cus=[u("u1","The task dispatcher must support 3 priority levels (high, normal, low) where high-priority tasks are always dispatched before normal, and low-priority tasks are only dispatched when the queue has no high or normal tasks pending."),
         u("u2","Add the priority field to the task schema and update the dispatching algorithm to check priority before round-robin selection.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines priority dispatching algorithm -> service_memory. u2 is schema/implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0058",
    rc={"project":"healthcare-admin","repo":"medflow","service":"lab-results-processor","task":"add abnormal result flagging"},
    cms=[m("m1","service_memory","The lab results processor ingests HL7 ORU messages, extracts test results with reference ranges, and stores them in the patient record."),
         m("m2","repo_memory","Reference ranges per test are configured in config/lab/reference_ranges.yaml and updated when the lab changes its equipment.")],
    cus=[u("u1","The lab results processor must flag any result that falls outside its reference range as 'abnormal' and, if the deviation exceeds 3 standard deviations, flag it as 'critical' requiring immediate provider review."),
         u("u2","Add the critical result notification that sends an SMS alert to the ordering provider when a critical result is flagged.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines result flagging rules with thresholds -> service_memory. u2 is notification implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0059",
    rc={"project":"supply-chain","repo":"logistix","service":"warehouse-allocator","task":"add zone-based picking optimization"},
    cms=[m("m1","service_memory","The warehouse allocator assigns incoming orders to warehouse zones based on inventory availability and proximity to the shipping dock."),
         m("m2","repo_memory","Warehouse zone maps are defined in config/warehouses/<id>/zone_map.geojson with shelf coordinates.")],
    cus=[u("u1","The warehouse allocator must optimize picking routes by grouping order lines by zone and sequencing zones to minimize travel distance, using a nearest-neighbor heuristic starting from the pack station."),
         u("u2","Implement the zone-sequencing algorithm and integrate it with the existing order assignment pipeline.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines zone-based optimization -> service_memory. u2 is implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0060",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"expiry-tracker","task":"add contract renewal forecasting"},
    cms=[m("m1","service_memory","The expiry tracker monitors contract end dates and sends notifications 90, 60, and 30 days before expiration."),
         m("m2","project_memory","The clausekeeper project does not initiate contract renewals; it only notifies responsible parties of upcoming expirations.")],
    cus=[u("u1","The expiry tracker must forecast renewal probability based on historical renewal rates by contract type and client industry, using a logistic regression model updated monthly."),
         u("u2","Add the renewal probability score to the contract dashboard and color-code contracts with low renewal probability.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is project scope limitation -> project_memory. u1 defines forecasting model -> service_memory. u2 is dashboard integration -> task_state."))

NEW200.append(make_case("v05_batch500_0061",
    rc={"project":"creator-tools","repo":"artisan","service":"export-manager","task":"add multi-format export with color profile conversion"},
    cms=[m("m1","service_memory","The export manager renders project files to PNG and JPEG formats at configurable resolutions."),
         m("m2","repo_memory","Export presets are stored in config/export/presets.yaml with format, resolution, and quality settings.")],
    cus=[u("u1","The export manager must support color profile conversion between sRGB, Adobe RGB, and Display P3, applying the destination profile after rendering but before encoding."),
         u("u2","Add the ICC profile embedding step so exported files include the color profile metadata in the file header.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines color profile conversion behavior -> service_memory. u2 is metadata embedding -> task_state."))

NEW200.append(make_case("v05_batch500_0062",
    rc={"project":"learning-assistant","repo":"tutorai","service":"content-adaptor","task":"add reading level adjustment"},
    cms=[m("m1","service_memory","The content adaptor serves study materials at the learner's configured difficulty level: beginner, intermediate, or advanced."),
         m("m2","user_profile","The user prefers study materials in British English spelling with metric units for all measurements.")],
    cus=[u("u1","The content adaptor must dynamically adjust the reading level of text passages by simplifying vocabulary and sentence structure when the learner's comprehension score drops below 70% on a topic."),
         u("u2","Add the Flesch-Kincaid readability scorer to evaluate text difficulty before and after simplification.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","user_profile_boundary","service_vs_task_state"],
    notes="u1 defines dynamic reading level adjustment -> service_memory. u2 is scoring implementation -> task_state. m2 is user_profile (British English preference)."))

NEW200.append(make_case("v05_batch500_0063",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"alert-manager","task":"add anomaly-based alert triggers"},
    cms=[m("m1","service_memory","The alert manager triggers notifications when a metric crosses a static threshold for a configurable duration."),
         m("m2","repo_memory","Alert rules are defined in config/alerts/rules.yaml and support comparison operators gt, lt, gte, lte.")],
    cus=[u("u1","The alert manager must support anomaly-based alerting where the trigger condition is 'value is outside 2 standard deviations of the rolling 7-day mean at the same hour', replacing static thresholds for seasonal metrics."),
         u("u2","Add the rolling statistics calculator that maintains a 168-hour window (7 days × 24 hours) for each metric.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines anomaly-based alerting -> service_memory. u2 is statistics implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0064",
    rc={"project":"travel-planner","repo":"voyager","service":"check-in","task":"add automated check-in with seat preference"},
    cms=[m("m1","service_memory","The check-in service submits passenger details to airline APIs and retrieves boarding passes 24 hours before departure."),
         m("m2","user_profile","The user prefers aisle seats in the front half of the aircraft for flights longer than 3 hours.")],
    cus=[u("u1","The check-in service must automatically select the best available seat matching the user's preferences, falling back to any aisle seat then any window seat."),
         u("u2","Add the seat preference scoring function that ranks available seats by proximity to the user's ideal seat type and cabin zone.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","user_profile_boundary","service_vs_task_state"],
    notes="u1 defines auto seat selection behavior -> service_memory. u2 is implementation -> task_state. m2 is user_profile for seat preference."))

NEW200.append(make_case("v05_batch500_0065",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"distribution-reporter","task":"add per-tag store-target breakdown"},
    cms=[m("m1","service_memory","The distribution reporter computes STORE target counts and percentages from a batch of case records."),
         m("m2","repo_memory","Distribution reports are written to reports/v05/ with the naming pattern v05_batch<N>_data_report.md.")],
    cus=[u("u1","The distribution reporter must generate a cross-tabulation: for each tag, show the count and percentage of STORE units per target, so we can see which tags correlate with which targets."),
         u("u2","Add the cross-tabulation table to the data report template in the reports section.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","repo_convention","repo_vs_service"],
    notes="u1 defines cross-tabulation feature -> service_memory. u2 is report template update -> task_state."))

NEW200.append(make_case("v05_batch500_0066",
    rc={"project":"customer-support","repo":"helpdesk","service":"knowledge-base","task":"add article effectiveness scoring"},
    cms=[m("m1","service_memory","The knowledge base serves help articles to both agents and customers, with articles tagged by product, topic, and difficulty."),
         m("m2","repo_memory","Knowledge base articles live under content/kb/<product>/<article_id>.md with frontmatter metadata.")],
    cus=[u("u1","The knowledge base must score article effectiveness by tracking whether a ticket is resolved within 24 hours after the article was linked, and de-prioritizing articles with an effectiveness score below 0.3 in search results."),
         u("u2","Add the article resolution tracking that links help article IDs to ticket resolution events in the analytics pipeline.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines article scoring algorithm -> service_memory. u2 is tracking implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0067",
    rc={"project":"finance-dashboard","repo":"finboard","service":"compliance-checker","task":"add insider trading surveillance rules"},
    cms=[m("m1","service_memory","The compliance checker scans trading activity for patterns that match regulatory rules, including wash sales and front-running."),
         m("m2","project_memory","The finboard compliance module must flag all trades executed within 48 hours of a material event announcement for review, per company policy.")],
    cus=[u("u1","The compliance checker must detect trades executed by employees in a security within 30 days before an earnings announcement, flagging them as potential insider trading for the compliance officer."),
         u("u2","Add the earnings-announcement calendar integration so the checker can cross-reference trade dates against announcement dates.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is company-wide policy -> project_memory. u1 defines detection rule -> service_memory. u2 is integration task -> task_state."))

NEW200.append(make_case("v05_batch500_0068",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"translator","task":"add glossary-enforced terminology translation"},
    cms=[m("m1","service_memory","The translator converts documentation pages from English to target languages using a neural MT model fine-tuned on technical documentation."),
         m("m2","repo_memory","Translation glossaries are stored in data/glossaries/<lang>.json and contain domain-specific term mappings.")],
    cus=[u("u1","The translator must enforce glossary terms during translation by post-processing the MT output and replacing any detected source term with its glossary-mapped translation, regardless of the model's choice."),
         u("u2","Add the glossary post-processor as a pipeline step between MT inference and the final rendered page.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines glossary enforcement behavior -> service_memory. u2 is pipeline integration -> task_state."))

NEW200.append(make_case("v05_batch500_0069",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"order-fulfillment","task":"add partial shipment support"},
    cms=[m("m1","service_memory","The order fulfillment system currently treats orders as atomic: all items must be in stock at one warehouse before the order can ship."),
         m("m2","repo_memory","Fulfillment rules including warehouse priority and shipping method are configured in config/fulfillment/rules.yaml.")],
    cus=[u("u1","The order fulfillment system must support partial shipments: when an order contains items split across multiple warehouses, ship each subset as it becomes available with its own tracking number, and update the order status to 'partially_shipped'."),
         u("u2","Add the partial shipment state machine that tracks each sub-shipment independently while maintaining the parent order status.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("service_memory","u2")], skip=[],
    tags=["read_store_joint","service_invariant","repo_vs_service"],
    notes="u1 defines partial shipment behavior -> service_memory. u2 defines sub-shipment state machine -> service_memory. Both are durable fulfillment behaviors."))

NEW200.append(make_case("v05_batch500_0070",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"training-logger","task":"add per-epoch target distribution logging during training"},
    cms=[m("m1","service_memory","The training logger records loss, learning rate, and gradient norm at each training step to TensorBoard."),
         m("m2","project_memory","The v0.5 evaluation philosophy prioritizes routing-specific metrics (STORE target accuracy, false store rate) over cross-entropy loss.")],
    cus=[u("u1","The training logger must compute and log the distribution of predicted STORE targets per epoch to detect target collapse early: if any target falls below 2% of predictions for 3 consecutive epochs, halt training."),
         u("u2","Add the target distribution histogram to the TensorBoard logging callback.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="u1 defines target collapse detection rule -> service_memory. u2 is implementation -> task_state. m2 is project philosophy context."))

# ── STORE/SKIP-only (78 cases) ─────────────────────────────────────────────

# === service_memory dominant ===

NEW200.append(make_case("v05_batch500_0071",
    rc={"project":"customer-support","repo":"helpdesk","service":"auto-responder","task":"define auto-response rules"},
    cms=[],
    cus=[u("u1","The auto-responder must send an immediate acknowledgement for tickets submitted via email, including the ticket ID and expected response time based on priority."),
         u("u2","The auto-responder must never include the agent's personal email or direct phone number in automated responses."),
         u("u3","Set up the auto-response template for the new European support queue.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","repo_vs_service"],
    notes="u1 defines auto-response behavior -> service_memory. u2 defines a privacy/security rule -> service_memory (durable constraint on auto-responder). u3 is setup task -> task_state."))

NEW200.append(make_case("v05_batch500_0072",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"query-optimizer","task":"define query cost estimation rules"},
    cms=[],
    cus=[u("u1","The query optimizer must estimate the cost of each query before execution by counting the number of rows scanned based on table statistics."),
         u("u2","Query execution schedules and off-peak window configurations are stored in config/query_optimizer/schedule.yaml."),
         u("u3","Run the query cost estimator on the top 20 slowest queries from last week.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines cost estimation -> service_memory. u2 defines schedule config path -> repo_memory. u3 is current diagnostic task -> task_state."))

NEW200.append(make_case("v05_batch500_0073",
    rc={"project":"healthcare-admin","repo":"medflow","service":"billing-coder","task":"define ICD-10 coding rules"},
    cms=[],
    cus=[u("u1","The billing coder must map diagnosis descriptions to ICD-10-CM codes using exact match on the SNOMED-CT crosswalk and fuzzy matching for unmapped terms."),
         u("u2","The SNOMED-CT to ICD-10-CM crosswalk file is stored at data/coding/crosswalk_snomed_icd10.csv and updated annually."),
         u("u3","The billing-coder currently uses the 2025 crosswalk; updating to the 2026 crosswalk is required before the next compliance audit.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines coding algorithm -> service_memory. u2 defines data file path -> repo_memory. u3 describes current update task -> task_state."))

NEW200.append(make_case("v05_batch500_0074",
    rc={"project":"supply-chain","repo":"logistix","service":"quality-inspector","task":"define defect classification criteria"},
    cms=[],
    cus=[u("u1","The quality inspector must classify received goods into grades A, B, C, or reject based on the count and severity of defects found during sampling."),
         u("u2","Defect grade thresholds per product category are stored in config/quality/defect_thresholds.yaml and reviewed annually."),
         u("u3","The quality inspector currently only samples 5% of incoming shipments; increasing to 10% for high-risk suppliers is under discussion.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines classification framework -> service_memory. u2 defines config path -> repo_memory. u3 describes current process and proposed change -> task_state."))

NEW200.append(make_case("v05_batch500_0075",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"risk-scorer","task":"define contract risk scoring methodology"},
    cms=[],
    cus=[u("u1","The risk scorer must evaluate each contract clause against a library of risky language patterns and assign a risk score from 0 to 100."),
         u("u2","Risk pattern definitions and score weights are stored in config/risk/patterns.yaml and reviewed quarterly by the legal team."),
         u("u3","The risk scorer currently uses a static pattern library from 2025; adding the new 2026 regulatory risk patterns is planned for this month.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines risk scoring -> service_memory. u2 defines config path -> repo_memory. u3 describes update plan -> task_state."))

NEW200.append(make_case("v05_batch500_0076",
    rc={"project":"creator-tools","repo":"artisan","service":"font-renderer","task":"define font fallback behavior"},
    cms=[],
    cus=[u("u1","The font renderer must implement a font fallback chain: when a glyph is missing in the primary font, the renderer checks secondary, then tertiary fonts in order."),
         u("u2","Font fallback chain configurations per script are stored in config/fonts/fallback_chains.json."),
         u("u3","The font renderer currently only supports Latin and CJK scripts; adding Arabic and Devanagari fallback chains is planned for the internationalization release.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines fallback behavior -> service_memory. u2 defines config path -> repo_memory. u3 describes current scope and plan -> task_state."))

# === task_state dominant ===

NEW200.append(make_case("v05_batch500_0077",
    rc={"project":"mobile-field","repo":"field-app","service":"crash-reporter","task":"plan crash reporter improvements"},
    cms=[],
    cus=[u("u1","The crash reporter currently captures stack traces but does not include the last 50 application log lines before the crash."),
         u("u2","Next, add a circular log buffer that keeps the last 200 log lines in memory and attaches them to crash reports."),
         u("u3","After the log buffer is implemented, add breadcrumb events for navigation and network calls.")],
    read=[], store=[st("task_state","u1"),st("task_state","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","task_progress","service_vs_task_state"],
    notes="u1 describes current limitation -> task_state. u2 is next implementation step -> task_state. u3 is future plan -> task_state. All correctly task_state: these describe progress/plans, not durable behaviors."))

NEW200.append(make_case("v05_batch500_0078",
    rc={"project":"data-platform","repo":"data-jobs","service":"data-lake","task":"plan data lake migration"},
    cms=[],
    cus=[u("u1","The data lake is currently on AWS S3 with data organized by source system in separate prefixes."),
         u("u2","The migration to GCS is blocked until the IAM cross-cloud access role is approved by the security team."),
         u("u3","After the migration, update all pipeline configurations to point to the new GCS bucket paths.")],
    read=[], store=[st("task_state","u1"),st("task_state","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","task_progress","service_vs_task_state"],
    notes="u1 is current architecture state -> task_state. u2 is current blocker -> task_state. u3 is post-migration task -> task_state. All transient migration-related state."))

NEW200.append(make_case("v05_batch500_0079",
    rc={"project":"education-platform","repo":"learnhub","service":"student-portal","task":"update student dashboard for new semester"},
    cms=[],
    cus=[u("u1","The student dashboard currently shows enrolled courses and grades from the previous semester only."),
         u("u2","Before the fall semester launch, add the course registration widget and the financial aid status panel."),
         u("u3","The registration widget should pull course availability from the enrollment service in real time.")],
    read=[], store=[st("task_state","u1"),st("task_state","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","task_progress","service_vs_task_state"],
    notes="u1 is current state -> task_state. u2 is task with deadline -> task_state. u3 describes implementation approach -> task_state. u3 mentions 'should' suggesting it's an active design choice, not yet settled, so task_state is appropriate."))

NEW200.append(make_case("v05_batch500_0080",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"scheduler","task":"migrate from cron to event-driven scheduling"},
    cms=[],
    cus=[u("u1","The scheduler currently uses cron expressions for all workflow triggers, which causes delays of up to 59 seconds."),
         u("u2","Migrate the top 10 most frequent workflows to event-driven triggers using the message queue."),
         u("u3","The remaining 40 low-frequency workflows can stay on cron until the next quarter.")],
    read=[], store=[st("task_state","u1"),st("task_state","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","task_progress","service_vs_task_state"],
    notes="u1 describes current limitation -> task_state. u2 is migration plan -> task_state. u3 is deferral decision -> task_state. All are about the current migration effort."))

NEW200.append(make_case("v05_batch500_0081",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"build-system","task":"optimize build times for console certification"},
    cms=[],
    cus=[u("u1","The current full build takes 45 minutes, and console certification requires 3 clean builds per submission."),
         u("u2","For this certification round, add distributed shader compilation across the 4 build machines to reduce build time."),
         u("u3","The build optimization is only needed for the certification submission; after passing, revert to the standard build process.")],
    read=[], store=[st("task_state","u1"),st("task_state","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","task_progress","temporary_request","service_vs_task_state"],
    notes="u1 is current state -> task_state. u2 is current plan -> task_state. u3 explicitly states this is temporary -> task_state (but also temporary_request tag). Shows that even service-domain topics can be task_state when explicitly temporary."))

# === repo_memory dominant ===

NEW200.append(make_case("v05_batch500_0082",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"ci-pipeline","task":"set up CI for v0.5 batch validation"},
    cms=[],
    cus=[u("u1","All v0.5 batch JSONL files must be validated by the CI pipeline on every push using the command: python src/v04/case_validator.py --input <file>."),
         u("u2","CI validation reports should be written to ci_reports/v05/ with the naming pattern <batch>_validation_<timestamp>.json."),
         u("u3","The CI pipeline must fail the build if any case validation fails or if SFT assistant content does not match gold.dsl.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is CI command convention -> repo_memory. u2 is CI output path convention -> repo_memory. u3 is CI rule -> repo_memory (pipeline configuration rule). All are repo-level operational conventions."))

NEW200.append(make_case("v05_batch500_0083",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"testing","task":"define e2e test conventions"},
    cms=[],
    cus=[u("u1","End-to-end tests must run against a Docker Compose environment defined in docker-compose.test.yaml, never against staging or production."),
         u("u2","E2E test fixtures for the checkout flow are in tests/e2e/fixtures/checkout/ and use the Factory pattern to create test orders."),
         u("u3","All e2e tests must pass before merging to the main branch; the merge hook is configured in .github/workflows/e2e.yml.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is test environment convention -> repo_memory. u2 is test fixture path -> repo_memory. u3 is CI merge rule -> repo_memory. All repo-level conventions."))

NEW200.append(make_case("v05_batch500_0084",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"release","task":"document release process conventions"},
    cms=[],
    cus=[u("u1","The release process requires a CHANGELOG.md entry under the Unreleased section, then moved to the version section on release day."),
         u("u2","Release tags must follow semantic versioning and be annotated with git tag -a v<major>.<minor>.<patch> -m 'Release <version>'."),
         u("u3","The release Docker image is built from Dockerfile.release and pushed to the container registry with the version tag.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is changelog convention -> repo_memory. u2 is git tag convention -> repo_memory. u3 is Docker build convention -> repo_memory. All repo-level operational standards."))

NEW200.append(make_case("v05_batch500_0085",
    rc={"project":"finance-dashboard","repo":"finboard","service":"deployment","task":"define deployment conventions"},
    cms=[],
    cus=[u("u1","Deployments to staging happen automatically on merge to develop; deployments to production require manual approval in the GitHub deployment dashboard."),
         u("u2","The Kubernetes deployment manifests are in k8s/overlays/<env>/ and use Kustomize for environment-specific patches."),
         u("u3","Database migrations must be applied before deploying new application code; the migration runner image is finboard/migrations:v2.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is deployment workflow -> repo_memory. u2 is k8s path convention -> repo_memory. u3 is migration order rule -> repo_memory. All repo-level operational conventions."))

NEW200.append(make_case("v05_batch500_0086",
    rc={"project":"travel-planner","repo":"voyager","service":"monitoring","task":"set up monitoring dashboards"},
    cms=[],
    cus=[u("u1","Prometheus metrics for all voyager services are exposed on port 9090 at the /metrics endpoint and scraped every 30 seconds."),
         u("u2","Grafana dashboards for the voyager project are stored in grafana/dashboards/ and imported via the Grafana provisioning API."),
         u("u3","Alert rules for production are defined in prometheus/rules/alerts.yml and must not be modified without review by the on-call rotation.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is monitoring port convention -> repo_memory. u2 is Grafana path -> repo_memory. u3 is alert rule convention -> repo_memory."))

# === project_memory dominant ===

NEW200.append(make_case("v05_batch500_0087",
    rc={"project":"healthcare-admin","repo":"medflow","service":"architecture","task":"define project-wide security policy"},
    cms=[],
    cus=[u("u1","All medflow services must encrypt data in transit using TLS 1.3 with cipher suites approved by the security team."),
         u("u2","The medflow project must never store patient health information in logs or error messages; PHI must be redacted before logging."),
         u("u3","Every medflow service must expose a /health endpoint that returns 200 only when all dependencies are reachable.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("project_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","target_boundary"],
    notes="u1 is cross-service security rule ('all medflow services') -> project_memory. u2 is cross-service logging prohibition -> project_memory. u3 is cross-service convention -> project_memory. All explicitly project-wide."))

NEW200.append(make_case("v05_batch500_0088",
    rc={"project":"supply-chain","repo":"logistix","service":"compliance","task":"define project data retention policy"},
    cms=[],
    cus=[u("u1","The logistix project must retain inventory transaction records for 7 years and shipment records for 3 years, per the corporate data retention schedule."),
         u("u2","After the retention period, data must be anonymized by replacing customer names with hash values before archival."),
         u("u3","The project's data retention policy applies to all services including warehouse, routing, and forecasting.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("project_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","target_boundary"],
    notes="u1 is project-level retention policy -> project_memory. u2 is project-level anonymization rule -> project_memory. u3 explicitly states cross-service application -> project_memory."))

NEW200.append(make_case("v05_batch500_0089",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"governance","task":"define project access control policy"},
    cms=[],
    cus=[u("u1","The clausekeeper project enforces role-based access: attorneys have read-write access to all documents, paralegals have read-write to assigned clients only, and auditors have read-only global access."),
         u("u2","All access to client documents must be logged with the user ID, document ID, action, and timestamp for audit purposes."),
         u("u3","The clausekeeper project does not support external client access; all users must be employees of the firm.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("project_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","target_boundary"],
    notes="u1 is project-wide RBAC policy -> project_memory. u2 is project-wide audit logging rule -> project_memory. u3 is project scope limitation -> project_memory. All project-level governance."))

NEW200.append(make_case("v05_batch500_0090",
    rc={"project":"creator-tools","repo":"artisan","service":"standards","task":"define project code standards"},
    cms=[],
    cus=[u("u1","The artisan project requires all Python code to pass pylint with a minimum score of 8.0 and all JavaScript code to pass ESLint with the project's .eslintrc.json."),
         u("u2","All public API endpoints must be documented using OpenAPI 3.0 specifications stored in docs/api/<service>.yaml."),
         u("u3","The project uses the MIT license for all open-source components and requires a CLA for external contributions.")],
    read=[], store=[st("project_memory","u1"),st("project_memory","u2"),st("project_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","target_boundary"],
    notes="u1 is project-wide linting standard -> project_memory. u2 is project-wide API doc requirement -> project_memory. u3 is project licensing policy -> project_memory."))

# === sensitive_boundary STORE/SKIP-only ===

NEW200.append(make_case("v05_batch500_0091",
    rc={"project":"customer-support","repo":"helpdesk","service":"ticket-system","task":"record ticket data handling rules"},
    cms=[],
    cus=[u("u1","The ticket system must redact government ID numbers from ticket descriptions before storing the ticket in the database."),
         u("u2","A customer included their driver's license number DL-9582-3314-7761 in the ticket body for identity verification."),
         u("u3","All customer PII in tickets must be encrypted at rest using AES-256 with keys managed by the central KMS.")],
    read=[], store=[st("service_memory","u1"),st("project_memory","u3")], skip=["u2"],
    tags=["store_skip_only","service_invariant","sensitive_boundary","project_vs_repo"],
    notes="u1 is a service-specific redaction rule -> service_memory. u2 contains a synthetic driver's license number -> must SKIP. u3 is cross-service encryption requirement -> project_memory."))

NEW200.append(make_case("v05_batch500_0092",
    rc={"project":"finance-dashboard","repo":"finboard","service":"account-service","task":"record account security rules"},
    cms=[],
    cus=[u("u1","The account service must never return full account numbers in API responses; only the last 4 digits may be displayed."),
         u("u2","A user submitted a support request with their full bank account number: 98765432109876."),
         u("u3","Failed login attempts must be rate-limited: 5 attempts per username per 15 minutes, then a 30-minute lockout.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u3")], skip=["u2"],
    tags=["store_skip_only","service_invariant","sensitive_boundary"],
    notes="u1 is data masking rule -> service_memory. u2 contains a synthetic bank account number -> must SKIP. u3 is rate-limiting behavior -> service_memory."))

NEW200.append(make_case("v05_batch500_0093",
    rc={"project":"healthcare-admin","repo":"medflow","service":"patient-api","task":"record patient data privacy rules"},
    cms=[],
    cus=[u("u1","The patient API must return de-identified data when the caller does not have the 'PHI_READ' scope in their OAuth token."),
         u("u2","The test patient record has SSN 123-45-6789 and date of birth 1965-03-21."),
         u("u3","All PHI access must be logged to the audit trail with the requesting user, patient ID, fields accessed, and timestamp.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u3")], skip=["u2"],
    tags=["store_skip_only","service_invariant","sensitive_boundary"],
    notes="u1 is de-identification rule -> service_memory. u2 contains SSN and DOB -> must SKIP. u3 is audit logging behavior -> service_memory."))

# === user_profile STORE/SKIP-only ===

NEW200.append(make_case("v05_batch500_0094",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"user-preferences","task":"record user display preferences"},
    cms=[],
    cus=[u("u1","I prefer dashboard charts to use a dark theme with the 'Nord' color palette instead of the default light theme."),
         u("u2","I want to receive weekly digest emails on Monday mornings instead of daily metric alerts."),
         u("u3","My login password for the staging dashboard is metricboard_stage_2026!")],
    read=[], store=[st("user_profile","u1"),st("user_profile","u2")], skip=["u3"],
    tags=["store_skip_only","user_profile_boundary","sensitive_boundary"],
    notes="u1 is a stable display preference -> user_profile. u2 is a stable notification preference -> user_profile. u3 is a password -> must SKIP."))

NEW200.append(make_case("v05_batch500_0095",
    rc={"project":"learning-assistant","repo":"tutorai","service":"study-planner","task":"record study preference"},
    cms=[],
    cus=[u("u1","I prefer to study new topics by reading the summary first, then diving into detailed sections, and finishing with the quiz."),
         u("u2","I want the platform to automatically schedule study sessions at 7:00 PM local time on weekdays."),
         u("u3","My personal email for account recovery is tutorai_user_2026@personal.example.com.")],
    read=[], store=[st("user_profile","u1"),st("user_profile","u2")], skip=["u3"],
    tags=["store_skip_only","user_profile_boundary","sensitive_boundary"],
    notes="u1 is learning style preference -> user_profile. u2 is scheduling preference -> user_profile. u3 is a personal email address -> must SKIP."))

# === SoP / skill out-of-scope STORE/SKIP-only ===

NEW200.append(make_case("v05_batch500_0096",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"documentation","task":"discuss skill system addition"},
    cms=[],
    cus=[u("u1","The project scope explicitly excludes retriever training, writer training, and MemoryOS implementation."),
         u("u2","We should create a reusable skill system for SOPs that agents can invoke during complex multi-step operations."),
         u("u3","The documentation for exclusion decisions lives under docs/v05/scope_exclusions.md.")],
    read=[], store=[st("project_memory","u1")], skip=["u2","u3"],
    tags=["store_skip_only","project_vs_repo","sop_skill_out_of_scope","target_boundary"],
    notes="u1 is project scope exclusion -> project_memory. u2 proposes a skill system (explicitly out of scope for v0.5 per training plan) -> SKIP. u3 is a documentation path suggestion but phrased as something that should exist (not a settled decision) -> SKIP."))

NEW200.append(make_case("v05_batch500_0097",
    rc={"project":"data-platform","repo":"data-jobs","service":"architecture","task":"discuss entity resolution addition"},
    cms=[],
    cus=[u("u1","Maybe we should add entity resolution to deduplicate customer records across the CRM and billing systems."),
         u("u2","The data-platform currently has no entity resolution capability and it is not in the current quarter's roadmap."),
         u("u3","The roadmap document is tracked in docs/planning/roadmap_2026_Q3.md.")],
    read=[], store=[st("task_state","u2")], skip=["u1","u3"],
    tags=["store_skip_only","sop_skill_out_of_scope","task_progress","service_vs_task_state"],
    notes="u1 is speculative ('Maybe we should') -> SKIP. u2 describes current state -> task_state. u3 is a document reference but not a durable convention -> SKIP (casual reference)."))

# === More diverse STORE/SKIP-only cases ===

NEW200.append(make_case("v05_batch500_0098",
    rc={"project":"mobile-field","repo":"field-app","service":"sync","task":"define offline-first data model"},
    cms=[],
    cus=[u("u1","The sync module must use a logical clock (Lamport timestamp) for ordering all mutations across devices, not wall-clock time."),
         u("u2","Mutations are persisted locally in SQLite with a 'pending_sync' flag and synced in timestamp order when connectivity is available."),
         u("u3","The sync conflict window is defined as the time between a mutation's local commit and its server acknowledgement; conflicts within this window use CRDT merge.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("service_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant"],
    notes="u1, u2, u3 define the sync data model with specific algorithms and semantics -> all service_memory. u1 is ordering, u2 is persistence, u3 is conflict resolution."))

NEW200.append(make_case("v05_batch500_0099",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"pricing-engine","task":"define pricing rule evaluation order"},
    cms=[],
    cus=[u("u1","The pricing engine must apply discounts in this order: item-level discounts first, then cart-level percentage discounts, then cart-level fixed-amount discounts, then loyalty points redemption."),
         u("u2","Discounts must never reduce the pre-tax item price below the cost price stored in the product catalog."),
         u("u3","The pricing engine must log the applied discount stack for each order line item, showing which discounts applied and in what order.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("service_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant"],
    notes="u1 defines discount application order -> service_memory. u2 defines a price floor constraint -> service_memory. u3 defines logging behavior -> service_memory."))

NEW200.append(make_case("v05_batch500_0100",
    rc={"project":"travel-planner","repo":"voyager","service":"booking-validator","task":"define booking constraint rules"},
    cms=[],
    cus=[u("u1","The booking validator must reject any itinerary where the arrival time of a flight segment is after the departure time of the next segment on the same calendar day."),
         u("u2","Multi-city bookings must have a minimum layover of 60 minutes for domestic connections and 90 minutes for international connections."),
         u("u3","The booking validator must check that the passenger's passport expiry date is at least 6 months after the return flight date for international bookings.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("service_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant"],
    notes="u1, u2, u3 are durable booking validation rules -> all service_memory."))

# STORE/SKIP-only 101-120

NEW200.append(make_case("v05_batch500_0101",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"ai-controller","task":"define NPC behavior tree evaluation"},
    cms=[],
    cus=[u("u1","The AI controller must evaluate behavior trees at 10Hz with a maximum node traversal depth of 50 to prevent frame drops."),
         u("u2","NPCs in the 'combat' state must re-evaluate their target every 500ms and switch targets if a higher-threat enemy enters their perception radius."),
         u("u3","The behavior tree debugger is currently broken on the PS5 target; it works fine on PC and Xbox.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines evaluation constraints -> service_memory. u2 defines combat re-evaluation behavior -> service_memory. u3 describes a current platform-specific bug -> task_state."))

NEW200.append(make_case("v05_batch500_0102",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"link-checker","task":"define broken link detection rules"},
    cms=[],
    cus=[u("u1","The link checker must validate all external links weekly by sending HEAD requests and flagging any URL that returns a status code >= 400 for two consecutive weeks."),
         u("u2","Internal links between documentation pages must be validated on every build by checking that the target anchor exists in the rendered HTML."),
         u("u3","The link checker report is generated at build time and written to reports/links/broken_links_<date>.md.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","repo_vs_service"],
    notes="u1 defines external link validation -> service_memory. u2 defines internal link validation -> service_memory. u3 defines report path convention -> repo_memory."))

NEW200.append(make_case("v05_batch500_0103",
    rc={"project":"education-platform","repo":"learnhub","service":"certificate-generator","task":"define certificate issuance criteria"},
    cms=[],
    cus=[u("u1","The certificate generator must issue a course completion certificate when the learner has completed all required modules and achieved a cumulative quiz score of at least 70%."),
         u("u2","Certificates must include the learner's full name, course title, completion date, and a verifiable QR code linking to the certificate validation page."),
         u("u3","The certificate template design was approved last week and the final PDF layout is due by Friday.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines issuance criteria -> service_memory. u2 defines certificate content format -> service_memory. u3 is current deadline -> task_state."))

NEW200.append(make_case("v05_batch500_0104",
    rc={"project":"customer-support","repo":"helpdesk","service":"escalation-engine","task":"define escalation rules"},
    cms=[],
    cus=[u("u1","The escalation engine must escalate a ticket when it has been in 'open' status for more than 4 hours for priority-critical, 8 hours for high, 24 hours for normal."),
         u("u2","Escalated tickets are assigned to the team lead's queue and must be acknowledged within 30 minutes."),
         u("u3","The current escalation rules were set during the 2025 Q4 review and need updating for the new priority definitions.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","service_vs_task_state","stale_memory"],
    notes="u1 defines escalation thresholds -> service_memory. u2 defines escalation handling SLA -> service_memory. u3 notes that rules are stale and need update -> task_state (describes state, not a durable rule)."))

NEW200.append(make_case("v05_batch500_0105",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"report-scheduler","task":"define scheduled report delivery rules"},
    cms=[],
    cus=[u("u1","The report scheduler must generate and deliver reports according to each recipient's configured schedule, supporting daily, weekly, and monthly frequencies."),
         u("u2","If a scheduled report generation fails, the scheduler must retry once after 5 minutes and then notify the report owner of the failure."),
         u("u3","The report scheduler currently has a known memory leak when processing more than 50 reports in a single cycle.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines scheduling behavior -> service_memory. u2 defines retry and notification behavior -> service_memory. u3 describes a known bug -> task_state (current implementation issue)."))

NEW200.append(make_case("v05_batch500_0106",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"approval-handler","task":"define approval chain logic"},
    cms=[],
    cus=[u("u1","The approval handler must route approval requests through a chain defined by the workflow: each approver must approve before the next in the chain is notified."),
         u("u2","The current approval handler only supports single-approver workflows; multi-level chains are planned for Q3."),
         u("u3","Approval chain configurations are defined in workflows/<name>/approval_chain.yaml and validated against the chain schema.")],
    read=[], store=[st("service_memory","u1"),st("task_state","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","repo_convention","repo_vs_service"],
    notes="u1 defines chain routing -> service_memory. u2 describes current limitation and plan -> task_state. u3 is config path -> repo_memory."))

NEW200.append(make_case("v05_batch500_0107",
    rc={"project":"learning-assistant","repo":"tutorai","service":"spaced-repetition","task":"define spaced repetition algorithm parameters"},
    cms=[],
    cus=[u("u1","The spaced repetition engine must use the FSRS algorithm with default parameters: decay=-0.5, factor=0.9, requested_retention=0.9."),
         u("u2","The FSRS model parameters are stored in config/spaced_repetition/fsrs_params.json and can be tuned per subject."),
         u("u3","Run an A/B test comparing FSRS against the current SM-2 algorithm on 500 learners before rolling out.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines algorithm -> service_memory. u2 defines config path -> repo_memory. u3 is current experiment -> task_state."))

NEW200.append(make_case("v05_batch500_0108",
    rc={"project":"supply-chain","repo":"logistix","service":"order-validator","task":"plan order validation improvements"},
    cms=[],
    cus=[u("u1","The order validator must reject purchase orders where the requested quantity exceeds the supplier's maximum order quantity for that SKU."),
         u("u2","The supplier max-quantity data is currently stale for 12 suppliers; update the supplier catalog before the next ordering cycle."),
         u("u3","The order validation rules must be the same across all logistix services including warehouse, shipping, and returns.")],
    read=[], store=[st("service_memory","u1"),st("task_state","u2"),st("project_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="u1 defines validation -> service_memory. u2 is current stale data issue -> task_state. u3 is cross-service policy -> project_memory."))

NEW200.append(make_case("v05_batch500_0109",
    rc={"project":"creator-tools","repo":"artisan","service":"layer-compositor","task":"plan compositor caching improvements"},
    cms=[],
    cus=[u("u1","The layer compositor must blend layers from bottom to top using the blend mode specified on each layer, supporting normal, multiply, screen, overlay, and soft-light modes."),
         u("u2","The compositor currently recomputes all layers on every frame; caching optimization is scheduled for the performance sprint next month."),
         u("u3","The compositor shader source files live under src/rendering/compositor/shaders/ and are compiled at build time.")],
    read=[], store=[st("service_memory","u1"),st("task_state","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","repo_convention","repo_vs_service"],
    notes="u1 defines blend behavior -> service_memory. u2 describes current state and plan -> task_state. u3 is source path -> repo_memory."))

NEW200.append(make_case("v05_batch500_0110",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"signature-validator","task":"document signature verification security"},
    cms=[],
    cus=[u("u1","The signature validator must verify electronic signatures by checking the digital certificate chain against the trusted CA store and confirming the certificate has not been revoked."),
         u("u2","The trusted CA certificate bundle is stored in config/certs/trusted_ca_bundle.pem and must be updated quarterly."),
         u("u3","The signature validator currently does not check certificate revocation via OCSP; adding OCSP is planned for the security audit remediation.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines verification -> service_memory. u2 defines cert path -> repo_memory. u3 describes current gap -> task_state."))

# STORE/SKIP-only 111-130: repo_memory + task_state combos

NEW200.append(make_case("v05_batch500_0111",
    rc={"project":"data-platform","repo":"data-jobs","service":"documentation","task":"document config file conventions"},
    cms=[],
    cus=[u("u1","All service configuration files must be in YAML format under config/<service_name>/ with a schema version field at the top of each file."),
         u("u2","The schema version follows the format YYYY-MM-DD and must be updated whenever a new config key is added or an existing key's type changes."),
         u("u3","Write the configuration conventions document in docs/platform/config_conventions.md by end of sprint.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","repo_convention","task_progress","project_vs_repo"],
    notes="u1 is config file convention -> repo_memory. u2 is schema version convention -> repo_memory. u3 is a documentation task with deadline -> task_state."))

NEW200.append(make_case("v05_batch500_0112",
    rc={"project":"mobile-field","repo":"field-app","service":"build","task":"document build and signing conventions"},
    cms=[],
    cus=[u("u1","Release builds must be signed with the field-app-release.keystore located in the keystores/ directory at the repo root."),
         u("u2","The keystore password and key alias are provided via environment variables FIELD_KEYSTORE_PASS and FIELD_KEY_ALIAS during CI builds."),
         u("u3","Debug builds use the default Android debug keystore and must never be distributed outside the development team.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is build signing convention -> repo_memory. u2 is env var convention -> repo_memory. u3 is debug build policy -> repo_memory."))

NEW200.append(make_case("v05_batch500_0113",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"database","task":"document database migration conventions"},
    cms=[],
    cus=[u("u1","Database migration files are named with a UTC timestamp prefix: YYYYMMDDHHMMSS_descriptive_name.sql and stored in db/migrations/."),
         u("u2","Every migration must include an up.sql for forward migration and a down.sql for rollback, both in the same directory."),
         u("u3","Migrations are applied by the migration runner container using the command: docker compose run migrations up.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is migration naming convention -> repo_memory. u2 is migration content convention -> repo_memory. u3 is migration execution command -> repo_memory."))

NEW200.append(make_case("v05_batch500_0114",
    rc={"project":"finance-dashboard","repo":"finboard","service":"linting","task":"document code style conventions"},
    cms=[],
    cus=[u("u1","Python code in the finboard project must use Black for formatting with line length 100, and isort for import ordering with the 'black' profile."),
         u("u2","TypeScript code must use Prettier with the project's .prettierrc.json and must pass tsc --noEmit before commit."),
         u("u3","The pre-commit hooks are defined in .pre-commit-config.yaml and run Black, isort, Prettier, and tsc on staged files.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is Python code style convention -> repo_memory. u2 is TypeScript code style convention -> repo_memory. u3 is pre-commit hook convention -> repo_memory."))

NEW200.append(make_case("v05_batch500_0115",
    rc={"project":"learning-assistant","repo":"tutorai","service":"dependencies","task":"document dependency management conventions"},
    cms=[],
    cus=[u("u1","Python dependencies are managed with Poetry and locked in poetry.lock; never pip install directly into the project environment."),
         u("u2","Node.js dependencies are managed with pnpm and locked in pnpm-lock.yaml; the workspace is defined in pnpm-workspace.yaml."),
         u("u3","All Docker images must pin their base image to a specific SHA256 digest, not a mutable tag like 'latest'.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","project_vs_repo"],
    notes="u1 is Python dep convention -> repo_memory. u2 is Node dep convention -> repo_memory. u3 is Docker convention -> repo_memory."))

# STORE/SKIP-only 116-130: More varied combos

NEW200.append(make_case("v05_batch500_0116",
    rc={"project":"healthcare-admin","repo":"medflow","service":"audit-log","task":"define audit log retention and format"},
    cms=[],
    cus=[u("u1","The audit log must store all access events in a structured JSON format with fields: event_id, timestamp, user_id, action, resource_type, resource_id, ip_address, and user_agent."),
         u("u2","Audit logs must be retained for a minimum of 7 years in immutable storage to comply with healthcare regulations."),
         u("u3","Audit log files are rotated daily and stored under /var/log/medflow/audit/YYYY/MM/DD/ with gzip compression.")],
    read=[], store=[st("service_memory","u1"),st("project_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","project_vs_repo","repo_convention","target_boundary"],
    notes="u1 defines audit event schema -> service_memory. u2 is a compliance retention requirement -> project_memory (regulatory, cross-service). u3 is file storage path -> repo_memory. Three-target distinction."))

NEW200.append(make_case("v05_batch500_0117",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"data-quality","task":"define data quality rules for training pool"},
    cms=[],
    cus=[u("u1","Every training case must have unit texts that are semantically unique; a cosine similarity above 0.80 with any other unit text triggers a review flag."),
         u("u2","The current batch500 is still under construction; the similarity check has not been run yet on the new200 cases."),
         u("u3","For this project, do not generate cases using LLM-based templates or automated fill-in-the-blank substitution.")],
    read=[], store=[st("service_memory","u1"),st("task_state","u2"),st("project_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="u1 defines a durable quality rule -> service_memory. u2 describes current validation status -> task_state. u3 is a project-level data generation policy -> project_memory."))

NEW200.append(make_case("v05_batch500_0118",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"data-export","task":"define data export API conventions"},
    cms=[],
    cus=[u("u1","The data export API must support CSV and JSON output formats, selected via the Accept header."),
         u("u2","Export requests that would return more than 100,000 rows must be processed asynchronously with a download link sent via email."),
         u("u3","The async export job currently has a bug where jobs with special characters in the query fail silently; fix this before the Q2 release.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines format support -> service_memory. u2 defines async threshold -> service_memory. u3 is a current bug fix task -> task_state."))

NEW200.append(make_case("v05_batch500_0119",
    rc={"project":"customer-support","repo":"helpdesk","service":"routing-engine","task":"define load-balancing strategy"},
    cms=[],
    cus=[u("u1","The routing engine must distribute incoming tickets to agents using weighted round-robin where the weight is inversely proportional to the agent's current open ticket count."),
         u("u2","The routing weight configuration and agent status mappings are stored in config/routing/weights.yaml."),
         u("u3","The routing engine currently does not account for agent skill specialization; adding skill-aware weighting is planned for next quarter.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines algorithm -> service_memory. u2 defines config path -> repo_memory. u3 describes current gap -> task_state."))

NEW200.append(make_case("v05_batch500_0120",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"spell-checker","task":"define spell-checking dictionary management"},
    cms=[],
    cus=[u("u1","The spell checker must use a project-specific dictionary at data/dictionaries/project_terms.txt that supplements the standard language dictionary."),
         u("u2","Terms added to the project dictionary must be reviewed in the PR that adds them; no direct commits to the dictionary file."),
         u("u3","The spell checker must flag words that appear in code blocks or inline code differently from prose: code content is excluded from spell checking.")],
    read=[], store=[st("repo_memory","u1"),st("repo_memory","u2"),st("service_memory","u3")], skip=[],
    tags=["store_skip_only","repo_convention","service_invariant","repo_vs_service"],
    notes="u1 defines dictionary file path -> repo_memory. u2 defines review convention -> repo_memory. u3 defines spell-check behavior for code -> service_memory."))

NEW200.append(make_case("v05_batch500_0121",
    rc={"project":"travel-planner","repo":"voyager","service":"api-gateway","task":"define API rate limiting rules"},
    cms=[],
    cus=[u("u1","The API gateway must enforce rate limits per API key: 100 requests per minute for free tier, 1000 for pro tier, and 5000 for enterprise tier."),
         u("u2","Rate-limited responses must include the Retry-After header with the number of seconds until the limit resets."),
         u("u3","The API gateway currently does not rate-limit internal service-to-service calls; only external API key requests are limited.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines rate limit tiers -> service_memory. u2 defines response header behavior -> service_memory. u3 describes current implementation scope -> task_state."))

NEW200.append(make_case("v05_batch500_0122",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"save-system","task":"define save file format and compatibility"},
    cms=[],
    cus=[u("u1","The save system must write save files in a binary format with a 16-byte header containing magic number, version, and CRC32 checksum of the payload."),
         u("u2","Save files from version N must be loadable by version N+1; if backward compatibility is broken, the version number must increment the major component."),
         u("u3","Save files are stored under the user's AppData directory at DungeonTools/saves/ with a subdirectory per character.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","repo_vs_service"],
    notes="u1 defines save file format -> service_memory. u2 defines compatibility rule -> service_memory. u3 defines storage path -> repo_memory."))

NEW200.append(make_case("v05_batch500_0123",
    rc={"project":"education-platform","repo":"learnhub","service":"notification-service","task":"define notification delivery rules"},
    cms=[],
    cus=[u("u1","The notification service must deliver announcements via email, in-app notification, and optional SMS based on the user's configured channels."),
         u("u2","Notification templates for each channel are stored in config/notifications/templates/ with separate directories per locale."),
         u("u3","The notification service currently does not support SMS delivery in European countries due to carrier restrictions; evaluate Twilio EU integration.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines delivery behavior -> service_memory. u2 defines template path -> repo_memory. u3 describes current gap and next step -> task_state."))

NEW200.append(make_case("v05_batch500_0124",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"logging-service","task":"define structured logging format"},
    cms=[],
    cus=[u("u1","All services must emit logs in structured JSON format with the following required fields: timestamp, level, service, trace_id, message."),
         u("u2","Log levels are DEBUG, INFO, WARN, ERROR, FATAL; production environments must run at INFO level minimum."),
         u("u3","Logs are shipped to the central logging platform via a Fluentd sidecar that tails the container's stdout.")],
    read=[], store=[st("project_memory","u1"),st("repo_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","project_vs_repo","repo_convention","target_boundary"],
    notes="u1 says 'All services must' -> project_memory. u2 is log level configuration convention -> repo_memory. u3 is infrastructure convention -> repo_memory."))

NEW200.append(make_case("v05_batch500_0125",
    rc={"project":"supply-chain","repo":"logistix","service":"barcode-scanner","task":"define barcode validation rules"},
    cms=[],
    cus=[u("u1","The barcode scanner must validate GTIN-14 barcodes by checking the check digit using the modulo 10 algorithm."),
         u("u2","Scanned barcodes that fail check-digit validation must be flagged for manual entry and not automatically added to the inventory count."),
         u("u3","The barcode scanner integration with the handheld devices is currently blocked on the Bluetooth pairing firmware update.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines check-digit validation -> service_memory. u2 defines failure handling -> service_memory. u3 is current blocker -> task_state."))

NEW200.append(make_case("v05_batch500_0126",
    rc={"project":"data-platform","repo":"data-jobs","service":"data-lineage","task":"define data lineage tracking rules"},
    cms=[],
    cus=[u("u1","The data lineage tracker must record every transformation applied to a dataset, including the source table, transformation SQL or code, destination table, and execution timestamp."),
         u("u2","Lineage records must be queryable by table name, column name, and time range to support impact analysis before schema changes."),
         u("u3","The lineage database schema is defined in db/migrations/lineage/ and uses PostgreSQL with TimescaleDB for time-series lineage queries.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","repo_vs_service"],
    notes="u1 defines lineage tracking behavior -> service_memory. u2 defines queryability requirements -> service_memory. u3 defines DB schema location -> repo_memory."))

# STORE/SKIP-only 127-148: completing to 78 target

NEW200.append(make_case("v05_batch500_0127",
    rc={"project":"mobile-field","repo":"field-app","service":"map-renderer","task":"define map tile caching rules"},
    cms=[],
    cus=[u("u1","The map renderer must cache map tiles locally with a maximum cache size of 200MB, evicting least-recently-used tiles when the limit is exceeded."),
         u("u2","Tiles for the currently visible area plus a 2-tile buffer in each direction must be preloaded when the map view stabilizes for more than 500ms."),
         u("u3","The tile cache directory is at <app_data>/map_tiles/ and is excluded from backups.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","repo_vs_service"],
    notes="u1 defines cache eviction policy -> service_memory. u2 defines preloading behavior -> service_memory. u3 defines cache path -> repo_memory."))

NEW200.append(make_case("v05_batch500_0128",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"cart-service","task":"define cart expiration rules"},
    cms=[],
    cus=[u("u1","The cart service must expire abandoned carts after 7 days of inactivity, removing reserved inventory."),
         u("u2","The cart expiration job runs daily at 03:00 UTC and processes carts in batches of 500; its schedule is defined in config/jobs/cart_expiration.yaml."),
         u("u3","The cart service currently holds inventory for 7 days but the business team wants to reduce this to 3 days; evaluate the impact before changing.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines expiration behavior -> service_memory. u2 defines job schedule path -> repo_memory. u3 is current evaluation task -> task_state."))

NEW200.append(make_case("v05_batch500_0129",
    rc={"project":"creator-tools","repo":"artisan","service":"collaboration-sync","task":"plan collaboration conflict resolution"},
    cms=[],
    cus=[u("u1","The collaboration sync engine must use Operational Transformation to resolve concurrent edits, with the server as the authoritative merge point."),
         u("u2","The OT algorithm implementation is currently a prototype that only handles text insertion; support for deletion and formatting operations is planned for the beta release."),
         u("u3","The OT operation log is stored in the collaboration_ops table defined in db/migrations/collaboration/002_ops_log.sql.")],
    read=[], store=[st("service_memory","u1"),st("task_state","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","repo_convention","repo_vs_service"],
    notes="u1 defines OT strategy -> service_memory. u2 describes current prototype scope and plan -> task_state. u3 is DB migration path -> repo_memory."))

NEW200.append(make_case("v05_batch500_0130",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"search-engine","task":"define legal search relevance rules"},
    cms=[],
    cus=[u("u1","The search engine must prioritize exact phrase matches in clause text over keyword matches, with a boost factor of 5.0 for quoted search terms."),
         u("u2","Search index settings including boost weights and tokenizer configuration are stored in config/search/legal_search_settings.json."),
         u("u3","The search index currently takes 4 hours to rebuild; optimize the rebuild to under 1 hour before adding weekly scheduled rebuilds.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines scoring -> service_memory. u2 defines config path -> repo_memory. u3 is current optimization task -> task_state."))

NEW200.append(make_case("v05_batch500_0131",
    rc={"project":"healthcare-admin","repo":"medflow","service":"vaccination-tracker","task":"define immunization schedule rules"},
    cms=[],
    cus=[u("u1","The vaccination tracker must maintain the CDC-recommended immunization schedule and alert providers when a patient is due for a vaccination based on their age and previous doses."),
         u("u2","For multi-dose vaccines, the tracker must enforce minimum intervals between doses: if a patient receives a dose earlier than the minimum interval, flag it for provider review."),
         u("u3","The immunization schedule data is loaded from a CSV published by the CDC and updated quarterly.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("repo_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","repo_vs_service"],
    notes="u1 defines schedule alerting -> service_memory. u2 defines interval enforcement -> service_memory. u3 defines data source -> repo_memory."))

NEW200.append(make_case("v05_batch500_0132",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"batch-builder","task":"define batch construction rules for v0.5"},
    cms=[],
    cus=[u("u1","Each batch must maintain target distribution within ±2pp of the blueprint for svc/task, and ±3pp for repo/project/profile."),
         u("u2","The batch builder must reject any case that duplicates more than 2 candidate memories from any other case in the same batch."),
         u("u3","The current batch500 new200 cases are being hand-crafted; after generation, run the full validation suite before merging.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines distribution tolerance rule -> service_memory. u2 defines dedup rule -> service_memory. u3 is current process state -> task_state."))

NEW200.append(make_case("v05_batch500_0133",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"auth-service","task":"define authentication and session rules"},
    cms=[],
    cus=[u("u1","The auth service must issue JWTs signed with RS256, with a 15-minute access token expiry and a 7-day refresh token expiry."),
         u("u2","The JWT signing keys are stored in config/auth/keys/ and rotated every 90 days via the key rotation script at scripts/rotate_jwt_keys.sh."),
         u("u3","The auth service currently does not support social login providers; adding Google and GitHub OAuth is planned for the next milestone.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines JWT management -> service_memory. u2 defines key path and rotation -> repo_memory. u3 describes current gap -> task_state."))

NEW200.append(make_case("v05_batch500_0134",
    rc={"project":"customer-support","repo":"helpdesk","service":"survey-engine","task":"define post-resolution survey rules"},
    cms=[],
    cus=[u("u1","The survey engine must send a CSAT survey 24 hours after ticket resolution, with a single question rated 1-5 and an optional comment field."),
         u("u2","Survey question templates and timing rules are configured in config/surveys/csat_config.yaml per support queue."),
         u("u3","The survey engine currently only supports CSAT; adding NPS surveys for enterprise customers is on the roadmap for Q4.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines survey behavior -> service_memory. u2 defines config path -> repo_memory. u3 describes roadmap -> task_state."))

NEW200.append(make_case("v05_batch500_0135",
    rc={"project":"finance-dashboard","repo":"finboard","service":"market-data","task":"define market data feed processing rules"},
    cms=[],
    cus=[u("u1","The market data service must process price ticks from the exchange feed and publish consolidated 1-minute OHLCV bars to the data bus."),
         u("u2","The exchange feed adapter configurations are stored in config/market_data/feeds/ with per-exchange connection parameters."),
         u("u3","The market data service currently only processes NYSE and NASDAQ feeds; adding LSE and TSE feeds is needed for the European client launch.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines bar aggregation -> service_memory. u2 defines config path -> repo_memory. u3 describes current scope and expansion plan -> task_state."))

NEW200.append(make_case("v05_batch500_0137",
    rc={"project":"education-platform","repo":"learnhub","service":"grading","task":"define rubric-based grading algorithm"},
    cms=[],
    cus=[u("u1","The grading service must evaluate essay submissions against a rubric with up to 5 criteria, each with a weight and 4 performance levels."),
         u("u2","Rubric definitions are stored as JSON files in config/grading/rubrics/ and referenced by assignment ID."),
         u("u3","The grading service currently only supports single-criterion rubrics for multiple-choice questions; essay rubric support is under development.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines rubric evaluation -> service_memory. u2 defines config path -> repo_memory. u3 describes current limitation -> task_state."))

NEW200.append(make_case("v05_batch500_0138",
    rc={"project":"learning-assistant","repo":"tutorai","service":"recommendation","task":"define content recommendation algorithm"},
    cms=[],
    cus=[u("u1","The content recommendation engine must rank learning resources by a composite score of relevance, difficulty match, and user rating, weighted 0.5, 0.3, and 0.2."),
         u("u2","Recommendation model weights and feature configurations are stored in models/recommendations/ranking_config.json."),
         u("u3","The recommendation engine currently does not account for the learner's preferred content format; adding format preference weighting is scheduled for the personalization sprint.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines ranking -> service_memory. u2 defines model path -> repo_memory. u3 describes future plan -> task_state."))

NEW200.append(make_case("v05_batch500_0139",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"compensation-handler","task":"plan saga compensation improvements"},
    cms=[],
    cus=[u("u1","The compensation handler must execute compensating actions in reverse order of the original steps when a saga fails at any step."),
         u("u2","Compensation action definitions are stored in workflows/<name>/compensations.yaml with a reverse flag that controls execution order."),
         u("u3","The compensation handler currently only supports database rollback compensations; adding support for API call compensations is planned after the DB layer is stable.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines compensation behavior -> service_memory. u2 defines config path -> repo_memory. u3 describes current scope -> task_state."))

NEW200.append(make_case("v05_batch500_0140",
    rc={"project":"supply-chain","repo":"logistix","service":"delivery-tracker","task":"plan delivery ETA improvements"},
    cms=[],
    cus=[u("u1","The delivery tracker must compute ETA using the driver's current GPS position, the remaining route distance, and the average speed over the last 15 minutes."),
         u("u2","The ETA calculation parameters including speed estimation weights are configured in config/delivery/eta_params.yaml."),
         u("u3","The delivery tracker currently does not account for real-time traffic conditions; integrating traffic data from the municipal traffic API is under evaluation.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines ETA algorithm -> service_memory. u2 defines config path -> repo_memory. u3 describes current gap -> task_state."))

NEW200.append(make_case("v05_batch500_0141",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"inventory-system","task":"define item stacking and durability rules"},
    cms=[],
    cus=[u("u1","The inventory system must stack identical items with the same durability value up to a maximum stack size defined per item type."),
         u("u2","Item type definitions including max stack sizes and durability thresholds are stored in config/items/item_types.json."),
         u("u3","The inventory system currently allows stacking items with different durability values, which causes confusion; fixing this is prioritized for the next patch.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines stacking -> service_memory. u2 defines item config path -> repo_memory. u3 describes current bug -> task_state."))

NEW200.append(make_case("v05_batch500_0142",
    rc={"project":"travel-planner","repo":"voyager","service":"price-alert","task":"define price alert triggering rules"},
    cms=[],
    cus=[u("u1","The price alert service must monitor subscribed routes and trigger an alert when the current price drops below the user's target price for that route."),
         u("u2","Alert rule configurations per user and route are stored in config/alerts/price_alerts/ with notification preferences."),
         u("u3","The price alert service currently checks prices every 30 minutes; reducing the check interval to 5 minutes is blocked on the pricing API rate limit negotiation.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines alert behavior -> service_memory. u2 defines config path -> repo_memory. u3 describes current limitation and blocker -> task_state."))

NEW200.append(make_case("v05_batch500_0144",
    rc={"project":"mobile-field","repo":"field-app","service":"bluetooth-connector","task":"plan BLE reconnection improvements"},
    cms=[],
    cus=[u("u1","The Bluetooth connector must attempt reconnection to a paired peripheral with exponential backoff: 1s, 2s, 4s, 8s, 16s, up to 5 retries."),
         u("u2","The BLE reconnection parameters are configured in config/bluetooth/reconnect_policy.xml with backoff base and max retries."),
         u("u3","The Bluetooth connector currently does not distinguish between transient disconnections and device-power-off; adding disconnection reason classification is planned.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines reconnection algorithm -> service_memory. u2 defines config path -> repo_memory. u3 describes current limitation -> task_state."))

NEW200.append(make_case("v05_batch500_0145",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"tax-calculator","task":"define tax calculation rules"},
    cms=[],
    cus=[u("u1","The tax calculator must determine the applicable tax rate based on the customer's shipping address, using destination-based sourcing for US orders."),
         u("u2","Tax rate tables per jurisdiction are stored in config/tax/rates/ and updated monthly from the tax data provider."),
         u("u3","The tax calculator currently does not handle digital products differently from physical goods; adding digital-product tax rules for EU VAT compliance is required before the European launch.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines tax sourcing -> service_memory. u2 defines config path -> repo_memory. u3 describes blocker for launch -> task_state."))

NEW200.append(make_case("v05_batch500_0146",
    rc={"project":"creator-tools","repo":"artisan","service":"undo-manager","task":"plan undo system enhancements"},
    cms=[],
    cus=[u("u1","The undo manager must maintain a stack of reversible operations with a maximum depth of 100 entries per document."),
         u("u2","Undo stack configuration including max depth and grouping thresholds is in config/undo/undo_settings.json."),
         u("u3","The undo manager currently does not support redo after a new action following undo; implementing full undo/redo tree is on the UX improvement backlog.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines undo stack -> service_memory. u2 defines config path -> repo_memory. u3 describes future enhancement -> task_state."))

NEW200.append(make_case("v05_batch500_0147",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"version-comparator","task":"define contract version diff visualization"},
    cms=[],
    cus=[u("u1","The version comparator must highlight textual differences between contract versions using a word-level diff algorithm with green underline for additions and red strikethrough for deletions."),
         u("u2","Diff visualization templates and color schemes are stored in config/diff/templates/ and can be customized per client."),
         u("u3","The version comparator currently only supports text diff; adding table comparison for schedules and exhibits is planned for the next major release.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines diff rendering -> service_memory. u2 defines config path -> repo_memory. u3 describes scope gap -> task_state."))

NEW200.append(make_case("v05_batch500_0148",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"eval-runner","task":"define eval runner early-stopping criteria"},
    cms=[],
    cus=[u("u1","The eval runner must support early stopping based on a monitored metric: if the metric does not improve for N consecutive evaluations, the run is terminated."),
         u("u2","The early-stopping configuration including patience and metric name is stored in config/eval/early_stopping.yaml per experiment."),
         u("u3","The eval runner currently only supports early stopping on dev set loss; adding support for stopping on STORE target accuracy is needed before the v0.5 training run.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines early stopping -> service_memory. u2 defines config path -> repo_memory. u3 describes current scope and need -> task_state."))

NEW200.append(make_case("v05_batch500_0136",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"pdf-generator","task":"define PDF generation standards"},
    cms=[],
    cus=[u("u1","The PDF generator must produce PDF/A-3 compliant documents with embedded fonts, metadata, and a table of contents generated from heading elements."),
         u("u2","PDF generation templates and compliance settings are stored in config/pdf/templates/ with separate templates for each documentation product."),
         u("u3","The PDF generator currently does not support right-to-left text rendering for Arabic and Hebrew; RTL support is planned for the internationalization milestone.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines PDF compliance -> service_memory. u2 defines template path -> repo_memory. u3 describes current gap -> task_state."))

NEW200.append(make_case("v05_batch500_0143",
    rc={"project":"data-platform","repo":"data-jobs","service":"data-masking","task":"define dynamic data masking rules"},
    cms=[],
    cus=[u("u1","The data masking service must apply masking rules based on the user's role: analysts see masked PII, data engineers see full data, external users see only aggregate counts."),
         u("u2","Data masking rule configurations per role and column are stored in config/masking/role_policies.yaml and evaluated at query time."),
         u("u3","The data masking service currently masks all PII columns uniformly; implementing column-specific masking granularity is planned for the data governance initiative.")],
    read=[], store=[st("service_memory","u1"),st("repo_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","repo_convention","task_progress","repo_vs_service"],
    notes="u1 defines role-based masking -> service_memory. u2 defines config path -> repo_memory. u3 describes current limitation -> task_state."))

# ── READ-only (43 cases) ────────────────────────────────────────────────────

NEW200.append(make_case("v05_batch500_0149",
    rc={"project":"healthcare-admin","repo":"medflow","service":"patient-records","task":"look up patient allergy information"},
    cms=[m("m1","service_memory","The patient records service stores allergies in a structured format with allergen name, reaction type, severity, and date recorded."),
         m("m2","service_memory","The old patient portal used free-text allergy notes which were migrated to the structured format in 2025.")],
    cus=[u("u1","Does the patient John Doe have any documented allergies to penicillin?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: factual lookup. m1 has the current allergy schema. m2 is stale migration history."))

NEW200.append(make_case("v05_batch500_0150",
    rc={"project":"supply-chain","repo":"logistix","service":"inventory-lookup","task":"check stock levels for a specific product"},
    cms=[m("m1","service_memory","Inventory levels are queried from the central inventory database which updates every 5 minutes from warehouse systems."),
         m("m2","repo_memory","The inventory query API is documented at docs/api/inventory_query.md with example requests.")],
    cus=[u("u1","What is the current stock level for product SKU WH-8842 in the Dallas warehouse?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","related_but_useless","temporary_request"],
    notes="READ-only: specific stock query. m1 explains how inventory works. m2 is API docs path — related but not needed for this query."))

NEW200.append(make_case("v05_batch500_0151",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"asset-db","task":"check texture format specification"},
    cms=[m("m1","service_memory","Game textures are stored in the ASTC 6x6 format for mobile and BC7 for desktop platforms, selected at build time."),
         m("m2","repo_memory","Texture source files in PSD format are stored under raw_assets/textures/ and converted during the asset build.")],
    cus=[u("u1","What texture compression format is used for the iOS build target?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","related_but_useless","temporary_request"],
    notes="READ-only: factual question. m1 answers it (ASTC for mobile/iOS). m2 is repo path, not needed."))

NEW200.append(make_case("v05_batch500_0152",
    rc={"project":"creator-tools","repo":"artisan","service":"plugin-system","task":"check plugin API version compatibility"},
    cms=[m("m1","service_memory","The plugin API currently at version 3 supports JavaScript plugins with access to the document model, selection API, and network requests."),
         m("m2","task_state","The plugin API v2 was deprecated in 2025 and will be removed in the next major release.")],
    cus=[u("u1","Will my existing v2 plugins still work after the next update?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: compatibility question. Both m1 (current version) and m2 (deprecation timeline) are needed to answer."))

NEW200.append(make_case("v05_batch500_0153",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"document-store","task":"find contracts for a specific client"},
    cms=[m("m1","service_memory","The document store indexes contracts by client_id, contract_type, and date range, supporting full-text search over clause text."),
         m("m2","repo_memory","Document metadata schemas are defined in docs/api/document_metadata_schema.md.")],
    cus=[u("u1","How many active contracts does client Acme Corp have with an effective date in 2026?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","related_but_useless","temporary_request"],
    notes="READ-only: data lookup. m1 explains how to search. m2 is schema docs, not needed."))

NEW200.append(make_case("v05_batch500_0154",
    rc={"project":"customer-support","repo":"helpdesk","service":"agent-dashboard","task":"check current queue status"},
    cms=[m("m1","service_memory","The agent dashboard shows real-time queue statistics including open tickets, average wait time, and agent availability."),
         m("m2","task_state","The morning shift handover reported a backlog of 23 priority-high tickets from the overnight queue.")],
    cus=[u("u1","What is the current average wait time for priority-normal tickets?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: current status query. m1 explains dashboard. m2 is stale shift report from earlier, not current."))

NEW200.append(make_case("v05_batch500_0155",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"query-history","task":"find a previously run query"},
    cms=[m("m1","service_memory","The query history stores all executed queries with the SQL text, execution time, row count, and timestamp."),
         m("m2","repo_memory","Query history is retained for 90 days in the query_history table and then archived to cold storage.")],
    cus=[u("u1","Show me the SQL query I ran last Tuesday that returned the monthly revenue by region.")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: history lookup. m1 explains the schema. m2 provides retention context (90 days, so last Tuesday should still be available)."))

NEW200.append(make_case("v05_batch500_0156",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"doc-generator","task":"check API reference generation settings"},
    cms=[m("m1","service_memory","The doc generator creates API reference pages from OpenAPI specs, extracting endpoint descriptions, parameters, and response schemas."),
         m("m2","repo_memory","OpenAPI spec files are expected in api_specs/<service_name>/openapi.yaml and are validated before generation.")],
    cus=[u("u1","Which OpenAPI version does the doc generator currently support?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","related_but_useless","temporary_request"],
    notes="READ-only: version check. m1 describes behavior but not version. m2 mentions validation but also not version. Both read for context."))

NEW200.append(make_case("v05_batch500_0157",
    rc={"project":"travel-planner","repo":"voyager","service":"airline-connector","task":"check airline API rate limits"},
    cms=[m("m1","service_memory","The airline connector respects rate limits returned in API response headers, throttling requests when the remaining count drops below 10%."),
         m("m2","task_state","The SkyConnect airline API integration was rate-limited last week during the fare sale, causing 2 hours of delayed price updates.")],
    cus=[u("u1","What is the current rate limit for the SkyConnect airline search API?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: rate limit inquiry. m1 explains general throttling. m2 is a stale incident report, not current limits."))

NEW200.append(make_case("v05_batch500_0158",
    rc={"project":"education-platform","repo":"learnhub","service":"enrollment-verifier","task":"verify student enrollment status"},
    cms=[m("m1","service_memory","The enrollment verifier checks a student's enrollment status against the registration database and returns active, waitlisted, dropped, or completed."),
         m("m2","repo_memory","Enrollment data is stored in the enrollments table with a composite primary key of student_id and course_section_id.")],
    cus=[u("u1","Is student S-44921 enrolled in CS-301 Section 02 this semester?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: enrollment lookup. Both memories provide schema context for the lookup."))

NEW200.append(make_case("v05_batch500_0159",
    rc={"project":"finance-dashboard","repo":"finboard","service":"data-importer","task":"check import schedule for a dataset"},
    cms=[m("m1","service_memory","The data importer supports scheduled imports defined by cron expressions, with each dataset having its own schedule in the import configuration."),
         m("m2","repo_memory","Import schedules are configured in config/imports/<dataset>/schedule.yaml with the cron expression and retry policy.")],
    cus=[u("u1","When is the next scheduled import for the trading_desk_pnl dataset?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: schedule inquiry. Both memories help locate the schedule configuration."))

NEW200.append(make_case("v05_batch500_0160",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"workflow-monitor","task":"check a specific workflow execution status"},
    cms=[m("m1","service_memory","The workflow monitor tracks execution status for all workflows with states: pending, running, paused, completed, failed, cancelled."),
         m("m2","task_state","The workflow 'monthly_invoice_generation' failed last night with a timeout error on the PDF generation step.")],
    cus=[u("u1","What is the current status of workflow execution #WF-2026-0602-0042?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: specific status check. m1 provides state machine. m2 is about a different workflow execution."))

NEW200.append(make_case("v05_batch500_0161",
    rc={"project":"mobile-field","repo":"field-app","service":"gps-logger","task":"check GPS logging configuration"},
    cms=[m("m1","service_memory","The GPS logger samples location at a configurable interval and stores coordinates locally when offline, uploading in batches when online."),
         m("m2","repo_memory","GPS sampling interval and accuracy profile are configured in config/gps/logger_config.xml.")],
    cus=[u("u1","What is the current GPS sampling interval for the field survey team's devices?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: config inquiry. Both memories needed to answer."))

NEW200.append(make_case("v05_batch500_0162",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"shipping-calculator","task":"verify shipping rate for a specific order"},
    cms=[m("m1","service_memory","The shipping calculator determines rates based on package weight, dimensions, origin warehouse, and destination address using carrier API integration."),
         m("m2","repo_memory","Carrier rate tables are cached in Redis under shipping_rates:<carrier> with a 1-hour TTL.")],
    cus=[u("u1","What would be the FedEx Ground shipping cost for a 5lb package from the Dallas warehouse to Chicago 60601?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: rate inquiry. m1 explains calculation. m2 explains cache mechanism."))

NEW200.append(make_case("v05_batch500_0163",
    rc={"project":"learning-assistant","repo":"tutorai","service":"progress-api","task":"retrieve learner progress statistics"},
    cms=[m("m1","service_memory","The progress API returns completion percentages, quiz scores, time spent, and mastery estimates per topic for a given learner."),
         m("m2","task_state","The progress API currently has a known bug where time spent is undercounted for sessions that span midnight UTC.")],
    cus=[u("u1","Show me the progress for learner L-8821 in the Python Basics course.")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: progress lookup. m1 explains the API. m2 is about a bug (stale task state), not needed for this query."))

NEW200.append(make_case("v05_batch500_0164",
    rc={"project":"data-platform","repo":"data-jobs","service":"monitoring","task":"check pipeline error rates for the past week"},
    cms=[m("m1","service_memory","Pipeline monitoring captures error counts, error types, and affected tables for each pipeline run, stored in the pipeline_metrics table."),
         m("m2","service_memory","The old v1 pipeline monitoring used a separate metrics database that was consolidated into the main analytics DB in 2025.")],
    cus=[u("u1","What was the error rate for the billing pipeline over the past 7 days?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: metric query. m1 explains where data lives. m2 is stale architecture reference."))

NEW200.append(make_case("v05_batch500_0165",
    rc={"project":"customer-support","repo":"helpdesk","service":"agent-schedule","task":"check agent availability for next shift"},
    cms=[m("m1","service_memory","The agent schedule shows shift assignments, current status, and skills for all support agents, refreshing every 5 minutes."),
         m("m2","repo_memory","Shift schedules are managed in config/schedules/ and imported from the workforce management system.")],
    cus=[u("u1","Which agents with the billing_certified skill are available for the 14:00-22:00 shift today?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: availability lookup. Both memories provide context."))

NEW200.append(make_case("v05_batch500_0166",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"batch-stats","task":"check current batch500 generation progress"},
    cms=[m("m1","service_memory","The batch stats reporter shows case counts, store target distributions, tag coverage, and validation status for the current batch."),
         m("m2","task_state","The batch500 new200 cases are being generated with targets: svc 60, task 80, repo 48, project 33, profile 10 store units.")],
    cus=[u("u1","How many READ+STORE joint cases have been created so far in the batch500 new200 generation?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","task_progress","temporary_request"],
    notes="READ-only: progress inquiry. Both memories help answer."))

# READ-only 167-191: More cases to reach 43

NEW200.append(make_case("v05_batch500_0167",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"chart-renderer","task":"check chart color configuration"},
    cms=[m("m1","service_memory","The chart renderer uses a configurable color palette per chart type, with defaults defined in the chart theme configuration."),
         m("m2","repo_memory","Chart themes are stored in config/charts/themes/ and can be applied per dashboard or per widget.")],
    cus=[u("u1","What color palette is currently configured for the revenue trend line chart on the executive dashboard?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","related_but_useless","temporary_request"],
    notes="READ-only: config inquiry. Both memories provide context."))

NEW200.append(make_case("v05_batch500_0168",
    rc={"project":"supply-chain","repo":"logistix","service":"supplier-portal","task":"check supplier onboarding status"},
    cms=[m("m1","service_memory","The supplier portal tracks onboarding progress through stages: invited, documents_submitted, validated, active, and rejected."),
         m("m2","task_state","Three new packaging suppliers were invited last week; two have submitted documents, one has not responded.")],
    cus=[u("u1","What is the onboarding status of the new supplier PackRight Inc.?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","related_but_useless","temporary_request"],
    notes="READ-only: status check. m1 provides the state machine. m2 is (possibly) stale invitation status from last week."))

NEW200.append(make_case("v05_batch500_0169",
    rc={"project":"healthcare-admin","repo":"medflow","service":"appointment-api","task":"check available appointment slots"},
    cms=[m("m1","service_memory","The appointment API returns available slots for a given provider, date range, and appointment type, excluding blocked time and existing bookings."),
         m("m2","repo_memory","Provider schedules are stored in the provider_schedules table with recurring availability patterns and exception dates.")],
    cus=[u("u1","Are there any open telehealth slots with Dr. Chen next Wednesday between 09:00 and 12:00?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: availability inquiry. Both memories explain the data model."))

NEW200.append(make_case("v05_batch500_0170",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"deadline-calendar","task":"check upcoming contract deadlines"},
    cms=[m("m1","service_memory","The deadline calendar tracks all contract dates: effective, renewal, expiration, and option exercise windows."),
         m("m2","project_memory","The clausekeeper project treats all deadline notifications as internal reminders; it does not send legal notices to counterparties.")],
    cus=[u("u1","Which contracts have a renewal deadline within the next 30 days?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request","project_vs_repo"],
    notes="READ-only: deadline query. m1 has the data. m2 is project-level context about notification scope."))

NEW200.append(make_case("v05_batch500_0171",
    rc={"project":"creator-tools","repo":"artisan","service":"export-queue","task":"check export job status"},
    cms=[m("m1","service_memory","The export queue processes jobs asynchronously and reports status as queued, rendering, encoding, uploading, completed, or failed."),
         m("m2","repo_memory","Export job logs are written to logs/exports/<job_id>.log and retained for 30 days.")],
    cus=[u("u1","What is the status of export job #EXP-2026-0602-0089?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","related_but_useless","temporary_request"],
    notes="READ-only: job status inquiry. m1 explains status states. m2 has log paths but not needed for status check."))

NEW200.append(make_case("v05_batch500_0172",
    rc={"project":"education-platform","repo":"learnhub","service":"quiz-engine","task":"check quiz question statistics"},
    cms=[m("m1","service_memory","The quiz engine tracks per-question statistics including attempt count, correct answer rate, average response time, and discrimination index."),
         m("m2","task_state","Last month's question quality review flagged 15 questions with discrimination index below 0.2 for revision.")],
    cus=[u("u1","What is the correct answer rate for question Q-3391 in the CS-301 final exam?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: question stat inquiry. m1 explains tracking. m2 is an old review flag, not current."))

NEW200.append(make_case("v05_batch500_0173",
    rc={"project":"game-studio","repo":"dungeon-tools","service":"build-pipeline","task":"check build artifact sizes"},
    cms=[m("m1","service_memory","The build pipeline produces per-platform builds with asset bundles, reporting total size and per-bundle breakdown in the build manifest."),
         m("m2","repo_memory","Build manifests are stored in builds/<platform>/<build_id>/manifest.json with asset sizes and compression ratios.")],
    cus=[u("u1","What is the total build size for the latest PS5 release candidate?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: build size inquiry. Both memories help locate the answer."))

NEW200.append(make_case("v05_batch500_0174",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"search-analytics","task":"check popular search queries"},
    cms=[m("m1","service_memory","The search analytics module tracks query frequency, click-through rate, and zero-result queries on a daily basis."),
         m("m2","repo_memory","Search analytics data is stored in the search_analytics table and aggregated into daily reports under reports/search/.")],
    cus=[u("u1","What were the top 5 search queries that returned zero results last week?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: analytics query. Both memories explain data source."))

NEW200.append(make_case("v05_batch500_0175",
    rc={"project":"finance-dashboard","repo":"finboard","service":"position-service","task":"check current portfolio positions"},
    cms=[m("m1","service_memory","The position service aggregates holdings across all accounts and computes market value using the latest cached prices."),
         m("m2","repo_memory","Position data is cached in Redis under position:<account_id> with a 30-second TTL and invalidated on trade execution.")],
    cus=[u("u1","What is the current market value of account A-7742's technology sector holdings?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: position lookup. Both memories explain data model."))

NEW200.append(make_case("v05_batch500_0176",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"audit-trail","task":"check workflow execution history for compliance"},
    cms=[m("m1","service_memory","The audit trail records every workflow state transition with timestamp, user, action, and input/output context snapshots."),
         m("m2","project_memory","The flowcraft project requires that all workflow executions be auditable for 3 years for SOC 2 compliance.")],
    cus=[u("u1","Show me the complete execution history for the purchase_order_approval workflow from May 2026.")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request","project_vs_repo"],
    notes="READ-only: audit query. m1 explains audit trail. m2 provides retention context."))

NEW200.append(make_case("v05_batch500_0177",
    rc={"project":"mobile-field","repo":"field-app","service":"data-usage","task":"check cellular data consumption"},
    cms=[m("m1","service_memory","The data usage tracker monitors bytes sent and received per service module and reports daily and monthly totals."),
         m("m2","repo_memory","Data usage thresholds are configured in config/data_usage/limits.yaml and trigger warnings at 80% and 100% of the monthly cap.")],
    cus=[u("u1","How much cellular data has the sync module used so far this billing cycle?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: data usage inquiry. Both memories help answer."))

NEW200.append(make_case("v05_batch500_0178",
    rc={"project":"ecommerce-platform","repo":"shopengine","service":"review-moderation","task":"check flagged product reviews"},
    cms=[m("m1","service_memory","The review moderation system automatically flags reviews containing profanity, external URLs, or repetitive text, holding them for human moderation."),
         m("m2","task_state","The moderation queue currently has 47 flagged reviews from the weekend that need review by the content team.")],
    cus=[u("u1","How many product reviews are currently awaiting moderation for the electronics category?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","related_but_useless","temporary_request"],
    notes="READ-only: queue inquiry. m1 explains flagging system. m2 is a snapshot (possibly stale) of the overall queue."))

NEW200.append(make_case("v05_batch500_0179",
    rc={"project":"travel-planner","repo":"voyager","service":"rebooking-engine","task":"check rebooking options for a cancelled flight"},
    cms=[m("m1","service_memory","The rebooking engine searches for alternative flights on the same airline within 24 hours of the original departure, prioritizing same-cabin availability."),
         m("m2","service_memory","The old rebooking system only offered refunds, not alternative flights; the rebooking engine was added in 2025.")],
    cus=[u("u1","What alternative flights are available for passenger booking PNR-8XK29W after flight AA-1042 was cancelled?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: rebooking inquiry. m1 explains current engine. m2 is stale legacy context."))

NEW200.append(make_case("v05_batch500_0180",
    rc={"project":"data-platform","repo":"data-jobs","service":"data-catalog","task":"search for datasets matching criteria"},
    cms=[m("m1","service_memory","The data catalog indexes all datasets with metadata including owner, update frequency, row count, and column schemas."),
         m("m2","repo_memory","Dataset metadata is stored in the data_catalog database and searchable via the catalog API at /api/catalog/search.")],
    cus=[u("u1","Find all datasets that contain customer_email columns and are updated daily.")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: catalog search. Both memories provide context."))

NEW200.append(make_case("v05_batch500_0181",
    rc={"project":"learning-assistant","repo":"tutorai","service":"content-search","task":"find learning resources on a specific topic"},
    cms=[m("m1","service_memory","The content search ranks learning resources by relevance to the query, learner's current level, and resource popularity score."),
         m("m2","user_profile","The user prefers video-based resources over text-based when available for the same topic.")],
    cus=[u("u1","Find beginner-level resources on Python list comprehensions, preferably video format.")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","user_profile_boundary","temporary_request"],
    notes="READ-only: content search. m1 explains ranking. m2 is user preference (relevant to the search)."))

NEW200.append(make_case("v05_batch500_0182",
    rc={"project":"customer-support","repo":"helpdesk","service":"ticket-search","task":"find similar historical tickets"},
    cms=[m("m1","service_memory","The ticket search supports similarity search using embedding vectors of ticket descriptions, returning the top 10 most similar resolved tickets."),
         m("m2","repo_memory","Ticket embeddings are generated by the model at models/embeddings/ticket_encoder_v3 and stored in the ticket_embeddings vector index.")],
    cus=[u("u1","Find previously resolved tickets similar to: customer reports that their account is locked after 3 failed password attempts.")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: similarity search. Both memories explain the search mechanism."))

NEW200.append(make_case("v05_batch500_0183",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"dashboard-api","task":"check dashboard sharing permissions"},
    cms=[m("m1","service_memory","Dashboard sharing permissions support view, edit, and admin roles, with sharing managed at the dashboard level."),
         m("m2","repo_memory","Sharing permission configurations are stored in dashboards/<id>/permissions.json.")],
    cus=[u("u1","Who has edit access to the Executive KPI Dashboard?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: permissions inquiry. Both memories help locate the answer."))

NEW200.append(make_case("v05_batch500_0184",
    rc={"project":"healthcare-admin","repo":"medflow","service":"lab-orders","task":"check outstanding lab order status"},
    cms=[m("m1","service_memory","The lab orders service tracks orders from creation through collection, processing, resulting, and review."),
         m("m2","task_state","The lab order STAT-4421 for patient Doe was marked as 'collected' at 09:30 but has not moved to 'processing' as of 11:00.")],
    cus=[u("u1","What is the current status of lab order STAT-4421?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: status check. m1 explains the state machine. m2 is a snapshot that's now stale."))

NEW200.append(make_case("v05_batch500_0185",
    rc={"project":"supply-chain","repo":"logistix","service":"shipment-tracker","task":"check shipment location"},
    cms=[m("m1","service_memory","The shipment tracker updates location at each scan point: pickup, origin_depot, in_transit, destination_depot, out_for_delivery, delivered."),
         m("m2","repo_memory","Shipment tracking events are stored in the shipment_events table with geolocation and timestamps.")],
    cus=[u("u1","Where is shipment SH-2026-8841 right now?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: location inquiry. Both memories help answer."))

NEW200.append(make_case("v05_batch500_0186",
    rc={"project":"legal-docs","repo":"clausekeeper","service":"template-library","task":"find a specific contract template"},
    cms=[m("m1","service_memory","The template library stores contract templates by type, jurisdiction, and last reviewed date, with full-text search over template text."),
         m("m2","repo_memory","Templates are stored as markdown files in templates/<jurisdiction>/<type>/ with YAML frontmatter metadata.")],
    cus=[u("u1","Find the latest reviewed template for a California NDA with a 2-year term.")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: template search. Both memories help locate the template."))

NEW200.append(make_case("v05_batch500_0187",
    rc={"project":"creator-tools","repo":"artisan","service":"asset-browser","task":"search for assets by metadata"},
    cms=[m("m1","service_memory","The asset browser indexes all project assets by file type, creation date, tags, and dimensions, supporting complex metadata queries."),
         m("m2","repo_memory","Asset metadata is stored in .artisan/asset_index.db as a SQLite database rebuilt on project open.")],
    cus=[u("u1","Find all PNG assets tagged with 'UI' and 'button' that are exactly 64x64 pixels.")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: asset search. Both memories explain the index."))

NEW200.append(make_case("v05_batch500_0188",
    rc={"project":"finance-dashboard","repo":"finboard","service":"compliance-api","task":"check compliance report status"},
    cms=[m("m1","service_memory","The compliance API generates regulatory reports on a schedule and tracks each report's generation status, review status, and filing status."),
         m("m2","task_state","The Q2 2026 Form 13F report is due for SEC filing by August 14 and is currently in draft review.")],
    cus=[u("u1","Has the Q1 2026 transaction compliance report been filed?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: report status. m1 explains the compliance report system. m2 is about a different report (Q2)."))

NEW200.append(make_case("v05_batch500_0189",
    rc={"project":"memory-router","repo":"distilled-memory-policy-router","service":"validator","task":"check validation report for a specific batch"},
    cms=[m("m1","service_memory","The validator produces a JSON report for each batch with case-level and aggregate validation results, errors, and distribution stats."),
         m("m2","repo_memory","Validation reports are stored in reports/v05/ with filenames matching the batch name pattern.")],
    cus=[u("u1","Show me the validation errors for case v05_batch300_0042 from the batch300 repair run.")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: report inquiry. Both memories provide context."))

NEW200.append(make_case("v05_batch500_0190",
    rc={"project":"education-platform","repo":"learnhub","service":"discussion-forum","task":"check forum moderation queue"},
    cms=[m("m1","service_memory","The discussion forum auto-moderates posts using a content filter that flags posts containing prohibited terms, excessive caps, or detected spam patterns."),
         m("m2","repo_memory","Flagged posts are held in the moderation_queue table and reviewed via the admin dashboard at /admin/moderation/.")],
    cus=[u("u1","How many posts in the CS-301 forum are currently flagged for moderation?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: moderation queue inquiry. Both memories help answer."))

NEW200.append(make_case("v05_batch500_0191",
    rc={"project":"docs-assistant","repo":"docs-bot","service":"feedback-collector","task":"check documentation page feedback"},
    cms=[m("m1","service_memory","The feedback collector captures page-level ratings (helpful/not helpful) and optional comments, aggregating results per page and per product area."),
         m("m2","task_state","The feedback dashboard was updated last sprint to include a 90-day trend view; the deployment is scheduled for this Friday.")],
    cus=[u("u1","Which documentation pages received the most 'not helpful' ratings in the past 30 days?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: feedback query. m1 explains the collector. m2 is stale deployment plan."))

# ── Fill remaining slots to exactly 200 ─────────────────────────────────────
# Currently we have: joint 70 (001-070), store-only 78 (071-148), read-only 43 (149-191)
# Total: 70 + 78 + 43 = 191. Need 9 more.

# Add 5 more READ+STORE joint to balance, 2 store-only, 2 read-only

NEW200.append(make_case("v05_batch500_0192",
    rc={"project":"learning-assistant","repo":"tutorai","service":"exam-simulator","task":"add timed exam mode with proctoring rules"},
    cms=[m("m1","service_memory","The exam simulator presents quiz questions in a timed sequence and enforces a maximum duration per exam."),
         m("m2","project_memory","The tutorai project does not implement live proctoring; exam integrity is based on time limits and question randomization.")],
    cus=[u("u1","The exam simulator must support a countdown timer that auto-submits when time expires, saving all answered questions and marking unanswered ones as incomplete."),
         u("u2","Add a 5-minute warning notification when the exam timer reaches the final 5 minutes.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","project_vs_repo","target_boundary"],
    notes="m2 is project scope decision (no live proctoring). u1 defines auto-submit behavior -> service_memory. u2 is feature addition -> task_state."))

NEW200.append(make_case("v05_batch500_0193",
    rc={"project":"customer-support","repo":"helpdesk","service":"response-suggester","task":"add AI-powered response suggestions"},
    cms=[m("m1","service_memory","The response suggester currently recommends saved macros and knowledge base articles based on ticket classification."),
         m("m2","repo_memory","Macro and article embeddings are computed offline and stored in the suggestions_index vector database.")],
    cus=[u("u1","The response suggester must generate draft reply text using the ticket context and relevant knowledge articles, presented as an editable suggestion to the agent."),
         u("u2","Add a feedback mechanism where agents rate suggestions as helpful or not, feeding back into the suggestion ranking model.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines draft generation behavior -> service_memory. u2 is feedback mechanism task -> task_state."))

NEW200.append(make_case("v05_batch500_0194",
    rc={"project":"analytics-dashboard","repo":"metricboard","service":"data-transform","task":"add derived column expressions"},
    cms=[m("m1","service_memory","The data transform service creates derived tables by applying SQL expressions to columns from source tables."),
         m("m2","repo_memory","Derived column definitions are stored in config/transforms/<table>.yaml and validated against the source schema.")],
    cus=[u("u1","The data transform service must support CASE/WHEN expressions for creating categorical columns from numeric ranges, with user-defined bucket boundaries."),
         u("u2","Add the CASE expression parser to the transform definition validator.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines CASE expression support -> service_memory. u2 is parser implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0195",
    rc={"project":"data-platform","repo":"data-jobs","service":"stream-processor","task":"add windowed aggregation for streaming data"},
    cms=[m("m1","service_memory","The stream processor consumes Kafka topics and applies stateless transformations before writing to the data lake."),
         m("m2","repo_memory","Stream processing jobs are defined in config/streams/<job_name>.yaml with source topic, transformation, and sink.")],
    cus=[u("u1","The stream processor must support tumbling windows of 60 seconds with late-data handling: events arriving up to 30 seconds late are included in the window they belong to; later events are discarded."),
         u("u2","Add the windowed aggregation operator to the stream processing DSL.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines windowing and late-data policy -> service_memory. u2 is DSL addition -> task_state."))

NEW200.append(make_case("v05_batch500_0196",
    rc={"project":"mobile-field","repo":"field-app","service":"media-uploader","task":"add chunked upload with resume capability"},
    cms=[m("m1","service_memory","The media uploader sends photos and videos to the server using multipart upload with a 10MB chunk size."),
         m("m2","repo_memory","Upload configuration including chunk size and retry count is in config/upload/media_upload.yaml.")],
    cus=[u("u1","The media uploader must support resumable uploads: if the connection drops, the upload resumes from the last acknowledged chunk instead of restarting from the beginning."),
         u("u2","Add chunk acknowledgment tracking using the server-returned upload_id and chunk index.")],
    read=["m1","m2"], store=[st("service_memory","u1"),st("task_state","u2")], skip=[],
    tags=["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    notes="u1 defines resumable upload behavior -> service_memory. u2 is tracking implementation -> task_state."))

NEW200.append(make_case("v05_batch500_0197",
    rc={"project":"workflow-automation","repo":"flowcraft","service":"template-engine","task":"define workflow template versioning rules"},
    cms=[],
    cus=[u("u1","The template engine must version every workflow template change with a semantic version number, where MAJOR bumps indicate breaking input schema changes."),
         u("u2","Running workflow instances must continue using the template version they were started with, even if a newer version is published."),
         u("u3","The template registry currently has 23 active templates but no version history for the first 10 created before versioning was added.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("task_state","u3")], skip=[],
    tags=["store_skip_only","service_invariant","task_progress","repo_vs_service","service_vs_task_state"],
    notes="u1 defines versioning semantics -> service_memory. u2 defines instance-template binding -> service_memory. u3 describes current legacy state -> task_state."))

NEW200.append(make_case("v05_batch500_0198",
    rc={"project":"supply-chain","repo":"logistix","service":"returns-processor","task":"define return authorization rules"},
    cms=[],
    cus=[u("u1","The returns processor must auto-authorize returns within 30 days of delivery for items in resalable condition, and route all other returns to manual review."),
         u("u2","Returned items flagged as 'defective' must be routed to the quality inspection queue instead of being restocked."),
         u("u3","The returns processing SLA requires that all auto-authorized returns receive a return label within 1 hour of request.")],
    read=[], store=[st("service_memory","u1"),st("service_memory","u2"),st("service_memory","u3")], skip=[],
    tags=["store_skip_only","service_invariant"],
    notes="u1 defines auto-authorization rules -> service_memory. u2 defines defective routing -> service_memory. u3 defines SLA -> service_memory."))

NEW200.append(make_case("v05_batch500_0199",
    rc={"project":"healthcare-admin","repo":"medflow","service":"claims-validator","task":"verify insurance claim pre-submission"},
    cms=[m("m1","service_memory","The claims validator checks claim fields against payer-specific rules before submission, including required fields, valid codes, and patient eligibility."),
         m("m2","task_state","The UnitedHealth payer rules were updated last week to require prior authorization numbers on all specialist visit claims.")],
    cus=[u("u1","Does claim CL-2026-8891 pass all pre-submission validation checks for BlueCross?")],
    read=["m1"], store=[], skip=["u1"],
    tags=["read_only","stale_memory","temporary_request"],
    notes="READ-only: validation check. m1 explains validator. m2 is stale payer update (different payer)."))

NEW200.append(make_case("v05_batch500_0200",
    rc={"project":"creator-tools","repo":"artisan","service":"timeline","task":"verify animation keyframe interpolation"},
    cms=[m("m1","service_memory","The timeline renders animation by interpolating between keyframes using the easing function specified per keyframe: linear, ease-in, ease-out, or ease-in-out."),
         m("m2","repo_memory","Animation data is stored in .artisan/animations/<clip_name>.json with keyframe arrays per property.")],
    cus=[u("u1","What easing function is used for the opacity keyframe transition at 2.5 seconds in the intro animation?")],
    read=["m1","m2"], store=[], skip=["u1"],
    tags=["read_only","temporary_request"],
    notes="READ-only: specific animation query. Both memories provide context."))


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION, WRITING, AND REPORTING
# ═══════════════════════════════════════════════════════════════════════════════

def validate_new200(new200: list[dict]) -> bool:
    """Validate all 200 new cases structurally."""
    from src.v04.case_validator import validate_case
    from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

    all_ok = True
    for case in new200:
        result = validate_case(case)
        if not result["valid"]:
            print(f"VALIDATION FAILED: {case['case_id']}")
            for e in result["errors"]:
                print(f"  {e}")
            all_ok = False

        # DSL parse check
        dsl = case["gold"]["dsl"]
        mem_ids = [m["memory_id"] for m in case["candidate_memories"]]
        unit_ids = [u["unit_id"] for u in case["current_units"]]
        parsed = parse_policy_dsl(dsl, mem_ids, unit_ids, LEGAL_TARGETS)
        if not parsed["validation"]["valid"]:
            print(f"DSL PARSE FAILED: {case['case_id']}")
            for e in parsed["validation"]["errors"]:
                print(f"  {e}")
            all_ok = False

        # Canonical consistency
        parsed_read = {item["memory_id"] for item in parsed["read"]}
        parsed_store = {item["unit_id"]: item["target"] for item in parsed["store"]}
        parsed_skip = {item["unit_id"] for item in parsed["skip"]}
        gold_read = set(case["gold"]["read"])
        gold_store = {s["unit_id"]: s["target"] for s in case["gold"]["store"]}
        gold_skip = set(case["gold"]["skip"])

        if parsed_read != gold_read:
            print(f"READ MISMATCH: {case['case_id']} parsed={parsed_read} gold={gold_read}")
            all_ok = False
        if parsed_store != gold_store:
            print(f"STORE MISMATCH: {case['case_id']} parsed={parsed_store} gold={gold_store}")
            all_ok = False
        if parsed_skip != gold_skip:
            print(f"SKIP MISMATCH: {case['case_id']} parsed={parsed_skip} gold={gold_skip}")
            all_ok = False

    return all_ok


def check_leakage(new200: list[dict], batch300: list[dict]) -> dict:
    """Check for ID and content leakage."""
    from src.v04.case_validator import validate_jsonl_file

    new_ids = {c["case_id"] for c in new200}
    old_ids = {c["case_id"] for c in batch300}

    # Check new200 uniqueness
    assert len(new_ids) == len(new200), f"Duplicate case_ids in new200: {len(new200)} vs {len(new_ids)}"

    # Check overlap with batch300
    overlap = new_ids & old_ids
    assert not overlap, f"Case ID overlap with batch300: {overlap}"

    # Check overlap with subset50
    subset50_path = ROOT / "data/v04/model_predictions/p5_subset50_case_ids.txt"
    subset50_ids = set(subset50_path.read_text().strip().splitlines()) if subset50_path.exists() else set()
    overlap_subset = new_ids & subset50_ids
    assert not overlap_subset, f"Case ID overlap with subset50: {overlap_subset}"

    # Check few-shot overlap
    fewshot_path = ROOT / "data/v04/model_predictions/qwen3_4b_unit_dsl_fewshot_examples.jsonl"
    fewshot_ids: set[str] = set()
    if fewshot_path.exists():
        with fewshot_path.open() as f:
            for line in f:
                if line.strip():
                    fewshot_ids.add(json.loads(line)["case_id"])
    overlap_fewshot = new_ids & fewshot_ids
    assert not overlap_fewshot, f"Case ID overlap with few-shot: {overlap_fewshot}"

    # Check duplicate unit texts within new200
    unit_texts = [u["text"] for c in new200 for u in c["current_units"]]
    from collections import Counter as Ctr
    dup_units = {t: c for t, c in Ctr(unit_texts).items() if c > 1}
    if dup_units:
        print(f"WARNING: Duplicate unit texts in new200: {list(dup_units.keys())[:5]}")

    # Check duplicate memory texts within new200
    mem_texts = [m["content"] for c in new200 for m in c["candidate_memories"]]
    dup_mems = {t: c for t, c in Ctr(mem_texts).items() if c > 1}
    if dup_mems:
        print(f"WARNING: Duplicate memory texts in new200: {list(dup_mems.keys())[:5]}")

    return {"overlap_batch300": len(overlap), "overlap_subset50": len(overlap_subset),
            "overlap_fewshot": len(overlap_fewshot), "dup_units": len(dup_units), "dup_mems": len(dup_mems)}


def compute_stats(cases: list[dict]) -> dict:
    """Compute distribution statistics for a set of cases."""
    from collections import Counter

    targets = Counter()
    shapes = Counter()
    tags = Counter()
    domains = Counter()

    for c in cases:
        for s in c["gold"]["store"]:
            targets[s["target"]] += 1
        has_read = bool(c["gold"]["read"])
        has_store = bool(c["gold"]["store"])
        if has_read and has_store:
            shapes["read_store_joint"] += 1
        elif has_read:
            shapes["read_only"] += 1
        else:
            shapes["store_skip_only"] += 1
        for t in c["tags"]:
            tags[t] += 1
        domains[c["runtime_context"]["project"]] += 1

    total_cases = len(cases)
    total_units = sum(targets.values())
    total_read = sum(len(c["gold"]["read"]) for c in cases)
    total_skip = sum(len(c["gold"]["skip"]) for c in cases)

    return {
        "total_cases": total_cases,
        "total_store_units": total_units,
        "total_read_refs": total_read,
        "total_skip_units": total_skip,
        "targets": dict(targets),
        "target_pcts": {t: round(c/total_units*100, 1) for t, c in targets.items()} if total_units else {},
        "shapes": dict(shapes),
        "shape_pcts": {s: round(c/total_cases*100, 1) for s, c in shapes.items()} if total_cases else {},
        "tags": dict(tags),
        "domains": dict(domains),
    }


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Generate batch500 from batch300 + new200.")
    ap.add_argument("--cases", default=None, help="Output path for batch500 cases JSONL")
    ap.add_argument("--out", default=None, help="Output path for batch500 SFT messages JSONL")
    ap.add_argument("--source", default="v05_batch500_dry_run", help="Source tag for SFT messages")
    args = ap.parse_args()

    # Load batch300
    batch300_path = ROOT / "data/v05/batches/v05_batch300_cases.jsonl"
    batch300 = []
    with batch300_path.open() as f:
        for line in f:
            if line.strip():
                batch300.append(json.loads(line))
    print(f"Loaded {len(batch300)} cases from batch300")

    # Validate new200
    print(f"\nValidating {len(NEW200)} new200 cases...")
    if not validate_new200(NEW200):
        print("NEW200 VALIDATION FAILED!")
        return 1
    print("All new200 cases structurally valid.")

    # Leakage check
    print("\nChecking leakage...")
    leakage = check_leakage(NEW200, batch300)
    print(f"Leakage: overlap_batch300={leakage['overlap_batch300']}, "
          f"overlap_subset50={leakage['overlap_subset50']}, "
          f"overlap_fewshot={leakage['overlap_fewshot']}, "
          f"dup_units={leakage['dup_units']}, dup_mems={leakage['dup_mems']}")

    # Merge batch500
    batch500 = batch300 + NEW200
    batch500_cases_path = args.cases or str(ROOT / "data/v05/batches/v05_batch500_cases.jsonl")
    Path(batch500_cases_path).parent.mkdir(parents=True, exist_ok=True)
    with open(batch500_cases_path, "w", encoding="utf-8") as f:
        for case in batch500:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(batch500)} cases to {batch500_cases_path}")

    # Write new200 separately
    new200_path = str(ROOT / "data/v05/batches/v05_batch500_new200_cases.jsonl")
    with open(new200_path, "w", encoding="utf-8") as f:
        for case in NEW200:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"Wrote {len(NEW200)} new200 cases to {new200_path}")

    # Generate SFT messages
    sft_path = args.out or str(ROOT / "data/v05/batches/v05_batch500_sft_messages.jsonl")
    sft_msgs = [build_sft_message(c, args.source) for c in batch500]
    with open(sft_path, "w", encoding="utf-8") as f:
        for msg in sft_msgs:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(sft_msgs)} SFT messages to {sft_path}")

    # Validate SFT messages
    sft_ok = True
    for case, msg in zip(batch500, sft_msgs):
        if msg["messages"][2]["content"] != case["gold"]["dsl"]:
            print(f"SFT ASSISTANT MISMATCH: {case['case_id']}")
            sft_ok = False
        if "```" in msg["messages"][2]["content"]:
            print(f"SFT MARKDOWN: {case['case_id']}")
            sft_ok = False
        if msg["messages"][2]["content"].strip().startswith("{"):
            print(f"SFT JSON: {case['case_id']}")
            sft_ok = False
        if msg["metadata"]["is_final_train_data"]:
            print(f"SFT IS_FINAL: {case['case_id']}")
            sft_ok = False
    print(f"SFT validation: {'OK' if sft_ok else 'ERRORS FOUND'}")

    # Stats
    print("\n" + "=" * 60)
    new200_stats = compute_stats(NEW200)
    batch500_stats = compute_stats(batch500)

    print("NEW200 SUMMARY:")
    print(f"  Cases: {new200_stats['total_cases']}")
    print(f"  STORE units: {new200_stats['total_store_units']}")
    print(f"  Targets: {new200_stats['targets']}")
    print(f"  Target %: {new200_stats['target_pcts']}")
    print(f"  Shapes: {new200_stats['shape_pcts']}")
    print(f"  Domains: {len(new200_stats['domains'])}")

    print(f"\nBATCH500 SUMMARY:")
    print(f"  Cases: {batch500_stats['total_cases']}")
    print(f"  STORE units: {batch500_stats['total_store_units']}")
    print(f"  Targets: {batch500_stats['targets']}")
    print(f"  Target %: {batch500_stats['target_pcts']}")
    print(f"  Shapes: {batch500_stats['shape_pcts']}")

    return 0 if sft_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
