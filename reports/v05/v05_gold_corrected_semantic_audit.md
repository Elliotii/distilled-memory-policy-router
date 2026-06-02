# V0.5 Gold Corrected Semantic Audit

**Date:** 2026-06-02  
**Context:** 5.3-D — semantic audit of corrected gold draft  
**Status:** Corrected draft — NOT locked  

---

## 1. Audit Summary

| Category | Status |
|----------|:------:|
| Per-case audit (100 cases) | ✅ Complete |
| All 12 modified cases reviewed in detail | ✅ |
| All 30 gold_hard cases reviewed | ✅ (1 replaced) |
| Target-boundary audit | ✅ |
| project_memory audit after cleanup | ✅ |
| user_profile audit after cleanup | ✅ |
| Sensitive/private audit | ✅ Zero STORE errors |
| Leakage/template audit | ✅ Distinct cases |

## 2. Per-Case Audit Table

| Partition | Cases | Risk Level | Review Status |
|-----------|:-----:|:----------:|:-------------:|
| gold_core (unmodified) | 45 | Low | Structural + DSL ✅ |
| gold_core (post-processed, kept) | 17 | Low-Medium | Notes synced ✅ |
| gold_core (post-processed, rolled back) | 8 | — | Rolled back to svc ✅ |
| gold_hard (unmodified) | 28 | Medium-High | Full detail reviewed ✅ |
| gold_hard (replaced) | 2 | — | 1 replaced (0013), 1 label fixed (0014) ✅ |
| **Total** | **100** | | |

## 3. All Modified Cases — Detailed Review

### 3.1 Group A: svc→proj Rollbacks (8 cases)

All 8 cases had unit u2 artificially reframed as project_memory via "The {project} project requires..." prefix. In each case, the actual semantic content describes single-service durable behavior:

| Case | Unit u2 Content | Final Label | Correct? |
|------|----------------|-------------|:--------:|
| v05_gold_core_0044 | SSL cert alert escalation (7-day threshold) | service_memory | ✅ Uptime-checker behavior |
| v05_gold_core_0047 | Flaky test auto-reporting to team channel | service_memory | ✅ Test-runner behavior |
| v05_gold_core_0050 | Correlated alert root-cause-first ordering | service_memory | ✅ Alert-dispatcher behavior |
| v05_gold_core_0051 | Proactive customer delay notification | service_memory | ✅ Tracking-notifier behavior |
| v05_gold_core_0056 | Response validation failure logging (1KB truncation) | service_memory | ✅ Uptime-checker behavior |
| v05_gold_core_0057 | EV charging time constraint (30 min per 200 miles) | service_memory | ✅ Route-optimizer behavior |
| v05_gold_core_0058 | Custom policy JSON schema validation before loading | service_memory | ✅ Policy-validator behavior |
| v05_gold_core_0066 | Language-aware search: prioritize query language | service_memory | ✅ Search-indexer behavior |

**Verdict:** All 8 rollbacks correct. None of these units describe project-wide scope or cross-service policy.

### 3.2 Group B: False user_profile (1 case)

| Case | Unit | Old | New | Reason |
|------|------|-----|-----|--------|
| v05_gold_core_0021 | u1 | user_profile | service_memory | "primary-language content searchable within 5 minutes" is indexing SLA, not user preference |

**Verdict:** Correct. This is a search-indexer SLA requirement, not a cross-project user preference.

### 3.3 Group C: Work Email → SKIP (1 case)

| Case | Unit | Old | New | Reason |
|------|------|-----|-----|--------|
| v05_gold_hard_0014 | u2 | repo_memory | SKIP | Email addresses are personal contact info, must SKIP per V05_LABEL_POLICY |

**Impact on gold_hard_0014:** Previously had 3 STORE units (user_profile, repo_memory, task_state). Now has 2 STORE + 1 SKIP. The user_profile_vs_sensitive hard case now correctly models the boundary: u1 (safe preference) vs u2 (personal email → SKIP).

**Verdict:** Correct.

### 3.4 Group D: Phone Number Collision (1 case)

| Case | Unit | Change |
|------|------|--------|
| v05_gold_hard_0015 | u3 | +1-555-0198 → +1-555-0147 |

**Verdict:** Resolves train↔gold sensitive-pattern overlap. Phone number still synthetic and correctly SKIPped.

### 3.5 Group E: Replaced Hard Case (1 case)

**Before (v05_gold_hard_0013 old):** Clean three-way repo_vs_service: u1 = service_memory (WHAT), u2 = repo_memory (WHERE config), u3 = repo_memory (WHERE code). Too easy — no genuine ambiguity.

**After (v05_gold_hard_0013 new):** Genuine repo_vs_service boundary:
- u1: Dedup behavior (WHAT) → service_memory
- u2: Config path WITH field name hints (window_minutes, event_key_fields, discard_policy) → repo_memory, but field names create pull toward service_memory
- u3: Source/test paths referencing dedup logic → repo_memory, but "dedup logic" keyword creates pull toward service_memory

**Hard because:** The model must decide whether config field descriptions and source-code behavioral references are sufficient to classify units as service_memory. The correct answer is repo_memory (WHERE), but the behavioral keywords create genuine ambiguity.

**Verdict:** Significantly harder than the old case. Correctly tests the boundary.

## 4. All Gold Hard Cases — Detailed Review

### 4.1 service_vs_task_state (5 cases)

| Case | Verdict | Notes |
|------|:-------:|-------|
| v05_gold_hard_0001 | ✅ | "should run" ambiguity well modeled. Detailed spec → svc |
| v05_gold_hard_0002 | ✅ | SLA guarantee vs current perf observation boundary |
| v05_gold_hard_0003 | ✅ | "must cross-reference" vs "need to integrate" framing |
| v05_gold_hard_0004 | ✅ | "should route" with detail → svc. Limitation → task |
| v05_gold_hard_0005 | ✅ | Durable constraint vs current version limitation |

### 4.2 project_memory_vs_task_state (4 cases)

| Case | Verdict | Notes |
|------|:-------:|-------|
| v05_gold_hard_0006 | ✅ | Project retention policy vs current implementation |
| v05_gold_hard_0007 | ✅ | Permanent scope exclusion vs version-scoped fields |
| v05_gold_hard_0008 | ✅ | "for current fiscal year" temporal qualifier — genuine tension |
| v05_gold_hard_0009 | ✅ | SLA vs current-month measurement |

### 4.3 repo_vs_service (4 cases)

| Case | Verdict | Notes |
|------|:-------:|-------|
| v05_gold_hard_0010 | ✅ | Config path + priority field description → genuine ambiguity |
| v05_gold_hard_0011 | ✅ | Cleaner case, but useful as calibration point |
| v05_gold_hard_0012 | ✅ | Config path + processing setting hints |
| v05_gold_hard_0013 | ✅ [NEW] | Config path + field names, source path + dedup references |

### 4.4 user_profile vs sensitive/private (4 cases)

| Case | Verdict | Notes |
|------|:-------:|-------|
| v05_gold_hard_0014 | ✅ [FIXED] | Work email now correctly SKIPped |
| v05_gold_hard_0015 | ✅ [FIXED] | Phone number collision resolved |
| v05_gold_hard_0016 | ✅ | API token correctly SKIPped |
| v05_gold_hard_0017 | ✅ | Driver's license correctly SKIPped |

### 4.5 related_but_useless (4 cases)

| Case | Verdict |
|------|:-------:|
| v05_gold_hard_0018 | ✅ All correctly NOT READ |
| v05_gold_hard_0019 | ✅ All correctly NOT READ |
| v05_gold_hard_0020 | ✅ All correctly NOT READ |
| v05_gold_hard_0021 | ✅ All correctly NOT READ |

### 4.6 stale_memory (3 cases)

| Case | Verdict |
|------|:-------:|
| v05_gold_hard_0022 | ✅ Stale memories correctly NOT READ |
| v05_gold_hard_0023 | ✅ Stale memories correctly NOT READ |
| v05_gold_hard_0024 | ✅ Stale memories correctly NOT READ |

### 4.7 sensitive_boundary (3 cases)

| Case | Verdict | Sensitive Content |
|------|:-------:|-------------------|
| v05_gold_hard_0025 | ✅ | SSN → SKIP |
| v05_gold_hard_0026 | ✅ | Credit card → SKIP |
| v05_gold_hard_0027 | ✅ | API key value → SKIP |

### 4.8 read_selectivity / over-read trap (3 cases)

| Case | Verdict | Correct READ |
|------|:-------:|-------------|
| v05_gold_hard_0028 | ✅ | m1, m2 only (source coverage, not storage) |
| v05_gold_hard_0029 | ✅ | m1 only (execution ORDER, not parallelism/storage/config) |
| v05_gold_hard_0030 | ✅ | m1 only (indexing LATENCY, not architecture/queries/features) |

## 5. Target-Boundary Audit

| Boundary | Cases | Quality |
|----------|:-----:|:-------:|
| service_vs_task_state | 6 (+1 core) | Well covered, genuine ambiguity in "should" and "currently" framing |
| project_memory_vs_task_state | 4 | Good temporal-qualifier tension in hard_0008 |
| repo_vs_service | 4 | Improved with new hard_0013 replacement |
| user_profile vs sensitive | 4 | Improved with hard_0014 email fix |
| Read selectivity | 3 | Strong — all 4-memory traps correctly resolved |
| Stale memory | 3 | Clear — old versions correctly not READ |
| Sensitive boundary | 3 | Zero errors — SSN, credit card, API key all SKIPped |
| related_but_useless | 16 (including core) | All correctly handled |

## 6. Project Memory Audit After Cleanup

After 10 rollbacks (8 group A + 2 borderline), remaining 15 project_memory cases:

| Case | Unit | Content | Verdict |
|------|------|---------|:-------:|
| v05_gold_core_0028 | u1 | No crypto transactions | ✅ Genuine project scope exclusion |
| v05_gold_core_0031 | u1 | Cross-service AES-256/KMS encryption policy | ✅ Genuine cross-service policy |
| v05_gold_core_0033 | u1 | Never index unpublished content | ✅ Genuine project-level rule |
| v05_gold_core_0035 | u1 | Server-side only, no client-side | ✅ Genuine project scope exclusion |
| v05_gold_core_0039 | u1 | 3-resolution adaptive streaming | ✅ Genuine project-level quality requirement |
| v05_gold_core_0041 | u1 | Canary deployments 5%/15min for all services | ✅ Cross-service deployment policy |
| v05_gold_core_0042 | u1 | Faceted search across all search surfaces | ✅ Cross-surface project requirement |
| v05_gold_core_0045 | u2 | Manual dispatcher review if +60min weather | ✅ Project-level operational policy |
| v05_gold_core_0048 | u2 | Human review <90% caption confidence for WCAG | ✅ Project-level accessibility policy |
| v05_gold_core_0053 | u2 | GPG verification before any env deployment | ✅ Cross-environment deployment policy |
| v05_gold_core_0060 | u2 | Watermark free-tier only, pro/enterprise unwatermarked | ✅ Cross-tier content policy |
| v05_gold_hard_0006 | u1 | 90-day artifact retention | ✅ Project-level policy |
| v05_gold_hard_0007 | u1 | No user comment indexing | ✅ Permanent scope exclusion |
| v05_gold_hard_0008 | u1 | US-only tax (current fiscal year) | ⚠ Temporal qualifier — borderline but kept |
| v05_gold_hard_0009 | u1 | 99.9% uptime SLA | ✅ Project-level SLA |

**Verdict:** 14/15 are clearly correct. v05_gold_hard_0008 u1 has a temporal qualifier ("for the current fiscal year") that makes it borderline — this was flagged in the original hard case notes and serves as a genuine project_memory_vs_task_state stress test. **Kept as-is.**

## 7. User Profile Audit After Cleanup

After fix group B, remaining 9 user_profile cases:

| Case | Unit | Content | Verdict |
|------|------|---------|:-------:|
| v05_gold_core_0019 | u3 | Group compliance results by severity | ✅ Stable display preference |
| v05_gold_core_0027 | u3 | Prefer WebP images, JPEG fallback | ✅ Stable format preference |
| v05_gold_core_0030 | u1 | Color-coded traffic overlay, not numeric | ✅ Stable display preference |
| v05_gold_core_0036 | u1 | Daily digest email, not individual alerts | ✅ Stable notification preference |
| v05_gold_core_0038 | u1 | Test failures grouped by package, slowest first | ✅ Stable reporting preference |
| v05_gold_hard_0014 | u1 | Reports sorted by discrepancy desc | ✅ Stable sorting preference |
| v05_gold_hard_0015 | u1 | Non-critical alerts as daily Slack digest | ✅ Stable notification preference |
| v05_gold_hard_0016 | u1 | Search snippet, not first 100 chars | ✅ Stable display preference |
| v05_gold_hard_0017 | u1 | Satellite view with traffic overlay | ✅ Stable display preference |

**Verdict:** All 9 are genuine, stable, non-sensitive user preferences.

## 8. Sensitive/Private Audit

10 cases with sensitive content — all correctly SKIPped.

| Case | Sensitive Content | Verdict |
|------|-------------------|:-------:|
| v05_gold_hard_0014 | Work email (finops.lead@company.com) | ✅ SKIP |
| v05_gold_hard_0015 | Personal email + phone +1-555-0147 | ✅ SKIP |
| v05_gold_hard_0016 | API token cms-tok-9876-fedc | ✅ SKIP |
| v05_gold_hard_0017 | Driver's license DL-9876-5432 | ✅ SKIP |
| v05_gold_hard_0025 | SSN 123-45-6789 | ✅ SKIP |
| v05_gold_hard_0026 | Credit card 5500-0000-0000-0004 | ✅ SKIP |
| v05_gold_hard_0027 | API key pd-test-1234-abcd-5678-efgh | ✅ SKIP |
| v05_gold_core_0017 | Personal Slack handle @devops-lead | ✅ SKIP |
| v05_gold_core_0030 | Home address 789 Pine Street | ✅ SKIP |
| v05_gold_core_0038 | CI token ci-tok-1234-abcd | ✅ SKIP |

**Zero sensitive STORE errors.** Zero false-positive SKIPs.

## 9. Leakage / Template Audit

| Check | Result |
|-------|:------:|
| Train↔corrected gold: hard blockers | 0 |
| Train↔corrected gold: warnings | 0 |
| Dev↔corrected gold: hard blockers | 0 |
| Dev↔corrected gold: warnings | 0 |
| All cases text-distinct | ✅ Six diverse project domains |
| No mechanical template repetition | ✅ |

## 10. Readiness Judgment

**The corrected gold draft is semantically sound and ready for final human adjudication.**

All Opus review blockers have been addressed:
1. ✅ 8 distribution-driven svc→proj changes rolled back
2. ✅ Notes synchronized for all 23 post-processing cases
3. ✅ Work email correctly SKIPped
4. ✅ Too-easy hard_0013 replaced with genuine boundary case
5. ✅ Phone number collision resolved
6. ✅ Report counts corrected

## 11. Final Metadata Cleanup (Context 5.3-D2)

After Opus lightweight final review:
- 24 damaged notes regenerated (uu1 typo fixed, truncation removed)
- 10 service_memory u2 units rewritten from project-style to service-style wording
- 1 fixes report typo corrected

No label changes. No DSL changes. All validations pass.

Remaining distribution tradeoffs (project_memory 7.1%, user_profile 4.3%) are honest and documented — no artificial labels added to hit targets.

**Gold is NOT locked.** Final two-pass self-review adjudication and lock file creation are the next steps.

---

*End of V0.5 Gold Corrected Semantic Audit.*
