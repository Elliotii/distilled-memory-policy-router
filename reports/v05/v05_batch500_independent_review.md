# V0.5 Batch500 Rebalanced — Independent Review Report

**Reviewer:** Independent review (read-only)  
**Date:** 2026-06-02  
**Scope:** 500 rebalanced training-pool cases  
**Status:** No files modified; no new cases generated; no model API called  

---

## 1. Executive Summary

**Recommendation: APPROVE WITH MINOR NOTES** → proceed to dev/gold construction after addressing 4 labeling concerns.

The rebalanced batch500 meets all blueprint distribution targets, passes all structural validations, contains no sensitive data in STORE, and has a healthy shape distribution. The 50 replacement cases are substantially better than the service-heavy originals they replaced. I found **4 labeling errors** and **2 template-pattern concerns** worth noting, but **no blockers**. The dataset is training-ready.

---

## 2. Blockers Found

| Blockers | Count |
|----------|:-----:|
| Critical (stop) | **0** |
| High (must fix before training) | **0** |
| Medium (should fix) | **4** |
| Low (consider fixing) | **2** |

**No critical or high-severity blockers were found.**

---

## 3. Target Distribution

| Target | Count | % | Blueprint | Status |
|--------|:-----:|:--:|:---------:|:------:|
| service_memory | 324 | 31.2% | 30-34% | ✓ |
| task_state | 336 | 32.3% | 30-34% | ✓ |
| repo_memory | 200 | 19.2% | 16-20% | ✓ |
| project_memory | 122 | 11.7% | 10-14% | ✓ |
| user_profile | 58 | 5.6% | 5-8% | ✓ |
| **Total STORE** | **1040** | — | — | — |

**svc:task gap:** -1.1pp (task_state slightly ahead — well within tolerance)  

**Verdict:** All five targets are within blueprint ranges. The rebalance successfully corrected the original service_memory overshoot (39.1% → 31.2%) while adding project_memory and user_profile coverage. The distribution is healthy and will not bias LoRA training toward any single target.

---

## 4. Shape Distribution

| Shape | Count | % | Blueprint | Status |
|-------|:-----:|:--:|:---------:|:------:|
| READ+STORE joint | 213 | 42.6% | 38-45% | ✓ |
| STORE/SKIP-only | 182 | 36.4% | 35-40% | ✓ |
| READ-only | 105 | 21.0% | 18-22% | ✓ |

**Verdict:** Shape distribution is within all ranges. Good diversity of input formats.

---

## 5. Replacement 50 — Quality Audit

### 5.1 Summary

| Metric | Value |
|--------|-------|
| Total replaced | 50 cases |
| service_memory units among replacements | 1 unit (v05_batch500_0125 u1 — correct) |
| project_memory units added | ~41 |
| user_profile units added | ~19 |
| repo_memory units added | ~33 |
| task_state units in replacements | ~35 |

### 5.2 Template Pattern Assessment

**Finding:** 19 of 50 replacement cases (38%) share a common structural pattern:

```
u1: "All <project> services must <cross-service rule>"
u2: "The <project> project requires/prohibits/does not <project-wide policy>"  
u3: "<action task> before <deadline>" or "<config path statement>"
```

**Assessment:** This is a **moderate concern**, not a blocker. Specifically:

- **Content diversity is real:** The 19 cases span 12+ distinct project domains (analytics-dashboard, travel-planner, ecommerce-platform, customer-support, healthcare-admin, etc.), each with genuinely different rules (data retention, accessibility, GDPR, auth standards, PII masking, access control, HIPAA, data usage, pricing, cancellation, academic integrity, QA standards, SOC 2, model risk, ToS enforcement, AI ethics, data export rights, data classification, sustainability).
- **No fill-in-the-blank:** The unit texts are fully written, not templated with placeholders. No two units are identical.
- **Training concern:** 19/500 = 3.8% of total cases follow this exact structure. The model may learn a spurious "project_memory + project_memory + task_state" → "compliance policy domain" correlation, but the effect is diluted by the other 481 cases.
- **Mitigation:** The replacement cases only changed 50/500 cases (10%). The remaining 450 cases have diverse structural patterns.

**Verdict:** Not a blocker. The replacement cases successfully achieve their distribution goals without template abuse.

### 5.3 Replacement Case — project_memory Audit

Every project_memory unit in the 50 replacement cases was manually reviewed. Key findings:

- **Cross-service rules dominate:** Almost all project_memory units begin with "All <project> services must..." or use explicit multi-service language. This is exactly what the label policy requires.
- **Scope exclusions are correct:** u2 patterns like "The <project> project does not..." describe permanent scope decisions → correct project_memory.
- **Compliance/safety policies are correct:** GDPR, HIPAA, SOC 2, sustainability, AI ethics policies are all correctly labeled as project_memory.
- **One borderline case:** v05_batch500_0002 u2 ("The retention policy applies uniformly to the query engine, alert manager, and report scheduler services.") — the automated scan flagged it as "single-service but labeled project_memory." However, it explicitly names three services, making it genuinely cross-service → **correctly labeled**.

**Verdict:** project_memory labeling in replacement cases is **high quality**. No evidence of overuse or catch-all abuse.

---

## 6. user_profile / Sensitive Audit

### 6.1 user_profile Quality

All 58 user_profile units across the full batch500 were audited. Key findings:

- **All are stable, non-sensitive preferences:** Currency display, notification schedule, sort order, report grouping, editor theme, diagram notation, search result ordering, QA workflow preferences.
- **No sensitive data stored as user_profile:** Zero cases of email addresses, phone numbers, or identifiers stored as user_profile.
- **3 keyword-flagged cases (false positives):** Three units contain the word "email" but describe email *preferences* (digest frequency, format preference), not email addresses → correctly labeled user_profile.

**Verdict:** user_profile units are high quality and correctly labeled.

### 6.2 Sensitive Content Scan

Full keyword scan across all 500 cases:

| Finding | Count | Status |
|---------|:-----:|--------|
| Actual sensitive data STOREd | **0** | ✓ |
| Sensitive data correctly SKIPped | 8 | ✓ |
| Policy/rules about sensitive data handling STOREd (false positive keywords) | ~15 | ✓ |

All sensitive content is correctly SKIPped:
- Passwords, API test keys, personal emails, phone numbers, credit card numbers, recovery codes → all SKIPped.
- The "false positive" cases (e.g., "All shopengine services must validate JWT tokens" → project_memory, "The orders service must tokenize payment information" → service_memory) are policies/procedures *about* sensitive data, not actual sensitive data. These are correctly STOREd per the label policy.

**Verdict:** Sensitive content handling is **correct**. Zero real secrets stored.

---

## 7. repo_memory Audit

### 7.1 Overall Quality

200 repo_memory units across 500 cases. Most have clear path, command, file convention, or directory structure markers.

### 7.2 Borderline Cases

Approximately 30-35 repo_memory units (15-18%) lack explicit path/command/directory markers. These describe:
- CI pipeline steps, build conventions, code review norms
- Deployment procedures, release tagging conventions
- Incident response procedures, on-call escalation rules

**Assessment:** Most of these are defensible as repo_memory under the definition "Repository-specific facts: paths, commands, directory structure, **test conventions, code norms**." The label policy explicitly calls out "code norms" and "test conventions" as repo_memory territory. CI, build, review, and deployment conventions fall under this.

However, a few cases stretch this definition:
- Incident/escalation procedures (v05_batch500_0091 u1, v05_batch500_0119 u2) describe operational processes more than repo-specific conventions.
- These are **borderline but not incorrect** — they could also be labeled project_memory.

**Verdict:** repo_memory quality is **acceptable**. Some borderline cases exist but don't violate the label policy.

---

## 8. service_memory vs task_state Audit

### 8.1 "Add/Implement/Build..." Rule Compliance

The label policy specifies: `"Add" / Implement / Integrate / Build / Update / Draft / Next / Currently missing / For this version → usually task_state`

**Key finding:** v05_batch100_0039 u1 violates this rule:
- `"Add a grade appeal workflow where students can submit an appeal within 14 days of grade posting with a written justification."` → labeled **service_memory**
- Per the label policy's explicit rule, "Add" phrasing → task_state
- The unit does describe a detailed workflow, but the "Add" framing dominates
- **This is a labeling error.**

Another concern: v05_batch50_0014 u3:
- `"Add a priority field to the notification payload schema in the API docs."` → labeled **repo_memory**
- "Add" phrasing → should be task_state
- **This is a labeling error.**

### 8.2 Durable Behavior vs Action Tasks

The boundary between service_memory (durable behavior) and task_state (current progress) is generally handled well. Cases like:
- "The notification service must deduplicate messages by notification_id within a 5-minute window." → service_memory ✓
- "Run the disaster recovery drill before peak holiday season." → task_state ✓

are consistently correct.

### 8.3 batch300 service_memory-heavy cases

Two non-replacement cases have 3 service_memory units each:
- **v05_batch100_0039** (education-platform/grading): 3 service_memory. u1 has the "Add..." issue noted above.
- **v05_batch300_0075** (mobile-field/camera): 3 service_memory — all genuinely describe durable camera permission UX behavior. Correctly labeled.

**Verdict:** The service_memory vs task_state boundary is well-maintained, with 2 exceptions noted above.

---

## 9. Template / Duplication Audit

### 9.1 Exact Duplicates

| Type | Content | Cases | Severity |
|------|---------|-------|----------|
| Candidate memory | "The case validator checks that every current unit appears exactly once in gold.store or gold.skip." | v05_batch50_0003 m1, v05_batch300_0001 m1 | **Low** — cross-batch duplicate. Both are in the training pool, which means the model sees this twice. Acceptable for training but noted. |
| Current unit | "The project scope explicitly excludes retriever training, writer training, and MemoryOS implementation." | v05_batch50_0009 u1, v05_batch500_0096 u1 | **Low** — this is a genuine project-scope statement that could reasonably appear in different contexts (memory-router project). The two cases have different surrounding content. Minor concern. |

### 9.2 Unit Text Prefix Similarity

3 repeated prefixes found in replacement cases:
- `"The finboard project requires that..."` (2x — different rules)
- `"All shopengine customer-facing services must..."` (2x — different rules)
- `"The metricboard project requires that..."` (2x — different rules)

These all come from same-domain cases with genuinely different content. Not a template concern.

**Verdict:** Duplication is minimal and acceptable. No evidence of lazy copy-paste.

---

## 10. SFT Format Audit

| Check | Result |
|-------|--------|
| 3 messages (system/user/assistant) per entry | 500/500 ✓ |
| Correct roles | 500/500 ✓ |
| Assistant content == gold.dsl | 500/500 ✓ |
| No markdown in assistant | 500/500 ✓ |
| No JSON in assistant | 500/500 ✓ |
| All DSL lines start with READ/STORE/SKIP | 500/500 ✓ |

Also verified:
- All unit IDs appear exactly once across STORE + SKIP
- DSL parsing matches structured gold fields

**Verdict:** SFT format is **clean**. Ready for training.

---

## 11. Additional Findings

### 11.1 v05_batch500_0096 u3 and v05_batch500_0097 u3 — SKIP of path units

- v05_batch500_0096 u3: `"The documentation for exclusion decisions lives under docs/v05/scope_exclusions.md."` → **SKIPped**
- v05_batch500_0097 u3: `"The roadmap document is tracked in docs/planning/roadmap_2026_Q3.md."` → **SKIPped**

Both units contain explicit file path information that matches the repo_memory definition. Should be labeled repo_memory instead of SKIP. These appear to have been SKIPped because the surrounding context (out-of-scope skill proposals) led the labeler to SKIP the entire case. However, each unit should be judged independently.

**Verdict:** 2 labeling errors — should be repo_memory.

### 11.2 batch300 false positive confirmation

Confirmed that the 5 batch300 cases flagged by keyword-based sensitive check in the rebalance report are genuinely storing policies/procedures about sensitive data — not actual sensitive data. These were previously reviewed and accepted.

### 11.3 Domain coverage

17 project domains represented. Good coverage across the blueprint's existing and new domains:
- Top: customer-support (46), analytics-dashboard (45), ecommerce-platform (44)
- Bottom: creator-tools (13), supply-chain (13), healthcare-admin (13), legal-docs (12)
- healthcare-admin and legal-docs have fewer cases but are niche domains with strong sensitive-boundary value.

---

## 12. Top 10 Cases for Human Review

| # | Case ID | Unit | Current Label | Concern | Proposed Correction | Confidence |
|---|---------|------|---------------|---------|---------------------|------------|
| 1 | v05_batch100_0039 | u1 | service_memory | "Add a grade appeal workflow..." — "Add" phrasing → task_state per label policy §7 | task_state | High |
| 2 | v05_batch50_0014 | u3 | repo_memory | "Add a priority field to the notification payload schema in the API docs." — "Add" phrasing → task_state | task_state | High |
| 3 | v05_batch500_0096 | u3 | SKIP | "The documentation for exclusion decisions lives under docs/v05/scope_exclusions.md." — contains explicit path → repo_memory | repo_memory | High |
| 4 | v05_batch500_0097 | u3 | SKIP | "The roadmap document is tracked in docs/planning/roadmap_2026_Q3.md." — contains explicit path → repo_memory | repo_memory | High |
| 5 | v05_batch500_0062 | u2 | repo_memory | "Secrets such as database passwords and API keys must never appear in config files" — config file convention (repo) vs project-wide policy (project). Borderline. | Keep repo_memory or change to project_memory | Medium |
| 6 | v05_batch200_0039 | u2 | repo_memory | "Report permissions are managed in the dashboard_permissions table with columns..." — describes data schema/behavior, not path/command/convention | service_memory | Medium |
| 7 | v05_batch500_0091 | u1 | repo_memory | "Security incidents must be reported within 15 minutes by posting in #security-incidents Slack channel" — operational process, more project-level than repo-level | project_memory | Medium |
| 8 | v05_batch500_0119 | u2 | repo_memory | "Production incidents must be acknowledged within 5 minutes..." — cross-service SLA procedure | project_memory | Medium |
| 9 | v05_batch500_0096 | u2 | SKIP | "We should create a reusable skill system for SOPs..." — This is a speculative proposal, correct to SKIP. But the same case also has u3 issue (see #3). | Keep SKIP | — (context for #3) |
| 10 | v05_batch50_0003 + v05_batch300_0001 | m1 | service_memory | Exact duplicate candidate memory across two cases. Not an error but worth noting for data quality. | Consider deduping or accepting as training variation | Low |

---

## 13. Detailed Case Analysis (for each medium+ concern)

### Case 1: v05_batch100_0039 u1

```
case_id: v05_batch100_0039
unit_id: u1
current_label: service_memory
concern: The unit begins with "Add a grade appeal workflow where students can submit
          an appeal within 14 days of grade posting with a written justification."
          The label policy §7 states: "Add / Implement / Integrate / Build / Update →
          usually task_state." While the unit contains durable behavior detail (14-day
          window, written justification), the dominant semantic frame is an "Add..."
          implementation action.
proposed_correction: task_state
confidence: High
notes: u2 ("Appeals must be reviewed by a different instructor...") and u3 ("All grade
       changes from appeals must be logged to grade_audit...") are correctly labeled
       service_memory. Only u1 needs correction.
```

### Case 2: v05_batch50_0014 u3

```
case_id: v05_batch50_0014
unit_id: u3
current_label: repo_memory
concern: "Add a priority field to the notification payload schema in the API docs."
          "Add..." phrasing is a clear task_state indicator per §7. There is no
          path/command/directory convention in this unit — it's an implementation
          action.
proposed_correction: task_state
confidence: High
```

### Case 3: v05_batch500_0096 u3

```
case_id: v05_batch500_0096
unit_id: u3
current_label: SKIP
concern: "The documentation for exclusion decisions lives under
          docs/v05/scope_exclusions.md." This is a clear file path, matching the
          repo_memory definition: "WHERE things live (paths, file locations)."
          Should be STOREd as repo_memory.
proposed_correction: repo_memory
confidence: High
```

### Case 4: v05_batch500_0097 u3

```
case_id: v05_batch500_0097
unit_id: u3
current_label: SKIP
concern: "The roadmap document is tracked in docs/planning/roadmap_2026_Q3.md."
          Same pattern as case 3 — explicit file path that should be repo_memory.
proposed_correction: repo_memory
confidence: High
```

---

## 14. Final Recommendation

**APPROVE WITH MINOR NOTES** — proceed to dev/gold construction.

### Rationale:

1. **Distribution is healthy:** All 5 targets within blueprint ranges. svc:task gap is negligible (-1.1pp).
2. **Shape distribution is healthy:** All 3 shapes within ranges.
3. **No sensitive data stored:** 100% of sensitive units correctly SKIPped.
4. **SFT format is clean:** 500/500 format checks pass.
5. **Label quality is high:** Only 4 clear labeling errors found across 1040 STORE decisions (~0.4% error rate).
6. **Replacement cases are quality:** They add genuine project_memory, user_profile, and repo_memory diversity without template abuse.
7. **6 borderline cases** exist that could benefit from human judgment, but none are clearly wrong.

### Actions before dev/gold construction:

**Must do:**
- [ ] Fix 4 labeling errors (cases 1-4 above)
- [ ] Run `validate_jsonl_file` on corrected batch500

**Should do:**
- [ ] Human review cases 5-8 (borderline repo_memory vs project_memory/service_memory)
- [ ] Review the 2 duplicate content instances — decide whether to deduplicate or accept

**Consider:**
- [ ] The 19 structurally-similar replacement cases are acceptable but worth noting in training documentation
- [ ] Add a note in the dataset card about the rebalancing methodology

### No-Go conditions checked — ALL CLEAR:

| No-Go Condition | Status |
|-----------------|--------|
| Label policy violations >5% | ✗ (actual: ~0.4%) |
| Sensitive content in STORE | ✗ (0 found) |
| Distribution collapse | ✗ (all within range) |
| SFT format corruption | ✗ (500/500 clean) |

---

*End of independent review.*
