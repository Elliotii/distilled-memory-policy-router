# V0.5c Qwen3.5 JSON LoRA Config Report

**Date:** 2026-06-02  
**Context:** 5.9-A — Feasibility and planning  

---

## 1. Config Files Created

| Config | Path |
|--------|------|
| 125-case smoke | `configs/v05c/qwen35_lora_json_125.yaml` |
| 250-case intermediate | `configs/v05c/qwen35_lora_json_250.yaml` |
| 500-case final | `configs/v05c/qwen35_lora_json_500.yaml` |

## 2. Key Hyperparameters

| Parameter | 125 | 250 | 500 | v0.5b (Qwen3-4B) |
|-----------|:---:|:---:|:---:|:----------------:|
| base_model_path | Qwen3.5-4B | Qwen3.5-4B | Qwen3.5-4B | Qwen3-4B-Instruct-2507 |
| train_file | …125_json_sft… | …250_json_sft… | …500_json_sft… | Same |
| eval_file | …dev_json_sft… | …dev_json_sft… | …dev_json_sft… | Same |
| output_dir | v05c_lora/qwen35_json_125 | v05c_lora/qwen35_json_250 | v05c_lora/qwen35_json_500 | v05b_lora/qwen3_4b_json_* |
| interface | unit_json | unit_json | unit_json | unit_json |
| lora_r | 8 | 8 | 8 | 8 |
| lora_alpha | 16 | 16 | 16 | 16 |
| lora_dropout | 0.05 | 0.05 | 0.05 | 0.05 |
| lora_target_modules | 6 modules | 6 modules | 6 modules | 4 modules |
| num_train_epochs | 3 | 3 | 3 | 3 |
| per_device_train_batch_size | 4 | 4 | 4 | 4 |
| gradient_accumulation_steps | 4 | 4 | 4 | 4 |
| learning_rate | 2.0e-4 | 2.0e-4 | 2.0e-4 | 2.0e-4 |
| max_seq_length | 2048 | 2048 | 2048 | 2048 |
| 4-bit type | nf4 | nf4 | nf4 | nf4 |
| bf16 | true | true | true | true |

## 3. Differences from v0.5b Configs

### 3.1 base_model_path
- v0.5b: `/home/abc16/hf_models/Qwen3-4B-Instruct-2507`
- v0.5c: `/home/abc16/hf_models/Qwen3.5-4B`
- **Rationale:** This is the changed variable — testing whether a stronger base model closes the gap to Qwen3.5 few-shot.

### 3.2 output_dir
- v0.5b: `results/v05b_lora/qwen3_4b_json_*`
- v0.5c: `results/v05c_lora/qwen35_json_*`
- **Rationale:** Separate namespace for v0.5c experiment; avoids overwriting v0.5b results.

### 3.3 lora_target_modules
- v0.5b: `[q_proj, k_proj, v_proj, o_proj]` (4 modules)
- v0.5c: `[q_proj, k_proj, v_proj, o_proj, in_proj_qkv, out_proj]` (6 modules)
- **Rationale:** Qwen3.5 has a hybrid architecture with 24 linear_attn layers using different projection names (`in_proj_qkv`, `out_proj`) and 8 self_attn layers using standard names (`q_proj`, `k_proj`, `v_proj`, `o_proj`). Without the linear_attn modules, only 8 of 32 layers (25%) would receive LoRA adapters. The expanded list provides coverage of all attention layers.

### 3.4 Unchanged Parameters
All training hyperparameters are identical to v0.5b:
- Same LR (2e-4), epochs (3), batch size (4), grad accum (4)
- Same LoRA rank (r=8), alpha (16), dropout (0.05)
- Same QLoRA settings (4-bit nf4, double quant, bf16 compute)
- Same eval/save strategy (epoch-based)

## 4. Trainable Parameter Comparison

| Config | Target Layers | Modules/Layer | Total Modules | ~Trainable Params |
|--------|:-------------:|:------------:|:------------:|:------------------:|
| v0.5b (Qwen3-4B) | 36 self_attn | 4 | 144 | ~5.8M |
| v0.5c (Qwen3.5) | 8 self + 24 linear | 4 + 2 | 80 | ~3.2M |

Despite having 6 module names, Qwen3.5 actually has fewer total LoRA target modules (80 vs 144) because:
- Fewer layers (32 vs 36)
- Only 2 modules per linear_attn layer (in_proj_qkv + out_proj) vs 4 per self_attn

The smaller trainable parameter count (~3.2M) is still well within the expected LoRA range for a 4B model (typically 0.05-0.5% of base parameters).

## 5. Rationale for Conservative 125 Smoke Settings

The 125-case smoke uses these defaults:
- **r=8, alpha=16:** Same as v0.5b; no change to LoRA capacity.
- **batch_size=4, grad_accum=4:** Effective batch size of 16. Fits within 12GB VRAM budget (est. 8-10GB peak).
- **LR=2e-4:** Same as v0.5b; known to work for Qwen3 SFT.
- **3 epochs:** Sufficient for 125 cases to converge without overfitting.

### If OOM occurs during smoke:
- Reduce to `per_device_train_batch_size: 2`, increase `gradient_accumulation_steps: 8`
- Or reduce `max_seq_length` to 1536

### If smoke shows poor results:
- Could try r=4 for parameter efficiency
- Could add MLP target modules (gate_proj, up_proj, down_proj)
- Could adjust LR (1e-4, 5e-5)

But **do not change configs mid-experiment** without a clear decision point and rationale.

## 6. Config Validation

All three configs:
- Point to existing data files (verified via `wc -l`)
- Use correct model path (verified via `config.json` inspection)
- Pass YAML syntax check (trivially valid)
- Use interface=`unit_json` (required by eval script)
- Reference no gold files
- Set deterministic seed=42

---

*End of V0.5c Qwen3.5 JSON LoRA Config Report.*
