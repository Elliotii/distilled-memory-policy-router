# V0.5c Qwen3.5 JSON LoRA 250 Dev Eval Report

**Date:** 2026-06-03  
**Context:** 5.9-C — Qwen3.5 Unit JSON LoRA 250 training + dev eval  

---

## 1. Structural Metrics

| Metric | Qwen3.5 250 | Qwen3.5 125 | Δ |
|--------|:-----------:|:-----------:|:--:|
| Parse success | **90.0%** ⚠ | 98.0% | −8.0pp |
| Invalid memory ID | 0.0% | 0.0% | — |
| Invalid unit/span | 0.0% | 0.0% | — |
| Invalid target | 2.7% | 0.0% | +2.7pp |
| Avg output chars | 131.9 | 116.4 | +15.5 |
| Repair cost | 2.37 | 2.07 | +0.30 |

**10 parse failures:**
- 7 cases: `"target":"skip"` in store array → missing `skip` key + invalid target
- 2 cases: truncated/invalid JSON
- 1 case: missing unit assignment

## 2. Semantic Metrics

| Metric | Qwen3.5 250 | Qwen3.5 125 | Δ |
|--------|:-----------:|:-----------:|:--:|
| Exact | **17.0%** ⚠ | 30.0% | −13.0pp |
| READ F1 | 0.892 | 0.907 | −0.015 |
| STORE unit F1 | **0.913** ✅ | 0.891 | +0.022 |
| Target accuracy | **73.1%** ✅✅ | 65.6% | +7.5pp |
| SKIP F1 | 0.623 | 0.644 | −0.021 |
| False store | 4.9% | 2.2% | +2.7pp |
| Irrelevant read | 18.2% | 12.3% | +5.9pp |
| Sensitive store | 66.7% | 33.3% | +33.4pp |

## 3. Key Finding: Parse Regression

**Qwen3.5 250 shows an unexpected parse regression (98% → 90%).** The primary failure mode (7/10 cases) is `"target":"skip"` — the model puts SKIP units into the store array with `"target":"skip"` instead of using the `"skip":["uN"]` field. This is a systematic error not seen in Qwen3-4B (which maintained 100% parse across all sizes).

Root cause analysis:
- The training data is clean (100% valid JSON, no `"target":"skip"` patterns)
- The model learned to use `"target":"skip"` as a confused shortcut for the skip mechanism
- This pattern did NOT appear at 125 cases (98% parse, only 2 unrelated failures)
- With 250 cases, the model may be overfitting to store patterns and confusing the schema

Impact on exact match:
- 10 parse failures directly remove 10 cases from exact match consideration
- Among the 90 parseable cases, exact is 17/90 = 18.9% (vs 30% overall at 125)
- The exact drop is a MIX of parse failures (mechanical) and genuine semantic decline

## 4. Positive Signal: Target Accuracy

Despite the parse regression, target accuracy improved strongly:
- 65.6% → 73.1% (+7.5pp)
- This is now above Qwen3-4B JSON LoRA 500 gold level (67.3%)
- The model IS learning target classification effectively

STORE F1 also improved:
- 0.891 → 0.913 (+0.022)
- Recovery from initial deficit at 125

## 5. Sensitive Store Worsening

Sensitive store increased from 33.3% (125) to 66.7% (250). This matches the Qwen3-4B pattern (33.3% → 66.7% → 66.7%) and reflects the data distribution — more STORE examples lead to more frequent STORE of sensitive content. This is a known data limitation, not a Qwen3.5-specific issue.

---

*End of V0.5c Qwen3.5 JSON LoRA 250 Dev Eval Report.*
