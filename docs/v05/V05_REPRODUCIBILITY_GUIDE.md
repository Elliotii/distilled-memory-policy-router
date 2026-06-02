# V0.5 Reproducibility Guide

## Environment

- WSL Ubuntu, RTX 4070 SUPER 11GB
- Qwen3-4B: `/home/abc16/hf_models/Qwen3-4B-Instruct-2507`
- Qwen3.5: `/home/abc16/hf_models/Qwen3.5-4B`
- Python 3.12, PyTorch 2.6, CUDA 12.4

## Key Commands

### Prompting baselines
```bash
python src/v05/qwen_v05_output_runner.py \
  --model-path /home/abc16/hf_models/Qwen3-4B-Instruct-2507 \
  --model-id qwen3_4b --models-label qwen3_4b \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --out predictions.jsonl --split dev
```

### Evaluation
```bash
python -m src.v04.eval_runner \
  --cases cases.jsonl --predictions predictions.jsonl \
  --report report.md --error-report errors.md
```

### LoRA training
```bash
python src/v05/train_lora_router.py \
  --config configs/v05/qwen3_4b_lora_dsl_500.yaml
```

### LoRA eval
```bash
python src/v05/eval_lora_router.py \
  --base-model /home/abc16/hf_models/Qwen3-4B-Instruct-2507 \
  --adapter results/v05_lora/qwen3_4b_dsl_500/adapter \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --out predictions.jsonl
```

### Leakage check
```bash
python -m src.v05.check_leakage \
  --train train.jsonl --candidate candidate.jsonl --out report.md
```

## Splits

| Split | Path | Usage |
|-------|------|-------|
| Train | `data/v05/train/v05_train_pool_500_cases.jsonl` | Training |
| Dev | `data/v05/dev/v05_dev_cases.jsonl` | Model selection |
| Gold | `data/v05/gold/v05_gold_corrected_cases.jsonl` | Final eval only |

## Locked Gold Rules

- Gold hash: `56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d`
- Final evaluation only — not for tuning, checkpoint selection, or prompt design

## Warnings

- Do not commit API keys, .env, or model files
- Model adapters and predictions may be large
- Gold must remain immutable
