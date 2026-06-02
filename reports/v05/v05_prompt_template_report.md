# V0.5 Prompt Template Report

**Date:** 2026-06-02  
**Context:** 5.4-B — v0.5 prompt template creation and smoke test  

---

## 1. Prompt Files Created

| File | Purpose | Size |
|------|---------|:----:|
| `prompts/v05/unit_dsl_zero_shot.txt` | Unit DSL zero-shot | 1.9 KB |
| `prompts/v05/unit_dsl_fewshot.txt` | Unit DSL few-shot (5 examples) | 5.4 KB |
| `prompts/v05/unit_json_zero_shot.txt` | Unit JSON zero-shot | 1.9 KB |
| `prompts/v05/unit_json_fewshot.txt` | Unit JSON few-shot (5 examples) | 5.6 KB |

## 2. Prompt Structure

All four prompts follow the same structure:
1. **Role:** "You are a memory policy router for coding-agent contexts."
2. **Task:** Decide which memories to read, which units to store/skip.
3. **Output format:** DSL or JSON specification.
4. **Legal targets:** 5 targets with definitions.
5. **Rules:** 7 rules covering READ, STORE, SKIP, coverage, IDs, and output format.
6. **Few-shot examples** (few-shot variants only): 5 examples from train-pool.

## 3. Prompt Differences

| Aspect | DSL | JSON |
|--------|-----|------|
| Output format | Line-based (`READ m1\nSTORE target u1\nSKIP u2`) | JSON object (`{"read":[],"store":[],"skip":[]}`) |
| Verbosity | Concise | Slightly more verbose (schema explanation) |
| Parsing | Line-by-line keyword parsing | JSON parsing |
| Few-shot | 5 DSL examples | 5 JSON examples (same cases, different format) |

## 4. Few-Shot Example Case IDs

All 5 few-shot examples are from the train-pool (`data/v05/batches/v05_batch500_corrected_cases.jsonl`):

| # | Case ID | Category | Shape |
|---|---------|----------|-------|
| 1 | `v05_sample_0001` | READ-only + stale memory | READ-only |
| 2 | `v05_sample_0005` | STORE/SKIP-only + sensitive + repo_vs_service | STORE/SKIP-only |
| 3 | `v05_sample_0009` | READ+STORE joint | READ+STORE joint |
| 4 | `v05_sample_0010` | Sensitive boundary + stale memory | READ+STORE joint |
| 5 | `v05_sample_0004` | Service vs task boundary | STORE/SKIP-only |

**Confirmation:** No dev or gold cases used as few-shot examples. ✅

## 5. Known Issues from Smoke Test

### Issue 1: Qwen3-4B zero-shot DSL produces empty defaults

Qwen3-4B zero-shot outputs `READ NONE\nSTORE NONE\nSKIP NONE` for all cases. The model doesn't seem to understand the task format without examples.

### Issue 2: Qwen3-4B few-shot DSL produces wrong unit IDs

Few-shot outputs use hardcoded patterns from examples (u4, project_memory, repo_memory, service_memory) rather than reading the actual case input. The model template-matches instead of reasoning.

### Issue 3: Qwen3.5 produces verbose thinking prose

All Qwen3.5 outputs (~2000+ chars) are thinking/analysis text rather than DSL or JSON. The model seems to engage a "thinking" mode and doesn't output the requested format.

### Issue 4: Qwen3-4B JSON outputs empty objects

JSON outputs are `{"read": [], "store": [], "skip": []}` for all cases.

## 6. Root Causes (Hypothesis)

1. **Single-message prompt format:** The current runner sends the entire prompt as a single user message. Qwen models may expect system + user role separation via chat template.
2. **Thinking mode:** Qwen3.5 has a thinking mode that is not being disabled. The model may need `enable_thinking=False` or a different approach.
3. **Few-shot format mismatch:** Few-shot examples are embedded in the user prompt rather than as separate conversation turns.
4. **Prompt may need structured input format:** The current approach blends system instructions, examples, and case input into one message.

## 7. Recommended Fixes (for future context)

1. **Use chat template properly:** Send system prompt as `system` role, case input as `user` role.
2. **Suppress thinking in Qwen3.5:** Investigate `enable_thinking` support or use `--chat-template` flag.
3. **Separate few-shot as conversation turns:** Few-shot examples as separate user/assistant pairs before the actual input.
4. **Test structured format on 5-case smoke before full dev baseline.**

## 8. Known Risks

- If prompt fixes don't work, Qwen3-4B and Qwen3.5 may need different prompt strategies
- Qwen3.5 may fundamentally be unsuitable for DSL output without fine-tuning
- Prompt iteration should be done on dev smoke only, not on locked gold
- The SFT few-shot format (system + user + assistant message format) may be the correct format for all models

---

*End of V0.5 Prompt Template Report.*
