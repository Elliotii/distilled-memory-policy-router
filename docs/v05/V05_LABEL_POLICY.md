# V0.5 Label Policy

Version: v0.5  
Date: 2026-06-01  
Status: Derived from batch100 audit lessons; governs 500-case generation

## 1. user_profile

**Definition:** Stable, non-sensitive, cross-project user preferences.

**Examples (STORE as user_profile):**
- "I prefer architecture explanations that name tradeoffs explicitly."
- "I prefer concise prompts with examples before rules when learning new APIs."
- "I prefer flight search results sorted by total price including taxes, not base fare."

**Negative examples (SKIP):**
- "My phone number is 555-0198." → SKIP (sensitive)
- "My API key is sk-live-..." → SKIP (secret)
- "Enable HDR mode by default." → repo_memory (app-specific setting)

## 2. project_memory

**Definition:** Project-level goals, scope decisions, global constraints, cross-repo/service agreements. Must NOT be a catch-all.

**Examples (STORE as project_memory):**
- "The project does not implement a full MemoryOS; it only studies the memory policy router layer."
- "The data-platform pilot uses synthetic service scenarios only; no real production data."
- "All finboard services must use TLS 1.3 for inter-service communication." (explicit cross-service)
- "The finboard project must comply with SOC 2 data integrity requirements for all financial reports."

**Negative examples:**
- "The export service must never log PII." → service_memory (names a specific service)
- "Run pytest before merging." → repo_memory (repo-level command)
- "Next, add a retry wrapper." → task_state (current task)

## 3. repo_memory

**Definition:** Repository-specific facts: paths, commands, directory structure, test conventions, code norms.

**Examples (STORE as repo_memory):**
- "Parser tests should live under tests/v04/ and run with pytest tests/v04/."
- "The case validator source lives under src/v04/case_validator.py."
- "v0.5 training documentation should go under docs/v05/."

**Negative examples:**
- "The parser converts DSL to canonical JSON." → service_memory (component behavior)
- "v0.4 is an interface pilot." → project_memory (project-level decision)

## 4. service_memory

**Definition:** Durable behavior, interfaces, dependencies, constraints, invariants of a specific service/module/component.

**Examples (STORE as service_memory):**
- "The parser must never guess or infer missing STORE targets from unit text."
- "The eval_runner computes READ F1, STORE unit F1, STORE target accuracy, SKIP F1."
- "The notification service must deduplicate messages by notification_id within a 5-minute window."
- "The aggregator must reject any input row where the transaction amount is negative and not flagged as a refund."

**Negative examples:**
- "Add a SHA-256 checksum validation step." → task_state (implementation action)
- "Use LoRA with rank 8." → task_state (current training plan)
- "All services must use TLS 1.3." → project_memory (cross-service rule)

## 5. task_state

**Definition:** Current task progress, next steps, blockers, active constraints, version-specific configurations, temporary plans.

**Examples (STORE as task_state):**
- "The eval_runner has been run on subset50 but not yet on full pilot."
- "The export job is blocked until the IAM role is updated."
- "Write parser tests for the new duplicate assignment check."
- "Add incremental indexing that only processes documents changed since the last indexed commit." (implementation plan)
- "The v0.5 training targets Qwen3-4B with LoRA, not full fine-tuning." (version-scoped config)

**Negative examples:**
- "The parser must never guess targets." → service_memory (permanent design invariant)
- "The project does not implement MemoryOS." → project_memory (permanent scope decision)

## 6. Sensitive/Private → ALWAYS SKIP

Anything resembling credentials, personal data, secrets must be SKIPped:
- Passwords, API keys, tokens, private keys
- Phone numbers, email addresses, home addresses
- Recovery codes, PINs, passport numbers
- Credit card numbers, bank details
- Webhook URLs, database connection strings

**Examples (SKIP):**
- "My test account password is testpass_1234."
- "My phone number is 555-0198."
- "My Stripe API test key is sk_test_..."
- "The Slack webhook URL is https://hooks.slack.com/..."

**Important:** Even synthetic placeholders must be SKIPped. The model must learn that credential-like content is never stored, regardless of being obviously fake.

## 7. service_memory vs task_state (THE KEY BOUNDARY)

This is the most important distinction in the batch100 audit.

**Rule of thumb:**
- "**Add** / Implement / Integrate / Build / Update / Draft / Next / Currently missing / For this version" → usually **task_state**
- "**The service does** / must / requires / rejects / returns / stores / writes" → usually **service_memory**

**If a unit mixes action phrasing with durable behavior description, prefer task_state unless the durable behavior is the dominant semantic content.**

**Examples of the boundary:**

| Unit | Should be | Why |
| --- | --- | --- |
| "Add incremental indexing that only processes documents changed since the last indexed commit." | task_state | Implementation plan dominates |
| "Add a dark mode toggle that switches chart colors to a dark palette." | task_state | UI feature, implementation |
| "The notification service must deduplicate messages by notification_id within a 5-minute window." | service_memory | Durable behavior specification |
| "Add a deadlock retry wrapper that catches PostgreSQL error 40P01 and retries up to 3 times with 1-second backoff." | service_memory | Detailed behavioral algorithm dominates over "Add" framing |
| "The aggregator must reject any input row where the transaction amount is negative and not flagged as a refund." | service_memory | Durable validation rule |

**For training data generation:** Prefer writing durable service specs without action verbs. Write "The service deduplicates messages by notification_id" not "Add deduplication to the service."

## 8. project_memory vs task_state

- **project_memory:** Durable project-level scope, strategy, policy. Transcends individual tasks.
- **task_state:** Current task plan, version-specific configuration, next step, blocker.

**Key test:** Would this still be true in v1.0? If yes → project_memory. If maybe not → task_state.

**Examples:**
- "The project will only ever use synthetic training data." → project_memory (permanent scope)
- "v0.5 training targets Qwen3-4B with LoRA." → task_state (version-specific, model-specific)
- "The project scope explicitly excludes retriever training." → project_memory (permanent scope exclusion)

## 9. repo_memory vs service_memory

- **repo_memory:** WHERE things live (paths, file locations, commands, directory conventions)
- **service_memory:** WHAT things DO (behavior, interface, constraints, invariants)

**Examples:**
- "Parser tests should live under tests/v04/." → repo_memory (path)
- "The parser rejects unknown STORE targets." → service_memory (behavior)

## 10. user_profile vs sensitive/private

- **user_profile:** Stable, non-sensitive, reusable across projects. Preferences, style choices, defaults.
- **sensitive:** Personal identifying information, credentials, secrets. ALWAYS SKIP.

**Test:** Would you put this in a public GitHub profile? If yes → user_profile. If no → SKIP.

**Examples:**
- "I prefer concise prompts with examples before rules." → user_profile (safe preference)
- "My personal backup email is abc16-backup@example.com." → SKIP (personal contact info)
- "I prefer flight results sorted by total price." → user_profile (safe preference)
- "My passport number is P12345678." → SKIP (personal identifying information)
