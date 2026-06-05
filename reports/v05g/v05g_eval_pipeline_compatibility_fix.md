# v05g Eval Pipeline Compatibility Fix

**Date:** 2026-06-05  
**Auditor:** ClaudeCode engineering audit  
**Issue:** `eval_lora_router.py` → `evaluate_predictions.py` incompatible — different prediction and gold schemas  
**Fix:** Created `src/v05/evaluate_lora_predictions.py` (Option A)

## Root Cause

Two fundamental incompatibilities between the eval pipeline components:

### 1. Prediction Format Mismatch

| Component | Output/Input Field | Schema |
|-----------|-------------------|--------|
| `eval_lora_router.py` | `raw_output` (JSON string) | `{"read": [...], "store": [...], "skip": [...]}` |
| `evaluate_predictions.py` (src/evaluation/) | `target` (dict) | `{"read_hints": [...], "write_spans": [...], "ignore_spans": [...]}` |

`evaluate_predictions.py` looks for `prediction.get("target")` but `eval_lora_router.py` writes `raw_output`.

### 2. Gold Schema Mismatch

| File | Field | Schema |
|------|-------|--------|
| `data/v05/dev/v05_dev_cases.jsonl` | `gold` | `{"read": [...], "store": [...], "skip": [...]}` |
| `evaluate_predictions.py` expects | `target` | `{"read_hints": [...], "write_spans": [...], "ignore_spans": [...]}` |

`evaluate_predictions.py` uses `gold_case["target"]` but v05 DecisionCase files use `gold_case["gold"]`.

### 3. Interface Evolution

The v05 project evolved from `read_hints`/`write_spans`/`ignore_spans` (original spec) to `read`/`store`/`skip` (Unit JSON). The `src/evaluation/evaluate_predictions.py` was built for the original schema. The v05e evaluation used `src/v04/metrics.evaluate_prediction_rows` which already supports both interfaces.

## Chosen Fix: Option A (New Evaluator)

Created `src/v05/evaluate_lora_predictions.py` — a thin CLI wrapper around `src/v04/metrics.evaluate_prediction_rows` with `interface="unit_json"`.

**Why Option A:**
- `evaluate_predictions.py` is built for a fundamentally different schema (`read_hints`/`write_spans`/`ignore_spans`)
- The v04 metrics module already has robust Unit JSON parsing and evaluation
- v05e gold_v2_009 evaluation used this same metrics code
- Creating a wrapper avoids breaking the old pipeline

## Verification

| Check | Result |
|-------|--------|
| `py_compile src/v05/evaluate_lora_predictions.py` | ✅ |
| `--help` output correct | ✅ |
| Perfect predictions → exact=1.0, parse=1.0, store_f1=1.0 | ✅ |
| Wrong predictions → exact=0.0 | ✅ |
| Malformed JSON → parse<1.0 | ✅ |
| Real dev data (20 cases) → all metrics correct | ✅ |
| Metrics JSON + Summary MD written | ✅ |
| No model inference run | ✅ |

## Impact on v05g Server Runbook

| Eval Step | Before (Invalid) | After (Fixed) |
|-----------|-----------------|---------------|
| Step 2 script | `src/evaluation/evaluate_predictions.py` | `src/v05/evaluate_lora_predictions.py` |
| Prediction field expected | `target` dict | `raw_output` string ✅ |
| Gold field expected | `target` | `gold` ✅ |
| Schema | `read_hints`/`write_spans`/`ignore_spans` | `read`/`store`/`skip` ✅ |
| Additional dep | pydantic | None (uses standard library) ✅ |

## Files Created

| File | Purpose |
|------|---------|
| `src/v05/evaluate_lora_predictions.py` | v05-specific Unit JSON evaluator |
| `reports/v05g/v05g_eval_pipeline_smoke_test_report.md` | Smoke test verification |
| `reports/v05g/v05g_eval_pipeline_compatibility_fix.md` | This file |

## Files Updated

| File | Change |
|------|--------|
| `reports/v05g/v05g_server_training_runbook.md` | Updated eval commands |
| `reports/v05g/v05g_dev_eval_plan.md` | Updated eval pipeline |
| `docs/v05g/V05G_BF16_LORA_SERVER_RUNBOOK.md` | Updated eval commands |
| `reports/v05g/v05g_server_eval_command_verification.md` | Updated verification |
| `reports/v05g/v05g_bf16_lora_server_readiness_decision.md` | Updated readiness |
