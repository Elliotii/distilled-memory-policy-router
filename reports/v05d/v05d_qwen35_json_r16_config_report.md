# V0.5d r=16 Config Report

**Date:** 2026-06-04  

## Config Diff from r=8

| Parameter | r=8 | r=16 | Rationale |
|-----------|:---:|:----:|-----------|
| lora_r | 8 | **16** | Double capacity |
| lora_alpha | 16 | **32** | Keep alpha/r = 2 |
| output_dir | v05c_lora/... | **v05d_lora/qwen35_json_r16_500** | Separate namespace |

## Unchanged

- Base model: Qwen3.5-4B
- Interface: unit_json
- Train file: v05b_train_500_json_sft_messages.jsonl
- Eval file: v05b_dev_json_sft_messages.jsonl
- Target modules: 6 (q/k/v/o_proj + in_proj_qkv + out_proj)
- QLoRA: 4-bit nf4, bf16 compute
- Training: 3 epochs, batch=4, grad_accum=4, LR=2e-4
- Seed: 42

## VRAM Estimate

With double the trainable params (9.8M vs 4.9M), VRAM increase is minimal (~+0.02GB for adapter weights). Still well within 12GB budget.
