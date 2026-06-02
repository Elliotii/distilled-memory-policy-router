# V0.5 Sample Correction Proposals

Date: 2026-06-01  
Context: 5.0-C — correction proposals for high-risk sample cases  
Status: Proposals only; NO data has been modified  

## 1. High-Risk Correction Proposal Table

| Case ID | Current Issue | Option A (Keep) | Option B (Modify) | Option C (Remove/Uncertain) | Recommended | Human Decision |
| --- | --- | --- | --- | --- | --- | --- |
| v05_sample_0014 | u1 (current limitation → task_state?) u2 (future spec → service_memory?) | Keep as-is | Swap: u1→service_memory, u2→task_state | Mark uncertain, remove from training | **Uncertain** | **Yes** |
| v05_sample_0018 | u2 "optimize for routing metrics" → project_memory? | Keep as-is | u2→task_state (both are current training decisions) | Remove u2, keep rest | Lean Keep | **Yes** |
| v05_sample_0015 | u2 "does not implement MemoryOS" → project_memory? | Keep as-is | u2→repo_memory (repo-level scope description) | Remove u2, keep rest | Keep | **Yes** |
| v05_sample_0006 | u1 "synthetic data only" → project_memory? Permanent or temporary? | Keep if permanent | u1→task_state if temporary | Add note clarifying permanence | Keep (conditional) | **Yes** |
| v05_sample_0009 | u2 "single-turn only" → service_memory? Design invariant or temporary? | Keep if design invariant | u2→task_state if temporary limitation | Add note clarifying intent | Keep (conditional) | **Yes** |

## 2. Per-Case Alternatives with Exact DSL Changes

---

### Case v05_sample_0014 — service_memory vs task_state

**Current label:**
```
STORE task_state u1
STORE service_memory u2
STORE repo_memory u3
```
DSL: `READ NONE\nSTORE task_state u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE`

**Concern:** u1 describes current implementation state ("currently reports X but not Y"). u2 describes future design spec ("should show gold vs predicted"). The boundary between "current limitation" and "durable specification" is extremely fine.

**Option A: Keep current label**
- Rationale: "Currently reports X but not Y" is a statement about current progress/missing feature → task_state. "Should show X vs Y" is a durable design specification for the component → service_memory. u3 is clearly repo_memory.
- Risk: A reviewer may disagree that "currently missing" is task_state rather than a statement about what the service does.
- DSL unchanged.

**Option B: Swap u1 and u2 targets**
- Rationale: "Currently reports X but not Y" describes what the metrics module DOES (or doesn't) — that IS its current behavior, which is service_memory. "Should show gold vs predicted" is a planned feature that hasn't been implemented → task_state (next step).
- Updated gold:
  ```
  STORE service_memory u1
  STORE task_state u2
  STORE repo_memory u3
  ```
- Updated DSL: `READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE`
- SFT regeneration: Yes, assistant content would change.

**Option C: Both are task_state**
- Rationale: Both u1 and u2 describe current/future state of the same feature (confusion matrix). Neither is a settled, durable service behavior yet.
- Updated gold:
  ```
  STORE task_state u1
  STORE task_state u2
  STORE repo_memory u3
  ```
- Updated DSL: `READ NONE\nSTORE task_state u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE`
- Risk: u2 is actually a design spec — labeling it task_state may teach the model that design specs are temporary.

**Recommended option:** **Uncertain between A and B.** Option A (keep) is the agent's original choice and is defensible. Option B is equally defensible. The reviewer must decide based on their understanding of whether "what the service currently does" is task_state or service_memory.

**Human decision required:** Yes.
**SFT regeneration needed:** Yes, if option B or C is chosen.

---

### Case v05_sample_0018 — project_memory vs task_state

**Current label:**
```
STORE task_state u1
STORE project_memory u2
SKIP u3
```
DSL: `READ m1,m2\nSTORE task_state u1\nSTORE project_memory u2\nSKIP u3`

**Concern:** u2 "Training should optimize for routing metrics, not just cross-entropy loss" is labeled project_memory. Is this a durable project-level design principle, or a specific constraint on the current training run?

**Option A: Keep current label**
- Rationale: "Optimize for routing metrics" is a durable evaluation philosophy that applies to ALL training runs in this project, not just the current one. It's a project-level design decision about how training success is measured. u1 "LoRA rank 8" is a specific implementation plan → task_state.
- Risk: The distinction between "design principle" (project_memory) and "implementation plan" (task_state) is philosophical and may not be clearly teachable to a 4B model.
- DSL unchanged.

**Option B: Both u1 and u2 → task_state**
- Rationale: Both are specific to the current v0.5 training run. "Optimize for routing metrics" is a constraint on THIS training task, not necessarily a permanent project decision. The project-level decisions are already in m1 and m2.
- Updated gold:
  ```
  STORE task_state u1
  STORE task_state u2
  SKIP u3
  ```
- Updated DSL: `READ m1,m2\nSTORE task_state u1\nSTORE task_state u2\nSKIP u3`
- Risk: Loses the opportunity to teach the model that some decisions transcend individual tasks.

**Option C: Remove u2 from this case**
- Rationale: u2 is ambiguous and doesn't add clear training value. Keep the case with u1 and u3 only.
- Updated units: Remove u2, renumber u3→u2.
- Risk: Case becomes too simple (only 2 units).

**Recommended option:** **Lean toward Option A (Keep), but with low confidence.** The agent believes "optimize for routing metrics" reads as a durable design philosophy. However, if the reviewer disagrees, Option B is the cleanest alternative.

**Human decision required:** Yes.
**SFT regeneration needed:** Yes, if option B is chosen.

---

### Case v05_sample_0015 — project_memory classification

**Current label:**
```
STORE repo_memory u1
STORE project_memory u2
STORE task_state u3
```
DSL: `READ NONE\nSTORE repo_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`

**Concern:** u2 "does not implement a full MemoryOS; it only studies the memory policy router layer" → project_memory. Is this a project-level scope decision or a repo-level description?

**Option A: Keep current label**
- Rationale: "Does not implement MemoryOS" is a classic project-level scope boundary. It defines what the ENTIRE project is and isn't, across all repos and services. This is the canonical use of project_memory.
- DSL unchanged.

**Option B: u2 → repo_memory**
- Rationale: This is essentially a README-level statement about what the repo contains/doesn't contain. It's similar to a project description in a repo README.
- Updated gold:
  ```
  STORE repo_memory u1
  STORE repo_memory u2
  STORE task_state u3
  ```
- Updated DSL: `READ NONE\nSTORE repo_memory u1\nSTORE repo_memory u2\nSTORE task_state u3\nSKIP NONE`
- Risk: Dilutes the project_memory category and teaches the model that scope decisions are repo-level.

**Option C: Keep, but add explicit note**
- Rationale: Keep as project_memory but annotate why this is a strong example. Add to notes: "This is a canonical project_memory example: a durable project-level scope boundary that transcends any single repo or service."

**Recommended option:** **Keep (Option A).** This is the strongest project_memory example in the sample set. "Does not implement MemoryOS, only studies the memory policy router" is a textbook project-level scope decision. The agent's classification is correct.

**Human decision required:** Yes, but recommendation is strong.
**SFT regeneration needed:** No, if kept.

---

### Case v05_sample_0006 — project_memory permanence

**Current label:**
```
STORE project_memory u1
STORE task_state u2
SKIP u3
```
DSL: `READ NONE\nSTORE project_memory u1\nSTORE task_state u2\nSKIP u3`

**Concern:** u1 "uses synthetic service scenarios only; no real production data" → project_memory. Is this a permanent project decision or a temporary pilot-phase constraint?

**Option A: Keep if permanent**
- Rationale: If "synthetic data only" is a durable project safety decision (e.g., this project will NEVER use real production data), then project_memory is correct.
- DSL unchanged.
- Add to notes: "Assumes synthetic-data-only is a permanent project safety decision, not a temporary pilot constraint."

**Option B: Change to task_state if temporary**
- Rationale: If "synthetic data only" is just for the current pilot phase and real data will be used later, this is a temporary constraint → task_state.
- Updated gold:
  ```
  STORE task_state u1
  STORE task_state u2
  SKIP u3
  ```
- Updated DSL: `READ NONE\nSTORE task_state u1\nSTORE task_state u2\nSKIP u3`
- Risk: Loses a project_memory example. Already few in the set (only 3).

**Option C: Keep as project_memory with a "pilot phase" caveat**
- Rationale: Even if temporary, "synthetic data only" is a project-level scope decision FOR THE CURRENT PHASE. It affects all services in the project and is more than a task-level constraint.
- Risk: Teaches the model that temporary constraints can be project_memory.

**Recommended option:** **Keep (Option A) if permanent; change (Option B) if temporary.** The agent cannot determine permanence from the text alone. The reviewer must decide.

**Human decision required:** Yes.
**SFT regeneration needed:** Yes, if option B is chosen.

---

### Case v05_sample_0009 — service_memory vs task_state

**Current label:**
```
STORE service_memory u1
STORE service_memory u2
STORE repo_memory u3
```
DSL: `READ m1,m2\nSTORE service_memory u1\nSTORE service_memory u2\nSTORE repo_memory u3\nSKIP NONE`

**Concern:** u2 "still evaluates only single-turn cases, not multi-turn sessions" → service_memory. Is this a design invariant (eval_runner is intentionally single-turn) or a temporary limitation (multi-turn support is planned)?

**Option A: Keep if design invariant**
- Rationale: If eval_runner is intentionally single-turn by design (not planned to support multi-turn), then u2 is correctly service_memory — it's a durable design constraint.
- Add to notes: "Assumes single-turn evaluation is an intentional design decision, not a temporary limitation."
- DSL unchanged.

**Option B: Change u2 to task_state if temporary**
- Rationale: If multi-turn evaluation IS planned for the future, then "still evaluates only single-turn" is a current limitation → task_state.
- Updated gold:
  ```
  STORE service_memory u1
  STORE task_state u2
  STORE repo_memory u3
  ```
- Updated DSL: `READ m1,m2\nSTORE service_memory u1\nSTORE task_state u2\nSTORE repo_memory u3\nSKIP NONE`
- Risk: Changes the case semantics but creates a good service_vs_task boundary example.

**Option C: Split into two cases**
- Rationale: u1+u3 in one case (service_memory + repo_memory), u2 in a separate case if needed.
- Risk: Overcomplicates for a 20-case sample set.

**Recommended option:** **Keep (Option A) with clarification note.** The agent's intent was that u2 is a design invariant. If the reviewer considers "single-turn only" temporary, change to Option B.

**Human decision required:** Yes.
**SFT regeneration needed:** Yes, if option B is chosen.

---

## 3. SFT Regeneration Implications

If any case's gold labels are modified:

1. The `v05_sample_cases.jsonl` gold.store, gold.skip, and gold.dsl fields must be updated
2. The `v05_sample_sft_messages.jsonl` assistant content must be regenerated to match the new gold.dsl
3. All structural validations (case_validator, parse_policy_dsl, canonical consistency) must be re-run
4. The generation script (`src/v05/render_sft_messages.py`) can regenerate SFT messages from updated cases

**Recommendation:** After human review, apply all corrections in a single batch, then regenerate SFT messages in one pass.

## 4. Human Decisions Required

The following decisions MUST be made by a human reviewer before the sample set can be validated:

| # | Case | Decision | Impact |
| --- | --- | --- | --- |
| 1 | v05_sample_0014 | u1→task_state or service_memory? u2→service_memory or task_state? | Changes 2 STORE targets; DSL changes |
| 2 | v05_sample_0018 | u2→project_memory (keep) or task_state (modify)? | Changes 1 STORE target; DSL changes if modified |
| 3 | v05_sample_0015 | u2→project_memory (keep) or repo_memory (modify)? | Changes 1 STORE target if modified |
| 4 | v05_sample_0006 | Is "synthetic data only" permanent (keep as project_memory) or temporary (change to task_state)? | Changes 1 STORE target if temporary |
| 5 | v05_sample_0009 | Is "single-turn only" a design invariant (keep as service_memory) or temporary limitation (change to task_state)? | Changes 1 STORE target if temporary |
| 6 | v05_sample_0020 | u3 "laptop runs Ubuntu" → SKIP (keep) or user_profile (modify)? | Adds 1 STORE target if modified |

**Total: 6 decisions across 6 cases. 1-4 STORE target changes possible.**

## 5. Cases Requiring No Decision

The following 5 spot-check cases are recommended to keep as-is:

- v05_sample_0004: Clean service vs task distinction — keep
- v05_sample_0010: Excellent stale/sensitive handling — keep (reference case)
- v05_sample_0013: Clean READ selectivity — keep
- v05_sample_0002: Clean READ-only with stale — keep
- Plus the remaining 10 un-reviewed cases from the full set of 20

## 6. Post-Review Actions (Future Context)

After human review is complete:

1. Apply confirmed corrections to `v05_sample_cases.jsonl`
2. Regenerate `v05_sample_sft_messages.jsonl`
3. Re-run all validations (case_validator, parser, canonical consistency, leakage)
4. Update semantic audit with reviewer's decisions
5. If approach is approved, proceed to scale: 50-100 cases → 500-1000 train
