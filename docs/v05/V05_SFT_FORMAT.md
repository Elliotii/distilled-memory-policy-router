# V0.5 SFT Format

Version: v0.5 draft  
Date: 2026-06-01  
Status: Planning; format specification only  

## 1. SFT Message Format

Training data for v0.5 LoRA/SFT uses a chat-style JSONL message format compatible with Hugging Face `apply_chat_template`.

### JSONL Row Structure

```json
{
  "messages": [
    {"role": "system", "content": "<system prompt>"},
    {"role": "user", "content": "<rendered input>"},
    {"role": "assistant", "content": "<Unit DSL output>"}
  ],
  "case_id": "v05_train_0001",
  "source": "v05_train",
  "metadata": {
    "tags": ["read_store_joint", "service_invariant"],
    "num_candidate_memories": 4,
    "num_current_units": 3,
    "gold_shape": "READ + STORE joint",
    "store_targets": ["service_memory", "repo_memory"]
  }
}
```

### Required Fields

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `messages` | array | yes | Chat messages: system, user, assistant |
| `case_id` | string | yes | Unique case identifier |
| `source` | string | yes | Split identifier: `v05_train`, `v05_dev`, `v05_gold` |
| `metadata` | object | yes | Case metadata for filtering and analysis |

### Messages

| Role | Content |
| --- | --- |
| `system` | Policy router instruction (system prompt) |
| `user` | Rendered input: runtime_context + candidate_memories + current_units |
| `assistant` | Unit DSL output only |

## 2. Assistant Target

The assistant message must contain **only** valid Unit DSL:

```
READ m1,m2
STORE service_memory u1
STORE repo_memory u2
SKIP u3
```

Rules:
- No explanations, commentary, or markdown
- No JSON
- Strict DSL grammar as defined by `src/v04/parser.py`
- Every current unit must appear exactly once (STORE or SKIP)
- READ may reference only valid candidate memory IDs
- Only the 5 legal STORE targets allowed

## 3. User Input Rendering

The user message renders three input sections in a consistent format:

```
RUNTIME_CONTEXT
project: <project>
repo: <repo>
service: <service>
task: <task>

CANDIDATE_MEMORIES
<m1> [target]: <content>
<m2> [target]: <content>

CURRENT_UNITS
<u1>: <text>
<u2>: <text>
<u3>: <text>
```

When candidate_memories is empty, render `NONE`:
```
CANDIDATE_MEMORIES
NONE
```

When current_units is empty (should not happen in valid cases), render `NONE`.

## 4. System Prompt

The system prompt should be based on the `unit_dsl_fewshot.txt` prompt design learnings:

```text
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

**Few-shot examples in training:**
- If training uses a few-shot system prompt, the examples MUST come from the train split
- Do NOT embed dev or gold cases in the system prompt
- Few-shot examples used in training should be recorded in metadata

## 5. Validation Before Training

Every assistant target in training data must be validated:

1. **Parse check**: Parse with `src/v04/parser.py` — must produce `validation.valid = true`
2. **Gold consistency**: Parsed READ IDs, STORE (unit_id, target) pairs, and SKIP IDs must match the case's gold labels
3. **Unit coverage**: Every current unit must appear exactly once across STORE and SKIP
4. **ID validity**: Only legal memory IDs, unit IDs, and targets
5. **No forbidden content**: No `ADD`, `UPDATE`, `DELETE`, `MERGE`, `confidence`, `reason`, `entity`, or other forbidden fields

### Validation Script (template)

```python
from src.v04.parser import parse_policy_dsl, LEGAL_TARGETS
from src.v04.case_validator import validate_case

def validate_training_case(case):
    result = validate_case(case)
    if not result["valid"]:
        return False, result["errors"]
    
    dsl = case["gold"]["dsl"]
    parsed = parse_policy_dsl(
        dsl,
        [m["memory_id"] for m in case["candidate_memories"]],
        [u["unit_id"] for u in case["current_units"]],
        LEGAL_TARGETS,
    )
    if not parsed["validation"]["valid"]:
        return False, parsed["validation"]["errors"]
    
    return True, []
```

## 6. Training / Eval Separation

### Train split (`v05_train`)
- Used for LoRA/SFT training
- May include few-shot examples in system prompt (from train only)
- Distribution targets as per `V05_DATA_PLAN.md`

### Dev split (`v05_dev`)
- Used for hyperparameter tuning and early stopping
- NOT used in system prompt
- NOT seen during training weight updates
- Representative distribution matching train

### Gold split (`v05_gold`)
- Locked. Never used during training, tuning, or prompt design
- Opened only for final evaluation
- Must be representative of real task distribution
- Includes challenging cases (target-boundary, sensitive, etc.)

## 7. Data File Convention

Proposed file paths:

```
data/v05/train.jsonl     # 500–1000 cases
data/v05/dev.jsonl       # 80–100 cases
data/v05/gold.jsonl      # 100 cases (locked)
```

Each file is a standard JSONL file with one training message per line.

## 8. Future Extension

### Unit JSON as alternative SFT format

If DSL training underperforms (fails Go criteria), Unit JSON may be used as an alternative training target:

```json
{
  "messages": [
    {"role": "system", "content": "...system prompt..."},
    {"role": "user", "content": "...rendered input..."},
    {"role": "assistant", "content": "{\"read\":[\"m1\"],\"store\":[{\"target\":\"service_memory\",\"unit_id\":\"u1\"}],\"skip\":[\"u2\"]}"}
  ]
}
```

This is a fallback only. Do not implement Unit JSON SFT format in this context unless DSL training has been attempted and failed.

### Qwen3.5 challenger

If Qwen3.5 becomes available, the same data format can be used to train a larger model for comparison. No format changes needed — only model path and training config differ.

## 9. Files Reference

| File | Purpose |
| --- | --- |
| `docs/v05/V05_SFT_FORMAT.md` | This document |
| `prompts/v04/unit_dsl.txt` | Zero-shot DSL prompt |
| `prompts/v04/unit_dsl_fewshot.txt` | Few-shot DSL prompt (3 examples) |
| `src/v04/parser.py` | DSL → canonical JSON parser |
| `src/v04/case_validator.py` | Case structure validator |
| `docs/v04_spec/CASE_SCHEMA.md` | Case record format |
