# V0.5 Batch50 Medium-Risk Review Packet

Date: 2026-06-01  
Context: 5.0-E2 — medium-risk review for batch50  
Status: Agent-generated review; no data modified

## 1. Scope

This packet provides a complete, human-readable review of the 3 medium-risk cases from the v0.5 batch50 semantic audit. The goal is to expose labeling uncertainties so a human reviewer can confirm or correct gold labels before scaling to 100 cases.

**No data has been modified.** These are review proposals only.

## 2. Why This Review Is Required Before Scaling

The batch50 semantic audit flagged 3 cases where target-boundary decisions are debatable:

1. **v05_batch50_0007**: Is "Qwen3-4B + LoRA" a durable project decision or a current-run config? (project_memory vs task_state)
2. **v05_batch50_0017**: Shares the "synthetic-data-only" pattern with v05_sample_0006. Is it redundant?
3. **v05_batch50_0024**: Are cross-service operational rules correctly project_memory? Or should u1 be service_memory?

Scaling to 100 cases without resolving these could propagate labeling errors or redundancy. Resolving them now ensures the next 50 cases don't reinforce questionable labels.

## 3. Target Guideline Checklist

Applied to the 3 review cases:

| # | Rule | Applies to which case(s) |
| --- | --- | --- |
| 1 | `user_profile`: stable, non-sensitive, cross-project preferences | — |
| 2 | `project_memory`: project-level goals, scope, global decisions, cross-repo/service agreements | 0007(u3), 0017(u2), 0024(u1,u2) |
| 3 | `repo_memory`: repo paths, commands, directory structure, test conventions | — |
| 4 | `service_memory`: durable behavior, interfaces, constraints of a specific component | 0007(u1) |
| 5 | `task_state`: current progress, next steps, blockers, temporary constraints | 0007(u2), 0017(u1,u3), 0024(u3) |
| 6 | Sensitive/private → SKIP always | — (no sensitive content in these 3) |
| 7 | `project_memory` must NOT be a catch-all | Check: 0024 u1 (does it really cross services?) |
| 8 | `task_state` must NOT carry long-term service rules | Check: 0007 u3 (is this long-term or temporary?) |
| 9 | `repo_memory` vs `service_memory`: path/command vs component behavior | — |
| 10 | Cross-service rule → project_memory ONLY if it crosses repo/service boundaries durably | Check: 0024 u1 (stated as export-specific) |

---

## 4. Full Review: v05_batch50_0007

### Case Details

| Field | Value |
| --- | --- |
| **case_id** | v05_batch50_0007 |
| **source** | new30 |
| **runtime_context** | project: memory-router, repo: distilled-memory-policy-router, service: eval_runner, task: plan evaluation improvements |
| **candidate_memories** | (none) |
| **shape** | STORE/SKIP-only |

**Current Units:**
- u1: "The eval_runner must support side-by-side comparison of multiple interfaces in a single run."
- u2: "Add a bar chart output mode to the eval_runner for visualizing per-interface metrics."
- u3: "The v0.5 training targets Qwen3-4B with LoRA, not full fine-tuning."

**Current Gold:**
- READ: []
- STORE: u1→service_memory, u2→task_state, u3→project_memory
- SKIP: []
- DSL: `READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE project_memory u3\nSKIP NONE`

**Tags:** store_skip_only, service_vs_task_state, project_vs_repo, target_boundary

**Notes:** u1 is durable eval_runner capability → service_memory. u2 is current feature request → task_state. u3 is a project-level training decision (Qwen3-4B + LoRA) → project_memory.

### Why Medium-Risk

The risk is isolated to **u3 only** (u1 and u2 are unambiguous).

u3 reads: "The v0.5 training targets Qwen3-4B with LoRA, not full fine-tuning."

The unit contains two claims in one sentence:
1. The training method is LoRA (not full fine-tuning) — an architectural decision
2. The model is Qwen3-4B — a specific model choice

The agent labeled the whole unit as `project_memory`, arguing it's a "project-level training decision."

### Target-Boundary Issue

The core question: Is this unit describing a **durable project decision** (project_memory) or a **current-run configuration** (task_state)?

**Arguments for project_memory (keep):**
- LoRA vs full fine-tuning is an architectural choice that sets project direction
- The decision affects all training infrastructure, not just one run
- It's recorded as a project-level scope/strategy decision, not a task checklist item

**Arguments for task_state (modify):**
- The unit explicitly says "v0.5" — this is version-specific
- Qwen3-4B is a specific model that could change in v0.6 or a challenger run
- Training configuration (model choice, method choice) is typically a task-level plan, not a project-level scope decision
- The TARGET_GUIDELINE says task_state is for "current task progress, active constraints, next steps" — a training plan fits this

**Arguments for splitting (not possible with parser):**
- If the unit could be split: "Use LoRA" → project_memory (durable method), "Qwen3-4B" → task_state (specific model choice)
- But the parser cannot split units — we must choose one label for the whole unit

### Possible Alternative Labeling

**Option A: Keep current (u3 → project_memory)**
- Rationale: Training methodology (LoRA) and model architecture are project-level strategic decisions that transcend any single run. Even if the specific model changes in v0.6, the LoRA approach is likely to persist.
- Risk: Teaches the model that version-specific training configurations are project_memory
- DSL unchanged

**Option B: Modify u3 → task_state**
- Rationale: "v0.5 training targets Qwen3-4B" is a current-run plan. Model choice and training method are task-level configuration decisions that could change between versions. The project-level decisions are already captured in memories (not present in this case but would be in real scenarios).
- Updated gold:
  ```
  STORE service_memory u1
  STORE task_state u2
  STORE task_state u3
  ```
- Updated DSL: `READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE task_state u3\nSKIP NONE`
- Risk: May train the model to under-assign project_memory for genuine strategic decisions

**Option C: Replace u3 with a clearer project_memory unit**
- Replace u3 with a unit that unambiguously describes a project-level scope or strategy decision (e.g., "The project scope explicitly excludes retriever training and writer training")
- Rationale: The current u3 is ambiguous and doesn't add clear training value. A cleaner unit would be more instructional.
- Risk: Changes the case structure; requires case regeneration

### Recommendation

**Lean toward Option B (modify to task_state).**

Reasoning:
- The unit is explicitly version-scoped ("v0.5"), making it a current-run plan
- Training configuration decisions are typically task-level, not project-level
- The stronger project_memory signal (LoRA as durable method) is diluted by the specific model choice (Qwen3-4B)
- Changing to task_state is the lower-risk correction: it avoids teaching the model that version-specific configs are durable project decisions

**Confidence:** Medium. Both interpretations are defensible. The deciding factor is whether the reviewer views training methodology as a project-level strategy or a task-level configuration.

**Human decision required:** Yes.

---

## 5. Full Review: v05_batch50_0017

### Case Details

| Field | Value |
| --- | --- |
| **case_id** | v05_batch50_0017 |
| **source** | new30 |
| **runtime_context** | project: memory-router, repo: distilled-memory-policy-router, service: training, task: design v0.5 training data split |
| **candidate_memories** | m1 [project_memory]: LoRA on Qwen3-4B with SFT; m2 [project_memory]: project only trains router, not retriever/writer; m3 [service_memory]: eval_runner requires locked gold |
| **shape** | READ+STORE joint |

**Current Units:**
- u1: "The training split should be 800 train / 100 dev / 100 gold, with gold locked immediately after creation."
- u2: "The project will only ever use synthetic training data; real production data is permanently out of scope."
- u3: "Draft the data split plan section in the training plan doc today."

**Current Gold:**
- READ: m1, m2 (skips m3)
- STORE: u1→task_state, u2→project_memory, u3→task_state
- SKIP: []
- DSL: `READ m1,m2\nSTORE task_state u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`

**Tags:** read_store_joint, project_vs_repo, target_boundary, related_but_useless

**Notes:** u1 is current split plan → task_state. u2 is permanent project safety decision (synthetic-only forever) → project_memory. u3 is current writing task → task_state.

### Why Medium-Risk

The risk is about **redundancy with v05_sample_0006**, not about labeling correctness.

Both cases teach the same core lesson: **"synthetic data only" → project_memory**. The question is whether having two cases teach the same pattern adds value or creates redundancy.

### Duplication Analysis: v05_batch50_0017 vs v05_sample_0006

See §7 for full comparison. Summary:

| Dimension | v05_sample_0006 | v05_batch50_0017 | Duplicate? |
| --- | --- | --- | --- |
| Project domain | data-platform / pipeline | memory-router / training | Different ✓ |
| Case shape | STORE/SKIP-only | READ+STORE joint | Different ✓ |
| Candidate memories | 0 | 3 (2 read, 1 skipped) | Different ✓ |
| Synthetic-data unit text | "The data-platform pilot uses synthetic service scenarios only; no real production data." | "The project will only ever use synthetic training data; real production data is permanently out of scope." | Similar meaning, different wording and domain |
| Synthetic-data unit label | project_memory | project_memory | Same ✓ |
| Other units | u2: task_state (next action), u3: SKIP (lunch) | u1: task_state (split plan), u3: task_state (writing task) | Different structure |
| Teaching signal | Basic: synthetic-data-only → project_memory | Enriched: synthetic-data-only → project_memory, WITH context from project memories, WITH READ selectivity | Not identical |

### Assessment

The two cases are **not exact duplicates and not semantic duplicates**. They differ in:
- Project domain (data-platform vs memory-router)
- Case shape (STORE/SKIP-only vs READ+STORE joint)
- Supporting context (0017 has memories that provide project-level context; 0006 has none)
- The synthetic-data unit wording: 0006 uses "pilot" language (could be temporary), 0017 uses "only ever" / "permanently" (unambiguously permanent)

**However**, they do teach the same core labeling pattern: a unit stating "synthetic data only" → project_memory. Having both in the batch provides two examples of this pattern, which is not harmful and could even be beneficial (showing the pattern generalizes across domains).

### Recommendation

**Keep v05_batch50_0017 as-is.**

Reasoning:
- Different domains provide generalization evidence
- Different case shapes (STORE/SKIP-only vs READ+STORE joint) teach different output formats
- 0017 uses stronger permanence language, addressing the concern raised in v05_sample_0006's P5.7-D review
- The batch50 is 50 cases — having 2 cases teach the same pattern across 2 domains is acceptable
- At 100+ case scale, more variety should be added; but for batch50, this level of signal overlap is fine

**Confidence:** Medium-High. The cases are clearly different in structure and domain; the shared teaching signal is not problematic at this scale.

**Human decision required:** Yes (but recommendation is strong).

---

## 6. Full Review: v05_batch50_0024

### Case Details

| Field | Value |
| --- | --- |
| **case_id** | v05_batch50_0024 |
| **source** | new30 |
| **runtime_context** | project: data-platform, repo: data-jobs, service: export, task: record permanent project data policy |
| **candidate_memories** | (none) |
| **shape** | STORE/SKIP-only |

**Current Units:**
- u1: "The export service must never log or store raw invoice line items that contain customer PII."
- u2: "All data-platform services must use the centralized secret manager for API keys and credentials."
- u3: "Add PII masking to the export debug logs before the next production deployment."

**Current Gold:**
- READ: []
- STORE: u1→project_memory, u2→project_memory, u3→task_state
- SKIP: []
- DSL: `READ NONE\nSTORE project_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`

**Tags:** store_skip_only, project_vs_repo, target_boundary

**Notes:** u1 is cross-service data safety rule → project_memory. u2 is cross-service infrastructure rule → project_memory. u3 is current task → task_state.

### Why Medium-Risk

The risk is about whether u1 and u2 are correctly labeled as **project_memory** (cross-service rules) or should be **service_memory** (service-specific rules).

The key question: does the wording of each unit support the cross-service interpretation?

### Target-Boundary Issue

**u1: "The export service must never log or store raw invoice line items that contain customer PII."**

- The unit text says "The export service" — this names a specific service
- The agent's notes argue it "applies across all services, not just export"
- But the text does NOT say "All services" — it says "The export service"

**Interpretations:**
- **project_memory argument:** The principle of "don't log PII" applies across all data-platform services. Even though u1 says "export service," the rule is intended to be project-wide. The unit is recording a project-level data safety policy.
- **service_memory argument:** The text names a specific service. If the rule is truly cross-service, the wording should say so (like u2 does). A reader would interpret this as an export-specific rule → service_memory.

**u2: "All data-platform services must use the centralized secret manager for API keys and credentials."**

- The text explicitly says "All data-platform services" — this IS cross-service
- This is unambiguously a project-level infrastructure policy
- **project_memory is clearly correct** for u2

**u3: "Add PII masking to the export debug logs before the next production deployment."**

- Current implementation task → task_state
- **task_state is clearly correct** for u3

### Possible Alternative Labeling

**Option A: Keep current (u1→project_memory, u2→project_memory, u3→task_state)**
- Rationale: The reviewer agrees with the agent's intent that u1 is a cross-service rule despite the export-specific wording. The case is about "permanent project data policy" as stated in the task context.
- Risk: Teaches the model that service-named rules can be project_memory if the intent is cross-service. This may confuse the model about when naming a service means service_memory.
- DSL unchanged

**Option B: u1→service_memory, u2→project_memory, u3→task_state**
- Rationale: u1's text names the export service specifically. If it were truly cross-service, it would say "All services" like u2 does. Following the text literally, u1 is a service-specific rule.
- Updated gold:
  ```
  STORE service_memory u1
  STORE project_memory u2
  STORE task_state u3
  ```
- Updated DSL: `READ NONE\nSTORE service_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`
- Benefit: Creates a cleaner contrast within the same case: u1 is service-level (export), u2 is project-level (all services). Teaches the distinction more clearly.
- Risk: May be too literal — the agent's intent was that the rule IS cross-service

**Option C: Reword u1 to make it explicitly cross-service**
- Change u1 text to: "No data-platform service may log or store raw data records that contain customer PII."
- Then keep as project_memory
- Rationale: Fix the wording to match the intent, rather than changing the label
- Risk: Changes case content; requires regeneration

### Recommendation

**Lean toward Option B (u1→service_memory, keep u2 as project_memory).**

Reasoning:
- u1's text literally says "The export service" — the model should learn that service-named rules are service_memory
- u2's text literally says "All data-platform services" — clear project_memory signal
- The case then teaches the contrast: service-specific rule (u1) vs project-wide rule (u2), both followed by an implementation task (u3)
- This creates a better teaching case than two project_memory labels
- The case still has one project_memory (u2), so project_memory representation doesn't drop

If the reviewer's intent is that u1 IS genuinely a cross-service policy, Option A is also defensible. But Option B is recommended because it follows the text more faithfully and creates a better contrast.

**Confidence:** Medium. Both options are defensible. The recommendation is driven by the literal text, not the agent's intended interpretation.

**Human decision required:** Yes.

---

## 7. v05_batch50_0017 vs v05_sample_0006 Duplication Analysis

### Full Text Comparison

| Dimension | v05_sample_0006 | v05_batch50_0017 |
| --- | --- | --- |
| **case_id** | v05_sample_0006 | v05_batch50_0017 |
| **source** | seed20 (corrected P5.7-D) | new30 |
| **project** | data-platform | memory-router |
| **repo** | data-jobs | distilled-memory-policy-router |
| **service** | pipeline | training |
| **task** | record pipeline scope decision | design v0.5 training data split |

### Runtime Context Comparison

| Field | v05_sample_0006 | v05_batch50_0017 |
| --- | --- | --- |
| project | data-platform | memory-router |
| repo | data-jobs | distilled-memory-policy-router |
| service | pipeline | training |
| task | record pipeline scope decision | design v0.5 training data split |

**Verdict: Different domains.** data-platform vs memory-router, pipeline vs training. No overlap.

### Candidate Memories Comparison

| | v05_sample_0006 | v05_batch50_0017 |
| --- | --- | --- |
| Count | 0 | 3 |
| Content | N/A | m1: LoRA on Qwen3-4B (project), m2: router-only training (project), m3: locked gold (service) |

**Verdict: Completely different.** 0006 has no memories; 0017 has 3 memories with READ selectivity.

### Current Units Comparison

| v05_sample_0006 | v05_batch50_0017 | Same? |
| --- | --- | --- |
| u1: "The data-platform pilot uses synthetic service scenarios only; no real production data." | u2: "The project will only ever use synthetic training data; real production data is permanently out of scope." | Similar meaning |
| u2: "Next, add a retry wrapper for the pipeline job that fails on transient network errors." | u1: "The training split should be 800 train / 100 dev / 100 gold, with gold locked immediately after creation." | Different |
| u3: "Today's lunch order will be from the Thai place." | u3: "Draft the data split plan section in the training plan doc today." | Different |

**Verdict on synthetic-data units:**
- 0006 u1: "The data-platform pilot uses synthetic service scenarios only; no real production data."
- 0017 u2: "The project will only ever use synthetic training data; real production data is permanently out of scope."

These are NOT exact duplicates (different words) and NOT semantic duplicates (different domain: data-platform services vs memory-router training data). They teach the same labeling pattern but in genuinely different contexts.

**Verdict: Different content.** Only 1/3 units share theme; 2/3 are completely different. Different project domains. Different case shapes.

### Gold Label Comparison

| v05_sample_0006 | v05_batch50_0017 | Pattern Match? |
| --- | --- | --- |
| u1 → project_memory (synthetic data) | u2 → project_memory (synthetic data) | Same pattern ✓ |
| u2 → task_state (next action) | u1 → task_state (split plan) | Different content, same target |
| u3 → SKIP (irrelevant chatter) | u3 → task_state (writing task) | Different |

### Overall Duplication Assessment

| Criteria | Result |
| --- | --- |
| Exact text duplicates? | No. Zero exact matches across units or memories. |
| Semantic duplicates? | Partially. One unit pair teaches the same labeling pattern (synthetic-data → project_memory), but in different domains with different wording. |
| Gold pattern identical? | Partially. Both have synthetic-data → project_memory + another unit → task_state. But 0006 has a SKIP; 0017 has 3 STOREs. |
| Same domain/project? | No. Different projects (data-platform vs memory-router). |
| Same case shape? | No. STORE/SKIP-only vs READ+STORE joint. |
| Provides new value? | Yes. Different domain, different shape, READ selectivity, stronger permanence language. |

### Recommendation on Duplication

**Keep both. Not redundant.**

- The shared "synthetic data → project_memory" pattern appears in TWO cases across TWO domains, which is actually desirable for generalization
- 0017 enriches the pattern with project-level memories (m1, m2) that provide context for why synthetic-data is project_memory
- 0017 uses stronger language ("only ever", "permanently out of scope") addressing the P5.7-D concern about permanence
- The cases have different shapes, different unit counts, and different READ decisions
- At 50-case scale, 2 cases sharing a thematic pattern is acceptable; at 100+ scale, ensure not >5% of cases teach the same single pattern

---

## 8. Summary of Recommended Decisions

| # | Case ID | Risk | Issue | Recommendation | Confidence | Human Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | v05_batch50_0007 | Medium | u3 (Qwen3-4B+LoRA) → project_memory or task_state? | **Modify: u3 → task_state** | Medium | **Yes** |
| 2 | v05_batch50_0017 | Medium | Redundant with v05_sample_0006? | **Keep**: not redundant, different domains/shapes | Medium-High | **Yes** |
| 3 | v05_batch50_0024 | Medium | u1 (export PII rule) → project_memory or service_memory? | **Modify: u1 → service_memory** | Medium | **Yes** |

## 9. Whether Batch50 Is Ready to Scale After Decisions

**After the 3 decisions are resolved, batch50 is ready to serve as a template for scaling to 100.**

Remaining considerations:
- user_profile count is at minimum (4) — scaling should add more
- project_memory boundary will continue to require human review at each scale step
- domain variety (3 projects) should expand in the next 50 cases

## 10. Recommended Next Step

**Context 5.0-F: Scale to 100-case batch** after human review of this packet.

1. Apply reviewer's decisions to the 3 medium-risk cases
2. Regenerate SFT messages for any modified cases
3. Generate 50 more cases (focus: user_profile, project_memory variety, new domains)
4. Merge → 100 cases → full validation → audit
5. Decide: ready for 500+ training data generation?

Do not:
- Scale to 100 before decisions are applied
- Start training
- Lock gold
- Generate full train/dev/gold
