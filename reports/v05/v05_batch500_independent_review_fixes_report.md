# V0.5 Batch500 Independent Review — Fixes Applied Report

**Date:** 2026-06-02  
**Context:** 5.2-D — apply batch500 independent review fixes  
**Source:** Rebalanced batch500 → corrected batch500  

---

## 1. Scope

This report documents the 4 labeling fixes identified by the independent review (Context 5.2-C) and applied to the rebalanced batch500, producing a corrected batch500 training-pool candidate.

---

## 2. Independent Review Verdict

**APPROVE WITH MINOR NOTES** — proceed to dev/gold construction after 4 labeling fixes.

- Target distribution: all 5 targets within blueprint ranges ✓
- Shape distribution: all 3 shapes within blueprint ranges ✓  
- Sensitive STORE: 0 real ✓
- SFT format: 500/500 clean ✓
- Label quality: ~0.4% error rate (4/1040 STORE decisions)
- No blockers found.

---

## 3. Four Fixes Applied

### Fix 1: v05_batch100_0039 u1
**Change:** service_memory → task_state  
**Reason:** "Add a grade appeal workflow..." follows the action-verb rule (§7) and reads as implementation/task state.

| | Before | After |
|---|---|---|
| u1 target | service_memory | **task_state** |
| DSL | `STORE service_memory u1` | `STORE task_state u1` |

### Fix 2: v05_batch50_0014 u3
**Change:** repo_memory → task_state  
**Reason:** "Add a priority field to the notification payload schema in the API docs." — implementation action, not a repo path/command/convention.

| | Before | After |
|---|---|---|
| u3 target | repo_memory | **task_state** |
| DSL | `STORE repo_memory u3` | `STORE task_state u3` |

### Fix 3: v05_batch500_0096 u3
**Change:** SKIP → repo_memory  
**Reason:** "The documentation for exclusion decisions lives under docs/v05/scope_exclusions.md." — explicit file path should be repo_memory.

| | Before | After |
|---|---|---|
| u3 status | SKIP | **STORE repo_memory** |
| gold.skip | ["u2", "u3"] | ["u2"] |
| gold.store | [project_memory u1] | [project_memory u1, repo_memory u3] |
| DSL | `SKIP u2,u3` | `STORE repo_memory u3` ... `SKIP u2` |

### Fix 4: v05_batch500_0097 u3
**Change:** SKIP → repo_memory  
**Reason:** "The roadmap document is tracked in docs/planning/roadmap_2026_Q3.md." — explicit file path should be repo_memory.

| | Before | After |
|---|---|---|
| u3 status | SKIP | **STORE repo_memory** |
| gold.skip | ["u1", "u3"] | ["u1"] |
| gold.store | [task_state u2] | [task_state u2, repo_memory u3] |
| DSL | `SKIP u1,u3` | `STORE repo_memory u3` ... `SKIP u1` |

---

## 4. Exact Before/After DSL

### v05_batch100_0039
```
BEFORE:                        AFTER:
READ m1,m2                     READ m1,m2
STORE service_memory u1        STORE task_state u1
STORE service_memory u2        STORE service_memory u2
STORE service_memory u3        STORE service_memory u3
SKIP NONE                      SKIP NONE
```

### v05_batch50_0014
```
BEFORE:                        AFTER:
READ m1,m2                     READ m1,m2
STORE service_memory u1        STORE service_memory u1
STORE repo_memory u3           STORE task_state u3
SKIP u2                        SKIP u2
```

### v05_batch500_0096
```
BEFORE:                        AFTER:
READ NONE                      READ NONE
STORE project_memory u1        STORE project_memory u1
SKIP u2,u3                     STORE repo_memory u3
                               SKIP u2
```

### v05_batch500_0097
```
BEFORE:                        AFTER:
READ NONE                      READ NONE
STORE task_state u2            STORE task_state u2
SKIP u1,u3                     STORE repo_memory u3
                               SKIP u1
```

---

## 5. Distribution Before/After

| Target | Before (Rebalanced) | After (Corrected) | Change | Blueprint | Status |
|--------|:-----:|:-----:|:------:|:---------:|:------:|
| service_memory | 324 (31.2%) | 323 (31.0%) | -1 | 30-34% | ✓ |
| task_state | 336 (32.3%) | 338 (32.4%) | +2 | 30-34% | ✓ |
| repo_memory | 200 (19.2%) | 201 (19.3%) | +1 | 16-20% | ✓ |
| project_memory | 122 (11.7%) | 122 (11.7%) | 0 | 10-14% | ✓ |
| user_profile | 58 (5.6%) | 58 (5.6%) | 0 | 5-8% | ✓ |
| **Total STORE** | 1040 | 1042 | +2 | — | — |
| **Total SKIP units** | 145 | 143 | -2 | — | — |

All five targets remain within blueprint ranges. svc:task gap: -1.1pp → -1.4pp (well within ≤8pp).

### Shape Distribution (unchanged)

| Shape | Count | % | Blueprint |
|-------|:-----:|:--:|:---------:|
| READ+STORE joint | 213 | 42.6% | 38-45% ✓ |
| STORE/SKIP-only | 182 | 36.4% | 35-40% ✓ |
| READ-only | 105 | 21.0% | 18-22% ✓ |

---

## 6. Validation Results

| Validation | Result |
|------------|--------|
| Corrected batch500 exactly 500 cases | ✓ |
| Corrected SFT exactly 500 rows | ✓ |
| Structural validation | PASS (500) |
| DSL parse | 500/500 |
| Canonical consistency | 500/500 |
| SFT assistant == gold.dsl | 500/500 |
| No markdown/JSON in SFT | 500/500 |
| All 4 fixes present | ✓ |
| No other labels changed | ✓ (0 unexpected changes) |
| Sensitive stored | 0 real (5 keyword false positives, previously reviewed) |
| Unittests | 49/49 PASS |
| Repeated unit texts | 1 (known cross-batch duplicate, non-blocking) |

---

## 7. Confirmation: No Other Labels Changed

A comparison of all 500 corrected cases against the rebalanced originals confirmed:
- **0** unmodified cases have any DSL change
- Only the 4 targeted cases were modified
- All other 496 cases have identical gold labels and DSL

---

## 8. Remaining Non-Blocking Borderline Cases

Per independent review, 6 borderline cases remain unchanged per instructions:
1. v05_batch500_0062 u2 — repo_memory vs project_memory (config file convention vs project-wide policy)
2. v05_batch200_0039 u2 — repo_memory vs service_memory (schema description)
3. v05_batch500_0091 u1 — repo_memory vs project_memory (operational process)
4. v05_batch500_0119 u2 — repo_memory vs project_memory (SLA procedure)
5. v05_batch500_0096 u2 — SKIP (speculative proposal) — confirmed correct, only u3 needed fix
6. v05_batch50_0003 + v05_batch300_0001 m1 — duplicate candidate memory (cross-batch, low severity)

These are non-blocking and should be addressed during dev/gold construction if desired.

---

## 9. Can Corrected Batch500 Move to Dev/Gold Planning?

**YES.** The corrected batch500 meets all quality and distribution criteria:

- All 5 target distributions within blueprint ranges
- All 3 shape distributions within ranges
- 0 real sensitive data stored
- 500/500 structural validation
- 500/500 DSL parse
- 500/500 canonical consistency
- 500/500 SFT format
- 49/49 unittests
- 4/1040 labeling errors fixed (original error rate ~0.4%)
- No other cases affected

**Recommendation: Proceed to dev/gold construction planning (Context 5.3).**

---

*End of independent review fixes report.*
