# V0.5c Qwen3.5 JSON LoRA 500 Dev Eval Report

**Date:** 2026-06-03  

## Structural Metrics

| Metric | Qwen3.5 500 | Qwen3.5 250 | Qwen3-4B 500 |
|--------|:-----------:|:-----------:|:------------:|
| Parse success | **98.0%** ✅ | 90.0% | 100.0% |
| Invalid target | 0.0% | 2.7% | 0.0% |
| Avg chars | 130.0 | 131.9 | 134.1 |

## Semantic Metrics

| Metric | Qwen3.5 500 | Qwen3.5 250 | Qwen3-4B 500 |
|--------|:-----------:|:-----------:|:------------:|
| Exact | **34.0%** | 17.0% | 34.0% |
| READ F1 | **0.908** | 0.892 | 0.902 |
| STORE unit F1 | **0.959** | 0.913 | 0.958 |
| Target accuracy | **77.4%** ✅✅ | 73.1% | 68.5% |
| SKIP F1 | **0.762** | 0.623 | 0.753 |
| False store | 4.5% | 4.9% | 6.5% |
| Irrelevant read | 13.5% | 18.2% | 15.9% |
| Sensitive store | 66.7% | 66.7% | 66.7% |

## Key Improvements from 250

| Metric | 250→500 Δ |
|--------|:---------:|
| Parse | +8.0pp (recovered!) |
| Exact | +17.0pp |
| STORE F1 | +0.046 |
| Target acc | +4.3pp |
| SKIP F1 | +0.139 |
| target=skip | 7→0 (eliminated!) |

The parse regression at 250 was transient — fully recovered at 500 with 0 `"target":"skip"` errors.
