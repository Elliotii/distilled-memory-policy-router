# V0.5 Batch500 Rebalance Report

**Date:** 2026-06-02
**Context:** 5.2-B — batch500 distribution rebalance

---

## 1. Scope

This report covers the distribution rebalancing of batch500, replacing 50 service-heavy new200 cases with balanced replacement cases to bring the STORE target distribution within blueprint targets.

---

## 2. Why Rebalance Was Needed

The original batch500 (Context 5.2-A) had:
- service_memory at 39.1% (blueprint target: 30-34%) — 5pp above upper bound
- project_memory at 7.9% (target: 10-14%) — 2.1pp below lower bound
- user_profile at 3.8% (target: 5-8%) — 1.2pp below lower bound

While task_state (32.7%) and repo_memory (16.4%) were within targets, the service_memory overshoot would bias LoRA training toward over-predicting service_memory.

---

## 3. Original Target Distribution

| Target | Units | % | Blueprint |
|--------|:-----:|:--:|:---------:|
| service_memory | 399 | 39.1% | 30-34% |
| task_state | 334 | 32.7% | 30-34% |
| repo_memory | 167 | 16.4% | 16-20% |
| project_memory | 81 | 7.9% | 10-14% |
| user_profile | 39 | 3.8% | 5-8% |
| **Total** | **1020** | — | — |

svc:task gap: 6.4pp

---

## 4. Rebalance Strategy

**Approach:** Replace cases, not relabel. Each replaced case gets a completely new case definition with the same case_id but different semantic content and target distribution.

**Selection criteria:**
1. Replace new200 cases with 2+ service_memory units (25 cases identified)
2. Replace additional new200 cases with 1+ service_memory to add project/user/repo diversity (25 more cases)
3. Do NOT touch repaired batch300 seed (300 cases unchanged)
4. Do NOT force incorrect labels — write genuinely different case content

**Replacement case design:**
- 15 project_memory-focused cases (cross-service policies, scope, compliance)
- 8 user_profile-focused cases (stable non-sensitive preferences)
- 12 repo_memory + task_state cases (CI, config, testing, release conventions)
- 15 balanced mixed-target cases (project + repo + task, or project + task, etc.)

---

## 5. Replaced Cases

**50 cases replaced** from new200 (v05_batch500_0001–0200):

```
v05_batch500_0002, v05_batch500_0010, v05_batch500_0011, v05_batch500_0015,
v05_batch500_0027, v05_batch500_0033, v05_batch500_0038, v05_batch500_0042,
v05_batch500_0044, v05_batch500_0053, v05_batch500_0057, v05_batch500_0062,
v05_batch500_0065, v05_batch500_0067, v05_batch500_0069, v05_batch500_0071,
v05_batch500_0074, v05_batch500_0078, v05_batch500_0088, v05_batch500_0091,
v05_batch500_0092, v05_batch500_0093, v05_batch500_0098, v05_batch500_0099,
v05_batch500_0100, v05_batch500_0101, v05_batch500_0102, v05_batch500_0103,
v05_batch500_0104, v05_batch500_0105, v05_batch500_0106, v05_batch500_0112,
v05_batch500_0118, v05_batch500_0119, v05_batch500_0121, v05_batch500_0122,
v05_batch500_0123, v05_batch500_0125, v05_batch500_0126, v05_batch500_0127,
v05_batch500_0129, v05_batch500_0131, v05_batch500_0132, v05_batch500_0135,
v05_batch500_0145, v05_batch500_0192, v05_batch500_0193, v05_batch500_0194,
v05_batch500_0197, v05_batch500_0198
```

**Original batch300:** 300 cases unchanged, 0 cases replaced.

---

## 6. Replacement Case Summary

| Category | Cases | Key contribution |
|----------|:-----:|------------------|
| project_memory-focused | 15 | Cross-service policies, scope exclusions, compliance standards |
| user_profile-focused | 8 | Stable user preferences for display, workflow, notification, search |
| repo_memory + task_state | 12 | CI commands, test paths, config conventions, release processes |
| Balanced mixed-target | 15 | project+repo+task combos, governance policies |

Average replacement case: 0.1 service_memory units, 1.8 project/repo/user units, 1.0 task_state units.

---

## 7. Before/After Target Counts

| Target | Before | After | Change |
|--------|:------:|:-----:|:------:|
| service_memory | 399 | 324 | -75 |
| task_state | 334 | 336 | +2 |
| repo_memory | 167 | 200 | +33 |
| project_memory | 81 | 122 | +41 |
| user_profile | 39 | 58 | +19 |
| **Total STORE** | **1020** | **1040** | +20 |

---

## 8. Before/After Target Percentages

| Target | Before | After | Blueprint | Status |
|--------|:------:|:-----:|:---------:|:------:|
| service_memory | 39.1% | **31.2%** | 30-34% | ✓ |
| task_state | 32.7% | **32.3%** | 30-34% | ✓ |
| repo_memory | 16.4% | **19.2%** | 16-20% | ✓ |
| project_memory | 7.9% | **11.7%** | 10-14% | ✓ |
| user_profile | 3.8% | **5.6%** | 5-8% | ✓ |

**svc:task gap:** 6.4pp → **-1.1pp** (task_state now slightly ahead, well within ≤8pp)

---

## 9. Before/After Shape Distribution

| Shape | Before | After | Target |
|-------|:------:|:-----:|:------:|
| READ+STORE joint | 41.6% | **42.6%** | 38-45% |
| STORE/SKIP-only | 37.4% | **36.4%** | 35-40% |
| READ-only | 21.0% | **21.0%** | 18-22% |

Shape distribution essentially unchanged — all within targets.

---

## 10. Validation Results

| Validation | Result |
|------------|--------|
| Structural validation (rebalanced) | PASS (500 cases) |
| DSL parse | 500/500 |
| Canonical consistency | 500/500 |
| SFT assistant == gold.dsl | 500/500 |
| No markdown/JSON in SFT | 500/500 |
| Original batch500 unchanged | Verified |
| Unittests | 49/49 OK |
| Duplicate case_ids | 0 |
| Sensitive STOREd | 0 real (5 false positives from batch300) |

---

## 11. Remaining Risks

1. **Replacement case quality:** The 50 replacement cases were hand-crafted following all label policies. No templates or fill-in-the-blank patterns. However, they have not been independently reviewed.

2. **batch300 false positives:** 5 units from repaired batch300 trigger the keyword-based sensitive check but are storing policies/rules about sensitive data handling, not actual sensitive data. These were previously reviewed and accepted in Context 5.1-D.

3. **Slightly increased total STORE units:** The rebancing added 20 more STORE units (from 1020 to 1040) because replacement cases have slightly more units on average. This is negligible.

---

## 12. Recommendation

**The rebalanced batch500 meets all blueprint targets.** All five STORE targets are within their specified ranges, the svc:task gap is negligible, and shape distribution is preserved. The data is ready for independent review and subsequent dev/gold construction.

**Recommended next action:** Proceed to independent human review (spot-check 50 cases = 10%) before dev/gold construction.

---

*End of rebalance report.*
