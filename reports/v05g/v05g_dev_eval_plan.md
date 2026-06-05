# v05g BF16 LoRA — Dev Evaluation Plan (CORRECTED)

**Date:** 2026-06-05 (corrected after ClaudeCode audit)  
**Eval data:** `data/v05/dev/v05_dev_cases.jsonl` (100 DecisionCase examples)  
**Eval pipeline:**
1. `src/v05/eval_lora_router.py` — generate predictions from adapter
2. `src/v05/evaluate_lora_predictions.py` — compute metrics from predictions

## Eval Commands

### Step 1: Generate Predictions
```bash
python3 src/v05/eval_lora_router.py \
  --interface unit_json \
  --base-model "${QWEN35_MODEL_PATH}" \
  --adapter <adapter_path> \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --out <predictions_output_path>
```

### Step 2: Compute Metrics
```bash
python3 src/v05/evaluate_lora_predictions.py \
  --gold data/v05/dev/v05_dev_cases.jsonl \
  --predictions <predictions_output_path> \
  --run-id <run_id> \
  --split dev \
  --metrics-json <metrics_json_path> \
  --summary-md <summary_md_path>
```

## Comparison Matrix

| # | Comparison | Baseline | Candidate | Purpose |
|---|-----------|----------|-----------|---------|
| 1 | BF16 r16 500 vs QLoRA r16 500 | v05d QLoRA r16 500 | v05g BF16 r16 500 | Precision comparison |
| 2 | BF16 r16 500 vs QLoRA r8 500 | v05c QLoRA r8 500 | v05g BF16 r16 500 | Rank + precision |
| 3 | BF16 r16 1000 vs BF16 r16 500 | v05g BF16 r16 500 | v05g BF16 r16 1000 | Data + domain scaling |

## Metrics

Reported by `evaluate_lora_predictions.py`:
- parse rate (% valid JSON)
- full exact match
- store/skip exact match
- STORE F1, SKIP F1
- target accuracy
- Read precision/recall (if available)

## Output Paths

| Variant | Predictions | Metrics JSON | Summary MD |
|---------|------------|-------------|------------|
| BF16 r16 500 | `data/v05g/model_predictions/bf16_r16_500_dev_predictions.jsonl` | `reports/v05g/server_runs/v05g_bf16_r16_500_dev_metrics.json` | `reports/v05g/server_runs/v05g_bf16_r16_500_dev_summary.md` |
| BF16 r16 1000 | `data/v05g/model_predictions/bf16_r16_1000_dev_predictions.jsonl` | `reports/v05g/server_runs/v05g_bf16_r16_1000_dev_metrics.json` | `reports/v05g/server_runs/v05g_bf16_r16_1000_dev_summary.md` |
| 4090 variants | `..._4090_dev_predictions.jsonl` | `..._4090_dev_metrics.json` | `..._4090_dev_summary.md` |

## Interpretation Guardrails

### For Comparison 1 (BF16 vs QLoRA, same data)
- If BF16 > QLoRA: BF16 precision benefits the task
- If BF16 ≈ QLoRA: Quantization doesn't hurt for this task/model
- If BF16 < QLoRA: Surprising; check for training issues

### For Comparison 3 (1000 vs 500)
- Interpret as "more data + broader domains" not "pure data volume"
- See `v05g_repaired_training_data_limitations.md` for confound documentation

## What NOT to Do

| ❌ Forbidden | ✅ Allowed |
|-------------|-----------|
| Evaluate on gold_v2_009 | Evaluate on dev only |
| Tune hyperparameters on dev | Run single evaluation per trained variant |
| Claim statistical significance | Report descriptive metrics |
