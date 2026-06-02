# V0.5 Leakage Checker Report

**Train file:** `data/v05/batches/v05_batch500_corrected_cases.jsonl`  
**Candidate file:** `data/v05/gold/v05_gold_draft_cases.jsonl`  
**Train cases:** 500  
**Candidate cases:** 100  

## Summary

| Category | Count |
|----------|:----:|
| Hard blockers | 0 |
| Review-level warnings | 0 |
| General warnings | 1 |

## ✅ No Hard Blockers

## Warnings (1)

### near_duplicate_unit (1 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_sample_0007` | `v05_gold_hard_0015` | 0.533 | My recovery phone number for PagerDuty account recovery is +1-555-0198. |
