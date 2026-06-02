# V0.5 LoRA v0.5 Final Result Decision

**Date:** 2026-06-02  
**Context:** 5.5-G — final locked-gold evaluation  

---

## Gold Eval Result

| Metric | LoRA 500 Gold | LoRA 500 Dev | Delta |
|--------|:------------:|:------------:|:-----:|
| Exact | 16% | 24% | -8pp |
| STORE F1 | 0.946 | 0.962 | -0.016 |
| Target acc | 47.5% | 54.1% | -6.6pp |
| SKIP F1 | 0.718 | 0.773 | -0.055 |
| READ F1 | 0.923 | 0.908 | +0.015 |
| Sensitive | 50% (6 cases) | 6 cases | = |

## Baseline Comparison

| System | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | **42%** | **0.963** | **79.1%** | **0.851** | **0%** |
| Qwen3.5 DSL fs | 36% | 0.959 | 77.6% | 0.795 | 0% |
| Qwen3-4B JSON fs | 26% | 0.923 | 57.5% | 0.766 | 0% |
| Qwen3-4B DSL fs | 7% | 0.850 | 60.5% | 0.422 | 0% |
| **LoRA 500** | 16% | 0.946 | 47.5% | 0.718 | 50% |

## Sensitive Failures

**6 genuine failures, including a credit card number.** Slack handle, home address, personal email, phone, driver's license, credit card — all stored as `user_profile`. Model treats all personal-looking info as a user preference. This is a safety-critical failure.

## Per-Target Accuracy

| Target | Gold | Accuracy |
|--------|:----:|:--------:|
| user_profile | 8/8 | 100% |
| task_state | 42/65 | 64.6% |
| project_memory | 9/15 | 60.0% |
| repo_memory | 17/34 | 50.0% |
| service_memory | 20/80 | **25.0%** |

Service memory (largest gold class at 80 units) has only 25% accuracy. Model confuses svc→task on ~40 cases.

## Decision: Result D — Not competitive

LoRA 500 improves over Qwen3-4B DSL few-shot on STORE/SKIP but:
- Does NOT beat Qwen3.5 prompting on any metric
- Does NOT beat Qwen3-4B JSON few-shot on most metrics
- Has safety-critical sensitive failures (credit card stored as user_profile)
- Has dismal service_memory target accuracy (25%)
- Best prompting baseline (Qwen3.5 JSON fs) remains superior across all dimensions

**v0.5 LoRA demonstrates that SFT training on 500 cases provides marginal STORE/SKIP improvement but fails on target classification and safety.** More/balanced data or target-focused training needed for v0.5b.

## Honest Assessment

- ✅ STORE/SKIP decision improves with supervised training
- ✅ Learning curve is valid and well-documented
- ❌ Target accuracy plateaus below prompting baselines
- ❌ Sensitive handling degrades with training (stores contacts as preferences)
- ❌ Service memory is the hardest target to learn
- ❌ QLoRA rank-8 insufficient for fine-grained target distinction
- ✅ Qwen3.5 remains the strongest model for this task (even few-shot only)

---

*End of V0.5 LoRA v0.5 Final Result Decision.*
