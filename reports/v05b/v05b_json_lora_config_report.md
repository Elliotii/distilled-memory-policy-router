# V0.5b JSON LoRA Config Report

**Date:** 2026-06-02  
**Status:** Complete — Configs ready, DO NOT train  

---

## Config Files

| Config | Train | Eval | Output Dir |
|--------|:-----:|:----:|------------|
| `configs/v05b/qwen3_4b_lora_json_125.yaml` | 125 JSON SFT | dev JSON SFT | `results/v05b_lora/qwen3_4b_json_125` |
| `configs/v05b/qwen3_4b_lora_json_250.yaml` | 250 JSON SFT | dev JSON SFT | `results/v05b_lora/qwen3_4b_json_250` |
| `configs/v05b/qwen3_4b_lora_json_500.yaml` | 500 JSON SFT | dev JSON SFT | `results/v05b_lora/qwen3_4b_json_500` |

## Changes from v0.5 DSL Configs

| Parameter | v0.5 (DSL) | v0.5b (JSON) |
|-----------|------------|--------------|
| `interface` | (none) | `unit_json` |
| `train_file` | `data/v05/train/subsets/v05_train_*_sft_messages.jsonl` | `data/v05b/json_sft/v05b_train_*_json_sft_messages.jsonl` |
| `eval_file` | `data/v05/dev/v05_dev_sft_messages.jsonl` | `data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl` |
| `output_dir` | `results/v05_lora/qwen3_4b_dsl_*` | `results/v05b_lora/qwen3_4b_json_*` |

## Unchanged Parameters

All QLoRA/training hyperparameters are identical to v0.5:

| Parameter | Value |
|-----------|-------|
| `lora_r` | 8 |
| `lora_alpha` | 16 |
| `lora_dropout` | 0.05 |
| `lora_target_modules` | q_proj, k_proj, v_proj, o_proj |
| `num_train_epochs` | 3 |
| `per_device_train_batch_size` | 4 |
| `gradient_accumulation_steps` | 4 |
| `learning_rate` | 2.0e-4 |
| `lr_scheduler_type` | cosine |
| `warmup_ratio` | 0.1 |
| `optim` | adamw_8bit |
| `max_seq_length` | 2048 |
| `bf16` | true |
| `seed` / `data_seed` | 42 |
| `eval_strategy` / `save_strategy` | epoch |
| `load_best_model_at_end` | true |
| `metric_for_best_model` | eval_loss |

## Config Validation

All configs parse as valid YAML and reference existing files.

---

*End of V0.5b JSON LoRA Config Report.*
