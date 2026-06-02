# V0.5 Qwen Smoke Model Comparison

**Date:** 2026-06-02  
**Context:** 5.4-B — Qwen3-4B vs Qwen3.5 smoke comparison  

---

## 1. Qwen3 vs Qwen3.5 Smoke Comparison

### 1.1 Parse Stability

| Metric | Qwen3-4B | Qwen3.5 |
|--------|:--------:|:-------:|
| DSL parse success | 0% | 0% |
| JSON parse success | 0% | 0% |
| Output format correct | No (empty/wrong IDs) | No (prose) |
| Structure recognizable | Yes (DSL keywords present) | No (free-form prose) |

**Neither model produces usable outputs under current prompt templates.**

### 1.2 Latency

| Interface | Qwen3-4B | Qwen3.5 | Ratio |
|-----------|:--------:|:-------:|:-----:|
| DSL zero-shot | 370ms | 19,900ms | 54× |
| DSL few-shot | 870ms | 19,600ms | 23× |
| JSON zero-shot | 580ms | 14,900ms | 26× |
| JSON few-shot | 690ms | 19,800ms | 29× |

**Qwen3-4B is 23-54× faster than Qwen3.5 for this task.** Qwen3.5's latency is dominated by verbose thinking output generation.

### 1.3 Output Format Issues

| Issue | Qwen3-4B | Qwen3.5 |
|-------|:--------:|:-------:|
| Empty/default output | ✅ (zero-shot) | ❌ |
| Wrong unit IDs (few-shot) | ✅ (u4 doesn't exist) | ❌ |
| Verbose prose instead of DSL | ❌ | ✅ (all modes) |
| JSON parseable | ✅ (valid JSON, empty) | ❌ |
| Thinking/analysis text | ❌ | ✅ (all modes) |

### 1.4 VRAM Usage

| Metric | Qwen3-4B | Qwen3.5 |
|--------|:--------:|:-------:|
| Model load VRAM | ~8 GB | ~9 GB |
| Peak VRAM during inference | ~9 GB | ~10 GB |
| Headroom (11 GB total) | 2 GB | 1 GB |
| Fits comfortably | ✅ | ⚠ Borderline |

## 2. Whether Qwen3.5 Should Proceed to Full Dev

**No — not in current state.** Qwen3.5 produces unusable outputs (0% parse success, verbose prose) under current prompt templates. Before Qwen3.5 can be evaluated:

1. Fix prompt template to suppress thinking mode
2. Test with structured system+user message format
3. Re-run 5-case smoke
4. If parse success > 0%, proceed to full dev

**Qwen3-4B should also not proceed to full dev without prompt fixes.** While Qwen3-4B produces structurally valid DSL (`READ NONE / STORE NONE / SKIP NONE`), the content is empty and few-shot outputs use wrong unit IDs.

## 3. What Blocked Qwen3.5

| Blocker | Detail |
|---------|--------|
| Thinking mode not suppressed | Model outputs ~2000 chars of analysis before (or instead of) DSL |
| Single-message prompt format | Prompt sent as one user message, not system+user |
| No chat template separation | Model may expect role-based message formatting |
| `enable_thinking` not available | The flag is not supported in this transformers/Qwen3.5 version |

## 4. Recommended Fix Sequence

### Step 1: Fix prompt format (both models)
- Use `apply_chat_template` with system + user roles
- Or send system prompt separately from user input
- This matches the SFT format the models may have been trained on

### Step 2: Fix Qwen3.5 thinking mode
- Investigate `enable_thinking` parameter availability
- Try `chat_template_kwargs={"enable_thinking": False}`
- Or add explicit instruction: "Do not think or analyze. Output only the requested format."

### Step 3: Fix few-shot format
- Embed few-shot examples as separate user/assistant conversation turns
- This gives the model proper context for the expected output format

### Step 4: Re-test 5-case smoke
- Run on same 5 dev cases
- Target: parse success > 80% for DSL, > 50% for JSON
- If met, proceed to full dev baseline

## 5. Fallback

If prompt fixes don't resolve Qwen3.5 issues:
- Qwen3-4B remains the primary baseline model
- Qwen3.5 comparison deferred until prompt issues are resolved
- LoRA training targets Qwen3-4B by default

---

*End of V0.5 Qwen Smoke Model Comparison.*
