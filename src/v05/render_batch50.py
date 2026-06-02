"""Generate v0.5 batch50: 20 seed + 30 new = 50 total cases + SFT messages.

Scope: batch50 validation only. Not final train/dev/gold. Not locked.
Context: P5.7-E — v0.5 batch50 data expansion and validation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from collections import Counter
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v05.render_sft_messages import (
    SYSTEM_PROMPT,
    render_user_input,
    build_sft_message,
)


# ═══════════════════════════════════════════════════════════════════
# 30 NEW BATCH50 CASES
# ═══════════════════════════════════════════════════════════════════

NEW30_CASES: list[dict[str, Any]] = [
    # ── READ-only (5) ──
    {
        "case_id": "v05_batch50_0001",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "check pipeline schedule",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The pipeline runs daily at 06:00 UTC and processes all tables in dependency order."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Pipeline schedule overrides are stored in config/pipeline_schedule.yaml."},
            {"memory_id": "m3", "target": "service_memory", "content": "The old v1 pipeline used cron-based scheduling with a single nightly batch."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "What time does the pipeline run on weekends?"},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ m1,m2\nSTORE NONE\nSKIP u1",
        },
        "tags": ["read_only", "stale_memory", "temporary_request"],
        "notes": "READ-only: u1 is a factual lookup question (transient). m1 and m2 are both needed to answer (schedule + overrides). m3 is stale legacy scheduling approach.",
    },
    {
        "case_id": "v05_batch50_0002",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "camera",
            "task": "debug camera startup crash",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The camera module initializes the hardware driver in onCreate and releases it in onDestroy."},
            {"memory_id": "m2", "target": "task_state", "content": "The last camera bug was a race condition on HDR initialization that was fixed last release."},
            {"memory_id": "m3", "target": "repo_memory", "content": "Camera module code lives under app/src/main/java/com/fieldapp/camera/."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The camera crashes on startup on Android 14 devices, show me the initialization code."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ m1\nSTORE NONE\nSKIP u1",
        },
        "tags": ["read_only", "stale_memory", "related_but_useless"],
        "notes": "READ-only: u1 is a debug request (transient). m1 is needed to understand the crash. m2 is stale (old bug, different issue). m3 is repo path but m1 has the behavioral info needed.",
    },
    {
        "case_id": "v05_batch50_0003",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "case_validator",
            "task": "check current validation rules",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The case validator checks that every current unit appears exactly once in gold.store or gold.skip."},
            {"memory_id": "m2", "target": "service_memory", "content": "The case validator also verifies that gold.dsl parses consistently with structured gold fields."},
            {"memory_id": "m3", "target": "project_memory", "content": "The v0.4 case schema defines gold as read, store, skip, and optional dsl."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "What checks does the case validator perform on gold data?"},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ m1,m2\nSTORE NONE\nSKIP u1",
        },
        "tags": ["read_only", "temporary_request", "related_but_useless"],
        "notes": "READ-only: u1 is a knowledge question. m1 and m2 both answer the question. m3 is project-level context but not directly about validator checks.",
    },
    {
        "case_id": "v05_batch50_0004",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "export",
            "task": "investigate missing invoice",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The export job writes invoices to S3 bucket export-invoices-prod with prefix by date."},
            {"memory_id": "m2", "target": "service_memory", "content": "Export failures are logged to CloudWatch under the log group /export/job-errors."},
            {"memory_id": "m3", "target": "task_state", "content": "Yesterday's export run completed at 02:15 UTC with 243 invoices written."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Why is invoice INV-2026-0582 missing from the S3 bucket?"},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ m1,m2\nSTORE NONE\nSKIP u1",
        },
        "tags": ["read_only", "related_but_useless", "temporary_request"],
        "notes": "READ-only: u1 is a debugging query. m1 (S3 location) and m2 (error logs) help investigate. m3 is stale task state — knowing yesterday's count doesn't explain this specific missing invoice.",
    },
    {
        "case_id": "v05_batch50_0005",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "sync",
            "task": "verify sync queue limits",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The sync offline queue has a maximum capacity of 5000 pending entries before it rejects new edits."},
            {"memory_id": "m2", "target": "service_memory", "content": "When the queue exceeds 4000 entries, the app shows a warning banner to the user."},
            {"memory_id": "m3", "target": "repo_memory", "content": "Queue limits are configurable in config/sync_limits.yaml but require a restart to apply."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "How many pending entries trigger the warning banner?"},
        ],
        "gold": {
            "read": ["m2"],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ m2\nSTORE NONE\nSKIP u1",
        },
        "tags": ["read_only", "related_but_useless", "temporary_request"],
        "notes": "READ-only: u1 is a specific factual question. Only m2 answers it directly. m1 provides context (max capacity) but not the warning threshold. m3 is repo config info, not needed.",
    },

    # ── STORE/SKIP-only (8) ──
    {
        "case_id": "v05_batch50_0006",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "add data quality check step",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The pipeline must reject any batch where the row count deviates by more than 10% from the 7-day average."},
            {"unit_id": "u2", "text": "Implement the row-count check in the validation stage before the transform stage."},
            {"unit_id": "u3", "text": "The 7-day average is calculated from the pipeline_metrics table in the analytics DB."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
                {"target": "repo_memory", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "service_invariant", "task_progress", "repo_convention", "service_vs_task_state"],
        "notes": "STORE/SKIP-only. u1 defines a durable quality rule for the pipeline → service_memory (WHAT the pipeline enforces). u2 is the current implementation plan → task_state (HOW to implement now). u3 describes where the metric source lives → repo_memory (WHERE the data comes from). Clean three-target distinction.",
    },
    {
        "case_id": "v05_batch50_0007",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "eval_runner",
            "task": "plan evaluation improvements",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The eval_runner must support side-by-side comparison of multiple interfaces in a single run."},
            {"unit_id": "u2", "text": "Add a bar chart output mode to the eval_runner for visualizing per-interface metrics."},
            {"unit_id": "u3", "text": "The v0.5 training targets Qwen3-4B with LoRA, not full fine-tuning."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
                {"target": "project_memory", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE project_memory u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "service_vs_task_state", "project_vs_repo", "target_boundary"],
        "notes": "STORE/SKIP-only with project_memory boundary. u1 is durable eval_runner capability → service_memory. u2 is current feature request → task_state. u3 is a project-level training decision (Qwen3-4B + LoRA) → project_memory. Shows project_memory: training approach is a project-level scope/strategy decision, not just task progress.",
    },
    {
        "case_id": "v05_batch50_0008",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "camera",
            "task": "update camera permission handling",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "Camera permission requests must show a rationale dialog before the system permission prompt on Android 13+."},
            {"unit_id": "u2", "text": "The camera module permission code lives under app/src/main/java/com/fieldapp/camera/permissions/."},
            {"unit_id": "u3", "text": "My personal Google account for app testing is devtest123@gmail.com."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3",
        },
        "tags": ["store_skip_only", "repo_vs_service", "sensitive_boundary"],
        "notes": "STORE/SKIP-only with repo_vs_service and sensitive. u1 is durable permission behavior → service_memory. u2 is repo path → repo_memory. u3 contains a personal email — must SKIP as sensitive.",
    },
    {
        "case_id": "v05_batch50_0009",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "documentation",
            "task": "update project scope docs",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The project scope explicitly excludes retriever training, writer training, and MemoryOS implementation."},
            {"unit_id": "u2", "text": "v0.5 training documentation lives under docs/v05/ with separate plan, data, and format docs."},
            {"unit_id": "u3", "text": "I prefer documentation that shows examples before abstract definitions."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "project_memory", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u2"},
                {"target": "user_profile", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE project_memory u1\nSTORE repo_memory u2\nSTORE user_profile u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "project_vs_repo", "user_profile_boundary", "target_boundary"],
        "notes": "STORE/SKIP-only with user_profile. u1 is project-level scope exclusion → project_memory (durable decision about what the project does NOT do). u2 is repo doc path → repo_memory. u3 is a stable, non-sensitive, cross-project user preference about documentation style → user_profile. Clear three-way boundary across project/repo/user.",
    },
    {
        "case_id": "v05_batch50_0010",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "export",
            "task": "update S3 bucket policy",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The export job must use server-side encryption with KMS key arn:aws:kms:us-east-1:123456789:key/export-key."},
            {"unit_id": "u2", "text": "The KMS key policy is defined in terraform/modules/export/kms.tf."},
            {"unit_id": "u3", "text": "My AWS access key for the test account is AKIA1234567890ABCDEF — use it for testing."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3",
        },
        "tags": ["store_skip_only", "repo_vs_service", "sensitive_boundary"],
        "notes": "STORE/SKIP-only with sensitive. u1 is durable export encryption behavior → service_memory. u2 is repo path → repo_memory. u3 contains a synthetic AWS access key — must SKIP as sensitive credential. Shows sensitive material must always be SKIPped regardless of task relevance.",
    },
    {
        "case_id": "v05_batch50_0011",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "parser",
            "task": "record parser design constraints",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The parser must never guess or infer missing STORE targets from unit text."},
            {"unit_id": "u2", "text": "The parser currently rejects duplicate STORE lines but does not yet reject STORE/SKIP conflicts."},
            {"unit_id": "u3", "text": "Parser source lives under src/v04/parser.py and uses strict line-by-line parsing."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
                {"target": "repo_memory", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "service_invariant", "task_progress", "repo_convention", "service_vs_task_state"],
        "notes": "STORE/SKIP-only with service vs task boundary. u1 is a durable design invariant → service_memory (NEVER guess). u2 describes current implementation gap → task_state (what it currently does vs doesn't do). u3 is repo path → repo_memory. Clear perpetual rule vs current state distinction.",
    },
    {
        "case_id": "v05_batch50_0012",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "sync",
            "task": "record sync testing conventions",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "All sync integration tests must run with a local SQLite database, never against the production sync endpoint."},
            {"unit_id": "u2", "text": "Sync integration tests live under tests/integration/sync/ and use pytest with the sync_test fixture."},
            {"unit_id": "u3", "text": "Remind me to check the CI pipeline logs after this."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "repo_memory", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ NONE\nSTORE repo_memory u1\nSTORE repo_memory u2\nSKIP u3",
        },
        "tags": ["store_skip_only", "repo_convention", "temporary_request"],
        "notes": "STORE/SKIP-only with dual repo_memory. u1 is a durable testing convention → repo_memory (repo-level rule). u2 is repo test path and command → repo_memory. u3 is a one-off reminder → SKIP. Shows that repo_memory covers both conventions and paths.",
    },

    # ── READ + STORE joint (10) ──
    {
        "case_id": "v05_batch50_0013",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "add pipeline retry for deadlocks",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The pipeline uses PostgreSQL as its metadata store with transaction isolation level READ COMMITTED."},
            {"memory_id": "m2", "target": "task_state", "content": "The last pipeline deadlock occurred during the 2026-05-28 night run on the billing_facts table."},
            {"memory_id": "m3", "target": "service_memory", "content": "The old v1 pipeline used MySQL with REPEATABLE READ isolation."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Add a deadlock retry wrapper that catches PostgreSQL error code 40P01 and retries up to 3 times with 1-second backoff."},
            {"unit_id": "u2", "text": "The retry wrapper should log each deadlock occurrence to the pipeline_errors table with the failed query text."},
            {"unit_id": "u3", "text": "Test the deadlock retry on the staging pipeline before deploying to production."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "service_memory", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ m1\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "stale_memory", "repo_vs_service"],
        "notes": "READ+STORE joint with stale. Reads m1 (current pipeline DB isolation). Skips m2 (stale task state — old deadlock, not current). Skips m3 (stale legacy MySQL reference). Stores u1 (durable retry behavior → service_memory) and u2 (durable logging behavior → service_memory). u3 is a current next step → task_state. Shows repo_vs_service: m3 is about a different DB engine (repo-level infrastructure distinction), while m1 is about the current service behavior.",
    },
    {
        "case_id": "v05_batch50_0014",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "notification",
            "task": "add notification priority levels",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The notification service delivers messages via Firebase Cloud Messaging and groups them by priority before sending."},
            {"memory_id": "m2", "target": "user_profile", "content": "The user prefers non-urgent notifications to be delivered silently between 22:00 and 07:00."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Notifications with priority CRITICAL must bypass the silent-hours filter and always trigger an alert sound."},
            {"unit_id": "u2", "text": "The user's home address for field-app deliveries is 1234 Rural Route 7."},
            {"unit_id": "u3", "text": "Add a priority field to the notification payload schema in the API docs."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u3"},
            ],
            "skip": ["u2"],
            "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u3\nSKIP u2",
        },
        "tags": ["read_store_joint", "service_invariant", "sensitive_boundary", "user_profile_boundary"],
        "notes": "READ+STORE joint with user_profile memory and sensitive boundary. Reads m1 (notification behavior) and m2 (user preference for silent hours — relevant because u1's critical-priority rule interacts with the silent-hours preference). Stores u1 (durable CRITICAL priority bypass behavior → service_memory). u2 contains a home address — personal/sensitive information, must SKIP (not user_profile — user_profile is for stable non-sensitive preferences, not personal contact details). Stores u3 (API doc update for priority field → repo_memory documentation convention).",
    },
    {
        "case_id": "v05_batch50_0015",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "prompt_builder",
            "task": "extend prompt builder to support v0.5 system prompt",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The prompt builder renders runtime_context, candidate_memories, and current_units into a structured text format."},
            {"memory_id": "m2", "target": "project_memory", "content": "v0.4 used three separate system prompts for the three interfaces; v0.5 uses one unified system prompt."},
            {"memory_id": "m3", "target": "repo_memory", "content": "Prompt templates live under prompts/v04/ and use python format-string placeholders."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The prompt builder must now also accept an optional few-shot example section to prepend before the current units."},
            {"unit_id": "u2", "text": "Write unit tests for the new few-shot section rendering."},
        ],
        "gold": {
            "read": ["m1", "m3"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": [],
            "dsl": "READ m1,m3\nSTORE service_memory u1\nSTORE task_state u2\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "related_but_useless"],
        "notes": "READ+STORE joint with related-but-useless. Reads m1 (prompt builder behavior) and m3 (template path). Skips m2 (project-level v0.4/v0.5 decision — related but not directly needed for this implementation task). Stores u1 (durable prompt builder capability → service_memory) and u2 (current task: write tests → task_state).",
    },
    {
        "case_id": "v05_batch50_0016",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "export",
            "task": "add export format option",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The export job currently outputs invoices in CSV format with columns: invoice_id, amount, currency, date, status."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Export output format is configured in config/export.yaml under the output_format key."},
            {"memory_id": "m3", "target": "service_memory", "content": "The billing report generator expects CSV input and will fail on any other format."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Add Parquet as an optional output format alongside CSV. The format selection should be per-export-run."},
            {"unit_id": "u2", "text": "Update the billing report generator to also accept Parquet input before enabling the new format in production."},
            {"unit_id": "u3", "text": "My Stripe API test key for the sandbox is sk_test_1234567890abcdef."},
        ],
        "gold": {
            "read": ["m1", "m2", "m3"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ m1,m2,m3\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "sensitive_boundary"],
        "notes": "READ+STORE joint with sensitive. Reads all three memories (all relevant — m3 tells us downstream depends on CSV format, which constrains u1's deployment). Stores u1 (new durable export capability → service_memory). Stores u2 (current blocker/dependency → task_state). Skips u3 (API key → sensitive, must SKIP regardless).",
    },
    {
        "case_id": "v05_batch50_0017",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "training",
            "task": "design v0.5 training data split",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "project_memory", "content": "v0.5 training uses LoRA on Qwen3-4B with supervised fine-tuning, not RLHF or DPO."},
            {"memory_id": "m2", "target": "project_memory", "content": "The project does not train a retriever or memory writer; the router is the only trained component."},
            {"memory_id": "m3", "target": "service_memory", "content": "The eval_runner requires a locked gold set that is never used during training or hyperparameter tuning."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The training split should be 800 train / 100 dev / 100 gold, with gold locked immediately after creation."},
            {"unit_id": "u2", "text": "The project will only ever use synthetic training data; real production data is permanently out of scope."},
            {"unit_id": "u3", "text": "Draft the data split plan section in the training plan doc today."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "task_state", "unit_id": "u1"},
                {"target": "project_memory", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ m1,m2\nSTORE task_state u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["read_store_joint", "project_vs_repo", "target_boundary", "related_but_useless"],
        "notes": "READ+STORE joint with project_memory vs task_state. Reads m1 and m2 (project-level training decisions) but skips m3 (eval_runner behavior — related to gold lock concept but not needed for split planning). u1 is the current split plan → task_state (HOW we split). u2 is a permanent project safety decision (synthetic-only forever) → project_memory (WHAT the project's data policy is). u3 is current writing task → task_state. Shows project_memory as durable scope, not catch-all.",
    },
    {
        "case_id": "v05_batch50_0018",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "camera",
            "task": "optimize camera capture latency",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The camera module uses a double-buffered preview surface with a 200ms frame timeout."},
            {"memory_id": "m2", "target": "service_memory", "content": "HDR processing adds approximately 150ms of latency per frame on the current pipeline."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Reduce the frame timeout from 200ms to 120ms and measure the impact on capture success rate."},
            {"unit_id": "u2", "text": "If capture latency remains above 300ms after the timeout change, profile the HDR pipeline next."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "task_state", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": [],
            "dsl": "READ m1,m2\nSTORE task_state u1\nSTORE task_state u2\nSKIP NONE",
        },
        "tags": ["read_store_joint", "task_progress", "service_vs_task_state", "target_boundary"],
        "notes": "READ+STORE joint where all STOREs are task_state. Both u1 and u2 are current optimization experiments, not durable service behaviors. u1 is a tuning attempt → task_state (experiment). u2 is a conditional next step → task_state (fork in plan). Important: not every service-related unit is service_memory. These are task-level experiments, not settled behaviors. Boundary case: teaches that service-domain units can be task_state when they describe active experiments.",
    },
    {
        "case_id": "v05_batch50_0019",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "document pipeline dependency graph",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The pipeline runs stages in topological order based on a DAG defined in config/pipeline_dag.yaml."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Pipeline DAG visualizations are generated by scripts/visualize_dag.py and output to docs/pipeline/dag.svg."},
            {"memory_id": "m3", "target": "task_state", "content": "The DAG was last updated three weeks ago when the billing stage was renamed to billing_2025."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The dependency graph should be documented in docs/pipeline/dependency_graph.md with each stage's inputs and outputs."},
            {"unit_id": "u2", "text": "Run the DAG visualization script after updating the dependency docs."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "repo_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": [],
            "dsl": "READ m1,m2\nSTORE repo_memory u1\nSTORE task_state u2\nSKIP NONE",
        },
        "tags": ["read_store_joint", "repo_convention", "task_progress", "stale_memory"],
        "notes": "READ+STORE joint with stale. Reads m1 (DAG behavior) and m2 (visualization script). Skips m3 (stale task state — three-week-old rename is no longer current). Stores u1 (repo documentation convention → repo_memory). Stores u2 (current next step → task_state).",
    },
    {
        "case_id": "v05_batch50_0020",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "case_validator",
            "task": "update case validator for v0.5 batch data",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The case validator checks gold.dsl consistency with structured gold fields using the strict parser."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Case validator source lives under src/v04/case_validator.py and tests under tests/v04/."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The case validator should now also check that no sample case duplicates exact text from subset50 or few-shot examples."},
            {"unit_id": "u2", "text": "Add the leakage check function to the case validator before the batch50 validation run."},
            {"unit_id": "u3", "text": "This leakage check is probably a one-time validation; we do not need to keep it permanently."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "service_vs_task_state"],
        "notes": "READ+STORE joint with service vs task. u1 defines a new durable validation rule → service_memory (WHAT the validator checks). u2 is the current implementation task → task_state (WHEN to implement). u3 speculates about temporariness — not a decision, just a guess → SKIP. Shows that speculation (even about the feature itself) should be SKIPped.",
    },
    {
        "case_id": "v05_batch50_0021",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "sync",
            "task": "add conflict resolution strategy",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The sync module currently uses last-write-wins conflict resolution based on modification timestamp."},
            {"memory_id": "m2", "target": "service_memory", "content": "Sync conflicts are logged to the sync_conflicts table with both versions of the conflicting record."},
            {"memory_id": "m3", "target": "task_state", "content": "The conflict resolution strategy was last discussed in the 2026-05-15 sprint planning."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Add a three-way merge strategy as an alternative to last-write-wins, selectable per collection."},
            {"unit_id": "u2", "text": "The three-way merge should use the server version as the common ancestor when available."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "service_memory", "unit_id": "u2"},
            ],
            "skip": [],
            "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "stale_memory"],
        "notes": "READ+STORE joint with stale. Reads m1 and m2 (current sync behavior). Skips m3 (stale sprint planning note — not current). Stores both u1 and u2 as service_memory — both define durable new sync behavior (three-way merge strategy and its algorithm). Two service_memory units in one case is valid when both describe durable component behaviors.",
    },
    {
        "case_id": "v05_batch50_0022",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "add data freshness SLA monitoring",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The pipeline currently measures end-to-end latency from source table commit to destination table availability."},
            {"memory_id": "m2", "target": "project_memory", "content": "The data-platform SLA guarantees that all tables are fresh within 4 hours of source commit."},
            {"memory_id": "m3", "target": "repo_memory", "content": "SLA dashboards are configured in grafana/dashboards/data_freshness.json."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Add a per-table freshness metric that alerts when any table exceeds the 4-hour SLA."},
            {"unit_id": "u2", "text": "The freshness alert should fire to the #data-alerts Slack channel with the table name and hours stale."},
            {"unit_id": "u3", "text": "Deploy the new metric to the staging Grafana instance first, then promote to production."},
        ],
        "gold": {
            "read": ["m1", "m2", "m3"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "service_memory", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ m1,m2,m3\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "project_vs_repo"],
        "notes": "READ+STORE joint with project-level SLA context. Reads all three (all relevant). Stores u1 and u2 as service_memory — durable monitoring behaviors. Stores u3 as task_state — deployment plan for current change. m2 is project_memory (SLA guarantee is project-level), correctly distinguished from service_memory behaviors.",
    },

    # ── Extended boundary / coverage cases (7) ──
    {
        "case_id": "v05_batch50_0023",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "metrics",
            "task": "add calibration metric",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The metrics module must report a calibration score comparing predicted vs gold target distributions across all five targets."},
            {"unit_id": "u2", "text": "Implement the calibration metric as a new function in src/v04/metrics.py alongside the existing F1 functions."},
            {"unit_id": "u3", "text": "The current metrics module only reports per-interface accuracy, not cross-target calibration."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "service_vs_task_state", "target_boundary"],
        "notes": "STORE/SKIP-only with service vs task boundary. u1 defines WHAT the module should report → service_memory (durable capability). u2 is HOW to implement → task_state. u3 describes current limitation → task_state (current implementation state, not a permanent design constraint). Unlike v05_sample_0021 where a limitation could be service_memory if it is a deliberate design invariant, here 'only reports per-interface accuracy' is a temporary state because calibration is being added.",
    },
    {
        "case_id": "v05_batch50_0024",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "export",
            "task": "record permanent project data policy",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The export service must never log or store raw invoice line items that contain customer PII."},
            {"unit_id": "u2", "text": "All data-platform services must use the centralized secret manager for API keys and credentials."},
            {"unit_id": "u3", "text": "Add PII masking to the export debug logs before the next production deployment."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "project_memory", "unit_id": "u1"},
                {"target": "project_memory", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE project_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "project_vs_repo", "target_boundary"],
        "notes": "STORE/SKIP-only with dual project_memory. u1 is a cross-service data safety rule → project_memory (applies across all services, not just export). u2 is a cross-service infrastructure rule → project_memory (centralized secret management is project policy, not service-specific). u3 is a current implementation task → task_state. Shows project_memory applies to rules that transcend any single service.",
    },
    {
        "case_id": "v05_batch50_0025",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "camera",
            "task": "record user preferences for the camera module",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "I prefer that the camera app always opens in photo mode, not video mode."},
            {"unit_id": "u2", "text": "For this repo, always run the camera integration tests with the --device emulator flag."},
            {"unit_id": "u3", "text": "My device unlock PIN for testing is 123456."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "user_profile", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ NONE\nSTORE user_profile u1\nSTORE repo_memory u2\nSKIP u3",
        },
        "tags": ["store_skip_only", "user_profile_boundary", "sensitive_boundary"],
        "notes": "STORE/SKIP-only with user_profile vs sensitive. u1 is a stable, non-sensitive, cross-session user preference → user_profile. u2 is repo-specific test command → repo_memory. u3 is a device PIN — sensitive credential, must SKIP. Shows user_profile vs sensitive boundary: preferences are fine, credentials are never stored.",
    },
    {
        "case_id": "v05_batch50_0026",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "training",
            "task": "decide training infrastructure",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "All v0.5 training runs must use the project-local Python virtual environment under .venv/ with pinned dependencies."},
            {"unit_id": "u2", "text": "Use the RTX 4070 SUPER GPU for training with batch size 4 to fit within 12GB VRAM."},
            {"unit_id": "u3", "text": "If training loss does not decrease within 50 steps, stop and investigate the data pipeline."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "repo_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE repo_memory u1\nSTORE task_state u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "project_vs_repo", "target_boundary"],
        "notes": "STORE/SKIP-only with project vs task boundary. u1 is a durable repo-level convention (venv + pinned deps) → repo_memory. u2 is a current hardware configuration decision for this training run → task_state (specific to current session, not a durable project rule). u3 is a conditional training procedure → task_state (operational checkpoint rule). Shows that hardware-specific choices are task_state, not project_memory.",
    },
    {
        "case_id": "v05_batch50_0027",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "update pipeline error handling",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The pipeline catches all exceptions at the stage level and writes error details to the pipeline_errors table."},
            {"memory_id": "m2", "target": "service_memory", "content": "The old v1 pipeline used a separate error queue that required manual draining."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Add a dead-letter queue for pipeline stages that fail after 3 retries. Failed records go to the DLQ for manual inspection."},
            {"unit_id": "u2", "text": "Remember to delete the old error queue after the DLQ is live for one week."},
            {"unit_id": "u3", "text": "My team's Slack webhook URL for pipeline alerts is https://hooks.slack.com/services/TEST/FAKE/abcdef."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ m1\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "sensitive_boundary", "stale_memory"],
        "notes": "READ+STORE joint with stale and sensitive. Reads m1 (current error handling). Skips m2 (stale legacy error queue — different architecture). Stores u1 (durable DLQ behavior → service_memory). Stores u2 (cleanup task → task_state, scheduled future action). Skips u3 (Slack webhook URL — sensitive credential, must SKIP). Shows webhook URLs are treated as sensitive like any other credential.",
    },
    {
        "case_id": "v05_batch50_0028",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "sync",
            "task": "update sync scheduling",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The sync module currently runs on a fixed 15-minute interval using Android WorkManager with a minimum battery constraint of 20%."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Sync scheduling parameters are configured in config/sync_schedule.xml with backoff and constraint policies."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Change the sync interval from fixed 15 minutes to adaptive: 5 minutes on Wi-Fi, 30 minutes on cellular."},
            {"unit_id": "u2", "text": "Add a network-type constraint to the WorkManager policy so it switches intervals automatically."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "service_memory", "unit_id": "u2"},
            ],
            "skip": [],
            "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "repo_vs_service"],
        "notes": "READ+STORE joint with dual service_memory. Reads both memories. u1 defines new adaptive scheduling behavior → service_memory. u2 defines network-type constraint mechanism → service_memory. Both are durable sync module behaviors. Note: u2 references WorkManager policy — this is about the sync service behavior, not a repo path, so service_memory is correct.",
    },
    {
        "case_id": "v05_batch50_0029",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "eval_runner",
            "task": "record evaluation priorities",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "For v0.5 evaluation, prioritize STORE target accuracy and false store rate over exact match rate."},
            {"unit_id": "u2", "text": "The project's evaluation standard emphasizes routing-specific metrics, not just output formatting."},
            {"unit_id": "u3", "text": "Write the evaluation priorities section in the training plan today."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "task_state", "unit_id": "u1"},
                {"target": "project_memory", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE task_state u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "project_vs_repo", "target_boundary"],
        "notes": "STORE/SKIP-only with project vs task boundary. u1 is a v0.5-specific evaluation priority → task_state (current run's emphasis). u2 states a durable project evaluation philosophy → project_memory (applies across all versions). u3 is immediate writing task → task_state. Fine boundary: u1 is the current specific directive, u2 is the enduring principle behind it. Shows that principles can be project_memory even when instantiated as task_state in a specific run.",
    },
    {
        "case_id": "v05_batch50_0030",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "add incremental load support",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The pipeline currently performs full-table refreshes for all dimension tables every night."},
            {"memory_id": "m2", "target": "service_memory", "content": "Full-table refreshes on the billing_facts table take approximately 45 minutes and lock the table for writes."},
            {"memory_id": "m3", "target": "task_state", "content": "The billing_facts table was last partitioned by month in the 2026-04 schema change."},
            {"memory_id": "m4", "target": "service_memory", "content": "The legacy v0 pipeline used a custom CDC connector that has since been deprecated."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Add incremental load support using a high-watermark column updated_at. The pipeline should only process rows where updated_at > last_load_time."},
            {"unit_id": "u2", "text": "The incremental load feature must support a full-refresh fallback when the high-watermark is detected as stale."},
            {"unit_id": "u3", "text": "The high-watermark values should be persisted in the pipeline_metadata table, not in memory."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "service_memory", "unit_id": "u2"},
                {"target": "repo_memory", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "repo_convention", "stale_memory", "related_but_useless"],
        "notes": "READ+STORE joint with stale and related-but-useless. Reads m1 and m2 (current pipeline behavior and performance). Skips m3 (stale task state — old partitioning change, not current). Skips m4 (stale legacy CDC reference — deprecated, different approach). Stores u1 and u2 as durable incremental load behaviors → service_memory. Stores u3 as repo data persistence convention → repo_memory (where state lives). Rich case with multiple stale detection decisions.",
    },
]


# ═══════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate batch50 cases and SFT messages.")
    parser.add_argument("--cases", default=str(ROOT / "data/v05/batches/v05_batch50_cases.jsonl"))
    parser.add_argument("--out", default=str(ROOT / "data/v05/batches/v05_batch50_sft_messages.jsonl"))
    parser.add_argument("--source", default="v05_batch50_dry_run")
    parser.add_argument("--new30-out", default=str(ROOT / "data/v05/batches/v05_batch50_new30_cases.jsonl"))
    args = parser.parse_args()

    cases_path = Path(args.cases)
    sft_path = Path(args.out)
    new30_path = Path(args.new30_out)
    source = args.source

    # 1. Load seed 20
    seed_path = ROOT / "data/v05/samples/v05_sample_cases.jsonl"
    seed_cases = []
    with seed_path.open() as f:
        for line in f:
            if line.strip():
                seed_cases.append(json.loads(line))
    print(f"Loaded {len(seed_cases)} seed cases from {seed_path}")

    # 2. Validate seed + new30
    from src.v04.case_validator import validate_case, validate_jsonl_file
    from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

    all_cases = seed_cases + NEW30_CASES

    # Quick dedup check
    case_ids = [c["case_id"] for c in all_cases]
    if len(case_ids) != len(set(case_ids)):
        dupes = [cid for cid, cnt in Counter(case_ids).items() if cnt > 1]
        print(f"ERROR: Duplicate case IDs: {dupes}")
        sys.exit(1)

    # Check new30 count
    if len(NEW30_CASES) != 30:
        print(f"ERROR: Expected 30 new cases, got {len(NEW30_CASES)}")
        sys.exit(1)

    # Leakage checks
    subset50_path = ROOT / "data/v04/model_predictions/p5_subset50_case_ids.txt"
    subset50_ids = set(subset50_path.read_text().strip().splitlines()) if subset50_path.exists() else set()

    fewshot_path = ROOT / "data/v04/model_predictions/qwen3_4b_unit_dsl_fewshot_examples.jsonl"
    fewshot_ids: set[str] = set()
    fewshot_texts: set[str] = set()
    if fewshot_path.exists():
        with fewshot_path.open() as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    fewshot_ids.add(obj["case_id"])
                    for u in obj.get("current_units", []):
                        fewshot_texts.add(u["text"])
                    for m in obj.get("candidate_memories", []):
                        fewshot_texts.add(m["content"])

    seed_texts: set[str] = set()
    for c in seed_cases:
        for u in c.get("current_units", []):
            seed_texts.add(u["text"])
        for m in c.get("candidate_memories", []):
            seed_texts.add(m["content"])

    new_ids = {c["case_id"] for c in NEW30_CASES}
    new_texts: set[str] = set()

    # 3. Validate every case
    all_ok = True
    errors: list[str] = []

    for case in all_cases:
        cid = case["case_id"]

        # Collect texts for new cases
        if cid in new_ids:
            for u in case.get("current_units", []):
                new_texts.add(u["text"])
            for m in case.get("candidate_memories", []):
                new_texts.add(m["content"])

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
            errors.append(f"{cid} READ mismatch: parsed={parsed_read} gold={gold_read}")
        if parsed_store != gold_store:
            all_ok = False
            errors.append(f"{cid} STORE mismatch")
        if parsed_skip != gold_skip:
            all_ok = False
            errors.append(f"{cid} SKIP mismatch: parsed={parsed_skip} gold={gold_skip}")

    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)

    # 4. Leakage checks
    overlap_ids = new_ids & subset50_ids
    if overlap_ids:
        print(f"LEAKAGE: new30 IDs in subset50: {overlap_ids}")
        all_ok = False

    overlap_fewshot_ids = new_ids & fewshot_ids
    if overlap_fewshot_ids:
        print(f"LEAKAGE: new30 IDs in few-shot: {overlap_fewshot_ids}")
        all_ok = False

    overlap_texts = new_texts & fewshot_texts
    if overlap_texts:
        print(f"LEAKAGE: new30 texts match few-shot texts: {len(overlap_texts)} matches")
        all_ok = False

    overlap_seed_texts = new_texts & seed_texts
    if overlap_seed_texts:
        print(f"LEAKAGE: new30 texts match seed20 texts: {len(overlap_seed_texts)} matches")
        all_ok = False

    # Also check against subset50 case texts
    subset50_cases_path = ROOT / "data/v04/model_predictions/p5_subset50_cases.jsonl"
    if subset50_cases_path.exists():
        subset50_texts: set[str] = set()
        with subset50_cases_path.open() as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    for u in obj.get("current_units", []):
                        subset50_texts.add(u["text"])
                    for m in obj.get("candidate_memories", []):
                        subset50_texts.add(m["content"])
        overlap_subset_texts = new_texts & subset50_texts
        if overlap_subset_texts:
            print(f"LEAKAGE: new30 texts match subset50 texts: {len(overlap_subset_texts)} matches")
            all_ok = False

    if not all_ok:
        sys.exit(1)

    print("All case validations PASSED. No leakage detected.")

    # 5. Write cases
    cases_path.parent.mkdir(parents=True, exist_ok=True)

    with cases_path.open("w", encoding="utf-8") as f:
        for case in all_cases:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"Wrote {len(all_cases)} cases to {cases_path}")

    with new30_path.open("w", encoding="utf-8") as f:
        for case in NEW30_CASES:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"Wrote {len(NEW30_CASES)} new30 cases to {new30_path}")

    # 6. Build and write SFT messages
    messages = []
    for case in all_cases:
        msg = {
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
                "gold_shape": (
                    "READ + STORE joint" if case["gold"]["read"] and case["gold"]["store"]
                    else "READ-only" if case["gold"]["read"]
                    else "STORE/SKIP-only"
                ),
                "store_targets": [s["target"] for s in case["gold"]["store"]],
                "is_final_train_data": False,
            },
        }
        messages.append(msg)

    with sft_path.open("w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(messages)} SFT messages to {sft_path}")

    # 7. SFT validation
    sft_ok = True
    for case, msg in zip(all_cases, messages):
        assistant = msg["messages"][2]["content"]
        if assistant != case["gold"]["dsl"]:
            print(f"SFT MISMATCH: {case['case_id']}")
            sft_ok = False
        if "```" in assistant:
            print(f"SFT MARKDOWN: {case['case_id']}")
            sft_ok = False
        if assistant.strip().startswith("{"):
            print(f"SFT JSON: {case['case_id']}")
            sft_ok = False
        if msg["metadata"]["is_final_train_data"]:
            print(f"SFT IS_FINAL: {case['case_id']}")
            sft_ok = False

    if sft_ok:
        print("All SFT messages validated OK")
    else:
        print("SFT validation had errors")
        sys.exit(1)

    # 8. Summary stats
    print("\n=== BATCH50 SUMMARY ===")
    print(f"Total cases: {len(all_cases)}")
    print(f"  Seed20: {len(seed_cases)}")
    print(f"  New30: {len(NEW30_CASES)}")

    shapes = Counter()
    for c in all_cases:
        has_read = bool(c["gold"]["read"])
        has_store = bool(c["gold"]["store"])
        if has_read and has_store:
            shapes["READ + STORE joint"] += 1
        elif has_read:
            shapes["READ-only"] += 1
        else:
            shapes["STORE/SKIP-only"] += 1
    print(f"Shape distribution: {dict(shapes)}")

    all_tags = [t for c in all_cases for t in c["tags"]]
    tag_counts = Counter(all_tags)
    print(f"Tag distribution (top 15): {dict(tag_counts.most_common(15))}")

    all_targets = [s["target"] for c in all_cases for s in c["gold"]["store"]]
    target_counts = Counter(all_targets)
    print(f"STORE target counts: {dict(target_counts)}")

    total_store = sum(len(c["gold"]["store"]) for c in all_cases)
    total_skip = sum(len(c["gold"]["skip"]) for c in all_cases)
    print(f"Total STORE units: {total_store}")
    print(f"Total SKIP units: {total_skip}")

    # Coverage checks for new30
    print("\n=== NEW30 COVERAGE CHECKS ===")
    new_tags = [t for c in NEW30_CASES for t in c["tags"]]
    new_tag_counts = Counter(new_tags)
    new_targets = [s["target"] for c in NEW30_CASES for s in c["gold"]["store"]]
    new_target_counts = Counter(new_targets)

    checks = {
        "READ-only >= 5": shapes.get("READ-only", 0) >= 5,
        "STORE/SKIP-only >= 7": shapes.get("STORE/SKIP-only", 0) >= 7,
        "READ+STORE joint >= 8": shapes.get("READ + STORE joint", 0) >= 8,
        "stale/related >= 5": new_tag_counts.get("stale_memory", 0) + new_tag_counts.get("related_but_useless", 0) >= 5,
        "target_boundary >= 8": new_tag_counts.get("target_boundary", 0) >= 8,
        "sensitive_boundary >= 5": new_tag_counts.get("sensitive_boundary", 0) >= 5,
        "project_vs_task >= 4": new_tag_counts.get("project_vs_repo", 0) >= 4,
        "service_vs_task >= 4": new_tag_counts.get("service_vs_task_state", 0) >= 4,
        "repo_vs_service >= 4": new_tag_counts.get("repo_vs_service", 0) >= 4,
        "user_profile_boundary >= 3": new_tag_counts.get("user_profile_boundary", 0) >= 3,
        "repo_convention >= 5": new_tag_counts.get("repo_convention", 0) >= 5,
        "service_invariant >= 6": new_tag_counts.get("service_invariant", 0) >= 6,
        "task_progress >= 5": new_tag_counts.get("task_progress", 0) >= 5,
        "temporary_request >= 4": new_tag_counts.get("temporary_request", 0) >= 4,
        "project_memory >= 8 (total)": target_counts.get("project_memory", 0) >= 8,
        "user_profile >= 4 (total)": target_counts.get("user_profile", 0) >= 4,
    }
    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {check}: {status}")
        if not passed:
            all_ok = False

    print(f"\nFinal validation: {'ALL PASSED' if all_ok else 'SOME FAILURES'}")


if __name__ == "__main__":
    main()
