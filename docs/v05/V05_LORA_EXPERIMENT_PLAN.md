# V0.5 LoRA Experiment Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — LoRA/SFT training experiment design
Context: 5.4-A

---

## 1. Training Input

### 1.1 Data Source

| Item | Value |
|------|-------|
| Training file | `data/v05/batches/v05_batch500_corrected_cases.jsonl` |
| SFT format | `data/v05/batches/v05_batch500_corrected_sft_messages.jsonl` |
| Assistant content | gold.dsl only (Unit DSL) |
| Few-shot examples | Drawn from train-pool only |
| Cases | 500 total |
| Label provenance | LLM-assisted generation + review fixes |

### 1.2 Data Preprocessing

- All training data is Unit DSL formatted (system + user + assistant messages)
- No dev or gold cases in training data
- Text is pre-tokenized by the model's tokenizer
- No data augmentation in initial experiment
- Shuffled labels variant is optional sanity check (postponed)

## 2. Learning Curve Design

### 2.1 Nested Subsets

```
Full train-pool: 500 cases
  ├── 250 subset: first 250 cases
  │     └── 125 subset: first 125 cases
```

### 2.2 Fixed Case ID Lists

To ensure reproducibility, fixed case_id lists should be created before training:

```
data/v05/train/v05_train_125_case_ids.txt
data/v05/train/v05_train_250_case_ids.txt
data/v05/train/v05_train_500_case_ids.txt
```

The subsets are nested: 125 ⊂ 250 ⊂ 500. This allows measuring whether more training data improves routing performance.

### 2.3 Evaluation Order

| Step | Data | Purpose |
|------|------|---------|
| Train 125 | 125 train cases | Smallest training set |
| Evaluate on dev | 100 dev cases | Checkpoint selection |
| Train 250 | 250 train cases | Medium training set |
| Evaluate on dev | 100 dev cases | Checkpoint selection |
| Train 500 | 500 train cases | Full training set |
| Evaluate on dev | 100 dev cases | Checkpoint selection |
| **Final eval on gold** | **100 locked gold** | **Final report only** |

## 3. Base Model Choice

### 3.1 Default: Qwen3-4B-Instruct-2507

Qwen3-4B is the default base model:
- Present locally (7.6 GB)
- Known to work with existing runner scripts
- Fits RTX 4070 SUPER 11GB with LoRA
- Established training configs available (LoRA rank 8, alpha 16, etc.)

### 3.2 Option: Qwen3.5-4B (If Available)

If Qwen3.5-4B is acquired and outperforms Qwen3-4B on dev baselines:
- Switch base model to Qwen3.5-4B for LoRA experiments
- Re-use same training pipeline with different model path
- Compare both Qwen3-LoRA and Qwen3.5-LoRA if resources allow

Decision: Evaluate baselines first, then choose base model.

## 4. Training Configuration

### 4.1 LoRA Hyperparameters (Initial)

| Parameter | Value | Notes |
|-----------|-------|-------|
| LoRA rank (r) | 8 | Standard for 4B models |
| LoRA alpha | 16 | 2× rank |
| Target modules | q_proj, v_proj, k_proj, o_proj | Attention only (conservative) |
| Learning rate | 2e-4 | Conservative start |
| Batch size | 4 | Fit in 11GB VRAM |
| Gradient accumulation | 4 | Effective batch 16 |
| Epochs | 3 | Monitor for overfitting |
| Optimizer | AdamW 8-bit | Memory efficient |
| LR scheduler | Cosine with warmup | Standard |

### 4.2 Training Infrastructure

| Component | Option |
|-----------|--------|
| Framework | Hugging Face PEFT + TRL (SFTTrainer) |
| Precision | bfloat16 (if supported) or float16 |
| Gradient checkpointing | Enabled (memory saving) |
| Logging | WandB or TensorBoard |

## 5. Go / No-Go Criteria

### 5.1 Must Pass Before Gold Evaluation

| Gate | Threshold | Check On |
|------|:---------:|----------|
| parse_success | ≥ 96% | Dev |
| sensitive_store_count | = 0 | Dev |
| store_unit_f1 | > qwen_few_shot_dsl on dev | Dev |
| store_target_accuracy | > qwen_few_shot_dsl on dev | Dev |
| No target collapse | ≤ 80% to any single target | Dev |

### 5.2 Partial Go

If training improves over few-shot on dev but falls short of DeepSeek teacher:
- Acceptable — student model is smaller
- Document the gap
- Report teacher ceiling for context

### 5.3 No-Go Scenarios

| Failure | Action |
|---------|--------|
| parse_success < 90% | Debug output format, may need training data fixes |
| sensitive_store > 0 | **Hard No-Go** — model is unsafe |
| Target collapse | Training failed — model defaults to one target |
| No improvement over zero-shot | Training didn't help — investigate data or config |

## 6. Risks

| Risk | Likelihood | Mitigation |
|------|:----------:|------------|
| Overfitting 500 cases | Medium | Dev checkpoint selection, monitor loss |
| Output format overfitting | Medium | JSON baseline comparison, shuffled-labels sanity |
| Base model incompatibility | Low | Test smoke before training |
| Gold misuse during training | Low | Process enforcement, separate gold access |
| VRAM overflow with LoRA | Low | QLoRA 4-bit if needed |
| Training loop bugs | Medium | 5-case dry run before full training |

## 7. Shuffled Labels Sanity Check (Optional)

A shuffled-labels LoRA variant can test whether training improves due to:
- **Content learning** (model learns the routing task) — desired
- **Format learning** (model learns DSL format but not routing) — partial
- **Label memorization** (model memorizes specific case→target mappings) — undesired

If shuffled-labels LoRA performs similarly to real-labels LoRA, training is learning format, not routing. This is a diagnostic, not a required baseline.

**Priority: Low.** Defer to after primary LoRA experiment if time permits.

---

*End of V0.5 LoRA Experiment Plan.*
