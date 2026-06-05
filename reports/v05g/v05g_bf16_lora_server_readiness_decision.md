# v05g BF16 LoRA — Server Readiness Decision (CORRECTED v3)

**Date:** 2026-06-05 (corrected after ClaudeCode eval pipeline audit)  
**Decision:** **Option A — Configs, scripts, evaluator, and runbook are ready for independent re-audit and server training.**

## Audit Corrections Applied (Cumulative)

| # | Issue | Fix | Verified |
|---|-------|-----|----------|
| C2-1 | Eval commands used nonexistent script | Fixed to `eval_lora_router.py` + `evaluate_predictions.py` | ✅ |
| C2-2 | `logs/` directory not created | Added `mkdir -p` commands | ✅ |
| C2-3 | Model path hardcoded | Uses `${QWEN35_MODEL_PATH}` env var | ✅ |
| C2-4 | `gradient_checkpointing` unsupported | Full support in training script + 4090 configs | ✅ |
| **C3-1** | **`evaluate_predictions.py` incompatible with `eval_lora_router.py`** | **Created `evaluate_lora_predictions.py`** | **✅ smoke tested** |

## Readiness Checklist

| # | Check | Result |
|---|-------|--------|
| 1 | Configs parse (4 v05g + 2 old) | ✅ |
| 2 | `train_lora_router.py` compiles | ✅ |
| 3 | `evaluate_lora_predictions.py` compiles | ✅ |
| 4 | Old QLoRA configs backward-compatible | ✅ |
| 5 | Env var `${QWEN35_MODEL_PATH}` resolves | ✅ |
| 6 | `gradient_checkpointing` default = false (backward compat) | ✅ |
| 7 | 4090 configs have `gradient_checkpointing: true` | ✅ |
| 8 | Data hashes verified (6/6) | ✅ |
| 9 | gold_v2_009 hash unchanged | ✅ |
| 10 | No training/evaluation run | ✅ |
| 11 | No data files modified | ✅ |
| 12 | Eval pipeline smoke tested (perfect/wrong/malformed/real data) | ✅ |
| 13 | All `tee` paths have parent dirs | ✅ |
| 14 | 4090 fallback configs created and parse | ✅ |

## Evaluator Verification

| Smoke Test | Result |
|------------|--------|
| Perfect predictions → exact=1.0, parse=1.0, store_f1=1.0, skip_f1=1.0 | ✅ |
| Wrong predictions → exact=0.0 | ✅ |
| Malformed JSON → parse<1.0 (2/3 parsed) | ✅ |
| Real dev data (20 cases) → all metrics correct | ✅ |
| E2E CLI pipeline (temp files) → exit 0, metrics + summary written | ✅ |

See: `reports/v05g/v05g_eval_pipeline_smoke_test_report.md`

## Recommendation

**Proceed to server rental and training.** Priority: L40S 48GB / A100 40GB with main configs.

1. Set `QWEN35_MODEL_PATH`, create dirs, verify hashes
2. Train BF16 r16 500
3. Eval BF16 r16 500 on dev (`eval_lora_router.py` → `evaluate_lora_predictions.py`)
4. Train BF16 r16 1000
5. Eval BF16 r16 1000 on dev
6. Compare using dev eval plan metrics
7. **Do NOT evaluate gold_v2_009** until explicitly instructed
