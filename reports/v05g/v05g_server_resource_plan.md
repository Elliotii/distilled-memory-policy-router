# v05g Server Resource Plan (CORRECTED)

**Date:** 2026-06-05 (corrected after ClaudeCode audit)  
**Model:** Qwen3.5-4B  
**Precision:** BF16 standard LoRA (no quantization)  
**Training script:** `src/v05/train_lora_router.py`

## Config Matrix

| GPU | VRAM | Config(s) | Batch Size | Grad Accum | Grad Ckpt | Effective Batch |
|-----|------|-----------|------------|------------|-----------|-----------------|
| L40S / A100 40GB+ | 40-80 GB | `qwen35_bf16_lora_json_r16_{500,1000}.yaml` | 4 | 4 | No | 16 |
| RTX 4090 | 24 GB | `qwen35_bf16_lora_json_r16_{500,1000}_4090.yaml` | 2 | 8 | **Yes** | 16 |

## VRAM Estimate

| Component | Size |
|-----------|------|
| Model params (4B × 2 bytes BF16) | ~8 GB |
| Optimizer (AdamW, 2× params) | ~16 GB |
| Gradients | ~8 GB |
| Activations | ~2-4 GB (higher without grad ckpt, lower with) |
| **Total peak (no grad ckpt)** | **~32-36 GB** |
| **Total peak (with grad ckpt)** | **~24-28 GB** |

## Recommended GPUs

| GPU | VRAM | Config Set | Suitability |
|-----|------|-----------|-------------|
| **L40S 48GB** | 48 GB | Main | ✅ Best — comfortable, no compromises |
| **A100 40GB** | 40 GB | Main | ✅ Good — slight buffer needed |
| **A100 80GB** | 80 GB | Main | ✅ Excellent — overkill |
| **A6000 48GB** | 48 GB | Main | ✅ Comfortable |
| **RTX 4090 24GB** | 24 GB | 4090 fallback | ⚠️ Works with grad ckpt, slower |
| **RTX 3090 24GB** | 24 GB | 4090 fallback | ⚠️ Same as 4090 |

## Training Throughput Estimates

### L40S / A100 40GB (Main Configs)

| Variant | Examples × Epochs | Est. Time |
|---------|-------------------|-----------|
| BF16 r16 500 | 500 × 3 = 1,500 | ~15-25 min |
| BF16 r16 1000 | 1000 × 3 = 3,000 | ~30-50 min |

### RTX 4090 24GB (4090 Fallback Configs)

| Variant | Examples × Epochs | Est. Time |
|---------|-------------------|-----------|
| BF16 r16 500 | 500 × 3 = 1,500 | ~45-70 min |
| BF16 r16 1000 | 1000 × 3 = 3,000 | ~90-140 min |

**Note:** RTX 4090 estimates are ~2-3× slower due to gradient checkpointing overhead and smaller batch size.

## Disk Requirements

| Item | Size |
|------|------|
| Model weights | ~8 GB |
| Training data | ~2 MB |
| Checkpoints (per variant) | ~1.5 GB |
| Adapter output (per variant) | ~50-100 MB |
| Logs + metrics | <10 MB |
| **Total (both variants)** | **~12 GB** |

## OOM Fallback Plan

### If L40S/A100 OOMs (unlikely)

| Tier | Action | VRAM Reduction |
|------|--------|---------------|
| 1 | Enable `gradient_checkpointing: true` in main config | ~30% |
| 2 | Use 4090 fallback configs (bs=2, ga=8) | ~50% |
| 3 | Reduce `max_seq_length: 1536` | Variable |
| 4 | QLoRA fallback (`quantization: "4bit"`) | ~60% |

### If RTX 4090 OOMs with 4090 configs

| Tier | Action |
|------|--------|
| 1 | Reduce `max_seq_length: 1536` |
| 2 | QLoRA fallback (`quantization: "4bit"`) — defeats BF16 purpose |

**Decision rule:** If QLoRA fallback is needed for 500 variant, the BF16-vs-QLoRA comparison is invalidated. Document the fallback and only compare 1000 QLoRA variants.

## Seq Length

- 2048 is the default, matching prior QLoRA experiments (v05c, v05d)
- v05g SFT messages are 400-1200 tokens after chat template
- Fallback to 1536 if OOM
- Do NOT go below 1536 without checking truncation impact
