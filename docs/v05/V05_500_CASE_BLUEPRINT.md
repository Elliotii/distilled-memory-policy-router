# V0.5 500-Case Blueprint

Version: v0.5  
Date: 2026-06-01  
Status: Blueprint only; NO data generated yet

## 1. Scope

This blueprint defines the plan for generating 500 training-style cases for v0.5 LoRA/SFT training. It does NOT generate data. It specifies distribution targets, domain plans, quality rules, and staging gates based on lessons learned from the batch100 audit.

**This blueprint must be reviewed and approved before any case generation begins.**

## 2. Proposed Split

Given current project risk (agent-generated labels, target-boundary ambiguity at scale), recommend a staged approach:

| Stage | Cases | Purpose | Locked? |
| --- | ---: | --- | --- |
| **Batch200** | 200 | Draft training pool — audit, correct, learn | No |
| **Batch500** | 500 | Training pool — full distribution, first training candidate | No |
| **Dev** | 80 | Hyperparameter tuning, early stopping | After batch500 audit |
| **Gold** | 100 | Final evaluation | After dev audit, locked |

**Staged rationale:** Do not jump from 100 to 500 directly. First generate 200 (batch200), audit, correct, then scale the validated pattern to 500. Dev and gold are created only after the training pool passes audit.

## 3. Target Distribution

Based on corrected batch100 (svc=79, task=60) and audit lessons:

| Target | Batch100 Actual | Batch500 Target | % Range |
| --- | ---: | ---: | ---: |
| `service_memory` | 79 (38.7%) | 150-170 | 30-34% |
| `task_state` | 60 (29.4%) | 150-170 | 30-34% |
| `repo_memory` | 33 (16.2%) | 80-100 | 16-20% |
| `project_memory` | 18 (8.8%) | 50-70 | 10-14% |
| `user_profile` | 14 (6.9%) | 25-40 | 5-8% |
| **Total STORE** | **204** | **~500** | — |

**Service/Task Rule:** service_memory should not exceed task_state by more than 10 percentage points. The target range allows for some domain-natural variance but prevents collapse.

## 4. Shape Distribution

| Shape | Batch100 | Batch500 Target |
| --- | ---: | ---: |
| READ-only | 18% | 15-20% |
| STORE/SKIP-only | 33% | 30-35% |
| READ + STORE joint | 49% | 45-50% |

## 5. Tag Coverage Requirements

Every 100 cases must include at minimum:

| Tag | Min per 100 | Notes |
| --- | ---: | --- |
| `stale_memory` | 20 | Stale memories correctly not read |
| `related_but_useless` | 15 | Related but not useful memories |
| `target_boundary` | 20 | Cases where target choice is subtle |
| `sensitive_boundary` | 15 | Sensitive units all correctly SKIPped |
| `user_profile_boundary` | 10 | User pref vs sensitive distinction |
| `project_vs_repo` | 15 | project_memory vs repo_memory boundary |
| `repo_vs_service` | 12 | repo_memory vs service_memory boundary |
| `service_vs_task_state` | 12 | service_memory vs task_state boundary |
| `repo_convention` | 15 | Repo paths, commands, test conventions |
| `service_invariant` | 30 | Durable service behaviors |
| `task_progress` | 25 | Current progress, next steps, blockers |
| `temporary_request` | 15 | One-off requests, transient queries |

## 6. Domain Plan

### Existing Domains (from batch100)

| Domain | Batch100 Cases | Batch500 Target |
| --- | ---: | ---: |
| memory-router | 19 | 60-80 |
| data-platform | 16 | 60-80 |
| mobile-field | 15 | 50-70 |
| docs-assistant | 12 | 50-60 |
| finance-dashboard | 12 | 50-60 |
| travel-planner | 10 | 40-50 |
| education-platform | 8 | 40-50 |
| game-studio | 8 | 40-50 |

### New Domains (suggested, 3-5)

| Domain | Suggested Cases | Key Value |
| --- | ---: | --- |
| customer-support | 40-60 | Sensitive boundary (customer data), task progress |
| ecommerce-platform | 40-60 | Repo convention (catalog, orders), service invariants |
| analytics-dashboard | 30-50 | Service memory (query engines), project scope |
| learning-assistant | 30-50 | User_profile (learning preferences), service behavior |
| workflow-automation | 30-50 | Task state (pipeline steps), repo convention |

**All domains must remain synthetic.** No real user data, no real company names, no real API endpoints.

## 7. Label Policy

All cases must follow `docs/v05/V05_LABEL_POLICY.md`. Key rules:

1. "Add/Implement/Build..." phrasing → task_state (unless durable behavior dominates)
2. "The service must/does..." → service_memory
3. "All services must..." → project_memory
4. "The project does not/scope is..." → project_memory
5. Sensitive content → ALWAYS SKIP
6. Prefer writing durable specs without action verbs in training data

## 8. Generation Stages

### Stage 1: Batch200 (200 cases)
- Generate 100 new cases (batch200_0001-0100)
- Merge with batch100 (already validated)
- Distribution targets: same as batch500 but at 200 scale
- Audit: full semantic audit, label policy check
- Apply corrections
- **Gate:** Batch200 passes audit with ≤5 human-review-needed cases → proceed to stage 2

### Stage 2: Batch500 (300 additional cases)
- Generate 300 more cases using validated batch200 as template
- Merge → 500 training-pool cases
- Audit: sample-based audit (spot-check 10% = 50 cases)
- Distribution report
- **Gate:** All distribution targets within range, 0 sensitive STOREd → proceed to dev/gold

### Stage 3: Dev + Gold
- Extract dev (80) and gold (100) from distinct generation batches
- Ensure no leakage between splits
- Lock gold after audit
- **Gate:** Dev passes same validations as train, gold is representative and locked

## 9. Human Review Gates

See `docs/v05/V05_GENERATION_REVIEW_GATES.md` for detailed checkpoint definitions.

Summary:
1. **After batch200:** Full audit, all high/medium-risk cases reviewed
2. **After batch500:** Spot-check audit, distribution report
3. **Before dev:** Dev set audit, confirm no leakage
4. **Before gold:** Gold set audit, lock gold
5. **Before training:** Final go/no-go with all gates passed

## 10. Go / No-Go for Training

### Go (proceed to training) if:
- All 500 training-pool cases pass structural validation
- Distribution targets within acceptable ranges
- 0 sensitive units STOREd
- Dev and gold sets created and audited
- No leakage between splits
- Label policy violations <2% in spot-check sample
- Baseline eval plan ready

### No-Go (stop and reassess) if:
- Label policy violations >5% in spot-check
- Sensitive content found in STORE
- Distribution collapse (any target <50% of minimum)
- Gold set not representative of task distribution
- Significant leakage between splits

### Partial-Go (fix specific issues):
- Distribution slightly off → add targeted cases
- 2-3% label policy violations → correct and re-audit
- Minor leakage → re-split

---

**This blueprint is a plan only. Do not generate cases until the blueprint is reviewed and approved.**
