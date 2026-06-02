# V0.5 Dev SFT Validation Report

**Date:** 2026-06-02  
**Context:** 5.3-B — Independent Dev Set Construction  
**File:** `data/v05/dev/v05_dev_sft_messages.jsonl`  

---

## 1. SFT Row Count

| Metric | Value |
|--------|:-----:|
| Expected rows | 100 |
| Actual rows | 100 |
| Match? | ✅ |

## 2. Assistant == gold.dsl Check

| Metric | Value |
|--------|:-----:|
| Rows checked | 100 |
| Mismatches | 0 |
| Match rate | 100% |

Every SFT message's `assistant` content equals the corresponding case's `gold.dsl` exactly.

## 3. Parse Check

All 100 DSL strings parse successfully via `src/v04/parser.py`. No parse errors.

## 4. No Markdown / No JSON Check

| Check | Violations |
|-------|:----------:|
| Markdown fences (```) in assistant | 0 |
| JSON (content starting with `{`) in assistant | 0 |

## 5. Source and Metadata Check

| Field | Expected | Actual | Status |
|-------|----------|--------|:------:|
| `source` | `v05_dev_dry_run` | `v05_dev_dry_run` | ✅ |
| `metadata.is_final_train_data` | `false` | `false` | ✅ |
| `metadata.split` | `dev` | `dev` | ✅ |
| `case_id` matches | Yes | Yes | ✅ |

## 6. Metadata Fields Present

Each SFT message contains:
- `messages` (system, user, assistant roles)
- `case_id`
- `source`
- `metadata`: `tags`, `num_candidate_memories`, `num_current_units`, `gold_shape`, `store_targets`, `is_final_train_data`, `split`

## 7. Example Row

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a memory policy router for coding-agent contexts.\n\nTask:\nGiven RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:\n- which candidate memories to READ;\n- which current unit IDs to STORE and to which target;\n- which current unit IDs to SKIP.\n\nOutput only the DSL. Do not include comments, prose, explanations, or JSON.\n\nAllowed DSL lines:\nREAD <memory_id_list|NONE>\nSTORE <target> <unit_id>\nSTORE NONE\nSKIP <unit_id_list|NONE>\n\nLegal STORE targets:\nuser_profile, project_memory, repo_memory, service_memory, task_state\n\nRules:\n- READ useful memories only; skip merely related or stale ones.\n- STORE durable, reusable information with correct target.\n- SKIP sensitive, temporary, one-off, or out-of-scope content.\n- Every current unit must appear exactly once in STORE or SKIP.\n- Do not invent IDs, targets, or content."
    },
    {
      "role": "user",
      "content": "RUNTIME_CONTEXT\nproject: telemetry-dashboard\nrepo: dashboard-backend\nservice: metrics-collector\ntask: verify collector retry policy\n\nCANDIDATE_MEMORIES\nm1 [service_memory]: The metrics-collector retries failed submissions 3 times with 5-second gaps before logging a permanent failure.\nm2 [repo_memory]: Collector configuration lives in config/metrics_collector.yaml with retry settings under the submission section.\n\nCURRENT_UNITS\nu1: What happens when the collector exhausts all retries — does it drop the data or queue it for later?"
    },
    {
      "role": "assistant",
      "content": "READ m1\nSTORE NONE\nSKIP u1"
    }
  ],
  "case_id": "v05_dev_0001",
  "source": "v05_dev_dry_run",
  "metadata": {
    "tags": ["read_only", "temporary_request"],
    "num_candidate_memories": 2,
    "num_current_units": 1,
    "gold_shape": "READ-only",
    "store_targets": [],
    "is_final_train_data": false,
    "split": "dev"
  }
}
```

## 8. Summary

All 100 SFT messages pass all validation checks. The SFT file is ready for training use (promotion to final train data pending all prerequisites in `V05_TRAIN_POOL_MANIFEST_PLAN.md`).

---

*End of V0.5 Dev SFT Validation Report.*
