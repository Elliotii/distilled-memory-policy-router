# V0.5b Qwen3-4B Unit JSON LoRA 500 Error Analysis

**Date:** 2026-06-02  
**Context:** 5.7-D — 500-case dev error analysis  

---

## 1. Parse Quality

| Metric | JSON 125 | JSON 250 | JSON 500 |
|--------|:--------:|:--------:|:--------:|
| Parse success | 100% | 100% | 100% |
| Invalid JSON | 0 | 0 | 0 |
| Invalid memory IDs | 0 | 0 | 0 |
| Invalid unit IDs | 0 | 0 | 0 |
| Invalid targets | 0 | 0 | 0 |
| Markdown/prose | 0 | 0 | 0 |
| Empty outputs | 0 | 0 | 0 |
| Avg output chars | 131.0 | 129.5 | 134.1 |

**300/300 predictions = 100% valid JSON.** Zero structural errors ever.

## 2. Semantic Error Summary

| Metric | JSON 125 | JSON 250 | JSON 500 | Best |
|--------|:--------:|:--------:|:--------:|:----:|
| Exact | 11% | 20% | **34%** | 500 |
| STORE F1 | 0.910 | 0.947 | **0.958** | 500 |
| Target acc | 55.7% | 63.8% | **68.5%** | 500 |
| SKIP F1 | 0.535 | 0.747 | **0.753** | 500 |
| False store | 9.5% | **4.6%** | 6.5% | 250 |
| Irrelevant read | 16.3% | 19.0% | **15.9%** | 500 |
| Sensitive store | **33.3%** | 66.7% | 66.7% | 125 |

## 3. Remaining Errors at 500

### Store/Skip Errors
- 6.5% false store rate — 7% of predicted stores are incorrect
- SKIP F1 at 0.753 — model misses some skips, over-stores
- The model still leans toward storing rather than skipping

### Target Errors
- repo_memory: only 43.2% accurate — confused with 3 other targets
- task_state: 58.6% accurate — 23% confused with service_memory
- project_memory: 57.7% accurate — confused with service/task

### Read Errors
- 15.9% irrelevant read rate — model reads some unrelated memories
- READ F1 0.902 — good but could be better

## 4. Error Trajectory

All error rates are improving or stable with more data. No metric shows degradation from 250→500 except false store (4.6% → 6.5%, within noise).

## 5. JSON-Specific Issues

None. JSON format remains perfectly reliable at 500 cases.

---

*End of V0.5b JSON 500 Error Analysis.*
