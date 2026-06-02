# V0.5 Qwen Smoke Retry Report

**Date:** 2026-06-02  
**Context:** 5.4-C — retry smoke after prompt/runner fixes  

---

## 1. Scope

Re-ran 5-case dev smoke after fixing root causes from 5.4-B audit. Same 5 cases, same two models, same 4 prompt variants. Different prompt/runner implementation.

## 2. Models

| Model | Status |
|-------|:------:|
| Qwen3-4B-Instruct-2507 | ✅ Ran successfully |
| Qwen3.5-4B | ✅ Ran successfully |

## 3. Prompts (Fixed)

| Variant | System Role | Chat Template | Few-Shot |
|---------|:-----------:|:------------:|:--------:|
| unit_dsl_zero_shot | ✅ | ✅ | — |
| unit_dsl_fewshot | ✅ | ✅ | 5 examples |
| unit_json_zero_shot | ✅ | ✅ | — |
| unit_json_fewshot | ✅ | ✅ | 5 examples |

## 4. Same Smoke Cases

v05_dev_0001, v05_dev_0019, v05_dev_0058, v05_dev_0020, v05_dev_0037 (unchanged from 5.4-B).

## 5. Prediction Row Counts

| Model | Rows | Errors | Empty |
|-------|:----:|:------:|:-----:|
| Qwen3-4B | 20 | 0 | 0 |
| Qwen3.5 | 20 | 0 | 0 |
| **Total** | **40** | **0** | **0** |

## 6. Parse Results

| System | Interface | Parse Success |
|--------|-----------|:------------:|
| qwen3-4b_unit_dsl_fewshot | unit_dsl | **100.0%** |
| qwen3-4b_unit_dsl_zero_shot | unit_dsl | **100.0%** |
| qwen3-4b_unit_json_fewshot | unit_json | **100.0%** |
| qwen3-4b_unit_json_zero_shot | unit_json | **100.0%** |
| qwen3.5_unit_dsl_fewshot | unit_dsl | **100.0%** |
| qwen3.5_unit_dsl_zero_shot | unit_dsl | 80.0% |
| qwen3.5_unit_json_fewshot | unit_json | **100.0%** |
| qwen3.5_unit_json_zero_shot | unit_json | 80.0% |

**All ≥ 80% parse success.** ✅

## 7. Semantic Metrics (Top Performers)

| System | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:--------:|:----------:|:-------:|:---------:|
| qwen3.5 DSL few-shot | 40.0% | 1.000 | 80.0% | 1.000 | 0 |
| qwen3-4b JSON few-shot | 40.0% | 0.947 | 77.8% | 0.857 | 0 |
| qwen3.5 JSON few-shot | 40.0% | 0.947 | 77.8% | 0.857 | 0 |
| qwen3-4b DSL few-shot | 20.0% | 0.900 | 66.7% | 0.667 | 0 |

## 8. Latency

| Model | DSL zero-shot | DSL few-shot | JSON zero-shot | JSON few-shot |
|-------|:------------:|:------------:|:--------------:|:-------------:|
| Qwen3-4B | ~700ms | ~700ms | ~1600ms | ~1200ms |
| Qwen3.5 | ~1100ms | ~1100ms | ~2500ms | ~1700ms |

## 9. Output Length

| Model | DSL | JSON |
|-------|:---:|:----:|
| Qwen3-4B | 63-68 chars | 114-151 chars |
| Qwen3.5 | 61-68 chars | 114-151 chars |

## 10. Whether Full Dev Is Allowed

**✅ YES — Full dev baseline is allowed.**

Success criteria met:
1. ✅ Qwen3-4B DSL few-shot parse ≥ 80% (100%)
2. ✅ Qwen3-4B zero empty outputs
3. ✅ Prediction/eval schema fixed (canonical interfaces, system names)
4. ✅ No gold usage violation
5. ✅ Qwen3.5 parse ≥ 80% for DSL few-shot (100%)
6. ✅ Qwen3.5 latency acceptable (1-3s per case, not 19s)
7. ✅ Thinking/prose contamination controlled

### Proceed to full dev baseline with:
- **Primary:** Qwen3-4B DSL few-shot (100% parse, robust)
- **Challenger:** Qwen3.5 DSL few-shot (100% parse, best STORE F1)
- **JSON baselines:** Both models (for interface comparison)

---

*End of V0.5 Qwen Smoke Retry Report.*
