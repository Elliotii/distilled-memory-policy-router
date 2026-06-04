# gold_v2_003 Construction Report

**Date:** 2026-06-04  

## Summary

| Metric | Value |
|--------|:-----:|
| Active | 150 |
| Holdout | 30 |
| Method | `build_gold_v2_003.py` — template-based with domain vocab, unique seeds per unit |

## Distribution

| Shape | Count | % |
|-------|:-----:|:--:|
| READ-only | 27 | 18% |
| STORE/SKIP-only | 56 | 37% |
| READ+STORE | 67 | 45% |

| Target | % of 233 STORE units |
|--------|:--------------------:|
| task_state | 36.5% |
| service_memory | 30.0% |
| repo_memory | 18.5% |
| project_memory | 8.2% |
| user_profile | 6.9% |

| Stress | Count | Range |
|--------|:-----:|:-----:|
| Sensitive | 24 | 18-27 ✅ |
| Boundary | 37 | 30-38 ✅ |

## Validation

- ✅ 0 schema errors
- ✅ 0 exact label conflicts
- ✅ 0 sensitive STORE
- ✅ SFT 100% JSON valid
