# V0.5b Qwen3-4B Unit JSON LoRA 500 Dev vs Gold Delta Report

**Date:** 2026-06-02  
**Context:** 5.7-E — generalization analysis  

---

## 1. Dev → Gold Comparison

| Metric | Dev | Gold | Δ | Interpretation |
|--------|:---:|:----:|:--:|----------------|
| Parse success | 100.0% | 100.0% | 0 | Perfect both splits ✅ |
| Exact match | 34.0% | 31.0% | **-3pp** | Small gap ← good generalization |
| READ F1 | 0.902 | **0.919** | +0.017 | Slightly better on gold |
| STORE unit F1 | 0.958 | 0.941 | -0.017 | Small gap |
| Target accuracy | 68.5% | 67.3% | **-1.2pp** | Very small gap ✅✅ |
| SKIP F1 | 0.753 | 0.706 | -0.047 | Moderate gap |
| False store rate | 6.5% | 6.6% | +0.1pp | Nearly identical |
| Irrelevant read rate | 15.9% | 14.2% | -1.7pp | Slightly better on gold |
| Sensitive store (eval) | 66.7% | 75.0% | +8.3pp | Worse on gold |
| Sensitive (genuine) | 1/4 = 25% | 6/10 = 60% | More on gold | Gold has more sensitive cases |

## 2. Answers

### What generalized?
- **Target accuracy: -1.2pp gap.** The model's target classification transfers almost perfectly from dev to gold. This is the strongest generalization signal.
- **Parse: 100% on both.** JSON format is robust across domains.
- **Exact: -3pp.** Close match — the model is consistent.
- **READ F1: +0.017 on gold.** Slightly better on gold's memory selection.

### What dropped?
- **SKIP F1: -0.047.** Gold has different skip patterns than dev.
- **Sensitive store: more on gold.** Gold has 6 true sensitive failures vs dev's 1 — gold intentionally includes hard sensitive cases.

### Was dev overly optimistic?
**No. Dev estimates were accurate.** Target accuracy (68.5% dev → 67.3% gold) and exact (34% → 31%) are within tight ranges. Dev correctly predicted that JSON would beat DSL on target classification.

### Does the target accuracy gain over DSL persist on gold?
**Yes, emphatically.** JSON 500 gets 67.3% target accuracy on gold vs DSL 500's 47.5% — a **+19.8pp margin**. The dev-estimated advantage (+14.4pp) actually grew on gold.

### Does the safety issue persist or worsen?
**Persists at similar severity.** 6 sensitive failures on gold (same count as DSL 500 on gold). Gold has more sensitive content than dev (10 sensitive units vs 4 on dev). Safety is not solved by JSON format.

## 3. Comparison: Dev→Gold Gap by System

| System | Dev Target | Gold Target | Gap |
|--------|:---------:|:----------:|:---:|
| **JSON LoRA 500** | 68.5% | 67.3% | **-1.2pp** |
| DSL LoRA 500 | 54.1% | 47.5% | -6.6pp |
| Qwen3-4B JSON fs | 67.1% | 57.5% | -9.6pp |

JSON 500 has the tightest dev→gold correlation of any system. The model's behavior is highly predictable — a sign of robust learning rather than overfitting to dev.

---

*End of V0.5b Dev vs Gold Delta Report.*
