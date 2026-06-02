"""Repair batch300 after independent review: replace 51 template cases + 4 label corrections.

Context 5.1-D: repair batch300 after independent review.
"""
from __future__ import annotations

import json, sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.v05.render_sft_messages import SYSTEM_PROMPT, render_user_input
from src.v04.case_validator import validate_case, validate_jsonl_file
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS


def _c(cid, project, repo, service, task, memories, units, gold, tags, notes=""):
    return {"case_id":cid,"runtime_context":{"project":project,"repo":repo,"service":service,"task":task},
            "candidate_memories":memories,"current_units":units,"gold":gold,"tags":tags,"notes":notes}

# ═══════════════════════════════════════════════════════════════
# 51 HAND-CRAFTED REPLACEMENT CASES (v05_batch300_0050–0100)
# ═══════════════════════════════════════════════════════════════
# Design targets:
#   READ+STORE joint: 48–51  (all 51)
#   service_memory STORE: 30–40
#   task_state STORE: 20–30
#   repo_memory STORE: 12–20
#   project_memory STORE: 5–10
#   user_profile STORE: 0–3
# Every case has unique semantic content. No fill-in-the-blank templates.
# Spanning all 13 domains.

REPLACEMENT51 = []

def add(*a): REPLACEMENT51.append(_c(*a))

# ── 0050: svc + task + repo on data-platform, sensitive boundary ──
add("v05_batch300_0050", "data-platform", "data-jobs", "pipeline", "update retry wrapper with disk spill",
    [{"memory_id":"m1","target":"service_memory","content":"The pipeline retry wrapper retries transient network errors 3 times with 1-second backoff."},
     {"memory_id":"m2","target":"repo_memory","content":"Pipeline job logs are written to /var/log/pipeline/job_${RUN_ID}.log on the job runner host."},
     {"memory_id":"m3","target":"service_memory","content":"The old v1 pipeline buffered all retry state in memory and lost it on crash."}],
    [{"unit_id":"u1","text":"The retry wrapper must spill retry state to disk when the in-memory buffer exceeds 100MB, using a tmpfs mount at /pipeline/spill/."},
     {"unit_id":"u2","text":"Add a disk-spill health check that alerts when the spill directory exceeds 80% of the allocated tmpfs size."},
     {"unit_id":"u3","text":"My SSH key for the staging pipeline host is pipeline-stage-ed25519 — it should be in the secrets vault."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"task_state","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory","target_boundary"],
    "READ+STORE joint with stale. u1 defines durable spill-to-disk behavior → service_memory. u2 is a health check implementation task → task_state. u3 contains the spill directory path → repo_memory. Note: the SSH key is mentioned in u3 as a reference to where it should live; the text is about the key's location, not the key value itself, so it's not treated as sensitive content to SKIP."),

# ── 0051: svc+svc+task on mobile-field, stale detection ──
add("v05_batch300_0051", "mobile-field", "field-app", "notification", "redesign notification batching windows",
    [{"memory_id":"m1","target":"service_memory","content":"The notification service groups messages by priority before delivering via FCM, sending at most one batch per 2 minutes."},
     {"memory_id":"m2","target":"task_state","content":"The current batching window of 2 minutes was chosen arbitrarily in January without load testing."},
     {"memory_id":"m3","target":"service_memory","content":"The legacy push module sent every notification immediately with no batching, causing FCM rate-limit errors."}],
    [{"unit_id":"u1","text":"The notification service must use adaptive batching: 30-second windows during peak hours (08:00-22:00) and 5-minute windows during off-peak."},
     {"unit_id":"u2","text":"Low-priority notifications (marketing, tips) must not delay high-priority notifications (alerts, sync failures) within the same window."},
     {"unit_id":"u3","text":"Run a 2-week A/B test comparing the adaptive batching against the fixed 2-minute window on 10% of users."}],
    {"read":["m1"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory","service_vs_task_state"],
    "READ+STORE joint with dual svc + stale. Reads m1 (current batching) but skips m2 (stale/arbitrary choice) and m3 (stale legacy). u1 and u2 define durable adaptive batching → service_memory. u3 is A/B test task → task_state."),

# ── 0052: project+task on finance-dashboard, compliance boundary ──
add("v05_batch300_0052", "finance-dashboard", "finboard", "aggregator", "implement data anonymization for analytics",
    [{"memory_id":"m1","target":"project_memory","content":"The finboard project must comply with GDPR data minimization principles for all EU customer transactions."},
     {"memory_id":"m2","target":"service_memory","content":"The aggregator currently stores raw transaction records with full customer name and account ID in the daily_aggregates table."},
     {"memory_id":"m3","target":"repo_memory","content":"Anonymization rules are defined in config/aggregator/anonymization.yaml with a list of PII columns to mask."}],
    [{"unit_id":"u1","text":"The aggregator must hash customer names and account IDs with SHA-256 before writing them to daily_aggregates, and never store them in plain text."},
     {"unit_id":"u2","text":"All finboard services must include a data-retention label on every log line: retention_30d, retention_7y, or retention_permanent."},
     {"unit_id":"u3","text":"Run the anonymization migration on a staging clone of the production DB and verify hashed values match across all tables."}],
    {"read":["m1","m2","m3"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"project_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE service_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","project_vs_repo","service_vs_task_state","target_boundary"],
    "READ+STORE joint with project vs service distinction. u1 is a durable aggregator anonymization behavior → service_memory. u2 is a cross-service retention labeling policy ('All finboard services') → project_memory. u3 is migration verification task → task_state."),

# ── 0053: svc+repo on travel-planner, rate-limiting ──
add("v05_batch300_0053", "travel-planner", "voyager", "pricing", "document rate-limit backpressure strategy",
    [{"memory_id":"m1","target":"service_memory","content":"The pricing service calls airline APIs with a rate limit of 100 requests per minute and caches responses for 5 minutes."},
     {"memory_id":"m2","target":"repo_memory","content":"Airline API integration documentation lives under docs/pricing/airline_apis/ with one markdown file per airline."}],
    [{"unit_id":"u1","text":"When the pricing service detects a 429 rate-limit response from an airline API, it must switch to cached fares for that airline and retry the live query after 60 seconds."},
     {"unit_id":"u2","text":"Document the rate-limit backpressure strategy in docs/pricing/rate_limit_handling.md with per-airline fallback rules."},
     {"unit_id":"u3","text":"Add a rate-limit dashboard widget to the pricing monitoring page showing per-airline 429 counts."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress"],
    "READ+STORE joint. u1 defines durable rate-limit backpressure behavior → service_memory. u2 is documentation path convention → repo_memory. u3 is dashboard widget task → task_state."),

# ── 0054: svc+repo on education-platform, audit trail ──
add("v05_batch300_0054", "education-platform", "learnhub", "grading", "implement grade change audit trail",
    [{"memory_id":"m1","target":"service_memory","content":"The grading service writes final grades to the submissions table with graded_at and grader_id columns."},
     {"memory_id":"m2","target":"project_memory","content":"The learnhub project requires an immutable audit trail for all grade changes to meet accreditation standards."},
     {"memory_id":"m3","target":"repo_memory","content":"The grade_audit table schema is defined in db/migrations/grading/V003__grade_audit.sql."}],
    [{"unit_id":"u1","text":"Every grade change must insert a row into grade_audit with old_grade, new_grade, changed_by, change_reason, and changed_at. The row must be insert-only — never updated or deleted."},
     {"unit_id":"u2","text":"Store the grade_audit table migration as an append-only log in db/migrations/grading/audit/ with one file per year."},
     {"unit_id":"u3","text":"Write a quarterly audit report query that lists all grade changes grouped by course and instructor."}],
    {"read":["m1","m2","m3"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress"],
    "READ+STORE joint. u1 defines immutable audit behavior → service_memory. u2 is migration file organization → repo_memory. u3 is report writing task → task_state."),

# ── 0055: svc+task on game-studio, shader compilation cache ──
add("v05_batch300_0055", "game-studio", "dungeon-tools", "build-system", "add shader compilation cache",
    [{"memory_id":"m1","target":"service_memory","content":"The build system compiles all shaders from source on every build, taking approximately 12 minutes for the full shader library."},
     {"memory_id":"m2","target":"repo_memory","content":"Shader source files live under assets/shaders/ and compiled outputs go to build/shaders/{platform}/."},
     {"memory_id":"m3","target":"task_state","content":"The last build optimization attempt reduced texture compression time by 40% but didn't touch shader compilation."}],
    [{"unit_id":"u1","text":"The build system must cache compiled shader binaries keyed by source file hash and platform target. Only recompile shaders whose source hash changed."},
     {"unit_id":"u2","text":"The shader cache must live under build/cache/shaders/{platform}/ and survive clean builds unless the --invalidate-shaders flag is passed."},
     {"unit_id":"u3","text":"Benchmark the full build with and without shader caching on Windows and PS5 targets before the next release."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress","stale_memory"],
    "READ+STORE joint with stale. Reads m1 (current build) and m2 (paths). Skips m3 (stale, unrelated optimization). u1 defines durable caching behavior → service_memory. u2 is cache path convention → repo_memory. u3 is benchmarking task → task_state."),

# ── 0056: svc+task on ecommerce, idempotency key generation ──
add("v05_batch300_0056", "ecommerce-platform", "shopengine", "orders", "standardize idempotency across order ops",
    [{"memory_id":"m1","target":"service_memory","content":"The orders service uses idempotency keys for payment processing but not for order creation or status updates."},
     {"memory_id":"m2","target":"repo_memory","content":"Idempotency key format is defined in docs/orders/idempotency.md as ORDER-{client_id}-{nonce}."}],
    [{"unit_id":"u1","text":"Extend idempotency key enforcement to all mutating order endpoints: create, update_status, add_item, and cancel."},
     {"unit_id":"u2","text":"The order service must reject duplicate idempotency keys with a 409 Conflict response containing the original request's result, not just an error message."},
     {"unit_id":"u3","text":"Update the idempotency documentation at docs/orders/idempotency.md to list all protected endpoints and their key formats."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress"],
    "READ+STORE joint. u1 is a scoped extension task → task_state (implementation plan with specific endpoints). u2 is durable idempotency rejection behavior → service_memory. u3 is doc update → repo_memory."),

# ── 0057: project+task on analytics-dashboard, multi-tenancy ──
add("v05_batch300_0057", "analytics-dashboard", "databoard", "query-engine", "enforce tenant isolation at query layer",
    [{"memory_id":"m1","target":"service_memory","content":"The query engine currently runs all queries against a shared analytics database without tenant-scoped filtering."},
     {"memory_id":"m2","target":"project_memory","content":"The databoard project's multi-tenancy model assigns each organization a tenant_id that must be enforced at every data access layer."},
     {"memory_id":"m3","target":"repo_memory","content":"Tenant configuration is managed in config/tenants/ with one YAML file per tenant containing the tenant_id and database schema prefix."}],
    [{"unit_id":"u1","text":"The query engine must prepend a WHERE tenant_id = :current_tenant clause to every user-initiated query. The tenant_id comes from the authenticated session, never from user input."},
     {"unit_id":"u2","text":"The databoard project categorically prohibits cross-tenant data access in any component; violating this is a P0 security incident."},
     {"unit_id":"u3","text":"Add an integration test that attempts to access another tenant's data and verifies the query engine blocks it."}],
    {"read":["m1","m2","m3"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"project_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE service_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","project_vs_repo","target_boundary"],
    "READ+STORE joint. u1 defines durable tenant isolation behavior for the query engine → service_memory. u2 is a cross-component security prohibition ('categorically prohibits') → project_memory. u3 is test writing task → task_state."),

# ── 0058: svc+task on customer-support, SLA escalation ──
add("v05_batch300_0058", "customer-support", "helpdesk", "routing", "implement SLA-based ticket escalation",
    [{"memory_id":"m1","target":"service_memory","content":"The routing service assigns tickets to agents based on skill tags and current workload, but does not consider SLA deadlines."},
     {"memory_id":"m2","target":"project_memory","content":"The helpdesk project SLA mandates: critical tickets must receive first response within 1 hour, normal within 4 hours."},
     {"memory_id":"m3","target":"task_state","content":"Last month's SLA report showed 8% of critical tickets breached the 1-hour first-response window."}],
    [{"unit_id":"u1","text":"The routing service must escalate any ticket that has been unacknowledged for 80% of its SLA window: reassign to the team lead and send a PagerDuty alert."},
     {"unit_id":"u2","text":"Escalated tickets must be flagged with a visual indicator in the agent dashboard and sorted to the top of the queue regardless of other priority rules."},
     {"unit_id":"u3","text":"Run the SLA report weekly and compare breach rates before and after the escalation feature is deployed."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory"],
    "READ+STORE joint with stale. Reads m1 (current routing) and m2 (SLA definition — needed for u1 threshold). Skips m3 (stale monthly SLA report). u1 and u2 define durable escalation behaviors → service_memory. u3 is monitoring task → task_state."),

# ── 0059: repo+task on docs-assistant, search index segmentation ──
add("v05_batch300_0059", "docs-assistant", "docs-bot", "indexer", "segment search index by doc version",
    [{"memory_id":"m1","target":"service_memory","content":"The indexer builds a single inverted index for all document versions, which causes stale results when searching for current-version APIs."},
     {"memory_id":"m2","target":"repo_memory","content":"Document version tags are extracted from the docs repo's git tags following the pattern v{major}.{minor}.{patch}."}],
    [{"unit_id":"u1","text":"The indexer must segment the inverted index by document version. The default search scope is the latest stable version, with a dropdown to select older versions."},
     {"unit_id":"u2","text":"Store versioned indexes under data/indexer/versions/{version_tag}/ with a symlink 'latest' pointing to the most recent stable version."},
     {"unit_id":"u3","text":"Rebuild all versioned indexes from scratch and validate that searches return only results from the selected version."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","repo_vs_service","task_progress"],
    "READ+STORE joint. u1 defines versioned index behavior → service_memory. u2 is index storage path convention → repo_memory. u3 is rebuild/validation task → task_state."),

# ── 0060: svc+task on workflow-automation, circuit breaker ──
add("v05_batch300_0060", "workflow-automation", "flowcraft", "orchestrator", "add circuit breaker for downstream failures",
    [{"memory_id":"m1","target":"service_memory","content":"The orchestrator calls external services for each workflow step and retries on failure, but has no circuit breaker pattern."},
     {"memory_id":"m2","target":"service_memory","content":"Last week's production incident: the payment gateway was down for 45 minutes, and the orchestrator retried 10,000+ payment steps, saturating connection pools."}],
    [{"unit_id":"u1","text":"The orchestrator must implement a circuit breaker per external service: open the circuit after 5 consecutive failures in a 60-second window, then half-open after 120 seconds with a single probe request."},
     {"unit_id":"u2","text":"When a circuit is open, the orchestrator must mark affected workflow steps as deferred rather than failed, and resume them automatically when the circuit closes."},
     {"unit_id":"u3","text":"Document the circuit breaker design in docs/orchestrator/circuit_breaker.md with a state diagram and per-service thresholds."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention"],
    "READ+STORE joint with incident context (m2 provides rationale but isn't stale — it's the motivating incident). u1 and u2 define durable circuit breaker behavior → service_memory. u3 is documentation path convention → repo_memory."),

# ── 0061: svc+repo on learning-assistant, spaced repetition ──
add("v05_batch300_0061", "learning-assistant", "studybuddy", "quiz-generator", "implement spaced repetition scheduling",
    [{"memory_id":"m1","target":"service_memory","content":"The quiz generator currently selects questions randomly from the question bank without considering the student's past performance or review history."},
     {"memory_id":"m2","target":"repo_memory","content":"Student quiz history is stored in the quiz_attempts table with columns student_id, question_id, correct, and attempted_at."},
     {"memory_id":"m3","target":"service_memory","content":"The legacy flashcard system used static Leitner boxes with fixed intervals of 1, 3, 7, and 30 days."}],
    [{"unit_id":"u1","text":"The quiz generator must use a spaced repetition algorithm (SM-2 variant) that schedules question review based on past performance: correct answers increase the interval by a factor of 2.5, incorrect answers reset to 1 day."},
     {"unit_id":"u2","text":"The spaced repetition schedule must be stored per student in a new table spaced_repetition_schedule with columns student_id, question_id, next_review_at, and ease_factor."},
     {"unit_id":"u3","text":"I prefer daily quiz reminders at 08:00 local time with a maximum of 20 review questions per session."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"user_profile","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE user_profile u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","user_profile_boundary","stale_memory"],
    "READ+STORE joint with stale + user_profile. Reads m1 (current quiz) and m2 (quiz history table). Skips m3 (stale legacy Leitner). u1 defines spaced repetition algorithm → service_memory. u2 is DB schema → repo_memory. u3 is stable user preference for quiz scheduling → user_profile."),

# ── 0062: svc+svc on memory-router, prompt builder output validation ──
add("v05_batch300_0062", "memory-router", "distilled-memory-policy-router", "prompt_builder", "add output validation to prompt builder",
    [{"memory_id":"m1","target":"service_memory","content":"The prompt builder renders runtime_context, candidate_memories, and current_units into a structured text format for the model."},
     {"memory_id":"m2","target":"service_memory","content":"The parser validates model output against DSL rules: duplicate detection, missing unit assignment, unknown targets, and STORE/SKIP conflicts."},
     {"memory_id":"m3","target":"repo_memory","content":"Prompt builder source is under src/v04/prompt_builder.py with tests under tests/v04/test_prompt_builder.py."}],
    [{"unit_id":"u1","text":"The prompt builder must validate its own output before sending it to the model: check that every current unit ID is rendered exactly once, candidate memory IDs are not truncated, and the system prompt is included."},
     {"unit_id":"u2","text":"If validation fails, the prompt builder must log the error to prompt_builder_errors.log and fall back to a minimal safe prompt containing only the system instruction and a truncated version of the user input."},
     {"unit_id":"u3","text":"Write a unit test that feeds the prompt builder a truncated candidate_memories list and verifies the validation catches it."}],
    {"read":["m1","m2","m3"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. Reads all three (all relevant: m1 for render behavior, m2 for parser validation model, m3 for test paths). u1 and u2 define durable prompt builder validation behavior → service_memory. u3 is test writing task → task_state."),

# ── 0063: svc+task+sensitive on ecommerce, payment tokenization ──
add("v05_batch300_0063", "ecommerce-platform", "shopengine", "orders", "enforce payment tokenization at service boundary",
    [{"memory_id":"m1","target":"service_memory","content":"The orders service receives raw payment information from the checkout form and passes it to the payment processor via the PSP SDK."},
     {"memory_id":"m2","target":"project_memory","content":"The shopengine project PCI compliance policy prohibits storing raw card numbers in any service log, database, or cache."}],
    [{"unit_id":"u1","text":"The orders service must tokenize payment information before any internal processing: replace the raw card number with a PSP-issued token immediately after the checkout form is submitted."},
     {"unit_id":"u2","text":"The raw card number must never appear in any log line, even at DEBUG level. Use the token ID in all log messages referencing the payment."},
     {"unit_id":"u3","text":"Remember to rotate the PSP API key before the next PCI audit — the current key expires in 30 days."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","sensitive_boundary"],
    "READ+STORE joint. u1 and u2 define durable tokenization and logging behaviors → service_memory. u3 is a key rotation reminder → task_state (future action, not a permanent rule). Note: u3 mentions an API key but does not contain the key value — it's about a rotation action."),

# ── 0064: svc+repo on customer-support, ticket merge deadline ──
add("v05_batch300_0064", "customer-support", "helpdesk", "ticketing", "add ticket merge deadline enforcement",
    [{"memory_id":"m1","target":"service_memory","content":"The ticketing service supports merging duplicate tickets. When merged, the newer ticket is closed and linked to the older ticket as the canonical record."},
     {"memory_id":"m2","target":"repo_memory","content":"Ticket merge rules are configured in config/ticketing/merge_rules.yaml with similarity thresholds for subject, body, and contact email."}],
    [{"unit_id":"u1","text":"Tickets can only be merged within 72 hours of the newer ticket's creation. After 72 hours, the merge must be approved by a team lead with a written justification."},
     {"unit_id":"u2","text":"The 72-hour merge deadline must be configurable per ticket category in config/ticketing/merge_rules.yaml with the deadline_hours key."},
     {"unit_id":"u3","text":"Audit last month's ticket merges and identify any that would have been blocked by the 72-hour rule for team lead review."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress"],
    "READ+STORE joint. u1 defines durable merge deadline behavior → service_memory. u2 is config location/key → repo_memory. u3 is audit task → task_state."),

# ── 0065: svc+task on travel-planner, booking hold expiration ──
add("v05_batch300_0065", "travel-planner", "voyager", "booking", "add booking hold with expiration",
    [{"memory_id":"m1","target":"service_memory","content":"The booking service currently reserves seats immediately upon payment authorization and issues the ticket within 2 minutes."},
     {"memory_id":"m2","target":"service_memory","content":"Airline partner agreements require that held but unpaid bookings be released after 24 hours to avoid inventory blocking."},
     {"memory_id":"m3","target":"repo_memory","content":"Booking hold configuration is managed in config/booking/hold_policy.yaml with airline-specific TTL values."}],
    [{"unit_id":"u1","text":"Add a booking hold feature: when a user selects flights but has not yet paid, hold the seats for 20 minutes. If payment is not completed within the hold window, release the seats and show a 'hold expired' message."},
     {"unit_id":"u2","text":"The hold must prevent other users from booking the same seats during the hold window. Expired holds must release seats within 5 seconds of expiration, not on a polling interval."},
     {"unit_id":"u3","text":"Deploy the booking hold feature behind a feature flag and enable it for 5% of users initially."}],
    {"read":["m1","m2","m3"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE task_state u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    "READ+STORE joint. u1 is an implementation plan → task_state. u2 is a durable seat-hold release constraint → service_memory. u3 is deployment plan → task_state."),

# ── 0066: project+task on game-studio, localization scope ──
add("v05_batch300_0066", "game-studio", "dungeon-tools", "build-system", "define localization scope and pipeline",
    [{"memory_id":"m1","target":"project_memory","content":"The dungeon-tools project currently ships in English only with no localization pipeline."},
     {"memory_id":"m2","target":"repo_memory","content":"UI string assets are stored in assets/strings/en/ with one JSON file per screen."}],
    [{"unit_id":"u1","text":"The dungeon-tools project will support localization for EFIGS languages (English, French, Italian, German, Spanish) starting with the Q3 release. Asian languages (CJK) are deferred to next year."},
     {"unit_id":"u2","text":"Localized string files must live under assets/strings/{locale}/ with the same filename as the English source. Missing translations must fall back to English, not show placeholder text."},
     {"unit_id":"u3","text":"The build system must validate that all locale directories have the same set of JSON files as the English source and fail the build if any file is missing."}],
    {"read":["m1","m2"],"store":[{"target":"project_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"service_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE project_memory u1\nSTORE repo_memory u2\nSTORE service_memory u3\nSKIP NONE"},
    ["read_store_joint","project_vs_repo","repo_vs_service","target_boundary"],
    "READ+STORE joint. u1 is project-level scope decision (which languages, when) → project_memory. u2 is repo-level directory convention → repo_memory. u3 is build system validation behavior → service_memory."),

# ── 0067: svc+task+stale on data-platform, dead-letter queue retention ──
add("v05_batch300_0067", "data-platform", "data-jobs", "pipeline", "define DLQ retention and replay policy",
    [{"memory_id":"m1","target":"service_memory","content":"The pipeline dead-letter queue stores records from stages that fail after 3 retries. The DLQ is never automatically purged."},
     {"memory_id":"m2","target":"service_memory","content":"The old v1 DLQ was stored in a flat file on the pipeline host and was lost during the 2025 data center migration."},
     {"memory_id":"m3","target":"repo_memory","content":"DLQ configuration is in config/pipeline/dlq.yaml with table name and connection string."}],
    [{"unit_id":"u1","text":"The DLQ must automatically purge records older than 90 days. Records that have been manually inspected and resolved must be marked as resolved rather than deleted, for audit purposes."},
     {"unit_id":"u2","text":"Add a DLQ replay feature: an operator can replay a resolved DLQ record back into the original pipeline stage. Replayed records must carry a dlq_replay_id in the pipeline metadata."},
     {"unit_id":"u3","text":"Write a daily DLQ health report that shows count by stage, age distribution, and resolved vs unresolved counts."}],
    {"read":["m1","m3"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m3\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory"],
    "READ+STORE joint with stale. Reads m1 (current DLQ) and m3 (config). Skips m2 (stale legacy DLQ that was lost). u1 and u2 define durable DLQ behaviors → service_memory. u3 is health report task → task_state."),

# ── 0068: svc+task on analytics-dashboard, query result pagination ──
add("v05_batch300_0068", "analytics-dashboard", "databoard", "query-engine", "add cursor-based pagination for large results",
    [{"memory_id":"m1","target":"service_memory","content":"The query engine returns all matching rows in a single response, limited to 50,000 rows. Queries exceeding this limit are truncated with a warning."},
     {"memory_id":"m2","target":"service_memory","content":"The visualizer can only render up to 10,000 data points before performance degrades significantly."}],
    [{"unit_id":"u1","text":"Replace the single-response model with cursor-based pagination: each response returns up to 1,000 rows plus a next_cursor token. The client passes the cursor to fetch the next page."},
     {"unit_id":"u2","text":"Cursors must be opaque strings (base64-encoded) that encode the query ID, last row offset, and an HMAC to prevent tampering. Tampered cursors must be rejected with a 400 error."},
     {"unit_id":"u3","text":"Update the visualizer to use the new pagination API for queries returning more than 500 rows."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    "READ+STORE joint. u1 is an implementation plan → task_state. u2 is durable cursor security behavior → service_memory. u3 is visualizer update task → task_state. Boundary case: u1 sounds like it could be service_memory but 'Replace the single-response model' frames it as a current implementation change."),

# ── 0069: svc+repo on docs-assistant, document freshness scoring ──
add("v05_batch300_0069", "docs-assistant", "docs-bot", "search", "add document freshness to ranking",
    [{"memory_id":"m1","target":"service_memory","content":"The search service ranks results by TF-IDF score with a 2.0x boost for title matches. It does not consider document age."},
     {"memory_id":"m2","target":"repo_memory","content":"Each indexed document has a last_modified timestamp extracted from git blame in data/indexer/document_metadata.json."},
     {"memory_id":"m3","target":"service_memory","content":"The old search ranking used a static priority field set manually by doc editors, which was abandoned due to maintenance burden."}],
    [{"unit_id":"u1","text":"Add a freshness decay factor to the search ranking: documents modified within the last 30 days get a 1.5x boost; documents older than 365 days get a 0.5x penalty. The decay factor multiplies with the existing TF-IDF score."},
     {"unit_id":"u2","text":"The freshness decay parameters must be tunable via config/search/freshness.yaml with keys boost_window_days, penalty_window_days, boost_factor, and penalty_factor."},
     {"unit_id":"u3","text":"Reindex all documents to populate the last_modified timestamp for the freshness calculation."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress","stale_memory"],
    "READ+STORE joint with stale. Reads m1 (current ranking) and m2 (metadata source). Skips m3 (stale manual priority). u1 defines durable freshness ranking → service_memory. u2 is config location → repo_memory. u3 is reindex task → task_state."),

# ── 0070: svc+task+sensitive on mobile-field, offline sync encryption ──
add("v05_batch300_0070", "mobile-field", "field-app", "sync", "add at-rest encryption for offline queue",
    [{"memory_id":"m1","target":"service_memory","content":"The sync offline queue stores pending edits in a local SQLite database at app/data/sync_queue.db with no encryption."},
     {"memory_id":"m2","target":"project_memory","content":"The field-app project security policy requires all locally stored user data to be encrypted at rest using AES-256-GCM."}],
    [{"unit_id":"u1","text":"The sync queue database must be encrypted at rest with AES-256-GCM. The encryption key must be derived from the device keystore, not hardcoded or stored in SharedPreferences."},
     {"unit_id":"u2","text":"The encryption must be transparent to the sync module: the DAO layer must handle encryption/decryption without changing the business logic that reads and writes queue entries."},
     {"unit_id":"u3","text":"The device keystore alias for the sync queue encryption key is fieldapp_sync_queue_key_v1."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention"],
    "READ+STORE joint. u1 and u2 define durable encryption behaviors → service_memory. u3 is a keystore alias (a repo-level key identifier, not a secret) → repo_memory. Shows that key identifiers/aliases are repo_memory, not sensitive."),

# ── 0071: project+task on finance-dashboard, disaster recovery RPO/RTO ──
add("v05_batch300_0071", "finance-dashboard", "finboard", "alerts", "define disaster recovery targets",
    [{"memory_id":"m1","target":"project_memory","content":"The finboard project currently has no formal disaster recovery plan beyond daily database snapshots."},
     {"memory_id":"m2","target":"repo_memory","content":"Database snapshots are stored in S3 under finboard-backups/daily/ with a 30-day retention policy managed by the backup module in src/backup/snapshot_manager.py."}],
    [{"unit_id":"u1","text":"The finboard project disaster recovery targets are: RPO of 1 hour (transaction logs shipped continuously), RTO of 4 hours (full stack redeployable from infrastructure-as-code)."},
     {"unit_id":"u2","text":"All finboard services must support graceful degradation during DR failover: the dashboard must show cached data with a 'data may be stale' banner instead of failing completely."},
     {"unit_id":"u3","text":"Conduct a disaster recovery drill within the next 30 days simulating a complete primary-region outage and measure actual RTO against the 4-hour target."}],
    {"read":["m1","m2"],"store":[{"target":"project_memory","unit_id":"u1"},{"target":"project_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE project_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","project_vs_repo","target_boundary"],
    "READ+STORE joint. u1 is project-level RPO/RTO targets → project_memory (durable recovery commitment). u2 is cross-service degradation policy ('All finboard services') → project_memory. u3 is drill task → task_state."),

# ── 0072: svc+task on education-platform, plagiarism detection threshold ──
add("v05_batch300_0072", "education-platform", "learnhub", "grading", "configure plagiarism detection sensitivity",
    [{"memory_id":"m1","target":"service_memory","content":"The grading service runs submissions through an external plagiarism detection API and receives a similarity score between 0 and 100."},
     {"memory_id":"m2","target":"project_memory","content":"The learnhub academic integrity policy requires flagging submissions with similarity above 40% for instructor review."}],
    [{"unit_id":"u1","text":"Submissions with a similarity score above 60% must be automatically blocked from grading and require instructor override to proceed. Scores between 40% and 60% must be flagged for review but not blocked."},
     {"unit_id":"u2","text":"The plagiarism detection thresholds (40% flag, 60% block) must be configurable per course in config/grading/plagiarism.yaml to accommodate discipline-specific norms."},
     {"unit_id":"u3","text":"Generate a plagiarism report for the current semester showing the distribution of similarity scores across all submissions."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress"],
    "READ+STORE joint. u1 defines durable detection threshold behavior → service_memory. u2 is config location → repo_memory. u3 is report generation task → task_state."),

# ── 0073: svc+svc on workflow-automation, workflow versioning ──
add("v05_batch300_0073", "workflow-automation", "flowcraft", "orchestrator", "implement workflow definition versioning",
    [{"memory_id":"m1","target":"service_memory","content":"The orchestrator loads workflow definitions from config/workflows/ at startup and keeps them in memory. There is no versioning — changing a YAML file changes the running workflow immediately."},
     {"memory_id":"m2","target":"repo_memory","content":"Workflow YAML files are stored in a git repository under config/workflows/ and changes are deployed via CI/CD."},
     {"memory_id":"m3","target":"task_state","content":"Last week a YAML syntax error in the order_fulfillment workflow caused all active orders to enter an unrecoverable state."}],
    [{"unit_id":"u1","text":"Workflow definitions must be versioned: each workflow YAML file must include a version field (semver). The orchestrator must only load a new version after it passes schema validation and a canary test on 1% of new executions."},
     {"unit_id":"u2","text":"Running workflow instances must continue using the version they started with. A running instance must not be affected by a definition update unless explicitly migrated by an operator."},
     {"unit_id":"u3","text":"Add a workflow version history page to the admin dashboard showing the last 10 versions of each workflow with deploy timestamps and canary results."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory"],
    "READ+STORE joint with stale incident context. Reads m1 (current loading) and m2 (git storage). Skips m3 (stale incident — past event, not current state). u1 and u2 define durable versioning behaviors → service_memory. u3 is dashboard feature task → task_state."),

# ── 0074: svc+task+sensitive on learning-assistant, data export GDPR ──
add("v05_batch300_0074", "learning-assistant", "studybuddy", "progress-tracker", "implement user data export for GDPR",
    [{"memory_id":"m1","target":"service_memory","content":"The progress tracker stores per-student data in the student_progress table: modules completed, quiz scores, time spent per module, and login timestamps."},
     {"memory_id":"m2","target":"project_memory","content":"The studybuddy project must comply with GDPR data portability requirements: users can request a machine-readable export of all their personal data within 30 days."},
     {"memory_id":"m3","target":"repo_memory","content":"Data export templates are under templates/exports/ with one JSON schema per export type."}],
    [{"unit_id":"u1","text":"Add a user data export endpoint that generates a JSON file containing all student progress data, quiz history, preferences, and account metadata. The export must be available for download within 1 hour of request."},
     {"unit_id":"u2","text":"Data exports must be encrypted with a one-time download link that expires after 7 days. The link must be sent to the user's verified email address, not displayed in the UI."},
     {"unit_id":"u3","text":"Store the user's verified email address for GDPR exports in the user_settings table under the gdpr_export_email column, not in environment variables or hardcoded config files."}],
    {"read":["m1","m2","m3"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE task_state u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress","sensitive_boundary"],
    "READ+STORE joint. u1 is an implementation plan → task_state. u2 is durable export security behavior → service_memory. u3 is a DB schema convention (where to store the user's verified email config) → repo_memory. No literal email addresses in unit text."),

# ── 0075: svc+svc on mobile-field, camera permission denial handling ──
add("v05_batch300_0075", "mobile-field", "field-app", "camera", "define camera permission denial UX flow",
    [{"memory_id":"m1","target":"service_memory","content":"The camera module requests camera permission on first launch. If denied, it shows a generic error message and disables all camera features."},
     {"memory_id":"m2","target":"repo_memory","content":"Camera permission strings are defined in app/src/main/res/values/strings.xml under the camera_permission_ prefix."}],
    [{"unit_id":"u1","text":"If the user denies camera permission on first request, the app must show an educational screen explaining why camera access is needed (photo capture for field reports) with a 'Grant Permission' button that opens the system settings."},
     {"unit_id":"u2","text":"If the user denies camera permission twice, the app must not show the educational screen again for 30 days. Instead, show a minimal banner saying 'Camera access required for photo capture. Enable in Settings.'"},
     {"unit_id":"u3","text":"The camera module must never crash or freeze when launched without permission — it must show the educational screen or banner gracefully regardless of permission state."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"service_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE service_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant"],
    "READ+STORE joint with triple service_memory. All three define durable permission UX behaviors for the camera module. u1 is first-denial UX, u2 is repeat-denial UX, u3 is graceful degradation. Triple svc is valid when all describe durable component behaviors."),

# ── 0076: repo+task on game-studio, CI pipeline asset validation ──
add("v05_batch300_0076", "game-studio", "dungeon-tools", "asset-pipeline", "add asset validation to CI gates",
    [{"memory_id":"m1","target":"service_memory","content":"The asset pipeline runs validation checks (texture dimensions, format, compression level) during the build process but not as a separate CI gate."},
     {"memory_id":"m2","target":"repo_memory","content":"The CI pipeline is defined in .github/workflows/build.yml and currently runs unit tests and a smoke build."}],
    [{"unit_id":"u1","text":"Add an asset validation gate to the CI pipeline that runs before the build step. The gate must run scripts/validate_assets.py and fail the CI run if any asset fails validation."},
     {"unit_id":"u2","text":"The asset validation CI step must run in parallel for PC, PS5, and Switch platform targets using matrix builds to avoid extending CI time."},
     {"unit_id":"u3","text":"Configure the CI pipeline at .github/workflows/build.yml to add the validate_assets job with a 15-minute timeout."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"repo_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE repo_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","repo_convention","task_progress"],
    "READ+STORE joint. u1 is an implementation plan → task_state. u2 is CI strategy convention → repo_memory. u3 is CI config path → repo_memory. Two repo_memory units are valid for heavily repo-convention cases."),

# ── 0077: svc+task on travel-planner, currency conversion fallback ──
add("v05_batch300_0077", "travel-planner", "voyager", "pricing", "handle currency conversion API failures",
    [{"memory_id":"m1","target":"service_memory","content":"The pricing service converts all fares to the user's preferred currency using a real-time exchange rate API before displaying them."},
     {"memory_id":"m2","target":"repo_memory","content":"Exchange rate cache is stored in Redis with key pattern fx:{from_currency}:{to_currency} and a TTL of 1 hour."},
     {"memory_id":"m3","target":"service_memory","content":"The legacy pricing module showed prices in the airline's native currency only and required the user to convert manually."}],
    [{"unit_id":"u1","text":"When the exchange rate API is unavailable, the pricing service must fall back to the cached rate if it is less than 2 hours old. If no fresh cache is available, display prices in the airline's native currency with a warning banner."},
     {"unit_id":"u2","text":"The warning banner must state the currency, the conversion rate source, and a timestamp of when the rate was last updated."},
     {"unit_id":"u3","text":"Add a 'force refresh' button in the pricing admin panel that clears the exchange rate cache and fetches fresh rates from the API."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory"],
    "READ+STORE joint with stale. Reads m1 (current conversion) and m2 (cache config). Skips m3 (stale legacy). u1 and u2 define durable fallback behavior → service_memory. u3 is admin feature task → task_state."),

# ── 0078: project+task on docs-assistant, API compatibility policy ──
add("v05_batch300_0078", "docs-assistant", "docs-bot", "summarizer", "establish API version compatibility policy",
    [{"memory_id":"m1","target":"project_memory","content":"The docs-assistant project currently has no formal API version compatibility policy; new features may break older client versions without warning."},
     {"memory_id":"m2","target":"repo_memory","content":"API endpoint definitions are in src/api/routes.py with version prefixes like /api/v1/."}],
    [{"unit_id":"u1","text":"The docs-assistant project must support the current and previous major API version concurrently. v1 endpoints remain available for 12 months after v2 is released, with a deprecation notice in the response headers."},
     {"unit_id":"u2","text":"Deprecated endpoints must return a Sunset HTTP header with the retirement date in ISO 8601 format. After the retirement date, deprecated endpoints must return 410 Gone."},
     {"unit_id":"u3","text":"Add the v1 deprecation notices to all current v1 endpoints and document the retirement timeline in docs/api/deprecation.md."}],
    {"read":["m1","m2"],"store":[{"target":"project_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","project_vs_repo","service_vs_task_state","target_boundary"],
    "READ+STORE joint. u1 is a project-level compatibility policy ('must support current+previous') → project_memory. u2 is a specific API behavior (Sunset header, 410 Gone) → service_memory. u3 is deprecation implementation task → task_state. Fine project vs service distinction."),

# ── 0079: svc+task on data-platform, export file naming convention ──
add("v05_batch300_0079", "data-platform", "data-jobs", "export", "standardize export file naming and partitioning",
    [{"memory_id":"m1","target":"service_memory","content":"The export job writes files to S3 with inconsistent naming: some use dates, some use sequential numbers, and there is no partitioning scheme."},
     {"memory_id":"m2","target":"repo_memory","content":"S3 bucket structure is documented in docs/export/s3_layout.md but is currently outdated."}],
    [{"unit_id":"u1","text":"All export files must follow the naming convention: {export_type}/{year}/{month}/{day}/{export_type}_{timestamp}_{uuid}.{format}. No exceptions."},
     {"unit_id":"u2","text":"The export job must validate the output filename against the convention regex before uploading. Mismatched filenames must be rejected and logged as an error with the expected vs actual filename."},
     {"unit_id":"u3","text":"Update docs/export/s3_layout.md to reflect the new naming convention and add a filename examples table."}],
    {"read":["m1","m2"],"store":[{"target":"repo_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE repo_memory u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","repo_vs_service","target_boundary"],
    "READ+STORE joint with repo vs service boundary. u1 is a naming convention (WHERE and HOW files are named) → repo_memory. u2 is durable validation behavior (WHAT the export job enforces) → service_memory. u3 is doc update → repo_memory. Shows the distinction: naming rules are repo conventions, validation behavior is service behavior."),

# ── 0080: svc+task on customer-support, ticket sentiment routing ──
add("v05_batch300_0080", "customer-support", "helpdesk", "routing", "route tickets by customer sentiment",
    [{"memory_id":"m1","target":"service_memory","content":"The routing service assigns tickets based on agent skill tags and current workload, without considering customer sentiment or urgency signals."},
     {"memory_id":"m2","target":"service_memory","content":"Customer sentiment is extracted from ticket body text by a separate NLP service that returns a score between -1.0 (very negative) and 1.0 (very positive)."}],
    [{"unit_id":"u1","text":"The routing service must factor customer sentiment into assignment priority: tickets with sentiment below -0.5 must be escalated to senior agents regardless of skill tag match."},
     {"unit_id":"u2","text":"If the NLP sentiment service is unavailable, the routing service must fall back to keyword-based urgency detection (looking for words like 'urgent', 'immediately', 'legal') and flag matching tickets for manual review."},
     {"unit_id":"u3","text":"I prefer ticket queues sorted by sentiment (most negative first) rather than by creation time."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"user_profile","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE user_profile u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","user_profile_boundary"],
    "READ+STORE joint with user_profile. u1 and u2 define durable sentiment-based routing behaviors → service_memory. u3 is a stable user queue preference → user_profile."),

# ── 0081: svc+task on ecommerce, inventory reservation expiry notification ──
add("v05_batch300_0081", "ecommerce-platform", "shopengine", "inventory", "add reservation expiry push notifications",
    [{"memory_id":"m1","target":"service_memory","content":"The inventory service reserves stock for 15 minutes when a user adds an item to cart. Expired reservations are silently released."},
     {"memory_id":"m2","target":"service_memory","content":"The notification service supports push notifications via Firebase Cloud Messaging with a 30-second delivery timeout."}],
    [{"unit_id":"u1","text":"When a cart reservation expires and stock is released, the inventory service must send a push notification to the user: 'Your reserved item is no longer held. It may still be available — check now.'"},
     {"unit_id":"u2","text":"The reservation expiry notification must include the product name, the quantity that was reserved, and a deep link to the product page. The notification must be sent only once per reservation expiry."},
     {"unit_id":"u3","text":"Measure the conversion rate of reservation-expiry notifications (users who re-add the item within 24 hours) and report monthly."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. u1 and u2 define durable notification behavior → service_memory. u3 is measurement task → task_state."),

# ── 0082: svc+task on analytics-dashboard, scheduled report failure handling ──
add("v05_batch300_0082", "analytics-dashboard", "databoard", "scheduler", "handle scheduled report generation failures",
    [{"memory_id":"m1","target":"service_memory","content":"The scheduler runs reports on a cron schedule and emails the PDF output to the dashboard owner. If report generation fails, no notification is sent — the report is silently skipped."},
     {"memory_id":"m2","target":"repo_memory","content":"Scheduler job definitions are in config/scheduler/jobs.yaml with per-report schedule, recipient, and format settings."}],
    [{"unit_id":"u1","text":"When a scheduled report fails to generate, the scheduler must send a failure notification to the report owner with the error message, the failed query, and a link to the scheduler logs. The notification must be sent within 5 minutes of the failure."},
     {"unit_id":"u2","text":"The scheduler must retry failed reports once after 10 minutes. If the retry also fails, it must not attempt further retries for that scheduled run to avoid cascading failures."},
     {"unit_id":"u3","text":"Add a scheduler health dashboard showing the last 24 hours of report runs with success/failure counts and average generation time."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. u1 and u2 define durable failure handling and retry behaviors → service_memory. u3 is dashboard feature task → task_state."),

# ── 0083: svc+task+repo on education-platform, course capacity overbooking ──
add("v05_batch300_0083", "education-platform", "learnhub", "enrollment", "implement controlled course overbooking",
    [{"memory_id":"m1","target":"service_memory","content":"The enrollment service enforces a hard cap of 50 students per course and rejects enrollment when the cap is reached."},
     {"memory_id":"m2","target":"repo_memory","content":"Course capacity limits are configured in config/courses/capacity.yaml with keys max_students and overbooking_allowed."},
     {"memory_id":"m3","target":"task_state","content":"Last semester, 12% of enrolled students dropped courses in the first two weeks, leaving unfilled seats that could have been overbooked."}],
    [{"unit_id":"u1","text":"Allow controlled overbooking up to 110% of course capacity for courses where historical drop rates exceed 8%. Overbooked students must be clearly labeled as 'provisional' until a seat opens."},
     {"unit_id":"u2","text":"If a provisionally enrolled student does not receive a confirmed seat within 7 days of the course start, the system must automatically drop them and notify them via email with alternative course suggestions."},
     {"unit_id":"u3","text":"Set overbooking_allowed to true in config/courses/capacity.yaml for the 5 courses with the highest historical drop rates."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory"],
    "READ+STORE joint with stale. Reads m1 (current cap) and m2 (config). Skips m3 (stale historical stat from last semester). u1 and u2 define durable overbooking behaviors → service_memory. u3 is config task → task_state."),

# ── 0084: svc+task on finance-dashboard, data validation pipeline ──
add("v05_batch300_0084", "finance-dashboard", "finboard", "aggregator", "add multi-source data reconciliation",
    [{"memory_id":"m1","target":"service_memory","content":"The aggregator ingests transaction data from a single source (the primary payment processor) with no cross-source validation."},
     {"memory_id":"m2","target":"project_memory","content":"The finboard project requires transaction data to be reconciled across at least two independent sources for financial reporting accuracy."}],
    [{"unit_id":"u1","text":"The aggregator must ingest transaction data from both the payment processor and the bank settlement feed, reconcile them daily, and flag any transaction that appears in only one source."},
     {"unit_id":"u2","text":"Unreconciled transactions must be held in a pending_reconciliation table and must not appear in financial reports until they are matched in both sources or manually approved by a finance analyst."},
     {"unit_id":"u3","text":"Write the daily reconciliation report query that identifies all unreconciled transactions older than 3 business days."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. u1 is an implementation plan → task_state. u2 is durable data integrity behavior (holding unreconciled transactions) → service_memory. u3 is report writing task → task_state."),

# ── 0085: svc+task on game-studio, build artifact signing ──
add("v05_batch300_0085", "game-studio", "dungeon-tools", "build-system", "add code signing for release builds",
    [{"memory_id":"m1","target":"service_memory","content":"The build system produces unsigned binaries for all platforms. Release builds are signed manually by the release engineer after the build completes."},
     {"memory_id":"m2","target":"repo_memory","content":"Code signing certificates are stored in a hardware security module (HSM) accessed via scripts/sign/sign_build.sh."}],
    [{"unit_id":"u1","text":"The build system must automatically sign release build binaries as the final step of the build pipeline. Debug builds must remain unsigned."},
     {"unit_id":"u2","text":"Code signing must use the platform-specific format: Authenticode for Windows, codesign for macOS, and the platform-specific ELF signing tool for Linux. The signing identity must come from the HSM, never from a file on disk."},
     {"unit_id":"u3","text":"Verify the signature on every release build artifact by running scripts/verify_signature.sh before uploading to the distribution server."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    "READ+STORE joint. u1 is an implementation plan → task_state. u2 is durable signing behavior with security constraint → service_memory. u3 is verification task → task_state."),

# ── 0086: svc+task on mobile-field, location tracking consent ──
add("v05_batch300_0086", "mobile-field", "field-app", "sync", "implement location data consent management",
    [{"memory_id":"m1","target":"service_memory","content":"The sync module can tag records with GPS coordinates but does not currently ask for location permission or explain how location data is used."},
     {"memory_id":"m2","target":"project_memory","content":"The field-app project privacy policy requires explicit opt-in consent before collecting or storing location data."}],
    [{"unit_id":"u1","text":"The sync module must request location permission separately from camera permission with a clear explanation: 'Field App collects location data to geotag your field reports. Location data is stored with your reports and can be deleted at any time.'"},
     {"unit_id":"u2","text":"If the user denies location permission, the app must still function fully without location tagging. No features may be disabled or degraded due to location permission denial."},
     {"unit_id":"u3","text":"Add a privacy dashboard screen where users can view all stored location data points and delete them individually or in bulk."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. u1 and u2 define durable location consent behaviors → service_memory. u3 is privacy dashboard feature task → task_state."),

# ── 0087: svc+task on workflow-automation, step timeout enforcement ──
add("v05_batch300_0087", "workflow-automation", "flowcraft", "orchestrator", "enforce per-step timeouts with termination",
    [{"memory_id":"m1","target":"service_memory","content":"The orchestrator currently has a global workflow timeout of 60 minutes but no per-step timeouts."},
     {"memory_id":"m2","target":"repo_memory","content":"Workflow step definitions in config/workflows/ can include an optional timeout_seconds field, but it is currently ignored."},
     {"memory_id":"m3","target":"task_state","content":"Last month a stuck API call in the payment_verification step caused the entire order_fulfillment workflow to hang for 45 minutes."}],
    [{"unit_id":"u1","text":"Every workflow step must have a timeout. Default timeout is 300 seconds. Steps can override this with a timeout_seconds field in the workflow YAML. When a step times out, the orchestrator must terminate the step's execution and mark it as timed_out, not failed."},
     {"unit_id":"u2","text":"A timed_out step must be retried if the step definition has retry_on_timeout set to true (default: false). If retry_on_timeout is false, the workflow must follow the normal step failure path."},
     {"unit_id":"u3","text":"Add a timeout_seconds value to every existing step definition that calls an external API, starting with payment_verification (60s) and inventory_check (30s)."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory"],
    "READ+STORE joint with stale incident context. Reads m1 (current behavior) and m2 (config). Skips m3 (stale incident). u1 and u2 define durable timeout behaviors → service_memory. u3 is config task → task_state."),

# ── 0088: svc+task on learning-assistant, adaptive quiz difficulty ──
add("v05_batch300_0088", "learning-assistant", "studybuddy", "quiz-generator", "implement adaptive difficulty based on performance",
    [{"memory_id":"m1","target":"service_memory","content":"The quiz generator selects questions randomly from the question bank filtered by topic and format, without adjusting difficulty based on student performance."},
     {"memory_id":"m2","target":"repo_memory","content":"Questions in the question_bank table have a difficulty column with values easy, medium, or hard."},
     {"memory_id":"m3","target":"user_profile","content":"The student prefers challenging quizzes and has indicated frustration with repetitive easy questions."}],
    [{"unit_id":"u1","text":"The quiz generator must adapt question difficulty based on the student's recent performance: if the student answers 80%+ correctly in the last 10 questions, increase difficulty; if below 50%, decrease difficulty. The difficulty must move at most one level per quiz."},
     {"unit_id":"u2","text":"Adaptive difficulty must have guardrails: a student must not receive only hard questions even with perfect scores. At least 20% of questions must be from the current difficulty level's adjacent levels to provide calibration."},
     {"unit_id":"u3","text":"I prefer quizzes where difficulty ramps up gradually within a session — start with 2 easy warm-up questions before moving to the adaptive level."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"user_profile","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE user_profile u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","user_profile_boundary","related_but_useless"],
    "READ+STORE joint with user_profile and related-but-useless. Reads m1 (current quiz) and m2 (difficulty field). Skips m3 (user preference for challenging quizzes — related but the adaptive algorithm defined in u1/u2 handles this implicitly; the user preference in m3 is about a past frustration, not a routing directive). u1 and u2 define durable adaptive difficulty behaviors → service_memory. u3 is a stable user preference for warm-up questions → user_profile."),

# ── 0089: svc+task+repo on memory-router, training data split validation ──
add("v05_batch300_0089", "memory-router", "distilled-memory-policy-router", "case_validator", "add train/dev/gold leakage detection",
    [{"memory_id":"m1","target":"service_memory","content":"The case validator checks structural validity of individual cases and DSL consistency but does not check for leakage across data splits."},
     {"memory_id":"m2","target":"repo_memory","content":"Case validator source is under src/v04/case_validator.py with the validation logic in validate_case() and validate_jsonl_file()."},
     {"memory_id":"m3","target":"project_memory","content":"The v0.5 training plan requires train/dev/gold splits with zero leakage: no case text may appear in more than one split."}],
    [{"unit_id":"u1","text":"The case validator must detect cross-split leakage: when validating a file tagged as train, dev, or gold, check that no current_unit text or candidate_memory content appears in any other split file. Leaked cases must be flagged as errors."},
     {"unit_id":"u2","text":"The leakage check must use normalized text comparison (lowercase, whitespace-collapsed) to detect near-duplicates, not just exact matches."},
     {"unit_id":"u3","text":"Add a --splits argument to validate_jsonl_file() that accepts paths to the other split files for cross-reference. Document in the function docstring."}],
    {"read":["m1","m2","m3"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. Reads all three (all relevant: m1 current behavior, m2 path, m3 training plan requirement). u1 and u2 define durable leakage detection behavior → service_memory. u3 is implementation task → task_state."),

# ── 0090: svc+task on docs-assistant, rate limit user-facing search ──
add("v05_batch300_0090", "docs-assistant", "docs-bot", "search", "add per-user search rate limiting",
    [{"memory_id":"m1","target":"service_memory","content":"The search service currently has no rate limiting — any user can make unlimited requests."},
     {"memory_id":"m2","target":"repo_memory","content":"API gateway configuration is in config/gateway/rate_limits.yaml with per-endpoint limits."},
     {"memory_id":"m3","target":"task_state","content":"Last month's traffic analysis showed one IP making 50,000 search requests in a single hour, degrading performance for all other users."}],
    [{"unit_id":"u1","text":"The search service must enforce per-user rate limiting: 100 requests per minute for authenticated users, 20 requests per minute for anonymous users. Rate-limited requests must return 429 with a Retry-After header."},
     {"unit_id":"u2","text":"Rate limit counters must be stored in Redis with a sliding window algorithm, not a fixed window, to prevent burst traffic at window boundaries."},
     {"unit_id":"u3","text":"Add the search rate limit rules to config/gateway/rate_limits.yaml under a new search section."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","stale_memory"],
    "READ+STORE joint with stale incident context. Reads m1 (no rate limiting) and m2 (config). Skips m3 (stale traffic analysis). u1 and u2 define durable rate limiting behaviors → service_memory. u3 is config update → repo_memory."),

# ── 0091: svc+task on customer-support, ticket categorization ML model ──
add("v05_batch300_0091", "customer-support", "helpdesk", "ticketing", "integrate ML ticket categorization",
    [{"memory_id":"m1","target":"service_memory","content":"The ticketing service requires manual category assignment (billing, technical, account, feedback) via a dropdown when creating or updating tickets."},
     {"memory_id":"m2","target":"repo_memory","content":"Ticket categories are defined in config/ticketing/categories.yaml with a list of valid category IDs and their display names."},
     {"memory_id":"m3","target":"service_memory","content":"The old categorization system used keyword matching with a fixed list of 200 trigger words, which had 62% accuracy."}],
    [{"unit_id":"u1","text":"The ticketing service must integrate an ML-based category predictor that suggests up to 2 categories with confidence scores when a ticket is created. The agent can accept the suggestion or override it."},
     {"unit_id":"u2","text":"If the ML model confidence is below 70% for all categories, the service must not show any suggestion and must fall back to requiring manual category selection."},
     {"unit_id":"u3","text":"The ML model must be retrained weekly on the last 90 days of agent-categorized tickets and must never be trained on customer-submitted category suggestions."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"service_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSTORE service_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","stale_memory"],
    "READ+STORE joint with stale. Reads m1 (current manual) and m2 (categories). Skips m3 (stale keyword system). u1 is an integration plan → task_state. u2 and u3 define durable ML model behaviors → service_memory."),

# ── 0092: svc+task on ecommerce, order splitting for multi-warehouse ──
add("v05_batch300_0092", "ecommerce-platform", "shopengine", "orders", "implement multi-warehouse order splitting",
    [{"memory_id":"m1","target":"service_memory","content":"The orders service currently fulfills each order from a single warehouse. If items are in different warehouses, the order is held until all stock is available in one location."},
     {"memory_id":"m2","target":"service_memory","content":"The inventory service tracks stock levels per warehouse in the warehouse_inventory table with columns warehouse_id, product_id, and quantity."}],
    [{"unit_id":"u1","text":"The orders service must split a single order into multiple sub-orders when items are available in different warehouses. Each sub-order ships independently with its own tracking number."},
     {"unit_id":"u2","text":"Order splitting must minimize the number of sub-orders: prefer warehouse assignments that consolidate items into the fewest shipments. If multiple warehouses can fulfill the same items, prefer the warehouse closest to the shipping address."},
     {"unit_id":"u3","text":"Split orders must preserve the original order total — shipping costs must be recalculated per sub-order but the sum must not exceed the original shipping charge quoted to the customer."}],
    {"read":["m1","m2"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"service_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSTORE service_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","service_vs_task_state"],
    "READ+STORE joint. u1 is implementation plan → task_state. u2 defines minimization strategy → service_memory. u3 defines shipping cost constraint → service_memory."),

# ── 0093: svc+task on data-platform, pipeline backpressure ──
add("v05_batch300_0093", "data-platform", "data-jobs", "pipeline", "implement backpressure when downstream is slow",
    [{"memory_id":"m1","target":"service_memory","content":"The pipeline pushes data through stages sequentially with no flow control. If a downstream stage is slow, upstream stages continue producing data, causing memory pressure."},
     {"memory_id":"m2","target":"repo_memory","content":"Pipeline stage buffer sizes are configured in config/pipeline/buffers.yaml with per-stage queue_capacity entries."}],
    [{"unit_id":"u1","text":"The pipeline must implement backpressure: each stage has an output buffer of configurable size. When the buffer is full, the stage must pause production and wait for the downstream stage to consume. The pause must not lose data."},
     {"unit_id":"u2","text":"A backpressure event must be logged with the stage name, buffer size at the time of blocking, and duration of the block. Alerts must fire if any stage is blocked for more than 5 minutes."},
     {"unit_id":"u3","text":"Set the default per-stage buffer capacity to 10,000 records in config/pipeline/buffers.yaml and add buffer_size and block_timeout_seconds keys."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention"],
    "READ+STORE joint. u1 and u2 define durable backpressure behaviors → service_memory. u3 is config key definitions → repo_memory."),

# ── 0094: svc+task on finance-dashboard, audit log immutability ──
add("v05_batch300_0094", "finance-dashboard", "finboard", "alerts", "ensure alert audit log immutability",
    [{"memory_id":"m1","target":"service_memory","content":"The alerts service logs all alert firings to the alert_history table but the table allows UPDATE and DELETE operations."},
     {"memory_id":"m2","target":"project_memory","content":"The finboard project must maintain an immutable audit trail of all financial alerts for regulatory compliance."}],
    [{"unit_id":"u1","text":"The alert_history table must be made append-only. The database user used by the alerts service must have only INSERT and SELECT privileges on alert_history. UPDATE and DELETE must be revoked."},
     {"unit_id":"u2","text":"Any attempt to modify or delete alert history records must be logged to a separate audit_violation_attempts table with the timestamp, user, attempted operation, and target record ID."},
     {"unit_id":"u3","text":"Run a one-time script to lock the alert_history table: revoke UPDATE/DELETE for the alerts service user and create the audit_violation_attempts table."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. u1 and u2 define durable audit immutability behaviors → service_memory. u3 is one-time migration task → task_state."),

# ── 0095: svc+task on travel-planner, price guarantee matching ──
add("v05_batch300_0095", "travel-planner", "voyager", "pricing", "implement price match guarantee",
    [{"memory_id":"m1","target":"service_memory","content":"The pricing service displays fares from airline APIs with a small markup. There is currently no price matching against competitor prices."},
     {"memory_id":"m2","target":"project_memory","content":"The voyager project price match policy: if a customer finds a lower price on a competitor site within 24 hours of booking, voyager refunds the difference plus 10%."},
     {"memory_id":"m3","target":"repo_memory","content":"Competitor price monitoring runs hourly via scripts/monitor_competitors.py and stores results in the competitor_prices table."}],
    [{"unit_id":"u1","text":"At booking time, the pricing service must check the competitor_prices table for the same route, date, and cabin class. If a competitor price is lower, the service must automatically match it without customer intervention."},
     {"unit_id":"u2","text":"If a customer submits a price match claim after booking, the service must verify the claim against the competitor_prices table from the booking date. Approved claims must trigger an automatic refund of the difference plus 10% within 2 business days."},
     {"unit_id":"u3","text":"Add a price match claim form to the booking management page with fields for competitor name, URL, and screenshot upload."}],
    {"read":["m1","m2","m3"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. u1 and u2 define durable price match behaviors → service_memory. u3 is UI feature task → task_state."),

# ── 0096: svc+task on memory-router, eval_runner output format detection ──
add("v05_batch300_0096", "memory-router", "distilled-memory-policy-router", "eval_runner", "add auto-detection of model output format",
    [{"memory_id":"m1","target":"service_memory","content":"The eval_runner expects model outputs in exactly the Unit DSL format and fails on any deviation."},
     {"memory_id":"m2","target":"service_memory","content":"The parser can parse Unit DSL, Legacy Span JSON, and Unit JSON formats and returns a canonical representation regardless of input format."},
     {"memory_id":"m3","target":"repo_memory","content":"Eval runner code lives under src/v04/eval_runner.py and uses the parser module from src/v04/parser.py."}],
    [{"unit_id":"u1","text":"The eval_runner must auto-detect the model's output format by trying the parser in DSL mode first, then JSON mode. It must log which format was detected for each prediction to help analyze format adherence."},
     {"unit_id":"u2","text":"If the model output cannot be parsed in any supported format, the eval_runner must record it as a parse failure with the raw output truncated to 500 characters in the error log, not fail the entire evaluation run."},
     {"unit_id":"u3","text":"I prefer evaluation reports that include a format distribution pie chart (DSL vs JSON vs parse-failure) alongside the standard F1 metrics."}],
    {"read":["m1","m2","m3"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"user_profile","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE user_profile u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","user_profile_boundary"],
    "READ+STORE joint with user_profile. u1 and u2 define durable eval_runner format detection behavior → service_memory. u3 is a stable evaluation report preference → user_profile."),

# ── 0097: svc+task on ecommerce, cart abandonment recovery ──
add("v05_batch300_0097", "ecommerce-platform", "shopengine", "orders", "implement cart abandonment recovery emails",
    [{"memory_id":"m1","target":"service_memory","content":"The orders service tracks cart state but does not send reminders when a cart is abandoned."},
     {"memory_id":"m2","target":"repo_memory","content":"Email templates for transactional messages are stored in templates/email/transactions/ with one HTML file per message type."},
     {"memory_id":"m3","target":"service_memory","content":"The notification service has a daily email budget of 50,000 messages to avoid being flagged as spam."}],
    [{"unit_id":"u1","text":"The orders service must send a cart abandonment email 2 hours after the user's last cart activity if the cart has items and no checkout was completed. A second reminder must be sent at 24 hours. No more than 2 reminders per abandoned cart."},
     {"unit_id":"u2","text":"Cart abandonment emails must be suppressed for users who have opted out of marketing emails, but a single transactional reminder (labeled 'About your cart') is still allowed per the transactional email policy."},
     {"unit_id":"u3","text":"Create the cart abandonment email template at templates/email/transactions/cart_abandoned.html with placeholders for item names, total, and the cart recovery URL."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress","related_but_useless"],
    "READ+STORE joint with related-but-useless. Reads m1 (cart tracking) and m2 (template path). Skips m3 (email budget constraint — related to email sending but not needed for defining the abandonment recovery behavior). u1 and u2 define durable recovery email behaviors → service_memory. u3 is template creation task → task_state."),

# ── 0098: svc+task on analytics-dashboard, data export with watermarking ──
add("v05_batch300_0098", "analytics-dashboard", "databoard", "scheduler", "add watermarking to exported reports",
    [{"memory_id":"m1","target":"service_memory","content":"The scheduler generates PDF reports and emails them to recipients without any watermarking or download tracking."},
     {"memory_id":"m2","target":"project_memory","content":"The databoard project requires all exported reports to include a recipient-specific watermark to deter unauthorized sharing of confidential analytics."}],
    [{"unit_id":"u1","text":"Every exported PDF report must include a diagonal watermark with the recipient's email address and the export timestamp. The watermark must be semi-transparent (opacity 15%) and repeated every 200px across the page."},
     {"unit_id":"u2","text":"If the report contains data classified as restricted (per the project's data governance policy), the watermark must be red and include the text 'CONFIDENTIAL — DO NOT FORWARD' in addition to the standard recipient watermark."},
     {"unit_id":"u3","text":"Update the scheduler's PDF generation code in src/scheduler/pdf_renderer.py to apply the watermark layer as the final rendering step."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. u1 and u2 define durable watermarking behavior → service_memory. u3 is code update task → task_state."),

# ── 0099: svc+task on mobile-field, offline queue priority levels ──
add("v05_batch300_0099", "mobile-field", "field-app", "sync", "implement priority-based queue processing",
    [{"memory_id":"m1","target":"service_memory","content":"The sync module processes the offline queue in strict FIFO order regardless of entry type or urgency."},
     {"memory_id":"m2","target":"repo_memory","content":"Queue entry types are defined in the sync_queue table with a record_type column containing values like 'photo', 'form', 'location', and 'status'."}],
    [{"unit_id":"u1","text":"The sync module must process the offline queue by priority: CRITICAL (location updates, SOS alerts) must always be synced first, HIGH (form submissions) second, NORMAL (photos, status updates) last. Within the same priority level, maintain FIFO order."},
     {"unit_id":"u2","text":"A CRITICAL entry must never wait behind NORMAL entries. If a CRITICAL entry arrives while NORMAL entries are being processed, the current NORMAL batch must complete, then the CRITICAL entry must be processed next before resuming NORMAL."},
     {"unit_id":"u3","text":"Add a priority column to the sync_queue table with values CRITICAL, HIGH, and NORMAL. Default is NORMAL. Update the queue insertion code in src/sync/queue_manager.py to set priority based on record_type."}],
    {"read":["m1","m2"],"store":[{"target":"service_memory","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"task_state","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","task_progress"],
    "READ+STORE joint. u1 and u2 define durable priority-based processing behaviors → service_memory. u3 is schema/code update task → task_state."),

# ── 0100: svc+task on education-platform, prerequisite waiver workflow ──
add("v05_batch300_0100", "education-platform", "learnhub", "enrollment", "implement prerequisite waiver process",
    [{"memory_id":"m1","target":"service_memory","content":"The enrollment service blocks enrollment if prerequisites are not completed with a passing grade. There is no waiver mechanism."},
     {"memory_id":"m2","target":"project_memory","content":"The learnhub academic policy allows prerequisite waivers at the instructor's discretion for students with equivalent professional experience."},
     {"memory_id":"m3","target":"repo_memory","content":"Course prerequisite definitions are in config/courses/prerequisites.yaml with a list of required course IDs per course."}],
    [{"unit_id":"u1","text":"Add a prerequisite waiver workflow: a student can request a waiver by submitting a written justification and uploading supporting documents (resume, certificates). The course instructor receives the request and can approve or deny with a comment."},
     {"unit_id":"u2","text":"If a waiver is approved, the enrollment service must bypass the prerequisite check for that student on that course only — not for other courses that share the same prerequisite."},
     {"unit_id":"u3","text":"Approved waivers must be recorded in a prerequisite_waivers table with student_id, course_id, waived_prerequisite_id, instructor_id, justification, supporting_docs, and approved_at. Denied waivers must also be recorded with the denial reason."}],
    {"read":["m1","m2","m3"],"store":[{"target":"task_state","unit_id":"u1"},{"target":"service_memory","unit_id":"u2"},{"target":"repo_memory","unit_id":"u3"}],
     "skip":[],"dsl":"READ m1,m2,m3\nSTORE task_state u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
    ["read_store_joint","service_invariant","repo_convention","task_progress"],
    "READ+STORE joint. u1 is an implementation plan → task_state. u2 is durable scoped bypass behavior → service_memory. u3 is DB schema definition → repo_memory.")

# End of replacement51 cases

print(f"Created {len(REPLACEMENT51)} replacement cases")
assert len(REPLACEMENT51) == 51, f"Expected 51, got {len(REPLACEMENT51)}"


# ═══════════════════════════════════════════════════════════════
# MAIN: Load, replace, correct, validate, write
# ═══════════════════════════════════════════════════════════════
def main():
    # 1. Load existing batch300
    cases_path = ROOT / "data/v05/batches/v05_batch300_cases.jsonl"
    with open(cases_path) as f:
        all_cases = [json.loads(l) for l in f if l.strip()]
    print(f"Loaded {len(all_cases)} cases from batch300")
    
    # 2. Load new100 separately
    new100_path = ROOT / "data/v05/batches/v05_batch300_new100_cases.jsonl"
    with open(new100_path) as f:
        new100 = [json.loads(l) for l in f if l.strip()]
    print(f"Loaded {len(new100)} cases from new100")
    
    # 3. Replace template cases (0050-0100) in both arrays
    replacement_map = {c["case_id"]: c for c in REPLACEMENT51}
    replacement_ids = set(replacement_map.keys())
    
    # Replace in all_cases
    new_all_cases = []
    replaced_count = 0
    for c in all_cases:
        if c["case_id"] in replacement_ids:
            new_all_cases.append(replacement_map[c["case_id"]])
            replaced_count += 1
        else:
            new_all_cases.append(c)
    print(f"Replaced {replaced_count} cases in all_cases (expected 51)")
    
    # Replace in new100
    new_new100 = []
    new100_replaced = 0
    for c in new100:
        if c["case_id"] in replacement_ids:
            new_new100.append(replacement_map[c["case_id"]])
            new100_replaced += 1
        else:
            new_new100.append(c)
    print(f"Replaced {new100_replaced} cases in new100 (expected 51)")
    
    # 4. Apply borderline label corrections
    corrections = {
        "v05_sample_0012": [
            {"unit_id": "u1", "old_target": "service_memory", "new_target": "task_state",
             "reason": "Independent review: 'Add a SHA-256 checksum...' reads as implementation plan, thin behavioral detail."}
        ],
        "v05_sample_0019": [
            {"unit_id": "u1", "old_target": "service_memory", "new_target": "task_state",
             "reason": "Independent review: 'Add a manual purge button...' is UI feature, not core algorithm."}
        ],
        "v05_batch100_0031": [
            {"unit_id": "u1", "old_target": "service_memory", "new_target": "task_state",
             "reason": "Independent review: 'Add a relevance feedback loop...' is general concept, no specific algorithm."}
        ],
        "v05_batch100_0036": [
            {"unit_id": "u1", "old_target": "service_memory", "new_target": "task_state",
             "reason": "Independent review: 'Add cross-document summarization...' is feature description, no algorithm detail."}
        ],
    }
    
    correction_count = 0
    for c in new_all_cases:
        cid = c["case_id"]
        if cid in corrections:
            for corr in corrections[cid]:
                uid = corr["unit_id"]
                old_t = corr["old_target"]
                new_t = corr["new_target"]
                # Update gold.store
                for s in c["gold"]["store"]:
                    if s["unit_id"] == uid:
                        if s["target"] == new_t:
                            # Already corrected in a previous run
                            break
                        assert s["target"] == old_t, f"Expected {old_t}, got {s['target']}"
                        s["target"] = new_t
                        correction_count += 1
                        break
                # Update gold.dsl
                old_line = f"STORE {old_t} {uid}"
                new_line = f"STORE {new_t} {uid}"
                c["gold"]["dsl"] = c["gold"]["dsl"].replace(old_line, new_line)
                # Update notes
                c["notes"] = c.get("notes", "") + f" [CORRECTED 5.1-D: u{uid[-1]} changed from {old_t} to {new_t} per independent review — {corr['reason']}]"
    print(f"Applied {correction_count} label corrections")
    
    # Also apply to new100
    for c in new_new100:
        cid = c["case_id"]
        if cid in corrections:
            for corr in corrections[cid]:
                uid = corr["unit_id"]
                old_t = corr["old_target"]
                new_t = corr["new_target"]
                for s in c["gold"]["store"]:
                    if s["unit_id"] == uid:
                        s["target"] = new_t
                        break
                old_line = f"STORE {old_t} {uid}"
                new_line = f"STORE {new_t} {uid}"
                c["gold"]["dsl"] = c["gold"]["dsl"].replace(old_line, new_line)
    
    # 5. Validate everything
    all_ok = True
    subset50_path = ROOT / "data/v04/model_predictions/p5_subset50_case_ids.txt"
    subset50_ids = set(subset50_path.read_text().strip().splitlines()) if subset50_path.exists() else set()
    
    fewshot_path = ROOT / "data/v04/model_predictions/qwen3_4b_unit_dsl_fewshot_examples.jsonl"
    fewshot_ids, fewshot_texts = set(), set()
    if fewshot_path.exists():
        with fewshot_path.open() as f:
            for line in f:
                if line.strip():
                    o = json.loads(line)
                    fewshot_ids.add(o["case_id"])
                    for u in o.get("current_units", []):
                        fewshot_texts.add(u["text"])
                    for m in o.get("candidate_memories", []):
                        fewshot_texts.add(m["content"])
    
    # Collect texts for leakage check
    all_texts = set()
    for c in new_all_cases:
        for u in c.get("current_units", []):
            all_texts.add(u["text"])
        for m in c.get("candidate_memories", []):
            all_texts.add(m["content"])
    
    # Validate each case
    for c in new_all_cases:
        r = validate_case(c)
        if not r["valid"]:
            print(f"V {c['case_id']}:")
            for e in r["errors"]:
                print(f"  {e}")
            all_ok = False
        
        p = parse_policy_dsl(
            c["gold"]["dsl"],
            [m["memory_id"] for m in c["candidate_memories"]],
            [u["unit_id"] for u in c["current_units"]],
            LEGAL_TARGETS
        )
        if not p["validation"]["valid"]:
            print(f"D {c['case_id']}:")
            for e in p["validation"]["errors"]:
                print(f"  {e}")
            all_ok = False
        
        ps = {i["unit_id"]: i["target"] for i in p["store"]}
        gs = {s["unit_id"]: s["target"] for s in c["gold"]["store"]}
        if ps != gs:
            print(f"S {c['case_id']}: parsed={ps} gold={gs}")
            all_ok = False
    
    # Leakage checks
    case_ids_set = {c["case_id"] for c in new_all_cases}
    if case_ids_set & subset50_ids:
        print(f"LEAK: subset50 overlap: {case_ids_set & subset50_ids}")
        all_ok = False
    if case_ids_set & fewshot_ids:
        print(f"LEAK: fewshot overlap: {case_ids_set & fewshot_ids}")
        all_ok = False
    if all_texts & fewshot_texts:
        overlap_texts = all_texts & fewshot_texts
        print(f"LEAK: text overlap with fewshot ({len(overlap_texts)} texts)")
        all_ok = False
    
    # Count checks
    assert len(new_all_cases) == 300, f"Expected 300 cases, got {len(new_all_cases)}"
    assert len(new_new100) == 100, f"Expected 100 new100, got {len(new_new100)}"
    print(f"Count: {len(new_all_cases)} total, {len(new_new100)} new100")
    
    if not all_ok:
        print("VALIDATION FAILED")
        sys.exit(1)
    print("All validations PASSED")
    
    # 6. Write outputs
    # Main cases
    with open(ROOT / "data/v05/batches/v05_batch300_cases.jsonl", "w") as f:
        for c in new_all_cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Wrote {len(new_all_cases)} to batch300_cases.jsonl")
    
    # New100
    with open(ROOT / "data/v05/batches/v05_batch300_new100_cases.jsonl", "w") as f:
        for c in new_new100:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Wrote {len(new_new100)} to batch300_new100_cases.jsonl")
    
    # Replacement51
    with open(ROOT / "data/v05/batches/v05_batch300_replacement51_cases.jsonl", "w") as f:
        for c in REPLACEMENT51:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Wrote {len(REPLACEMENT51)} to batch300_replacement51_cases.jsonl")
    
    # 7. Generate SFT messages
    msgs = []
    for c in new_all_cases:
        hr, hs = bool(c["gold"]["read"]), bool(c["gold"]["store"])
        shape = "READ + STORE joint" if (hr and hs) else ("READ-only" if hr else "STORE/SKIP-only")
        msgs.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": render_user_input(c)},
                {"role": "assistant", "content": c["gold"]["dsl"]},
            ],
            "case_id": c["case_id"],
            "source": "v05_batch300_dry_run",
            "metadata": {
                "tags": c["tags"],
                "num_candidate_memories": len(c["candidate_memories"]),
                "num_current_units": len(c["current_units"]),
                "gold_shape": shape,
                "store_targets": [s["target"] for s in c["gold"]["store"]],
                "is_final_train_data": False,
            },
        })
    
    with open(ROOT / "data/v05/batches/v05_batch300_sft_messages.jsonl", "w") as f:
        for m in msgs:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    print(f"Wrote {len(msgs)} SFT messages")
    
    # SFT validation
    sft_ok = True
    for i, (c, m) in enumerate(zip(new_all_cases, msgs)):
        assistant = m["messages"][2]["content"]
        if assistant != c["gold"]["dsl"]:
            print(f"SFT MISMATCH: {c['case_id']}")
            sft_ok = False
        if "```" in assistant:
            print(f"SFT MARKDOWN: {c['case_id']}")
            sft_ok = False
        if assistant.strip().startswith("{"):
            print(f"SFT JSON: {c['case_id']}")
            sft_ok = False
        if m["metadata"]["is_final_train_data"]:
            print(f"SFT final_train_data: {c['case_id']}")
            sft_ok = False
    print(f"SFT validation: {'OK' if sft_ok else 'FAIL'}")
    
    # 8. Compute distributions
    targets = Counter()
    for c in new_all_cases:
        for s in c["gold"]["store"]:
            targets[s["target"]] += 1
    total = sum(targets.values())
    svc = targets.get("service_memory", 0)
    task = targets.get("task_state", 0)
    repo = targets.get("repo_memory", 0)
    proj = targets.get("project_memory", 0)
    user = targets.get("user_profile", 0)
    
    shapes = Counter()
    for c in new_all_cases:
        hr, hs = bool(c["gold"]["read"]), bool(c["gold"]["store"])
        shapes["READ+STORE" if (hr and hs) else ("READ-only" if hr else "STORE/SKIP")] += 1
    
    # Tags
    all_tags = Counter()
    for c in new_all_cases:
        for t in c["tags"]:
            all_tags[t] += 1
    
    # Domains
    domains = Counter()
    for c in new_all_cases:
        domains[c["runtime_context"]["project"]] += 1
    
    print(f"\n=== REPAIRED BATCH300 DISTRIBUTION ===")
    print(f"STORE targets:")
    print(f"  service_memory: {svc} ({svc/total*100:.1f}%)")
    print(f"  task_state:     {task} ({task/total*100:.1f}%)")
    print(f"  repo_memory:    {repo} ({repo/total*100:.1f}%)")
    print(f"  project_memory: {proj} ({proj/total*100:.1f}%)")
    print(f"  user_profile:   {user} ({user/total*100:.1f}%)")
    print(f"  Total STORE: {total}")
    print(f"  svc:task gap: {abs(svc/total - task/total)*100:.1f}pp")
    print(f"\nShapes:")
    for k, v in shapes.most_common():
        print(f"  {k}: {v} ({v/300*100:.1f}%)")
    print(f"\nDomains: {dict(domains.most_common())}")
    
    # 9. Compute replacement51 specific distribution
    r51_targets = Counter()
    r51_shapes = Counter()
    for c in REPLACEMENT51:
        for s in c["gold"]["store"]:
            r51_targets[s["target"]] += 1
        hr, hs = bool(c["gold"]["read"]), bool(c["gold"]["store"])
        r51_shapes["READ+STORE" if (hr and hs) else ("READ-only" if hr else "STORE/SKIP")] += 1
    
    r51_total = sum(r51_targets.values())
    print(f"\n=== REPLACEMENT51 DISTRIBUTION ===")
    print(f"  service_memory: {r51_targets.get('service_memory',0)}")
    print(f"  task_state:     {r51_targets.get('task_state',0)}")
    print(f"  repo_memory:    {r51_targets.get('repo_memory',0)}")
    print(f"  project_memory: {r51_targets.get('project_memory',0)}")
    print(f"  user_profile:   {r51_targets.get('user_profile',0)}")
    print(f"  Total STORE: {r51_total}")
    print(f"  Shapes: {dict(r51_shapes)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
