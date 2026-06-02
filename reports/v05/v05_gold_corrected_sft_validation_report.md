# V0.5 Gold Corrected SFT Validation Report

**Date:** 2026-06-02  
**Context:** 5.3-D — SFT validation of corrected gold draft  
**Status:** Corrected draft — NOT locked  

---

## 1. SFT Row Count

| Property | Value |
|----------|:-----:|
| SFT messages | 100 |
| Source | v05_gold_corrected |
| Generated from | v05_gold_corrected_cases.jsonl |

## 2. Assistant == Gold DSL

| Check | Result |
|-------|:------:|
| All 100 assistant messages == gold.dsl | ✅ |
| No mismatches | ✅ |

**Sample verification:** For every row, `messages[2]["content"]` exactly matches the corresponding case's `gold.dsl` field.

## 3. Parse Check

| Check | Result |
|-------|:------:|
| All 100 gold.dsl parses via src/v04/parser.py | ✅ |
| Parsed canonical == structured gold | ✅ |
| No parse errors | ✅ |

## 4. No Markdown / JSON Check

| Check | Result |
|-------|:------:|
| No "```" in any assistant message | ✅ |
| No assistant starts with "{" | ✅ |
| All assistants are pure DSL | ✅ |

## 5. Source / Metadata Check

| Field | Expected | Actual |
|-------|----------|--------|
| `source` | `v05_gold_corrected` | ✅ |
| `metadata.split` | `gold_corrected` | ✅ |
| `metadata.is_locked_gold` | `false` | ✅ |
| `metadata.is_final_train_data` | `false` | ✅ |
| `metadata.gold_partition` (core) | `gold_core` | ✅ |
| `metadata.gold_partition` (hard) | `gold_hard` | ✅ |

## 6. Example Row

```json
{
  "messages": [
    {"role": "system", "content": "You are a memory policy router..."},
    {"role": "user", "content": "RUNTIME_CONTEXT\nproject: ci-pipeline\nrepo: build-system\nservice: artifact-publisher\ntask: check artifact retention policy\n\nCANDIDATE_MEMORIES\nm1 [service_memory]: The artifact-publisher retains build artifacts for 30 days...\nm2 [repo_memory]: Artifact retention settings are in config/artifact_policy.yaml...\n\nCURRENT_UNITS\nu1: How long are snapshot builds kept in the artifact store before cleanup?"},
    {"role": "assistant", "content": "READ m1\nSTORE NONE\nSKIP u1"}
  ],
  "case_id": "v05_gold_core_0001",
  "source": "v05_gold_corrected",
  "metadata": {
    "tags": ["read_only", "temporary_request"],
    "num_candidate_memories": 2,
    "num_current_units": 1,
    "gold_shape": "READ-only",
    "store_targets": [],
    "split": "gold_corrected",
    "is_locked_gold": false,
    "is_final_train_data": false,
    "gold_partition": "gold_core"
  }
}
```

## 7. Summary

All SFT messages correctly generated from corrected gold cases. All structural, DSL, metadata, and content checks pass. SFT is ready for use **only after gold is locked** — currently it is a corrected draft.

---

*End of V0.5 Gold Corrected SFT Validation Report.*
