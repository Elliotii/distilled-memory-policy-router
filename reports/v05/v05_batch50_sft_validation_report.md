# V0.5 Batch50 SFT Validation Report

Date: 2026-06-01  
Context: 5.0-E — SFT format validation for batch50  
Status: Format validation only; no training performed

## 1. SFT Row Count

| Item | Count |
| --- | ---: |
| Batch50 cases | 50 |
| SFT messages | 50 |
| Source tag | `v05_batch50_dry_run` |
| `is_final_train_data` | all `false` |

## 2. Schema Check

All 50 SFT messages follow the chat format:

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "case_id": "...",
  "source": "v05_batch50_dry_run",
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

All required fields present. No extra fields.

## 3. Assistant == gold.dsl

All 50 assistant messages exactly match their case's `gold.dsl`. **0 mismatches.**

## 4. Parse Check

All 50 assistant DSL outputs parse correctly with `src.v04.parser.parse_policy_dsl()`:
- 50/50 → `validation.valid = True`
- 0 parse errors

## 5. No Markdown / No JSON Check

- 0 messages contain markdown fences (```)
- 0 messages start with `{` (no JSON output)
- All messages are pure DSL text

## 6. System / User Rendering Summary

- System prompt: consistent across all 50 messages (~980 chars)
- User message format: `RUNTIME_CONTEXT / CANDIDATE_MEMORIES / CURRENT_UNITS`
- `CANDIDATE_MEMORIES` renders `NONE` when empty (16 messages)
- Average user message length: ~400 chars
- Average assistant message length: ~47 chars

## 7. One Rendered Example

### v05_batch50_0030 (READ + STORE joint, stale + related)

**System:** (standard system prompt, same as all messages)

**User:**
```
RUNTIME_CONTEXT
project: data-platform
repo: data-jobs
service: pipeline
task: add incremental load support

CANDIDATE_MEMORIES
m1 [service_memory]: The pipeline currently performs full-table refreshes for all dimension tables every night.
m2 [service_memory]: Full-table refreshes on the billing_facts table take approximately 45 minutes and lock the table for writes.
m3 [task_state]: The billing_facts table was last partitioned by month in the 2026-04 schema change.
m4 [service_memory]: The legacy v0 pipeline used a custom CDC connector that has since been deprecated.

CURRENT_UNITS
u1: Add incremental load support using a high-watermark column updated_at. The pipeline should only process rows where updated_at > last_load_time.
u2: The incremental load feature must support a full-refresh fallback when the high-watermark is detected as stale.
u3: The high-watermark values should be persisted in the pipeline_metadata table, not in memory.
```

**Assistant:**
```
READ m1,m2
STORE service_memory u1
STORE service_memory u2
STORE repo_memory u3
SKIP NONE
```

## 8. Risks Before Real Training

### Format Risks
- System prompt length (~980 chars) is fixed; any change would require regenerating all SFT messages
- User messages for complex cases approach ~600 chars; max token length for Qwen3-4B (32K context) is not at risk but should be monitored at 500+ case scale

### Content Risks
- Assistant must remain pure DSL; any training deviation (model outputting markdown or JSON) would break parsing
- Gold DSL quality depends on semantic label correctness — see semantic audit for flagged cases

### Pipeline Risks
- Tokenizer must handle DSL line breaks and commas; tested on 30-case dry run previously (100% parse success on DSL interface)
- Batch training requires consistent padding across different numbers of STORE lines

## 9. Recommendation

The SFT format is stable and well-validated at 50-case scale. No format issues were found. The format is ready for training data generation at 100+ case scale.
