# V0.5c Qwen3.5 JSON LoRA 500 Training Report

**Date:** 2026-06-03  
**Context:** 5.9-D  

## Training Summary

| Metric | Qwen3.5 500 | Qwen3.5 250 | Qwen3-4B 500 |
|--------|:-----------:|:-----------:|:------------:|
| Duration | 2982s (~50 min) | 1864s | 573s |
| Trainable params | 4,915,200 | same | ~5.8M |
| OOM | No | No | No |
| NaN | No | No | No |

## Training Progress

| Epoch | Train Loss | Eval Loss | Token Accuracy |
|:-----:|:----------:|:---------:|:--------------:|
| 1 | 1.905 → 0.472 | 0.460 | 88.6% |
| 2 | 0.429 → 0.366 | 0.435 | 89.2% |
| 3 | 0.364 → 0.359 | **0.435** | **89.3%** |

Convergence healthy — eval loss plateaus at 0.435 with token accuracy 89.3%. No overfitting signs.

## Qwen3.5 Learning Curve (Training)

| Metric | 125 | 250 | 500 |
|--------|:---:|:---:|:---:|
| Epoch 1 eval loss | 1.264 | 0.576 | 0.460 |
| Epoch 3 eval loss | 0.544 | 0.461 | **0.435** |
| Epoch 3 token acc | 86.9% | 88.5% | **89.3%** |
| Training time | 903s | 1864s | 2982s |
