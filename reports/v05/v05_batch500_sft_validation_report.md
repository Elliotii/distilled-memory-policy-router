# V0.5 Batch500 SFT Validation Report

**Date:** 2026-06-02  
**Context:** 5.2-A — SFT message validation for batch500

---

## 1. SFT Row Count

| Metric | Value |
|--------|-------|
| Batch500 cases | 500 |
| SFT messages generated | 500 |
| Missing messages | 0 |
| Extra messages | 0 |

---

## 2. Schema Check

All 500 SFT messages conform to the V0.5 SFT format specification:

```json
{
  "messages": [
    {"role": "system", "content": "<system prompt>"},
    {"role": "user", "content": "<rendered input>"},
    {"role": "assistant", "content": "<Unit DSL output>"}
  ],
  "case_id": "v05_batch500_0001",
  "source": "v05_batch500_dry_run",
  "metadata": {
    "tags": [...],
    "num_candidate_memories": <int>,
    "num_current_units": <int>,
    "gold_shape": "<shape>",
    "store_targets": [...],
    "is_final_train_data": false
  }
}
```

All required fields present in all 500 messages.

---

## 3. Assistant == Gold DSL

| Check | Result |
|-------|--------|
| assistant content equals case gold.dsl | 500/500 (100%) |
| Mismatches | 0 |

---

## 4. Parse Check

| Check | Result |
|-------|--------|
| assistant DSL parses with strict parser | 500/500 (100%) |
| Parser errors | 0 |

---

## 5. No Markdown / No JSON Check

| Check | Result |
|-------|--------|
| Markdown fences (```) in assistant | 0/500 |
| JSON in assistant (starts with `{`) | 0/500 |
| Prose/explanations in assistant | 0/500 |

All assistant messages contain only valid Unit DSL.

---

## 6. System/User Rendering Summary

System prompt: Standard policy router instruction (~420 chars) defining task, DSL grammar, legal targets, and routing rules. No few-shot examples embedded (zero-shot training format).

User input format:
```
RUNTIME_CONTEXT
project: <project>
repo: <repo>
service: <service>
task: <task>

CANDIDATE_MEMORIES
<m1> [target]: <content>
...
(or NONE)

CURRENT_UNITS
<u1>: <text>
...
```

All 500 user messages follow this format consistently.

---

## 7. One Rendered Example

### Case v05_batch500_0001

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
project: customer-support
repo: helpdesk
service: ticket-router
task: define ticket routing algorithm

CANDIDATE_MEMORIES
m1 [service_memory]: The ticket router assigns incoming tickets to agents based on skill tags and current queue depth.
m2 [task_state]: The current routing uses round-robin assignment without considering agent expertise.

CURRENT_UNITS
u1: The ticket router must route billing-related tickets to agents with the billing_certified skill tag, ignoring queue-balance for these tickets.
u2: Update the agent skill matrix to include the new billing_certified tag for 5 agents.
```

**Assistant:**
```
READ m1,m2
STORE service_memory u1
STORE task_state u2
SKIP NONE
```

---

## 8. SFT Validation Summary

| Check | Result |
|-------|--------|
| Row count matches cases | 500/500 |
| Schema compliance | 500/500 |
| Assistant == gold.dsl | 500/500 |
| DSL parse success | 500/500 |
| No markdown in assistant | 500/500 |
| No JSON in assistant | 500/500 |
| is_final_train_data = false | 500/500 |
| System prompt consistent | 500/500 |
| User format consistent | 500/500 |

**All SFT validation checks passed.**

---

## 9. Risks Before Real Training

1. **service_memory distribution (39.1%):** Above the 30-34% blueprint target. Training on this data may bias the model toward predicting service_memory over other targets. Mitigation: rebalance before training.

2. **Zero-shot format:** No few-shot examples in system prompt. The model must learn the DSL format purely from training. This is the intended zero-shot-to-trained comparison, but may require careful learning rate scheduling.

3. **17-domain diversity:** While beneficial for generalization, 17 domains with ~30 cases each may dilute domain-specific patterns. Consider whether to reduce domain count for training.

4. **False negatives in validation:** The keyword-based sensitive check produces false positives; actual sensitive content may exist in edge cases. A manual review of 10% of cases is recommended.

---

*End of SFT validation report.*
