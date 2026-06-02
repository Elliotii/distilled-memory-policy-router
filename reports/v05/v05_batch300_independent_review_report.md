# Independent Review Report: v0.5 batch300

**Reviewer:** Independent audit (read-only)
**Date:** 2026-06-02
**Scope:** batch300 full audit — 300 cases, v05_batch300_cases.jsonl + v05_batch300_new100_cases.jsonl + v05_batch300_sft_messages.jsonl
**Question:** Can batch300 serve as seed for batch500?

---

## 1. Executive Summary

batch300 is structurally valid (300 SFT messages, 0 DSL mismatches, all `system/user/assistant` format) and all sensitive content is correctly SKIPped. However, **51% of the corrective new100 batch (51 of 100 cases) is template-generated** via domain-name substitution, which introduces a serious data quality concern. Additionally, 19 service_memory units use "Add" action-verb framing without durable-behavior markers, requiring case-by-case review.

**Overall verdict: CORRECTION REQUIRED BEFORE BATCH500.** The base structure is sound, but the template problem must be addressed before scaling to 500. Without correction, the model will learn to pattern-match on domain names rather than semantic target distinctions.

---

## 2. Blockers Found

| # | Blocker | Severity | Detail |
|---|---------|----------|--------|
| B1 | **Template-generated cases (51/100 corrective)** | HIGH | Cases v05_batch300_0050–0100 are fill-in-the-blank templates with only domain name swapped. 32 duplicate unit texts across cases. Risk: model learns domain-name gating instead of semantic routing. |
| B2 | **task_state overshoot at 36.5%** | MEDIUM | Blueprint targets 30-34%. The 36.5% is explained as "corrective overshoot" but exceeds the upper bound by 2.5pp. Batch500 must compensate. |
| B3 | **19 service_memory units with "Add" framing, no durable markers** | MEDIUM | Policy allows "Add" when behavioral detail dominates, but several cases (e.g., "Add a manual purge button", "Add a SHA-256 checksum validation step") have thin behavioral detail and may be more appropriate as task_state. |
| B4 | **Duplicate candidate_memory contents across cases** | LOW | 5 duplicate memory contents. Minor but indicates generation pipeline reuse without dedup. |
| B5 | **Real platform names in synthetic data** | LOW | "Slack", "GitHub", "OpenAI", "Stripe", "AWS", "Google" appear in unit text. Acceptable for synthetic scenarios but creates unnecessary real-world anchoring. |

---

## 3. Target Distribution Assessment

### Current vs Blueprint

| Target | batch300 Actual | Blueprint Target | In Range? |
|--------|:-:|:-:|:-:|
| service_memory | 165 (27.7%) | 30-34% | **BELOW** (-2.3pp) |
| task_state | 217 (36.5%) | 30-34% | **ABOVE** (+2.5pp) |
| repo_memory | 94 (15.8%) | 16-20% | **BELOW** (-0.2pp) |
| project_memory | 72 (12.1%) | 10-14% | IN RANGE |
| user_profile | 47 (7.9%) | 5-8% | **UPPER EDGE** (+0.9pp, borderline) |

**svc:task gap:** 8.7pp (near 8pp target). The data report's claim of "near 8pp target" is accurate.

### Shapes vs Blueprint

| Shape | batch300 Actual | Blueprint Target | In Range? |
|-------|:-:|:-:|:-:|
| READ-only | 75 (25.0%) | 15-20% | **ABOVE** (+5pp) |
| STORE/SKIP-only | 143 (47.7%) | 30-35% | **ABOVE** (+12.7pp) |
| READ+STORE joint | 82 (27.3%) | 45-50% | **BELOW** (-17.7pp) |

**The shape distribution is significantly off-target.** The corrective batch added 33 READ-only and 67 STORE/SKIP-only cases with 0 READ+STORE joint. This is consistent with the corrective strategy but creates a shape imbalance that batch500 must repair.

### Judgment

The distribution is **functional but not optimal**. The task_state overshoot is explained by the corrective strategy (counterbalancing a service_memory-heavy batch200 base). However:
- The task_state 36.5% represents a genuine overshoot, not just correction
- service_memory at 27.7% is now below target — the pendulum swung too far
- The READ+STORE joint shape (the most realistic operational pattern) is severely underrepresented at 27.3% vs 45-50% target
- user_profile is creeping toward the upper boundary

**For batch500:** Add ~30-40 service_memory units, ~10-15 READ+STORE joint cases, and keep task_state additions modest to bring both into range. Do not add more user_profile units.

---

## 4. service_memory vs task_state Audit

### 4.1 task_state: Action-Verb Analysis

- **152/217 task_state units (70.0%)** contain action verbs (Add, Implement, Build, Write, Deploy, etc.)
- **65/217 task_state units (30.0%)** are non-action status descriptions ("The export job is blocked", "The eval_runner has been run on subset50")

This 70/30 split is healthy. The task_state units that use action verbs are clearly implementation tasks, blockers, or deployment plans. Examples:
- "Next, add a retry wrapper for the pipeline job" (v05_sample_0006 u2) — correct task_state
- "Write parser tests for the new duplicate assignment check" (v05_sample_0013 u2) — correct task_state
- "The eval_runner has been run on subset50 but not yet on full pilot" (v05_sample_0004 u2) — correct task_state (progress status)

**Verdict: task_state labeling is generally correct.** No systematic mislabeling found.

### 4.2 service_memory: Boundary Cases (19 units with "Add" framing)

These 19 service_memory units use "Add/Implement" action verbs without explicit durable-behavior markers ("must", "does", "rejects", etc.):

**Acceptable per policy (rich behavioral detail):**
- v05_batch50_0013 u1: "Add a deadlock retry wrapper that catches PostgreSQL error code 40P01 and retries up to 3 times with 1-second backoff." — Detailed algorithm (policy's own example of this pattern)
- v05_batch50_0021 u1: "Add a three-way merge strategy as an alternative to last-write-wins, selectable per collection." — Algorithm detail
- v05_batch50_0027 u1: "Add a dead-letter queue for pipeline stages that fail after 3 retries." — Architectural pattern
- v05_batch50_0028 u2: "Add a network-type constraint to the WorkManager policy so it switches intervals automatically." — Behavioral constraint
- v05_batch100_0029 u1: "Add rubric-based grading as an alternative to points-based." — Grading algorithm
- v05_batch100_0030 u1: "Add automatic texture atlas generation that packs textures into power-of-two atlases using the max-rects algorithm." — Named algorithm
- v05_batch100_0032 u1: "Add anomaly detection using a rolling z-score with a window of 30 days and a threshold of 3 standard deviations." — Specific parameters
- v05_batch100_0038 u1: "Add a tiered cancellation policy engine: refundable fares get 100% refund, standard fares get 50%, basic fares are non-refundable." — Detailed policy
- v05_batch100_0050 u1: "Add a quality scoring system that evaluates textures on resolution, compression artifacts, and color consistency." — Scoring criteria

**Needs review (thin behavioral detail, may be better as task_state):**
1. v05_sample_0012 u1: "Add a SHA-256 checksum validation step that runs after the S3 write and logs the result." — SHA-256 is just naming the hash; the behavior is "validate after write and log". Thin detail.
2. v05_sample_0019 u1: "Add a manual purge button that clears all pending offline edits older than 7 days." — UI feature, "purge button" is user-facing. Enterprise app feature, not core algorithm.
3. v05_batch50_0022 u1: "Add a per-table freshness metric that alerts when any table exceeds the 4-hour SLA." — Metric + alert, moderate detail. Borderline.
4. v05_batch100_0031 u1: "Add a relevance feedback loop that boosts documents users clicked for the same query in future searches." — General concept, no implementation detail.
5. v05_batch100_0033 u1: "Add demand-based surge pricing that increases fares by up to 40% when seat availability drops below 20% on a route." — Has specific parameters. Borderline acceptable.
6. v05_batch100_0034 u1: "Add a waitlist that automatically enrolls the next student when someone drops, up to 7 days before the course starts." — Business rule, moderate detail. Borderline.
7. v05_batch100_0036 u1: "Add cross-document summarization that takes up to 10 related documents and produces a unified summary highlighting common themes." — Feature description, no algorithm detail.
8. v05_batch100_0037 u1: "Add a streaming aggregation path using Kafka that updates dashboard metrics in real-time for transactions during market hours." — Architecture pattern naming (Kafka). Borderline but has architectural detail.
9. v05_batch100_0039 u1: "Add a grade appeal workflow where students can submit an appeal within 14 days of grade posting with a written justification." — Business workflow, not algorithm. Borderline.
10. v05_batch200_0084 u2: "The progress tracker enforces prerequisite completion by checking the student's completed_modules list before unlocking the next module." — Actually has durable markers ("enforces", "checks"). My regex may have missed this. Looks correct as service_memory.

### 4.3 service_memory Verdict

The policy is being followed. 9/19 ambiguous cases have sufficient behavioral detail to justify service_memory. 9 others border on task_state (thin detail). 1 (v05_batch200_0084 u2) is actually correctly labeled. The net effect is ~9 cases that could be debated but are not clearly wrong per the policy's own "Add + algorithm detail → service_memory" rule. **This is not a blocker, but a human review on these 9 is recommended.**

---

## 5. project_memory Audit

### 5.1 Catch-all Check

**72 project_memory units.** Classification check:

- **Project scope decisions** (~25 units): "The project does not implement a full MemoryOS", "The data-platform pilot uses synthetic service scenarios only", "The docs-assistant project scope does not include real-time collaboration features." — Correct.
- **Cross-service policies** (~20 units): "All finboard services must use TLS 1.3 for inter-service communication", "All helpdesk services must mask customer email addresses in logs", "All databoard services must use OAuth 2.0 for authentication." — Correct.
- **Compliance/retention** (~12 units): "The finboard project must comply with SOC 2 data integrity requirements", "The helpdesk project retains ticket data for 7 years." — Correct.
- **Evaluation standards** (~3 units): "The project's evaluation standard emphasizes routing-specific metrics", "Training should optimize for routing metrics." — Correct.

**Only 1 unit names a specific service in a way that borders on service_memory:**
- v05_batch100_0048 u1: "The voyager booking service only supports flight bookings; hotel and car rental are explicitly out of scope for the current project phase." — This IS a project scope decision (what the project includes/excludes). The service name is incidental to defining scope. **Acceptable.**

### 5.2 Template project_memory Cases

Cases v05_batch300_0085–0100 contain the template unit: "The {DOMAIN} project requires all externally shared documents to include a confidentiality classification footer." This is:
- Correctly labeled as project_memory (cross-domain policy)
- But template-generated (quality concern)
- Appears 16 times with only the domain name changed

### 5.3 project_memory Verdict

**Not a catch-all.** All 72 units are legitimate project-level scope, policy, compliance, or cross-service rules. The only concern is the 16 template-generated confidentiality-footer units, which inflate the count without adding training diversity.

---

## 6. repo_memory Audit

### 6.1 Content Classification

**94 repo_memory units.** Checking classification quality:

- **File paths / config locations** (~50 units): "Parser tests should live under tests/v04/", "Booking-related database migrations live under db/migrations/booking/", "Eval runner code lives under src/v04/eval_runner.py." — Correct.
- **Test conventions / CI rules** (~15 units): "All sync integration tests must run with a local SQLite database", "All game builds must pass the asset validation suite before the build is considered complete." — Correct (repo-level conventions).
- **App-specific settings** (~5 units): "Enable HDR mode by default", "Set the default flash mode to auto." — Correct per policy (app-specific setting → repo_memory).
- **DB table / schema locations** (~8 units): "The high-watermark values should be persisted in the pipeline_metadata table", "Stock adjustments are logged in the inventory_adjustments table." — Correct (WHERE data lives).
- **Deployment conventions** (~3 units): "Booking service deployments follow the blue-green pattern with the active environment defined in config/deployment/active_env.txt." — Correct (repo-level convention).
- **Code review rules** (~3 units): "All order service PRs require at least two approvals", "Code review comments must reference the specific line number." — These are borderline. Code review rules are team/project conventions, not file paths. Could arguably be project_memory. But they're repo-level process rules, acceptable under "code norms."

### 6.2 Template repo_memory Cases

Cases v05_batch300_0050–0069 contain the template unit: "Document the {DOMAIN} data export API endpoint in the API reference docs." This is:
- Correctly labeled as repo_memory (WHERE to document)
- Template-generated
- Appears 20 times

Cases v05_batch300_0070–0084 contain the template unit asking "Where is the API specification file for the {DOMAIN} service?" These are labeled as READ-only SKIP units. The labeling is correct but the templating persists.

### 6.3 repo_memory Verdict

**Classification is correct.** No systematic mislabeling. The borderline cases (code review rules) are acceptable as "code norms." The main concern is the 20 template-generated "Document the API endpoint" units.

---

## 7. user_profile / Sensitive Audit

### 7.1 user_profile Content

**47 user_profile units.** All express stable, non-sensitive user preferences:
- "I prefer architecture explanations that name tradeoffs explicitly."
- "I prefer flight search results sorted by total price including taxes."
- "I prefer dashboards with compact layouts showing 4 charts per row."

All follow the "I prefer / I like / Always show" preference pattern. No sensitive content found in any user_profile unit.

### 7.2 Sensitive Content

**18 SKIPped units contain sensitive-like patterns.** All correctly SKIPped:
- Passwords: "testpass_1234_do_not_store", "finboard_stage_2026", "HD-admin-2026!"
- Phone: "555-0198"
- Recovery codes: "ABCD-1234-EFGH"
- API tokens: "dba-token-xxxxxxxxxxxx", "docs-beta-token-xxxxxxxxxxxxx"
- Credit cards: "4111-1111-1111-1111"
- Passport: "P12345678"
- Webhooks: "https://hooks.slack.com/services/TEST/FAKE/abcdef"
- Email: "abc16-backup@example.com", "devtest123@gmail.com", "personal.student@email.com"
- PIN: "123456" (device unlock)

**0 sensitive units STOREd.** This is clean.

### 7.3 False Positives in STOREd Units

13 STOREd units matched sensitive keyword patterns but are all **false positives** — they discuss policies ABOUT sensitive data, not actual sensitive data:
- "use the centralized secret manager for API keys and credentials" — policy statement, not a credential
- "mask customer email addresses in logs" — policy about masking, not an actual address
- "does not store full credit card numbers; only the last 4 digits and the payment processor token" — policy about NOT storing sensitive data
- "validate that the shipping address is in a supported country" — business rule, not an actual address

**All 13 are safe.** The model will not learn to store sensitive data from these.

### 7.4 user_profile Verdict

**Clean.** All user_profile units are appropriate preferences. All sensitive units are correctly SKIPped. No corrective action needed in this category.

---

## 8. Template / Duplication Audit

### 8.1 Template Patterns (MAJOR FINDING)

**51 of 100 corrective cases (v05_batch300_0050–0100) are template-generated.** Three template families:

| Template Family | Cases | Units | Pattern |
|----------------|-------|-------|---------|
| Data Export Trilogy | 20 (0050-0069) | 3 per case | u1: "Implement the {DOMAIN} data export feature for the quarterly business review." u2: "Write unit tests for the {DOMAIN} data export module in the test suite." u3: "Document the {DOMAIN} data export API endpoint in the API reference docs." |
| API Spec Location | 15 (0070-0084) | 1+ per case | u1: "Where is the API specification file for the {DOMAIN} service?" |
| Report Trilogy | 16 (0085-0100) | 3 per case | u1: "I prefer {DOMAIN} reports in landscape PDF format..." u2: "The {DOMAIN} project requires all externally shared documents to include a confidentiality classification footer." u3: "Generate the monthly {DOMAIN} summary report and email it to the stakeholders." |

**Impact assessment:**
- The model will see 51 cases where the only difference is the domain name
- It may learn "domain-name → target" shortcuts rather than semantic reasoning
- The data-export trilogy cases have identical runtime_context.service = "service" (generic placeholder — evidence of template artifacts)
- The report trilogy cases have runtime_context.repo = "{domain}-repo" with task = "record preferences and policies" (generic)
- These cases contribute ~153 units to the distribution but add almost zero semantic diversity

### 8.2 Duplicate Units

- **32 duplicate current_unit texts** across cases (all from the template families appearing in both batch200 and batch300 ranges, or within batch300_0050-0100 where some domains repeat)
- **5 duplicate candidate_memory contents** across cases (minor, from reused context)
- **0 duplicates within individual cases** — each case's own units are unique

### 8.3 Template Verdict

**This is the single biggest quality issue in batch300.** The 49 non-template corrective cases (v05_batch300_0001–0049) are all READ-only factual questions ("What happens when a query runs longer than 30 seconds?") which DO add value as temporary_request / read_only training examples. But the 51 template cases are low-quality filler that inflates the distribution count without adding training signal.

**Recommendation:** Remove or significantly reduce template cases before batch500. Replace with semantically diverse cases that achieve the same distribution targets through genuine variety.

---

## 9. Domain Safety Audit

### 9.1 Real Platform References

Units contain references to real platforms/products:
- **Slack**: Referenced 10 times (channel names, webhooks, alerts) — synthetic usage, acceptable
- **GitHub**: Referenced once ("public GitHub repositories") — domain context, acceptable
- **OpenAI**: Referenced once ("OpenAI-compatible APIs") — technology reference, acceptable
- **Stripe**: Referenced once ("Stripe API test key") — correctly SKIPped
- **AWS**: Referenced twice (KMS key ARN, access key) — one correctly SKIPped as sensitive, one is a KMS key reference in a service description
- **Google**: Referenced once ("personal Google account") — correctly SKIPped

**Verdict:** Acceptable. Real platform names are used as technology references in synthetic scenarios, not as corporate secrets. Sensitive-looking platform references (API keys, accounts) are correctly SKIPped.

### 9.2 No Real Personal Data

All email addresses, phone numbers, and credentials are obviously synthetic (e.g., "abc16-backup@example.com", "555-0198", "testpass_1234"). No real-world PII detected.

### 9.3 No Real Company/Product Names

All project, repo, and service names are synthetic: "memory-router", "data-platform", "mobile-field", "docs-assistant", "finance-dashboard", "travel-planner", "education-platform", "game-studio", "customer-support", "ecommerce-platform", "analytics-dashboard", "learning-assistant", "workflow-automation", "helpdesk", "shopengine", "studybuddy", "flowcraft", "databoard", "voyager", "learnhub", "finboard", "dungeon-tools". No real products or companies.

---

## 10. Top 10 Cases Requiring Human Review

| # | case_id | unit_id | Current Label | Concern | Proposed Correction | Confidence |
|---|---------|---------|---------------|---------|---------------------|------------|
| 1 | v05_batch300_0050–0069 | all | task_state / repo_memory | **Template-generated.** 20 cases with identical structure, only domain name differs. Runtime context uses "service": "service" (placeholder artifact). Adds quantity without quality. | Replace with 5-7 semantically diverse cases covering data export scenarios. Keep distribution targets. | HIGH |
| 2 | v05_batch300_0085–0100 | all | user_profile / project_memory / task_state | **Template-generated.** 16 cases of the same report+footer+preference triplet. "game-studio" appears twice (0085 and 0098). The "confidentiality footer" unit is repeated 16 times with only domain name changed. | Remove template cases. Replace with 5-6 diverse cases covering document policies across different project types. | HIGH |
| 3 | v05_batch300_0070–0084 | all | SKIP (READ-only) | **Template-generated.** 15 cases asking "Where is the API specification file for the {DOMAIN} service?" All are READ-only queries with the same structure. | Reduce to 3-4 cases with genuinely different query structures and candidate memory contexts. | HIGH |
| 4 | v05_sample_0012 | u1 | service_memory | "Add a SHA-256 checksum validation step that runs after the S3 write and logs the result." Thin behavioral detail. "SHA-256" names the algorithm but doesn't describe it. The core content is "validate after S3 write and log." | Consider task_state. The framing is implementation-plan ("Add X that does Y after Z"), and the behavioral detail is minimal compared to the policy's deadlock-retry example. | MEDIUM |
| 5 | v05_sample_0019 | u1 | service_memory | "Add a manual purge button that clears all pending offline edits older than 7 days." This describes a UI feature ("purge button"), not a service behavior algorithm. Enterprise app feature description. | Consider task_state. UI features are explicitly task_state per policy. The "older than 7 days" constraint is a parameter, not an algorithm. | MEDIUM |
| 6 | v05_batch100_0031 | u1 | service_memory | "Add a relevance feedback loop that boosts documents users clicked for the same query in future searches." General concept description. No specific algorithm, no parameters, no constraints beyond "boost documents users clicked." | Consider task_state. This is a feature idea/implementation plan, not a detailed behavioral specification. | MEDIUM |
| 7 | v05_batch100_0034 | u1 | service_memory | "Add a waitlist that automatically enrolls the next student when someone drops, up to 7 days before the course starts." Business rule with one parameter (7 days). The "waitlist" is a feature concept, not a behavioral algorithm. | Borderline. The 7-day parameter adds some specificity. Could be argued either way. Suggest keeping as service_memory if policy is interpreted generously. | LOW |
| 8 | v05_batch100_0039 | u1 | service_memory | "Add a grade appeal workflow where students can submit an appeal within 14 days of grade posting with a written justification." Business workflow. The 14-day window is a parameter. | Borderline. Like #7, this is feature-level with one constraint parameter. Suggest keeping as service_memory. | LOW |
| 9 | v05_batch100_0036 | u1 | service_memory | "Add cross-document summarization that takes up to 10 related documents and produces a unified summary highlighting common themes." High-level feature description. "Up to 10 documents" is the only parameter. | Consider task_state. Very thin on behavioral detail. The summarization approach is not specified (extractive? abstractive? how are common themes identified?). | MEDIUM |
| 10 | v05_batch50_0022 | u1 | service_memory | "Add a per-table freshness metric that alerts when any table exceeds the 4-hour SLA." Monitoring behavior. Links to project-level SLA. | Borderline acceptable. The 4-hour SLA provides context and the alerting behavior is durable monitoring infrastructure. Suggest keeping as service_memory. | LOW |

---

## 11. batch300_new100 Corrective Effectiveness

### 11.1 What Worked

1. **Distribution correction achieved.** The corrective batch successfully reduced the svc:task gap from 11.9pp to 8.7pp by adding 99 task_state units with 0 new service_memory units.
2. **Sensitive boundary training strengthened.** The batch added cases covering token, email, and sensitive-content scenarios (e.g., v05_batch300_0023 u3: personal access token correctly SKIPped).
3. **repo_memory diversity improved.** 40 new repo_memory units covering CI pipelines, deployment conventions, code review rules, and DB schema locations.
4. **project_memory scope cases added.** 36 new project_memory units covering data retention, platform support, authentication policies, and completion criteria.

### 11.2 What Didn't Work

1. **51% template generation.** The corrective batch relied heavily on domain-name-substitution templates to hit distribution targets quickly. This undermines the corrective intent — the model won't learn better target discrimination from seeing the same sentence 16 times with different domain names.
2. **0 READ+STORE joint cases.** The corrective batch added only READ-only (33) and STORE/SKIP-only (67) cases, further skewing the shape distribution away from the blueprint target of 45-50% READ+STORE joint.
3. **Generic runtime_context.** Template cases use "service": "service" and "repo": "{domain}-repo" — placeholder artifacts that leak generation mechanics into training data.
4. **Duplicate domain coverage.** "game-studio" appears twice in the report template family (v05_batch300_0085 and v05_batch300_0098), and "data-platform" data export units appear in the main file under both batch200 and batch300 IDs with identical text.

### 11.3 Net Assessment

The corrective batch **partially succeeded** — it fixed the distribution numbers but at the cost of data quality. The 49 non-template cases (0001-0049) are good READ-only examples. The 51 template cases (0050-0100) need to be largely replaced before batch500.

---

## 12. SFT Message Validation

- **300/300** SFT messages have valid `system/user/assistant` role structure
- **0/300** DSL mismatches between assistant content and gold.dsl
- **0/300** markdown or JSON formatting in assistant messages
- **Format is stable** at 300-case scale

**No issues found.** SFT format is production-ready.

---

## 13. batch500 Recommendation

### Recommendation: **CORRECTION REQUIRED BEFORE BATCH500**

**Rationale:** batch300 is structurally valid and has no critical labeling errors (no sensitive STOREd, no systematic target confusion). However, the template-generation problem in the corrective batch is a quality blocker that must be resolved before scaling to 500. Using template-generated cases as seed for batch500 would propagate low-quality patterns.

### Required Corrections

| Priority | Action | Cases Affected |
|----------|--------|---------------|
| **P0** | Replace 51 template cases (v05_batch300_0050–0100) with semantically diverse cases | 51 |
| **P0** | Add 30-40 READ+STORE joint cases to bring shape distribution toward 45-50% target | 30-40 new |
| **P1** | Review 9 borderline service_memory cases (thin "Add" detail) | 9 |
| **P1** | Add ~30 service_memory units to bring svc% from 27.7% back toward 30-34% | 30 new |
| **P2** | Remove duplicate domain entries (e.g., second "game-studio" in report templates) | 2-3 |
| **P2** | Fix template artifact: "service": "service" in runtime_context | 51 |

### Post-Correction batch500 Design

After corrections:
1. Start with corrected ~250 cases from batch300 (remove/replace templates, keep the good 249)
2. Generate 250 new cases targeting:
   - 60-70 READ+STORE joint
   - 40-50 service_memory
   - 30-40 task_state
   - 20-30 repo_memory
   - 10-15 project_memory
   - 0 user_profile (already at upper bound)
3. This brings the 500-case pool into blueprint range for both distribution and shapes
4. Apply strict no-template policy for new cases: each case must have unique semantic content

### If Corrections Are Not Made

Proceeding to batch500 without correction risks:
- Model learning domain-name gating instead of semantic routing
- Inflated confidence on template-like patterns that don't generalize
- Poor READ+STORE joint performance (model won't have seen enough joint reasoning examples)
- Distribution targets met on paper but training signal diluted by template repetition

---

## 14. Summary

| Dimension | Status | Notes |
|-----------|--------|-------|
| Structural validity | PASS | 300/300 parse correctly, 0 DSL mismatches |
| Sensitive content | PASS | 0 sensitive units STOREd, all 18 correctly SKIPped |
| Label policy compliance | CONDITIONAL PASS | ~93-95% correct. 9 borderline service_memory cases, no systematic errors |
| Distribution targets | CONDITIONAL PASS | task_state 2.5pp above, service_memory 2.3pp below target range |
| Shape distribution | FAIL | READ+STORE joint at 27.3% vs 45-50% target |
| Template/duplication | FAIL | 51% of corrective batch is template-generated |
| Domain safety | PASS | All synthetic, no real PII |
| SFT format | PASS | 300/300 valid system/user/assistant |
| Seed readiness for batch500 | **NO — correction required** | Template cases must be replaced; shape imbalance must be addressed |

---

**Bottom line:** Don't train on this as-is. Fix the templates, review the boundary cases, add READ+STORE joint diversity, then proceed. The foundation is solid — the execution needs cleanup.

---

*End of independent review. No files modified. All findings are read-only audit observations.*
