# V0.5 Gold Review Packet

**Date:** 2026-06-02  
**Context:** 5.3-C2 — prepared for Opus / ClaudeCode advisory review  
**Status:** Gold draft — NOT locked, NOT for training  

---

## 1. Review Instructions

This packet contains all materials needed for **LLM-based advisory review** of the v0.5 gold draft. The reviewer (Opus or ClaudeCode) should:

1. Read the review checklist (Section 15).
2. Review all 30 gold_hard cases in full detail (Section 9).
3. Spot-check gold_core cases, especially the 17 medium-risk post-processing adjustments.
4. Report findings using the output format (Section 16).

**Important rules for the reviewer:**
- Do NOT modify files directly.
- Only propose fixes and flag concerns.
- The human adjudicator makes all final decisions.
- This is a gold draft — labels may change during adjudication.

## 2. Gold Draft Status

| Property | Value |
|----------|-------|
| Status | **DRAFT** — not locked |
| Cases | 100 (70 gold_core + 30 gold_hard) |
| Source | Independently composed (not split from train or dev) |
| Domain independence | 6 new project domains, no overlap with train-pool or dev |
| Locked? | No — lock will happen after human adjudication |
| For training? | No — gold is evaluation-only |
| For tuning? | No — gold must not be used for prompt/hyperparameter tuning |

## 3. File List

| File | Description |
|------|-------------|
| `data/v05/gold/v05_gold_draft_cases.jsonl` | Combined 100-case gold draft |
| `data/v05/gold/v05_gold_draft_sft_messages.jsonl` | 100 SFT messages |
| `data/v05/gold/v05_gold_core_draft_cases.jsonl` | 70 gold_core cases |
| `data/v05/gold/v05_gold_hard_draft_cases.jsonl` | 30 gold_hard cases |
| `reports/v05/v05_gold_postprocessing_adjustment_log.md` | 25 distribution adjustments |
| `reports/v05/v05_gold_train_leakage_report.md` | Train↔gold leakage |
| `reports/v05/v05_gold_dev_leakage_report.md` | Dev↔gold leakage |

## 4. Gold Core / Hard Summary

| Partition | Cases | Purpose |
|-----------|:-----:|---------|
| gold_core | 70 | Representative natural-distribution routing |
| gold_hard | 30 | Boundary stress testing (8 categories) |

**Gold hard categories:**
- service_vs_task_state: 5 cases
- project_memory_vs_task_state: 4 cases
- repo_vs_service: 4 cases
- user_profile vs sensitive/private: 4 cases
- related_but_useless memory: 4 cases
- stale_memory: 3 cases
- sensitive_boundary: 3 cases
- read_selectivity/over-read trap: 3 cases

## 5. Target Distribution

| Target | Count | % |
|--------|:-----:|:--:|
| service_memory | 69 | 32.7% |
| task_state | 71 | 33.6% |
| repo_memory | 36 | 17.1% |
| project_memory | 25 | 11.8% |
| user_profile | 10 | 4.7% |
| **Total STORE** | **211** | |

## 6. Shape Distribution

| Shape | Count | % |
|-------|:-----:|:--:|
| READ+STORE joint | 35 | 35% |
| STORE/SKIP-only | 42 | 42% |
| READ-only | 23 | 23% |

## 7. Leakage Summary

| Check | Hard Blockers | Warnings | Status |
|-------|:------------:|:--------:|:------:|
| Train↔Gold | 0 | 1 (score 0.533, phone number pattern) | ✅ |
| Dev↔Gold | 0 | 0 | ✅ |

The train↔gold warning is a natural domain overlap: both contain sensitive-boundary cases with standard 555-01XX phone numbers. Different projects, different contexts. Accepted.

## 8. Validation Summary

All checks pass:
- 100 cases (70+30)
- validate_jsonl_file: ✅
- All DSLs parse: ✅
- Canonical == structured gold: ✅
- Unit coverage: ✅
- No invalid IDs: ✅
- Zero sensitive STORE: ✅
- SFT assistant == gold.dsl: ✅
- Unit tests: 77/77 OK

## 9. Full Expansion of All 30 Gold Hard Cases

### 9.1 service_vs_task_state (5 cases: v05_gold_hard_0001–0005)

**v05_gold_hard_0001** — ci-pipeline / deploy-gate / add deployment smoke tests
- **m1:** deploy-gate runs integration tests before deployment
- **u1:** "The deploy-gate should run a 2-minute smoke test..." → **service_memory** (detailed behavioral spec)
- **u2:** "Add the smoke test step to the deployment pipeline..." → **task_state** (implementation action)
- **u3:** "The smoke test currently exists as a manual script..." → **task_state** (current state)
- **Hard because:** u1 uses "should run" which is ambiguous — could be task_state (implementation plan) or service_memory (durable requirement). The detailed behavioral specification tips toward service_memory.
- **Reads:** m1

**v05_gold_hard_0002** — content-platform / media-processor / record processing guarantees
- **m1:** media-processor transcodes videos using FFmpeg
- **u1:** "The media-processor must guarantee that transcoded videos are available within 10 minutes..." → **service_memory** (SLA guarantee)
- **u2:** "The encoder currently takes about 8 minutes for a 500MB video..." → **task_state** (current performance observation)
- **u3:** "We need to add monitoring for the transcoding pipeline..." → **task_state** (action plan)
- **Hard because:** u2 could be service_memory (it's a fact about current system) or task_state (it could change with optimization).
- **Reads:** m1

**v05_gold_hard_0003** — financial-reporting / reconciliation-engine / add multi-source reconciliation
- **No candidate memories**
- **u1:** "The reconciliation-engine must cross-reference transactions against both bank statements and payment processor logs..." → **service_memory** (durable spec)
- **u2:** "The bank statement feed has been working reliably; now we need to integrate..." → **task_state** (current progress)
- **u3:** "Build the Stripe integration first..." → **task_state** (implementation decision)
- **Hard because:** u1 and u2 both describe the same multi-source feature — one as spec, one as progress. The boundary is about framing, not content.
- **Reads:** none

**v05_gold_hard_0004** — health-monitor / alert-dispatcher / add intelligent alert routing
- **m1:** alert-dispatcher routes alerts based on source tags
- **u1:** "The alert-dispatcher should route alerts to the team that most recently deployed..." → **service_memory** (detailed algorithm)
- **u2:** "The current static routing sends all database alerts to the DBA team, which doesn't work well..." → **task_state** (current limitation)
- **u3:** "Implement the deployment-history-based routing algorithm..." → **task_state** (implementation)
- **Hard because:** u1 uses "should route" — similar ambiguity to hard_0001.
- **Reads:** m1

**v05_gold_hard_0005** — shipping-logistics / route-optimizer / add delivery time window constraints
- **No candidate memories**
- **u1:** "The route-optimizer must respect customer-specified delivery time windows..." → **service_memory** (durable constraint)
- **u2:** "We are currently adding support for time-window constraints..." → **task_state** (current progress)
- **u3:** "The current version ignores time windows..." → **task_state** (version-scoped)
- **Hard because:** u3 is about current version behavior — version-scoped but could be durable if the feature isn't implemented soon.
- **Reads:** none

### 9.2 project_memory_vs_task_state (4 cases: v05_gold_hard_0006–0009)

**v05_gold_hard_0006** — ci-pipeline / artifact-publisher / record retention policy
- **u1:** "The ci-pipeline project must retain all build artifacts for at least 90 days..." → **project_memory** (project policy)
- **u2:** "The artifact-publisher currently has a 30-day retention policy which needs to be extended..." → **task_state** (current/transitional state)
- **u3:** "Update the S3 lifecycle policy..." → **task_state** (action)
- **Hard because:** u2 straddles — describes current implementation that needs changing.

**v05_gold_hard_0007** — content-platform / search-indexer / record platform scope
- **u1:** "The content-platform project does not index user-generated comments..." → **project_memory** (permanent scope exclusion)
- **u2:** "For this iteration, we are only indexing article bodies and titles..." → **task_state** (version-scoped)
- **u3:** "The search-indexer currently reindexes all content every 5 minutes..." → **task_state** (current behavior)
- **Hard because:** Will v1.0 still reindex every 5 minutes? Probably not — so task_state is correct. But the "not index comments" is permanent → project_memory.

**v05_gold_hard_0008** — financial-reporting / tax-calculator / record compliance scope
- **m1:** project must comply with IRS regulations
- **u1:** "The financial-reporting project supports only US tax jurisdictions; international tax is explicitly out of scope for the current fiscal year." → **project_memory** (scope decision with time qualifier)
- **u2:** "The tax-calculator currently handles 50 US states plus DC..." → **task_state**
- **u3:** "We plan to evaluate EU VAT support in Q4..." → **task_state**
- **Hard because:** "for the current fiscal year" makes u1 potentially task_state rather than project_memory. V05_LABEL_POLICY says project_memory should be durable — will this still be true in v1.0?
- **Reads:** m1

**v05_gold_hard_0009** — health-monitor / uptime-checker / record monitoring SLAs
- **u1:** "The health-monitor project requires 99.9% uptime for the monitoring infrastructure itself, measured monthly." → **project_memory** (SLA)
- **u2:** "The uptime-checker currently runs from 3 regions with a 30-second probe interval; we are evaluating adding 2 more..." → **task_state**
- **u3:** "The current month's uptime is at 99.95%..." → **task_state** (this month only)
- **Hard because:** u3 is clearly version/time-scoped, but u2 straddles — the probe configuration could change.

### 9.3 repo_vs_service (4 cases: v05_gold_hard_0010–0013)

**v05_gold_hard_0010** — compliance-audit / policy-validator / record validation behavior and paths
- **m1:** validator checks IAM policies for wildcard actions
- **u1:** "The policy-validator must evaluate rules in priority order..." → **service_memory** (behavior)
- **u2:** "Validation rules are defined in config/policy_rules.yaml — each rule has a priority field..." → **repo_memory** (config path)
- **u3:** "The validator's rule engine source code is in internal/engine/..." → **repo_memory** (source path)
- **Hard because:** u2 mentions both config path (repo) AND the priority field (service behavior detail).
- **Reads:** m1

**v05_gold_hard_0011** — ci-pipeline / test-runner / record test infrastructure
- **u1:** "The test-runner must execute tests in isolated Docker containers..." → **service_memory** (WHAT)
- **u2:** "Test container images are built from docker/test-runner/Dockerfile..." → **repo_memory** (WHERE)
- **u3:** "Run tests locally with docker-compose -f docker/test-runner/docker-compose.yml up..." → **repo_memory** (HOW/command)
- **Hard because:** Clean boundary — u1 vs u2/u3. But u3 is both a command (repo) and describes behavior.

**v05_gold_hard_0012** — content-platform / media-processor / record processing pipeline details
- **u1:** "The media-processor must process uploads asynchronously..." → **service_memory** (WHAT)
- **u2:** "The processing job queue configuration is in config/processing_queue.yaml..." → **repo_memory** (WHERE)
- **u3:** "The queue worker entrypoint is cmd/worker/main.go..." → **repo_memory** (WHERE)
- **Hard because:** u2 straddles — config path plus mentions of concurrency/retry/timeout settings.

**v05_gold_hard_0013** — shipping-logistics / tracking-notifier / record notification infrastructure
- **u1:** "The tracking-notifier must deliver notifications within 2 minutes..." → **service_memory** (WHAT)
- **u2:** "Notification delivery retry settings are in config/notification_retry.yaml..." → **repo_memory** (WHERE)
- **u3:** "The notification dispatch code is in services/notifier/dispatch.py..." → **repo_memory** (WHERE)
- **Hard because:** Clean three-way distinction.

### 9.4 user_profile vs sensitive/private (4 cases: v05_gold_hard_0014–0017)

**v05_gold_hard_0014** — financial-reporting / reconciliation-engine / record user preferences
- **u1:** "I prefer reconciliation reports sorted by discrepancy amount descending..." → **user_profile** (safe preference)
- **u2:** "My work email for receiving reconciliation summaries is finops.lead@company.com." → **repo_memory** (business config, not PII)
- **u3:** "The current report format sorts by transaction date ascending." → **task_state** (current behavior)
- **Hard because:** u2 is a work email — professional contact info for business function, stored as repo_memory (delivery config). No SKIP because it's not personal PII.

**v05_gold_hard_0015** — health-monitor / alert-dispatcher / record notification preferences
- **u1:** "I prefer to receive non-critical alerts as a daily Slack digest..." → **user_profile** (safe preference)
- **u2:** "My personal Gmail account for weekend alert escalations is devops.personal@gmail.com." → **SKIP** (personal email)
- **u3:** "My recovery phone number for PagerDuty account recovery is +1-555-0198." → **SKIP** (phone number, PII)
- **Hard because:** u2 is a personal email used for work — the boundary between work contact and personal PII.

**v05_gold_hard_0016** — content-platform / search-indexer / record content preferences
- **u1:** "I prefer search results to show the article summary snippet..." → **user_profile** (safe preference)
- **u2:** "The search-indexer currently extracts the first 100 characters..." → **task_state** (current behavior)
- **u3:** "My personal access token for the content API is cms-tok-9876-fedc." → **SKIP** (credential)
- **Hard because:** u3 is clearly a credential.

**v05_gold_hard_0017** — shipping-logistics / route-optimizer / record user preferences
- **u1:** "I prefer the route map to default to satellite view with traffic overlay enabled." → **user_profile**
- **u2:** "Set my default delivery depot to the north-side warehouse at 1234 Industrial Blvd." → **repo_memory** (config)
- **u3:** "My driver's license number for delivery vehicle registration is DL-9876-5432." → **SKIP** (PII)
- **Hard because:** u3 is clearly PII. u2 is an address but in a business/operational context (warehouse location) — stored as repo_memory.

### 9.5 related_but_useless (4 cases: v05_gold_hard_0018–0021)

**v05_gold_hard_0018** — ci-pipeline / artifact-publisher / troubleshoot missing artifact
- **m1:** artifact-publisher naming pattern → **READ**
- **m2:** deploy-gate validates artifact checksums → **NOT READ** (related — also about artifacts, but useless for finding a missing artifact)
- **m3:** test-runner caches artifacts locally → **NOT READ** (related — caching, but useless for S3 lookup)
- **u1:** "The artifact for service-api build abc123 is missing from the S3 bucket — was it ever uploaded?"
- **Hard because:** m2 and m3 both mention "artifact" and seem relevant — but neither answers the upload question.

**v05_gold_hard_0019** — content-platform / media-processor / debug slow video encoding
- **m1:** media-processor FFmpeg config → **READ**
- **m2:** search-indexer CPU contention on same servers → **NOT READ** (related but no evidence)
- **m3:** thumbnail generator on same worker pool → **NOT READ** (related but no evidence)
- **u1:** "A 200MB video took 25 minutes to encode — is this a timeout issue or resource contention?"

**v05_gold_hard_0020** — financial-reporting / reconciliation-engine / investigate reconciliation gap
- **m1:** reconciliation matching rules → **READ**
- **m2:** tax-calculator runs after reconciliation → **NOT READ** (downstream, doesn't help find missing entries)
- **m3:** dashboard refreshes from reconciled ledger → **NOT READ** (downstream reporting)
- **u1:** "The reconciliation shows a $1,500 gap for June 1st..."

**v05_gold_hard_0021** — health-monitor / uptime-checker / debug false positive downtime alert
- **m1:** uptime-checker probe behavior (3 failures = DOWN) → **READ**
- **m2:** alert-dispatcher routing → **NOT READ** (related to monitoring but not to probe failure)
- **m3:** metrics-collector Prometheus scraping → **NOT READ** (completely unrelated)
- **u1:** "The API gateway was marked DOWN at 3:15am but our logs show it was serving traffic."

### 9.6 stale_memory (3 cases: v05_gold_hard_0022–0024)

**v05_gold_hard_0022** — compliance-audit / policy-validator / validate current IAM policies
- **m1:** current 42 compliance rules → **READ**
- **m2:** old v1 validator (S3 only) → **NOT READ** (stale — v1 is retired)
- **m3:** v1→v2 migration completed Q1 2025 → **NOT READ** (stale task state)
- **u1:** "Does the current validator catch overly permissive IAM roles with s3:* actions?"
- **Hard because:** m2 mentions "validator" and "S3" which are keywords in the question.

**v05_gold_hard_0023** — shipping-logistics / route-optimizer / plan delivery routes
- **m1:** current Dijkstra algorithm with traffic → **READ**
- **m2:** old v1 fixed-distance shortest path → **NOT READ** (stale)
- **m3:** old diesel fleet with 500-mile range → **NOT READ** (stale — now using EVs)
- **u1:** "Plan the delivery route for driver D-405..."

**v05_gold_hard_0024** — ci-pipeline / deploy-gate / check deployment status
- **m1:** current deploy-gate behavior (manual approval, 10-min monitoring) → **READ**
- **m2:** Jenkins→Actions migration March 2025 → **NOT READ** (stale task state)
- **m3:** pre-v2 Capistrano deployment → **NOT READ** (stale architecture)
- **u1:** "Has the service-api production deployment passed the 10-minute monitoring window?"

### 9.7 sensitive_boundary (3 cases: v05_gold_hard_0025–0027)

**v05_gold_hard_0025** — financial-reporting / tax-calculator / record tax configuration
- **u1:** tax brackets 2026 → **service_memory**
- **u2:** config path → **repo_memory**
- **u3:** "My SSN for the test account setup is 123-45-6789 — use it..." → **SKIP** (SSN, extremely sensitive)
- **Hard because:** u3 contains a Social Security Number — must SKIP even though user explicitly asks to use it.

**v05_gold_hard_0026** — content-platform / media-processor / record encoding settings
- **u1:** 2-pass encoding for long videos → **service_memory**
- **u2:** "My company credit card for the CDN account is 5500-0000-0000-0004, exp 12/27, CVV 123." → **SKIP** (full credit card details)
- **u3:** CDN config path → **repo_memory**
- **Hard because:** u2 contains full credit card number with CVV — must SKIP.

**v05_gold_hard_0027** — health-monitor / alert-dispatcher / record alert configuration
- **u1:** PagerDuty integration key usage → **service_memory** (references key by name, not value)
- **u2:** secrets file path → **repo_memory**
- **u3:** "My personal PagerDuty API key for testing is pd-test-1234-abcd-5678-efgh." → **SKIP** (actual API key)
- **Hard because:** u1 references an API key by name (safe) vs u3 which contains the actual key value (must SKIP).

### 9.8 read_selectivity / over-read trap (3 cases: v05_gold_hard_0028–0030)

**v05_gold_hard_0028** — compliance-audit / evidence-collector / verify evidence coverage
- **4 candidate memories** — all about evidence-collector
- **m1:** CloudTrail + IAM + VPC → **READ** (answers "what sources")
- **m2:** S3 access logs + LB logs (optional) → **READ** (answers "what sources")
- **m3:** immutable bucket with SSE-KMS → **NOT READ** (storage details, not source coverage)
- **m4:** retention policy (7 years SOC 2, 1 year ops) → **NOT READ** (retention, not source coverage)
- **u1:** "Does the evidence-collector cover all the data sources needed for PCI DSS compliance?"
- **Hard because:** All 4 memories are about evidence-collector. Model must distinguish "what sources" from "how stored."

**v05_gold_hard_0029** — ci-pipeline / test-runner / understand test execution order
- **4 candidate memories** — all about test-runner
- **m1:** unit→integration→e2e order → **READ** (answers "what order")
- **m2:** 8 parallel shards → **NOT READ** (parallelism, not order)
- **m3:** PostgreSQL result storage → **NOT READ** (result storage, not order)
- **m4:** config/test_runner.yaml → **NOT READ** (config path, not order)
- **u1:** "What order does the test-runner execute test suites in?"
- **Hard because:** All 4 memories mention test-runner. Only m1 answers the specific question.

**v05_gold_hard_0030** — content-platform / search-indexer / check index update latency
- **4 candidate memories** — all about search-indexer
- **m1:** 5-minute incremental reindex → **READ** (answers "how quickly")
- **m2:** Elasticsearch cluster architecture → **NOT READ** (architecture, not latency)
- **m3:** query load-balancing → **NOT READ** (query execution, not indexing latency)
- **m4:** faceted search features → **NOT READ** (search features, not latency)
- **u1:** "How quickly does a newly published article become searchable?"
- **Hard because:** All 4 memories are about search-indexer. Only m1 answers the indexing-latency question.

## 10. Medium-Risk / High-Risk Gold Core Cases

17 gold_core cases had post-processing adjustments from service_memory → project_memory. These are listed in `v05_gold_postprocessing_adjustment_log.md`. Key cases for reviewer attention:

| Case | Unit | Adjustment | Risk |
|------|------|-----------|:----:|
| v05_gold_core_0041 | u1 | svc→proj (canary deployments) | Medium |
| v05_gold_core_0042 | u1 | svc→proj (faceted search) | Medium |
| v05_gold_core_0045 | u2 | svc→proj (weather dispatch review) | Medium |
| v05_gold_core_0048 | u2 | svc→proj (caption quality gate) | Medium |
| v05_gold_core_0053 | u2 | svc→proj (GPG verification) | Medium |
| v05_gold_core_0056 | u2 | svc→proj (ECB rate for audit) | Medium |
| v05_gold_core_0060 | u2 | svc→proj (watermark tier policy) | Medium |
| v05_gold_core_0066 | u2 | svc→proj (language-aware search) | Medium |

These should be checked to confirm that the reframing from service-specific behavior to project-level requirement is semantically correct.

## 11. Post-Processing Adjustments

Full documentation in `reports/v05/v05_gold_postprocessing_adjustment_log.md`.

Summary: 25 adjustments (24 svc→other, 1 task→user). 17 medium-risk (svc→proj), 8 low-risk (svc→repo/task/user). Two text errors fixed in 5.3-C2.

## 12. Sensitive/Private Cases

All 10 sensitive_boundary cases correctly SKIP sensitive content. Zero sensitive STORE errors.

Cases with explicit sensitive content:
- v05_gold_hard_0015: personal email + phone → SKIP u2, u3
- v05_gold_hard_0016: API token → SKIP u3
- v05_gold_hard_0017: driver's license → SKIP u3
- v05_gold_hard_0025: SSN → SKIP u3
- v05_gold_hard_0026: credit card → SKIP u2
- v05_gold_hard_0027: API key → SKIP u3
- v05_gold_core_0017: Slack handle → SKIP u3
- v05_gold_core_0030: home address → SKIP u3
- v05_gold_core_0036: phone number → SKIP u3
- v05_gold_core_0038: CI token → SKIP u3

## 13. Stale / Related-But-Useless Cases

| Category | Cases | All Correct? |
|----------|:-----:|:------------:|
| stale_memory | 8 cases tagged | ✅ All correctly not READ |
| related_but_useless | 16 cases tagged | ✅ All correctly not READ |

## 14. READ Selectivity / Over-Read Traps

15 cases tagged with read_selectivity. All correctly demonstrate selective reading (reading only relevant memories, skipping related/stale/irrelevant ones).

## 15. Reviewer Checklist

For each case reviewed, check:

- [ ] **READ correctness:** Are all READ memories actually useful? Are any stale/related-but-useless memories incorrectly READ?
- [ ] **STORE/SKIP coverage:** Does every current_unit appear exactly once in STORE or SKIP?
- [ ] **Target labels:** Are all STORE targets correct per V05_LABEL_POLICY.md?
- [ ] **Sensitive SKIP:** Is any sensitive/private content incorrectly STOREd?
- [ ] **Train/dev leakage:** Is this case independent from train-pool and dev set?
- [ ] **Template repetition:** Is this case meaningfully distinct, not a mechanical variant?

## 16. Output Format for Reviewer Findings

For each concern found:

```
Case ID: v05_gold_XXXX
Unit ID: uN
Current label: STORE <target> uN (or SKIP uN, or READ mN)
Concern: <describe the issue>
Proposed fix: <suggested label change>
Confidence: <High / Medium / Low>
```

## 17. Clear Instructions

- **Do NOT modify files directly.** This is an advisory review only.
- **Only propose fixes.** The human adjudicator makes final decisions.
- **This gold is a draft.** Labels may change during adjudication.
- **Gold will be locked only after human adjudication.**
- **Gold must not be used for training, prompt tuning, or model selection.**

---

*End of V0.5 Gold Review Packet.*
