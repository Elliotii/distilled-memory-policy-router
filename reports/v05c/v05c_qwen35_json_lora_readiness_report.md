# V0.5c Qwen3.5 JSON LoRA Readiness Report

**Date:** 2026-06-02  
**Context:** 5.9-A — Feasibility and planning  

---

## Decision: Option A — Ready for Qwen3.5 JSON LoRA 125 Smoke

All gates passed. The experiment is technically feasible and procedurally sound.

---

## Readiness Checklist

| Gate | Status | Detail |
|------|:------:|--------|
| Model available | ✅ | `/home/abc16/hf_models/Qwen3.5-4B` (8.8 GB, 2 safetensors) |
| Model loads | ✅ | transformers 5.9.0 native support for `qwen3_5` |
| GPU sufficient | ✅ | RTX 4070 12GB, est. 8-10 GB for 4B QLoRA |
| Configs created | ✅ | 3 configs: 125, 250, 500 |
| Train data ready | ✅ | 125/250/500 JSON SFT messages from v0.5b |
| Dev data ready | ✅ | 100 JSON SFT messages from v0.5b |
| Gold protected | ✅ | Hash `56e16078...` unchanged, not read, not touched |
| Scripts compile | ✅ | `py_compile` passes for train/eval |
| Unit tests pass | ✅ | 77/77 OK |
| No data modifications | ✅ | Zero changes to train/dev/gold |
| No training | ✅ | This is planning only |
| No inference | ✅ | This is planning only |
| No DeepSeek | ✅ | No API calls |
| No git operations | ✅ | No add/commit/push |

## Script Compatibility

| Script | Qwen3.5 Compatible | Notes |
|--------|:------------------:|-------|
| `src/v05/train_lora_router.py` | ✅ | Uses `AutoModelForCausalLM` + `trust_remote_code=True`; works with any architecture. Preflight auto-detects interface from config. |
| `src/v05/eval_lora_router.py` | ✅ | Uses `AutoModelForCausalLM` + `PeftModel`; `--interface unit_json` supported. |
| `src/v04/eval_runner.py` | N/A | Not used for LoRA eval. |
| `src/v04/metrics.py` | N/A | Not used for LoRA eval. |

**No script changes required.** Both train and eval scripts are model-agnostic via `AutoModel` and `trust_remote_code=True`.

## Known Caveats

1. **LoRA target_modules differ from v0.5b.** Qwen3.5's hybrid architecture (linear_attn + self_attn) requires 6 target modules vs 4 for Qwen3-4B. This is a forced design change, not an experiment variable tweak.

2. **Fewer total LoRA parameters.** Qwen3.5 has ~3.2M trainable parameters vs ~5.8M for Qwen3-4B (due to fewer layers and combined QKV in linear_attn). This is inherent to the architecture.

3. **Flash-linear-attention not installed.** The model loads with a warning about missing `fla` library. Falls back to torch implementation. Training will be functionally correct but potentially slower.

4. **Gold not fully blind.** Gold has been evaluated twice (v0.5 DSL 500, v0.5b JSON 500). v0.5c is the third evaluation on the same gold. Risk of implicit overfitting is low (no hyperparameter tuning on gold).

5. **Safety not targeted.** This experiment uses the same data as v0.5b, which has 6 sensitive failures in the train-pool but no dedicated safety weighting. Safety is future work.

## Pre-Smoke Verification Commands

The following should be run at the START of Context 5.9-B (before training):

```bash
# Verify gold hash unchanged
sha256sum data/v05/gold/v05_gold_corrected_cases.jsonl

# Verify train data exists
wc -l data/v05b/json_sft/v05b_train_125_json_sft_messages.jsonl

# Verify CUDA available
.venv/bin/python -c "import torch; print(torch.cuda.get_device_name(0))"

# Dry-run config parse
.venv/bin/python -c "import yaml; yaml.safe_load(open('configs/v05c/qwen35_lora_json_125.yaml'))"

# Run preflight (stops before training)
.venv/bin/python src/v05/train_lora_router.py --config configs/v05c/qwen35_lora_json_125.yaml
```

## Recommended Next Step

**Context 5.9-B: Qwen3.5 Unit JSON LoRA 125-case smoke training**

1. Run preflight check.
2. Train Qwen3.5 JSON LoRA 125.
3. Evaluate on dev.
4. Report: dev metrics, parse rate, vs Qwen3-4B JSON LoRA 125.
5. Decide: proceed to 250, adjust config, or abort.

---

*End of V0.5c Qwen3.5 JSON LoRA Readiness Report.*
