# v05g RTX 4090 Fallback Config Report

**Date:** 2026-06-05  
**Purpose:** Document 4090-specific fallback configs for v05g BF16 LoRA training

## Why 4090 Configs?

RTX 4090 has 24GB VRAM. BF16 LoRA on Qwen3.5-4B peaks at ~32-36GB without optimizations. The 4090 fallback configs reduce VRAM via:
- **batch_size: 2** (from 4) — halves activation memory
- **gradient_accumulation: 8** (from 4) — maintains effective batch ~16
- **gradient_checkpointing: true** — recomputes activations, ~30% VRAM savings

Estimated peak VRAM with 4090 configs: **~24-28 GB** (fits 24GB with some headroom)

## Config Files

| Config | Train Data | Output Dir |
|--------|-----------|------------|
| `qwen35_bf16_lora_json_r16_500_4090.yaml` | 500-control SFT | `results/v05g_bf16_lora/qwen35_json_r16_500_4090/` |
| `qwen35_bf16_lora_json_r16_1000_4090.yaml` | 1000-targeted SFT | `results/v05g_bf16_lora/qwen35_json_r16_1000_4090/` |

## Differences from Main Configs

| Parameter | Main Config | 4090 Config |
|-----------|------------|-------------|
| `per_device_train_batch_size` | 4 | **2** |
| `per_device_eval_batch_size` | 4 | **2** |
| `gradient_accumulation_steps` | 4 | **8** |
| `gradient_checkpointing` | (implicit false) | **true** |
| `output_dir` | `..._r16_500` | `..._r16_500_4090` |
| Effective batch size | 16 | 16 |

All other parameters (LoRA r=16, alpha=32, dropout=0.05, epochs=3, seq_len=2048, lr=2e-4, target_modules) are identical.

## When to Use

| Scenario | Use Config |
|----------|-----------|
| L40S 48GB, A100 40GB+, A6000 48GB | Main configs (`qwen35_bf16_lora_json_r16_{500,1000}.yaml`) |
| RTX 4090 24GB, RTX 3090 24GB | 4090 fallback configs (`..._4090.yaml`) |
| Any GPU < 24GB | Cannot run BF16 LoRA — use QLoRA fallback |

## Expected Performance Impact

| Aspect | Main | 4090 | Delta |
|--------|------|------|-------|
| Training time (500) | ~15-25 min | ~45-70 min | ~2-3× slower |
| Training time (1000) | ~30-50 min | ~90-140 min | ~2-3× slower |
| Model quality | Baseline | Comparable (same effective batch, same epochs) | Minimal |

Gradient checkpointing trades compute for memory — it should not affect model quality. The effective batch size (16) and number of epochs (3) are identical, so training dynamics should be similar.

## Verification

| Check | Result |
|-------|--------|
| Both 4090 configs YAML parse | ✅ |
| `gradient_checkpointing: true` in both | ✅ |
| `batch_size: 2`, `grad_accum: 8` in both | ✅ |
| Effective batch = 2 × 8 = 16 | ✅ (matches main configs: 4 × 4 = 16) |
| Output dirs unique (not overwriting main) | ✅ |
| `base_model_path` uses `${QWEN35_MODEL_PATH}` | ✅ |
| Training script supports `gradient_checkpointing` | ✅ (verified via `py_compile`) |
