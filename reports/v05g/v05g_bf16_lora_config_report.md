# v05g BF16 LoRA Config Report (CORRECTED)

**Date:** 2026-06-05 (corrected after ClaudeCode audit)  
**Status:** All configs verified, script compiles, old configs backward-compatible

## Config Files

| Config | Path | Purpose | GPU |
|--------|------|---------|-----|
| BF16 r16 500 | `configs/v05g/qwen35_bf16_lora_json_r16_500.yaml` | Main 500 on L40S/A100 | 40GB+ |
| BF16 r16 1000 | `configs/v05g/qwen35_bf16_lora_json_r16_1000.yaml` | Main 1000 on L40S/A100 | 40GB+ |
| BF16 r16 500 (4090) | `configs/v05g/qwen35_bf16_lora_json_r16_500_4090.yaml` | Fallback 500 on RTX 4090 | 24GB |
| BF16 r16 1000 (4090) | `configs/v05g/qwen35_bf16_lora_json_r16_1000_4090.yaml` | Fallback 1000 on RTX 4090 | 24GB |

## Config Verification

| Check | Result |
|-------|--------|
| All 4 v05g configs parse via YAML | ✅ |
| Training script compiles (`py_compile`) | ✅ |
| Old QLoRA configs still parse (v05c, v05d) | ✅ (quantization defaults to "4bit") |
| Env var `${QWEN35_MODEL_PATH}` resolves correctly | ✅ |
| Train paths exist | ✅ |
| Eval path exists (`data/v05/dev/v05_dev_cases.jsonl`) | ✅ |
| Data hashes match lock manifest | ✅ (6/6) |
| gold_v2_009 hash unchanged | ✅ (`f5cf7be1...`) |

## Training Script Changes (from audit)

| # | Change | Purpose |
|---|--------|---------|
| 1 | `_resolve_path()` with `os.path.expandvars`/`expanduser` | Configurable model path via `${QWEN35_MODEL_PATH}` |
| 2 | `gradient_checkpointing` config field (default false) | OOM fallback for RTX 4090 |
| 3 | `model.config.use_cache = False` when grad ckpt enabled | Required for gradient checkpointing |
| 4 | `model.gradient_checkpointing_enable()` when enabled | Enables activation checkpointing |
| 5 | `gradient_checkpointing` passed to `TrainingArguments` | Trainer integration |
| 6 | Resolved model path printed in preflight | Debugging aid |

### Backward Compatibility

| Config | `quantization` | `gradient_checkpointing` | Effect |
|--------|---------------|--------------------------|--------|
| v05c/v05d | Missing → "4bit" | Missing → `False` | Same as before ✅ |
| v05g main | `"none"` | Missing → `False` | BF16 LoRA, no grad ckpt ✅ |
| v05g 4090 | `"none"` | `True` | BF16 LoRA + grad ckpt ✅ |

## Audit Fixes Applied

| Issue | Fix |
|-------|-----|
| Model path hardcoded to `/home/abc16/...` | Uses `${QWEN35_MODEL_PATH}` env var |
| `gradient_checkpointing` not supported in script | Added full support (config field + model calls) |
| 4090 fallback needed configs | Created both 4090 configs |
| `logs/` directory missing | Added `mkdir -p` in runbook |
| Eval commands used nonexistent script | Fixed to `eval_lora_router.py` + `evaluate_predictions.py` |
