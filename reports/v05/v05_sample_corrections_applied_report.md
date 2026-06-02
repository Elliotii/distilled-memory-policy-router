# V0.5 Sample Corrections Applied Report

Date: 2026-06-01  
Context: 5.0-D — apply approved sample corrections + regenerate SFT messages  
Status: Corrections applied; sample set re-validated

## 1. Scope

Apply the 6 human decisions from Context 5.0-C review to the v0.5 sample case set, regenerate SFT messages, re-run all validations, and document the changes.

## 2. Human Decisions Applied

| # | Case ID | Decision | Action |
| --- | --- | --- | --- |
| 1 | v05_sample_0014 | Remove — too ambiguous; replace with cleaner case | Removed; replaced by v05_sample_0021 |
| 2 | v05_sample_0018 | Keep — u2 remains project_memory | No change |
| 3 | v05_sample_0015 | Keep — u2 remains project_memory | No change |
| 4 | v05_sample_0006 | Keep u1 as project_memory; clarify notes | Notes updated |
| 5 | v05_sample_0009 | Modify u2 from service_memory to task_state | DSL + store changed |
| 6 | v05_sample_0020 | Keep — u3 remains SKIP | No change |

## 3. Exact Changes Made

### Change 1: v05_sample_0014 Removed

- Removed case v05_sample_0014 entirely from `SAMPLE_CASES` list in `src/v05/render_sft_messages.py`.
- Added comment: `# v05_sample_0014 REMOVED per human review Decision 1: too ambiguous for training.`
- Rationale: Both service_memory/task_state interpretations were defensible; too ambiguous for clean training signal.

### Change 2: v05_sample_0021 Added (replacement)

- New case v05_sample_0021 inserted at the position previously occupied by v05_sample_0014.
- See §4 below for full case details.

### Change 3: v05_sample_0009 u2 target changed

Before:
```
STORE service_memory u2
```
After:
```
STORE task_state u2
```
Updated DSL: `READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE`

Updated notes to clarify: u2 is a current implementation limitation, not a permanent design invariant.

### Change 4: v05_sample_0006 notes updated

Added permanence clarification to notes:
> Assumes synthetic-data-only is a permanent project safety/scope decision, not a temporary pilot constraint.

No DSL or gold labels changed.

### Changes 5-6: v05_sample_0018, v05_sample_0015, v05_sample_0020

No changes. Labels kept as-is per human decisions.

## 4. Replacement Case Summary — v05_sample_0021

**Case ID:** v05_sample_0021
**Project:** mobile-field / field-app
**Service:** notification
**Task:** add push notification retry logic

**Candidate Memories:**
- m1 [service_memory]: notification service delivers via Firebase Cloud Messaging with 30s timeout
- m2 [repo_memory]: config lives in config/notification.yaml

**Current Units:**
- u1: "The notification service must deduplicate messages by notification_id within a 5-minute window to prevent double-delivery." → **service_memory**
- u2: "Integrate the notification retry into the existing sync retry wrapper that already handles 429 responses." → **task_state**
- u3: "Write the FCM credential setup guide in docs/notification/fcm_setup.md." → **repo_memory**

**Gold DSL:** `READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE`

**Why this is a clean boundary case:**
- u1 defines WHAT the service does (durable deduplication behavior) — classically service_memory.
- u2 defines HOW to implement retry now (current integration step) — classically task_state.
- u3 defines WHERE docs go (repo path convention) — classically repo_memory.
- No ambiguous wording like "currently should."
- Clear, durable vs. temporal distinction.

**Leakage checks:** No overlap with subset50, few-shot examples, or existing v05 sample texts.

## 5. Before/After Case IDs

| Before (20) | After (20) |
| --- | --- |
| v05_sample_0001–0020 | v05_sample_0001–0013, 0015–0021 |
| v05_sample_0014 included | v05_sample_0014 **removed** |
| — | v05_sample_0021 **added** |

IDs kept: 0001–0013, 0015–0020 (19 cases unchanged in ID and most labels).
IDs changed: 0014 → 0021 (1 replacement).

## 6. Before/After STORE Target Counts

| Target | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `service_memory` | 14 | 13 | −1 |
| `task_state` | 10 | 11 | +1 |
| `repo_memory` | 9 | 9 | 0 |
| `project_memory` | 3 | 3 | 0 |
| `user_profile` | 2 | 2 | 0 |
| **Total STORE** | **38** | **38** | **0** |

The net effect: one service_memory → task_state change (v05_sample_0009 u2), balanced by the replacement case adding one service_memory (v05_sample_0021 u1) and one task_state (v05_sample_0021 u2).

## 7. Before/After Shape Distribution

| Shape | Before | After | Delta |
| --- | ---: | ---: | --- |
| READ-only | 3 | 3 | 0 |
| STORE/SKIP-only | 7 | 6 | −1 |
| READ + STORE joint | 10 | 11 | +1 |

The removed case (v05_sample_0014) was STORE/SKIP-only. The replacement case (v05_sample_0021) is READ + STORE joint.

## 8. Validation Results

| Check | Result |
| --- | --- |
| Sample case count = 20 | ✓ |
| SFT messages count = 20 | ✓ |
| v05_sample_0014 absent | ✓ |
| v05_sample_0021 present | ✓ |
| `validate_jsonl_file` valid | ✓ (20 records, 0 errors) |
| `parse_policy_dsl` succeeds for all gold.dsl | ✓ (20/20) |
| Canonical parse output matches structured gold | ✓ (20/20) |
| Every current unit exactly once STORE or SKIP | ✓ (52/52) |
| No invalid targets | ✓ |
| No sensitive units in STORE | ✓ (0 violations) |
| No subset50 overlap | ✓ |
| No few-shot example overlap | ✓ |
| SFT assistant == gold.dsl | ✓ (20/20) |
| No markdown / JSON in assistant content | ✓ |
| `unittest discover` | ✓ (49/49 OK) |
| `py_compile` on generation script | ✓ |

## 9. Remaining Human Review Points

1. **v05_sample_0018:** Decision to keep u2 as project_memory is confirmed. However, the distinction between "design principle" (project_memory) and "implementation plan" (task_state) remains philosophically subtle. Reviewer should verify this distinction is teachable to a 4B model.

2. **v05_sample_0006:** Notes now clarify permanence assumption. If "synthetic data only" later proves to be temporary, this case should be revisited.

3. **v05_sample_0021:** New replacement case uses mobile-field/field-app/notification domain. Reviewer should confirm the service_memory vs task_state distinction reads as clearly as intended.

4. **v05_sample_0020 u3:** Confirmed as SKIP, not user_profile. This is the correct call per reviewer decision, but it's worth noting that in a different training objective, "laptop runs Ubuntu" could be user_profile.

## 10. Whether Sample Set Is Ready for 50-100 Case Scale

**Yes, with caveats.**

The 20-case sample set is now structurally validated, semantically reviewed, and corrected. All 6 human decisions have been applied. The set provides coverage of all 3 shapes, all 5 targets, and all major boundary types.

**Before scaling to 50-100 cases:**
- Reviewer should skim v05_sample_0021 for semantic quality
- The generation pipeline (case → SFT message) is working correctly
- Leakage checks are in place
- The corrected set can serve as a style/template reference for expanded generation

## 11. Risks / Limitations

1. **20 cases is still not training data.** This is a validated template set only.
2. **Agent-generated cases:** Even after human correction of 1 case, 19 cases remain agent-generated and may contain subtle labeling biases.
3. **Template repetition:** Three project domains (memory-router, mobile-field, data-platform) recur across cases. Expanded set should add variety.
4. **project_memory count = 3:** This is at minimum. Scaling should increase project_memory representation.
5. **No multi-turn context:** All cases are single-turn. If multi-turn is a future goal, training data should eventually include it.

## 12. Recommended Next Step

**Proceed to Context 5.0-E (or equivalent): Scale to 50-100 case batch.**

Post-conditions for next context:
1. Use the corrected 20-case set as a template/style reference
2. Generate 30-80 additional cases covering the same target distribution requirements
3. Maintain all leakage checks against subset50, few-shot examples, and the existing 20
4. Re-run all validations on the expanded set
5. Prepare for train/dev/gold split planning

Do NOT:
- Start training
- Lock gold
- Generate full 500-1000 train set
- Connect to any API or model
