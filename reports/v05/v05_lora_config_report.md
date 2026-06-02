# V0.5 LoRA Config Report

**Date:** 2026-06-02  
**Context:** 5.5-A2 — QLoRA config documentation (fixed epoch-based eval)  

---

## QLoRA Config Summary

3 configs for Qwen3-4B Unit DSL QLoRA training:

| Config | Subset | Effective Batch | Steps/Epoch | Total Steps |
|--------|:------:|:---------------:|:-----------:|:-----------:|
| `qwen3_4b_lora_dsl_125.yaml` | 125 | 16 | 8 | 24 |
| `qwen3_4b_lora_dsl_250.yaml` | 250 | 16 | 16 | 48 |
| `qwen3_4b_lora_dsl_500.yaml` | 500 | 16 | 32 | 96 |

Effective batch = 4 (per_device) × 4 (grad_accum) = 16.

## 11GB GPU Rationale

RTX 4070 SUPER has 11GB VRAM. Qwen3-4B in bf16 requires ~8GB. With LoRA adapters + optimizer states + activations, full LoRA may not fit comfortably. QLoRA (4-bit nf4 quantization) reduces model memory to ~2-3GB, leaving ample room for training.

## Eval/Save Strategy

**Fixed (5.5-A2):** Changed from `eval_steps: 50` to `eval_strategy: epoch`, `save_strategy: epoch`.

Reason: 125 has ~24 steps, 250 has ~48 steps. Step 50 would never trigger eval for 125 or 250. Epoch-based eval ensures at least 3 checkpoints per run (one per epoch).

For 500 (96 steps), epoch-based eval is also fine — 3 checkpoints.

## metric_for_best_model Caveat

`metric_for_best_model: eval_loss` is the training loss on the dev SFT dataset. This is NOT a routing task metric.

**Checkpoint selection for project claims should use external dev task metrics** (parse success, STORE F1, target accuracy, SKIP F1) via eval_runner. After each training run, generate dev predictions and evaluate with eval_runner.

For 125 smoke: use eval_loss as a rough guide. If smoke succeeds, incorporate dev task metric checkpoint selection for 250/500.

## Learning Rate Caveat

`learning_rate: 2e-4` is used for all configs. Fallback plan:
- If loss diverges or outputs degrade → retry 1e-4
- If still unstable → retry 5e-5
- Do NOT tune LR based on gold results

## Output Dirs

| Config | Output Dir |
|--------|-----------|
| 125 | `results/v05_lora/qwen3_4b_dsl_125/` |
| 250 | `results/v05_lora/qwen3_4b_dsl_250/` |
| 500 | `results/v05_lora/qwen3_4b_dsl_500/` |

## No Gold Usage

Configs reference dev for eval only. No gold paths, no gold case IDs, no gold-derived content.

---

*End of V0.5 LoRA Config Report.*
