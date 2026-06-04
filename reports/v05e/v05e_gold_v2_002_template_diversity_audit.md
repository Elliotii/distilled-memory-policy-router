# gold_v2_002 Template Diversity Audit

**Date:** 2026-06-04  

## Unit Diversity

| Metric | v001 | v002 |
|--------|:----:|:----:|
| Total unit instances | ~346 | 343 |
| Unique unit texts | 134 (38.6%) | **230 (67.1%)** |
| Max raw skeleton repeats | 14 | 7 |
| Max normalized skeleton repeats | — | 7 |

## Memory Diversity

| Metric | v001 | v002 |
|--------|:----:|:----:|
| Total memory instances | ~452 | 501 |
| Unique memory texts | 74 (16.4%) | **208 (41.5%)** |
| Stale memory pool size | 4 | 20 |
| Max stale repeat | ~30x | ~12x |

## Template Analysis

v002 eliminated fill-in-the-blank templates. Unit texts are hand-crafted per domain with varied:
- Sentence openings (questions, statements, imperatives)
- Technical detail (specific error codes, version numbers, metric names)
- Domain-specific jargon (geocoding, adjudication, consumer groups, enrollment, etc.)

No mass SLA/root-cause/connection-pool templates detected.

## Normalized Skeleton Repeat

Post-normalization (domain names → SVC), max unit skeleton repeat is 7. The most-common skeletons are structurally similar but semantically distinct (different services, different situations). This is within acceptable range for a 150-case dataset.

## Verdict: PASS ✅
