# v05g BF16 LoRA — Server Training Runbook (CORRECTED)

**Date:** 2026-06-05 (corrected 2026-06-05 after ClaudeCode audit)  
**Server:** To be rented (recommended: L40S 48GB, A100 40GB; fallback: RTX 4090 24GB)  
**Model:** Qwen3.5-4B  
**Training:** BF16 standard LoRA r=16  

**Corrections from audit:**
- Eval commands fixed: use `eval_lora_router.py` + `evaluate_lora_predictions.py`, not nonexistent `run_model_eval.py`
- Model path configurable via `QWEN35_MODEL_PATH` env var
- Gradient checkpointing supported for RTX 4090
- Directory creation commands added before training/eval
- 4090 fallback configs created

---

## Step 0: Server Setup

### GPU Recommendation
- **Primary:** L40S 48GB or A100 40GB (comfortable for batch_size=4, no gradient checkpointing)
- **Fallback:** RTX 4090 24GB (needs 4090 configs with batch_size=2 + gradient checkpointing)

### Repository Upload
```bash
# Option A: git clone
git clone <repo_url> /workspace/distilled-memory-policy-router
cd /workspace/distilled-memory-policy-router

# Option B: rsync
rsync -avz --exclude '.venv' --exclude '__pycache__' --exclude 'checkpoints' \
  --exclude 'models' --exclude 'outputs' --exclude 'wandb' --exclude '*.log' \
  ~/distilled-memory-policy-router/ user@server:/workspace/distilled-memory-policy-router/
```

### Python Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install torch transformers peft trl datasets accelerate bitsandbytes pyyaml pydantic
```

### Model Path Setup
```bash
# Set the environment variable (adjust path to your server's model location)
export QWEN35_MODEL_PATH=/path/to/Qwen3.5-4B

# Verify
test -d "$QWEN35_MODEL_PATH" && echo "✅ Model found" || echo "❌ Model not found"
ls -lah "$QWEN35_MODEL_PATH" | head -5
```

---

## Step 1: Pre-Training Verification

### 1a. Create required directories
```bash
mkdir -p logs/v05g
mkdir -p results/v05g_bf16_lora
mkdir -p data/v05g/model_predictions
mkdir -p reports/v05g/server_runs
```

### 1b. Data Hash Verification
```bash
python3 -c "
import hashlib, json
lock = json.load(open('data/v05g/v05g_training_data_lock.json'))
for name, info in lock['files'].items():
    h = hashlib.sha256(open(info['path'],'rb').read()).hexdigest()
    match = '✅' if h == info['sha256'] else '❌'
    print(f'{match} {name}: {h[:16]}...')
"

# Verify gold_v2_009 unchanged
sha256sum data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl
# Expected: f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72
```

### 1c. Config Verification
```bash
# Verify QWEN35_MODEL_PATH is set
echo "Model path: $QWEN35_MODEL_PATH"

# Verify main configs
python3 -c "
import yaml, os
for p in ['configs/v05g/qwen35_bf16_lora_json_r16_500.yaml',
          'configs/v05g/qwen35_bf16_lora_json_r16_1000.yaml']:
    c = yaml.safe_load(open(p))
    mp = os.path.expandvars(c['base_model_path'])
    print(f'{p.split(\"/\")[-1]}: quant={c[\"quantization\"]}, r={c[\"lora_r\"]}, '
          f'model={mp}, exists={os.path.isdir(mp)}')
"

# If on RTX 4090, also verify fallback configs
python3 -c "
import yaml, os
for p in ['configs/v05g/qwen35_bf16_lora_json_r16_500_4090.yaml',
          'configs/v05g/qwen35_bf16_lora_json_r16_1000_4090.yaml']:
    c = yaml.safe_load(open(p))
    mp = os.path.expandvars(c['base_model_path'])
    assert c.get('gradient_checkpointing') == True, f'{p}: gradient_checkpointing not enabled'
    print(f'{p.split(\"/\")[-1]}: gp_ckpt={c[\"gradient_checkpointing\"]}, '
          f'bs={c[\"per_device_train_batch_size\"]}, ga={c[\"gradient_accumulation_steps\"]}')
"
```

### 1d. CUDA Check
```bash
python3 -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem // 1024**3} GB')
"
```

---

## Step 2: BF16 r16 500 Training

Choose the appropriate config:

| GPU | Config |
|-----|--------|
| L40S / A100 40GB+ | `configs/v05g/qwen35_bf16_lora_json_r16_500.yaml` |
| RTX 4090 24GB | `configs/v05g/qwen35_bf16_lora_json_r16_500_4090.yaml` |

```bash
tmux new -s v05g_500
source .venv/bin/activate

# L40S/A100:
PYTHONDONTWRITEBYTECODE=1 python3 src/v05/train_lora_router.py \
  --config configs/v05g/qwen35_bf16_lora_json_r16_500.yaml \
  2>&1 | tee logs/v05g/v05g_bf16_r16_500_train.log

# RTX 4090:
PYTHONDONTWRITEBYTECODE=1 python3 src/v05/train_lora_router.py \
  --config configs/v05g/qwen35_bf16_lora_json_r16_500_4090.yaml \
  2>&1 | tee logs/v05g/v05g_bf16_r16_500_4090_train.log

# Detach: Ctrl+B, D | Reattach: tmux attach -t v05g_500
```

**Expected output:**
```
PREFLIGHT CHECK
✅ Resolved model path: /path/to/Qwen3.5-4B
✅ train: data/v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl
✅ eval: data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl
✅ train rows: 500  |  eval rows: 100
✅ Quantization mode: none
✅ PREFLIGHT PASSED

TRAINING
Quantization: none
Loading model in BF16 (standard LoRA, no quantization)...
Gradient checkpointing: disabled (or "Enabling gradient checkpointing..." for 4090)
```

---

## Step 3: BF16 r16 500 Dev Evaluation

```bash
tmux new -s v05g_500_eval
source .venv/bin/activate

# Step 1: Generate predictions (use correct adapter path for your config)
python3 src/v05/eval_lora_router.py \
  --interface unit_json \
  --base-model "${QWEN35_MODEL_PATH}" \
  --adapter results/v05g_bf16_lora/qwen35_json_r16_500/adapter \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --out data/v05g/model_predictions/bf16_r16_500_dev_predictions.jsonl \
  2>&1 | tee logs/v05g/v05g_bf16_r16_500_eval.log

# Step 2: Compute metrics
python3 src/v05/evaluate_lora_predictions.py \
  --gold data/v05/dev/v05_dev_cases.jsonl \
  --predictions data/v05g/model_predictions/bf16_r16_500_dev_predictions.jsonl \
  --run-id v05g_bf16_r16_500 \
  --split dev \
  --metrics-json reports/v05g/server_runs/v05g_bf16_r16_500_dev_metrics.json \
  --summary-md reports/v05g/server_runs/v05g_bf16_r16_500_dev_summary.md
```

---

## Step 4: BF16 r16 1000 Training

```bash
tmux new -s v05g_1000
source .venv/bin/activate

# L40S/A100:
PYTHONDONTWRITEBYTECODE=1 python3 src/v05/train_lora_router.py \
  --config configs/v05g/qwen35_bf16_lora_json_r16_1000.yaml \
  2>&1 | tee logs/v05g/v05g_bf16_r16_1000_train.log

# RTX 4090:
PYTHONDONTWRITEBYTECODE=1 python3 src/v05/train_lora_router.py \
  --config configs/v05g/qwen35_bf16_lora_json_r16_1000_4090.yaml \
  2>&1 | tee logs/v05g/v05g_bf16_r16_1000_4090_train.log
```

---

## Step 5: BF16 r16 1000 Dev Evaluation

```bash
tmux new -s v05g_1000_eval
source .venv/bin/activate

# Step 1: Generate predictions
python3 src/v05/eval_lora_router.py \
  --interface unit_json \
  --base-model "${QWEN35_MODEL_PATH}" \
  --adapter results/v05g_bf16_lora/qwen35_json_r16_1000/adapter \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --out data/v05g/model_predictions/bf16_r16_1000_dev_predictions.jsonl \
  2>&1 | tee logs/v05g/v05g_bf16_r16_1000_eval.log

# Step 2: Compute metrics
python3 src/v05/evaluate_lora_predictions.py \
  --gold data/v05/dev/v05_dev_cases.jsonl \
  --predictions data/v05g/model_predictions/bf16_r16_1000_dev_predictions.jsonl \
  --run-id v05g_bf16_r16_1000 \
  --split dev \
  --metrics-json reports/v05g/server_runs/v05g_bf16_r16_1000_dev_metrics.json \
  --summary-md reports/v05g/server_runs/v05g_bf16_r16_1000_dev_summary.md
```

---

## OOM Recovery

If training OOMs on L40S/A100 (unlikely but possible):

### Tier 1: Gradient Checkpointing
Edit config to add: `gradient_checkpointing: true`

### Tier 2: Reduce batch size
```yaml
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
```

### Tier 3: QLoRA fallback (last resort)
```yaml
quantization: "4bit"
# Defeats BF16 purpose for 500 variant. Document if used.
```

---

## Resume Strategy

- TrainingArguments `save_strategy: epoch` saves checkpoint after each epoch
- Checkpoints in `results/v05g_bf16_lora/qwen35_json_r16_<N>/checkpoint-<N>/`
- To resume: trainer automatically resumes from latest checkpoint if output_dir exists

---

## Artifact Packing / Download

```bash
# Create archive
tar -czf v05g_bf16_results.tar.gz \
  results/v05g_bf16_lora/ \
  logs/v05g/ \
  data/v05g/model_predictions/ \
  reports/v05g/server_runs/

# Download
scp user@server:/workspace/distilled-memory-policy-router/v05g_bf16_results.tar.gz .
```

---

## Codex Constraints

| Allowed | Forbidden |
|---------|-----------|
| Run training/eval commands | Change metrics |
| Monitor logs via `tail -f` | Modify gold_v2_009 |
| Download artifacts | Run gold evaluation (unless explicitly instructed) |
| Create summary reports | Git commit/push |
| Run preflight checks | Delete checkpoints without approval |
| Help debug OOM | Modify data files |
| Install Python packages | Change training hyperparameters mid-run |
