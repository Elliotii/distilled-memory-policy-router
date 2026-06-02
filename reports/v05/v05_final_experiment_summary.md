# V0.5 Final Experiment Summary

**Date:** 2026-06-02  
**Context:** 5.6-A — final v0.5 result consolidation  

---

## Dev Learning Curve (Qwen3-4B Unit DSL QLoRA)

| Checkpoint | Exact | READ F1 | STORE F1 | Target Acc | SKIP F1 |
|-----------:|:-----:|:-------:|:--------:|:----------:|:-------:|
| 125-case | 12% | 0.822 | 0.867 | 60.0% | 0.492 |
| 250-case | 14% | 0.900 | 0.944 | 55.7% | 0.684 |
| 500-case | 24% | 0.908 | 0.962 | 54.1% | 0.773 |

STORE/SKIP/READ improve with data. Target accuracy plateaus. Sensitive: 6-10 genuine failures.

## Locked Gold Comparison (All Systems)

| System | Exact | READ F1 | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:-------:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON few-shot | **42%** | 0.911 | **0.963** | **79.1%** | **0.851** | **0%** |
| Qwen3.5 DSL few-shot | 36% | 0.901 | 0.959 | 77.6% | 0.795 | 0% |
| Qwen3-4B JSON few-shot | 26% | **0.936** | 0.923 | 57.5% | 0.766 | 0% |
| Qwen3-4B DSL few-shot | 7% | 0.882 | 0.850 | 60.5% | 0.422 | 0% |
| **LoRA 500** | 16% | 0.923 | 0.946 | 47.5% | 0.718 | 50% |

## Dev vs Gold Delta (LoRA 500)

| Metric | Dev | Gold | Delta |
|--------|:---:|:----:|:-----:|
| Exact | 24% | 16% | -8pp |
| STORE F1 | 0.962 | 0.946 | -0.016 |
| Target acc | 54.1% | 47.5% | -6.6pp |
| SKIP F1 | 0.773 | 0.718 | -0.055 |

Moderate generalization gap. Gold is harder than dev (includes gold_hard boundary cases).

## Per-Target Accuracy (LoRA 500 on Gold)

| Target | Correct/Total | Accuracy |
|--------|:------------:|:--------:|
| user_profile | 8/8 | 100% |
| task_state | 42/65 | 64.6% |
| project_memory | 9/15 | 60.0% |
| repo_memory | 17/34 | 50.0% |
| service_memory | 20/80 | **25.0%** |

## Strength/Weakness Summary

| Dimension | LoRA vs Qwen3-4B DSL fs | LoRA vs Best |
|-----------|:-----------------------:|:------------:|
| READ | ✅ +0.041 | Comparable |
| STORE | ✅ +0.096 | ❌ -0.017 |
| SKIP | ✅ +0.296 | ❌ -0.133 |
| Target accuracy | ❌ -13.0pp | ❌ -31.6pp |
| Sensitive safety | ❌ Worse | ❌ Much worse |

## Final Verdict

**Result D: Not competitive overall.** LoRA improves action-level routing over same-model DSL prompting. But target classification and safety remain serious issues. Qwen3.5 JSON few-shot is the strongest system across all dimensions. v0.5 is a successful diagnostic experiment.

---

*End of V0.5 Final Experiment Summary.*
