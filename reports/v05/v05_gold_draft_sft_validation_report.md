# V0.5 Gold Draft SFT Validation Report

**Date:** 2026-06-02  
**Context:** 5.3-C2  

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

## 3. Parse Check

All 100 DSL strings parse successfully. No parse errors.

## 4. No Markdown / No JSON Check

| Check | Violations |
|-------|:----------:|
| Markdown fences (```) | 0 |
| JSON (starts with `{`) | 0 |

## 5. Source and Metadata Check

| Field | Expected | Actual |
|-------|----------|-------|
| `source` | `v05_gold_draft` | ✅ |
| `metadata.is_final_train_data` | `false` | ✅ |
| `metadata.is_locked_gold` | `false` | ✅ |
| `metadata.split` | `gold_draft` | ✅ |
| `metadata.gold_partition` | `gold_core` or `gold_hard` | ✅ |

## 6. Example Row

```json
{
  "messages": [
    {"role": "system", "content": "You are a memory policy router for coding-agent contexts..."},
    {"role": "user", "content": "RUNTIME_CONTEXT\nproject: ci-pipeline\nrepo: build-system\nservice: artifact-publisher\ntask: check artifact retention policy\n\nCANDIDATE_MEMORIES\nm1 [service_memory]: The artifact-publisher retains build artifacts for 30 days...\nm2 [repo_memory]: Artifact retention settings are in config/artifact_policy.yaml...\n\nCURRENT_UNITS\nu1: How long are snapshot builds kept in the artifact store before cleanup?"},
    {"role": "assistant", "content": "READ m1\nSTORE NONE\nSKIP u1"}
  ],
  "case_id": "v05_gold_core_0001",
  "source": "v05_gold_draft",
  "metadata": {
    "tags": ["read_only", "temporary_request"],
    "num_candidate_memories": 2,
    "num_current_units": 1,
    "gold_shape": "READ-only",
    "store_targets": [],
    "is_final_train_data": false,
    "is_locked_gold": false,
    "gold_partition": "gold_core",
    "split": "gold_draft"
  }
}
```

## 7. Summary

All 100 SFT messages valid. Ready for training use only after gold is locked and promoted to final.

---

*End of V0.5 Gold Draft SFT Validation Report.*
