# V0.5b Ablation Plan

**Date:** 2026-06-02  
**Status:** Planning only — do NOT run  

---

## Candidate Ablations

### 1. Unit JSON LoRA

**Hypothesis:** JSON few-shot was the strongest prompting baseline (42% gold). Training in JSON format may transfer better.

**Risk:** JSON output longer (~120 chars vs ~60 DSL), less training-efficiency. May introduce JSON parsing errors.

**Success:** Beat Qwen3.5 JSON few-shot on gold (42% exact, 0.963 STORE F1).

### 2. Target-Balanced Training

**Hypothesis:** Oversample service_memory, project_memory, repo_memory to match task_state frequency. Current imbalance (task_state 32%, service_memory 31%, repo_memory 19%, project_memory 12%, user_profile 6%) causes task_state over-prediction.

**Risk:** May hurt STORE/SKIP if original distribution is important. May require more total data.

**Success:** Per-target accuracy ≥ 60% for all targets on dev.

### 3. Safety-Focused Training

**Hypothesis:** Oversample sensitive SKIP cases, add loss penalty for storing sensitive units. Currently ~10 sensitive cases in 500.

**Risk:** May over-correct and skip legitimate user_profile content. Needs careful threshold.

**Success:** 0 sensitive store on gold. Or at most 1-2 false positives.

### 4. LoRA Capacity

**Hypothesis:** r=8 may be too small for 5-class target classification. r=16 or r=32 may improve target accuracy.

**Risk:** More VRAM. May overfit on 500 cases.

**Success:** Target accuracy > 60% on dev.

### 5. Training Duration

**Hypothesis:** 3 epochs insufficient. 5 or 10 epochs may improve convergence.

**Risk:** Overfitting. Dev eval loss already stabilizing at epoch 3.

**Success:** Target accuracy improvement without STORE F1 regression.

### 6. Two-Stage Router

**Hypothesis:** Separate action classifier (STORE/SKIP) from target classifier. Train two LoRA adapters.

**Risk:** Complexity. May not work with current architecture.

**Success:** Both stages perform well on dev.

## Gold Usage Rules for v0.5b

- Dev for all development and ablation selection.
- Locked gold only for final evaluation of pre-declared variants.
- Maximum 2-3 gold evaluations for v0.5b.
- Do NOT iterate on gold.

---

*End of V0.5b Ablation Plan.*
