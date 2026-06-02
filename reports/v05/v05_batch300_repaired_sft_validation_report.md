# V0.5 Batch300 Repaired SFT Validation Report

**Date:** 2026-06-02  
**Context:** 5.1-D — SFT validation of repaired batch300

---

## 1. SFT Row Count

| File | Rows | Expected |
|------|:----:|:--------:|
| v05_batch300_sft_messages.jsonl | 300 | 300 |

**PASS:** Row count matches case count exactly.

---

## 2. Schema Check

Each SFT message has the required structure:

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "case_id": "v05_...",
  "source": "v05_batch300_dry_run",
  "metadata": {
    "tags": [...],
    "num_candidate_memories": N,
    "num_current_units": N,
    "gold_shape": "...",
    "store_targets": [...],
    "is_final_train_data": false
  }
}
```

**All 300 rows pass schema validation.** All `messages` arrays have exactly 3 elements in the correct role order (system, user, assistant).

---

## 3. Assistant == Gold DSL

| Check | Result |
|-------|:------:|
| assistant content equals case gold.dsl | **300/300 PASS** |
| DSL parsed canonical equals structured gold | **300/300 PASS** |

Every SFT assistant message contains exactly the DSL string from the corresponding case's `gold.dsl` field. The parser confirms that the DSL is semantically consistent with the structured `gold.read`, `gold.store`, and `gold.skip` fields.

---

## 4. Parse Check

All 300 DSL strings parse correctly:
- READ lines reference valid candidate_memory IDs
- STORE lines use valid targets (user_profile, project_memory, repo_memory, service_memory, task_state)
- STORE lines reference valid current_unit IDs
- SKIP lines reference valid current_unit IDs
- Every current_unit appears exactly once in STORE or SKIP
- No duplicate STORE or SKIP assignments
- No STORE/SKIP conflicts
- No unknown targets
- No invented IDs

---

## 5. No Markdown / No JSON Check

| Check | Result |
|-------|:------:|
| Markdown fences (```) in assistant | **0/300** |
| JSON content in assistant | **0/300** |
| HTML/markdown formatting in assistant | **0/300** |

All assistant messages contain only plain-text DSL. No formatting artifacts.

---

## 6. System/User Rendering Summary

**System prompt:** Used consistently across all 300 SFT messages. Contains:
- Router task description
- Allowed DSL lines
- Legal STORE targets
- Rules for READ, STORE, SKIP

**User input:** Rendered from `runtime_context`, `candidate_memories`, and `current_units` using the standard `render_user_input()` function. Format:
```
RUNTIME_CONTEXT
project: <project>
repo: <repo>
service: <service>
task: <task>

CANDIDATE_MEMORIES
<m_id> [<target>]: <content>
...
(or "NONE")

CURRENT_UNITS
<u_id>: <text>
...
```

---

## 7. One Rendered Example

### Case: v05_batch300_0060 (Circuit Breaker)

**System:**
```
You are a memory policy router for coding-agent contexts.

Task:
Given RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:
- which candidate memories to READ;
- which current unit IDs to STORE and to which target;
- which current unit IDs to SKIP.

Output only the DSL. Do not include comments, prose, explanations, or JSON.

Allowed DSL lines:
READ <memory_id_list|NONE>
STORE <target> <unit_id>
STORE NONE
SKIP <unit_id_list|NONE>

Legal STORE targets:
user_profile, project_memory, repo_memory, service_memory, task_state

Rules:
- READ useful memories only; skip merely related or stale ones.
- STORE durable, reusable information with correct target.
- SKIP sensitive, temporary, one-off, or out-of-scope content.
- Every current unit must appear exactly once in STORE or SKIP.
- Do not invent IDs, targets, or content.
```

**User:**
```
RUNTIME_CONTEXT
project: workflow-automation
repo: flowcraft
service: orchestrator
task: add circuit breaker for downstream failures

CANDIDATE_MEMORIES
m1 [service_memory]: The orchestrator calls external services for each workflow step and retries on failure, but has no circuit breaker pattern.
m2 [service_memory]: Last week's production incident: the payment gateway was down for 45 minutes, and the orchestrator retried 10,000+ payment steps, saturating connection pools.

CURRENT_UNITS
u1: The orchestrator must implement a circuit breaker per external service: open the circuit after 5 consecutive failures in a 60-second window, then half-open after 120 seconds with a single probe request.
u2: When a circuit is open, the orchestrator must mark affected workflow steps as deferred rather than failed, and resume them automatically when the circuit closes.
u3: Document the circuit breaker design in docs/orchestrator/circuit_breaker.md with a state diagram and per-service thresholds.
```

**Assistant:**
```
READ m1,m2
STORE service_memory u1
STORE service_memory u2
STORE repo_memory u3
SKIP NONE
```

---

## 8. Risks Before Real Training

| Risk | Severity | Mitigation |
|------|:--------:|------------|
| System prompt drift | LOW | System prompt is frozen in source code; changes require explicit update |
| DSL format inconsistency | LOW | All 300 assistant messages use identical DSL format with consistent ordering (READ, STORE, SKIP) |
| Metadata.is_final_train_data | NONE | All 300 messages have `is_final_train_data: false` |
| Assistant content truncation | LOW | DSL strings are short (typically <200 chars), far below any truncation threshold |
| Role ordering | NONE | All messages follow system → user → assistant order |
| Case_id tracking | NONE | Every SFT message has a unique case_id matching the source case |
| Source tag | NONE | All messages use `v05_batch300_dry_run` source tag (appropriate for training pool) |

---

## 9. Recommendation

The SFT messages are production-ready for training infrastructure. Before real training:
1. Update `source` tag from `v05_batch300_dry_run` to a training-specific tag
2. Set `is_final_train_data` to `true` after final audit
3. Verify the system prompt is appropriate for the target model
4. Confirm DSL format is compatible with the model's output expectations

---

*End of SFT validation report.*
