# V0.5b Qwen3-4B Unit JSON LoRA 125 Training Report

**Date:** 2026-06-02  
**Context:** 5.7-B — 125-case Unit JSON LoRA smoke training  

---

## 1. Configuration

| Parameter | Value |
|-----------|-------|
| Config | `configs/v05b/qwen3_4b_lora_json_125.yaml` |
| Base model | Qwen3-4B-Instruct-2507 |
| Interface | unit_json |
| Train rows | 125 |
| Eval rows (dev) | 100 |
| LoRA rank | 8 |
| LoRA alpha | 16 |
| Epochs | 3 |
| Learning rate | 2.0e-4 |
| Batch size | 4 × 4 grad accum = 16 effective |
| Quantization | 4-bit nf4 |

## 2. Hardware

| Property | Value |
|----------|-------|
| GPU | NVIDIA GeForce RTX 4070 SUPER |
| VRAM total | 11 GB |
| VRAM free | ~10 GB |
| Trainable params | 5,898,240 (0.1464%) |

## 3. Training Runtime

| Metric | Value |
|--------|-------|
| Total time | 217s (3m 37s) |
| Train steps | 24 |
| Eval steps per epoch | 25 |
| No OOM | ✅ |
| No NaN | ✅ |
| Adapter saved | ✅ |

## 4. Loss Summary

| Epoch | Eval Loss | Train Loss | Mean Token Acc |
|:-----:|:---------:|:----------:|:--------------:|
| 1 | 1.919 | — | 65.2% |
| 2 | 1.424 | 1.541 | 70.4% |
| 3 | 1.300 | — | 72.6% |

Eval loss decreased smoothly (1.92 → 1.42 → 1.30). Strong convergence. No overfitting pattern.

For comparison, DSL LoRA 125 had eval loss 2.30 → 1.67 → 1.52 — JSON converges to lower loss (1.30 vs 1.52), suggesting easier format learning.

## 5. Checkpoints

| Path |
|------|
| `results/v05b_lora/qwen3_4b_json_125/adapter/` |
| `results/v05b_lora/qwen3_4b_json_125/checkpoint-8/` |
| `results/v05b_lora/qwen3_4b_json_125/checkpoint-16/` |
| `results/v05b_lora/qwen3_4b_json_125/checkpoint-24/` |

## 6. Errors

None.

---

*End of V0.5b Qwen3-4B Unit JSON LoRA 125 Training Report.*
