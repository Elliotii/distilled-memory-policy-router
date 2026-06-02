# V0.5b Qwen3-4B Unit JSON LoRA 250 Error Analysis

**Date:** 2026-06-02  
**Context:** 5.7-C — 250-case Unit JSON LoRA dev error analysis  

---

## 1. Parse Quality

| Metric | JSON 125 | JSON 250 |
|--------|:--------:|:--------:|
| Parse success | 100% | 100% |
| Invalid JSON | 0 | 0 |
| Invalid memory IDs | 0 | 0 |
| Invalid unit IDs | 0 | 0 |
| Invalid targets | 0 | 0 |
| Markdown/prose | 0 | 0 |
| Empty outputs | 0 | 0 |
| Avg output chars | 131.0 | 129.5 |

**100% structural quality maintained at 250.** JSON format eliminates all parse errors — no regression.

## 2. Semantic Error Breakdown

### Target Confusion (JSON 250)

| Gold Target | → task_state | → service_memory | → repo_memory | → project_memory | → user_profile |
|-------------|:---:|:---:|:---:|:---:|:---:|
| service_memory | 18 | 44 | 1 | 3 | 5 |
| task_state | 46 | 14 | 5 | 5 | 4 |
| repo_memory | 6 | 4 | 22 | 5 | 0 |
| project_memory | 9 | 3 | 1 | 12 | 1 |
| user_profile | 2 | 4 | 0 | 0 | 6 |

### Changes from JSON 125

| Gold Target | JSON 125 Correct | JSON 250 Correct | Change |
|-------------|:---:|:---:|:---:|
| service_memory (71 total) | 39 (55%) | 44 (62%) | +5 ✅ |
| task_state (74 total) | 42 (57%) | 46 (62%) | +4 ✅ |
| repo_memory (37 total) | 21 (57%) | 22 (59%) | +1 |
| project_memory (26 total) | 10 (38%) | 12 (46%) | +2 ✅ |
| user_profile (12 total) | 5 (42%) | 6 (50%) | +1 |

**All 5 target classes improved their individual accuracy.** The largest improvement is service_memory (+5, from 55% to 62%).

### Main Confusion: service_memory → task_state

Down from 30/71 (42%) to 18/71 (25%) — a 17pp reduction in the dominant confusion. The model is getting better at distinguishing service behavior from task progress.

### Store/Skip Balance

JSON 250 now predicts SKIP for 44 total units — much closer to gold (44 SKIP units). JSON 125 predicted nearly 0 skips. This is a major improvement.

### Sensitive Store

66.7% — same as DSL 250. The 10 sensitive_boundary cases remain hard. JSON 250 stores some sensitive units as user_profile, same pattern as DSL.

## 3. JSON-Specific Issues

None. No regressions. All outputs remain valid JSON with correct structure.

---

*End of V0.5b Qwen3-4B Unit JSON LoRA 250 Error Analysis.*
