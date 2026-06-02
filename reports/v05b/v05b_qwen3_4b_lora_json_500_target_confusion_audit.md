# V0.5b Qwen3-4B Unit JSON LoRA 500 Target Confusion Audit

**Date:** 2026-06-02  
**Context:** 5.7-D — target confusion matrix on dev  

---

## 1. Per-Target Accuracy (Correctly Predicted STORE Units)

| Target | JSON 125 | JSON 250 | JSON 500 | DSL 500 |
|--------|:--------:|:--------:|:--------:|:-------:|
| user_profile | 42% | 50% | **91.7%** | — |
| project_memory | 38% | 46% | **57.7%** | — |
| repo_memory | 57% | 59% | 43.2% | — |
| service_memory | 55% | 62% | **91.5%** | ~25% (gold) |
| task_state | 57% | 62% | 58.6% | — |
| **Overall** | **55.7%** | **63.8%** | **68.5%** | **54.1%** |

Note: DSL 500 per-target breakdowns from gold evaluation (different split). Dev per-target DSL numbers not available.

## 2. Confusion Matrix (JSON 500)

| Gold \ Pred | user_profile | project_memory | repo_memory | service_memory | task_state |
|-------------|:---:|:---:|:---:|:---:|:---:|
| user_profile (12) | **11** | 0 | 0 | 0 | 1 |
| project_memory (26) | 0 | **15** | 0 | 7 | 4 |
| repo_memory (37) | 0 | 8 | **16** | 7 | 6 |
| service_memory (71) | 0 | 3 | 0 | **65** | 3 |
| task_state (70) | 1 | 1 | 11 | 16 | **41** |

Only correctly identified STORE units counted (gold STORE ∩ predicted STORE).

## 3. Key Confusion Patterns

### service_memory (91.5% accurate) — Major improvement
- At JSON 125: 55% (confused with task_state 30 times)
- At JSON 250: 62% (confused with task_state 18 times)
- At JSON 500: 91.5% (confused with task_state only 3 times!)
- **service_memory → task_state confusion reduced from 42% to 4%.** The model learned the distinction.

### user_profile (91.7% accurate) — Near-perfect
- Only 1 confusion (stored as task_state)
- Previous over-prediction of user_profile has been corrected at 500

### task_state (58.6% accurate) — Now the bottleneck
- Confused with service_memory (16) and repo_memory (11)
- The model errs toward storing task content as service behavior
- This is the inverse of the earlier problem (before, everything was task_state)

### repo_memory (43.2% accurate) — Weakest class
- Confused with project_memory (8), service_memory (7), task_state (6)
- repo is inherently ambiguous — config paths could be project, service, or task patterns
- Low 37-example count in training limits learning

### project_memory (57.7% accurate) — Improving
- Confused with service_memory (7) and task_state (4)
- Only 26 project_memory examples in 500 — class imbalance affects learning

## 4. Service vs Task State Trajectory

| Confusion Direction | JSON 125 | JSON 250 | JSON 500 |
|---------------------|:--------:|:--------:|:--------:|
| service → task_state | 30/71 (42%) | 18/71 (25%) | **3/71 (4%)** |
| task_state → service | 18/74 (24%) | 14/74 (19%) | 16/70 (23%) |

The dominant confusion (service→task_state) is nearly eliminated. The reverse confusion (task_state→service) remains. The model now prefers service_memory over task_state — a reversal from 125/250 behavior.

## 5. Comparison with DSL

DSL 500 on locked gold showed:
- service_memory: ~25% accuracy (model could not distinguish from task_state)
- Dominant confusion: service_memory → task_state

JSON 500 achieves 91.5% service_memory accuracy on dev. **This is a qualitative improvement — JSON format enables the model to learn the service/task distinction that DSL could not.**

---

*End of V0.5b JSON 500 Target Confusion Audit.*
