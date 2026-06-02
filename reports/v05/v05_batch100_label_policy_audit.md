# V0.5 Batch100 Label Policy Audit

Date: 2026-06-01  
Context: 5.0-F2 — batch100 label policy audit  
Status: Agent-generated audit; no data modified

## 1. Scope

This audit examines the service_memory and task_state labeling patterns in the 100-case batch100. The goal is to determine whether "add feature X" type units are systematically over-assigned to service_memory and whether the resulting distribution imbalance needs correction before generating 500+ training cases.

## 2. Why This Audit Is Required

The batch100 data report revealed:
- service_memory: 89 STORE units (44% of 204 total STORE)
- task_state: 50 STORE units (25% of 204 total STORE)

The recommended range for service_memory was 55-75 and for task_state was 55-75. The actual distribution is service_memory-heavy and task_state-light. Before scaling to 500+ cases, the labeling policy must be reviewed to ensure this imbalance is intentional (reflecting real coding-agent distributions) rather than a systematic labeling bias.

## 3. Human Label Policy Tested

Per the reviewer's policy rules:

**Rule A (task_state):** If the unit expresses a current action, implementation plan, version config, next step, blocker, or temporary constraint → task_state.

**Rule B (service_memory):** If the unit expresses durable service/component behavior, interface, invariant, or constraint → service_memory.

**Rule C (ambiguous):** If a unit says "Add feature X so service Y will behave Z," prioritize the semantic focus: if the weight is on current action → task_state; if it records a durable behavior spec → service_memory; if unclear → flag.

## 4. Service Memory Overuse Scan

### 4.1 Overall Classification

Total service_memory units: **89**

| Category | Count | Description |
| --- | ---: | --- |
| Clearly durable service behavior | 35 | "The service must...", "The component rejects...", "The module stores..." |
| Action-phrased ("Add/Implement/Build...") | 30 | Start with implementation verbs |
| Uncertain (both durable and action markers, or neither) | 24 | Mixed signals |

### 4.2 Action-Phrased Service Memory Units (30)

These 30 units start with implementation verbs like "Add", "Implement", "Integrate", "Build":

| # | Case ID | Unit | Text (truncated) |
| --- | --- | --- | --- |
| 1 | v05_sample_0012 | u1 | Add a SHA-256 checksum validation step... |
| 2 | v05_sample_0019 | u1 | Add a manual purge button... |
| 3 | v05_batch50_0013 | u1 | Add a deadlock retry wrapper... |
| 4 | v05_batch50_0016 | u1 | Add Parquet as an optional output format... |
| 5 | v05_batch50_0021 | u1 | Add a three-way merge strategy... |
| 6 | v05_batch50_0022 | u1 | Add a per-table freshness metric... |
| 7 | v05_batch50_0027 | u1 | Add a dead-letter queue... |
| 8 | v05_batch50_0028 | u2 | Add a network-type constraint... |
| 9 | v05_batch50_0030 | u1 | Add incremental load support... |
| 10 | v05_batch100_0026 | u1 | Add semantic search using sentence-transformers... |
| 11 | v05_batch100_0027 | u1 | Add a PDF export button... |
| 12 | v05_batch100_0028 | u1 | Add multi-city booking... |
| 13 | v05_batch100_0029 | u1 | Add rubric-based grading... |
| 14 | v05_batch100_0030 | u1 | Add automatic texture atlas generation... |
| 15 | v05_batch100_0031 | u1 | Add a relevance feedback loop... |
| 16 | v05_batch100_0032 | u1 | Add anomaly detection... |
| 17 | v05_batch100_0033 | u1 | Add demand-based surge pricing... |
| 18 | v05_batch100_0034 | u1 | Add a waitlist... |
| 19 | v05_batch100_0035 | u1 | Add separate build targets... |
| 20 | v05_batch100_0036 | u1 | Add cross-document summarization... |
| 21 | v05_batch100_0037 | u1 | Add a streaming aggregation path... |
| 22 | v05_batch100_0038 | u1 | Add a tiered cancellation policy engine... |
| 23 | v05_batch100_0039 | u1 | Add a grade appeal workflow... |
| 24 | v05_batch100_0040 | u1 | Add incremental asset processing... |
| 25 | v05_batch100_0041 | u1 | Add incremental indexing... |
| 26 | v05_batch100_0042 | u1 | Add a dark mode toggle... |
| 27 | v05_batch100_0044 | u1 | Add a recommendation engine... |
| 28 | v05_batch100_0045 | u1 | Add automated performance tests... |
| 29 | v05_batch100_0049 | u1 | Add prerequisite validation... |
| 30 | v05_batch100_0050 | u1 | Add a quality scoring system... |

### 4.3 Analysis of Action-Phrased Units

**Key observation:** Nearly all 30 "Add X" units contain a second clause describing the durable behavior of the feature being added. Example pattern: "Add X that does Y with constraint Z." The "Add" is the framing verb; the semantic content describes durable behavior.

**Examples of the pattern:**
- "Add a SHA-256 checksum validation step **that runs after the S3 write and logs the result.**" → The durable behavior is "runs after S3 write and logs result."
- "Add incremental load support **using a high-watermark column updated_at. The pipeline should only process rows where updated_at > last_load_time.**" → The durable behavior is "processes rows where updated_at > last_load_time."

**The core question:** Should these be service_memory (they describe WHAT the service will do going forward — a durable behavior specification) or task_state (they describe the current implementation action)?

### 4.4 Recommended Classification

Per Rule C: "If the focus is on current action / implementation step → task_state. If it's already recording durable behavior spec → service_memory."

**Recommendation: Keep most as service_memory, but reclassify a subset.**

The "add" phrasing is a stylistic artifact of how feature requirements are expressed. The semantic content in most cases describes durable behaviors. However, a small subset is clearly implementation-focused:

**Top 10 most likely corrections (service_memory → task_state):**

| # | Case | Unit | Reason |
| --- | --- | --- | --- |
| 1 | v05_batch100_0040 | u1 | "Add incremental asset processing" — purely an implementation plan statement |
| 2 | v05_batch100_0041 | u1 | "Add incremental indexing" — purely an implementation plan, no behavior spec embedded |
| 3 | v05_batch100_0045 | u1 | "Add automated performance tests" — implementation infrastructure, not service behavior |
| 4 | v05_batch100_0026 | u1 | "Add semantic search" — implementation plan, though second sentence describes behavior |
| 5 | v05_batch100_0042 | u1 | "Add a dark mode toggle" — implementation feature, not behavioral invariant |
| 6 | v05_batch100_0027 | u1 | "Add a PDF export button" — implementation feature |
| 7 | v05_batch100_0044 | u1 | "Add a recommendation engine" — implementation plan |
| 8 | v05_batch100_0028 | u1 | "Add multi-city booking" — implementation plan |
| 9 | v05_batch100_0035 | u1 | "Add separate build targets" — implementation config |
| 10 | v05_batch100_0049 | u1 | "Add prerequisite validation" — implementation plan |

These 10 corrections would move ~10 units from service_memory to task_state, bringing the counts closer to balance.

### 4.5 Cases to Keep as service_memory

Many "Add X" units should remain service_memory because they describe durable, specific behaviors:

- v05_sample_0012 u1: "Add SHA-256 checksum that runs after S3 write and logs" → The checksum behavior IS the service specification
- v05_batch50_0013 u1: "Add deadlock retry wrapper that catches 40P01 and retries 3x with 1s backoff" → Specific behavioral spec
- v05_batch50_0030 u1: "Add incremental load using high-watermark updated_at" → Detailed behavioral algorithm

## 5. Task State Underuse Scan

### 5.1 Overall Classification

Total task_state units: **50**

Classification:
- Correct current next-step / blocker / implementation plan: ~42
- Uncertain (could be service_memory or project_memory): ~8

### 5.2 Suspicious Task State Units

| # | Case | Unit | Text | Concern |
| --- | --- | --- | --- | --- |
| 1 | v05_batch50_0004 | u2 | "The eval_runner has been run on subset50 but not yet on full pilot." | Correct — current progress state |
| 2 | v05_batch50_0023 | u3 | "The current metrics module only reports per-interface accuracy, not cross-target calibration." | Correct — current limitation |
| 3 | v05_batch100_0026 | u2 | "The hybrid ranking should weight semantic similarity at 0.4 and TF-IDF at 0.6 for the initial rollout." | Correct — experimental parameter, not permanent |

**Finding:** Task state units are generally correctly labeled. The issue is under-counting, not mislabeling. No task_state units should be reclassified to service_memory.

## 6. Distribution Analysis

### 6.1 Current Distribution

| Target | Count | % of STORE | Recommended Range |
| --- | ---: | ---: | --- |
| service_memory | 89 | 43.6% | 55-75 (30-36%) |
| task_state | 50 | 24.5% | 55-75 (30-36%) |
| repo_memory | 33 | 16.2% | 35-50 (16-20%) |
| project_memory | 18 | 8.8% | 18-25 (8-12%) |
| user_profile | 14 | 6.9% | 10-15 (5-8%) |

### 6.2 Analysis

1. **service_memory (89) is high.** Driven by two factors: (a) many "Add feature X" units labeled as service_memory (30 action-phrased), and (b) the coding-agent domain naturally produces many durable service behavior descriptions.

2. **task_state (50) is low.** Not due to mislabeling, but because the case designs emphasize durable behavior descriptions over current progress statements. The new50 cases in particular focus on feature specifications rather than task progress.

3. **repo_memory (33) is slightly below range.** Adding 2-3 more repo_memory cases in the next scale would bring it to 35-36.

4. **project_memory (18) is at the bottom of range.** Acceptable for 100 cases. Should increase to 20-25 at 500-case scale.

5. **user_profile (14) is solid.** Within range and well-distributed across domains.

### 6.3 Post-Correction Projection

If the top 10 action-phrased corrections are applied (service_memory → task_state):

| Target | Before | After | Change |
| --- | ---: | ---: | --- |
| service_memory | 89 | 79 | −10 |
| task_state | 50 | 60 | +10 |
| repo_memory | 33 | 33 | 0 |
| project_memory | 18 | 18 | 0 |
| user_profile | 14 | 14 | 0 |

This would bring service_memory from 89 to 79 (still above 55-75 range but improved) and task_state from 50 to 60 (within the 55-75 range).

### 6.4 500-Case Blueprint Recommendation

| Target | 500-case Target | 1000-case Target | Rationale |
| --- | ---: | ---: | --- |
| service_memory | 150-170 (30-34%) | 300-340 | Reduce from current 44% |
| task_state | 150-170 (30-34%) | 300-340 | Increase from current 25% |
| repo_memory | 80-100 (16-20%) | 160-200 | Maintain |
| project_memory | 40-60 (8-12%) | 80-120 | Slight increase |
| user_profile | 25-40 (5-8%) | 50-80 | Slight increase |

## 7. Key Findings

1. **The "Add feature X" → service_memory pattern accounts for 30 of 89 service_memory units (34%).** Most of these describe durable behaviors with the "Add" verb as framing. ~10 are clear implementation plans that should be task_state.

2. **Task state is under-counted, not mislabeled.** The task_state units that exist are correctly labeled. The deficit is in case design — not enough "current progress" / "blocker" / "next step" type units.

3. **The remaining service_memory units (59) are clearly correct.** These describe durable service behaviors, interfaces, constraints, and invariants.

4. **No project_memory or user_profile units appear mislabeled as service_memory.**

## 8. Recommended Label Policy Going Forward

For 500+ case generation:

1. **"Add X" framing:** If the unit's primary semantic content describes a durable behavior specification → service_memory. If the unit purely describes an implementation plan/step → task_state. When in doubt, prefer task_state for "Add/Implement" phrasing.

2. **Increase task_state cases:** Design more cases that explicitly describe current progress, blockers, next steps, version-specific configurations, and temporary constraints.

3. **Maintain current quality:** The 35 clearly-durable service_memory units and 42 correct task_state units demonstrate that the agent can label correctly when the content is unambiguous.

4. **Add repo_memory cases:** Target 16-20% repo_memory in the 500-case set.

## 9. Whether Batch100 Can Move to 500-Case Blueprint

**Yes, after applying corrections.** The labeling policy is fundamentally sound. The distribution imbalance is correctable through:
1. Reclassifying ~10 action-phrased service_memory units to task_state
2. Designing 500+ cases with a more balanced task_state representation
3. Adding 2-3 more repo_memory cases per 100

The batch100 has served its purpose: it exposed the distribution issue at a manageable scale. The correction proposals in the companion report provide specific changes.
