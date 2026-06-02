# V0.5 Batch100 Service vs Task Review

Date: 2026-06-01  
Context: 5.0-F2 — service vs task boundary review  
Status: Agent-generated; no data modified

## 1. Full Review: v05_batch100_0012

### Case Details

| Field | Value |
| --- | --- |
| **case_id** | v05_batch100_0012 |
| **source** | new50 |
| **project** | finance-dashboard |
| **service** | aggregator |
| **task** | record aggregator data quality rules |

**Current Units:**
- u1: "The aggregator must reject any input row where the transaction amount is negative and not flagged as a refund." → service_memory
- u2: "The aggregator currently processes data in hourly batches but does not yet handle late-arriving data." → task_state
- u3: "The finance-dashboard project must comply with SOC 2 data integrity requirements for all financial reports." → project_memory

**Gold DSL:** `READ NONE\nSTORE service_memory u1\nSTORE task_state u2\nSTORE project_memory u3\nSKIP NONE`

### Why Medium-Risk

The risk is about u3: is "SOC 2 compliance" correctly project_memory?

### Target-Boundary Analysis

**u1 → service_memory:** Clearly correct. "The aggregator must reject..." defines a specific data validation rule for the aggregator service. This is a durable component behavior.

**u2 → task_state:** Clearly correct. "currently processes... but does not yet handle..." describes current implementation state and a known gap. This is current progress/limitation.

**u3 → project_memory:** The key question. "The finance-dashboard project must comply with SOC 2 data integrity requirements for all financial reports."

Arguments for project_memory:
- SOC 2 compliance applies across the entire project, not a single service
- It's a regulatory requirement that shapes all services' design
- The text says "for all financial reports" — cross-cutting scope

Arguments against project_memory:
- Could be seen as a task constraint ("must comply" = current requirement)
- SOC 2 is a compliance standard, which could be project-level infrastructure

**Verdict:** project_memory is correct. SOC 2 compliance is a project-level regulatory requirement that transcends any single service. It's analogous to "the project uses synthetic data only" or "the project does not implement MemoryOS" — both confirmed as project_memory in prior reviews.

**Recommendation:** **Keep u3 as project_memory.** Confidence: High.

### Human Decision Required

No. This case is correctly labeled. The medium-risk flag was overly conservative.

---

## 2. Full Review: v05_batch100_0047

### Case Details

| Field | Value |
| --- | --- |
| **case_id** | v05_batch100_0047 |
| **source** | new50 |
| **project** | finance-dashboard |
| **service** | alerts |
| **task** | record alert suppression rules |

**Current Units:**
- u1: "All finboard services must suppress non-critical alerts during the monthly maintenance window from 02:00-04:00 UTC on the first Sunday." → project_memory
- u2: "Critical PagerDuty alerts must never be suppressed, even during maintenance windows." → project_memory
- u3: "Add the monthly maintenance suppression rule to the alerts configuration before the next maintenance window." → task_state

**Gold DSL:** `READ m1\nSTORE project_memory u1\nSTORE project_memory u2\nSTORE task_state u3\nSKIP NONE`

### Why Medium-Risk

The risk is about u2: is "Critical PagerDuty alerts must never be suppressed" correctly project_memory?

### Target-Boundary Analysis

**u1 → project_memory:** Clearly correct. "All finboard services must..." is explicitly cross-service. The maintenance window policy applies project-wide.

**u2 → project_memory:** The key question. "Critical PagerDuty alerts must never be suppressed, even during maintenance windows."

Arguments for project_memory:
- This is a permanent safety policy: critical alerts should ALWAYS fire
- It applies across ALL services (not just the alerts service)
- "even during maintenance windows" shows it overrides the cross-service u1 rule
- It's a project-level design principle about alert reliability

Arguments for service_memory:
- PagerDuty is a specific tool/ integration → could be service-specific behavior
- The alerts service handles PagerDuty — this could be an alerts-service rule

**Verdict:** project_memory is correct. The rule "critical alerts must never be suppressed" is a project-level safety policy that applies regardless of which service generates the alert. It's NOT about how the alerts service works internally — it's about what the project guarantees about alert delivery.

**u3 → task_state:** Clearly correct. "Add the rule to configuration before next window" is an implementation task with a deadline.

**Recommendation:** **Keep u2 as project_memory.** Confidence: High.

### Human Decision Required

No. This case is correctly labeled. The medium-risk flag was overly conservative.

---

## 3. Top Suspicious Service/Task Boundary Cases

These are cases where the service_memory vs task_state boundary is genuinely debatable:

### 3.1 v05_batch100_0040 (game-studio)

- u1: "Add incremental asset processing: only rebuild assets whose content hash has changed since the last build." → service_memory
- u3: "Run a full rebuild after implementing incremental processing to establish the baseline content hashes." → task_state

**Analysis:** u1 says "Add" — this is an implementation plan statement. The second clause describes the behavior. Per Rule C, this is ambiguous. The "Add" framing suggests task_state; the behavioral description suggests service_memory.

**Recommendation:** Flag as uncertain. Reviewer should decide. Leaning toward task_state because the "Add" verb is the primary framing. (Included in top 10 corrections.)

### 3.2 v05_batch100_0041 (docs-assistant)

- u1: "Add incremental indexing that only processes documents changed since the last indexed commit." → service_memory

**Analysis:** Pure implementation plan statement. No durable behavioral specification embedded. The incremental behavior is implied but the sentence is about the implementation action.

**Recommendation:** Change to task_state. (Included in top 10 corrections.)

### 3.3 v05_batch100_0042 (finance-dashboard)

- u1: "Add a dark mode toggle that switches all chart colors to a dark palette with light text and muted gridlines." → service_memory

**Analysis:** "Add a toggle" is implementation-focused. The color scheme description is behavioral but the framing is implementation.

**Recommendation:** Change to task_state. (Included in top 10 corrections.)

### 3.4 v05_batch100_0026 (docs-assistant)

- u1: "Add semantic search using sentence-transformers to augment the existing TF-IDF results with a hybrid ranking." → service_memory
- u2: "The hybrid ranking should weight semantic similarity at 0.4 and TF-IDF at 0.6 for the initial rollout." → task_state

**Analysis:** u1 → service_memory is debatable but defensible (describes a durable new search capability). u2 → task_state is clearly correct ("for the initial rollout" = temporary/experimental). The contrast between u1 and u2 in the same case shows good labeling practice.

**Recommendation:** Keep u1 as service_memory (not in top 10). The hybrid ranking capability IS a durable behavior, even if the specific weights are experimental.

---

## 4. New Domain Quality Spot-Check

### 4.1 docs-assistant (12 cases)

**Reviewed:** v05_batch100_0001, 0004, 0011, 0014, 0019, 0024, 0026, 0031, 0036, 0041, 0046

**Assessment:**
- Domain is synthetic and safe (documentation search/index/summarize assistant)
- Memory targets make sense (indexer behavior → service, config paths → repo, scope decisions → project)
- Cases show good variety: READ-only debugging queries, STORE/SKIP scope decisions, READ+STORE feature additions
- Not too template-like; different service components (indexer, search, summarizer) provide variety
- **Should remain in 500-case data.** Provides good coverage of documentation-domain scenarios.

**Concerns:** Minor. Some "Add X" cases follow the same pattern. Recommend varying the framing in future cases.

### 4.2 finance-dashboard (12 cases)

**Reviewed:** v05_batch100_0002, 0005, 0010, 0012, 0015, 0020, 0025, 0027, 0032, 0037, 0042, 0047

**Assessment:**
- Domain is synthetic and safe (financial dashboard with aggregator, visualizer, alerts services)
- Memory targets make sense: revenue alerts → service, TLS policy → project, config paths → repo
- Good target-boundary cases: 0012 (SOC2), 0015 (TLS 1.3 cross-service vs visualizer-specific), 0047 (maintenance suppression)
- **Should remain in 500-case data.** Provides strong project_memory examples.

**Concerns:** None significant. The finance domain naturally generates cross-service compliance cases.

### 4.3 travel-planner (10 cases)

**Reviewed:** v05_batch100_0003, 0006, 0013, 0016, 0021, 0028, 0033, 0038, 0043, 0048

**Assessment:**
- Domain is synthetic and safe (flight booking/pricing/caching)
- Memory targets make sense: pricing cache behavior → service, fare rules → service, scope decisions → project
- Good user_profile cases: 0013 (sort by total price), 0043 (EUR currency, stops display)
- **Should remain in 500-case data.** Provides travel-domain variety.

**Concerns:** Some cases reference airline APIs and real-sounding terms (IATA, SendGrid). These are synthetic but should remain obviously fake.

### 4.4 education-platform (8 cases)

**Reviewed:** v05_batch100_0007, 0017, 0022, 0029, 0034, 0039, 0044, 0049

**Assessment:**
- Domain is synthetic and safe (course enrollment, grading, recommendations)
- Memory targets make sense: grading policies → service, enrollment validation → service, scope exclusions → project
- Good user_profile cases: 0022 (materials organization), 0029 (rubric breakdown), 0044 (instructor preferences)
- **Should remain in 500-case data.** Provides education-domain variety with strong user_profile coverage.

**Concerns:** Minor. Student IDs and test data are synthetic but could be more obviously fake (already use obvious placeholders like STUDENT-TEST-0001).

### 4.5 game-studio (8 cases)

**Reviewed:** v05_batch100_0008, 0018, 0023, 0030, 0035, 0040, 0045, 0050

**Assessment:**
- Domain is synthetic and safe (game asset pipeline, build system, texture compression)
- Memory targets make sense: asset validation → service, build conventions → repo, quality requirements → project
- Good repo_memory cases: 0018 (config path), 0023 (build artifact path, build conventions)
- **Should remain in 500-case data.** Provides game-dev domain variety.

**Concerns:** Minor. "Nintendo Switch" and "PlayStation 5" are real platform names but used generically. These are safe in a synthetic context but consider using fictional platform names in final training data to avoid any real-product associations.

## 5. Recommended Corrections Summary

### Critical (strongly recommended)
None. No critical mislabelings found.

### Medium (recommended for distribution balance)
Top 10 service_memory → task_state reclassifications (see corrections proposal report for exact DSL changes):

| # | Case | Unit | Current | Proposed |
| --- | --- | --- | --- | --- |
| 1 | v05_batch100_0040 | u1 | service_memory | task_state |
| 2 | v05_batch100_0041 | u1 | service_memory | task_state |
| 3 | v05_batch100_0045 | u1 | service_memory | task_state |
| 4 | v05_batch100_0026 | u1 | service_memory | task_state |
| 5 | v05_batch100_0042 | u1 | service_memory | task_state |
| 6 | v05_batch100_0027 | u1 | service_memory | task_state |
| 7 | v05_batch100_0044 | u1 | service_memory | task_state |
| 8 | v05_batch100_0028 | u1 | service_memory | task_state |
| 9 | v05_batch100_0035 | u1 | service_memory | task_state |
| 10 | v05_batch100_0049 | u1 | service_memory | task_state |

### Optional (reviewer's discretion)
~20 additional action-phrased service_memory units could be reclassified, but these are more defensible as durable behavior specifications. The agent recommends keeping them as service_memory.

## 6. Remaining Uncertainties

1. **"Add X" framing:** The boundary between "implementation plan" and "behavior specification" is inherently fuzzy. The reviewer should confirm whether the agent's preferred classification (keep most "Add X that does Y" as service_memory) is correct.
2. **Distribution balance:** Even with the 10 corrections, service_memory (79) would still be above task_state (60). Is this acceptable for the coding-agent domain, or should the ratio be closer to 1:1?
3. **batch100_0012 and 0047:** Agent recommends keeping both as-is. Reviewer should confirm these project_memory assignments.
