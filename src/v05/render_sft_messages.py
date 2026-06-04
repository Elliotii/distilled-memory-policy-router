"""Generate 20 v0.5 sample cases and SFT messages for dry run validation.

Scope: sample data only. Not final train/dev/gold. Not locked.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

# Ensure src is importable
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


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
    context_lines = [
        "RUNTIME_CONTEXT",
        f"project: {rc['project']}",
        f"repo: {rc['repo']}",
        f"service: {rc['service']}",
        f"task: {rc['task']}",
    ]

    mems = case["candidate_memories"]
    if mems:
        mem_lines = ["CANDIDATE_MEMORIES"]
        for m in mems:
            mem_lines.append(f"{m['memory_id']} [{m['target']}]: {m.get('text', m.get('content', ''))}")
    else:
        mem_lines = ["CANDIDATE_MEMORIES", "NONE"]

    units = case["current_units"]
    unit_lines = ["CURRENT_UNITS"]
    for u in units:
        unit_lines.append(f"{u['unit_id']}: {u['text']}")

    return "\n".join(context_lines + [""] + mem_lines + [""] + unit_lines)


def build_sft_message(case: dict[str, Any]) -> dict[str, Any]:
    dsl = case["gold"]["dsl"]
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
            {"role": "assistant", "content": dsl},
        ],
        "case_id": case["case_id"],
        "source": "v05_sample_dry_run",
        "metadata": {
            "tags": case["tags"],
            "num_candidate_memories": len(case["candidate_memories"]),
            "num_current_units": len(case["current_units"]),
            "gold_shape": shape,
            "store_targets": [s["target"] for s in gold_store],
            "is_final_train_data": False,
        },
    }


# ── 20 SAMPLE CASES ──────────────────────────────────────────────

SAMPLE_CASES: list[dict[str, Any]] = [
    # ── READ-only cases (3) ──
    {
        "case_id": "v05_sample_0001",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "parser",
            "task": "verify parser rejects unknown STORE targets",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The parser rejects unknown STORE targets and does not do semantic repair."},
            {"memory_id": "m2", "target": "project_memory", "content": "The v0.4 pilot evaluates Unit DSL before v0.5 training."},
            {"memory_id": "m3", "target": "service_memory", "content": "The old v0.3 validator checked exact write_spans substrings only."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The parser should refuse to accept fact as a valid STORE target."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ m1\nSTORE NONE\nSKIP u1",
        },
        "tags": ["read_only", "service_invariant", "temporary_request"],
        "notes": "READ-only: parser unit is a temporary verification request, not new durable information. Relevant memory m1 is read for context. m2 is project-level but not directly relevant. m3 is stale v0.3 reference.",
    },
    {
        "case_id": "v05_sample_0002",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "sync",
            "task": "understand sync retry behavior",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The sync module retries failed uploads in batches of 10 with exponential backoff."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Sync-related integration tests live under tests/integration/sync/."},
            {"memory_id": "m3", "target": "service_memory", "content": "The old v0.2 sync used polling instead of push notifications."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Does the current sync retry respect the upload timeout setting, or does it use a hardcoded 30s?"},
        ],
        "gold": {
            "read": ["m1"],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ m1\nSTORE NONE\nSKIP u1",
        },
        "tags": ["read_only", "stale_memory", "temporary_request"],
        "notes": "READ-only with stale memory: m1 is relevant for understanding retry behavior. m2 is repo path, not needed for this question. m3 is stale old-sync reference. u1 is a one-off question.",
    },
    {
        "case_id": "v05_sample_0003",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "export",
            "task": "check export job configuration",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The export job writes invoices to S3 daily at 02:00 UTC and uses the credentials from IAM role export-writer."},
            {"memory_id": "m2", "target": "service_memory", "content": "The billing report generator is a separate service that reads exported invoices."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Please check today's weather before running the export validation."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ m1\nSTORE NONE\nSKIP u1",
        },
        "tags": ["read_only", "related_but_useless"],
        "notes": "READ-only with related-but-useless: m1 is needed for export context. m2 is related (billing) but not directly useful for export validation. u1 is completely unrelated (weather).",
    },

    # ── STORE/SKIP-only cases (5) ──
    {
        "case_id": "v05_sample_0004",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "eval_runner",
            "task": "record eval_runner capabilities",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The eval_runner computes READ F1, STORE unit F1, STORE target accuracy, SKIP F1, false store rate, and irrelevant read rate."},
            {"unit_id": "u2", "text": "The eval_runner has been run on subset50 but not yet on full pilot."},
            {"unit_id": "u3", "text": "Maybe the eval_runner should also report confidence scores."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSKIP u3",
        },
        "tags": ["store_skip_only", "service_invariant", "task_progress", "service_vs_task_state"],
        "notes": "STORE/SKIP-only: u1 is durable service behavior (service_memory). u2 is current task progress (task_state). u3 is unresolved speculation — SKIP (not a project decision yet). Shows service_memory vs task_state distinction.",
    },
    {
        "case_id": "v05_sample_0005",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "parser",
            "task": "record parser memory",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "Parser tests should live under tests/v04/ and run with pytest tests/v04/."},
            {"unit_id": "u2", "text": "The parser converts Unit DSL to canonical JSON without guessing targets."},
            {"unit_id": "u3", "text": "Remember my personal backup email: abc16-backup@example.com."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "repo_memory", "unit_id": "u1"},
                {"target": "service_memory", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ NONE\nSTORE repo_memory u1\nSTORE service_memory u2\nSKIP u3",
        },
        "tags": ["store_skip_only", "repo_vs_service", "sensitive_boundary"],
        "notes": "STORE/SKIP-only with sensitive SKIP: u1 is repo path/convention (repo_memory). u2 is durable service behavior (service_memory). u3 is personal email — must SKIP. Shows repo_memory vs service_memory distinction.",
    },
    {
        "case_id": "v05_sample_0006",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "record pipeline scope decision",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The data-platform pilot uses synthetic service scenarios only; no real production data."},
            {"unit_id": "u2", "text": "Next, add a retry wrapper for the pipeline job that fails on transient network errors."},
            {"unit_id": "u3", "text": "Today's lunch order will be from the Thai place."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "project_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ NONE\nSTORE project_memory u1\nSTORE task_state u2\nSKIP u3",
        },
        "tags": ["store_skip_only", "project_vs_repo", "target_boundary"],
        "notes": "STORE/SKIP-only with project_memory vs task_state: u1 is a project-level scope decision (uses synthetic data) → project_memory. Assumes synthetic-data-only is a permanent project safety/scope decision, not a temporary pilot constraint. u2 is current task progress (next action) → task_state. u3 is irrelevant chatter. Shows project_memory vs task_state boundary.",
    },
    {
        "case_id": "v05_sample_0007",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "camera",
            "task": "record user preference",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "I prefer architecture explanations that name tradeoffs explicitly."},
            {"unit_id": "u2", "text": "Enable HDR mode by default for all future camera captures in this app."},
            {"unit_id": "u3", "text": "My phone number is 555-0198, use it for the test account."},
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
        "notes": "STORE/SKIP-only with user_profile and sensitive: u1 is stable cross-project user preference → user_profile. u2 is app-specific setting → repo_memory (app code change). u3 is phone number → must SKIP. Shows user_profile vs sensitive boundary.",
    },
    {
        "case_id": "v05_sample_0008",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "case_validator",
            "task": "record case validation rules",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "The case validator checks that gold.dsl parses consistently with gold.read, gold.store, and gold.skip fields."},
            {"unit_id": "u2", "text": "The case validator source lives under src/v04/case_validator.py."},
            {"unit_id": "u3", "text": "Add a sixth target called team_memory for team-level conventions."},
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
        "tags": ["store_skip_only", "repo_vs_service", "sop_skill_out_of_scope"],
        "notes": "STORE/SKIP-only: u1 is durable service behavior (service_memory). u2 is repo path (repo_memory). u3 proposes a new target (team_memory) which is out of scope for v0.4/v0.5 — SKIP as unresolved scope change. Shows repo_memory vs service_memory.",
    },

    # ── READ + STORE joint cases (5) ──
    {
        "case_id": "v05_sample_0009",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "eval_runner",
            "task": "extend eval_runner with new metric",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The eval_runner groups predictions by interface and system, then scores each group independently."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Eval runner code lives under src/v04/eval_runner.py and reports go to reports/v04/."},
            {"memory_id": "m3", "target": "project_memory", "content": "The v0.4 pilot compares three raw-output interfaces before training."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The eval_runner must now also report per-tag accuracy breakdowns in addition to aggregate metrics."},
            {"unit_id": "u2", "text": "The eval_runner still evaluates only single-turn cases, not multi-turn sessions."},
            {"unit_id": "u3", "text": "Add the per-tag report section to reports/v04/interface_pilot_report.md template."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
                {"target": "repo_memory", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "repo_convention", "service_vs_task_state"],
        "notes": "READ+STORE joint: reads m1 (eval_runner behavior) and m2 (repo path) for context, skips m3 (project-level, not directly relevant). Stores u1 (new eval_runner capability → service_memory — durable behavior). u2 describes a current implementation limitation (evaluates only single-turn, not multi-turn) → task_state — this is current implementation state, not a permanent design invariant. u3 is repo path convention (repo_memory). No units to SKIP.",
    },
    {
        "case_id": "v05_sample_0010",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "sync",
            "task": "update sync error handling",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The sync module queues offline edits and retries them in creation order with exponential backoff."},
            {"memory_id": "m2", "target": "task_state", "content": "The previous sync change was deployed last week and passed integration tests."},
            {"memory_id": "m3", "target": "service_memory", "content": "The old v0.2 notification service used polling instead of push."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Sync error handling should be updated to retry on 429 rate-limit responses with a 60s delay."},
            {"unit_id": "u2", "text": "Run the sync integration tests after the change and report results."},
            {"unit_id": "u3", "text": "My test account password is testpass_1234_do_not_store."},
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
        "notes": "READ+STORE joint with sensitive+stale: reads m1 (sync behavior). Skips m2 (stale task state from last week, no longer current). Skips m3 (stale old service reference). Stores u1 (durable service behavior → service_memory), u2 (current task next step → task_state). Skips u3 (password → sensitive). Shows task_state vs stale memory: m2 is old task state, not current.",
    },
    {
        "case_id": "v05_sample_0011",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "prompt_builder",
            "task": "document prompt builder behavior",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The prompt builder renders current units with stable unit IDs and targets for the model."},
            {"memory_id": "m2", "target": "project_memory", "content": "The v0.4 interface pilot does not implement LLM unitization."},
            {"memory_id": "m3", "target": "repo_memory", "content": "Prompt templates live under prompts/v04/ and use {runtime_context} as placeholder."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The prompt builder must always include the five legal STORE targets in the system instruction."},
            {"unit_id": "u2", "text": "Add a few-shot example section to the prompt builder output format."},
            {"unit_id": "u3", "text": "I like concise prompts with examples before rules when learning new APIs."},
        ],
        "gold": {
            "read": ["m1", "m2", "m3"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
                {"target": "user_profile", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ m1,m2,m3\nSTORE service_memory u1\nSTORE task_state u2\nSTORE user_profile u3\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "user_profile_boundary"],
        "notes": "READ+STORE joint: reads all three memories (all relevant). Stores u1 (durable prompt builder behavior → service_memory), u2 (current task → task_state), u3 (user preference for learning style → user_profile, non-sensitive, cross-project). Shows user_profile is stable preference, not sensitive.",
    },
    {
        "case_id": "v05_sample_0012",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "export",
            "task": "add export validation step",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The export job writes invoices to S3 daily at 02:00 UTC using IAM role export-writer."},
            {"memory_id": "m2", "target": "service_memory", "content": "The export job currently does NOT validate file integrity after writing."},
            {"memory_id": "m3", "target": "repo_memory", "content": "Export job configuration lives in config/export.yaml with schema version 2."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Add a SHA-256 checksum validation step that runs after the S3 write and logs the result."},
            {"unit_id": "u2", "text": "The export job is blocked until the IAM role is updated with the new S3 permissions."},
        ],
        "gold": {
            "read": ["m1", "m2", "m3"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
            ],
            "skip": [],
            "dsl": "READ m1,m2,m3\nSTORE service_memory u1\nSTORE task_state u2\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "service_vs_task_state"],
        "notes": "READ+STORE joint: reads all memories for context. Stores u1 (new durable export behavior → service_memory), u2 (current blocker → task_state). Shows service_memory (durable service behavior change) vs task_state (temporary blocker).",
    },
    {
        "case_id": "v05_sample_0013",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "parser",
            "task": "add parser feature",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The parser rejects duplicate STORE assignments and missing unit assignments."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Parser tests live under tests/v04/test_parser.py and use pytest."},
            {"memory_id": "m3", "target": "project_memory", "content": "v0.4 is an interface pilot before v0.5 LoRA/SFT training."},
            {"memory_id": "m4", "target": "service_memory", "content": "The old v0.3 validator accepted JSON with read_hints and write_spans only."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The parser should now also reject STORE lines where the target is valid but the unit_id has already been assigned to SKIP in the same output."},
            {"unit_id": "u2", "text": "Write parser tests for the new duplicate assignment across STORE/SKIP check."},
            {"unit_id": "u3", "text": "This parser change is small and should take about 30 minutes."},
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
        "tags": ["read_store_joint", "service_invariant", "task_progress", "related_but_useless", "stale_memory"],
        "notes": "READ+STORE joint with related_but_useless and stale: reads m1 (parser behavior) and m2 (test location). Skips m3 (project-level, not needed for this parser change). Skips m4 (stale v0.3 reference). Stores u1 (durable parser constraint → service_memory), u2 (current task next step → task_state). Skips u3 (time estimate, temporary). Shows selective reading of related memories.",
    },

    # ── Additional boundary / coverage cases (7) ──
    # v05_sample_0014 REMOVED per human review Decision 1: too ambiguous for training.
    # Replaced by v05_sample_0021 below.
    {
        "case_id": "v05_sample_0021",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "notification",
            "task": "add push notification retry logic",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The notification service delivers push notifications via Firebase Cloud Messaging with a 30-second delivery timeout."},
            {"memory_id": "m2", "target": "repo_memory", "content": "Notification service configuration lives in config/notification.yaml with environment-specific FCM credentials."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The notification service must deduplicate messages by notification_id within a 5-minute window to prevent double-delivery."},
            {"unit_id": "u2", "text": "Integrate the notification retry into the existing sync retry wrapper that already handles 429 responses."},
            {"unit_id": "u3", "text": "Write the FCM credential setup guide in docs/notification/fcm_setup.md."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "task_state", "unit_id": "u2"},
                {"target": "repo_memory", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE",
        },
        "tags": ["read_store_joint", "service_invariant", "task_progress", "repo_convention", "service_vs_task_state"],
        "notes": "Clean service_memory vs task_state boundary. u1 defines durable deduplication behavior for the notification service — this is a component behavior constraint that persists beyond the current task (service_memory). u2 describes the current implementation plan: integrating notification retry into the existing sync wrapper — this is a current next step (task_state). u3 is repo documentation convention (repo_memory). Key distinction: u1 is about WHAT the service does (durable interface behavior), u2 is about HOW to implement it now (current progress). No ambiguous wording; no 'currently should' phrasing.",
    },
    {
        "case_id": "v05_sample_0015",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "documentation",
            "task": "decide v0.5 documentation structure",
        },
        "candidate_memories": [],
        "current_units": [
            {"unit_id": "u1", "text": "v0.5 training documentation should go under docs/v05/ with training plan, data plan, and SFT format."},
            {"unit_id": "u2", "text": "The project does not implement a full MemoryOS; it only studies the memory policy router layer."},
            {"unit_id": "u3", "text": "Write the v0.5 training plan as a markdown file today."},
        ],
        "gold": {
            "read": [],
            "store": [
                {"target": "repo_memory", "unit_id": "u1"},
                {"target": "project_memory", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ NONE\nSTORE repo_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["store_skip_only", "project_vs_repo", "target_boundary"],
        "notes": "STORE/SKIP-only with project_vs_repo boundary: u1 is repo path convention → repo_memory. u2 is project-level scope decision (not MemoryOS) → project_memory. u3 is immediate task → task_state. Shows all three targets used correctly in one case. project_memory is a durable scope decision, not a catch-all.",
    },
    {
        "case_id": "v05_sample_0016",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "camera",
            "task": "configure camera defaults",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "repo_memory", "content": "Camera default preferences are stored in config/camera_defaults.yaml and must be JSON-serializable."},
            {"memory_id": "m2", "target": "user_profile", "content": "The user prefers low-light enhancement enabled for all photo captures."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Set the default flash mode to auto for the camera module in this app."},
            {"unit_id": "u2", "text": "The user has informed us that their recovery code for the field-app account is ABCD-1234-EFGH."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [
                {"target": "repo_memory", "unit_id": "u1"},
            ],
            "skip": ["u2"],
            "dsl": "READ m1\nSTORE repo_memory u1\nSKIP u2",
        },
        "tags": ["read_store_joint", "repo_convention", "sensitive_boundary", "related_but_useless"],
        "notes": "READ+STORE joint with sensitive and related-but-useless: reads m1 (camera config format) but NOT m2 (user preference — related but this is about a different camera setting, not low-light). Stores u1 (app-specific camera setting → repo_memory). Skips u2 (recovery code → sensitive, must SKIP). Shows related_but_useless: m2 is about the user but for a different camera feature.",
    },
    {
        "case_id": "v05_sample_0017",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "pipeline",
            "task": "review pipeline monitoring",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The pipeline publishes job completion events to the monitoring queue."},
            {"memory_id": "m2", "target": "service_memory", "content": "The old v1 pipeline wrote logs to a flat file instead of structured events."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The pipeline should also publish failure events with stack traces to the monitoring queue."},
            {"unit_id": "u2", "text": "The monitoring queue message schema is defined in docs/pipeline/monitoring_schema.md."},
            {"unit_id": "u3", "text": "Add a Slack alert for pipeline failures that happen during off-hours."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u2"},
                {"target": "task_state", "unit_id": "u3"},
            ],
            "skip": [],
            "dsl": "READ m1\nSTORE service_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE",
        },
        "tags": ["read_store_joint", "stale_memory", "service_memory", "repo_memory", "task_state"],
        "notes": "READ+STORE joint with stale memory: reads m1 (current pipeline behavior). Skips m2 (stale old-pipeline reference). Stores u1 (durable pipeline behavior → service_memory), u2 (repo documentation path → repo_memory), u3 (current task action → task_state). All three STORE targets in one case.",
    },
    {
        "case_id": "v05_sample_0018",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "training",
            "task": "plan v0.5 training approach",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "project_memory", "content": "The v0.4 interface pilot confirmed Unit DSL as the primary training interface for v0.5."},
            {"memory_id": "m2", "target": "project_memory", "content": "The project does not train a retriever or writer; it only trains the memory policy router."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Use LoRA with rank 8 on Qwen3-4B for the v0.5 SFT training run."},
            {"unit_id": "u2", "text": "Training should optimize for routing metrics, not just cross-entropy loss."},
            {"unit_id": "u3", "text": "Start training tomorrow morning once the data is ready."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "task_state", "unit_id": "u1"},
                {"target": "project_memory", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ m1,m2\nSTORE task_state u1\nSTORE project_memory u2\nSKIP u3",
        },
        "tags": ["read_store_joint", "project_vs_repo", "target_boundary"],
        "notes": "READ+STORE joint with project_memory vs task_state: reads both project memories. Stores u1 (current training plan → task_state — this is a current decision/plan, not a project-level scope decision). Stores u2 (training evaluation philosophy → project_memory — this is a durable project-level design principle). Skips u3 (time estimate, temporary). Shows fine project_memory vs task_state boundary: u1 is plan (task), u2 is principle (project).",
    },
    {
        "case_id": "v05_sample_0019",
        "runtime_context": {
            "project": "mobile-field",
            "repo": "field-app",
            "service": "sync",
            "task": "add offline queue purge feature",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The sync offline queue stores pending edits in SQLite with a maximum of 5000 entries."},
            {"memory_id": "m2", "target": "service_memory", "content": "The sync module retries failed uploads with exponential backoff: 1s, 2s, 4s, 8s, then gives up."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "Add a manual purge button that clears all pending offline edits older than 7 days."},
            {"unit_id": "u2", "text": "The user has requested that we store their location history for personalized recommendations."},
            {"unit_id": "u3", "text": "The purge feature should log how many entries were removed and their total size."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "service_memory", "unit_id": "u3"},
            ],
            "skip": ["u2"],
            "dsl": "READ m1\nSTORE service_memory u1\nSTORE service_memory u3\nSKIP u2",
        },
        "tags": ["read_store_joint", "service_invariant", "sensitive_boundary", "related_but_useless"],
        "notes": "READ+STORE joint with sensitive boundary: reads m1 (queue limits). Skips m2 (retry behavior — related to sync but not to purge feature). Stores u1 (new sync behavior → service_memory), u3 (logging behavior → service_memory). Skips u2 (location history — sensitive/privacy concern, must SKIP even though user requested it). Shows sensitive content is SKIP regardless of user request.",
    },
    {
        "case_id": "v05_sample_0020",
        "runtime_context": {
            "project": "data-platform",
            "repo": "data-jobs",
            "service": "export",
            "task": "implement export retry logic",
        },
        "candidate_memories": [
            {"memory_id": "m1", "target": "service_memory", "content": "The export job writes invoices to S3 daily and expects exactly-once delivery semantics."},
            {"memory_id": "m2", "target": "project_memory", "content": "The data-platform pilot scope is limited to synthetic service scenarios only."},
            {"memory_id": "m3", "target": "service_memory", "content": "The legacy v1 invoice generator ran on-premise and used FTP for delivery."},
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The export retry logic must use idempotency keys to prevent duplicate invoice uploads when S3 writes are retried."},
            {"unit_id": "u2", "text": "Store the idempotency key schema in docs/export/idempotency.md."},
            {"unit_id": "u3", "text": "My company laptop runs Ubuntu 24.04 and I use it for all development work."},
        ],
        "gold": {
            "read": ["m1", "m2"],
            "store": [
                {"target": "service_memory", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u2"},
            ],
            "skip": ["u3"],
            "dsl": "READ m1,m2\nSTORE service_memory u1\nSTORE repo_memory u2\nSKIP u3",
        },
        "tags": ["read_store_joint", "service_invariant", "repo_convention", "stale_memory", "target_boundary"],
        "notes": "READ+STORE joint with stale memory and target_boundary: reads m1 (export behavior) and m2 (project scope). Skips m3 (stale legacy reference, on-premise FTP no longer relevant). Stores u1 (durable export behavior → service_memory with idempotency design). Stores u2 (repo documentation path → repo_memory). Skips u3 (personal laptop info — not harmful but not worth storing, temporary context). Shows repo_memory (where docs go) vs service_memory (what the service does) boundary.",
    },
]


def validate_everything() -> int:
    from src.v04.case_validator import validate_case, validate_jsonl_file
    from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS

    # Load existing IDs to check leakage
    subset50_path = ROOT / "data/v04/model_predictions/p5_subset50_case_ids.txt"
    subset50_ids = set(subset50_path.read_text().strip().splitlines()) if subset50_path.exists() else set()

    fewshot_path = ROOT / "data/v04/model_predictions/qwen3_4b_unit_dsl_fewshot_examples.jsonl"
    fewshot_ids: set[str] = set()
    if fewshot_path.exists():
        with fewshot_path.open() as f:
            for line in f:
                if line.strip():
                    fewshot_ids.add(json.loads(line)["case_id"])

    # 1. Validate individual cases
    all_ok = True
    for case in SAMPLE_CASES:
        result = validate_case(case)
        if not result["valid"]:
            print(f"VALIDATION FAILED: {case['case_id']}")
            for e in result["errors"]:
                print(f"  {e}")
            all_ok = False

        # Check DSL parse
        dsl = case["gold"]["dsl"]
        mem_ids = [m["memory_id"] for m in case["candidate_memories"]]
        unit_ids = [u["unit_id"] for u in case["current_units"]]
        parsed = parse_policy_dsl(dsl, mem_ids, unit_ids, LEGAL_TARGETS)
        if not parsed["validation"]["valid"]:
            print(f"DSL PARSE FAILED: {case['case_id']}")
            for e in parsed["validation"]["errors"]:
                print(f"  {e}")
            all_ok = False

        # Check canonical consistency
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
            print(f"STORE MISMATCH: {case['case_id']}")
            all_ok = False
        if parsed_skip != gold_skip:
            print(f"SKIP MISMATCH: {case['case_id']}")
            all_ok = False

    # 2. Leakage checks
    sample_ids = {c["case_id"] for c in SAMPLE_CASES}
    overlap_subset = sample_ids & subset50_ids
    overlap_fewshot = sample_ids & fewshot_ids
    if overlap_subset:
        print(f"LEAKAGE: sample IDs in subset50: {overlap_subset}")
        all_ok = False
    if overlap_fewshot:
        print(f"LEAKAGE: sample IDs in few-shot examples: {overlap_fewshot}")
        all_ok = False

    # 3. Coverage checks
    total_read_only = sum(1 for c in SAMPLE_CASES if c["gold"]["read"] and not c["gold"]["store"])
    total_store_only = sum(1 for c in SAMPLE_CASES if not c["gold"]["read"] and c["gold"]["store"])
    total_joint = sum(1 for c in SAMPLE_CASES if c["gold"]["read"] and c["gold"]["store"])
    all_tags = [t for c in SAMPLE_CASES for t in c["tags"]]
    from collections import Counter
    tag_counts = Counter(all_tags)

    all_targets = [s["target"] for c in SAMPLE_CASES for s in c["gold"]["store"]]
    target_counts = Counter(all_targets)

    total_store_units = sum(len(c["gold"]["store"]) for c in SAMPLE_CASES)
    total_skip_units = sum(len(c["gold"]["skip"]) for c in SAMPLE_CASES)

    print(f"\n=== SAMPLE DATA SUMMARY ===")
    print(f"Total cases: {len(SAMPLE_CASES)}")
    print(f"READ-only: {total_read_only}")
    print(f"STORE/SKIP-only: {total_store_only}")
    print(f"READ+STORE joint: {total_joint}")
    print(f"Tags: {dict(tag_counts.most_common())}")
    print(f"STORE targets: {dict(target_counts)}")
    print(f"Total STORE units: {total_store_units}")
    print(f"Total SKIP units: {total_skip_units}")
    print(f"Subset50 overlap: {overlap_subset or 'none'}")
    print(f"Few-shot overlap: {overlap_fewshot or 'none'}")

    # Coverage requirements check
    checks = {
        "READ-only >= 3": total_read_only >= 3,
        "STORE/SKIP-only >= 4": total_store_only >= 4,
        "READ+STORE joint >= 5": total_joint >= 5,
        "stale/related >= 3": tag_counts.get("stale_memory", 0) + tag_counts.get("related_but_useless", 0) >= 3,
        "target_boundary >= 4": tag_counts.get("target_boundary", 0) >= 4,
        "sensitive_boundary >= 3": tag_counts.get("sensitive_boundary", 0) >= 3,
        "repo_memory >= 4": target_counts.get("repo_memory", 0) >= 4,
        "service_memory >= 5": target_counts.get("service_memory", 0) >= 5,
        "task_state >= 5": target_counts.get("task_state", 0) >= 5,
        "project_memory >= 3": target_counts.get("project_memory", 0) >= 3,
        "user_profile >= 2": target_counts.get("user_profile", 0) >= 2,
    }
    print(f"\n=== COVERAGE CHECKS ===")
    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {check}: {status}")
        if not passed:
            all_ok = False

    return 0 if all_ok else 1


def write_outputs() -> None:
    cases_path = ROOT / "data/v05/samples/v05_sample_cases.jsonl"
    sft_path = ROOT / "data/v05/samples/v05_sample_sft_messages.jsonl"

    # Write cases
    with cases_path.open("w", encoding="utf-8") as f:
        for case in SAMPLE_CASES:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"Wrote {len(SAMPLE_CASES)} cases to {cases_path}")

    # Build and write SFT messages
    messages = [build_sft_message(c) for c in SAMPLE_CASES]
    with sft_path.open("w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(messages)} SFT messages to {sft_path}")

    # Validate SFT messages
    all_ok = True
    for i, (case, msg) in enumerate(zip(SAMPLE_CASES, messages)):
        assistant = msg["messages"][2]["content"]
        if assistant != case["gold"]["dsl"]:
            print(f"SFT ASSISTANT MISMATCH: {case['case_id']}")
            all_ok = False
        # No markdown fence in assistant
        if "```" in assistant:
            print(f"SFT MARKDOWN DETECTED: {case['case_id']}")
            all_ok = False
        # No JSON in assistant
        if assistant.strip().startswith("{"):
            print(f"SFT JSON DETECTED: {case['case_id']}")
            all_ok = False
        if msg["metadata"]["is_final_train_data"]:
            print(f"SFT IS_FINAL_TRAIN_DATA unexpected: {case['case_id']}")
            all_ok = False

    if all_ok:
        print("All SFT messages validated OK")
    else:
        print("SFT message validation had errors")


def render_sft_from_cases(cases_path: str, out_path: str, source: str) -> None:
    """Read cases from JSONL, build SFT messages, write to out path."""
    with open(cases_path, encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]
    print(f"Loaded {len(cases)} cases from {cases_path}")

    messages = []
    for case in cases:
        msg = build_sft_message(case)
        msg["source"] = source
        msg["metadata"]["is_final_train_data"] = False
        messages.append(msg)

    with open(out_path, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"Wrote {len(messages)} SFT messages to {out_path}")

    # Validate SFT messages
    all_ok = True
    for c, m in zip(cases, messages):
        assistant = m["messages"][2]["content"]
        if assistant != c["gold"]["dsl"]:
            print(f"SFT ASSISTANT MISMATCH: {c['case_id']}")
            all_ok = False
        if "```" in assistant:
            print(f"SFT MARKDOWN DETECTED: {c['case_id']}")
            all_ok = False
        if assistant.strip().startswith("{"):
            print(f"SFT JSON DETECTED: {c['case_id']}")
            all_ok = False
        if m["metadata"]["is_final_train_data"]:
            print(f"SFT IS_FINAL_TRAIN_DATA unexpected: {c['case_id']}")
            all_ok = False
    if all_ok:
        print("All SFT messages validated OK")
    else:
        print("SFT message validation had errors")
        raise SystemExit(1)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Generate sample cases and SFT messages.")
    ap.add_argument("--cases", default=None, help="Path to input cases JSONL (if provided, renders SFT from these cases)")
    ap.add_argument("--out", default=None, help="Output path for SFT messages JSONL")
    ap.add_argument("--source", default="v05_sample_dry_run", help="Source tag for metadata")
    args = ap.parse_args()

    if args.cases:
        # External mode: render SFT from provided cases file
        if not args.out:
            print("ERROR: --out required when --cases is provided")
            raise SystemExit(1)
        render_sft_from_cases(args.cases, args.out, args.source)
    else:
        # Default mode: generate 20 sample cases
        exit_code = validate_everything()
        write_outputs()
        raise SystemExit(exit_code)
