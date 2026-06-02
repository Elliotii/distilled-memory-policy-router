# V0.5 Qwen3-4B LoRA 250 Postmortem

**Date:** 2026-06-02  

## 250 Result Summary

| Metric | 250 LoRA | 125 LoRA | Few-shot DSL |
|--------|:--------:|:--------:|:------------:|
| Parse success | ~85% | 75% | 96% |
| Exact | 14% | 12% | 22% |
| STORE F1 | **0.944** ✅ | 0.867 | 0.936 |
| Target acc | 55.7% | 60.0% | 71.1% |
| SKIP F1 | 0.684 | 0.492 | 0.690 |
| Sensitive (actual) | 3 cases | ~3 cases | ~3 cases |

## Why STORE F1 Improved But Target Accuracy Dropped

Train250 eval: target acc 50.4% (LOWER than dev 55.7%). Target confusion audit shows model defaults to `task_state` when uncertain (most common training class, 32% of units). The model learned STORE/SKIP boundary but not fine-grained target classification.

This is a class-imbalance effect: with only 250 cases, the model hasn't seen enough examples of rarer targets (project_memory, user_profile, repo_memory) to distinguish them confidently.

## Target Confusion

Top confusions: service_memory→task_state (23), project_memory→task_state (13), repo_memory→task_state (13). Model overuses task_state.

## Sensitive Store

3 genuine failures (phone, 2 emails). Eval_runner tag-based metric (66.7%) inflated by false positives.

## Train250 vs Dev

Train STORE F1 (0.952) close to dev (0.944) — good generalization. Train target acc (50.4%) lower than dev (55.7%) — model underfitting targets, not overfitting.

## Decision

**Option A: Proceed to 500 unchanged.** STORE F1 beats few-shot. Target accuracy needs more data (500 doubles training examples, improving target distribution learning). Sensitive store is 3 genuine cases — manageable.

---

*End of V0.5 Qwen3-4B LoRA 250 Postmortem.*
