# V0.5 Batch100 Correction Proposals

Date: 2026-06-01  
Context: 5.0-F2 — batch100 correction proposals  
Status: Proposals only; NO data modified

## 1. Correction Proposal Table

| Priority | Case ID | Unit | Current Target | Proposed Target | Rationale |
| --- | --- | --- | --- | --- | --- |
| Medium | v05_batch100_0040 | u1 | service_memory | task_state | Pure implementation plan: "Add incremental asset processing" |
| Medium | v05_batch100_0041 | u1 | service_memory | task_state | Pure implementation plan: "Add incremental indexing" |
| Medium | v05_batch100_0045 | u1 | service_memory | task_state | Implementation infrastructure: "Add automated performance tests" |
| Medium | v05_batch100_0026 | u1 | service_memory | task_state | Implementation-focused: "Add semantic search" |
| Medium | v05_batch100_0042 | u1 | service_memory | task_state | Implementation feature: "Add a dark mode toggle" |
| Medium | v05_batch100_0027 | u1 | service_memory | task_state | Implementation feature: "Add a PDF export button" |
| Medium | v05_batch100_0044 | u1 | service_memory | task_state | Implementation plan: "Add a recommendation engine" |
| Medium | v05_batch100_0028 | u1 | service_memory | task_state | Implementation plan: "Add multi-city booking" |
| Medium | v05_batch100_0035 | u1 | service_memory | task_state | Implementation config: "Add separate build targets" |
| Medium | v05_batch100_0049 | u1 | service_memory | task_state | Implementation plan: "Add prerequisite validation" |
| Optional | v05_batch100_0029 | u1 | service_memory | task_state | Debatable: "Add rubric-based grading" has behavioral spec embedded |
| Optional | v05_batch100_0030 | u1 | service_memory | task_state | Debatable: "Add automatic texture atlas" has behavioral spec |
| Optional | v05_batch100_0034 | u1 | service_memory | task_state | Debatable: "Add a waitlist" has behavioral spec |
| Keep | v05_batch100_0012 | u3 | project_memory | (keep) | SOC2 compliance is correctly project-level |
| Keep | v05_batch100_0047 | u1,u2 | project_memory | (keep) | Cross-service maintenance/safety policies correctly project-level |

## 2. Per-Case Alternatives (Top 10)

---

### Case v05_batch100_0040 — u1: service_memory → task_state

**Current:** u1 "Add incremental asset processing: only rebuild assets whose content hash has changed since the last build." → service_memory

**Option A (Keep):** The incremental processing behavior IS a durable pipeline capability.

**Option B (Modify):** Change to task_state. The "Add" framing is the primary signal — this is an implementation task.

**Recommended:** Option B. The unit starts with "Add" and describes what to implement, not what the service permanently does.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0041 — u1: service_memory → task_state

**Current:** u1 "Add incremental indexing that only processes documents changed since the last indexed commit." → service_memory

**Recommended:** Option B (task_state). Pure implementation plan with no durable behavioral spec embedded.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0045 — u1: service_memory → task_state

**Current:** u1 "Add automated performance tests that run after each build and fail if frame-time exceeds 16ms on the target platform." → service_memory

**Recommended:** Option B (task_state). Performance test infrastructure is implementation, not a service behavior.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0026 — u1: service_memory → task_state

**Current:** u1 "Add semantic search using sentence-transformers to augment the existing TF-IDF results with a hybrid ranking." → service_memory

**Option A (Keep):** Hybrid ranking IS a durable new search capability.

**Option B (Modify):** Change to task_state. The "Add" framing and specific tool choice (sentence-transformers) are implementation-level.

**Recommended:** Option B. The tool-specific nature ("sentence-transformers") makes this more implementation than durable specification.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0042 — u1: service_memory → task_state

**Current:** u1 "Add a dark mode toggle that switches all chart colors to a dark palette with light text and muted gridlines." → service_memory

**Recommended:** Option B (task_state). A UI toggle is a feature, not a behavioral invariant.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0027 — u1: service_memory → task_state

**Current:** u1 "Add a PDF export button that renders the current dashboard view using headless Chromium." → service_memory

**Recommended:** Option B (task_state). UI feature + specific tool choice (headless Chromium).

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0044 — u1: service_memory → task_state

**Current:** u1 "Add a recommendation engine that suggests courses based on a student's completed courses and stated preferences." → service_memory

**Recommended:** Option B (task_state). "Add a recommendation engine" is an implementation plan.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0028 — u1: service_memory → task_state

**Current:** u1 "Add multi-city booking that allows up to 5 segments in a single booking, with each segment priced independently." → service_memory

**Recommended:** Option B (task_state). Implementation plan for a new feature.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0035 — u1: service_memory → task_state

**Current:** u1 "Add separate build targets for PC, PlayStation 5, and Nintendo Switch with platform-specific texture compression settings." → service_memory

**Recommended:** Option B (task_state). Build configuration change, not durable behavior.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

### Case v05_batch100_0049 — u1: service_memory → task_state

**Current:** u1 "Add prerequisite validation that blocks enrollment if the student has not completed all prerequisite courses with a passing grade." → service_memory

**Recommended:** Option B (task_state). Implementation plan for enrollment validation feature.

**DSL change:** `STORE service_memory u1` → `STORE task_state u1`

---

## 3. Expected Target Count Changes

If all 10 medium corrections are applied:

| Case | Before | After | Change |
| --- | --- | --- | --- |
| v05_batch100_0040 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0041 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0045 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0026 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0042 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0027 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0044 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0028 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0035 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |
| v05_batch100_0049 | `STORE service_memory u1` | `STORE task_state u1` | svc −1, task +1 |

**Net effect:** service_memory: 89 → 79, task_state: 50 → 60.

## 4. SFT Regeneration Implications

If corrections are applied:
- 10 cases modified out of 100
- 10 DSL lines changed
- SFT messages for those 10 cases regenerated
- Full batch100 validation re-run

## 5. Notes on Optional Corrections

The 3 optional corrections (0029, 0030, 0034) have stronger behavioral specifications embedded in their "Add X" phrasing. The agent recommends keeping them as service_memory because the behavioral descriptions outweigh the "Add" framing. Reviewer may choose to apply some or all.

## 6. Confirmed-Keep Cases

- v05_batch100_0012 u3 (SOC2 → project_memory): Correct. Cross-service regulatory compliance.
- v05_batch100_0047 u1,u2 (maintenance/safety policies → project_memory): Correct. Cross-service rules with permanent safety implications.

## 7. Human Decisions Required

| # | Case | Unit | Decision | Impact |
| --- | --- | --- | --- | --- |
| 1 | v05_batch100_0040 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 2 | v05_batch100_0041 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 3 | v05_batch100_0045 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 4 | v05_batch100_0026 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 5 | v05_batch100_0042 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 6 | v05_batch100_0027 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 7 | v05_batch100_0044 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 8 | v05_batch100_0028 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 9 | v05_batch100_0035 | u1 | service_memory or task_state? | svc −1 / task +1 |
| 10 | v05_batch100_0049 | u1 | service_memory or task_state? | svc −1 / task +1 |
| — | v05_batch100_0012 | u3 | Keep project_memory? | Confirm |
| — | v05_batch100_0047 | u1,u2 | Keep project_memory? | Confirm |

**Total: 10 decisions on service/task boundary + 2 confirmations on project_memory.**
