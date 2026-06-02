# V0.5 Qwen3-4B QLoRA 125-Case Smoke Runbook

**Date:** 2026-06-02  
**Context:** 5.5-A2 — exact training command for 125-case smoke  

---

## Pre-Flight Checks

Before training, verify:
```bash
sha256sum data/v05/gold/v05_gold_corrected_cases.jsonl
# Must be: 56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d
```

## Exact Training Command

```bash
cd /home/abc16/distilled-memory-policy-router

PYTHONDONTWRITEBYTECODE=1 accelerate launch \
  --config_file configs/v05/qwen3_4b_lora_dsl_125.yaml \
  src/v05/train_lora_router.py \
  --config configs/v05/qwen3_4b_lora_dsl_125.yaml
```

Or if using TRL SFTTrainer directly:

```bash
cd /home/abc16/distilled-memory-policy-router

PYTHONDONTWRITEBYTECODE=1 python src/v05/train_lora_router.py \
  --config configs/v05/qwen3_4b_lora_dsl_125.yaml
```

## Expected Output

```
results/v05_lora/qwen3_4b_dsl_125/
  ├── adapter_config.json
  ├── adapter_model.safetensors
  ├── checkpoint-8/
  ├── checkpoint-16/
  ├── checkpoint-24/
  └── trainer_state.json
```

## Expected Duration

~24 training steps at batch 16. With efficient loading, ~2-5 minutes on RTX 4070 SUPER.

## Dev Evaluation After Training

```bash
# Load best checkpoint and run dev predictions
PYTHONDONTWRITEBYTECODE=1 python src/v05/qwen_v05_output_runner.py \
  --model-path results/v05_lora/qwen3_4b_dsl_125 \
  --model-id qwen3_4b_lora_125 \
  --models-label qwen3_4b_lora_125 \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --out data/v05/model_predictions/qwen3_4b_lora_125_dev_predictions.jsonl \
  --split dev

# Evaluate
PYTHONDONTWRITEBYTECODE=1 python -m src.v04.eval_runner \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --predictions data/v05/model_predictions/qwen3_4b_lora_125_dev_predictions.jsonl \
  --report reports/v05/v05_qwen3_4b_lora_125_dev_report.md \
  --error-report reports/v05/v05_qwen3_4b_lora_125_dev_error_analysis.md
```

## Success Criteria for 125 Smoke

| Metric | Threshold |
|--------|:---------:|
| Training completes | No crash |
| Parse success (DSL) | ≥ 90% |
| STORE unit F1 | > Qwen3-4B DSL few-shot (0.936 on dev) |
| STORE target accuracy | > 60% |
| Sensitive store | = 0 |
| No output format collapse | DSL output looks correct |

## Failure Handling

| Symptom | Action |
|---------|--------|
| OOM | Reduce batch to 2, increase grad_accum to 8, or try smaller max_seq_length |
| Loss diverges (NaN or explosion) | Retry with lr=1e-4 |
| Parse success < 80% | Model format collapsed — check training data, reduce lr to 5e-5 |
| No improvement over few-shot | Training didn't help — check data quality, may need more epochs |
| Output invents targets/IDs | Training overfit — reduce epochs or increase regularization |

## Explicit Rules

- ❌ Do NOT evaluate on locked gold during or after 125 smoke
- ❌ Do NOT use gold for checkpoint selection
- ❌ Do NOT tune LR or config based on dev results during smoke (only for crash recovery)
- ✅ Dev only for all smoke evaluation
- ✅ Gold only for final evaluation after best 500 checkpoint selected

---

*End of V0.5 Qwen3-4B QLoRA 125 Smoke Runbook.*
