# V0.5c Final Report Consistency Check

**Date:** 2026-06-04  

---

## Cross-Report Audit

| Check | Result |
|-------|:------:|
| Gold hash consistent across all reports | ✅ `56e16078...` |
| Exact match: 41% on gold | ✅ Consistent |
| STORE F1: 0.969 on gold | ✅ Consistent |
| Target accuracy: 73.7% on gold | ✅ Consistent |
| Parse: 100% on gold | ✅ Consistent |
| Sensitive: 5 genuine failures | ✅ Consistent |
| Dev→Gold delta: +7pp exact | ✅ Consistent |
| 250 parse regression documented | ✅ All reports acknowledge |
| Qwen3-4B 500: 31% exact on gold | ✅ Consistent across v0.5b and v0.5c |
| Qwen3.5 few-shot: 42% exact on gold | ✅ Consistent |

## Forbidden Claims Check

| Claim | Appears? | Status |
|-------|:--------:|:------:|
| "LoRA beats few-shot overall" | No | ✅ Safe |
| "Production-safe" | No | ✅ Safe |
| "Safety solved" | No | ✅ Safe |
| "All LoRA settings exhausted" | No | ✅ Safe |
| "Qwen3.5 universally better than Qwen3-4B" | No | ✅ Safe (parse regression noted) |
| "Target routing solved" | No | ✅ Safe (73.7% = 26.3% error) |
| "Gold fully blind for future" | No | ✅ Safe (3 evals noted) |
| "500 cases sufficient" | No | ✅ Safe |

## Metric Mixing Check

| Check | Result |
|-------|:------:|
| Dev metrics labeled "dev" | ✅ |
| Gold metrics labeled "gold" | ✅ |
| No dev/gold comparisons as same-split | ✅ |
| Few-shot baselines labeled as gold | ✅ |
| LoRA comparisons correctly split-labeled | ✅ |

## File Count

| Category | Count |
|----------|:-----:|
| v05c reports | 42 |
| v05c docs | 4 |
| v05c configs | 3 |
| v05c prediction files | 4 |
| Scripts modified | 2 |

## Report List Complete?

| Phase | Reports |
|-------|:-------:|
| Planning | 5 ✅ |
| 125 Smoke | 5 ✅ |
| 250 | 6 ✅ |
| 500 Dev | 9 ✅ |
| Gold | 9 ✅ |
| Final consolidation | 8 ✅ |
| **Total** | **42** ✅ |

---

**Consistency check: PASSED. All metrics align, no forbidden claims, no dev/gold mixing.**
