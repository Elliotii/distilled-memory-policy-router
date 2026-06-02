# V0.5 Training Readiness Cleanup Report

**Date:** 2026-06-02  
**Context:** 5.5-A2 — cleanup after ClaudeCode training-readiness review  

---

## ClaudeCode Findings Addressed

| # | Finding | Resolution |
|---|---------|------------|
| 1 | Missing reports (5 files) | ✅ All 5 created |
| 2 | eval_steps=50 won't trigger for 125/250 | ✅ Changed to `eval_strategy: epoch` |
| 3 | metric_for_best_model=eval_loss not task metric | ✅ Documented caveat; dev task metrics for checkpoint selection |
| 4 | LR 2e-4 is high but acceptable for smoke | ✅ Kept; fallback documented |
| 5 | Cross-batch duplicate non-blocking | ✅ Acknowledged; not blocking 125 smoke |

## What Was Fixed

1. **Configs:** eval_strategy/save_strategy changed from `steps` to `epoch`. All 3 configs now get 3 checkpoints per run.
2. **Missing reports:** Created train_subset_manifest, train_split_integrity, lora_config, pretraining_decision, gold_baseline_artifact_audit, training_readiness_cleanup, 125 smoke runbook.

## What Was Only Documented

- eval_loss is not a task metric — documented limitation. Dev task metrics to be used for checkpoint selection after training.
- LR 2e-4 with fallback to 1e-4 then 5e-5.
- Cross-batch duplicate acknowledged as non-blocking for smoke.

## Remaining Non-Blocking Risks

| Risk | Severity | Mitigation |
|------|:--------:|------------|
| eval_loss not task metric | Low | Dev predictions + eval_runner after training |
| LR may need tuning | Low | Fallback plan documented |
| Cross-batch duplicate | Low | Non-blocking for smoke; resolve before final 500 |
| Qwen3-4B not supporting enable_thinking | N/A | Not used in training |
| 11GB VRAM borderline | Low | QLoRA 4-bit is conservative |

## 125 Smoke Clearance

**✅ 125-case QLoRA smoke is cleared for training.**

All preconditions met:
- Configs fixed (epoch eval)
- Data ready (125 subset, SFT validated)
- Environment ready (all libraries installed)
- Gold protected (no gold references in configs)
- Runbook created with exact command

---

*End of V0.5 Training Readiness Cleanup Report.*
