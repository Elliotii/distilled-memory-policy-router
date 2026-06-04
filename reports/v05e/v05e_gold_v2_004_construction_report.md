# gold_v2_004 Construction Report

**Date:** 2026-06-04  

## Summary

| Metric | Value |
|--------|:-----:|
| Active | 150 |
| Holdout | 30 |
| STORE units | 231 |
| Method | `build_gold_v2_004.py` — disjoint pools, hard gates |

## Distribution (all within protocol)

| Target | % | Range |
|--------|:--:|:-----:|
| task_state | 34.2% | ≤36% ✅ |
| service_memory | 33.8% | 29-35% ✅ |
| repo_memory | 15.2% | 14-20% ✅ |
| project_memory | 9.1% | 9-15% ✅ |
| user_profile | 7.8% | 3-9% ✅ |

| Gate | Result |
|------|:------:|
| Exact label conflicts | 0 |
| Domain leakage | 0 |
| Filler bugs | 0 |
| Sensitive 18-27 | 25 ✅ |
| Boundary 30-38 | 30 ✅ |
| Boundary on READ-only | 0 ✅ |
| Unit uniqueness | 97.9% |
