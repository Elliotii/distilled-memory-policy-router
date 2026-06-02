"""Generate 100-case v0.5 gold draft (70 gold_core + 30 gold_hard).

Gold draft is for later final evaluation after review and locking.
NOT locked gold. NOT for training. NOT for model selection.

Independently generated — distinct domains from train-pool and dev.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v04.case_validator import validate_case, validate_jsonl_file
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

# ── Gold core: 70 natural-distribution cases ──────────────────

GOLD_CORE: list[dict[str, Any]] = [
    # ═══ READ-only (13 cases: v05_gold_core_0001 – v05_gold_core_0013) ═══
    {
        "case_id": "v05_gold_core_0001",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "artifact-publisher", "task": "check artifact retention policy"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The artifact-publisher retains build artifacts for 30 days in S3 before automatic deletion, with release artifacts kept permanently."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Artifact retention settings are in config/artifact_policy.yaml with separate TTLs for snapshots and releases."},
        ],
        "current_units": [{"unit_id": "u1", "text": "How long are snapshot builds kept in the artifact store before cleanup?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request"],
        "notes": "READ-only: u1 is a factual lookup about existing retention policy. m1 answers it directly (30 days). m2 is config path, not needed for this lookup.",
    },
    {
        "case_id": "v05_gold_core_0002",
        "runtime_context": {"project": "content-platform", "repo": "cms-backend", "service": "media-processor", "task": "troubleshoot video encoding failure"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The media-processor transcodes uploaded videos to H.264 at 1080p using FFmpeg with a 10-minute timeout per file."},
            {"memory_id": "m2", "target": "service_memory", "content": "The old v2 processor used a fixed bitrate of 5Mbps; the current version uses CRF 23 with variable bitrate."},
            {"memory_id": "m3", "target": "task_state", "content": "The FFmpeg binary was upgraded to version 6.1 last week as part of a security patch cycle."},
        ],
        "current_units": [{"unit_id": "u1", "text": "A 45-minute 4K video upload failed to encode. Did it time out, or is there another issue?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request", "stale_memory", "related_but_useless"],
        "notes": "READ-only with stale and related-but-useless: u1 is a debugging query. m1 provides the timeout info (10 min). m2 is stale old encoding approach. m3 is related (FFmpeg upgrade) but doesn't explain a timeout on a 45-min file.",
    },
    {
        "case_id": "v05_gold_core_0003",
        "runtime_context": {"project": "financial-reporting", "repo": "ledger-service", "service": "reconciliation-engine", "task": "investigate reconciliation gap"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The reconciliation-engine compares ledger entries against bank statements daily and flags any unmatched transactions for manual review."},
            {"memory_id": "m2", "target": "service_memory", "content": "The engine currently tolerates a 2-day lag for bank statement imports before marking an entry as unmatched."},
            {"memory_id": "m3", "target": "repo_memory", "content": "Reconciliation reports are stored in reports/reconciliation/ with YYYY-MM-DD directory naming."},
        ],
        "current_units": [{"unit_id": "u1", "text": "Why is transaction LED-44921 showing as unmatched when the bank statement for that day just arrived?"}],
        "gold": {"read": ["m1", "m2"], "store": [], "skip": ["u1"], "dsl": "READ m1,m2\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request", "read_selectivity"],
        "notes": "READ-only with read_selectivity: u1 is an investigation query. m1 (daily reconciliation) and m2 (2-day lag tolerance) help diagnose. m3 is report path, not directly useful.",
    },
    {
        "case_id": "v05_gold_core_0004",
        "runtime_context": {"project": "health-monitor", "repo": "monitoring-stack", "service": "uptime-checker", "task": "verify check frequency"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The uptime-checker probes every registered endpoint every 30 seconds from 3 geographic regions and logs response times to Prometheus."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Check frequency overrides for specific endpoints are in config/uptime_overrides.yaml."},
        ],
        "current_units": [{"unit_id": "u1", "text": "How often does the uptime-checker hit our API gateway endpoint?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request"],
        "notes": "READ-only: u1 is a factual question. m1 answers directly (30 seconds, 3 regions). m2 is override config path, not needed.",
    },
    {
        "case_id": "v05_gold_core_0005",
        "runtime_context": {"project": "shipping-logistics", "repo": "delivery-router", "service": "route-optimizer", "task": "explain route selection"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The route-optimizer uses a modified Dijkstra algorithm with real-time traffic data and prefers highways over local roads when the time difference exceeds 5 minutes."},
            {"memory_id": "m2", "target": "service_memory", "content": "The legacy v1 optimizer used fixed-distance shortest path with no traffic awareness."},
            {"memory_id": "m3", "target": "task_state", "content": "Traffic data integration with the HERE Maps API was completed in last quarter's infrastructure sprint."},
        ],
        "current_units": [{"unit_id": "u1", "text": "Does the route optimizer prefer highways even when the distance is longer?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request", "stale_memory", "read_selectivity"],
        "notes": "READ-only with stale: u1 is a knowledge question. m1 answers it (prefers highways if >5min saved). m2 is stale legacy. m3 is related infrastructure info but not needed for this question.",
    },
    {
        "case_id": "v05_gold_core_0006",
        "runtime_context": {"project": "compliance-audit", "repo": "audit-engine", "service": "policy-validator", "task": "check policy coverage"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The policy-validator checks infrastructure configurations against 42 compliance rules covering SOC 2, GDPR, and PCI DSS requirements."},
            {"memory_id": "m2", "target": "project_memory", "content": "The compliance-audit project must complete annual SOC 2 Type II certification with all controls passing."},
        ],
        "current_units": [{"unit_id": "u1", "text": "Does the policy-validator cover all the PCI DSS rules, or just some of them?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request", "related_but_useless"],
        "notes": "READ-only: u1 is a coverage question. m1 explains the 42 rules cover PCI DSS. m2 is project-level SOC 2 requirement — related domain but doesn't answer the PCI DSS coverage question.",
    },
    {
        "case_id": "v05_gold_core_0007",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "test-runner", "task": "debug flaky test"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The test-runner retries failed tests up to 2 times before marking them as FAILED, and logs the failure reason and stack trace for each attempt."},
            {"memory_id": "m2", "target": "task_state", "content": "The integration test suite was recently split into 8 parallel shards to reduce total run time from 45 to 12 minutes."},
            {"memory_id": "m3", "target": "service_memory", "content": "The old test-runner used a single-threaded execution model with a hard 30-minute timeout for the entire suite."},
        ],
        "current_units": [{"unit_id": "u1", "text": "The user-auth integration test fails about 1 in 4 runs. Is the retry mechanism catching this?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request", "stale_memory", "related_but_useless"],
        "notes": "READ-only: u1 is a debugging question about flaky test handling. m1 explains the retry mechanism (2 retries). m2 is related (sharding) but doesn't address retry behavior. m3 is stale legacy architecture.",
    },
    {
        "case_id": "v05_gold_core_0008",
        "runtime_context": {"project": "content-platform", "repo": "cms-backend", "service": "search-indexer", "task": "verify index refresh interval"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The search-indexer reindexes content every 5 minutes from the primary database and uses incremental updates based on a last_modified timestamp."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Index configuration including refresh interval and batch size is in config/search_indexer.yaml."},
        ],
        "current_units": [{"unit_id": "u1", "text": "How long after publishing an article does it appear in search results?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request"],
        "notes": "READ-only: u1 is a user-facing latency question. m1 answers it (reindexes every 5 minutes). m2 is config path, not needed.",
    },
    {
        "case_id": "v05_gold_core_0009",
        "runtime_context": {"project": "financial-reporting", "repo": "ledger-service", "service": "tax-calculator", "task": "understand tax rule application"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The tax-calculator applies jurisdiction-specific tax rates based on the billing address ZIP code and maintains a quarterly-updated rate table."},
            {"memory_id": "m2", "target": "service_memory", "content": "Tax-exempt entities are handled by a separate exemption-certificate validator that runs before the tax calculation."},
            {"memory_id": "m3", "target": "project_memory", "content": "The financial-reporting project must apply correct tax rates for all 50 US states plus DC and US territories."},
        ],
        "current_units": [{"unit_id": "u1", "text": "How does the system determine which tax rate to use for a customer in Texas?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request", "related_but_useless", "read_selectivity"],
        "notes": "READ-only with read_selectivity: u1 asks about rate determination. m1 answers (ZIP code + rate table). m2 is about tax-exempt entities, not rate determination. m3 is project scope — interesting context but doesn't explain the mechanism.",
    },
    {
        "case_id": "v05_gold_core_0010",
        "runtime_context": {"project": "health-monitor", "repo": "monitoring-stack", "service": "alert-dispatcher", "task": "check escalation path"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The alert-dispatcher sends critical alerts to the on-call engineer via PagerDuty with a 5-minute acknowledgment timeout before escalating to the secondary contact."},
            {"memory_id": "m2", "target": "repo_memory", "content": "On-call rotation schedules are managed in config/oncall_rotation.yaml with weekly shifts."},
            {"memory_id": "m3", "target": "task_state", "content": "The secondary on-call contact for this week is being updated due to a team member's vacation."},
        ],
        "current_units": [{"unit_id": "u1", "text": "Who gets paged if the primary on-call doesn't acknowledge within 5 minutes?"}],
        "gold": {"read": ["m1", "m2"], "store": [], "skip": ["u1"], "dsl": "READ m1,m2\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request", "related_but_useless"],
        "notes": "READ-only: u1 asks about escalation. m1 (5-min timeout, secondary contact) and m2 (rotation schedule) help answer. m3 is stale task state about a specific week's update.",
    },
    {
        "case_id": "v05_gold_core_0011",
        "runtime_context": {"project": "shipping-logistics", "repo": "delivery-router", "service": "tracking-notifier", "task": "explain notification timing"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The tracking-notifier sends status updates to customers at 3 key points: order picked up, out for delivery, and delivered. Notifications are sent within 2 minutes of the carrier scan event."},
            {"memory_id": "m2", "target": "service_memory", "content": "The old notification system only sent delivery confirmation and did not include pickup or out-for-delivery events."},
        ],
        "current_units": [{"unit_id": "u1", "text": "Will customers get a notification when the package is loaded onto the delivery truck?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request", "stale_memory"],
        "notes": "READ-only: u1 is a customer experience question. m1 answers it (yes, 'out for delivery' notification within 2 minutes). m2 is stale legacy system reference.",
    },
    {
        "case_id": "v05_gold_core_0012",
        "runtime_context": {"project": "compliance-audit", "repo": "audit-engine", "service": "evidence-collector", "task": "verify evidence collection scope"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The evidence-collector gathers AWS CloudTrail logs, IAM policy snapshots, and security group configurations across all accounts in the organization."},
            {"memory_id": "m2", "target": "project_memory", "content": "The compliance-audit project scope covers all production AWS accounts (currently 8) but excludes development sandbox accounts."},
        ],
        "current_units": [{"unit_id": "u1", "text": "Does the evidence-collector pull data from the dev-sandbox account as well?"}],
        "gold": {"read": ["m1", "m2"], "store": [], "skip": ["u1"], "dsl": "READ m1,m2\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request"],
        "notes": "READ-only: u1 asks about scope. m1 (gathers across all org accounts) and m2 (excludes sandbox) together answer: no, sandbox is excluded.",
    },
    {
        "case_id": "v05_gold_core_0013",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "deploy-gate", "task": "check deployment approval rules"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The deploy-gate requires manual approval for production deployments but auto-approves staging deployments after all tests pass."},
            {"memory_id": "m2", "target": "service_memory", "content": "Deploy-gate also enforces a mandatory 30-minute cool-down between production deployments to allow monitoring observation."},
        ],
        "current_units": [{"unit_id": "u1", "text": "Can I deploy to staging without waiting for someone to approve the PR?"}],
        "gold": {"read": ["m1"], "store": [], "skip": ["u1"], "dsl": "READ m1\nSTORE NONE\nSKIP u1"},
        "tags": ["read_only", "temporary_request"],
        "notes": "READ-only: u1 asks about staging deployment rules. m1 answers (auto-approves staging). m2 is about production cool-down, not relevant to staging.",
    },

    # ═══ STORE/SKIP-only (27 cases: v05_gold_core_0014 – v05_gold_core_0040) ═══
    {
        "case_id": "v05_gold_core_0014",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "artifact-publisher", "task": "record artifact naming convention"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "Build artifacts must be named with the pattern {service}-{git_sha}-{timestamp}.tar.gz and uploaded to the artifacts bucket with the build-id prefix."},
            {"unit_id": "u2", "text": "Artifact naming conventions are documented in docs/builds/artifact_naming.md with examples for each service type."},
            {"unit_id": "u3", "text": "I need to check if yesterday's nightly build artifacts were cleaned up."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "temporary_request"],
        "notes": "STORE/SKIP-only: u1 is a durable artifact naming rule (service_memory). u2 is documentation path (repo_memory). u3 is a one-off status check — SKIP.",
    },
    {
        "case_id": "v05_gold_core_0015",
        "runtime_context": {"project": "content-platform", "repo": "cms-backend", "service": "media-processor", "task": "record processing constraints"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The media-processor must reject any video file larger than 2GB and return a 413 status with a message suggesting the user split the file."},
            {"unit_id": "u2", "text": "Add support for AV1 codec transcoding to reduce bandwidth costs for mobile viewers."},
            {"unit_id": "u3", "text": "I'm not sure AV1 is worth the effort since most mobile devices still prefer H.264."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "task_state", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3"},
        "tags": ["store_skip_only", "service_invariant", "task_progress", "service_vs_task_state"],
        "notes": "STORE/SKIP-only with service_vs_task_state: u1 is a durable size limit constraint (service_memory — rejects >2GB). u2 is a feature implementation plan (task_state — 'Add support for AV1'). u3 is undecided opinion — SKIP.",
    },
    {
        "case_id": "v05_gold_core_0016",
        "runtime_context": {"project": "financial-reporting", "repo": "ledger-service", "service": "reconciliation-engine", "task": "record reconciliation rules"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The reconciliation-engine must match transactions using a composite key of transaction_date, amount, and merchant_name with a 1-day date tolerance."},
            {"unit_id": "u2", "text": "Write a reconciliation accuracy report for the CFO that compares this quarter against last quarter."},
            {"unit_id": "u3", "text": "The engine currently only reconciles USD transactions; multi-currency support is planned for the next fiscal year."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "task_state", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a durable matching rule (service_memory). u2 is a current reporting task (task_state). u3 is current limitation status (task_state — 'currently only reconciles USD').",
    },
    {
        "case_id": "v05_gold_core_0017",
        "runtime_context": {"project": "health-monitor", "repo": "monitoring-stack", "service": "uptime-checker", "task": "record check configuration"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The uptime-checker must consider an endpoint DOWN after 3 consecutive failed probes and UP after 2 consecutive successful probes to avoid flapping."},
            {"unit_id": "u2", "text": "Uptime check probe configurations are stored in config/probes.yaml with per-endpoint thresholds and expected status codes."},
            {"unit_id": "u3", "text": "My personal Slack handle for alert DMs is @devops-lead — use it as a test notification target."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "sensitive_boundary"],
        "notes": "STORE/SKIP-only with sensitive_boundary: u1 is durable flapping prevention rule (service_memory). u2 is config file path (repo_memory). u3 contains a personal Slack handle — personal contact info, must SKIP.",
    },
    {
        "case_id": "v05_gold_core_0018",
        "runtime_context": {"project": "shipping-logistics", "repo": "delivery-router", "service": "route-optimizer", "task": "record optimization constraints"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The route-optimizer must never plan a route that exceeds the driver's maximum daily driving hours as defined by DOT regulations."},
            {"unit_id": "u2", "text": "Route optimization algorithm documentation lives in docs/routing/optimization_algorithm.md with pseudocode and complexity analysis."},
            {"unit_id": "u3", "text": "Let's try using a genetic algorithm approach for route optimization next quarter."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a durable safety constraint (service_memory). u2 is doc path (repo_memory). u3 is a future exploration plan (task_state — 'next quarter').",
    },
    {
        "case_id": "v05_gold_core_0019",
        "runtime_context": {"project": "compliance-audit", "repo": "audit-engine", "service": "policy-validator", "task": "record validation scope"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The policy-validator must check every IAM policy for wildcard actions and flag any policy that grants s3:* or iam:* as a CRITICAL finding."},
            {"unit_id": "u2", "text": "Validation rules are defined in config/policy_rules.yaml as structured YAML with rule_id, severity, resource_pattern, and remediation fields."},
            {"unit_id": "u3", "text": "Run the validator against the production account before the auditor visit next Monday."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a durable security rule (service_memory). u2 is config path (repo_memory). u3 is a time-bound task (task_state — 'before Monday').",
    },
    {
        "case_id": "v05_gold_core_0020",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "test-runner", "task": "record test execution policy"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The test-runner must abort the entire test suite if any critical-path test fails, but should continue running non-dependent tests if a non-critical test fails."},
            {"unit_id": "u2", "text": "Write integration tests for the new deploy-gate approval workflow before the end of this sprint."},
            {"unit_id": "u3", "text": "I need to leave early today for a dentist appointment."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "task_state", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3"},
        "tags": ["store_skip_only", "service_invariant", "task_progress", "temporary_request"],
        "notes": "STORE/SKIP-only: u1 is a durable test execution policy (service_memory). u2 is a sprint task (task_state). u3 is irrelevant personal chatter — SKIP.",
    },
    {
        "case_id": "v05_gold_core_0021",
        "runtime_context": {"project": "content-platform", "repo": "cms-backend", "service": "search-indexer", "task": "record indexing constraints"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The search-indexer must index content in the site's primary language within 5 minutes, but secondary-language content may be indexed within 30 minutes."},
            {"unit_id": "u2", "text": "Search index shard configuration is in config/search_shards.yaml with 3 primary shards and 2 replicas per index."},
            {"unit_id": "u3", "text": "Add a search relevance dashboard to track click-through rates by query term."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a durable SLA for indexing (service_memory). u2 is config path (repo_memory). u3 is a feature plan (task_state — 'Add a search relevance dashboard').",
    },
    {
        "case_id": "v05_gold_core_0022",
        "runtime_context": {"project": "financial-reporting", "repo": "ledger-service", "service": "tax-calculator", "task": "record tax calculation rules"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The tax-calculator must round all tax amounts to the nearest cent using half-up rounding after applying the tax rate to the taxable subtotal."},
            {"unit_id": "u2", "text": "Tax calculation tests live under tests/tax/ and must cover all 50 state tax rates plus edge cases for exempt transactions."},
            {"unit_id": "u3", "text": "The tax rate table needs to be updated for the new quarter — the new rates come into effect on July 1st."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a durable rounding rule (service_memory). u2 is test convention (repo_memory). u3 is a scheduled update reminder (task_state).",
    },
    {
        "case_id": "v05_gold_core_0023",
        "runtime_context": {"project": "health-monitor", "repo": "monitoring-stack", "service": "alert-dispatcher", "task": "record alert routing rules"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The alert-dispatcher must route database-related alerts to the DBA team channel and infrastructure alerts to the SRE channel based on the alert's source tag."},
            {"unit_id": "u2", "text": "Alert routing rules are defined in config/alert_routing.yaml with source_tag to channel mappings."},
            {"unit_id": "u3", "text": "Remind me to check the PagerDuty integration after the on-call rotation changes next week."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "temporary_request"],
        "notes": "STORE/SKIP-only: u1 is a durable routing rule (service_memory). u2 is config path (repo_memory). u3 is a personal reminder — one-off, SKIP.",
    },
    {
        "case_id": "v05_gold_core_0024",
        "runtime_context": {"project": "shipping-logistics", "repo": "delivery-router", "service": "tracking-notifier", "task": "record notification rules"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The tracking-notifier must suppress duplicate delivery confirmations if the carrier sends the same scan event multiple times within a 5-minute window."},
            {"unit_id": "u2", "text": "Notification templates live under templates/notifications/ with separate templates for email, SMS, and push notification channels."},
            {"unit_id": "u3", "text": "We plan to add WhatsApp as a notification channel next quarter."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a durable dedup rule (service_memory). u2 is template path (repo_memory). u3 is a future plan (task_state — 'next quarter').",
    },
    {
        "case_id": "v05_gold_core_0025",
        "runtime_context": {"project": "compliance-audit", "repo": "audit-engine", "service": "evidence-collector", "task": "record collection schedule"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The evidence-collector must gather all AWS CloudTrail logs within 1 hour of their generation and store them in the immutable evidence bucket with SSE-KMS encryption."},
            {"unit_id": "u2", "text": "Evidence collection scripts live under scripts/evidence/ and are triggered by a daily cron job defined in cron/evidence_collection.cron."},
            {"unit_id": "u3", "text": "Check if the evidence bucket has enough space for this month's collection volume."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "temporary_request"],
        "notes": "STORE/SKIP-only: u1 is a durable collection requirement (service_memory). u2 is script path (repo_memory). u3 is a one-off check — SKIP.",
    },
    {
        "case_id": "v05_gold_core_0026",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "deploy-gate", "task": "record deployment rules"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The deploy-gate must automatically roll back a production deployment if the error rate exceeds 1% within the first 10 minutes after deployment."},
            {"unit_id": "u2", "text": "Add a pre-deployment checklist validation step that confirms all integration tests passed before the gate opens for production."},
            {"unit_id": "u3", "text": "We are currently evaluating Spinnaker as an alternative to our custom deploy-gate."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "task_state", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a durable auto-rollback rule (service_memory). u2 is a feature plan (task_state). u3 is current evaluation status (task_state — 'currently evaluating').",
    },
]

print(f"Generated {len(GOLD_CORE)} gold_core cases so far...")

# ── Continue GOLD_CORE cases ──────────────────────────────────

GOLD_CORE.extend([
    {
        "case_id": "v05_gold_core_0027",
        "runtime_context": {"project": "content-platform", "repo": "cms-backend", "service": "media-processor", "task": "record processing pipeline"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The media-processor must generate a WebP thumbnail at 400px width for every uploaded image alongside the original file."},
            {"unit_id": "u2", "text": "Thumbnail generation is handled by a separate worker pool configured in config/thumbnail_workers.yaml with queue size and concurrency settings."},
            {"unit_id": "u3", "text": "I prefer images to be served as WebP by default with JPEG fallback for older browsers."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}, {"target": "user_profile", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE user_profile u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "user_profile_boundary"],
        "notes": "STORE/SKIP-only: u1 is durable thumbnail requirement (service_memory). u2 is config path (repo_memory). u3 is a stable non-sensitive image format preference (user_profile).",
    },
    {
        "case_id": "v05_gold_core_0028",
        "runtime_context": {"project": "financial-reporting", "repo": "ledger-service", "service": "reconciliation-engine", "task": "record project scope decision"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The financial-reporting project does not support cryptocurrency transactions; all ledger entries must be denominated in fiat currency."},
            {"unit_id": "u2", "text": "The reconciliation-engine must flag any transaction where the amount differs from the bank statement by more than 0.01 as a REVIEW_REQUIRED item."},
            {"unit_id": "u3", "text": "Prepare the quarterly reconciliation summary for the audit committee meeting next month."},
        ],
        "gold": {"read": [], "store": [{"target": "project_memory", "unit_id": "u1"}, {"target": "service_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "project_vs_repo", "service_invariant", "task_progress"],
        "notes": "STORE/SKIP-only with project_memory: u1 is a durable project-level scope exclusion (project_memory — no crypto). u2 is a specific service rule (service_memory). u3 is a time-bound task (task_state).",
    },
    {
        "case_id": "v05_gold_core_0029",
        "runtime_context": {"project": "health-monitor", "repo": "monitoring-stack", "service": "uptime-checker", "task": "record repo conventions"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "All uptime-checker probes must log their results to Prometheus using the gauge metric type with labels for endpoint, region, and status_code."},
            {"unit_id": "u2", "text": "Check probe implementations live under internal/probes/ with one Go file per protocol: http.go, tcp.go, dns.go."},
            {"unit_id": "u3", "text": "Run the probe test suite with go test ./internal/probes/... -count=1 before submitting the PR."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}, {"target": "repo_memory", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE repo_memory u3\nSKIP NONE"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention"],
        "notes": "STORE/SKIP-only with dual repo_memory: u1 is durable logging requirement (service_memory). u2 is source code path (repo_memory). u3 is a test command convention (repo_memory).",
    },
    {
        "case_id": "v05_gold_core_0030",
        "runtime_context": {"project": "shipping-logistics", "repo": "delivery-router", "service": "route-optimizer", "task": "record user preferences"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "I prefer delivery route maps to show traffic conditions as color-coded overlays rather than numeric delay estimates."},
            {"unit_id": "u2", "text": "The route-optimizer currently displays estimated delay in minutes next to each alternative route."},
            {"unit_id": "u3", "text": "My home address for delivery testing is 789 Pine Street, Portland, OR 97201."},
        ],
        "gold": {"read": [], "store": [{"target": "user_profile", "unit_id": "u1"}, {"target": "task_state", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE user_profile u1\nSTORE task_state u2\nSKIP u3"},
        "tags": ["store_skip_only", "user_profile_boundary", "task_progress", "sensitive_boundary", "user_profile_vs_sensitive_private"],
        "notes": "STORE/SKIP-only with user_profile_vs_sensitive: u1 is a stable display preference (user_profile). u2 is current behavior (task_state). u3 contains a personal home address — PII, must SKIP.",
    },
    {
        "case_id": "v05_gold_core_0031",
        "runtime_context": {"project": "compliance-audit", "repo": "audit-engine", "service": "policy-validator", "task": "record cross-service policy"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "All compliance-audit services must encrypt data at rest using AES-256 with keys managed through AWS KMS and rotated every 90 days."},
            {"unit_id": "u2", "text": "The policy-validator checks encryption configurations for S3 buckets, RDS instances, and EBS volumes across all accounts."},
            {"unit_id": "u3", "text": "Update the KMS key policy to grant the audit-engine service role encrypt and decrypt permissions."},
        ],
        "gold": {"read": [], "store": [{"target": "project_memory", "unit_id": "u1"}, {"target": "service_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "project_vs_repo", "service_invariant", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a cross-service encryption policy (project_memory — 'All compliance-audit services must'). u2 is specific validator behavior (service_memory). u3 is current action (task_state).",
    },
    {
        "case_id": "v05_gold_core_0032",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "artifact-publisher", "task": "record build conventions"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "All Docker images built by the CI pipeline must be tagged with both the git SHA and the semantic version before pushing to the container registry."},
            {"unit_id": "u2", "text": "Container image build definitions are in docker/ with one Dockerfile per service and a common base image in docker/base/."},
            {"unit_id": "u3", "text": "I need to check if the image for service-api was pushed with the correct version tag yesterday."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3"},
        "tags": ["store_skip_only", "service_invariant", "repo_convention", "temporary_request"],
        "notes": "STORE/SKIP-only: u1 is a durable tagging rule (service_memory). u2 is Dockerfile paths (repo_memory). u3 is a one-off verification — SKIP.",
    },
    {
        "case_id": "v05_gold_core_0033",
        "runtime_context": {"project": "content-platform", "repo": "cms-backend", "service": "search-indexer", "task": "record project constraints"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The content-platform project must never index draft or unpublished content; only articles with status published may appear in search results."},
            {"unit_id": "u2", "text": "The search-indexer queries the content database every 5 minutes and filters by status='published' before sending documents to the index."},
            {"unit_id": "u3", "text": "Write a content moderation guide for editors that explains how to unpublish an article and remove it from search."},
        ],
        "gold": {"read": [], "store": [{"target": "project_memory", "unit_id": "u1"}, {"target": "service_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "project_vs_repo", "service_invariant", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a project-level content safety rule (project_memory). u2 is the indexer's implementation of that rule (service_memory). u3 is current documentation task (task_state).",
    },
    {
        "case_id": "v05_gold_core_0034",
        "runtime_context": {"project": "financial-reporting", "repo": "ledger-service", "service": "tax-calculator", "task": "record test conventions"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "Tax calculation unit tests must use the tax_rate_fixtures.json file from tests/fixtures/ which contains pre-computed expected results for all 50 states."},
            {"unit_id": "u2", "text": "Run tax tests with pytest tests/tax/ --tax-fixtures and ensure the tax_rate_fixtures.json is up to date before each test run."},
            {"unit_id": "u3", "text": "Let me know when the tax rate fixtures have been updated for the new quarter."},
        ],
        "gold": {"read": [], "store": [{"target": "repo_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE repo_memory u1\nSTORE repo_memory u2\nSKIP u3"},
        "tags": ["store_skip_only", "repo_convention", "temporary_request"],
        "notes": "STORE/SKIP-only: u1 is fixture path convention (repo_memory). u2 is test command convention (repo_memory). u3 is a one-off notification request — SKIP.",
    },
    {
        "case_id": "v05_gold_core_0035",
        "runtime_context": {"project": "health-monitor", "repo": "monitoring-stack", "service": "alert-dispatcher", "task": "record project scope"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The health-monitor project does not monitor end-user devices or client-side performance; it monitors only server-side infrastructure and APIs."},
            {"unit_id": "u2", "text": "The alert-dispatcher sends notifications only for server-side alerts categorized as infrastructure, database, or api-gateway."},
            {"unit_id": "u3", "text": "We should consider adding client-side Real User Monitoring in the next planning cycle."},
        ],
        "gold": {"read": [], "store": [{"target": "project_memory", "unit_id": "u1"}, {"target": "service_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "project_vs_repo", "service_invariant", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a project-level scope exclusion (project_memory — no client-side). u2 is specific dispatcher behavior (service_memory). u3 is future consideration (task_state).",
    },
    {
        "case_id": "v05_gold_core_0036",
        "runtime_context": {"project": "shipping-logistics", "repo": "delivery-router", "service": "tracking-notifier", "task": "record user preference"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "I prefer tracking notifications delivered as a single daily digest email rather than individual alerts for each status change."},
            {"unit_id": "u2", "text": "The tracking-notifier currently sends individual notifications for each scan event (pickup, out-for-delivery, delivered)."},
            {"unit_id": "u3", "text": "My personal phone number for SMS delivery alerts is +1-555-0100."},
        ],
        "gold": {"read": [], "store": [{"target": "user_profile", "unit_id": "u1"}, {"target": "task_state", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE user_profile u1\nSTORE task_state u2\nSKIP u3"},
        "tags": ["store_skip_only", "user_profile_boundary", "task_progress", "sensitive_boundary"],
        "notes": "STORE/SKIP-only with user_profile: u1 is a stable notification preference (user_profile — daily digest). u2 is current behavior (task_state). u3 contains a phone number — PII, must SKIP.",
    },
    {
        "case_id": "v05_gold_core_0037",
        "runtime_context": {"project": "compliance-audit", "repo": "audit-engine", "service": "evidence-collector", "task": "record repo structure"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "Evidence collection Terraform modules live under terraform/modules/evidence/ with separate submodules for CloudTrail, IAM, and VPC flow logs."},
            {"unit_id": "u2", "text": "Run terraform plan in the evidence directory before applying any changes to the collector infrastructure."},
            {"unit_id": "u3", "text": "Schedule a review of the Terraform state files for the evidence collection modules."},
        ],
        "gold": {"read": [], "store": [{"target": "repo_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE repo_memory u1\nSTORE repo_memory u2\nSKIP u3"},
        "tags": ["store_skip_only", "repo_convention", "temporary_request"],
        "notes": "STORE/SKIP-only: u1 is Terraform module paths (repo_memory). u2 is an infra command convention (repo_memory). u3 is a one-off scheduling request — SKIP.",
    },
    {
        "case_id": "v05_gold_core_0038",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "test-runner", "task": "record user preferences"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "I prefer test failure reports grouped by package rather than by test class, with the slowest tests listed first."},
            {"unit_id": "u2", "text": "The test-runner currently groups failures by test class alphabetically and does not sort by duration."},
            {"unit_id": "u3", "text": "My CI access token for triggering builds remotely is ci-tok-1234-abcd."},
        ],
        "gold": {"read": [], "store": [{"target": "user_profile", "unit_id": "u1"}, {"target": "task_state", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE user_profile u1\nSTORE task_state u2\nSKIP u3"},
        "tags": ["store_skip_only", "user_profile_boundary", "task_progress", "sensitive_boundary"],
        "notes": "STORE/SKIP-only with sensitive_boundary: u1 is a stable reporting preference (user_profile). u2 is current behavior (task_state). u3 contains an access token — credential, must SKIP.",
    },
    {
        "case_id": "v05_gold_core_0039",
        "runtime_context": {"project": "content-platform", "repo": "cms-backend", "service": "media-processor", "task": "record project encoding policy"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The content-platform project requires all video content to be encoded in at least 3 resolutions (360p, 720p, 1080p) for adaptive streaming support."},
            {"unit_id": "u2", "text": "The media-processor generates an HLS manifest alongside the encoded video segments for each resolution."},
            {"unit_id": "u3", "text": "Add 4K encoding support to the media-processor for premium content creators."},
        ],
        "gold": {"read": [], "store": [{"target": "project_memory", "unit_id": "u1"}, {"target": "service_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ NONE\nSTORE project_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["store_skip_only", "project_vs_repo", "service_invariant", "task_progress"],
        "notes": "STORE/SKIP-only: u1 is a project-level encoding requirement (project_memory — 3 resolutions). u2 is specific processor behavior (service_memory). u3 is feature plan (task_state — 'Add 4K').",
    },
    {
        "case_id": "v05_gold_core_0040",
        "runtime_context": {"project": "financial-reporting", "repo": "ledger-service", "service": "reconciliation-engine", "task": "record stale pattern recognition"},
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The reconciliation-engine now uses PostgreSQL 15 for the transaction store. The old engine used MongoDB 4.2 which lacked transaction support."},
            {"unit_id": "u2", "text": "The MongoDB-based reconciliation scripts under scripts/legacy_reconciliation/ should be archived now that all data is in PostgreSQL."},
            {"unit_id": "u3", "text": "I still think MongoDB was faster for our use case — maybe we should benchmark it again."},
        ],
        "gold": {"read": [], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "task_state", "unit_id": "u2"}], "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3"},
        "tags": ["store_skip_only", "service_invariant", "task_progress", "stale_memory"],
        "notes": "STORE/SKIP-only with stale_memory: u1 documents current technology choice (service_memory — PG15). u2 is a cleanup task (task_state). u3 is a nostalgic opinion about deprecated tech — SKIP as non-actionable.",
    },
])

# The remaining gold_core READ+STORE joint cases (0041-0070) and all gold_hard cases
# will be added in the next section.

print(f"Extended gold_core to {len(GOLD_CORE)} cases.")

# ── GOLD_CORE READ+STORE joint cases (v05_gold_core_0041 – v05_gold_core_0070) ──

GOLD_CORE.extend([
    {
        "case_id": "v05_gold_core_0041",
        "runtime_context": {"project": "ci-pipeline", "repo": "build-system", "service": "deploy-gate", "task": "add canary deployment support"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The deploy-gate currently deploys to all production instances simultaneously with a 10-minute error-rate monitoring window."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Deployment strategies are configured in config/deploy_strategies.yaml with blue-green and rolling options already supported."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The deploy-gate must support canary deployments that route 5% of production traffic to the new version for 15 minutes before rolling out to 100%."},
            {"unit_id": "u2", "text": "Canary deployment configuration must be added to config/deploy_strategies.yaml under a new canary section."},
            {"unit_id": "u3", "text": "Test the canary deployment on the staging environment with the service-api before enabling it for production."},
        ],
        "gold": {"read": ["m1", "m2"], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "repo_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["read_store_joint", "service_invariant", "repo_convention", "task_progress"],
        "notes": "READ+STORE joint: reads m1 (current deploy behavior) and m2 (config structure). Stores u1 (durable canary capability — service_memory), u2 (config path — repo_memory), u3 (testing plan — task_state).",
    },
    {
        "case_id": "v05_gold_core_0042",
        "runtime_context": {"project": "content-platform", "repo": "cms-backend", "service": "search-indexer", "task": "add faceted search"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The search-indexer currently supports full-text search across article titles and body text with basic relevance scoring."},
            {"memory_id": "m2", "target": "service_memory", "content": "The index schema includes fields for author, category, publish_date, and tags but these are not yet exposed as filterable facets."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The search-indexer must support faceted search allowing users to filter results by category, author, and date range."},
            {"unit_id": "u2", "text": "Facet counts must be returned alongside search results showing the number of matching documents per category and per author."},
            {"unit_id": "u3", "text": "Add the faceted search API endpoint and update the frontend search component to display the facet filters."},
        ],
        "gold": {"read": ["m1", "m2"], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "service_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["read_store_joint", "service_invariant", "task_progress"],
        "notes": "READ+STORE joint: reads m1 (current search) and m2 (index schema). Stores u1 (durable faceted search capability — service_memory), u2 (facet count behavior — service_memory), u3 (implementation plan — task_state).",
    },
    {
        "case_id": "v05_gold_core_0043",
        "runtime_context": {"project": "financial-reporting", "repo": "ledger-service", "service": "tax-calculator", "task": "add tax exemption handling"},
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The tax-calculator currently applies the standard rate for every transaction and does not check for tax-exempt status."},
            {"memory_id": "m2", "target": "service_memory", "content": "The customer database includes a tax_exempt boolean field and an exemption_certificate_expiry date field that are not yet read by the calculator."},
            {"memory_id": "m3", "target": "project_memory", "content": "The financial-reporting project must correctly handle tax-exempt entities to comply with IRS regulations."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The tax-calculator must check the customer's tax_exempt flag before applying any tax rate and skip calculation for exempt customers."},
            {"unit_id": "u2", "text": "If the exemption_certificate_expiry date has passed, the calculator must treat the customer as non-exempt and apply the standard rate with a warning log."},
            {"unit_id": "u3", "text": "Add the tax exemption check to the calculator pipeline before the rate lookup step."},
        ],
        "gold": {"read": ["m1", "m2", "m3"], "store": [{"target": "service_memory", "unit_id": "u1"}, {"target": "service_memory", "unit_id": "u2"}, {"target": "task_state", "unit_id": "u3"}],
            "skip": [], "dsl": "READ m1,m2,m3\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE"},
        "tags": ["read_store_joint", "service_invariant", "task_progress"],
        "notes": "READ+STORE joint: reads all three memories. Stores u1 (durable exemption check — service_memory), u2 (expiry behavior — service_memory), u3 (implementation — task_state).",
    },
])

print(f"Extended gold_core to {len(GOLD_CORE)} cases")

# ── Load remaining gold_core cases from external file ──────────

# ── NOTE: Canonical gold draft lives in v05_gold_draft_cases.jsonl ──
# The embedded GOLD_CORE cases above represent the initial composition.
# The canonical file has been post-processed for distribution balance.
# This script now loads from the canonical JSONL for validation + SFT generation.

CANONICAL_GOLD = ROOT / "data/v05/gold/v05_gold_draft_cases.jsonl"
if CANONICAL_GOLD.exists():
    with open(CANONICAL_GOLD) as f:
        ALL_CASES = [json.loads(line) for line in f if line.strip()]
    GOLD_CORE = [c for c in ALL_CASES if "gold_core" in c["case_id"]]
    GOLD_HARD = [c for c in ALL_CASES if "gold_hard" in c["case_id"]]
    print(f"Loaded {len(ALL_CASES)} cases from canonical gold draft (core={len(GOLD_CORE)}, hard={len(GOLD_HARD)})")
else:
    # Fallback: merge embedded + external files
    GOLD_CORE_REST_PATH = ROOT / "data/v05/gold/v05_gold_core_rest.jsonl"
    if GOLD_CORE_REST_PATH.exists():
        with open(GOLD_CORE_REST_PATH) as f:
            GOLD_CORE.extend([json.loads(line) for line in f if line.strip()])
    GOLD_HARD_PATH = ROOT / "data/v05/gold/v05_gold_hard_draft_cases.jsonl"
    GOLD_HARD = []
    if GOLD_HARD_PATH.exists():
        with open(GOLD_HARD_PATH) as f:
            GOLD_HARD = [json.loads(line) for line in f if line.strip()]
    ALL_CASES = GOLD_CORE + GOLD_HARD
    print(f"Merged {len(ALL_CASES)} cases from embedded + external files")

# ── Validation ────────────────────────────────────────────────

def validate_all(cases: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    all_ok = True
    errors: list[str] = []

    if len(cases) != 100:
        all_ok = False
        errors.append(f"Expected 100 cases, got {len(cases)}")

    core_ids = [c["case_id"] for c in cases if "gold_core" in c["case_id"]]
    hard_ids = [c["case_id"] for c in cases if "gold_hard" in c["case_id"]]
    if len(core_ids) != 70:
        all_ok = False
        errors.append(f"Expected 70 gold_core, got {len(core_ids)}")
    if len(hard_ids) != 30:
        all_ok = False
        errors.append(f"Expected 30 gold_hard, got {len(hard_ids)}")

    for case in cases:
        cid = case["case_id"]
        result = validate_case(case)
        if not result["valid"]:
            all_ok = False
            for e in result["errors"]:
                errors.append(f"{cid}: {e}")

        dsl = case["gold"]["dsl"]
        mem_ids = [m["memory_id"] for m in case["candidate_memories"]]
        unit_ids = [u["unit_id"] for u in case["current_units"]]
        parsed = parse_policy_dsl(dsl, mem_ids, unit_ids, LEGAL_TARGETS)
        if not parsed["validation"]["valid"]:
            all_ok = False
            for e in parsed["validation"]["errors"]:
                errors.append(f"{cid} DSL: {e}")

        parsed_read = {item["memory_id"] for item in parsed["read"]}
        parsed_store = {item["unit_id"]: item["target"] for item in parsed["store"]}
        parsed_skip = {item["unit_id"] for item in parsed["skip"]}
        gold_read = set(case["gold"]["read"])
        gold_store = {s["unit_id"]: s["target"] for s in case["gold"]["store"]}
        gold_skip = set(case["gold"]["skip"])

        if parsed_read != gold_read:
            all_ok = False
            errors.append(f"{cid} READ mismatch")
        if parsed_store != gold_store:
            all_ok = False
            errors.append(f"{cid} STORE mismatch: parsed={parsed_store} gold={gold_store}")
        if parsed_skip != gold_skip:
            all_ok = False
            errors.append(f"{cid} SKIP mismatch")

        store_units = {s["unit_id"] for s in case["gold"]["store"]}
        skip_units = set(case["gold"]["skip"])
        all_units = {u["unit_id"] for u in case["current_units"]}
        covered = store_units | skip_units
        both = store_units & skip_units
        missing = all_units - covered
        if both:
            all_ok = False
            errors.append(f"{cid} unit in both: {both}")
        if missing:
            all_ok = False
            errors.append(f"{cid} unit missing: {missing}")

        read_set = set(case["gold"]["read"])
        mem_set = {m["memory_id"] for m in case["candidate_memories"]}
        invalid_reads = read_set - mem_set
        if invalid_reads:
            all_ok = False
            errors.append(f"{cid} invalid READ: {invalid_reads}")

        for s in case["gold"]["store"]:
            if s["target"] not in LEGAL_TARGETS:
                all_ok = False
                errors.append(f"{cid} invalid target: {s['target']}")
            if s["unit_id"] not in all_units:
                all_ok = False
                errors.append(f"{cid} invalid STORE unit_id: {s['unit_id']}")

        sensitive_patterns = [
            "my password is", "my api key", "my phone number is", "my address is",
            "my passport", "my credit card", "my recovery code", "my backup email",
            "my personal email", "my mother's maiden", "webhook url is http",
            "my ssn", "my social security", "my driver's license", "cvv ",
        ]
        for s in case["gold"]["store"]:
            uid = s["unit_id"]
            for u in case["current_units"]:
                if u["unit_id"] == uid:
                    text = u["text"].lower()
                    for pat in sensitive_patterns:
                        if pat in text:
                            all_ok = False
                            errors.append(f"{cid} SENSITIVE STORE: {uid} contains '{pat}'")

    return all_ok, errors

def compute_distributions(cases):
    total = len(cases)
    ro = sum(1 for c in cases if c["gold"]["read"] and not c["gold"]["store"])
    so = sum(1 for c in cases if not c["gold"]["read"] and c["gold"]["store"])
    rj = sum(1 for c in cases if c["gold"]["read"] and c["gold"]["store"])
    targets = [s["target"] for c in cases for s in c["gold"]["store"]]
    tc = Counter(targets)
    total_store = sum(tc.values())
    return {
        "total": total, "read_only": ro, "store_skip_only": so, "read_store_joint": rj,
        "total_store": total_store, "target_counts": dict(tc),
        "target_pcts": {t: c/total_store*100 for t, c in tc.items()} if total_store else {},
    }

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

def build_sft(cases):
    def render(case):
        rc = case["runtime_context"]
        ctx = ["RUNTIME_CONTEXT", f"project: {rc['project']}", f"repo: {rc['repo']}",
               f"service: {rc['service']}", f"task: {rc['task']}"]
        mems = case["candidate_memories"]
        mem_lines = ["CANDIDATE_MEMORIES"]
        if mems:
            for m in mems:
                mem_lines.append(f"{m['memory_id']} [{m['target']}]: {m['content']}")
        else:
            mem_lines.append("NONE")
        units = case["current_units"]
        unit_lines = ["CURRENT_UNITS"]
        for u in units:
            unit_lines.append(f"{u['unit_id']}: {u['text']}")
        return "\n".join(ctx + [""] + mem_lines + [""] + unit_lines)

    msgs = []
    for case in cases:
        dsl = case["gold"]["dsl"]
        gs = case["gold"]["store"]
        hr = bool(case["gold"]["read"])
        hs = bool(gs)
        shape = "READ + STORE joint" if (hr and hs) else "READ-only" if hr else "STORE/SKIP-only" if hs else "other"
        partition = "gold_core" if "gold_core" in case["case_id"] else "gold_hard"
        msg = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": render(case)},
                {"role": "assistant", "content": dsl},
            ],
            "case_id": case["case_id"],
            "source": "v05_gold_draft",
            "metadata": {
                "tags": case["tags"],
                "num_candidate_memories": len(case["candidate_memories"]),
                "num_current_units": len(case["current_units"]),
                "gold_shape": shape,
                "store_targets": [s["target"] for s in gs],
                "is_final_train_data": False,
                "is_locked_gold": False,
                "gold_partition": partition,
                "split": "gold_draft",
            },
        }
        msgs.append(msg)
    return msgs

def main():
    print(f"\n=== Validating {len(ALL_CASES)} gold draft cases ===\n")
    ok, errors = validate_all(ALL_CASES)
    if errors:
        for e in errors[:30]:
            print(f"  ❌ {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors)-30} more")
    if not ok:
        print(f"\n❌ {len(errors)} validation errors")
        raise SystemExit(1)

    print("✅ All validations passed\n")

    # Distributions
    dist = compute_distributions(ALL_CASES)
    print(f"Cases: {dist['total']} (core={len(GOLD_CORE)}, hard={len(GOLD_HARD)})")
    print(f"Shapes: READ-only={dist['read_only']}, STORE/SKIP={dist['store_skip_only']}, Joint={dist['read_store_joint']}")
    print(f"STORE units: {dist['total_store']}")
    for t in ["service_memory","task_state","repo_memory","project_memory","user_profile"]:
        cnt = dist["target_counts"].get(t,0)
        pct = dist["target_pcts"].get(t,0)
        print(f"  {t}: {cnt} ({pct:.1f}%)")

    # Write cases
    CASES_OUT = ROOT / "data/v05/gold/v05_gold_draft_cases.jsonl"
    with open(CASES_OUT, "w", encoding="utf-8") as f:
        for case in ALL_CASES:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(ALL_CASES)} cases to {CASES_OUT}")

    # Write SFT
    SFT_OUT = ROOT / "data/v05/gold/v05_gold_draft_sft_messages.jsonl"
    msgs = build_sft(ALL_CASES)
    with open(SFT_OUT, "w", encoding="utf-8") as f:
        for msg in msgs:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(msgs)} SFT messages to {SFT_OUT}")

    # Validate SFT
    sft_ok = True
    for case, msg in zip(ALL_CASES, msgs):
        assistant = msg["messages"][2]["content"]
        if assistant != case["gold"]["dsl"]:
            print(f"  ❌ SFT mismatch: {case['case_id']}")
            sft_ok = False
        if "```" in assistant:
            print(f"  ❌ Markdown: {case['case_id']}")
            sft_ok = False
        if assistant.strip().startswith("{"):
            print(f"  ❌ JSON: {case['case_id']}")
            sft_ok = False
    if sft_ok:
        print("✅ SFT validation passed")

    # Write core/hard split files
    CORE_OUT = ROOT / "data/v05/gold/v05_gold_core_draft_cases.jsonl"
    HARD_OUT = ROOT / "data/v05/gold/v05_gold_hard_draft_cases.jsonl"
    with open(CORE_OUT, "w") as f:
        for c in GOLD_CORE:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(HARD_OUT, "w") as f:
        for c in GOLD_HARD:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Wrote {len(GOLD_CORE)} core to {CORE_OUT}")
    print(f"Wrote {len(GOLD_HARD)} hard to {HARD_OUT}")

    print("\n=== GOLD DRAFT GENERATION COMPLETE ===")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
