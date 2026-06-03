# V0.5c Final Error Analysis

**Date:** 2026-06-04  

---

## 1. Structural Errors (Gold)

| Error Type | Count |
|-----------|:-----:|
| Invalid JSON | 0 |
| target="skip" | 0 |
| Truncation | 0 |
| Missing key | 0 |
| Missing unit | 0 |
| Invalid target | 0 |
| **Total** | **0** |

Qwen3.5 JSON LoRA 500 achieved **100% parse** on locked gold — zero structural errors. The transient `"target":"skip"` regression at 250 (7 cases on dev) was fully resolved by 500.

## 2. Parse Regression Timeline

| Stage | Parse | target=skip | Context |
|-------|:-----:|:-----------:|---------|
| Qwen3.5 125 dev | 98% | 0 | P5.22-B |
| Qwen3.5 250 dev | 90% | 7 | P5.22-C (regression) |
| Qwen3.5 500 dev | 98% | 0 | P5.22-D (recovered) |
| Qwen3.5 500 gold | **100%** | 0 | P5.22-E (perfect) |

The 250 parse dip was transient and fully resolved. No structural issues remain.

## 3. Target Errors (Gold)

Target accuracy: 73.7% → 26.3% error rate on 210 STORE units.

| Known confusion | Expected prevalence |
|----------------|:------------------:|
| service_memory ↔ task_state | Most common |
| repo_memory → project_memory | Moderate |
| PII → user_profile (safety) | 5 of 26.3% |
| user_profile overuse | Persistent pattern |

## 4. Sensitive Store (Gold)

**5 genuine failures** — all PII stored as user_profile:
- Home address → user_profile
- Personal phone → user_profile
- Work email → user_profile
- Personal email → user_profile
- Recovery phone → service_memory

**Successfully skipped:** CI token, CMS token, SSN, credit card+CVV, PagerDuty API key. Credential safety improved over Qwen3-4B (2 fewer credential stores).

## 5. Dev→Gold Discrepancies

| Metric | Dev | Gold | Direction |
|--------|:---:|:----:|-----------|
| Exact | 34% | 41% | Dev underestimated |
| Target acc | 77.4% | 73.7% | Dev overestimated |
| Parse | 98% | 100% | Dev underestimated |

Dev was slightly optimistic on target accuracy (−3.7pp) but conservative on exact (+7pp). Net: dev was a fair development proxy.

## 6. Remaining Bottlenecks

| Bottleneck | Severity | Fix |
|-----------|:--------:|-----|
| PII → user_profile | High | Safety-focused training |
| Service/task confusion | Moderate | Target-balanced data |
| repo_memory weakness | Moderate | Target-balanced data |
| Exact ceiling at 41% | Low | Standard LoRA / r=16 |

---

*End of V0.5c Final Error Analysis.*
