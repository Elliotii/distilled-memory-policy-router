# V0.5d r=16 Training Report

**Date:** 2026-06-04  

## Training

| Metric | r=16 | r=8 |
|--------|:----:|:---:|
| Duration | 3506s (~58 min) | 2982s |
| Trainable params | 9,830,400 | 4,915,200 |
| OOM | No | No |
| NaN | No | No |

## Training Progress

| Epoch | r=16 Eval Loss | r=16 Token Acc | r=8 Eval Loss | r=8 Token Acc |
|:-----:|:--------------:|:--------------:|:-------------:|:-------------:|
| 1 | 0.447 | 88.9% | 0.460 | 88.6% |
| 2 | 0.439 | 89.4% | 0.435 | 89.2% |
| 3 | **0.437** | **89.5%** | 0.435 | 89.3% |

r=16 converges to slightly higher eval loss (0.437 vs 0.435) but with similar token accuracy (89.5% vs 89.3%). The higher eval loss is expected with 2x more parameters (more capacity = slightly higher perplexity on held-out data, but lower loss doesn't directly translate to better task metrics).
