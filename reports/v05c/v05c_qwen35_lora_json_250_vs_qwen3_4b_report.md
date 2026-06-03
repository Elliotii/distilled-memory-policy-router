# V0.5c Qwen3.5 vs Qwen3-4B JSON LoRA 250 Comparison

**Date:** 2026-06-03  
**Context:** 5.9-C  
**Split:** Dev only (100 cases)  

---

## 1. Head-to-Head: 250-Case

| Metric | Qwen3.5 250 | Qwen3-4B 250 | Δ (Qwen3.5 − Qwen3-4B) |
|--------|:-----------:|:------------:|:----------------------:|
| Parse success | 90.0% | **100.0%** | **−10.0pp ❌** |
| Exact | 17.0% | **20.0%** | −3.0pp |
| READ F1 | **0.892** | 0.884 | +0.008 |
| STORE unit F1 | 0.913 | **0.947** | −0.034 |
| **Target accuracy** | **73.1%** | 63.8% | **+9.3pp ✅✅** |
| SKIP F1 | 0.623 | **0.747** | −0.124 |
| False store | 4.9% | **4.6%** | +0.3pp |
| Irrelevant read | **18.2%** | 19.0% | −0.8pp |
| Sensitive store | 66.7% | 66.7% | 0.0pp |

## 2. Full Learning Curve Context

| Metric | Q3.5 125 | Q3.5 250 | Q3-4B 125 | Q3-4B 250 | Q3-4B 500 |
|--------|:--------:|:--------:|:---------:|:---------:|:---------:|
| Parse | 98.0% | 90.0% | 100% | 100% | 100% |
| Exact | 30.0% | 17.0% | 11% | 20% | 34% |
| READ F1 | 0.907 | 0.892 | 0.889 | 0.884 | 0.902 |
| STORE F1 | 0.891 | 0.913 | 0.910 | 0.947 | 0.958 |
| Target acc | 65.6% | **73.1%** | 55.7% | 63.8% | 68.5% |
| SKIP F1 | 0.644 | 0.623 | 0.535 | 0.747 | 0.753 |

## 3. Key Findings

1. **Qwen3.5 250 target accuracy (73.1%) exceeds Qwen3-4B 500 (68.5%).** Target routing is the experiment's primary metric, and Qwen3.5 achieves this with HALF the data.

2. **Qwen3.5 has a unique parse regression** — Qwen3-4B maintained 100% parse across all sizes. The `"target":"skip"` pattern suggests Qwen3.5 is more prone to schema confusion under QLoRA.

3. **Qwen3.5 STORE F1 lags Qwen3-4B** (0.913 vs 0.947) — consistent with the 125 result (0.891 vs 0.910). Qwen3.5 is less precise about WHICH units to store.

4. **Exact match is heavily depressed by parse failures.** 10 parse failures remove 10 exact match candidates. Among parseable cases, Qwen3.5 exact is 18.9% vs Qwen3-4B's 20.0% — roughly tied.

5. **Qwen3.5 training is 5x slower** than Qwen3-4B (1864s vs 367s for 250 cases).

## 4. Few-Shot Baseline Comparison

No Qwen3.5 few-shot dev baseline exists (few-shot was only run on gold). For reference:
- Qwen3.5 JSON few-shot gold: 42% exact, 0.963 STORE F1, 79.1% target
- Qwen3-4B JSON few-shot gold: 26% exact, 0.923 STORE F1, 57.5% target

Qwen3.5 LoRA 250's 73.1% target accuracy on dev is approaching Qwen3.5 few-shot gold's 79.1% — encouraging for 500.

---

*End of V0.5c Qwen3.5 vs Qwen3-4B JSON LoRA 250 Comparison.*
