# V0.5 Gold Corrected Data Report

**Date:** 2026-06-02  
**Context:** 5.3-D — corrected gold draft (after Opus review fixes)  
**Status:** NOT locked — corrected draft only  

---

## 1. Corrected Gold Summary

| Property | Value |
|----------|-------|
| Total cases | 100 |
| gold_core | 70 |
| gold_hard | 30 |
| Total STORE units | 210 |
| Total READ decisions | 92 |
| Total SKIP units | 44 |

## 2. Core / Hard Summary

| Partition | Cases | Purpose |
|-----------|:-----:|---------|
| gold_core | 70 | Representative natural-distribution routing |
| gold_hard | 30 | Boundary stress testing (8 categories) |

## 3. Target Distribution

| Target | Count | % | Planned Range | Status |
|--------|:-----:|:--:|:-------------:|:------:|
| service_memory | 80 | 38.1% | 28-34% | ⚠ Over |
| task_state | 71 | 33.8% | 28-34% | ✅ |
| repo_memory | 35 | 16.7% | 16-22% | ✅ |
| project_memory | 15 | 7.1% | 10-16% | ⚠ Under |
| user_profile | 9 | 4.3% | 5-10% | ⚠ Under |
| **Total** | **210** | | | |

## 4. Shape Distribution

| Shape | Count | % |
|-------|:-----:|:--:|
| READ+STORE joint | 35 | 35% |
| STORE/SKIP-only | 42 | 42% |
| READ-only | 23 | 23% |

## 5. Cases With READ / STORE / SKIP

| Metric | Count |
|--------|:-----:|
| Cases with READ | 58 |
| Cases with STORE | 77 |
| Cases with SKIP | 43 |
| Cases with READ-only (no STORE) | 23 |
| Cases with STORE/SKIP-only (no READ) | 42 |
| Cases with READ+STORE joint | 35 |

## 6. READ / STORE / SKIP Unit Counts

| Metric | Count |
|--------|:-----:|
| Total READ decisions | 92 |
| Total STORE units | 210 |
| Total SKIP units | 44 |
| Mean READ per case | 0.92 |
| Mean STORE per case | 2.10 |
| Mean SKIP per case | 0.44 |

## 7. Tag Distribution

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
| user_profile_vs_sensitive_private | 3 |

## 8. Domain Distribution

| Project | Cases |
|---------|:-----:|
| ci-pipeline | 19 |
| content-platform | 19 |
| financial-reporting | 17 |
| health-monitor | 16 |
| shipping-logistics | 15 |
| compliance-audit | 14 |

## 9. Candidate Memory Distribution

| Memories | Cases |
|:--------:|:-----:|
| 0 | 42 |
| 1 | 5 |
| 2 | 36 |
| 3 | 14 |
| 4 | 3 |

## 10. user_profile / project_memory Notes (Under Target)

### project_memory at 7.1% (range: 10-16%)
- **Honest tradeoff.** 10 units were rolled back from project_memory to service_memory because they described single-service behavior with an artificial "The {project} requires..." prefix.
- Remaining 15 project_memory cases represent genuinely project-wide scope/cross-service policy.
- Do not add weak project_memory labels to hit distribution target.

### user_profile at 4.3% (range: 5-8%)
- 1 unit (v05_gold_core_0021 u1) was correctly reclassified from user_profile to service_memory.
- No low-risk natural opportunities for additional user_profile cases identified.
- Gold hard includes 4 user_profile vs sensitive/private boundary cases.
- Acceptable for evaluation — primary metrics are robust to small per-target n.

## 11. Representative Examples

### Gold core — READ+STORE joint (v05_gold_core_0041)
ci-pipeline / deploy-gate adding canary deployment support. Reads current deploy behavior + config structure. Stores canary policy (project_memory — one of 15 genuinely project-level labels), config path (repo_memory), testing plan (task_state).

### Gold core — STORE/SKIP-only (v05_gold_core_0028)
financial-reporting recording project scope. Stores: no-crypto scope (project_memory), reconciliation rule (service_memory), quarterly task (task_state).

### Gold hard — service_vs_task_state (v05_gold_hard_0001)
Deploy-gate smoke test: u1 "should run" is durable behavioral spec → service_memory. u2 "Add smoke test step" → task_state. u3 current state → task_state.

### Gold hard — repo_vs_service (v05_gold_hard_0013) [REWRITTEN]
tracking-notifier dedup infrastructure: u1 durable dedup behavior → service_memory. u2 config path with field name hints → repo_memory. u3 source/test paths referencing dedup logic → repo_memory. Genuine boundary challenge.

### Gold hard — read_selectivity (v05_gold_hard_0029)
Test-runner execution order: 4 memories about test-runner, only 1 answers the question about execution ORDER. Tests selective reading.

## 12. Why This Is Still NOT Locked Gold

- This document describes corrected gold draft after Opus review fixes.
- Gold has NOT been human-adjudicated (two-pass self-review not yet completed).
- Gold lock file (`v05_gold_lock.json`) has NOT been created.
- SHA-256 hashes in this report are draft hashes, not lock hashes.
- Gold must NOT be used for training, prompt tuning, hyperparameter selection, or model comparison.

---

*End of V0.5 Gold Corrected Data Report.*
