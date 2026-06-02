# V0.5 Batch50 Semantic Audit

Date: 2026-06-01  
Context: 5.0-E — batch50 semantic audit  
Status: Agent-generated; human review required

## 1. Purpose

This audit examines all 50 v0.5 batch cases for semantic labeling quality, target-boundary correctness, sensitive-content handling, and READ decision quality. Every case is evaluated; high-risk cases are flagged for human review.

## 2. Per-Case Audit Table

Legend: Source S=seed20, N=new30. Boundary risk: L=Low, M=Medium, H=High. HR=Human Review needed.

| # | Case ID | Src | Shape | Main Tags | READ | STORE | SKIP | Risk | HR | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | v05_sample_0001 | S | READ-only | read_only, service_invariant | m1 (parser behavior) | NONE | u1 (temp verification) | L | N | Clean |
| 2 | v05_sample_0002 | S | READ-only | read_only, stale_memory | m1 (sync retry) | NONE | u1 (one-off) | L | N | Clean stale detection |
| 3 | v05_sample_0003 | S | READ-only | read_only, related_but_useless | m1 (export) | NONE | u1 (weather) | L | N | Clean unrelated SKIP |
| 4 | v05_sample_0004 | S | STORE/SKIP-only | service_vs_task_state | NONE | u1→service, u2→task | u3 (speculation) | M | N | Reviewed P5.7-C, kept |
| 5 | v05_sample_0005 | S | STORE/SKIP-only | repo_vs_service, sensitive | NONE | u1→repo, u2→service | u3 (email) | L | N | Sensitive SKIP correct |
| 6 | v05_sample_0006 | S | STORE/SKIP-only | project_vs_repo, target_boundary | NONE | u1→project, u2→task | u3 (lunch) | M | N | Notes clarified P5.7-D |
| 7 | v05_sample_0007 | S | STORE/SKIP-only | user_profile, sensitive | NONE | u1→user_profile, u2→repo | u3 (phone) | L | N | Sensitive SKIP correct |
| 8 | v05_sample_0008 | S | STORE/SKIP-only | repo_vs_service | NONE | u1→service, u2→repo | u3 (new target) | L | N | Out-of-scope SKIP |
| 9 | v05_sample_0009 | S | READ+STORE | service_vs_task_state, repo_convention | m1,m2 | u1→service, u2→task, u3→repo | NONE | M | N | Corrected P5.7-D: u2→task_state |
| 10 | v05_sample_0010 | S | READ+STORE | service_invariant, sensitive, stale | m1 | u1→service, u2→task | u3 (password) | L | N | Reference-quality case |
| 11 | v05_sample_0011 | S | READ+STORE | user_profile_boundary | m1,m2,m3 | u1→service, u2→task, u3→user | NONE | L | N | Clean user_profile |
| 12 | v05_sample_0012 | S | READ+STORE | service_vs_task_state | m1,m2,m3 | u1→service, u2→task | NONE | L | N | Clean blocker vs behavior |
| 13 | v05_sample_0013 | S | READ+STORE | related_but_useless, stale | m1,m2 | u1→service, u2→task | u3 (time) | L | N | Clean stale detection |
| 14 | v05_sample_0015 | S | STORE/SKIP-only | project_vs_repo, target_boundary | NONE | u1→repo, u2→project, u3→task | NONE | M | N | Kept P5.7-D: u2=project correct |
| 15 | v05_sample_0016 | S | READ+STORE | sensitive, related_but_useless | m1 | u1→repo | u2 (recovery code) | L | N | Sensitive SKIP correct |
| 16 | v05_sample_0017 | S | READ+STORE | stale_memory | m1 | u1→service, u2→repo, u3→task | NONE | L | N | All three targets |
| 17 | v05_sample_0018 | S | READ+STORE | project_vs_repo, target_boundary | m1,m2 | u1→task, u2→project | u3 (time) | M | N | Kept P5.7-D: u2=project correct |
| 18 | v05_sample_0019 | S | READ+STORE | sensitive, related_but_useless | m1 | u1→service, u3→service | u2 (location) | L | N | Sensitive SKIP correct |
| 19 | v05_sample_0020 | S | READ+STORE | stale, target_boundary | m1,m2 | u1→service, u2→repo | u3 (laptop) | L | N | Kept P5.7-D: u3=SKIP |
| 20 | v05_sample_0021 | S | READ+STORE | service_vs_task_state, repo_convention | m1,m2 | u1→service, u2→task, u3→repo | NONE | L | N | Clean boundary. See §7 full review |
| 21 | v05_batch50_0001 | N | READ-only | stale, temporary_request | m1,m2 | NONE | u1 (question) | L | N | Clean |
| 22 | v05_batch50_0002 | N | READ-only | stale, related_but_useless | m1 | NONE | u1 (debug) | L | N | Clean stale detection |
| 23 | v05_batch50_0003 | N | READ-only | temporary_request, related | m1,m2 | NONE | u1 (knowledge q) | L | N | Clean READ selectivity |
| 24 | v05_batch50_0004 | N | READ-only | related_but_useless, temporary | m1,m2 | NONE | u1 (debug query) | L | N | Skips m3 correctly |
| 25 | v05_batch50_0005 | N | READ-only | related_but_useless, temporary | m2 | NONE | u1 (factual q) | L | N | Only reads exact answer m2 |
| 26 | v05_batch50_0006 | N | STORE/SKIP-only | service_vs_task_state, repo_convention | NONE | u1→service, u2→task, u3→repo | NONE | L | N | Clean WHAT vs HOW vs WHERE |
| 27 | v05_batch50_0007 | N | STORE/SKIP-only | service_vs_task_state, project_vs_repo, target_boundary | NONE | u1→service, u2→task, u3→project | NONE | M | Y | u3 training approach as project_memory — is this project-level enough? |
| 28 | v05_batch50_0008 | N | STORE/SKIP-only | repo_vs_service, sensitive | NONE | u1→service, u2→repo | u3 (email) | L | N | Sensitive SKIP correct |
| 29 | v05_batch50_0009 | N | STORE/SKIP-only | project_vs_repo, user_profile, target_boundary | NONE | u1→project, u2→repo, u3→user | NONE | M | N | Three-way boundary. u1 (scope exclusion) = project is solid. u3 = user_profile is correct |
| 30 | v05_batch50_0010 | N | STORE/SKIP-only | repo_vs_service, sensitive | NONE | u1→service, u2→repo | u3 (access key) | L | N | Synthetic access key SKIPped |
| 31 | v05_batch50_0011 | N | STORE/SKIP-only | service_vs_task_state, repo_convention | NONE | u1→service, u2→task, u3→repo | NONE | L | N | Clean perpetual rule vs current gap |
| 32 | v05_batch50_0012 | N | STORE/SKIP-only | repo_convention, temporary | NONE | u1→repo, u2→repo | u3 (reminder) | L | N | Dual repo_memory is valid |
| 33 | v05_batch50_0013 | N | READ+STORE | service_invariant, task_progress, stale, repo_vs_service | m1 | u1→service, u2→service, u3→task | NONE | L | N | Clean stale detection for m2,m3 |
| 34 | v05_batch50_0014 | N | READ+STORE | service_invariant, sensitive, user_profile | m1,m2 | u1→service, u3→repo | u2 (address) | L | N | Reads m2 (user pref) because CRITICAL interacts with silent hours. Address correctly SKIPped |
| 35 | v05_batch50_0015 | N | READ+STORE | service_invariant, task_progress, related | m1,m3 | u1→service, u2→task | NONE | L | N | Skips project-level m2 correctly |
| 36 | v05_batch50_0016 | N | READ+STORE | service_invariant, task_progress, sensitive | m1,m2,m3 | u1→service, u2→task | u3 (API key) | L | N | API key SKIPped. m3 tells us downstream constraint |
| 37 | v05_batch50_0017 | N | READ+STORE | project_vs_repo, target_boundary, related | m1,m2 | u1→task, u2→project, u3→task | NONE | M | Y | u2 synthetic-data-only as project_memory. Same as v05_sample_0006. Is it definitely project-level? |
| 38 | v05_batch50_0018 | N | READ+STORE | task_progress, service_vs_task_state, target_boundary | m1,m2 | u1→task, u2→task | NONE | M | N | Both task_state: experiments, not durable behaviors. Important teaching case |
| 39 | v05_batch50_0019 | N | READ+STORE | repo_convention, task_progress, stale | m1,m2 | u1→repo, u2→task | NONE | L | N | Clean stale m3 skip |
| 40 | v05_batch50_0020 | N | READ+STORE | service_invariant, task_progress, service_vs_task | m1,m2 | u1→service, u2→task | u3 (speculation) | L | N | u3 speculation correctly SKIPped |
| 41 | v05_batch50_0021 | N | READ+STORE | service_invariant, stale | m1,m2 | u1→service, u2→service | NONE | L | N | Dual service_memory valid. Stale m3 skip correct |
| 42 | v05_batch50_0022 | N | READ+STORE | service_invariant, task_progress, project_vs_repo | m1,m2,m3 | u1→service, u2→service, u3→task | NONE | L | N | m2 project_memory (SLA) used correctly |
| 43 | v05_batch50_0023 | N | STORE/SKIP-only | service_vs_task_state, target_boundary | NONE | u1→service, u2→task, u3→task | NONE | M | N | u3 "only reports" as task_state (temporary). See §6.2 |
| 44 | v05_batch50_0024 | N | STORE/SKIP-only | project_vs_repo, target_boundary | NONE | u1→project, u2→project, u3→task | NONE | M | Y | Dual project_memory. u1 (no PII) and u2 (secret manager) are both cross-service rules. Is this correct project_memory or should they be service_memory? |
| 45 | v05_batch50_0025 | N | STORE/SKIP-only | user_profile, sensitive | NONE | u1→user, u2→repo | u3 (PIN) | L | N | PIN correctly SKIPped |
| 46 | v05_batch50_0026 | N | STORE/SKIP-only | project_vs_repo, target_boundary | NONE | u1→repo, u2→task, u3→task | NONE | M | N | u1 venv+pinned deps → repo_memory (could be project_memory?). Reviewer should check |
| 47 | v05_batch50_0027 | N | READ+STORE | service_invariant, task_progress, sensitive, stale | m1 | u1→service, u2→task | u3 (webhook) | L | N | Webhook URL correctly SKIPped as sensitive |
| 48 | v05_batch50_0028 | N | READ+STORE | service_invariant, repo_vs_service | m1,m2 | u1→service, u2→service | NONE | L | N | Dual service_memory: both durable sync behaviors |
| 49 | v05_batch50_0029 | N | STORE/SKIP-only | project_vs_repo, target_boundary | NONE | u1→task, u2→project, u3→task | NONE | M | N | u2 evaluation philosophy → project_memory (correct: durable cross-version principle) |
| 50 | v05_batch50_0030 | N | READ+STORE | service_invariant, repo_convention, stale, related | m1,m2 | u1→service, u2→service, u3→repo | NONE | L | N | Rich stale detection (skips m3,m4). Clean high-watermark design |

## 3. High-Risk Cases (Human Review Needed)

### Case v05_batch50_0007 — project_memory boundary
**Why:** u3 "v0.5 training targets Qwen3-4B with LoRA, not full fine-tuning" → project_memory. Is this a project-level training strategy decision or a task_state about the current training run?
**Risk:** Medium. The choice of model and method could be seen as task_state (specific to this run) rather than project_memory (permanent project direction). However, the agent chose project_memory because training methodology (LoRA vs full fine-tuning) is a project-level architectural decision that affects all future training runs.
**Review question:** Is "Qwen3-4B + LoRA" a durable project decision or a current-run configuration?

### Case v05_batch50_0017 — synthetic-data-only as project_memory
**Why:** u2 "The project will only ever use synthetic training data; real production data is permanently out of scope" → project_memory. Same boundary issue as v05_sample_0006 (reviewed and confirmed in P5.7-D).
**Risk:** Medium. The wording "permanently out of scope" is stronger than v05_sample_0006. The agent intentionally used "only ever" and "permanently" to make the project_memory classification unambiguous. This is a deliberate replay of the v05_sample_0006 decision with clearer wording.
**Review question:** Is this sufficiently different from v05_sample_0006 to add training value, or is it redundant?

### Case v05_batch50_0024 — dual project_memory
**Why:** Both u1 (never log PII) and u2 (centralized secret manager) are labeled project_memory. These are cross-service infrastructure rules.
**Risk:** Medium. u1 could be argued as service_memory for the export service specifically. u2 could be argued as repo_memory (infrastructure setup). The agent chose project_memory because both rules apply across ALL services in the data-platform project, not just export.
**Review question:** Are cross-service operational rules project_memory or service_memory? The TARGET_GUIDELINE says project_memory is for "cross-repo or cross-service agreements" — which supports project_memory.

### Case v05_batch50_0026 — repo_memory vs project_memory
**Why:** u1 "All v0.5 training runs must use the project-local Python virtual environment under .venv/ with pinned dependencies" → repo_memory. Could also be project_memory since it's a project-wide convention.
**Risk:** Medium. The agent chose repo_memory because .venv/ and pinned dependencies are repo-level setup commands. But it's stated as applying to "all v0.5 training runs" which sounds like a project convention. Reviewer should confirm.
**Note:** Agent flagged this in notes: "reviewer should check whether u1 is better as project_memory."

## 4. Target-Boundary Audit

### 4.1 project_memory vs task_state

Cases with this boundary (both tags present or explicit in notes):

| Case | project_memory unit | task_state unit | Assessment |
| --- | --- | --- | --- |
| v05_sample_0006 | u1: synthetic data only | u2: add retry wrapper | ✓ Confirmed P5.7-D (permanent) |
| v05_sample_0015 | u2: no MemoryOS | u3: write plan today | ✓ Confirmed P5.7-D |
| v05_sample_0018 | u2: routing metrics > loss | u1: LoRA rank 8 | ✓ Confirmed P5.7-D |
| v05_batch50_0007 | u3: Qwen3-4B + LoRA | u2: add bar chart | **Review needed** |
| v05_batch50_0017 | u2: synthetic only forever | u1/u3: split/task | **Review needed** (see §3) |
| v05_batch50_0024 | u1: no PII, u2: secret mgr | u3: add PII masking | **Review needed** (see §3) |
| v05_batch50_0029 | u2: routing-specific eval | u1/u3: priority/write | Clean: principle vs instantiation |

**Finding:** project_memory usage is generally conservative and well-justified. The few cases flagged for review are about whether specific rules are truly project-level or should be one level lower.

### 4.2 service_memory vs task_state

| Case | service_memory unit | task_state unit | Assessment |
| --- | --- | --- | --- |
| v05_sample_0004 | u1: eval_runner metrics | u2: run on subset50 | ✓ Clean |
| v05_sample_0009 | u1: per-tag breakdown | u2: single-turn limitation | ✓ Corrected P5.7-D |
| v05_sample_0012 | u1: SHA-256 checksum | u2: IAM blocked | ✓ Clean |
| v05_sample_0021 | u1: deduplication | u2: integrate retry | ✓ Clean (see §7) |
| v05_batch50_0006 | u1: 10% deviation rule | u2: implement check | ✓ Clean WHAT vs HOW |
| v05_batch50_0011 | u1: never guess target | u2: no STORE/SKIP conflict check | ✓ Clean perpetual vs current |
| v05_batch50_0018 | — | u1/u2: both task_state | ✓ Important: service-domain experiments are task_state |
| v05_batch50_0023 | u1: calibration metric | u2/u3: implement, current limitation | ✓ Clean. u3 as task_state: limitation is temporary |
| v05_batch50_0020 | u1: leakage check rule | u2: add before batch50 | ✓ Clean |

**Finding:** The service_memory vs task_state boundary is generally clean. The key insight cases are v05_batch50_0018 (all task_state for experiments) and v05_batch50_0023 (current limitation as task_state when the limitation is temporary/being addressed).

### 4.3 repo_memory vs service_memory

| Case | repo_memory unit | service_memory unit | Assessment |
| --- | --- | --- | --- |
| v05_sample_0005 | u1: test path | u2: parser behavior | ✓ Clean |
| v05_sample_0008 | u2: source path | u1: validator behavior | ✓ Clean |
| v05_batch50_0008 | u2: permissions code path | u1: rationale dialog rule | ✓ Clean |
| v05_batch50_0010 | u2: KMS terraform path | u1: encryption behavior | ✓ Clean |
| v05_batch50_0030 | u3: metadata table | u1/u2: incremental load | ✓ Clean |

**Finding:** Repo vs service distinctions are straightforward and low-risk. Path/command → repo, behavior/rule → service.

### 4.4 user_profile vs sensitive/private

| Case | user_profile unit | sensitive SKIP unit | Assessment |
| --- | --- | --- | --- |
| v05_sample_0007 | u1: tradeoff explanations | u3: phone number | ✓ Clean |
| v05_sample_0011 | u3: concise prompts | — | ✓ Clean |
| v05_batch50_0009 | u3: examples before definitions | — | ✓ Clean |
| v05_batch50_0025 | u1: photo mode default | u3: device PIN | ✓ Clean |

**Finding:** user_profile is used only for stable, non-sensitive preferences. All personal contact info, PINs, credentials are correctly SKIPped.

## 5. Sensitive / Private Audit

All 11 sensitive_boundary cases audited:

| Case | Sensitive content | Stored? | Status |
| --- | --- | --- | --- |
| v05_sample_0005 | backup email | No (SKIP) | ✓ |
| v05_sample_0007 | phone number 555-0198 | No (SKIP) | ✓ |
| v05_sample_0010 | test password testpass_1234 | No (SKIP) | ✓ |
| v05_sample_0016 | recovery code ABCD-1234-EFGH | No (SKIP) | ✓ |
| v05_sample_0019 | location history request | No (SKIP) | ✓ |
| v05_batch50_0008 | personal email devtest123@gmail.com | No (SKIP) | ✓ |
| v05_batch50_0010 | AWS access key AKIA1234567890ABCDEF | No (SKIP) | ✓ |
| v05_batch50_0014 | home address 1234 Rural Route 7 | No (SKIP) | ✓ |
| v05_batch50_0016 | Stripe API test key sk_test_... | No (SKIP) | ✓ |
| v05_batch50_0025 | device unlock PIN 123456 | No (SKIP) | ✓ |
| v05_batch50_0027 | Slack webhook URL | No (SKIP) | ✓ |

**All 11 sensitive cases correctly SKIPped. 0 sensitive units in STORE.**  
All sensitive values use obvious synthetic placeholders.

## 6. Related / Stale Audit

Cases where memories should NOT be read:

| Case | Memory | Reason | Status |
| --- | --- | --- | --- |
| v05_batch50_0001 | m3 (old v1 pipeline) | Stale — legacy cron scheduling | ✓ |
| v05_batch50_0002 | m2 (old camera bug) | Stale — different bug, old release | ✓ |
| v05_batch50_0003 | m3 (project schema) | Related but not about validator checks | ✓ |
| v05_batch50_0004 | m3 (yesterday's count) | Stale task state — doesn't explain missing invoice | ✓ |
| v05_batch50_0005 | m1 (max capacity) | Related but not the warning threshold | ✓ |
| v05_batch50_0013 | m2 (old deadlock), m3 (legacy MySQL) | Stale + stale | ✓ |
| v05_batch50_0015 | m2 (project-level v0.4/v0.5) | Related but not needed for implementation | ✓ |
| v05_batch50_0017 | m3 (eval_runner) | Related to gold lock concept but not needed | ✓ |
| v05_batch50_0019 | m3 (three-week-old rename) | Stale task state | ✓ |
| v05_batch50_0021 | m3 (old sprint planning note) | Stale — not current | ✓ |
| v05_batch50_0027 | m2 (legacy error queue) | Stale — different architecture | ✓ |
| v05_batch50_0030 | m3 (old partition), m4 (legacy CDC) | Stale + stale legacy | ✓ |

**All stale/related-but-useless decisions appear correct.**

## 7. v05_sample_0021 Full Review

This is the replacement case from P5.7-D, specifically designed as a clean service_memory vs task_state reference case.

**Runtime Context:**
- project: mobile-field
- repo: field-app
- service: notification
- task: add push notification retry logic

**Candidate Memories:**
- m1 [service_memory]: notification service delivers via Firebase Cloud Messaging with 30s timeout
- m2 [repo_memory]: config lives in config/notification.yaml

**Current Units:**
- u1: "The notification service must deduplicate messages by notification_id within a 5-minute window to prevent double-delivery."
- u2: "Integrate the notification retry into the existing sync retry wrapper that already handles 429 responses."
- u3: "Write the FCM credential setup guide in docs/notification/fcm_setup.md."

**Gold DSL:** `READ m1,m2 / STORE service_memory u1 / STORE task_state u2 / STORE repo_memory u3 / SKIP NONE`

### Why u1 is service_memory

u1 defines a durable deduplication behavior for the notification service. It specifies:
- WHAT the service must do (deduplicate by notification_id)
- The constraint (5-minute window)
- The purpose (prevent double-delivery)

This is a component-level behavioral invariant. It describes the service's interface/behavior, not what the current task is doing. Even after the retry logic task is complete, this deduplication rule persists as a service behavior.

**Key signal:** The phrase "must deduplicate" (not "should add deduplication" or "currently needs deduplication"). The modal "must" indicates a perpetual requirement.

### Why u2 is task_state

u2 describes the current implementation plan: integrating notification retry into the existing sync retry wrapper. It specifies:
- HOW to implement it now (integrate into existing wrapper)
- A current action/next step
- References a specific existing component (sync retry wrapper)

This is clearly a task-level decision. Once the integration is done, this unit is no longer current. The instruction is tied to the current implementation phase.

**Key signal:** "Integrate... into the existing..." is an implementation directive, not a behavioral specification. It's about HOW, not WHAT.

### Why u3 is repo_memory

u3 says where to store documentation: `docs/notification/fcm_setup.md`. This is a repo-level path convention.

### Cleanliness assessment

**No ambiguous wording.** The case avoids:
- "currently should" (present in the removed v05_sample_0014)
- "still only" / "currently does" with unclear permanence
- "should show" (future spec vs current behavior ambiguity)

**Clear semantic categories:**
- WHAT the service does → service_memory (u1)
- HOW to implement now → task_state (u2)
- WHERE the docs live → repo_memory (u3)

**Verdict:** v05_sample_0021 is clean. It serves well as a reference case for service_memory vs task_state. No human_review_needed.

## 8. Scale Readiness Judgment

### Strengths
- 50 cases cover all 5 targets with reasonable distribution
- All shapes (READ-only, STORE/SKIP-only, READ+STORE joint) represented
- Sensitive boundary cases handled correctly (11/11)
- Stale/related memory detection working (12 cases)
- All structural validations pass
- No leakage to subset50/few-shot/seed20
- v05_sample_0021 provides a clean reference case

### Weaknesses
- 3 cases flagged for human review (batch50_0007, 0017, 0024)
- user_profile at minimum count (4) — needs more representation
- Only 3 project domains (memory-router, mobile-field, data-platform)
- project_memory still has boundary ambiguity in some cases
- All single-turn — multi-turn training not addressed

### Readiness: **Conditional — proceed to 100 with targeted additions**

The batch50 is structurally valid and semantically mostly sound. Before scaling to 100:
1. Review the 3 flagged cases
2. Add 5-10 more user_profile cases
3. Add 2-3 more project domains for variety
4. Consider adding project_memory edge cases reviewed by human

The batch50 can serve as a template base for the next scale step.
