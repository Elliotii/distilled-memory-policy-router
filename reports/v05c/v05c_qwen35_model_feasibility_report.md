# V0.5c Qwen3.5 Model Feasibility Report

**Date:** 2026-06-02  
**Context:** 5.9-A — Feasibility and planning  

---

## 1. Model Path

| Property | Value |
|----------|-------|
| Path | `/home/abc16/hf_models/Qwen3.5-4B` |
| Status | **Found and available** |
| Size on disk | 8.8 GB (2 safetensors files: 5.0G + 3.8G) |
| Download method | HF mirror (previously downloaded for v0.5 few-shot baselines) |

## 2. Model Configuration

| Property | Qwen3.5-4B | Qwen3-4B-Instruct-2507 (v0.5b) |
|----------|------------|--------------------------------|
| Architecture | Qwen3_5ForConditionalGeneration | Qwen3ForCausalLM |
| model_type | qwen3_5 | qwen3 |
| hidden_size | 2560 | 2560 |
| num_hidden_layers | 32 | 36 |
| num_attention_heads | 16 | 32 |
| num_key_value_heads | 4 | 8 |
| head_dim | 256 | 128 |
| intermediate_size | 9216 | 9728 |
| vocab_size | 248,320 | 151,936 |
| max_position_embeddings | 262,144 | 262,144 |
| dtype | bfloat16 | bfloat16 |
| Attention types | 24 linear_attn + 8 full_attn | 36 full_attn (self_attn) |
| attn_output_gate | true | N/A |
| rope_theta | 10,000,000 | 5,000,000 |

## 3. Architectural Differences

Qwen3.5-4B is architecturally significantly different from Qwen3-4B:

1. **Hybrid attention:** 24 layers use `linear_attn` (efficient linear attention) and 8 layers use `self_attn` (standard full attention). Full attention layers at indices 3, 7, 11, 15, 19, 23, 27, 31.

2. **Fewer layers, bigger heads:** 32 layers with head_dim=256 vs 36 layers with head_dim=128.

3. **More aggressive GQA:** 4 KV heads vs 8 for the same total attention dimension.

4. **Larger vocabulary:** 248K tokens vs 152K tokens (+63%).

5. **Attention output gating:** `attn_output_gate: true` provides per-head learnable output gating.

## 4. GPU / VRAM

| Property | Value |
|----------|-------|
| GPU | NVIDIA GeForce RTX 4070 (Laptop) |
| Total VRAM | 12,282 MiB (~12 GB) |
| Free VRAM (idle) | ~11.6 GB (695 MiB used) |
| CUDA Version | 13.1 |
| Driver Version | 591.86 |

## 5. QLoRA Feasibility Assessment

### 4-bit QLoRA Memory Estimate

| Component | Estimated VRAM |
|-----------|:--------------:|
| Qwen3.5-4B in 4-bit nf4 | ~2.5 GB |
| LoRA adapters (r=8, 6 target modules × 32 layers) | ~0.05 GB |
| Optimizer states (AdamW 8-bit) | ~0.5 GB |
| Activations (batch=4, seq=2048, grad_accum=4) | ~5-7 GB |
| **Total estimated** | **~8-10 GB** |

### Feasibility Verdict

✅ **FEASIBLE with conservative settings.**

The RTX 4070 12GB should handle Qwen3.5 QLoRA training with batch_size=4, grad_accum=4, and max_seq_length=2048. The estimated peak VRAM of 8-10 GB leaves 2-4 GB headroom.

### Recommendations

1. **Use existing batch_size=4, grad_accumulation_steps=4** — no reduction needed for 125 smoke.
2. **Monitor VRAM during 125 smoke** — reduce to batch_size=2, grad_accum=8 if OOM.
3. **Qwen3.5 has larger vocabulary (248K)** — embedding layer is ~635 MB in bf16. In 4-bit, this shrinks to ~160 MB.
4. **Flash-linear-attention not installed** (warning during load). The model falls back to torch implementation. This is functionally correct but may be slower and use slightly more memory. Consider installing for 250/500 runs.

## 6. Transformers / PEFT Compatibility

| Component | Version | Qwen3.5 Support |
|-----------|:-------:|:---------------:|
| transformers | 5.9.0 | ✅ Native qwen3_5 support |
| PEFT | 0.19.1 | ✅ Manual target_modules (no auto-mapping for qwen3_5) |
| PyTorch | 2.6+ | ✅ |
| bitsandbytes | 0.49+ | ✅ 4-bit quantization |

The model loads successfully with `AutoModelForCausalLM.from_pretrained(trust_remote_code=True)`. transformers 5.9.0 has native support for `Qwen3_5ForConditionalGeneration`.

## 7. LoRA Target Modules — Architectural Impact

Qwen3.5's hybrid architecture requires different LoRA target modules than Qwen3-4B:

| Model | Attention Type | Target Modules | Layers Targeted |
|-------|---------------|----------------|:---------------:|
| Qwen3-4B | 36 self_attn | q_proj, k_proj, v_proj, o_proj | 36/36 (100%) |
| Qwen3.5 | 8 self_attn | q_proj, k_proj, v_proj, o_proj | 8/32 (25%) |
| Qwen3.5 | 24 linear_attn | in_proj_qkv, out_proj | 24/32 (75%) |

The v0.5c config targets all 6 modules across all 32 layers:
- `q_proj`, `k_proj`, `v_proj`, `o_proj` → 8 self_attn layers
- `in_proj_qkv`, `out_proj` → 24 linear_attn layers

This provides full coverage of Qwen3.5's attention mechanism. The total trainable parameter count is approximately:
- 8 layers × 4 modules + 24 layers × 2 modules = 80 target modules
- At r=8, ~3.2M trainable parameters (~0.08% of 4B base model)

For comparison, Qwen3-4B had 36 × 4 = 144 target modules, ~5.8M trainable parameters (~0.15% of 4B).

## 8. Blockers

| Blocker | Status |
|---------|:------:|
| Model missing | ✅ Resolved — model at `/home/abc16/hf_models/Qwen3.5-4B` |
| GPU insufficient | ✅ Resolved — 12GB RTX 4070 sufficient for 4B QLoRA |
| transformers/PEFT incompatible | ✅ Resolved — transformers 5.9.0 supports qwen3_5 |
| Script incompatibility | ✅ Resolved — train/eval use generic AutoModel loading |
| Gold corrupted | ✅ Resolved — hash `56e16078...` unchanged |
| Train data missing | ✅ Resolved — JSON SFT files from v0.5b available |

---

*End of V0.5c Qwen3.5 Model Feasibility Report.*
