# V0.5b Final Results

**Date:** 2026-06-02  

---

## Locked-Gold Comparison

| System | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | **42%** | **0.963** | **79.1%** | **0.851** | **0** |
| Qwen3.5 DSL fs | 36% | 0.959 | 77.6% | 0.795 | **0** |
| **JSON LoRA 500** | **31%** | 0.941 | 67.3% | 0.706 | 6 fails |
| Qwen3-4B JSON fs | 26% | 0.923 | 57.5% | 0.766 | **0** |
| DSL LoRA 500 | 16% | 0.946 | 47.5% | 0.718 | 6 fails |
| Qwen3-4B DSL fs | 7% | 0.850 | 60.5% | 0.422 | **0** |

## Interface Ablation: DSL 500 vs JSON 500 (Gold)

| Metric | DSL 500 | JSON 500 | Δ |
|--------|:-------:|:--------:|:--:|
| Exact | 16% | **31%** | **+15pp** |
| Target acc | 47.5% | **67.3%** | **+19.8pp** |

## JSON Dev Learning Curve

| | 125 | 250 | 500 |
|---|:---:|:---:|:---:|
| Exact | 11% | 20% | 34% |
| STORE F1 | 0.910 | 0.947 | 0.958 |
| Target acc | 55.7% | 63.8% | 68.5% |

## Verdict

**Result B:** Unit JSON LoRA improves target routing over DSL and Qwen3-4B prompting, but trails Qwen3.5. Safety unsolved.

**Unit JSON is now the preferred training interface.**

## Full Reports

See `reports/v05b/` for complete documentation.

---

*End of V0.5b Final Results.*
