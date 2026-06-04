# V0.5e gold_v2 — Opus 4.8 Review Response

**Date:** 2026-06-04  

---

## External Review Summary

An external Opus 4.8 Thinking review of the v0.5c/v0.5d results recommended:

1. **gold_v2 is needed for final r=16 claim** — old gold has been evaluated 3 times and is no longer fully blind.

2. **n=100 is too small for 1-5pp claims** — statistical uncertainty at n=100 is ~4-5pp for binary outcomes near 35-40%. Gaps of 1-5pp are statistically fragile without CIs.

3. **Use paired comparisons and confidence intervals** — bootstrap CIs on paired differences account for case-level correlation better than independent proportions.

4. **Re-run all candidate systems on gold_v2** — don't compare new r=16 results to old-gold r=8 results as same-split evidence.

5. **Do not compare gold_v2 metrics to old-gold metrics** — cross-set comparisons are not valid same-split evidence.

## How This Project Adopts the Review

| Recommendation | Adoption |
|---------------|----------|
| gold_v2 needed | ✅ **Adopted.** 150-case gold_v2 with pre-registered protocol. |
| n=100 too small | ✅ **Adopted.** n=150 active + 30 optional holdout = 180 total possible. |
| Paired CIs | ✅ **Adopted.** Bootstrap 95% CI on paired exact difference. CI lower bound > 0 required for "better" claim. |
| Re-run all systems | ✅ **Adopted.** r=16, r=8, Qwen3.5 few-shot, Qwen3-4B r=8 all evaluated on same gold_v2. |
| No cross-set comparison | ✅ **Adopted.** Old gold is secondary/non-blind only. |

## Modifications from Review

| Review Suggestion | Project Decision |
|-------------------|-----------------|
| Opus suggested even larger n | Project uses 150 (up from 100). 30-case holdout for future. Larger n would increase construction cost without proportionate benefit at this stage. |
| Full McNemar test | Project includes McNemar-style table if feasible, but bootstrap is primary CI method. |

## Review Acceptance

The external review's core concerns (blinding, n-size, CIs, re-evaluation) are fully addressed. The project adopts a statistically rigorous protocol while keeping scope feasible for a single-researcher project.

---

*End of Opus Review Response.*
