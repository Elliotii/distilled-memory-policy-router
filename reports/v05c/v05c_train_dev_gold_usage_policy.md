# V0.5c Train / Dev / Gold Usage Policy

**Date:** 2026-06-02  
**Context:** 5.9-A — Feasibility and planning  

---

## 1. Policy Statement

The v0.5c experiment (Qwen3.5 Unit JSON LoRA) reuses the existing train, dev, and gold data from v0.5/v0.5b without modification, relabeling, or regeneration.

## 2. Train Data

| File | Rows | Source | Status |
|------|:----:|--------|:------:|
| `data/v05b/json_sft/v05b_train_125_json_sft_messages.jsonl` | 125 | v0.5b JSON SFT rendering | **Reuse as-is** |
| `data/v05b/json_sft/v05b_train_250_json_sft_messages.jsonl` | 250 | v0.5b JSON SFT rendering | **Reuse as-is** |
| `data/v05b/json_sft/v05b_train_500_json_sft_messages.jsonl` | 500 | v0.5b JSON SFT rendering | **Reuse as-is** |

- **Nesting:** 125 ⊂ 250 ⊂ 500 (same case IDs as v0.5/v0.5b).
- **Format:** Chat messages with Unit JSON assistant output.
- **No relabeling:** Labels match v0.5 gold annotations.
- **No regeneration:** These files are frozen from v0.5b.

## 3. Dev Data

| File | Rows | Source | Status |
|------|:----:|--------|:------:|
| `data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl` | 100 | v0.5b JSON SFT rendering | **Reuse as-is** |

- **Purpose:** Development evaluation during 125/250/500 training phases.
- **Leakage:** Dev is disjoint from train-pool (verified in v0.5 P5.11-A).
- **No gold use:** Dev is used for ALL development decisions — model selection, smoke gating, and error analysis.

## 4. Gold Data

| File | Rows | Lock Status | SHA-256 |
|------|:----:|:-----------:|---------|
| `data/v05/gold/v05_gold_corrected_cases.jsonl` | 100 | **LOCKED** (v05_gold_001) | `56e16078...` |

- **Usage:** Final evaluation only — after 500-case training completes.
- **No development use:** Gold is not used for model selection, hyperparameter tuning, or smoke gating.
- **Lock status:** Gold has been locked since P5.12-E. No modifications.
- **Prior evaluations:** Gold was evaluated twice (v0.5 DSL LoRA 500, v0.5b JSON LoRA 500). It is not fully blind for v0.5c.
- **Mitigation:** Prior evaluations used different base models (Qwen3-4B) and interfaces (DSL/JSON). No hyperparameters were tuned on gold. Risk of gold overfitting is low.

## 5. Gold Blindness Assessment

| Experiment | Base Model | Interface | Gold Used |
|------------|------------|-----------|:---------:|
| v0.5 (P5.16-A) | Qwen3-4B | Unit DSL | ✅ (once) |
| v0.5b (P5.20-A) | Qwen3-4B | Unit JSON | ✅ (once) |
| **v0.5c (planned)** | **Qwen3.5** | **Unit JSON** | **Pending** |

Since gold has been evaluated twice, a third evaluation in v0.5c carries a modest risk of inflated metrics from implicit tuning. However:
- **No explicit tuning on gold:** All hyperparameter decisions (r, alpha, LR, epochs) were fixed before any gold evaluation.
- **Dev is the primary evaluation surface:** The learning curve (125→250→500) is measured on dev only.
- **Gold is a single final snapshot:** One evaluation at the end of 500 training.

### Recommended future action:
- After v0.5c, consider creating `gold_v2` for any further experiments (safety, target-balanced).
- gold_v2 would be constructed from the same methodology but with different cases.

## 6. Data Modification Prohibitions

| Action | Allowed? |
|--------|:--------:|
| Modify train JSON SFT files | ❌ No |
| Modify dev JSON SFT files | ❌ No |
| Modify gold cases | ❌ No |
| Relabel any cases | ❌ No |
| Regenerate SFT messages | ❌ No |
| Add new training data | ❌ No |
| Add new dev cases | ❌ No |
| Create new gold cases | ❌ No |
| Read gold case content | ❌ No (except hash/lock metadata) |
| Use gold for development | ❌ No |
| Use gold loss for early stopping | ❌ No |

## 7. Leakage Status

| Check | Status |
|-------|:------:|
| Train↔Dev hard blockers | 0 (verified in v0.5 P5.11-A) |
| Train↔Gold hard blockers | 0 (verified in v0.5 P5.12-E) |
| Dev↔Gold hard blockers | 0 (verified in v0.5 P5.12-E) |
| Cross-batch duplicates in train-pool | 1 known (not in subsets) |

---

*End of V0.5c Train / Dev / Gold Usage Policy.*
