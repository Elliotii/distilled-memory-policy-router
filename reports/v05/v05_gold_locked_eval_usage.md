# V0.5 Gold Locked Eval Usage Guide

**Date:** 2026-06-02  
**Context:** 5.3-E — evaluation usage rules for locked gold  
**Status:** Gold locked — this document governs all evaluation usage  

---

## 1. Gold Role

Gold is the **sole final evaluation standard** for v0.5 memory policy router claims.

- 100 cases (70 gold_core + 30 gold_hard)
- Independently constructed from train-pool and dev
- Human-adjudicated with Opus advisory review
- Lock file: `data/v05/gold/v05_gold_lock.json`

**Rules:**
- Gold is opened ONLY for final evaluation
- Gold must NOT be inspected during training or development
- Any metric reported as a project claim must come from gold, not dev

## 2. Dev Role

Dev is the **development diagnostics** set:

- 100 independently constructed cases
- Used for checkpoint selection, hyperparameter comparison, prompt-setting choice
- NOT used for final claims

**Rules:**
- Use dev for all development decisions
- Dev metrics are diagnostics only
- Do NOT report dev metrics as final results

## 3. Train Role

Training pool is the corrected batch500 (500 cases):

- Used for LoRA/SFT training
- Source: `data/v05/batches/v05_batch500_corrected_cases.jsonl`
- Not split from dev or gold
- Few-shot examples must be sourced from train only

## 4. Allowed Systems to Evaluate on Locked Gold

### Baseline Systems

| # | System | Description |
|---|--------|-------------|
| 1 | `empty` | READ none, STORE none, SKIP all |
| 2 | `topk_read` | READ first K memories, STORE none, SKIP all |
| 3 | `heuristic` | Deterministic lexical rules |
| 4 | `per_target_majority` | Always predict majority target |

### Teacher Reference

| # | System | Description |
|---|--------|-------------|
| 5 | `deepseek_teacher` | DeepSeek V4 Flash-compatible with same prompt |

### Qwen3-4B Baselines

| # | System | Description |
|---|--------|-------------|
| 6 | `qwen3_4b_zero_shot_dsl` | Qwen3-4B zero-shot Unit DSL |
| 7 | `qwen3_4b_few_shot_dsl` | Qwen3-4B few-shot Unit DSL (3 examples from train) |
| 8 | `qwen3_4b_zero_shot_json` | Qwen3-4B zero-shot Unit JSON |

### Qwen3.5 Same-Tier Baselines

| # | System | Description |
|---|--------|-------------|
| 9 | `qwen3_5_zero_shot_dsl` | Qwen3.5 zero-shot Unit DSL (same-tier comparison) |
| 10 | `qwen3_5_few_shot_dsl` | Qwen3.5 few-shot Unit DSL |

### LoRA/SFT Trained Routers

| # | System | Description |
|---|--------|-------------|
| 11 | `qwen_lora_125` | Qwen3-4B LoRA trained on 125 cases |
| 12 | `qwen_lora_250` | Qwen3-4B LoRA trained on 250 cases |
| 13 | `qwen_lora_500` | Qwen3-4B LoRA trained on 500 cases |

## 5. Forbidden Uses of Locked Gold

| Prohibited Use | Reason |
|----------------|--------|
| Prompt tuning | Prompt must not be optimized against gold |
| LoRA checkpoint selection | Use dev for checkpoint selection |
| Hyperparameter selection | Use dev for hyperparameter tuning |
| Data generation feedback | Indirect leakage |
| Few-shot examples | Must be train-sourced only |
| System prompt design | Prompt must not memorize gold patterns |
| Model comparison during development | Only dev during development phase |

## 6. Recommended Experimental Order

### Phase 1: Baseline Comparison on Dev

```
Run Qwen3-4B and Qwen3.5 zero-shot/few-shot DSL on dev.
Select best-performing prompt and interface configuration.
Do NOT evaluate on gold during this phase.
```

### Phase 2: Final Baseline Evaluation on Locked Gold

```
Run all baseline systems (1-8 and optionally 9-10) on locked gold.
Record metrics for final report.
DeepSeek teacher is evaluated once on gold.
```

### Phase 3: LoRA Learning Curve

```
Train Qwen3-4B LoRA routers on nested subsets:
  - 125 cases (from train-pool)
  - 250 cases (from train-pool)
  - 500 cases (from train-pool)
Select best checkpoint per training run using dev.
```

### Phase 4: Final Trained Router Evaluation

```
Evaluate best LoRA checkpoint on locked gold.
Compare against all baselines from Phase 2.
Report all metrics on gold only.
```

## 7. Prediction File Convention

```
predictions/v05/<system>_gold_predictions.jsonl
```

Example:
```
predictions/v05/qwen3_4b_zero_shot_dsl_gold_predictions.jsonl
predictions/v05/deepseek_teacher_gold_predictions.jsonl
predictions/v05/qwen_lora_500_gold_predictions.jsonl
```

## 8. Reporting Requirements

Final evaluation report must:
- Use locked gold for all metrics
- Report per-target breakdowns
- Report gold_core vs gold_hard separately
- Include target confusion matrices
- Report sensitive store rate (must be 0)
- Use honest language (see V05_EVAL_PROTOCOL.md Section 6.3)
- Reference the gold lock SHA-256 hashes

---

*End of V0.5 Gold Locked Eval Usage Guide.*
