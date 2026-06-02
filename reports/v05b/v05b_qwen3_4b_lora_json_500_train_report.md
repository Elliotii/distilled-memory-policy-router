# V0.5b Qwen3-4B Unit JSON LoRA 500 Training Report

**Date:** 2026-06-02  
**Context:** 5.7-D — 500-case Unit JSON LoRA training + dev eval  

---

## 1. Configuration

| Parameter | Value |
|-----------|-------|
| Config | `configs/v05b/qwen3_4b_lora_json_500.yaml` |
| Base model | Qwen3-4B-Instruct-2507 |
| Interface | unit_json |
| Train rows | 500 |
| Eval rows (dev) | 100 |
| LoRA rank | 8 |
| LoRA alpha | 16 |
| Epochs | 3 |
| Learning rate | 2.0e-4 |

## 2. Hardware

| Property | Value |
|----------|-------|
| GPU | NVIDIA GeForce RTX 4070 SUPER |
| VRAM total | 11 GB |
| Trainable params | 5,898,240 (0.1464%) |

## 3. Training Runtime

| Metric | Value |
|--------|-------|
| Total time | 842s (14m 2s) |
| Train steps | 96 |
| No OOM | ✅ |
| No NaN | ✅ |
| Adapter saved | ✅ |

## 4. Loss Summary

| Epoch | Eval Loss | Mean Token Acc |
|:-----:|:---------:|:--------------:|
| 1 | 0.611 | 86.5% |
| 2 | 0.548 | 87.1% |
| 3 | 0.544 | 87.2% |

Eval loss nearly flat from epoch 2→3 (0.548→0.544). The model is near the learning ceiling with 500 JSON cases.

## 5. JSON LoRA Training Comparison

| Metric | JSON 125 | JSON 250 | JSON 500 | DSL 500 |
|--------|:--------:|:--------:|:--------:|:-------:|
| Duration | 217s | 367s | 842s | 573s |
| Final eval loss | 1.300 | 0.608 | 0.544 | 0.62 |
| Final token acc | 72.6% | 86.5% | 87.2% | — |

JSON 500 achieves the lowest eval loss (0.544) of all LoRA variants.

## 6. Checkpoints

| Path |
|------|
| `results/v05b_lora/qwen3_4b_json_500/adapter/` |
| `results/v05b_lora/qwen3_4b_json_500/checkpoint-32/` |
| `results/v05b_lora/qwen3_4b_json_500/checkpoint-64/` |
| `results/v05b_lora/qwen3_4b_json_500/checkpoint-96/` |

## 7. Errors

None.

---

*End of V0.5b Qwen3-4B Unit JSON LoRA 500 Training Report.*
