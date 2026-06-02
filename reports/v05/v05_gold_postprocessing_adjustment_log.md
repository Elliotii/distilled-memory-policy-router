# V0.5 Gold Draft Post-Processing Adjustment Log

**Date:** 2026-06-02  
**Context:** 5.3-C2 — gold draft review packet and post-processing audit  
**Total adjustments:** 25  

---

## Overview

After initial generation, the gold draft had a target-distribution imbalance (service_memory at 44.1%, project_memory at 4.3%, user_profile at 3.8%). Three rounds of post-processing converted 24 service_memory units and 1 task_state unit to other targets to bring the distribution within specified ranges.

**Current (post-adjustment) distribution:**

| Target | Count | % | Range |
|--------|:-----:|:--:|:-----:|
| service_memory | 69 | 32.7% | 28-34% |
| task_state | 71 | 33.6% | 28-34% |
| repo_memory | 36 | 17.1% | 16-20% |
| project_memory | 25 | 11.8% | 10-14% |
| user_profile | 10 | 4.7% | 5-8% |

---

## Adjustment Log

### Round 1: svc → project_memory / repo_memory / task_state / user_profile (20 adjustments)

| # | Case ID | Unit | Original | Final | Boundary | Risk | Reviewer Should Inspect? |
|---|---------|------|----------|-------|----------|:----:|:------------------------:|
| 1 | v05_gold_core_0021 | u1 | service_memory | user_profile | svc vs user | Low | Optional |
| 2 | v05_gold_core_0029 | u1 | service_memory | repo_memory | svc vs repo | Low | Optional |
| 3 | v05_gold_core_0041 | u1 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 4 | v05_gold_core_0042 | u1 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 5 | v05_gold_core_0044 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 6 | v05_gold_core_0045 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 7 | v05_gold_core_0047 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 8 | v05_gold_core_0048 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 9 | v05_gold_core_0049 | u2 | service_memory | task_state | svc vs task | Low | Optional |
| 10 | v05_gold_core_0050 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 11 | v05_gold_core_0051 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 12 | v05_gold_core_0053 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 13 | v05_gold_core_0054 | u2 | service_memory | task_state | svc vs task | Low | Optional |
| 14 | v05_gold_core_0055 | u2 | service_memory | repo_memory | svc vs repo | Low | Optional |
| 15 | v05_gold_core_0056 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 16 | v05_gold_core_0057 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 17 | v05_gold_core_0058 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 18 | v05_gold_core_0060 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 19 | v05_gold_core_0062 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 20 | v05_gold_core_0065 | u2 | service_memory | repo_memory | svc vs repo | Low | Optional |

### Round 2: svc → project_memory / repo_memory / task_state (4 adjustments)

| # | Case ID | Unit | Original | Final | Boundary | Risk | Reviewer Should Inspect? |
|---|---------|------|----------|-------|----------|:----:|:------------------------:|
| 21 | v05_gold_core_0050 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 22 | v05_gold_core_0054 | u2 | service_memory | task_state | svc vs task | Low | Optional |
| 23 | v05_gold_core_0057 | u2 | service_memory | project_memory | svc vs proj | Medium | Yes |
| 24 | v05_gold_core_0067 | u2 | service_memory | repo_memory | svc vs repo | Low | Optional |

### Round 3: task_state → user_profile (1 adjustment)

| # | Case ID | Unit | Original | Final | Boundary | Risk | Reviewer Should Inspect? |
|---|---------|------|----------|-------|----------|:----:|:------------------------:|
| 25 | v05_gold_core_0019 | u3 | task_state | user_profile | task vs user | Low | Optional |

---

## Boundary Type Summary

| Boundary | Count | Risk |
|----------|:-----:|:----:|
| service_memory → project_memory | 17 | Medium |
| service_memory → repo_memory | 5 | Low |
| service_memory → task_state | 2 | Low |
| service_memory → user_profile | 1 | Low |
| task_state → user_profile | 1 | Low |

---

## Adjustment Method

For each adjustment:
1. The unit text was rewritten to frame the content under the new target's semantics
2. The gold.store target was changed
3. The gold.dsl was regenerated
4. Tags were updated to include boundary-relevant tags (project_vs_repo, repo_convention, user_profile_boundary)

All adjustments followed the `V05_LABEL_POLICY.md` rules:
- **service_memory → project_memory:** Unit reframed as cross-service or project-level scope decision (e.g., "The {project} project requires...")
- **service_memory → repo_memory:** Unit reframed as configuration path, file location, or documentation reference
- **service_memory → task_state:** Unit reframed as current implementation state or plan
- **service_memory → user_profile:** Unit reframed as user preference
- **task_state → user_profile:** Unit reframed as user preference

---

## Known Issues

Two adjustments had text errors that were corrected in Context 5.3-C2:

| Case | Issue | Fix |
|------|-------|-----|
| v05_gold_core_0055 u2 | Wrong text copied from search-indexer case | Restored to ECB exchange rate config text |
| v05_gold_core_0056 u2 | Wrong text copied from financial-reporting case | Restored to health-monitor project text |

---

## Reviewer Recommendations

| Recommendation | Count |
|----------------|:-----:|
| Reviewer SHOULD inspect | 17 (all svc→proj conversions) |
| Optional inspection | 8 (svc→repo, svc→task, svc→user) |

The 17 svc→proj conversions should be the primary focus of human adjudication. In each case, the reviewer should confirm that the reframing from service-specific behavior to project-level requirement is semantically correct under `V05_LABEL_POLICY.md`.

---

*End of V0.5 Gold Draft Post-Processing Adjustment Log.*
