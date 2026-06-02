# V0.5 Gold Draft Data Report

**Date:** 2026-06-02  
**Context:** 5.3-C2  

---

## 1. Gold Draft Summary

| Property | Value |
|----------|-------|
| Total cases | 100 |
| gold_core | 70 |
| gold_hard | 30 |
| Total STORE units | 211 |
| Total READ decisions | 92 |
| Total SKIP units | 43 |

## 2. Target Distribution

| Target | Count | % |
|--------|:-----:|:--:|
| service_memory | 69 | 32.7% |
| task_state | 71 | 33.6% |
| repo_memory | 36 | 17.1% |
| project_memory | 25 | 11.8% |
| user_profile | 10 | 4.7% |

user_profile at 4.7% is slightly below the 5-8% target. This is acceptable for gold which will be adjudicated.

## 3. Shape Distribution

| Shape | Count | % |
|-------|:-----:|:--:|
| READ+STORE joint | 35 | 35% |
| STORE/SKIP-only | 42 | 42% |
| READ-only | 23 | 23% |

## 4. Tag Distribution

| Tag | Cases |
|-----|:-----:|
| service_invariant | 55 |
| task_progress | 48 |
| store_skip_only | 42 |
| read_store_joint | 35 |
| temporary_request | 30 |
| read_only | 23 |
| repo_convention | 23 |
| project_vs_repo | 22 |
| related_but_useless | 16 |
| read_selectivity | 15 |
| target_boundary | 14 |
| sensitive_boundary | 10 |
| user_profile_boundary | 10 |
| stale_memory | 8 |
| service_vs_task_state | 6 |
| project_memory_vs_task_state | 4 |
| repo_vs_service | 4 |

## 5. READ / STORE / SKIP Counts

| Metric | Count |
|--------|:-----:|
| Total READ decisions | 92 |
| Total STORE units | 211 |
| Total SKIP units | 43 |
| Cases with READ | 54 |
| Cases with STORE | 77 |
| Cases with SKIP | 44 |

## 6. Domain Distribution

| Project | Cases |
|---------|:-----:|
| ci-pipeline | 19 |
| content-platform | 19 |
| financial-reporting | 17 |
| health-monitor | 16 |
| shipping-logistics | 15 |
| compliance-audit | 14 |

## 7. Candidate Memory Distribution

| Memories | Cases |
|:--------:|:-----:|
| 0 | 42 |
| 1 | 5 |
| 2 | 36 |
| 3 | 14 |
| 4 | 3 |

## 8. Representative Examples

### Gold core — READ+STORE joint (v05_gold_core_0041)

ci-pipeline / deploy-gate adding canary deployment support. Reads current deploy behavior + config structure. Stores canary capability (project_memory), config path (repo_memory), testing plan (task_state).

### Gold core — STORE/SKIP-only (v05_gold_core_0028)

financial-reporting recording project scope decision. Stores: project scope (no crypto → project_memory), reconciliation rule (service_memory), quarterly task (task_state).

### Gold hard — service_vs_task_state (v05_gold_hard_0001)

Deploy-gate smoke test: u1 uses "should run" — boundary between durable spec and implementation plan.

### Gold hard — read_selectivity (v05_gold_hard_0029)

Test-runner execution order: 4 memories about test-runner, only 1 answers the specific question about execution ORDER.

## 9. user_profile 4.7% Note

The user_profile target (4.7%) is slightly below the 5-8% planned range. This is acceptable for gold because:
1. Gold hard cases include 4 user_profile vs sensitive/private boundary cases
2. The distribution can be adjusted during adjudication if needed
3. The primary evaluation metrics (STORE unit F1, target accuracy) are robust to small per-target n

## 10. Limitations

- 25 post-processing adjustments from original composition
- Single-pass composition, not human-adjudicated
- Gold hard cases independently composed, not manually curated
- user_profile under-represented relative to target range

---

*End of V0.5 Gold Draft Data Report.*
