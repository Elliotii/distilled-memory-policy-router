# V0.5 Qwen3-4B LoRA 500 Gold Readiness Decision

**Date:** 2026-06-02  

## Decision: Option A — Ready for locked-gold final eval

## Evidence

### STORE/SKIP: Excellent
STORE F1 0.962 (dev), 0.977 (train). Model reliably decides WHAT to store/skip. Matches best prompting baselines.

### Target Classification: Known Ceiling
Target acc 54.1% (dev), 56.7% (train). Per-target accuracy: user_profile 100%, task_state 65%, service_memory 47%, repo_memory 41%, project_memory 42%. Model defaults to task_state when uncertain; svc→task confusion is the dominant error (30 cases). 

This ceiling is not overfitting — train target acc is only +2.6pp above dev. More of the same data won't help. Target-balanced training is a future ablation.

### Sensitive: 6 Genuine Failures
Phone, emails, address, Slack handle stored as user_profile or task_state. Pattern: model over-applies user_profile to contact info. Documented limitation.

### Learning Curve Complete
125→250→500 shows clear improvement in STORE/SKIP/READ decisions. Target accuracy plateaus at 54%. The curve is honest and complete.

## Caveats for Gold Evaluation

1. Target accuracy will likely be ~50-55% on gold, similar to dev
2. Sensitive failures will likely persist (user_profile over-application)
3. STORE F1 should remain competitive with prompting baselines
4. Per-target breakdown on gold will guide future ablations

## Next Step

**Context 5.5-F: Final locked-gold evaluation of Qwen3-4B LoRA 500.** Evaluate against all gold baselines. Report learning curve. Document where LoRA beats/falls short.

---

*End of V0.5 Qwen3-4B LoRA 500 Gold Readiness Decision.*
