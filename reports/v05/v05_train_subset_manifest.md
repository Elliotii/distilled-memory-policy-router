# V0.5 Training Subset Manifest

**Date:** 2026-06-02  
**Context:** 5.5-A2 — training subset documentation  

---

## Subset Sizes

| Subset | Cases | Nesting |
|--------|:-----:|:-------:|
| 125 | 125 | ⊂ 250 |
| 250 | 250 | ⊂ 500 |
| 500 | 500 | Full train pool |

## Files

| Subset | Case IDs | Cases JSONL | SFT Messages |
|--------|----------|-------------|-------------|
| 125 | `v05_train_125_case_ids.txt` | `v05_train_125_cases.jsonl` | `v05_train_125_sft_messages.jsonl` |
| 250 | `v05_train_250_case_ids.txt` | `v05_train_250_cases.jsonl` | `v05_train_250_sft_messages.jsonl` |
| 500 | `v05_train_500_case_ids.txt` | `v05_train_500_cases.jsonl` | `v05_train_500_sft_messages.jsonl` |

All under `data/v05/train/subsets/`.

## Construction

- **Source:** `data/v05/batches/v05_batch500_corrected_cases.jsonl` (500 cases)
- **Random seed:** 42
- **Method:** Stratified random sampling by shape (READ-only, STORE/SKIP-only, READ+STORE joint)
- **125:** Random sample of 125 from 250 subset
- **250:** Stratified proportional sample from 500 (50% per shape category)
- **500:** Full train pool

## Nesting Proof

```
125 IDs ⊂ 250 IDs: True
250 IDs ⊂ 500 IDs: True
```

## Distribution Summary

500-case pool:
- Shapes: READ-only 105 (21%), STORE/SKIP-only 182 (36.4%), READ+STORE joint 213 (42.6%)
- Targets: task_state 338, service_memory 323, repo_memory 201, project_memory 122, user_profile 58

Subsets maintain approximate proportional representation through stratified sampling.

## Intended Use

- **125:** Smoke training — verify pipeline, check parse success, measure first improvement
- **250:** Intermediate training — learning curve data point
- **500:** Full training — best expected performance

## Split Integrity

- Train ∩ Dev = 0 ✅
- Train ∩ Gold = 0 ✅
- All SFT assistant == gold.dsl ✅

---

*End of V0.5 Training Subset Manifest.*
