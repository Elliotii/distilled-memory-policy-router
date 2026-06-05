# gold_v2_009 Four-System Evaluation Report

**Date:** 2026-06-04  

## Systems Evaluated on gold_v2_009 (150 cases)

| # | System | Exact | Parse | STORE F1 | Target Acc | SKIP F1 | Sens(tag) |
|:-:|--------|:-----:|:-----:|:--------:|:----------:|:-------:|:---------:|
| 1 | **Qwen3.5 JSON few-shot** | **30.7%** | 86.0% | 0.856 | 75.3% | 0.847 | 0% |
| 2 | Qwen3.5 r=16 LoRA | 22.7% | 94.7% | **0.909** | **84.2%** | **0.892** | 0% |
| 3 | Qwen3.5 r=8 LoRA | 22.7% | **98.7%** | 0.880 | 79.1% | 0.834 | 0% |
| 4 | Qwen3-4B r=8 LoRA | 16.0% | 100.0% | 0.925 | 76.8% | 0.860 | 100% tag |

## Key Observations

- **Qwen3.5 few-shot #1 on exact** (30.7%) — but worst parse (86%)
- **r=16 and r=8 TIED on exact** (22.7%)
- **r=16 leads on all routing metrics**: STORE F1 +0.029, target acc +5.1pp, SKIP F1 +0.058
- **r=16 has best target accuracy of any system** (84.2%)
- **r=8 has best parse** (98.7%)
- **Qwen3-4B r=8 lags on exact** (16.0%) but maintains 100% parse
- **Few-shot parse is poor** (86%) — 21 parse failures on v009. The few-shot model may need enable_thinking=False (same fix as LoRA eval). This inflates few-shot exact.

## Store/Skip-Exact (ignoring READ)

| System | Store/Skip-Exact |
|--------|:----------------:|
| Qwen3.5 r=16 | **62.0%** |
| Qwen3.5 r=8 | 53.3% |
| Qwen3-4B r=8 | 52.0% |

r=16 leads r=8 by +8.7pp on the write side.
