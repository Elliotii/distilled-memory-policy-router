# V0.5b JSON SFT Rendering Report

**Date:** 2026-06-02  
**Status:** Complete — All 4 JSON SFT files rendered and validated  

---

## Rendering Script

`src/v05/render_json_sft_messages.py`

### Method

1. Loads v0.5 case JSONL (unchanged).
2. Reuses `render_user_input(case)` from `src/v05/render_sft_messages.py` for user message.
3. Uses `JSON_SYSTEM_PROMPT` with Unit JSON format specification.
4. Converts `case.gold` to canonical Unit JSON assistant via `build_json_assistant()`.
5. Validates every rendered message against the source case gold.
6. Writes chat-style SFT JSONL with strict JSON-only assistant.

### System Prompt

The JSON system prompt specifies:
- Task description (same as DSL)
- Output format: `{"read": [...], "store": [...], "skip": [...]}`
- Legal STORE targets: user_profile, project_memory, repo_memory, service_memory, task_state
- Rules: READ useful only, STORE durable info, SKIP sensitive/temp, cover all units, don't invent IDs/targets
- Explicit prohibition: no markdown, no prose, no comments, no explanations

### Assistant Format

Compact JSON (matching eval_runner's `render_unit_json`):
```json
{"read":["m1","m3"],"store":[{"target":"service_memory","unit_id":"u1"}],"skip":["u2"]}
```

Use of `json.dumps(ensure_ascii=True, separators=(",", ":"))` for consistency with eval_runner.

---

## Rendered Files

| File | Input Cases | Rows |
|------|:-----------:|:----:|
| `data/v05b/json_sft/v05b_train_125_json_sft_messages.jsonl` | train 125 | 125 |
| `data/v05b/json_sft/v05b_train_250_json_sft_messages.jsonl` | train 250 | 250 |
| `data/v05b/json_sft/v05b_train_500_json_sft_messages.jsonl` | train 500 | 500 |
| `data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl` | dev | 100 |

---

## SFT Message Structure

Each row:
```json
{
  "messages": [
    {"role": "system", "content": "<JSON_SYSTEM_PROMPT>"},
    {"role": "user", "content": "<render_user_input(case)>"},
    {"role": "assistant", "content": "{\"read\":[\"m1\"],\"store\":[],\"skip\":[\"u1\"]}"}
  ],
  "case_id": "v05_batch100_0002",
  "source": "v05b_train_125",
  "metadata": {
    "tags": ["read_only", "temporary_request"],
    "num_candidate_memories": 3,
    "num_current_units": 1,
    "gold_shape": "READ-only",
    "store_targets": [],
    "is_final_train_data": false
  }
}
```

---

## Case Coverage

All 975 cases (125+250+500+100) rendered with 0 errors.

Case IDs preserved exactly from source files. No label modifications.

---

*End of V0.5b JSON SFT Rendering Report.*
