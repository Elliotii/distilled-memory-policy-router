# V0.5 Qwen Full Dev Run Report

**Date:** 2026-06-02  
**Context:** 5.4-D — full 100-case dev baseline for Qwen3-4B vs Qwen3.5  

---

## 1. Scope

Full dev baseline evaluation on 100 independently constructed dev cases. Used for model selection, interface comparison, and baseline planning. **Not for final claims — locked gold is the final evaluation standard.**

## 2. Dev-Only Usage

All predictions and evaluations in this report use dev data only. No locked gold was accessed or used in any way.

## 3. Models

| Model | Path | Predictions | Errors | Empty | Runtime |
|-------|------|:-----------:|:------:|:-----:|:-------:|
| Qwen3-4B | `/home/abc16/hf_models/Qwen3-4B-Instruct-2507` | 400 | 0 | 0 | ~8.5 min |
| Qwen3.5 | `/home/abc16/hf_models/Qwen3.5-4B` | 400 | 0 | 0 | ~13 min |
| **Total** | | **800** | **0** | **0** | **~22 min** |

## 4. Prompt Variants

| Variant | Interface | Few-Shot | Prompt File |
|---------|-----------|:--------:|-------------|
| DSL zero-shot | unit_dsl | — | `unit_dsl_zero_shot.txt` |
| DSL few-shot | unit_dsl | 5 train-pool | `unit_dsl_fewshot.txt` |
| JSON zero-shot | unit_json | — | `unit_json_zero_shot.txt` |
| JSON few-shot | unit_json | 5 train-pool | `unit_json_fewshot.txt` |

## 5. Decoding Settings

| Parameter | Value |
|-----------|-------|
| temperature | 0 |
| do_sample | False |
| max_new_tokens | 512 |
| precision | bfloat16 |
| enable_thinking (Qwen3.5) | Requested and applied |
| local_files_only | True |

## 6. Prediction Row Counts

| Model | DSL zs | DSL fs | JSON zs | JSON fs | Total |
|-------|:------:|:------:|:-------:|:-------:|:-----:|
| Qwen3-4B | 100 | 100 | 100 | 100 | 400 |
| Qwen3.5 | 100 | 100 | 100 | 100 | 400 |

All 800 predictions completed successfully. 0 errors, 0 empty outputs.

## 7. Structural Metrics Summary

| System | Parse | Best Interface |
|--------|:-----:|:-------------:|
| qwen3_4b DSL few-shot | 96.0% | DSL |
| qwen3_4b JSON few-shot | 99.0% | JSON |
| qwen35_4b DSL few-shot | 99.0% | DSL |
| qwen35_4b JSON few-shot | 98.0% | JSON |

**Zero-shot parse rates are much lower** (43-47% DSL, 97% JSON). Qwen3-4B DSL zero-shot has 82% invalid memory ID rate (uses space-separated READ IDs instead of comma-separated).

## 8. Semantic Metrics (Top Systems)

| System | Exact | READ F1 | STORE F1 | Target Acc | SKIP F1 | False Store | Sensitive |
|--------|:-----:|:-------:|:--------:|:----------:|:-------:|:-----------:|:---------:|
| **qwen35_4b DSL fs** | **41.0%** | 0.912 | **0.975** | **74.8%** | 0.864 | 2.3% | 33.3% |
| qwen35_4b JSON fs | 37.0% | 0.891 | 0.965 | 73.9% | **0.903** | **1.0%** | 33.3% |
| qwen3_4b JSON fs | 23.0% | 0.882 | 0.961 | 67.1% | 0.851 | 1.9% | 33.3% |
| qwen3_4b DSL fs | 22.0% | 0.871 | 0.936 | 71.1% | 0.690 | 5.6% | 33.3% |
| qwen35_4b JSON zs | 23.0% | 0.840 | 0.941 | 71.0% | 0.787 | 2.4% | 33.3% |

## 9. Gold Protection Confirmation

| Check | Before | After |
|-------|:------:|:-----:|
| Gold SHA-256 | `56e16078...` | `56e16078...` |
| Gold modified | No | No |

Gold was NEVER accessed during this full dev baseline run.

## 10. Next Step

Select best model/interface for locked gold evaluation. Qwen3.5 DSL few-shot is the clear leader on dev metrics.

---

*End of V0.5 Qwen Full Dev Run Report.*
