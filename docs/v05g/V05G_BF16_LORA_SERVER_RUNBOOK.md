# V05G BF16 LoRA Server Runbook (CORRECTED)

**Status:** ✅ Ready for server training  
**Date:** 2026-06-05 (corrected after ClaudeCode audit)

## Quick Reference

| Variant | Config | GPU | Train Data |
|---------|--------|-----|-----------|
| BF16 r16 500 | `qwen35_bf16_lora_json_r16_500.yaml` | L40S/A100 | 500-control SFT |
| BF16 r16 1000 | `qwen35_bf16_lora_json_r16_1000.yaml` | L40S/A100 | 1000-targeted SFT |
| BF16 r16 500 (4090) | `qwen35_bf16_lora_json_r16_500_4090.yaml` | RTX 4090 | 500-control SFT |
| BF16 r16 1000 (4090) | `qwen35_bf16_lora_json_r16_1000_4090.yaml` | RTX 4090 | 1000-targeted SFT |

## Prerequisites

```bash
# Set model path
export QWEN35_MODEL_PATH=/path/to/Qwen3.5-4B
test -d "$QWEN35_MODEL_PATH" && echo "✅ Model found"

# Create directories
mkdir -p logs/v05g results/v05g_bf16_lora \
  data/v05g/model_predictions reports/v05g/server_runs

# Install deps
pip install pydantic
```

## Training (L40S/A100)

```bash
tmux new -s v05g_500
source .venv/bin/activate
PYTHONDONTWRITEBYTECODE=1 python3 src/v05/train_lora_router.py \
  --config configs/v05g/qwen35_bf16_lora_json_r16_500.yaml \
  2>&1 | tee logs/v05g/v05g_bf16_r16_500_train.log
```

## Training (RTX 4090)

```bash
tmux new -s v05g_500_4090
source .venv/bin/activate
PYTHONDONTWRITEBYTECODE=1 python3 src/v05/train_lora_router.py \
  --config configs/v05g/qwen35_bf16_lora_json_r16_500_4090.yaml \
  2>&1 | tee logs/v05g/v05g_bf16_r16_500_4090_train.log
```

## Dev Evaluation (all variants)

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

Repeat for 1000 variant with appropriate adapter/prediction paths.

## Full Runbook

See: `reports/v05g/v05g_server_training_runbook.md` for complete step-by-step with hash verification, preflight, tmux workflow, OOM recovery, resume strategy, and artifact download.

## Codex Constraints

- ✅ Run commands, monitor logs, download artifacts
- ❌ Change metrics, modify gold_v2_009, run gold eval without instruction
- ❌ Git commit/push, delete checkpoints without approval
