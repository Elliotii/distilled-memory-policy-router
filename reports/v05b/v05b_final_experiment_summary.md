# V0.5b Final Experiment Summary

**Date:** 2026-06-02  
**Status:** Complete  

---

## 1. Unit JSON LoRA Dev Learning Curve

| Metric | 125 | 250 | 500 |
|--------|:---:|:---:|:---:|
| Parse success | 100% | 100% | 100% |
| Exact match | 11% | 20% | 34% |
| STORE F1 | 0.910 | 0.947 | 0.958 |
| Target accuracy | 55.7% | 63.8% | 68.5% |
| SKIP F1 | 0.535 | 0.747 | 0.753 |
| False store | 9.5% | 4.6% | 6.5% |

## 2. Locked-Gold Final Comparison

| System | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | **42%** | **0.963** | **79.1%** | **0.851** | **0** |
| Qwen3.5 DSL fs | 36% | 0.959 | 77.6% | 0.795 | **0** |
| **JSON LoRA 500** | **31%** | 0.941 | 67.3% | 0.706 | 6 fails |
| Qwen3-4B JSON fs | 26% | 0.923 | 57.5% | 0.766 | **0** |
| DSL LoRA 500 | 16% | 0.946 | 47.5% | 0.718 | 6 fails |
| Qwen3-4B DSL fs | 7% | 0.850 | 60.5% | 0.422 | **0** |

## 3. Interface Ablation: DSL 500 vs JSON 500 (Gold)

| Metric | DSL 500 | JSON 500 | Δ |
|--------|:-------:|:--------:|:--:|
| Exact | 16% | **31%** | **+15pp** |
| STORE F1 | **0.946** | 0.941 | -0.005 |
| Target acc | 47.5% | **67.3%** | **+19.8pp** |
| SKIP F1 | 0.718 | 0.706 | -0.012 |
| Sensitive | 6 | 6 | tied |
| Parse (dev) | 86-99% | **100%** | fixed |

## 4. JSON 500 vs Qwen3-4B JSON Few-Shot (Gold)

| Metric | JSON fs | JSON 500 | Δ |
|--------|:-------:|:--------:|:--:|
| Exact | 26% | **31%** | **+5pp** |
| STORE F1 | 0.923 | **0.941** | +0.018 |
| Target acc | 57.5% | **67.3%** | **+9.8pp** |
| SKIP F1 | **0.766** | 0.706 | -0.060 |
| Sensitive | **0** | 6 | -6 |

## 5. Dev→Gold Generalization (JSON 500)

| Metric | Dev | Gold | Δ |
|--------|:---:|:----:|:--:|
| Exact | 34% | 31% | -3pp |
| Target acc | 68.5% | 67.3% | **-1.2pp** |
| STORE F1 | 0.958 | 0.941 | -0.017 |
| SKIP F1 | 0.753 | 0.706 | -0.047 |

## 6. Training Convergence

| System | Final Eval Loss | Token Acc |
|--------|:---------------:|:---------:|
| JSON 125 | 1.300 | 72.6% |
| JSON 250 | 0.608 | 86.5% |
| JSON 500 | 0.544 | 87.2% |
| DSL 500 | 0.62 | — |

## 7. Final Verdict

**Result B:** Unit JSON LoRA improves target routing over DSL LoRA and Qwen3-4B JSON few-shot, but still trails Qwen3.5 JSON few-shot. Safety remains unsolved.

**Unit JSON is now the preferred training interface for all future work.**

---

*End of V0.5b Final Experiment Summary.*
