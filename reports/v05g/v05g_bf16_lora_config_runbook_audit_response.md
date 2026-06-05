# v05g BF16 LoRA Config/Runbook Audit Response

**Date:** 2026-06-05  
**Auditor:** ClaudeCode (Windows) / DeepSeek independent audit  
**Verdict:** CORRECTION REQUIRED → All issues fixed  
**Response:** All 4 blockers resolved

## Issues Found and Fixes

### Blocker 1: Wrong Eval Commands ✅ FIXED

| Issue | Fix |
|-------|-----|
| `src/v05/run_model_eval.py` does not exist | Replaced with `src/v05/eval_lora_router.py` ✅ |
| Wrong arguments `--eval_file` / `--output` | Correct arguments: `--cases`, `--out`, `--adapter`, `--base-model` ✅ |
| Missing metrics step | Added `src/evaluation/evaluate_predictions.py` commands ✅ |
| `--cases` takes DecisionCase, not SFT format | Documented correct data path: `data/v05/dev/v05_dev_cases.jsonl` ✅ |

**Verification:** `eval_lora_router.py --help` and `evaluate_predictions.py --help` confirmed. No inference was run.

See: `reports/v05g/v05g_server_eval_command_verification.md`

### Blocker 2: Missing logs/ Directories ✅ FIXED

Added to runbook Step 1a:
```bash
mkdir -p logs/v05g
mkdir -p results/v05g_bf16_lora
mkdir -p data/v05g/model_predictions
mkdir -p reports/v05g/server_runs
```

All `tee` paths now have existing parent directories.

### Blocker 3: Hardcoded Model Path ✅ FIXED

| Before | After |
|--------|-------|
| `base_model_path: /home/abc16/hf_models/Qwen3.5-4B` | `base_model_path: "${QWEN35_MODEL_PATH}"` |

**Script changes:** Added `_resolve_path()` with `os.path.expandvars` and `os.path.expanduser`. Resolved path printed in preflight. Works with both env vars and absolute paths.

**Runbook:** Added `export QWEN35_MODEL_PATH=/path/to/Qwen3.5-4B` to setup.

### Blocker 4: Gradient Checkpointing Not Supported ✅ FIXED

**Script changes:**
1. New config field: `gradient_checkpointing: true/false` (default false)
2. When true:
   - `model.config.use_cache = False`
   - `model.gradient_checkpointing_enable()`
   - Falls back to `enable_input_require_grads()` for PEFT compat
3. Passed to `TrainingArguments`
4. Logged in training output

**Config changes:**
- Main configs: no `gradient_checkpointing` (defaults to false)
- 4090 configs: `gradient_checkpointing: true`

## Verification

| # | Check | Result |
|---|-------|--------|
| 1 | `py_compile src/v05/train_lora_router.py` | ✅ |
| 2 | 4 v05g configs YAML parse | ✅ |
| 3 | Old v05c/v05d configs parse | ✅ |
| 4 | Env var expansion `${QWEN35_MODEL_PATH}` | ✅ |
| 5 | `gradient_checkpointing` default = false | ✅ (backward compat) |
| 6 | 4090 configs have `gradient_checkpointing: true` | ✅ |
| 7 | Data hashes (6/6) verified | ✅ |
| 8 | gold_v2_009 hash unchanged | ✅ |
| 9 | No training/inference run | ✅ |
| 10 | No data files modified | ✅ |

## Files Modified

| File | Change |
|------|--------|
| `src/v05/train_lora_router.py` | Env var resolution + gradient checkpointing |
| `configs/v05g/qwen35_bf16_lora_json_r16_500.yaml` | `${QWEN35_MODEL_PATH}` |
| `configs/v05g/qwen35_bf16_lora_json_r16_1000.yaml` | `${QWEN35_MODEL_PATH}` |
| `reports/v05g/v05g_server_training_runbook.md` | Full rewrite with correct commands |
| `reports/v05g/v05g_dev_eval_plan.md` | Corrected eval pipeline |
| `reports/v05g/v05g_server_resource_plan.md` | Added 4090 config matrix |
| `reports/v05g/v05g_bf16_lora_config_report.md` | Updated with audit fixes |
| `docs/v05g/V05G_BF16_LORA_SERVER_RUNBOOK.md` | Corrected quick reference |

## Files Created

| File | Purpose |
|------|---------|
| `configs/v05g/qwen35_bf16_lora_json_r16_500_4090.yaml` | 4090 fallback config |
| `configs/v05g/qwen35_bf16_lora_json_r16_1000_4090.yaml` | 4090 fallback config |
| `reports/v05g/v05g_server_eval_command_verification.md` | Eval CLI verification |
| `reports/v05g/v05g_bf16_lora_config_runbook_audit_response.md` | This file |
| `reports/v05g/v05g_4090_fallback_config_report.md` | 4090 config documentation |

## Files Preserved (Unchanged)

- All `data/v05g/` files (hashes verified)
- `data/v05e/gold_v2/` (hash verified)
- Old QLoRA configs (`configs/v05c/`, `configs/v05d/`)
- `data/v05/dev/v05_dev_cases.jsonl`
