# V0.5 Model Comparison Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — model baseline readiness and comparison planning
Context: 5.4-A

---

## 1. Stage Transition

The data construction stage is complete:

| Data Set | Status | Cases | Role |
|----------|:------:|:-----:|------|
| Train-pool (corrected batch500) | ✅ Complete | 500 | LoRA/SFT training candidate |
| Dev | ✅ Accepted | 100 | Model selection / checkpoint / prompt-setting |
| Locked Gold (v05_gold_001) | ✅ Locked | 100 | Final evaluation only |

The model experiment stage begins. All subsequent contexts must respect locked gold immutability.

## 2. Splits and Their Roles

### 2.1 Train-Pool (500 cases)

| Item | Value |
|------|-------|
| File | `data/v05/batches/v05_batch500_corrected_cases.jsonl` |
| Cases | 500 |
| Role | LoRA/SFT training |
| Few-shot source | Yes (3 examples drawn from train only) |
| Subsets for learning curve | 125 ⊂ 250 ⊂ 500 |
| Must not overlap | Dev, gold |

### 2.2 Dev (100 cases)

| Item | Value |
|------|-------|
| File | `data/v05/dev/v05_dev_cases.jsonl` |
| Cases | 100 |
| Role | Model selection, checkpoint choice, prompt comparison |
| Used for | Choosing best model/interface/config |
| Not for | Final claims — all final metrics from gold |

### 2.3 Locked Gold (100 cases)

| Item | Value |
|------|-------|
| Lock file | `data/v05/gold/v05_gold_lock.json` |
| Lock version | v05_gold_001 |
| Cases | 70 gold_core + 30 gold_hard |
| SHA-256 combined | `56e16078...2173d` |
| Role | Final evaluation only |
| Immutable | Yes — any change requires new lock version |

## 3. Model Candidates

### 3.1 Primary: Qwen3-4B-Instruct-2507

| Property | Value |
|----------|-------|
| Local path | `/home/abc16/hf_models/Qwen3-4B-Instruct-2507` |
| Size on disk | 7.6 GB |
| Architecture | Qwen3-4B, instruction-tuned |
| Thinking mode | `enable_thinking=False` for zero-shot/few-shot |
| VRAM required | ~8 GB (fits RTX 4070 SUPER 11GB) |
| Status | ✅ Present and ready |

### 3.2 Challenger: Qwen3.5 same-tier 4B

| Property | Value |
|----------|-------|
| Candidate ID | `Qwen/Qwen3.5-4B` |
| Local path | `/home/abc16/hf_models/Qwen3.5-4B` (not present) |
| Status | ❌ Not downloaded |
| Plan | See V05_QWEN35_ACQUISITION_PLAN.md |

## 4. Baseline Systems

### 4.1 Non-Model Baselines

| # | System | Type | Config |
|---|--------|------|--------|
| 1 | `empty` | No-action | READ NONE, STORE NONE, SKIP all |
| 2 | `topk_read` | Retrieval | READ first K candidate memories |
| 3 | `heuristic` | Lexical | Rule-based READ/STORE/SKIP |
| 4 | `per_target_majority` | Guessing | Always predict most frequent target |

### 4.2 Teacher Reference

| # | System | Type | Config |
|---|--------|------|--------|
| 5 | `deepseek_teacher` | Reference | DeepSeek V4 Flash Unit DSL (API) |

### 4.3 Qwen3-4B Model Baselines

| # | System | Interface | Config |
|---|--------|-----------|--------|
| 6 | `qwen3_zero_shot_dsl` | Unit DSL | zero-shot, temperature=0 |
| 7 | `qwen3_few_shot_dsl` | Unit DSL | 3 examples from train, temperature=0 |
| 8 | `qwen3_zero_shot_json` | Unit JSON | zero-shot, temperature=0 |
| 9 | `qwen3_few_shot_json` | Unit JSON | 3 examples from train (optional) |

### 4.4 Qwen3.5 Model Baselines (if acquired)

| # | System | Interface | Config |
|---|--------|-----------|--------|
| 10 | `qwen35_zero_shot_dsl` | Unit DSL | zero-shot, temperature=0 |
| 11 | `qwen35_few_shot_dsl` | Unit DSL | 3 examples from train, temperature=0 |
| 12 | `qwen35_zero_shot_json` | Unit JSON | zero-shot, temperature=0 (optional) |

### 4.5 LoRA/SFT Trained Router

| # | System | Base Model | Data |
|---|--------|-----------|------|
| 13 | `qwen_lora_125` | Qwen3-4B | 125 train cases |
| 14 | `qwen_lora_250` | Qwen3-4B | 250 train cases |
| 15 | `qwen_lora_500` | Qwen3-4B | 500 train cases |

**Note:** LoRA experiments target Qwen3-4B by default. If Qwen3.5 shows significant improvement on dev baselines, the LoRA base model may be switched per V05_LORA_EXPERIMENT_PLAN.md.

## 5. Evaluation Order

### Phase 1: Smoke Test (5 dev cases, 3 interfaces)

```
Goal: Verify runner compatibility, parse success, latency, VRAM.
Systems: Qwen3-4B zero-shot DSL, few-shot DSL, zero-shot JSON.
Split: dev only (5 cases).
Do NOT use gold.
```

### Phase 2: Full Dev Baseline (100 dev cases)

```
Goal: Select best model + interface combination.
Systems: All non-model baselines + Qwen3-4B DSL/JSON + Qwen3.5 DSL (if available).
Split: dev only.
Metrics: parse_success, store_unit_f1, store_target_accuracy, skip_f1, sensitive_store.
Selection criterion: Best store_unit_f1 + store_target_accuracy on dev.
```

### Phase 3: Selected Baselines on Locked Gold

```
Goal: Establish pre-training baseline on final holdout.
Systems: Empty, topk, heuristic, best Qwen3 zero-shot, best Qwen3 few-shot,
         DeepSeek teacher, best Qwen3.5 (if available).
Split: locked gold only.
Report: All metrics for baseline comparison table.
```

### Phase 4: LoRA Learning Curve

```
Goal: Measure training effect at different data scales.
Training: 125 ⊂ 250 ⊂ 500 from train-pool.
Checkpoint selection: dev (highest store_unit_f1).
Evaluation: Selected checkpoint on locked gold.
```

### Phase 5: Final Locked-Gold Evaluation

```
Goal: Full comparison table for final report.
Systems: All baselines + best LoRA checkpoint.
Split: locked gold (core + hard separately).
Report: Aggregate, per-target, per-tag, confusion matrices, error analysis.
```

## 6. Gold Protection

### Absolute Rules

| Rule | Enforcement |
|------|------------|
| No tuning on gold | Process enforced — gold only in Phase 3 and Phase 5 |
| No few-shot examples from gold | Few-shot from train-pool only |
| No error-driven data changes based on gold | Gold errors documented but NOT fixed (unless critical) |
| No gold inspection during training | Training pipeline must not access gold files |
| No gold in system prompt | System prompt is fixed, no gold-derived content |
| No checkpoint selection on gold | Use dev for all checkpoint choices |

### Violation Consequences

Any use of gold before Phase 3 invalidates the final evaluation. Gold is a clean holdout — once opened for training decisions, it is no longer a valid holdout.

---

*End of V0.5 Model Comparison Plan.*
