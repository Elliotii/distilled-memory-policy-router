# V0.5d Qwen3.5 JSON QLoRA r=16 — Plan and Config

**Date:** 2026-06-04  
**Experiment:** r=16 QLoRA capacity ablation (dev-only)

## Config

Created `configs/v05d/qwen35_lora_json_r16_500.yaml` from r=8 config with:
- `lora_r: 16` (was 8)
- `lora_alpha: 32` (was 16, keeps alpha/r=2)
- `output_dir: results/v05d_lora/qwen35_json_r16_500`
- All other settings unchanged

## Trainable Parameters

| Config | Trainable Params | % of Base |
|--------|:----------------:|:---------:|
| r=8 | 4,915,200 | 0.12% |
| r=16 | 9,830,400 | 0.23% |

2x parameter increase while staying within QLoRA VRAM budget.

## Hypothesis

Doubling LoRA rank provides more capacity for the adapter to learn:
1. Better JSON structure (parse should stay ≥98%)
2. Higher exact match (target: +2-5pp)
3. Improved target classification
4. No degradation in STORE/SKIP or safety
