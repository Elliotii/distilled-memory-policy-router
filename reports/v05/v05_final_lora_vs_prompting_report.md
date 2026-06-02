# V0.5 Final LoRA vs Prompting Report

**Date:** 2026-06-02  
**Split:** Locked gold only  

---

## Locked Gold Comparison

| System | Exact | READ F1 | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:-------:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | **42%** | 0.911 | **0.963** | **79.1%** | **0.851** | **0 failures** |
| Qwen3.5 DSL fs | 36% | 0.901 | 0.959 | 77.6% | 0.795 | 0 failures |
| Qwen3-4B JSON fs | 26% | **0.936** | 0.923 | 57.5% | 0.766 | 0 failures |
| Qwen3-4B LoRA 500 | 16% | 0.923 | 0.946 | 47.5% | 0.718 | 6 failures |
| Qwen3-4B DSL fs | 7% | 0.882 | 0.850 | 60.5% | 0.422 | 0 failures |

## Conclusion

- **LoRA beats Qwen3-4B DSL few-shot** on STORE F1 (+0.096) and SKIP F1 (+0.296). Action-level routing improves with supervised training.
- **LoRA does NOT beat Qwen3.5 JSON few-shot** on any metric. Qwen3.5 prompting is the strongest system.
- **LoRA is NOT production-safe.** 6 sensitive failures including credit card on locked gold.
- Qwen3.5 JSON few-shot (42% exact, 0% sensitive) is the recommended v0.5 baseline.

---

*End of V0.5 Final LoRA vs Prompting Report.*
