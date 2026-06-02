# V0.5 Qwen Smoke Root Cause Audit

**Date:** 2026-06-02  
**Context:** 5.4-C — diagnosis of 0% parse success in 5.4-B smoke  

---

## 1. Previous 0% Parse Summary

In Context 5.4-B, eval_runner reported 0% parse success for all 40 predictions (2 models × 4 interfaces × 5 cases). This audit identifies the root causes.

## 2. Raw Output Samples

### Qwen3-4B DSL zero-shot (all 5 cases identical)

```
READ NONE
STORE NONE
SKIP NONE
```

Verdict: **Valid DSL syntax.** Parses to empty read/store/skip. Not a parse failure — a content failure. Metrics would be non-zero (some computed correctly for empty predictions).

### Qwen3-4B DSL few-shot (all 5 cases identical)

```
READ NONE
STORE project_memory u1
STORE repo_memory u2
STORE service_memory u3
SKIP u4
```

Verdict: **Valid DSL syntax.** BUT uses template-matched unit IDs from few-shot examples, not from the actual case input. Parses but semantically wrong. Not a parse failure — a content failure.

### Qwen3-4B JSON zero/few-shot (all 5 cases identical)

```json
{"read": [], "store": [], "skip": []}
```

Verdict: **Valid JSON.** Empty content. Not a parse failure — a content failure.

### Qwen3.5 all interfaces

```
~2000-2400 chars of verbose prose/analysis thinking text.
No DSL lines. No JSON. No parseable content.
Contains: "let's tackle this problem step by step" thinking pattern.
```

Verdict: **Not parseable as DSL or JSON.** True parse failure — the model outputs prose exclusively.

## 3. Interface Field Audit

| Field in prediction JSONL | eval_runner expects | Match? |
|---------------------------|---------------------|:------:|
| `unit_dsl_zero_shot` | `unit_dsl` | ❌ |
| `unit_dsl_fewshot` | `unit_dsl` | ❌ |
| `unit_json_zero_shot` | `unit_json` | ❌ |
| `unit_json_fewshot` | `unit_json` | ❌ |

**ROOT CAUSE #1:** All 40 predictions used non-canonical interface values. eval_runner's `parse_prediction()` function has an exact string match:

```python
if interface == INTERFACE_UNIT_DSL: ...    # "unit_dsl"
if interface == INTERFACE_UNIT_JSON: ...   # "unit_json"
raise ValueError(f"unknown interface: {interface}")
```

Every prediction was rejected at the parser level — the raw output was never even examined by the metric computation.

**Impact:** Even though Qwen3-4B outputs were structurally valid DSL/JSON, they scored 0% because the interface field didn't route to any parser.

## 4. Eval Runner Compatibility Audit

| Check | Finding |
|-------|---------|
| Interface routing | Only `unit_dsl` and `unit_json` accepted |
| DSL parser | Would parse Qwen3-4B outputs correctly |
| JSON parser | Would parse Qwen3-4B JSON outputs correctly |
| Repair behavior | No auto-repair — failures counted as errors |
| System grouping | Uses `system` field, which was `qwen_local` (not model-specific) |

**Fix needed:** Use canonical `interface` values. Use descriptive `system` names.

## 5. Prompt Role Audit

Current prompt format: Single user message containing everything (instructions + case input).

```python
messages = [{"role": "user", "content": prompt}]  # everything in one message
```

This may cause issues:
- Qwen models are instruction-tuned with system + user role separation
- Without role separation, the model may treat instructions differently
- Few-shot examples embedded in user message aren't recognized as conversation turns

**ROOT CAUSE #2:** Single-message prompt format. The model doesn't properly separate system instructions from user input, leading to template-matching (few-shot) or empty defaults (zero-shot).

## 6. Qwen3.5 Thinking Audit

| Check | Finding |
|-------|---------|
| Output contains `<think>` tags | No explicit tags found |
| Output contains thinking patterns | Yes — "let's tackle this step by step" |
| `enable_thinking` flag | Not supported in this transformers version |
| `apply_chat_template` thinking kwarg | Not tested yet |

**ROOT CAUSE #3:** Qwen3.5 engages in verbose thinking before/instead of producing the requested output format. The model's instruction-following is overridden by its thinking behavior.

## 7. Root Cause Conclusion

| # | Root Cause | Impact | Severity |
|---|-----------|--------|:--------:|
| 1 | Non-canonical interface field names | ALL 40 predictions rejected at parser level | **Critical** |
| 2 | Single-message prompt format | Qwen3-4B template-matches or outputs empty; Qwen3.5 produces prose | **Critical** |
| 3 | Qwen3.5 thinking mode | All Qwen3.5 outputs are prose, not DSL/JSON | **High** |

**All three causes contributed to the 0% parse success.** Fix #1 alone would give Qwen3-4B some metrics from the few-shot outputs (though they'd be wrong). Fix #2 should improve both models. Fix #3 is Qwen3.5-specific.

## 8. Required Fixes

1. **Canonical interface names:** Use `unit_dsl` and `unit_json` in prediction JSONL
2. **SFT-style chat roles:** System prompt as `system` role, case input as `user` role
3. **Few-shot as conversation turns:** Examples as separate user/assistant message pairs
4. **Qwen3.5 thinking suppression:** Try `apply_chat_template` with `enable_thinking=False`
5. **System names:** Use descriptive names like `qwen3_4b_unit_dsl_zero_shot`

---

*End of V0.5 Qwen Smoke Root Cause Audit.*
