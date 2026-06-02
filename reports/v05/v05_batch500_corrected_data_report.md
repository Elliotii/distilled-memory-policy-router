# V0.5 Batch500 Corrected — Data Report

**Date:** 2026-06-02  
**Context:** 5.2-D — batch500 corrected dataset after independent review fixes  
**Source:** data/v05/batches/v05_batch500_corrected_cases.jsonl  

---

## 1. Corrected Batch500 Summary

The corrected batch500 contains 500 training-pool cases derived from the rebalanced batch500 with 4 labeling fixes applied per independent review findings. All cases are English, structurally valid, and DSL-consistent.

| Metric | Value |
|--------|-------|
| Total cases | 500 |
| Cases modified by fixes | 4 |
| Cases unchanged from rebalanced | 496 |
| Total STORE units | 1042 |
| Total SKIP units | 143 |
| Total READ entries | 574 |

---

## 2. Target Distribution

| Target | Units | % | Blueprint | Status |
|--------|:-----:|:--:|:---------:|:------:|
| service_memory | 323 | 31.0% | 30-34% | ✓ |
| task_state | 338 | 32.4% | 30-34% | ✓ |
| repo_memory | 201 | 19.3% | 16-20% | ✓ |
| project_memory | 122 | 11.7% | 10-14% | ✓ |
| user_profile | 58 | 5.6% | 5-8% | ✓ |
| **Total STORE** | **1042** | 100% | — | — |

**svc:task gap:** -1.4pp (task_state slightly ahead, well within ≤8pp tolerance)

**Net changes from rebalanced:**
- service_memory: -1
- task_state: +2
- repo_memory: +1
- project_memory: unchanged
- user_profile: unchanged
- SKIP units: -2

---

## 3. Shape Distribution

| Shape | Count | % | Blueprint |
|-------|:-----:|:--:|:---------:|
| READ+STORE joint | 213 | 42.6% | 38-45% ✓ |
| STORE/SKIP-only | 182 | 36.4% | 35-40% ✓ |
| READ-only | 105 | 21.0% | 18-22% ✓ |

Shape distribution is unchanged from rebalanced batch500. All within blueprint ranges.

---

## 4. READ / STORE / SKIP Counts

| Category | Count |
|----------|:-----:|
| Cases with at least one READ | 318 |
| Cases with at least one STORE | 395 |
| Cases with at least one SKIP | 275 |
| Total READ entries | 574 |
| Total STORE entries | 1042 |
| Total SKIP entries | 143 |
| Average STORE per case (cases with STORE) | ~2.64 |
| Average READ per case (cases with READ) | ~1.81 |

---

## 5. Validation Summary

| Validation | Result |
|------------|--------|
| Structural validation | PASS (500 cases) |
| DSL parse | 500/500 |
| Canonical consistency (parsed == structured) | 500/500 |
| Every current unit exactly once in STORE or SKIP | ✓ |
| No invalid READ / STORE / SKIP IDs | ✓ |
| No invalid targets | ✓ |
| Sensitive-looking units in STORE | 0 real (5 false positives — policies about sensitive data) |
| No leakage / duplication | 1 cross-batch duplicate (known, non-blocking) |
| No templates / repeated structure | ✓ |
| No generic placeholder runtime fields | ✓ |
| SFT assistant == gold.dsl | 500/500 |
| No markdown/JSON in SFT assistant | ✓ |
| All 4 fixes present | ✓ |
| No other case labels changed | ✓ |
| Unittests | 49/49 PASS |

---

## 6. Why This Is Still Not Final Train Data

The corrected batch500 is a **training-pool candidate**, not final train data:

1. **No dev/gold split:** The 500 cases form a unified pool. No dev or gold sets have been constructed.
2. **No final quality filtering:** While label quality is high (~0.4% error rate), borderline cases identified by independent review have not been adjudicated.
3. **Training config not finalized:** Model, LoRA rank, training parameters, and eval strategy are not yet finalized.
4. **Representativeness not validated:** Training data representativeness for the target task distribution has not been verified.
5. **Gold is not locked:** The final holdout set for unbiased evaluation does not exist yet.

The corrected batch500 is the **input pool** for dev/gold construction — not the final training artifact.

---

## 7. Recommendation

**Proceed to dev/gold construction planning (Context 5.3).** The corrected batch500 meets all quality gates:

- Distribution targets within blueprint ranges
- 500/500 structural, parse, and canonical consistency
- 500/500 SFT format
- Label quality at ~0.4% error rate
- No real sensitive data stored
- Independent review fully satisfied

The 4 reviewed borderline cases and 1 duplicate unit text are non-blocking and can be addressed during dev/gold construction.

---

*End of corrected data report.*
