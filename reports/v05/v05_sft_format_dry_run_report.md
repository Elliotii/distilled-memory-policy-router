# V0.5 SFT Format Dry Run Report

Date: 2026-06-01  
Context: 5.0-B — v0.5 sample data dry run  
Status: Format validation only; no training performed

## 1. SFT Message Schema

Each JSONL row follows the chat message format:

```json
{
  "messages": [
    {"role": "system", "content": "<system prompt>"},
    {"role": "user", "content": "<rendered input>"},
    {"role": "assistant", "content": "<Unit DSL>"}
  ],
  "case_id": "v05_sample_0001",
  "source": "v05_sample_dry_run",
  "metadata": {
    "tags": ["read_only", "service_invariant"],
    "num_candidate_memories": 3,
    "num_current_units": 1,
    "gold_shape": "READ-only",
    "store_targets": [],
    "is_final_train_data": false
  }
}
```

## 2. System Prompt Summary

The system prompt is based on the `unit_dsl_fewshot.txt` design learnings, adapted for SFT (no few-shot examples in the system prompt — those would go in training-specific versions):

- Defines the task: READ, STORE, SKIP
- Specifies allowed DSL lines and grammar
- Lists the five legal STORE targets
- Provides core rules: read useful only, store durable, skip sensitive/temporary
- Requires exactly-once unit assignment
- Forbids inventing IDs, targets, or content

The prompt is concise (~1KB) and does not include few-shot examples in this dry run version. For actual training, few-shot examples could be added to the system prompt if they come from the train split only.

## 3. User Rendering Format

The user message renders three sections:

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

Format verified for all 20 SFT messages. When candidate_memories is empty, renders "NONE".

## 4. Assistant Target Format

The assistant message contains **only** Unit DSL:

```
READ m1,m2
STORE service_memory u1
STORE repo_memory u2
SKIP u3
```

Or with empty sets:
```
READ NONE
STORE NONE
SKIP u1,u2
```

## 5. Dry Run Statistics

| Item | Count |
| --- | ---: |
| Total SFT messages | 20 |
| Source | all `v05_sample_dry_run` |
| `is_final_train_data` | all `false` |
| System prompt length | ~980 chars |
| Avg user message length | ~350 chars |
| Avg assistant message length | ~43 chars |
| Unique DSL patterns | 17 distinct DSL outputs |

## 6. Validation Checks

### Assistant == gold.dsl

All 20 SFT messages have `assistant.content == case.gold.dsl`. **0 mismatches.**

### Parse Check

All 20 assistant DSL outputs parse correctly with `src.v04/parser.py`:

```
parse_policy_dsl(assistant_content, candidate_ids, unit_ids, LEGAL_TARGETS)
→ validation.valid = True for all 20
```

### No Markdown / No JSON

All 20 assistant messages:
- No markdown fences (```)
- No JSON (does not start with `{`)
- Pure DSL text only

### Structural Consistency

For all 20 messages:
- Every current unit appears exactly once in STORE or SKIP
- All READ IDs reference valid candidate memory IDs
- All STORE/SKIP IDs reference valid current unit IDs
- All STORE targets are from the 5 legal targets

### Metadata

All 20 messages have:
- `metadata.is_final_train_data = false`
- `metadata.tags` matches case tags
- `metadata.gold_shape` consistent with case
- `metadata.store_targets` consistent with case gold

## 7. Example Rendered Message

### v05_sample_0012 (READ + STORE joint, service vs task boundary)

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
project: data-platform
repo: data-jobs
service: export
task: add export validation step

CANDIDATE_MEMORIES
m1 [service_memory]: The export job writes invoices to S3 daily at 02:00 UTC using IAM role export-writer.
m2 [service_memory]: The export job currently does NOT validate file integrity after writing.
m3 [repo_memory]: Export job configuration lives in config/export.yaml with schema version 2.

CURRENT_UNITS
u1: Add a SHA-256 checksum validation step that runs after the S3 write and logs the result.
u2: The export job is blocked until the IAM role is updated with the new S3 permissions.
```

**Assistant:**
```
READ m1,m2,m3
STORE service_memory u1
STORE task_state u2
SKIP NONE
```

## 8. Risks Before Real Training

### Format Risks
- **System prompt length:** ~980 chars is reasonable but needs testing whether longer prompts impact 4B model attention
- **Few-shot examples:** If added to system prompt, examples must come from train split only
- **User message length:** Some cases with many candidate memories could produce very long user messages — need max-length testing

### Content Risks
- **Assistant must be pure DSL:** Any deviation (markdown, JSON, explanations) would break parser. Training must enforce this.
- **Label quality:** Gold DSL must be semantically correct — see semantic audit report for 5 high-risk cases
- **Target boundary:** project_memory vs task_state confusion in training data would train the model to make the same mistakes

### Pipeline Risks
- **Tokenizer compatibility:** The Qwen3-4B tokenizer must handle DSL line breaks and commas correctly
- **Max token length:** System + user messages for complex cases may exceed model context window
- **Batch consistency:** Different cases have different numbers of STORE lines — padding strategy needed

## 9. Recommendations

1. **SFT format is viable.** The dry run confirms the format is well-defined, parseable, and structurally consistent.
2. **Test with 50-100 cases** before scaling to 500+ to detect format or length issues.
3. **Add max-input-length validation** to prevent cases from exceeding model context window.
4. **Lock system prompt** for a training run; do not change it between train/dev/gold.
5. **Human review required** before any SFT messages are used for training (see semantic audit).
