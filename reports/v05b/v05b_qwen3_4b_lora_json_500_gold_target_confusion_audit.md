# V0.5b Qwen3-4B Unit JSON LoRA 500 Gold Target Confusion Audit

**Date:** 2026-06-02  
**Context:** 5.7-E — locked-gold target confusion analysis  

---

## 1. Per-Target Accuracy (Gold)

| Target | Correct/Total | Accuracy | Dev Accuracy | Δ |
|--------|:---:|:--------:|:-----------:|:--:|
| user_profile | 7/9 | 77.8% | 91.7% | -13.9pp |
| project_memory | 12/15 | 80.0% | 57.7% | **+22.3pp** |
| repo_memory | 17/34 | 50.0% | 43.2% | +6.8pp |
| service_memory | 56/80 | **70.0%** | 91.5% | -21.5pp |
| task_state | 42/61 | 68.9% | 58.6% | +10.3pp |
| **Overall** | **134/199** | **67.3%** | 68.5% | -1.2pp |

## 2. Confusion Matrix (Gold)

| Gold \ Pred | user_profile | project_memory | repo_memory | service_memory | task_state |
|-------------|:---:|:---:|:---:|:---:|:---:|
| user_profile (9) | **7** | 1 | 0 | 0 | 1 |
| project_memory (15) | 0 | **12** | 0 | 0 | 3 |
| repo_memory (34) | 1 | 5 | **17** | 5 | 6 |
| service_memory (80) | 0 | 9 | 2 | **56** | 13 |
| task_state (61) | 1 | 5 | 1 | 12 | **42** |

Only correctly identified STORE units counted (gold STORE ∩ predicted STORE).

## 3. Key Analyses

### Q1: Did JSON fix service_memory vs task_state on gold?

**Partially.** On dev, service→task_state confusion was reduced from 42% to 4% (excellent). On gold, service→task_state is 13/80 = 16.3% — higher than dev but dramatically lower than DSL 500 (where service_memory was only ~25% accurate overall).

DSL 500 on gold: service_memory accuracy ~25%
JSON 500 on gold: service_memory accuracy **70.0%**

**JSON improves service_memory accuracy by ~45pp over DSL on gold.** This is a qualitative improvement — the service/task distinction that DSL could not learn is substantially learned in JSON format.

### Q2: Which target remains weakest?

**repo_memory: 50.0% accurate.** Confused with task_state (6), service_memory (5), and project_memory (5). repo is inherently ambiguous — code paths, config files, and repo conventions can overlap with other targets. Only 37 repo examples in 500 training cases.

### Q3: Did repo_memory remain a weakness?

**Yes.** Accuracy only improved from 43.2% (dev) to 50.0% (gold) — still the lowest. Gold has 34 repo_memory labels vs dev's 37, but the distribution may be harder.

### Q4: Did user_profile overuse remain a safety risk?

**Reduced but present.** On gold, user_profile is predicted correctly 7/9 times. But 3 sensitive failures were stored as user_profile (address, 2 phones). The model correctly identifies user_profile content but cannot distinguish "legitimate user profile" from "sensitive PII."

## 4. Comparison: Service Memory Accuracy

| System | Dev | Gold |
|--------|:---:|:----:|
| JSON LoRA 500 | 91.5% | **70.0%** |
| DSL LoRA 500 | — | ~25% (estimated) |
| Qwen3-4B JSON fs | — | ~57.5% (overall target acc) |

**JSON LoRA 500 achieves the highest service_memory accuracy of any trained system.** The JSON format makes the service/task distinction learnable.

## 5. Task State Overuse Analysis

At 125, the model over-predicted task_state (30 service units → task_state). At 500, this reversed: task_state→service_memory is 12/61 (19.7%) while service→task_state is 13/80 (16.3%). The bias has balanced — the model no longer defaults to one class.

---

*End of V0.5b Gold Target Confusion Audit.*
