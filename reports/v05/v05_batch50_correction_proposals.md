# V0.5 Batch50 Correction Proposals

Date: 2026-06-01  
Context: 5.0-E2 — correction proposals for batch50 medium-risk cases  
Status: Proposals only; NO data has been modified

## 1. Correction Proposal Table

| Case ID | Current Issue | Option A (Keep) | Option B (Modify) | Option C (Replace/Remove) | Recommended | Human Decision |
| --- | --- | --- | --- | --- | --- | --- |
| v05_batch50_0007 | u3 "Qwen3-4B+LoRA" → project_memory or task_state? | Keep as project_memory | u3→task_state | Replace u3 with clearer project_memory unit | B: u3→task_state | **Yes** |
| v05_batch50_0017 | Redundant with v05_sample_0006? | Keep — not redundant | — | Replace with different project_memory case | A: Keep | **Yes** |
| v05_batch50_0024 | u1 "export service PII rule" → project_memory or service_memory? | Keep as project_memory | u1→service_memory | Reword u1 to be explicitly cross-service | B: u1→service_memory | **Yes** |

## 2. Per-Case Alternatives with Exact DSL Changes

---

### Case v05_batch50_0007 — project_memory vs task_state

**Current label:**
```
STORE service_memory u1
STORE task_state u2
STORE project_memory u3
```
DSL: `READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE project_memory u3\nSKIP NONE`

**Concern:** u3 "The v0.5 training targets Qwen3-4B with LoRA, not full fine-tuning." Is this a durable project-level training strategy or a current-run configuration?

**Option A: Keep current label (u3→project_memory)**
- Rationale: LoRA vs full fine-tuning is a project-level architectural decision about training methodology. This decision shapes all training infrastructure and is more than a task-level detail.
- Risk: "v0.5" is version-specific. Qwen3-4B is a specific model choice. Teaching the model that version-scoped, model-specific choices are project_memory may be confusing.
- DSL unchanged.

**Option B: Modify u3 → task_state**
- Rationale: The unit is explicitly scoped to "v0.5" — it's a current-run plan. Model selection and training method are task-level configuration decisions. The project-level strategic decisions are captured elsewhere (e.g., in m1/m2 of v05_batch50_0017).
- Updated gold:
  ```
  STORE service_memory u1
  STORE task_state u2
  STORE task_state u3
  ```
- Updated DSL: `READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE task_state u3\nSKIP NONE`
- Tags unchanged.
- Notes updated: "u3 describes current v0.5 training configuration (Qwen3-4B + LoRA) → task_state. This is a specific run plan, not a permanent project decision."
- SFT regeneration: Yes.

**Option C: Replace u3 with a clearer project_memory unit**
- Rationale: The current u3 is ambiguous. Replace with something like "The project uses LoRA-based training exclusively; full fine-tuning is permanently out of scope for all versions." → project_memory.
- Risk: Requires case regeneration; may not be worth the effort for one unit.
- Not recommended for batch50 scale.

**Recommended option:** **Option B (u3→task_state).** The version-scoped, model-specific nature of "v0.5 training targets Qwen3-4B" reads as a current plan, not a durable project decision. This is the lower-risk correction.

**Human decision required:** Yes.
**SFT regeneration needed:** Yes, if Option B chosen.

---

### Case v05_batch50_0017 — duplication

**Current label:**
```
STORE task_state u1
STORE project_memory u2
STORE task_state u3
```
DSL: `READ m1,m2\nSTORE task_state u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`

**Concern:** u2 "The project will only ever use synthetic training data; real production data is permanently out of scope" teaches the same labeling pattern as v05_sample_0006 u1 "The data-platform pilot uses synthetic service scenarios only; no real production data." Both are synthetic-data-only → project_memory. Is this redundant?

**Option A: Keep (not redundant)**
- Rationale: Different project domains (memory-router vs data-platform), different case shapes (READ+STORE joint vs STORE/SKIP-only), different supporting context (3 candidate memories with READ selectivity vs no memories). The shared teaching signal across two domains aids generalization. At 50-case scale, 2 cases sharing a thematic pattern is not excessive.
- DSL unchanged.

**Option B: Replace with different project_memory case**
- Rationale: The pattern is already covered by v05_sample_0006. Replace 0017 with a case teaching a different project_memory concept (e.g., cross-repo architecture decision, evaluation standard, scope exclusion).
- Risk: Requires generating a new case, revalidating, and potentially losing a well-structured READ+STORE joint case.
- Not recommended at batch50 scale. Consider at 100+ scale if synthetic-data pattern appears >3 times.

**Recommended option:** **Option A (Keep).** The cases are structurally and contextually different. Two instances of the same labeling pattern in a 50-case batch is acceptable and arguably beneficial for teaching generalization.

**Human decision required:** Yes.
**SFT regeneration needed:** No (if kept).

---

### Case v05_batch50_0024 — project_memory vs service_memory

**Current label:**
```
STORE project_memory u1
STORE project_memory u2
STORE task_state u3
```
DSL: `READ NONE\nSTORE project_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`

**Concern:** u1 "The export service must never log or store raw invoice line items that contain customer PII" is labeled project_memory (cross-service rule), but the text names a specific service ("The export service"). Should it be service_memory instead?

**Option A: Keep current label (u1→project_memory)**
- Rationale: The intent is that the "don't log PII" rule applies across ALL data-platform services, not just export. The case is recording a project-level data safety policy. The reviewer may agree with the agent's intent.
- Risk: The literal text says "The export service." If the model learns from text alone, it sees a service-named rule and may over-assign project_memory to service-specific rules.
- DSL unchanged.

**Option B: Modify u1 → service_memory**
- Rationale: The text literally names a specific service. The model should learn that rules naming a specific service → service_memory, while rules naming "All services" → project_memory. u2 already provides the project_memory example with its cross-service wording. Changing u1 to service_memory creates a better contrast case.
- Updated gold:
  ```
  STORE service_memory u1
  STORE project_memory u2
  STORE task_state u3
  ```
- Updated DSL: `READ NONE\nSTORE service_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`
- Tags unchanged (project_vs_repo still applies via u2).
- Notes updated: "u1 is an export-specific PII rule → service_memory (the text names 'The export service'). u2 is an explicitly cross-service rule → project_memory ('All data-platform services'). u3 is current task → task_state. Shows the contrast: service-named rules are service_memory; cross-service rules are project_memory."
- SFT regeneration: Yes.

**Option C: Reword u1 to be explicitly cross-service, keep project_memory**
- Change u1 text to: "No data-platform service may log or store raw data records that contain customer PII."
- Keep project_memory label.
- Rationale: Fix the wording to match the intent.
- Risk: Changes the case content. At batch50 scale, Option B is simpler and achieves the same teaching value.

**Recommended option:** **Option B (u1→service_memory).** The literal text should drive the label. When the text names a specific service, the rule is service_memory. When the text names "all services," the rule is project_memory. This creates a clear, text-driven distinction that the model can learn. The case still has one project_memory (u2), so project_memory representation doesn't drop significantly (9→8).

**Human decision required:** Yes.
**SFT regeneration needed:** Yes, if Option B chosen.

## 3. SFT Regeneration Implications

If any case's gold labels are modified, the SFT messages must be regenerated:

| Case | SFT change? | What changes |
| --- | --- | --- |
| v05_batch50_0007 | If Option B | DSL: `STORE project_memory u3` → `STORE task_state u3`; assistant content changes |
| v05_batch50_0017 | If kept (Option A) | None |
| v05_batch50_0024 | If Option B | DSL: `STORE project_memory u1` → `STORE service_memory u1`; assistant content changes |

If both 0007 Option B and 0024 Option B are applied:
- 2 cases modified out of 50
- 2 DSL lines changed
- SFT messages for those 2 cases regenerated
- Full validation re-run
- project_memory STORE count: 9 → 8 (still ≥8 minimum)
- service_memory STORE count: 34 → 35
- task_state STORE count: 32 → 33

## 4. Human Decisions Required

| # | Case | Decision | Impact |
| --- | --- | --- | --- |
| 1 | v05_batch50_0007 | u3→project_memory (keep) or task_state (modify)? | Changes 1 STORE target; DSL changes if modified |
| 2 | v05_batch50_0017 | Keep or replace? | No change if kept; new case needed if replaced |
| 3 | v05_batch50_0024 | u1→project_memory (keep) or service_memory (modify)? | Changes 1 STORE target; DSL changes if modified |

**Total: 3 decisions across 3 cases. 0-2 STORE target changes possible.**
