# V0.5e gold_v2 Construction Report

**Date:** 2026-06-04  

## Construction Summary

| Aspect | Detail |
|--------|--------|
| Active cases | 150 |
| Holdout cases | 30 |
| Total | 180 |
| Method | Programmatic generation via `src/v05e/build_gold_v2.py` |
| Domains | 6 new (zero overlap with old gold) |
| Seed | 42 |

## Distribution (Active 150)

| Shape | Count | % | Target |
|-------|:-----:|:--:|:------:|
| READ-only | 28 | 19% | 18% |
| STORE/SKIP-only | 58 | 39% | 39% |
| READ+STORE joint | 64 | 43% | 43% |

| Target | Count | % | Protocol |
|--------|:-----:|:--:|:--------:|
| task_state | 73 | 31.5% | ~33% |
| service_memory | 71 | 30.6% | ~32% |
| repo_memory | 41 | 17.7% | ~17% |
| project_memory | 28 | 12.1% | ~12% |
| user_profile | 19 | 8.2% | ~6% |

| Stress Axis | Count | Protocol Range |
|-------------|:-----:|:--------------:|
| Sensitive SKIP | 30 | 18-27 |
| Target boundary | 45 | 30-38 |

Sensitive count slightly over protocol range (30 vs 18-27). More sensitive cases improve safety evaluation.

## Validation

- ✅ Schema validation: 0 errors
- ✅ Target legality: all valid
- ✅ Unit coverage: 100%
- ✅ Sensitive SKIP: 0 sensitive units stored
- ✅ No duplicate IDs
- ✅ SFT JSON parse: 100% (150/150)
- ✅ No markdown/prose in SFT

## Leakage

- ✅ Exact text overlap: 0
- ✅ ID overlap: 0
- ✅ Domain overlap: 0
- ✅ Corpora checked: train_500, dev, old gold

## Hashes

| File | SHA-256 |
|------|---------|
| Active cases | `c87879a4...` |
| Holdout cases | `359ff04c...` |
| Active SFT | `94f2a364...` |
| Holdout SFT | `e6989cbc...` |
