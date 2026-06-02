# V0.5b Qwen3-4B Unit JSON LoRA 250 Training Report

**Date:** 2026-06-02  
**Context:** 5.7-C — 250-case Unit JSON LoRA training + dev eval  

---

## 1. Configuration

| Parameter | Value |
|-----------|-------|
| Config | `configs/v05b/qwen3_4b_lora_json_250.yaml` |
| Base model | Qwen3-4B-Instruct-2507 |
| Interface | unit_json |
| Train rows | 250 |
| Eval rows (dev) | 100 |
| LoRA rank | 8 |
| LoRA alpha | 16 |
| Epochs | 3 |
| Learning rate | 2.0e-4 |
| Batch size | 4 × 4 grad accum = 16 effective |

## 2. Hardware

| Property | Value |
|----------|-------|
| GPU | NVIDIA GeForce RTX 4070 SUPER |
| VRAM total | 11 GB |
| Trainable params | 5,898,240 (0.1464%) |

## 3. Training Runtime

| Metric | Value |
|--------|-------|
| Total time | 367s (6m 7s) |
| Train steps | 48 |
| Eval steps per epoch | 25 |
| No OOM | ✅ |
| No NaN | ✅ |
| Adapter saved | ✅ |

## 4. Loss Summary

| Epoch | Eval Loss | Mean Token Acc |
|:-----:|:---------:|:--------------:|
| 1 | 1.326 | 72.7% |
| 2 | 0.659 | 85.5% |
| 3 | 0.608 | 86.5% |

Eval loss decreased smoothly: 1.33 → 0.66 → 0.61. Very strong convergence. Mean token accuracy reached 86.5% — the model is confidently generating correct JSON.

## 5. Comparison with DSL 250 Training

| Metric | DSL 250 | JSON 250 |
|--------|:-------:|:--------:|
| Duration | 326s | 367s |
| Eval loss epoch 1 | 1.54 | 1.33 |
| Eval loss epoch 2 | 0.73 | 0.66 |
| Eval loss epoch 3 | 0.68 | **0.61** |

JSON training converges to a lower loss (0.61 vs 0.68), suggesting the JSON format is intrinsically easier for the model to learn.

## 6. Checkpoints

| Path |
|------|
| `results/v05b_lora/qwen3_4b_json_250/adapter/` |
| `results/v05b_lora/qwen3_4b_json_250/checkpoint-16/` |
| `results/v05b_lora/qwen3_4b_json_250/checkpoint-32/` |
| `results/v05b_lora/qwen3_4b_json_250/checkpoint-48/` |

## 7. Errors

None.

---

*End of V0.5b Qwen3-4B Unit JSON LoRA 250 Training Report.*
