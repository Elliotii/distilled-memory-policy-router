# gold_v2_002 Construction Report

**Date:** 2026-06-04  

## Summary

| Aspect | v001 | v002 |
|--------|:----:|:----:|
| Active | 150 | 150 ✅ |
| Holdout | 30 | 30 ✅ |
| Domains | 6 (leaked) | 8 (verified clean) |
| Unit uniqueness | 38.6% | **67.1%** ✅ |
| Memory uniqueness | 16.4% | 41.5% |
| Max unit skeleton | 14 | 7 |
| Max memory skeleton | 12 | 12 (stale memories) |
| READ positional | Yes | No (shuffled) |
| Method | `build_gold_v2.py` | `build_gold_v2_002.py` |

## Distribution

| Shape | Count | % |
|-------|:-----:|:--:|
| READ-only | 26 | 17% |
| STORE/SKIP-only | 60 | 40% |
| READ+STORE | 64 | 43% |

| Target | % |
|--------|:--:|
| task_state | 33.8% |
| service_memory | 29.7% |
| repo_memory | 17.1% |
| project_memory | 13.1% |
| user_profile | 6.3% |

| Stress | Count | Range |
|--------|:-----:|:-----:|
| Sensitive | 24 | 18-27 ✅ |
| Boundary | 34 | 30-38 ✅ |
