# V0.5c Next Ablation Decision Memo

**Date:** 2026-06-04  
**Status:** Advisory only — no training authorized  

---

## Current State

Qwen3.5 JSON LoRA 500: 41% exact, 0.969 STORE F1, 73.7% target acc on gold. Best trained system, #2 overall.

Remaining gap to Qwen3.5 JSON few-shot (#1): −1pp exact, −5.4pp target acc, +5 sensitive failures (vs 0).

---

## Candidate Next Ablations

### Priority 1: Standard LoRA / BF16 LoRA

| Aspect | Current (QLoRA) | Proposed |
|--------|:---------------:|----------|
| Precision | 4-bit nf4 | BF16 |
| Expected impact | — | +2-5pp exact |
| Risk | Higher VRAM | 12GB RTX 4070 may not fit BF16 4B model |
| Feasibility | — | May need gradient checkpointing or smaller batch |

**Rationale:** QLoRA r=8 is 1pp from few-shot. Standard LoRA could close this gap. But VRAM is the blocker — 4B model in BF16 ≈ 8GB + optimizer + activations could exceed 12GB.

### Priority 2: r=16 QLoRA

| Aspect | Current | Proposed |
|--------|:-------:|----------|
| LoRA rank | 8 | 16 |
| Trainable params | 4.9M → 9.8M |
| Expected impact | +1-3pp exact |
| Risk | Minimal (still QLoRA, VRAM-safe) |

**Rationale:** Doubling LoRA capacity is the safest "more capacity" experiment. Fits within VRAM budget.

### Priority 3: Safety-Focused Training

| Aspect | Detail |
|--------|--------|
| Problem | 5 PII stores on gold (phones, addresses, emails) |
| Approach | Oversample sensitive cases, add SKIP loss penalty |
| Expected impact | 5 → 0-2 sensitive failures |
| Risk | May reduce STORE F1 if too aggressive |

**Rationale:** The most impactful remaining bottleneck for real-world claims.

### Priority 4: Target-Balanced Training

| Aspect | Detail |
|--------|--------|
| Problem | repo_memory and project_memory likely weakest targets |
| Approach | Oversample underrepresented targets |
| Expected impact | +3-5pp target accuracy |
| Risk | May reduce overall STORE F1 |

### Priority 5: gold_v2 Creation

| Aspect | Detail |
|--------|--------|
| Problem | Gold evaluated 3 times — not fully blind for future tuned variants |
| Approach | Create new 100-case gold set using same methodology |
| Timing | Before any hyperparameter tuning experiments |

---

## Recommended Sequence

1. **gold_v2** — new gold for clean evaluation of future variants
2. **r=16 QLoRA** — safest capacity increase (VRAM-safe)
3. **Safety-focused training** — address the PII bottleneck
4. **Standard LoRA** — only if VRAM allows or AutoDL available
5. **Target-balanced training** — refine target classification

## Decision Criteria

| Experiment | Run if | Skip if |
|-----------|--------|---------|
| gold_v2 | Before any new hyperparameter tuning | If sticking with current gold |
| r=16 QLoRA | Want safer capacity increase than standard LoRA | If exact is not the priority |
| Safety training | PII is the top concern | If pursuing exact/target first |
| Standard LoRA | VRAM confirmed feasible (BF16 4B < 12GB) | If VRAM is the bottleneck |
| Target-balanced | Target accuracy is the top concern | If safety or exact take priority |

---

**Do not start any of these without explicit user authorization.**
