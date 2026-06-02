# V0.5 Data Plan

Version: v0.5 draft  
Date: 2026-06-01  
Status: Planning; no data generated yet  

## 1. Data Source

Training data for v0.5 will be based on:

- **v0.4 pilot cases** (`data/v04/pilot_cases.jsonl`, 200 cases) — primary seed and style reference
- **v0.4 bridge cases** (`data/v04/bridge_cases.jsonl`, 40 cases) — boundary and edge-case reference
- **v0.4 spec and target guideline** — defines legal outputs, targets, and annotation rules

Existing pilot cases should be reviewed and possibly expanded, not mechanically duplicated. Bridge cases provide target-boundary examples that should inform new training case design.

## 2. Suggested Data Split

### Primary target (recommended)

| Split | Cases | Purpose |
| --- | ---: | --- |
| Train | 800–1000 | Training LoRA/SFT |
| Dev | 100 | Hyperparameter tuning, early stopping |
| Gold | 100 | Locked final evaluation |

### Fallback (if time/resource constrained)

| Split | Cases | Purpose |
| --- | ---: | --- |
| Train | 500 | Training LoRA/SFT |
| Dev | 80 | Hyperparameter tuning, early stopping |
| Gold | 100 | Locked final evaluation |

### Current State

- Existing pilot: 200 cases
- Existing bridge: 40 cases
- Existing subset50: 50 cases (used for A/B/C eval so far)
- **Need**: 360–860 additional training cases, 60–100 additional dev cases, 50–100 additional gold cases

## 3. Required Data Categories

Training data must cover these categories to ensure the model learns robust routing:

### Case Shape Distribution

| Shape | Description | Min % |
| --- | --- | ---: |
| READ-only | Only read memories, skip all units | 10–15% |
| STORE/SKIP-only | No memories to read, store or skip units | 20–25% |
| READ + STORE joint | Read memories AND store units | 25–35% |

### Tag / Difficulty Distribution

| Tag | Description | Target presence |
| --- | --- | ---: |
| `stale_memory` | Outdated memories that should NOT be read | ✓ |
| `related_but_useless` | Related but unhelpful memories | ✓ |
| `target_boundary` | Cases where target choice is subtle | ✓ (high priority) |
| `sensitive_boundary` | Units with private/sensitive content → SKIP | ✓ (high priority) |
| `user_profile_boundary` | User preference vs sensitive/private vs task_state | ✓ |
| `project_vs_repo` | Project-level decision vs repo implementation | ✓ |
| `repo_vs_service` | Repo path/convention vs service behavior | ✓ |
| `service_vs_task_state` | Durable service behavior vs current progress | ✓ (high priority) |
| `repo_convention` | Repository commands, paths, test conventions | ✓ |
| `service_invariant` | Durable service/component behavior | ✓ |
| `task_progress` | Current task progress, next steps, blockers | ✓ |
| `temporary_request` | One-off requests that should be SKIPped | ✓ |

### Target Distribution

Do not force exact balance, but prevent collapse. Approximate guidance:

| Target | Approximate % | Reasoning |
| --- | ---: | --- |
| `task_state` | 25–35% | Common in agent contexts; progress, next steps, blockers |
| `service_memory` | 20–30% | Common for component behavior descriptions |
| `repo_memory` | 15–20% | Coding-agent relevant; paths, commands, conventions |
| `project_memory` | 10–15% | Project-level decisions; NOT a catch-all |
| `user_profile` | 5–10% | Stable user preferences; smaller but important |
| SKIP (no target) | 30–40% of units | One-off, temporary, sensitive, and unrelated units |

## 4. Leakage Prevention Rules

To ensure fair evaluation:

1. **Subset50 cases**: If subset50 remains the primary evaluation set, do NOT include them in train or dev. They may be folded into gold if the evaluation standard changes, but this must be explicit.

2. **Few-shot examples**: The 3 few-shot examples (`v04_pilot_0082`, `v04_pilot_0037`, `v04_pilot_0056`) must be recorded. If used in training, they must NOT appear in dev or gold.

3. **Gold lock**: Once gold set is created, it must never be used for training, prompt design, or hyperparameter tuning. It is opened only for final evaluation.

4. **No exact duplicates**: No case should appear identically in more than one split. Cases with similar structure but different content are acceptable.

5. **No prompt examples from gold**: If training uses few-shot prompts, those examples must come from train, not dev or gold.

6. **Bridge cases**: Existing bridge cases may inform new case design but should not be directly copied into train/dev/gold without review.

## 5. Validation Requirements

Every training/dev/gold case must:

- Pass `src/v04/case_validator.py` (structural validation)
- Have gold.dsl that parses correctly with `src/v04/parser.py`
- Have consistent `gold.read`/`gold.store`/`gold.skip` with `gold.dsl`
- Not contain forbidden gold fields (`fact`, `decision`, `confidence`, etc.)
- Use only legal STORE targets (5 targets only)
- Cover every current unit exactly once in STORE or SKIP
- Reference only valid memory IDs in READ

Distribution checks:
- Tag distribution report
- Target distribution report
- Case shape distribution report
- Sensitive content audit (all `sensitive_boundary` cases must SKIP sensitive units)

## 6. Sensitive Content Safeguards

- All cases tagged `sensitive_boundary` must have sensitive units in `gold.skip`
- Audit: manually review at least 20% of `sensitive_boundary` cases in train
- If training introduces sensitive store behavior, halt training and investigate

## 7. Human Review Requirements

The following areas require explicit human review before training data is locked:

| Review Area | Why |
| --- | --- |
| `project_memory` vs `task_state` | Primary source of target confusion across all experiments |
| `service_memory` vs `task_state` | "Current progress" vs "durable service behavior" boundary |
| `related_but_useless` READ decisions | Model tends to over-read; gold labels must be clear |
| Sensitive/private SKIP | Must absolutely be SKIP; no exceptions |
| `user_profile` vs sensitive/private | Stable preferences vs things that must not be stored |
| Gold set labels | Final evaluation depends on gold quality |

## 8. Data Generation Strategy

### Phase 1: Review existing pilot

- Audit existing 200 pilot cases for target-boundary quality
- Identify cases that need label revision (especially `project_memory` vs `task_state`)
- Tag distribution check across all 200 cases

### Phase 2: Generate training cases

- Use pilot + bridge as style/template reference
- Target 500–1000 train cases covering all required categories
- Focus on target-boundary and sensitive-boundary cases
- Every new case must pass `case_validator`

### Phase 3: Create dev/gold splits

- Dev: 80–100 cases, representative distribution, used for tuning
- Gold: 100 cases, locked, never seen during training
- Validate no leakage between splits

### Phase 4: Final audit

- Run all validators
- Generate distribution reports
- Human review of flagged cases
- Lock gold set

## 9. Next Context (5.0-B)

Context 5.0-B should:
- Create a data split blueprint (exact case counts per category)
- Generate 20–30 sample training cases to validate the data generation pipeline
- NOT generate the full 500–1000 case dataset
- NOT lock the gold set yet

## 10. Files Reference

| File | Purpose |
| --- | --- |
| `docs/v05/V05_DATA_PLAN.md` | This document |
| `data/v04/pilot_cases.jsonl` | 200 existing pilot cases |
| `data/v04/bridge_cases.jsonl` | 40 bridge/boundary cases |
| `src/v04/case_validator.py` | Case structure validator |
| `src/v04/parser.py` | DSL parser for gold validation |
| `docs/v04_spec/CASE_SCHEMA.md` | Case record format |
| `docs/v04_spec/TARGET_GUIDELINE.md` | Target annotation rules |
