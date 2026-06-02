# V0.5 Batch50 Corrections Applied Report

Date: 2026-06-01  
Context: 5.0-F Step A — apply batch50 decisions  
Status: Corrections applied; batch50 re-validated

## 1. Scope

Apply the 3 human decisions from Context 5.0-E2 review to the v0.5 batch50 cases, regenerate SFT messages, and re-validate. This is Step A of the batch100 scale process.

## 2. Human Decisions Applied

| # | Case ID | Decision | Action |
| --- | --- | --- | --- |
| 1 | v05_batch50_0007 | u3 → task_state (Option B) | Modified |
| 2 | v05_batch50_0017 | Keep (not redundant) | No change |
| 3 | v05_batch50_0024 | u1 → service_memory (Option B) | Modified |

## 3. Exact Changes

### v05_batch50_0007

**Before:**
```
STORE service_memory u1
STORE task_state u2
STORE project_memory u3
```
DSL: `READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE project_memory u3\nSKIP NONE`

**After:**
```
STORE service_memory u1
STORE task_state u2
STORE task_state u3
```
DSL: `READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE task_state u3\nSKIP NONE`

**Notes updated:** u3 is now described as "version-scoped, model-specific training plan → task_state, not a permanent project decision."

### v05_batch50_0024

**Before:**
```
STORE project_memory u1
STORE project_memory u2
STORE task_state u3
```
DSL: `READ NONE\nSTORE project_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`

**After:**
```
STORE service_memory u1
STORE project_memory u2
STORE task_state u3
```
DSL: `READ NONE\nSTORE service_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`

**Notes updated:** u1 is now "export-specific PII rule → service_memory (the text names 'The export service')" and u2 is "explicitly cross-service rule → project_memory ('All data-platform services')." Creates a clean text-driven contrast.

### v05_batch50_0017

No changes. Confirmed not redundant with v05_sample_0006.

## 4. Before/After Target Counts (batch50)

| Target | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `service_memory` | 34 | 35 | +1 |
| `task_state` | 32 | 33 | +1 |
| `repo_memory` | 21 | 21 | 0 |
| `project_memory` | 9 | 8 | −1 |
| `user_profile` | 4 | 4 | 0 |

## 5. Validation Results (corrected batch50)

| Check | Result |
| --- | --- |
| 50 cases | ✓ |
| 50 SFT messages | ✓ |
| `validate_jsonl_file` valid | ✓ |
| All gold.dsl parse OK | ✓ |
| Canonical == structured gold | ✓ (50/50) |
| SFT assistant == gold.dsl | ✓ (50/50) |
| No markdown/JSON in assistant | ✓ |
| No leakage | ✓ |

## 6. Remaining Human Review Points

None. All 3 flagged cases from P5.7-E2 have been resolved per human decisions.

## 7. Readiness for Batch100 Scaling

**Ready.** The corrected batch50 serves as a clean seed for the batch100 expansion. Key improvements from corrections:
- v05_batch50_0007 no longer teaches version-scoped configs as project_memory
- v05_batch50_0024 now teaches the text-driven contrast: service-named rules → service_memory, cross-service rules → project_memory
