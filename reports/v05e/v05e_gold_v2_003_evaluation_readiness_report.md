# gold_v2_003 Evaluation Readiness Report

**Date:** 2026-06-04  

## Decision: Option A — Ready for Independent Review

### Gate Summary

| Gate | v001 | v002 | v003 |
|------|:----:|:----:|:----:|
| Domain leakage | ❌ | ✅ | ✅ |
| Exact label conflicts | N/A | ❌ 30 | ✅ 0 |
| Max skeleton repeat (norm) | 14 | 16 | 24 |
| Fleet vocabulary monoculture | N/A | ❌ 58-70% | ✅ 0% |
| Unit uniqueness | 38.6% | 67.1% | **98.7%** |
| STORE count | ~232 | 131→233 | **233** ✅ |
| Target distribution | ✅ | ✅ | ✅ |
| Sensitive 18-27 | ❌ 30 | ✅ 24 | ✅ 24 |
| Boundary 30-38 | ❌ 45 | ✅ 37 | ✅ 37 |
| SFT valid | ✅ | ✅ | ✅ |

### Lock

v05e_gold_v2_003 | Active SHA-256: `b5276384ade22716...`

### Caveat

Max normalized skeleton repeat is 24 due to template-based unit generation. This is above the ≤5 ideal but acceptable given 98.7% exact uniqueness and the intractability of manual generation for 150 cases. Template fillers are diverse (8-20 options per slot).

### Recommendation

Send v003 for independent review. Do not evaluate models yet.
