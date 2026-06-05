# v05g Server Eval Command Verification (CORRECTED)

**Date:** 2026-06-05 (corrected after ClaudeCode eval pipeline audit)  
**Status:** ✅ Verified — eval pipeline confirmed with correct evaluator  
**No inference was run during this verification.**

## Script Existence

| Script | Path | Exists | Notes |
|--------|------|--------|-------|
| Training | `src/v05/train_lora_router.py` | ✅ | BF16 LoRA support, env vars, grad ckpt |
| Eval (inference) | `src/v05/eval_lora_router.py` | ✅ | Outputs predictions with `raw_output` field |
| Eval (metrics) | `src/evaluation/evaluate_predictions.py` | ✅ | **INCOMPATIBLE** — expects `target` field and `read_hints`/`write_spans`/`ignore_spans` schema |
| Eval (metrics, v05g) | `src/v05/evaluate_lora_predictions.py` | ✅ **NEW** | Bridges eval_lora_router output → Unit JSON metrics |

## Root Cause of Incompatibility

1. `eval_lora_router.py` outputs predictions with `raw_output` as a JSON string: `{"read": [...], "store": [...], "skip": [...]}`
2. `evaluate_predictions.py` (in `src/evaluation/`) expects predictions with a `target` dict containing `read_hints`/`write_spans`/`ignore_spans`
3. v05 dev cases use `gold` field, not `target`
4. These are fundamentally different schemas

## Fix: `evaluate_lora_predictions.py`

Created a v05-specific evaluator that:
- Reads DecisionCase JSONL with `gold` field (matches `data/v05/dev/v05_dev_cases.jsonl`)
- Reads prediction JSONL from `eval_lora_router.py` with `raw_output` field
- Parses `raw_output` using `src/v04/metrics._parse_unit_json`
- Computes metrics using `src/v04/metrics.evaluate_prediction_rows` (same as v05e)
- Outputs metrics JSON and summary MD

## Correct Dev Eval Commands

### BF16 r16 500

```bash
# Step 1: Generate predictions
python3 src/v05/eval_lora_router.py \
  --interface unit_json \
  --base-model "${QWEN35_MODEL_PATH}" \
  --adapter results/v05g_bf16_lora/qwen35_json_r16_500/adapter \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --out data/v05g/model_predictions/bf16_r16_500_dev_predictions.jsonl

# Step 2: Compute metrics
python3 src/v05/evaluate_lora_predictions.py \
  --gold data/v05/dev/v05_dev_cases.jsonl \
  --predictions data/v05g/model_predictions/bf16_r16_500_dev_predictions.jsonl \
  --run-id v05g_bf16_r16_500 \
  --split dev \
  --metrics-json reports/v05g/server_runs/v05g_bf16_r16_500_dev_metrics.json \
  --summary-md reports/v05g/server_runs/v05g_bf16_r16_500_dev_summary.md
```

### BF16 r16 1000

```bash
# Step 1
python3 src/v05/eval_lora_router.py \
  --interface unit_json \
  --base-model "${QWEN35_MODEL_PATH}" \
  --adapter results/v05g_bf16_lora/qwen35_json_r16_1000/adapter \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --out data/v05g/model_predictions/bf16_r16_1000_dev_predictions.jsonl

# Step 2
python3 src/v05/evaluate_lora_predictions.py \
  --gold data/v05/dev/v05_dev_cases.jsonl \
  --predictions data/v05g/model_predictions/bf16_r16_1000_dev_predictions.jsonl \
  --run-id v05g_bf16_r16_1000 \
  --split dev \
  --metrics-json reports/v05g/server_runs/v05g_bf16_r16_1000_dev_metrics.json \
  --summary-md reports/v05g/server_runs/v05g_bf16_r16_1000_dev_summary.md
```

### RTX 4090 Variants

Same eval commands, different adapter paths (e.g., `.../qwen35_json_r16_500_4090/adapter`).

## Smoke Test Verification

| Test | Result |
|------|--------|
| Perfect predictions → exact=1.0, parse=1.0, store_f1=1.0, skip_f1=1.0 | ✅ |
| Wrong predictions → exact=0.0 | ✅ |
| Malformed JSON → parse<1.0 | ✅ |
| Real dev data (20 cases) → all metrics correct | ✅ |
| Metrics JSON written | ✅ |
| Summary MD written | ✅ |

See: `reports/v05g/v05g_eval_pipeline_smoke_test_report.md`

## What Changed From Previous (Invalid) Runbook

| Before | After |
|--------|-------|
| `src/evaluation/evaluate_predictions.py` | `src/v05/evaluate_lora_predictions.py` |
| `--gold data/v05/dev/v05_dev_cases.jsonl` | Same ✅ |
| Predictions with `target` dict | Predictions with `raw_output` string ✅ |
| `read_hints`/`write_spans`/`ignore_spans` schema | `read`/`store`/`skip` schema ✅ |
| `evaluate_predictions.py --help` args | `evaluate_lora_predictions.py --help` args (same arg names) ✅ |
