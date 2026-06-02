# V0.5 Qwen Prompt/Runner Fix Report

**Date:** 2026-06-02  
**Context:** 5.4-C — prompt and runner fixes after root cause audit  

---

## 1. Files Changed

| File | Change |
|------|--------|
| `src/v05/qwen_v05_output_runner.py` | Complete rewrite — SFT-style chat roles, canonical interfaces, thinking suppression |
| `prompts/v05/unit_dsl_zero_shot.txt` | No longer used directly — system prompt embedded in runner |
| `prompts/v05/unit_dsl_fewshot.txt` | No longer used directly |
| `prompts/v05/unit_json_zero_shot.txt` | No longer used directly |
| `prompts/v05/unit_json_fewshot.txt` | No longer used directly |

## 2. Canonical Interface Fix

**Before:** `"interface": "unit_dsl_zero_shot"` → eval_runner rejected (unknown interface)

**After:** `"interface": "unit_dsl"` with `"prompt_variant": "zero_shot"` → eval_runner routes correctly

System names now unique and descriptive:
- `qwen3-4b_unit_dsl_zero_shot`
- `qwen3-4b_unit_dsl_fewshot`
- `qwen3-4b_unit_json_zero_shot`
- `qwen3-4b_unit_json_fewshot`
- `qwen3.5_unit_dsl_zero_shot`
- `qwen3.5_unit_dsl_fewshot`
- `qwen3.5_unit_json_zero_shot`
- `qwen3.5_unit_json_fewshot`

## 3. Chat Role Fix

**Before:** Single user message with everything blended.
```python
messages = [{"role": "user", "content": prompt}]
```

**After:** Proper role separation.
```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": case_input}
]
```

For few-shot: conversation turns.
```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": ex1_input},
    {"role": "assistant", "content": ex1_output},
    ...,
    {"role": "user", "content": target_case_input}
]
```

## 4. Prompt Template Fix

- System instructions (role, targets, rules) moved to `system` role
- Case data (runtime_context, candidate_memories, current_units) rendered as `user` role
- Few-shot examples as separate user/assistant conversation turns
- READ list format clarified: "comma-separated memory_ids"

## 5. Thinking Suppression Fix

For Qwen3.5:
```python
chat_kwargs = {"enable_thinking": False}
tokenizer.apply_chat_template(messages, ..., **chat_kwargs)
```

Metadata recorded: `enable_thinking_requested`, `enable_thinking_applied`, `thinking_tags_present`.

**Result:** Qwen3.5 now produces concise DSL/JSON (40-200 chars) instead of 2000+ chars of prose. Latency dropped from ~19s to ~1-2s per case.

## 6. Raw Output Preservation

- All predictions store unmodified `raw_output`
- No post-processing, no silent repair
- Both parseable and unparseable outputs preserved as-is

## 7. Risks

- System prompt is now embedded in runner code rather than separate files — harder to version independently
- `enable_thinking=False` in `apply_chat_template` kwargs may not be universally supported — recorded in metadata for audit
- Few-shot examples hardcoded in runner — changing examples requires code changes

---

*End of V0.5 Qwen Prompt/Runner Fix Report.*
