# V0.5c Qwen3.5 JSON LoRA 250 Training Report

**Date:** 2026-06-03  
**Context:** 5.9-C — Qwen3.5 Unit JSON LoRA 250 training + dev eval  

---

## 1. Preflight

All 16 checks passed. Config, data paths, CUDA, gold hash all verified.

## 2. Training Summary

| Metric | Qwen3.5 250 | Qwen3.5 125 | Qwen3-4B 250 |
|--------|:-----------:|:-----------:|:------------:|
| Duration | 1864s (~31 min) | 903s | 367s |
| Trainable params | 4,915,200 | same | ~5.8M |
| OOM | No | No | No |
| NaN | No | No | No |

## 3. Training Progress

| Epoch | Train Loss | Eval Loss | Token Accuracy |
|:-----:|:----------:|:---------:|:--------------:|
| 1 | 1.777 → 0.739 | 0.576 | 86.5% |
| 2 | 0.476 | 0.469 | 88.5% |
| 3 | 0.446 | **0.461** | **88.5%** |

## 4. Convergence Comparison

| Metric | Qwen3.5 125 | Qwen3.5 250 | Qwen3-4B 250 |
|--------|:-----------:|:-----------:|:------------:|
| Epoch 1 eval loss | 1.264 | 0.576 | 1.326 |
| Epoch 2 eval loss | 0.626 | 0.469 | 0.659 |
| Epoch 3 eval loss | 0.544 | **0.461** | 0.608 |
| Epoch 3 token acc | 86.9% | 88.5% | 86.5% |

Qwen3.5 250 achieves much lower eval loss than Qwen3-4B 250 (0.461 vs 0.608) and lower than Qwen3.5 125 (0.461 vs 0.544). The model is converging well — no signs of overfitting.

## 5. Training Time Analysis

Qwen3.5 training is significantly slower than Qwen3-4B:
- Qwen3.5 125: 903s vs Qwen3-4B 125: 217s (4.2x slower)
- Qwen3.5 250: 1864s vs Qwen3-4B 250: 367s (5.1x slower)

Causes:
1. Larger vocabulary (248K vs 152K tokens)
2. Flash-linear-attention not installed — falls back to torch implementation
3. 6 target modules vs 4, though total params are fewer (4.9M vs 5.8M)

Training time is not a blocker but worth noting for 500 planning (estimate: ~3700s / ~62 min).

---

*End of V0.5c Qwen3.5 JSON LoRA 250 Training Report.*
