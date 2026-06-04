# gold_v2_002 Audit Adjudication Report

**Date:** 2026-06-04  

## Reviews

| Reviewer | Verdict | Key Claims |
|----------|:-------:|------------|
| DeepSeek/ClaudeCode | APPROVE with notes | v001 fixed; minor issues only |
| Opus | BLOCKER | 30 exact-text label conflicts; fleet vocabulary across all 8 domains |

## Audit Results (Local Scripts)

### A. Exact-Text Label Conflicts
**Opus claim: 30 conflicts. CONFIRMED.**

- 30 conflict groups, 61 affected instances
- All conflicts: SKIP vs STORE→task_state
- Root cause: same text from unit pool assigned to different positions in different cases
- No visible context disambiguates the conflicts
- **Verdict: BLOCKER**

### B. Normalized Skeleton Conflicts
**Opus claim: max repeat 16, 17 skeletons >7. CONFIRMED.**

- Max normalized skeleton repeat: 16
- 25 skeletons repeated >5 times
- 17 skeletons repeated >7 times
- 15 normalized skeleton conflict groups (different labels for same skeleton)
- **Verdict: BLOCKER**

### C. Fleet Vocabulary Contamination
**Opus claim: route/vehicle/fleet vocabulary across all domains. CONFIRMED.**

| Domain | Fleet Terms |
|--------|:-----------:|
| claims-adjudication | 70% |
| clinical-trials | 65% |
| energy-trading | 62% |
| event-streaming | 64% |
| fleet-optimizer | 159% |
| fraud-detection | 58% |
| smart-building | 67% |
| talent-acquisition | 62% |

All non-fleet domains have >58% fleet vocabulary. Root cause: unit pools for all 8 domains used similar templates derived from fleet-optimizer domain.
**Verdict: BLOCKER**

### D. DeepSeek Claims
- Domain leakage fixed: **CONFIRMED** ✅
- READ positional bias fixed: **CONFIRMED** ✅
- Sensitive/boundary within range: **CONFIRMED** ✅
- Template diversity "improved" but still below threshold: **Opus's stricter standard preferred**

## Final Adjudication

**v002 is REJECTED.** Opus's blockers are confirmed by local audit. Three independent issues (exact-text conflicts, skeleton conflicts, fleet vocabulary contamination) are genuine and require regeneration.
