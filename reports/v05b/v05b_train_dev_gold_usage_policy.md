# V0.5b Train / Dev / Gold Usage Policy

**Date:** 2026-06-02  
**Status:** Policy — enforced for all v0.5b contexts  

---

## Data Provenance

| Split | Source | Cases | Locked? | Usage |
|-------|--------|:-----:|:-------:|-------|
| Train 125 | v0.5 train pool subset | 125 | No | LoRA training |
| Train 250 | v0.5 train pool subset | 250 | No | LoRA training |
| Train 500 | v0.5 train pool | 500 | No | LoRA training |
| Dev | v0.5 dev set | 100 | No | Model selection, eval during training |
| Locked Gold | v0.5 gold | 100 | **YES** | Final evaluation only |

## Case ID Integrity

- Train subset IDs are identical to v0.5: 125 ⊂ 250 ⊂ 500.
- Dev case IDs are identical to v0.5 dev.
- Gold case IDs are identical to v0.5 gold.
- **No case labels, targets, or content have been modified.**

## Input Cases (Read-Only)

The following files are the sole source of truth for labels:

| File | Never modified |
|------|:---:|
| `data/v05/train/subsets/v05_train_125_cases.jsonl` | ✅ |
| `data/v05/train/subsets/v05_train_250_cases.jsonl` | ✅ |
| `data/v05/train/subsets/v05_train_500_cases.jsonl` | ✅ |
| `data/v05/dev/v05_dev_cases.jsonl` | ✅ |
| `data/v05/gold/v05_gold_corrected_cases.jsonl` | ✅ (locked) |

## JSON SFT Messages (Generated)

These are rendered from input cases and must be regenerated if input cases change:

| File | Source |
|------|--------|
| `data/v05b/json_sft/v05b_train_125_json_sft_messages.jsonl` | train 125 cases |
| `data/v05b/json_sft/v05b_train_250_json_sft_messages.jsonl` | train 250 cases |
| `data/v05b/json_sft/v05b_train_500_json_sft_messages.jsonl` | train 500 cases |
| `data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl` | dev cases |

## Gold Protection Rules

1. Locked gold is **immutable** — hash `56e16078...` must never change.
2. Gold is **not used** for training, prompt tuning, model selection, or checkpoint selection.
3. Gold is **only used** for final evaluation of pre-declared variants.
4. Maximum 2-3 gold evaluations for entire v0.5b.
5. Dev set is used for all development decisions.

## Forbidden Actions

1. ❌ Do not add new training data.
2. ❌ Do not relabel any case.
3. ❌ Do not modify locked gold.
4. ❌ Do not use gold during training.
5. ❌ Do not modify v0.5 train/dev/gold cases.
6. ❌ Do not run Qwen3.5 LoRA in this ablation.

---

*End of V0.5b Train / Dev / Gold Usage Policy.*
