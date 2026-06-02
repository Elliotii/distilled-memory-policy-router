# V0.5 Leakage Checker Report

**Train file:** `data/v05/batches/v05_batch500_corrected_cases.jsonl`  
**Candidate file:** `data/v05/dev/v05_dev_cases.jsonl`  
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

### near_duplicate_memory (1 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_batch500_0133` | `v05_dev_0006` | 0.500 | The token-issuer generates access tokens with 15-minute expiry and refresh token |
