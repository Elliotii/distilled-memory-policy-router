# V0.5 Final Claims and Limitations

**Date:** 2026-06-02  

---

## Allowed Claims

✅ **Built an end-to-end memory-router evaluation pipeline.** Created 700-case data split (500 train, 100 dev, 100 locked gold) with leakage protection, deterministic baselines, and multi-model prompting comparisons.

✅ **Compared Unit DSL and Unit JSON interfaces.** Evaluated both formats across Qwen3-4B and Qwen3.5 under zero-shot and few-shot conditions. Unit JSON showed better generalization.

✅ **Established Qwen3/Qwen3.5 prompting baselines.** Characterized zero/few-shot performance on dev and locked gold. Qwen3.5 JSON few-shot (42% exact, 0.963 STORE F1) is the strongest prompting system.

✅ **Ran Qwen3-4B QLoRA learning curve.** Trained on 125→250→500 cases with controlled hyperparameters. STORE/SKIP/READ decisions improve with more data.

✅ **LoRA improves action-level routing.** 500-case LoRA achieves 0.946 STORE F1 on gold vs 0.850 for same-model DSL few-shot (+0.096). Demonstrates supervised training helps STORE/SKIP/READ decisions.

✅ **Documented target/safety bottlenecks.** Per-target accuracy reveals service_memory (25%) as the hardest class. Sensitive content stored as user_profile.

---

## Forbidden Claims

❌ **Do not claim production-safe.** Model stores credit cards, emails, phones, addresses as user_profile.

❌ **Do not claim LoRA beats Qwen3.5.** Qwen3.5 JSON few-shot outperforms LoRA 500 across all metrics.

❌ **Do not claim target routing solved.** Target accuracy at 47.5% on gold remains below prompting baselines.

❌ **Do not claim sensitive handling solved.** 6 genuine sensitive failures on locked gold including credit card.

❌ **Do not claim Unit DSL is universally superior.** Unit JSON few-shot outperformed Unit DSL few-shot on gold (42% vs 36% exact).

❌ **Do not claim 500 cases are enough.** Target accuracy plateaued at 54% on dev, 47.5% on gold. More data needed.

---

*End of V0.5 Final Claims and Limitations.*
