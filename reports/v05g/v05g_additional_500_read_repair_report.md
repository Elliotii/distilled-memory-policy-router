# v05g Additional 500 READ Semantic Recoverability Repair Report

**Date:** 2026-06-05  
**Auditor:** Opus 4.8 (defect identification) + Automated repair  
**Script:** `src/v05g/repair_v05g_additional_500.py`

## Defect Summary (Opus 4.8)

1. READ labels among non-stale relevant memories were arbitrary / not recoverable from prompt-visible content.
2. STORE/SKIP/target decisions were 100% recoverable from the first three words of each unit (see prefix shortcut repair report for fix).

## Original Defect Analysis

In the v05g additional 500 (pre-repair), READ labels were determined entirely by template shape, not by visible semantics:

| Shape | READ behavior (pre-repair) |
|-------|---------------------------|
| `read_only` | ALL non-stale memories read |
| `store_skip_only` | NO memories read (even clearly relevant ones) |
| `read_store_joint` | First 2-3 memories always read |

This created unrecoverable READ labels because the same candidate memory in a `read_only` case was read, while in a `store_skip_only` case it was not — with no visible semantic difference to justify the decision.

## Repair Implementation

### Gold READ Rule

A memory is READ iff:
- It is **non-stale** AND
- Its text **visibly mentions the current runtime service or repo** (visible semantic relevance)

A memory is NOT READ if:
- It is **stale** (deprecated/archived/historical — visible via NOTE markers)
- It is a **cross-service distractor** (mentions a different service from the runtime, visible in the text)
- It is a **cross-domain distractor** (mentions a different project from the runtime, visible in the text)
- It is a **user_profile** memory in a case with no user-profile store units (no user preference context)

### Memory Design Changes

| Memory type | Purpose | READ? |
|-------------|---------|-------|
| In-domain service_memory | Mentions runtime service name | YES |
| In-domain repo_memory | Mentions runtime repo or service name | YES |
| User_profile (with user stores) | Preferences relevant to current task | YES |
| Cross-service distractor | Different service, same project | NO (visible reason) |
| Cross-domain distractor | Different project entirely | NO (visible reason) |
| Stale memory | Clearly marked as deprecated | NO (visible reason) |
| User_profile (no user stores) | No user preference context | NO (visible reason) |

### Memory Mode Control

To maintain distribution balance, a `memory_mode` parameter controls whether in-domain relevant memories are included:

| Case shape | `no_relevant` fraction | Effect |
|------------|----------------------|--------|
| `store_skip_only` | 65% | True STORE/SKIP-only (no reads possible) |
| `read_store_joint` | 30% | True STORE/SKIP-only when no relevant memories |
| `read_only` | 0% | Always has relevant memories to read |

Cases with `no_relevant` mode contain only stale + cross-domain distractor memories. This is semantically valid — the user's task has candidate memories available, but none are relevant to the current runtime context.

## Repair Results

### READ Rates by Target (Additional 500)

| Target | Total | Read | Not Read | Rate |
|--------|-------|------|-----------|------|
| service_memory | 1,043 | 310 | 733 | 29.7% |
| repo_memory | 310 | 310 | 0 | 100% |
| project_memory | 405 | 0 | 405 | 0% |
| user_profile | 82 | 82 | 0 | 100% |

- service_memory: 310 in-domain relevant (all READ) + 233 stale (all NOT READ) + 500 cross-service distractor (all NOT READ)
- repo_memory: 310 in-domain relevant (all READ)
- project_memory: 405 cross-domain distractor (all NOT READ)
- user_profile: 82 memories, all READ when case has user-profile store units; 0 user_profile memories in cases without user stores

### Hard Gates

| Gate | Result |
|------|--------|
| Stale reads | **0** ✅ |
| Distractor/off-topic reads | **0** ✅ |
| Non-stale in-domain not-read without visible distractor reason | **0** ✅ |
| Identical memory text READ conflict | **0** ✅ |
| Normalized memory skeleton READ conflict | **0** ✅ |

### Semantic Recoverability

Every READ decision is now **recoverable from the prompt-visible context**:

- **READ**: Memory text contains the runtime service/repo name → visible relevance
- **NOT READ (stale)**: Memory text starts with "NOTE: Archived/Deprecated/Historical" → visible staleness
- **NOT READ (distractor)**: Memory text contains a different service/project name → visible irrelevance
- **NOT READ (user_profile)**: No user units in the case → user preferences not needed

### Example: Relevant READ

```
Runtime: project=energy-monitoring, service=meter-collector
m1 [service_memory]: The meter-collector uses Prometheus for peak demand forecasting... => READ
m2 [repo_memory]: Run make bench-svc in the powergrid repo to run integration tests for the meter-collector... => READ
m3 [service_memory]: The attrition-predictor runs outage detection checks every 5 minutes... => NOTREAD (different service)
```

### Example: Stale / Distractor-Only Case

```
Runtime: project=hr-analytics, service=attrition-predictor
m1 [project_memory]: The energy-monitoring project requires bi-weekly security reviews... => NOTREAD (different project)
m2 [service_memory]: NOTE: This procedure was deprecated when we moved from Bitbucket... => NOTREAD (stale)
m3 [service_memory]: The topology-mapper guarantees 99.5% uptime with max response latency... => NOTREAD (different service)
```

All 3 memories are non-stale or clearly stale, and each NOT READ decision has a visible reason.

## Conclusion

- READ labels are now fully determined by visible semantics.
- 0 stale reads.
- 0 distractor reads.
- All non-stale not-read memories have visible distractor/stale reasons.
- No hidden relevance labels required.
- Combined 1000 shape and target distributions remain within spec (see distribution report).
