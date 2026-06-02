# V0.5 Gold Opus Review Fixes Report

**Date:** 2026-06-02  
**Context:** 5.3-D — apply Opus gold review fixes  
**Status:** Fixes applied — gold NOT locked  

---

## 1. Scope

Applied all required fixes from the Opus 4.8 Thinking advisory review of the v0.5 gold draft. 12 required fixes were applied across 5 groups (A-E). 5 borderline cases were reviewed with 2 additional changes. Notes were synchronized for all 23 post-processing adjusted cases.

## 2. Opus Verdict

Opus review found:
- **No need to regenerate the full gold draft** — the 100-case draft is structurally sound
- **Correction required before lock** — 6 specific findings that are blockers
- The gold draft is on the right track but needs targeted fixes before lock and final adjudication

## 3. Blockers Accepted

| # | Finding | Accepted? |
|---|---------|:---------:|
| 1 | Several post-processing svc→proj changes are distribution-driven rather than semantic | ✅ Yes — 8 rollbacks applied |
| 2 | Notes for adjusted cases are out of sync with final labels | ✅ Yes — 23 notes synchronized |
| 3 | gold_hard_0014 stores a work email as repo_memory (violates sensitive/PII policy) | ✅ Yes — email → SKIP |
| 4 | gold_hard_0013 is too clean/easy for hard subset | ✅ Yes — replaced |
| 5 | Phone number in gold duplicates train sensitive-boundary pattern | ✅ Yes — changed to +1-555-0147 |
| 6 | Data report has inconsistent READ/SKIP case counts | ✅ Yes — corrected in new report |

## 4. Required Fixes Applied

### Fix Group A: svc→proj Rollback to service_memory (8 changes)

Rationale: These units describe single-service durable behavior, not project-level scope/policy. The "The {project} project requires..." prefix is not sufficient to make them project_memory.

| # | Case | Unit | Old → New | Unit Text (abbreviated) |
|---|------|------|-----------|--------------------------|
| 1 | v05_gold_core_0044 | u2 | proj→svc | "The health-monitor project requires that SSL certificate expiry alerts escalate..." |
| 2 | v05_gold_core_0047 | u2 | proj→svc | "The ci-pipeline project requires that flaky tests be reported automatically..." |
| 3 | v05_gold_core_0050 | u2 | proj→svc | "The health-monitor project requires that correlated alerts list the root cause first..." |
| 4 | v05_gold_core_0051 | u2 | proj→svc | "The shipping-logistics project requires proactive customer notification..." |
| 5 | v05_gold_core_0056 | u2 | proj→svc | "The health-monitor project requires that API response body validation failures log..." |
| 6 | v05_gold_core_0057 | u2 | proj→svc | "The shipping-logistics project requires that EV charging stops add no more than 30 min..." |
| 7 | v05_gold_core_0058 | u2 | proj→svc | "The compliance-audit project requires that all custom policies pass JSON schema validation..." |
| 8 | v05_gold_core_0066 | u2 | proj→svc | "The content-platform project requires language-aware search..." |

### Fix Group B: False user_profile (1 change)

| # | Case | Unit | Old → New | Rationale |
|---|------|------|-----------|-----------|
| 1 | v05_gold_core_0021 | u1 | user_profile→service_memory | "primary-language content searchable within 5 minutes" is an indexing SLA/service behavior, not a stable user preference |

### Fix Group C: Work email → SKIP (1 change)

| # | Case | Unit | Old → New | Rationale |
|---|------|------|-----------|-----------|
| 1 | v05_gold_hard_0014 | u2 | repo_memory→SKIP | Email addresses are sensitive/private per V05_LABEL_POLICY. No work-email exception. |

### Fix Group D: Phone Number Collision (1 change)

| # | Case | Unit | Change | Rationale |
|---|------|------|--------|-----------|
| 1 | v05_gold_hard_0015 | u3 | +1-555-0198 → +1-555-0147 | Avoid exact sensitive-token overlap with train sensitive-boundary pattern |

### Fix Group E: Replace Too-Easy Hard Case (1 change)

| # | Case | Change |
|---|------|--------|
| 1 | v05_gold_hard_0013 | Replaced with genuine repo-vs-service boundary case |

**New v05_gold_hard_0013:**
- **u1 (svc):** Tracking-notifier deduplication behavior by shipment_id and event_type within 10-min window
- **u2 (repo):** Config path `config/notification_dedup.yaml` with field names that hint at service behavior
- **u3 (repo):** Source code path and test paths, referencing dedup logic
- **Challenge:** u2 straddles config path + field descriptions; u3 mentions dedup logic in path context. Model must resist being pulled toward service_memory by behavioral keywords in path descriptions.

**v05_gold_hard_0011 review:** Reviewed as optionally requested. It is clean (clear service_vs_repo distinction) but still useful as a lower-hardness boundary case for training calibration. **Kept unchanged.**

## 5. Before/After DSL for Each Modified Case

### Group A (svc→proj rollback)

| Case | Before DSL (relevant line) | After DSL (relevant line) |
|------|---------------------------|---------------------------|
| v05_gold_core_0044 | `STORE project_memory u2` | `STORE service_memory u2` |
| v05_gold_core_0047 | `STORE project_memory u2` | `STORE service_memory u2` |
| v05_gold_core_0050 | `STORE project_memory u2` | `STORE service_memory u2` |
| v05_gold_core_0051 | `STORE project_memory u2` | `STORE service_memory u2` |
| v05_gold_core_0056 | `STORE project_memory u2` | `STORE service_memory u2` |
| v05_gold_core_0057 | `STORE project_memory u2` | `STORE service_memory u2` |
| v05_gold_core_0058 | `STORE project_memory u2` | `STORE service_memory u2` |
| v05_gold_core_0066 | `STORE project_memory u2` | `STORE service_memory u2` |

### Group B

| Case | Before DSL | After DSL |
|------|------------|-----------|
| v05_gold_core_0021 | `STORE user_profile u1` | `STORE service_memory u1` |

### Group C

| Case | Before DSL | After DSL |
|------|------------|-----------|
| v05_gold_hard_0014 | `STORE repo_memory u2` | `SKIP u2` (u2 removed from STORE, u3 remains STORE task_state) |

### Group D

| Case | Before | After |
|------|--------|-------|
| v05_gold_hard_0015 | u3 text: "...+1-555-0198" | u3 text: "...+1-555-0147" |

### Group E

| Case | Before DSL | After DSL |
|------|------------|-----------|
| v05_gold_hard_0013 | `STORE service_memory u1\nSTORE repo_memory u2\nSTORE repo_memory u3` | `STORE service_memory u1\nSTORE repo_memory u2\nSTORE repo_memory u3` (same targets, entirely new unit texts) |

## 6. Borderline Review Results

| # | Case | Unit | Current | Opus Flag | Decision | Rationale | Confidence |
|---|------|------|---------|-----------|----------|-----------|:----------:|
| 1 | v05_gold_core_0045 | u2 | project_memory | Could be svc | **KEPT proj** | Manual dispatcher review threshold is project-level operational policy, not route-optimizer specific | Medium |
| 2 | v05_gold_core_0048 | u2 | project_memory | Could be svc | **KEPT proj** | WCAG 2.1 AA accessibility compliance is inherently project-level | Medium |
| 3 | v05_gold_core_0062 | u2 | project_memory | Could be svc | **CHANGED to svc** | Hourly digest is alert-dispatcher-specific behavior; "project requires" prefix insufficient | High |
| 4 | v05_gold_core_0069 | u2 | project_memory | Could be svc | **CHANGED to svc** | 30-second timeout is route-optimizer service SLA, not project-wide policy | High |
| 5 | v05_gold_core_0049 | u2 | task_state | Could be svc | **KEPT task** | "should run before" phrasing indicates implementation intention, not durable spec | Medium |

**Result:** 3 kept, 2 changed (both project_memory → service_memory).

## 7. Notes Synchronization Summary

All 23 post-processing adjusted cases had their notes rewritten to match final labels. Each note now:
- States the actual final target labels
- Does not reference original generation labels unless explicitly contrasting
- Justifies the current label with reasoning from V05_LABEL_POLICY

Cases synchronized: v05_gold_core_0019, v05_gold_core_0021, v05_gold_core_0029, v05_gold_core_0041, v05_gold_core_0042, v05_gold_core_0044, v05_gold_core_0045, v05_gold_core_0047, v05_gold_core_0048, v05_gold_core_0049, v05_gold_core_0050, v05_gold_core_0051, v05_gold_core_0053, v05_gold_core_0054, v05_gold_core_0055, v05_gold_core_0056, v05_gold_core_0057, v05_gold_core_0058, v05_gold_core_0060, v05_gold_core_0062, v05_gold_core_0065, v05_gold_core_0066, v05_gold_core_0067.

## 8. Distribution Before/After

### Before (Gold Draft)

| Target | Count | % | Range |
|--------|:-----:|:--:|:-----:|
| service_memory | 69 | 32.7% | 28-34% |
| task_state | 71 | 33.6% | 28-34% |
| repo_memory | 36 | 17.1% | 16-22% |
| project_memory | 25 | 11.8% | 10-16% |
| user_profile | 10 | 4.7% | 5-10% |
| **Total** | **211** | | |

### After (Corrected Gold)

| Target | Count | % | Range |
|--------|:-----:|:--:|:-----:|
| service_memory | 80 | 38.1% | — |
| task_state | 71 | 33.8% | 28-34% |
| repo_memory | 35 | 16.7% | 16-22% |
| project_memory | 15 | 7.1% | 10-16% ⚠ |
| user_profile | 9 | 4.3% | 5-10% ⚠ |
| **Total** | **210** | | |

**Honest tradeoffs acknowledged:**
- **project_memory at 7.1%** (range: 10-16%). Dropped by 10 units (8 rollbacks + 2 borderline changes). These 10 units all contain single-service behavior with an artificial "The {project} requires..." prefix. Keeping them as project_memory would sacrifice label quality for distribution. Project_memory now only represents genuinely project-wide scope/cross-service policy.
- **user_profile at 4.3%** (range: 5-8%). Dropped 2 units (1 false user_profile fix + 1 notes sync). These units did not represent genuine user preferences. No additional real user_profile cases were identified for replacement at this time. Acceptable for gold evaluation.

## 9. Leakage Before/After

| Check | Before (Draft) | After (Corrected) |
|-------|:--------------:|:-----------------:|
| Train↔Gold hard blockers | 0 | 0 |
| Train↔Gold warnings | 1 (phone pattern 0.533) | 0 |
| Dev↔Gold hard blockers | 0 | 0 |
| Dev↔Gold warnings | 0 | 0 |

The previous phone number pattern warning (score 0.533) was resolved by the Fix Group D change (+1-555-0198 → +1-555-0147).

## 10. Validation Results

| Check | Status |
|-------|:------:|
| Corrected gold exactly 100 rows | ✅ |
| Corrected gold_core exactly 70 rows | ✅ |
| Corrected gold_hard exactly 30 rows | ✅ |
| Corrected SFT exactly 100 rows | ✅ |
| validate_jsonl_file valid | ✅ |
| Every gold.dsl parses | ✅ |
| Parsed canonical == structured gold | ✅ |
| Every unit exactly once STORE/SKIP | ✅ |
| No invalid READ/STORE/SKIP IDs | ✅ |
| No invalid targets | ✅ |
| Sensitive-looking units never STORE | ✅ |
| Train↔corrected_gold: 0 hard blockers | ✅ |
| Dev↔corrected_gold: 0 hard blockers | ✅ |
| SFT assistant == gold.dsl | ✅ |
| No markdown/JSON in assistant | ✅ |
| Unittest passes (77/77) | ✅ |

## 11. Remaining Limitations

1. **project_memory under target:** 7.1% vs 10-16% range. This is an honest tradeoff — the removed units were distribution-driven artifacts. Do not add weak project_memory labels to hit distribution.
2. **user_profile under target:** 4.3% vs 5-8% range. Low-risk. No easy natural opportunities for additional genuine user_profile cases.
3. **service_memory over target:** 38.1% vs 28-34% range. This reflects the rollback of artificial project_memory labels. Within acceptable bounds.
4. **Gold still not locked:** Requires final human adjudication per GOLD_REVIEW_GUIDE.
5. **Single-adjudicator limitation:** This project is a single-human research effort with LLM advisory input, as documented.

## 12. Readiness for Final Review / Lock

**Status: Corrected gold draft is ready for final adjudication review.**

All blocker findings from the Opus review have been addressed. Distribution tradeoffs are honest and documented. The corrected gold correctly represents the V05_LABEL_POLICY with semantically valid labels.

**Next step:** Final human adjudication (two-pass self-review) per V05_GOLD_REVIEW_GUIDE Section 5.2, followed by gold locking.

**This is NOT locked gold.** Do not train, do not use for model selection.

---

*End of V0.5 Gold Opus Review Fixes Report.*
