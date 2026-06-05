# v05g Combined 1000 Distribution Report

**Date:** 2026-06-05  
**Composition:** 500-control + 500 additional targeted-balanced (REPAIRED)  
**Status:** All distributions within target ranges

## Summary

| Metric | 500-control | Additional 500 | Combined 1000 |
|--------|-------------|----------------|---------------|
| Cases | 500 | 500 | 1,000 |
| STORE units | 1,042 | 1,037 | 2,079 |

## Shape Distribution

| Shape | 500-control | Additional 500 | Combined 1000 | Target |
|-------|-------------|----------------|---------------|--------|
| READ-only | 21.0% | 18.0% | 19.5% | 10-20% ✅ |
| STORE/SKIP-only | 36.4% | 38.0% | 37.2% | 35-45% ✅ |
| READ+STORE | 42.6% | 44.0% | 43.3% | 40-50% ✅ |

## Target Distribution (STORE units)

| Target | 500-control | Additional 500 | Combined 1000 | Target | Status |
|--------|-------------|----------------|---------------|--------|--------|
| task_state | 32.4% | 23.9% | 28.2% | 25-32% | ✅ |
| service_memory | 31.0% | 22.1% | 26.6% | 24-32% | ✅ |
| repo_memory | 19.3% | 20.2% | 19.7% | 16-22% | ✅ |
| project_memory | 11.7% | 18.0% | 14.9% | 12-20% | ✅ |
| user_profile | 5.6% | 15.8% | 10.7% | 6-12% | ✅ |

## Stress Coverage

| Category | 500-control | Additional 500 | Combined 1000 |
|----------|-------------|----------------|---------------|
| Sensitive/private | 30 | 90 | 120 |
| Target-boundary | 100 | 150 | 250 |
| Hard SKIP | ~30 | 180 | ~210 |
| READ distractor/stale | ~60 | 233 | ~293 |

## Semantic Quality (Post-Repair)

| Metric | Value |
|--------|-------|
| Stale reads | 0 |
| Distractor reads | 0 |
| READ decisions recovered from visible semantics | 100% |
| User_profile reads (when relevant) | 100% |
| Sensitive literal unique texts | 70 |
| Sensitive literal max repetition | 2x |

## Prefix/Opener Quality (Post-Repair)

| Metric | Value |
|--------|-------|
| 3-word-prefix binary accuracy | 90.9% |
| Ambiguous prefixes (multi-label) | 26 |
| Body-dependent cases | 321 (64.2%) |

## Domain Diversity

| Set | Unique projects | Unique services | Unique repos |
|-----|-----------------|-----------------|--------------|
| 500-control | 17 | 198 | 19 |
| Additional 500 | 8 | 8 | 8 |
| Combined 1000 | 25 | 206 | 27 |

## Key Observations

1. All 5 target distributions fall within recommended ranges.
2. All 3 shape distributions fall within recommended ranges.
3. READ labels are semantically recoverable from visible context.
4. Opener-template separability is substantially reduced from 100% to 90.9%.
5. Sensitive literals diversified from 18 to 70 unique texts.
6. The additional 500 balances the 500-control skew toward task_state and service_memory.

## Comparison with Desired Distribution

| Metric | Desired | Achieved |
|--------|---------|----------|
| task_state | 25-32% | 28.2% ✅ |
| service_memory | 24-32% | 26.6% ✅ |
| repo_memory | 16-22% | 19.7% ✅ |
| project_memory | 12-20% | 14.9% ✅ |
| user_profile | 6-12% | 10.7% ✅ |
| READ-only | 10-20% | 19.5% ✅ |
| STORE/SKIP-only | 35-45% | 37.2% ✅ |
| READ+STORE | 40-50% | 43.3% ✅ |
