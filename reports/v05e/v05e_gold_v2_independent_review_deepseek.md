# V0.5e gold_v2 Independent Review — DeepSeek

**Date:** 2026-06-04
**Reviewer:** DeepSeek (automated audit + manual inspection)
**Status:** Independent review only — no data modified, no models run

---

## Verdict

**CORRECTION REQUIRED**

The domain name overlap with train_500 (`ecommerce-platform` / `shopengine` / `cart-service`) violates the pre-registered construction constraint that gold_v2 be "independent from all existing data." Additionally, several protocol distribution targets are out of range, and template diversity is critically low. The 24 affected cases must be regenerated with a genuinely new domain before evaluation.

---

## Checks Run

| # | Check | Result |
|---|-------|--------|
| 1 | Active cases = 150 | ✅ PASS |
| 2 | Holdout cases = 30 | ✅ PASS |
| 3 | Active/holdout separation | ✅ PASS (zero ID overlap, distinct prefixes) |
| 4 | Lock hash integrity | ✅ PASS (all 4 hashes match) |
| 5 | Target legality (5 legal targets only) | ✅ PASS (0 illegal targets in stores or memories) |
| 6 | Sensitive units in STORE | ✅ PASS (0 sensitive units stored across active+holdout) |
| 7 | Schema validation | ✅ PASS (0 errors) |
| 8 | SFT JSON parse | ✅ PASS (180/180 parse clean, 0 markdown) |
| 9 | SFT ↔ gold consistency | ✅ PASS (assistant JSON matches gold labels for all cases) |
| 10 | Leakage: train_500 | ⚠️ REVIEW (domain name overlap, see below) |
| 11 | Leakage: dev | ✅ PASS (0 ID, 0 exact, 0 near-dup, 0 domain) |
| 12 | Leakage: old gold | ✅ PASS (0 ID, 0 exact, 0 near-dup, 0 domain) |
| 13 | Leakage: few-shot exemplars | ✅ PASS (0 overlap on all dimensions) |
| 14 | Leakage: surface strings (phone/email/token) | ✅ PASS (0 shared values) |
| 15 | Distribution: shapes | ✅ PASS (within protocol range) |
| 16 | Distribution: targets | ⚠️ REVIEW (user_profile out of range) |
| 17 | Distribution: stress axes | ⚠️ REVIEW (both sensitive and boundary exceed protocol) |
| 18 | Template diversity | ⚠️ REVIEW (critically low unique-unit ratio) |
| 19 | Sensitive label plausibility | ✅ PASS (all sensitive units correctly SKIP-labeled) |
| 20 | Boundary label plausibility | ✅ PASS (sample inspected, labels are reasonable) |
| 21 | user_profile vs sensitive audit | ✅ PASS (0 PII stored as user_profile) |
| 22 | Fairness for 4-system comparison | ⚠️ REVIEW (domain leakage favors LoRA systems) |
| 23 | SFT assistant JSON parse (100%) | ✅ PASS |

---

## Protocol Compliance

### Shape Distribution

| Shape | Actual (n=150) | Protocol Target | Status |
|-------|:-------------:|:---------------:|:------:|
| READ-only | 28 (18.7%) | ~27 (18%) | ✅ |
| STORE/SKIP-only | 58 (38.7%) | ~58 (39%) | ✅ |
| READ+STORE joint | 64 (42.7%) | ~65 (43%) | ✅ |

Shapes are within ±1 of protocol targets. **Compliant.**

### Target Distribution (STORE units, n=232)

| Target | Actual | % | Protocol | Status |
|--------|:------:|:--:|:--------:|:------:|
| task_state | 73 | 31.5% | ~33% | ✅ |
| service_memory | 71 | 30.6% | ~32% | ✅ |
| repo_memory | 41 | 17.7% | ~17% | ✅ |
| project_memory | 28 | 12.1% | ~12% | ✅ |
| user_profile | 19 | **8.2%** | ~6% | ⚠️ **2.2pp over** |

user_profile at 8.2% exceeds the protocol target of ~6% by 2.2pp. The protocol allows ±3pp, so this is technically within the 3pp tolerance, but it is at the upper edge. The higher user_profile rate means more preference-style units, which are among the easiest to classify (dashboard preferences, error format preferences). This may slightly inflate target accuracy metrics.

**Marginal compliance.** Acceptable under ±3pp tolerance but contributes to an easier evaluation set.

### Stress Axes

| Axis | Actual | Protocol Range | Status |
|------|:------:|:--------------:|:------:|
| Sensitive SKIP | **30** | 18-27 | ❌ **Over by 3** |
| Target boundary | **45** | 30-38 | ❌ **Over by 7** |

**Both stress axes exceed protocol maxima.** The construction report acknowledges sensitive is "slightly over" but frames it as beneficial ("more sensitive cases improve safety evaluation"). The boundary excess (45 vs 38) is not acknowledged. This deviation matters because:
- More boundary cases make the set harder on target classification (favoring systems with stronger target routing)
- More sensitive cases make the set marginally harder on SKIP classification (favoring systems better at recognizing PII)

**Non-compliant.** The protocol ranges were pre-registered. Deviations need explicit justification and should be documented as protocol amendments, not presented as compliant.

### Domains

| Domain | Active Cases |
|--------|:------------:|
| edu-platform | 27 |
| iot-monitoring | 27 |
| legal-doc-review | 25 |
| ecommerce-platform | 24 |
| inventory-mgmt | 24 |
| support-ticketing | 23 |

Six domains, all distinct from old gold's six domains. Domain distribution is reasonably balanced (23-27 each).

**Old gold domain overlap:** NONE. **Compliant.**

**New domain quality:** The six domains are plausible and distinct (edu, IoT, legal, ecommerce, inventory, support). However, they are all "microservice CRUD/SLA" domains — there is no genuine domain diversity in terms of task type. Every domain uses the same memory templates, the same unit templates, and the same scenario types. See Template/Diversity Audit below.

---

## Leakage Audit

### Hard Blocker Results (L0-L2)

| Corpus | L0 (ID overlap) | L1 (Exact text) | L2 (Near-dup J≥0.9) |
|--------|:---:|:---:|:---:|
| train_500 | 0 | 0 | 0 |
| dev | 0 | 0 | 0 |
| old gold | 0 | 0 | 0 |
| few-shot exemplars | 0 | 0 | 0 |

**All hard blockers pass.** No exact text, ID, or near-duplicate leakage.

### Domain Name Overlap (L3 — Scenario Collision)

**CRITICAL FINDING:** The domain name `ecommerce-platform`, the repo name `shopengine`, and the service name `cart-service` all appear in both train_500 and gold_v2.

| Aspect | train_500 | gold_v2 |
|--------|-----------|---------|
| Project | ecommerce-platform | ecommerce-platform |
| Repo | shopengine | shopengine |
| Service containing "cart-service" | Yes (1 of 15 services) | Yes (the ONLY service) |
| ecommerce-platform cases | 44 / 500 (8.8%) | 24 / 150 (16.0%) |

Additionally, three other service/repo names overlap:
- `learnhub` (in train "learning-assistant" project, in gold_v2 "edu-platform")
- `alert-manager` (in train "customer-support" project, in gold_v2 "iot-monitoring")
- `shopengine` (shared, as above)

**Why this matters for the r=16 vs r=8 comparison:**

The LoRA systems (r=16, r=8, Qwen3-4B r=8) were trained on train_500. This training data includes 44 cases in the `ecommerce-platform` / `shopengine` domain. When these systems encounter gold_v2 cases from the same project/repo, they benefit from **domain-name memorization**: the model has learned associations between the project name "ecommerce-platform," the repo name "shopengine," and the types of outputs expected. This is not content leakage (no specific texts overlap), but it is **namespace leakage** — the model has a familiarity advantage.

The few-shot baseline (Qwen3.5 JSON few-shot) sees no training data and thus gains no such advantage. This makes the comparison **unfair**: LoRA systems get a ~16% "home field advantage" that the few-shot baseline does not.

The pre-registered construction constraint states: "Independent from all existing data: train_500, dev, old gold, few-shot exemplars." The domain name overlap violates this constraint.

**Surface string patterns (L3b):**

| Pattern | Old datasets | gold_v2 | Overlap |
|---------|:-----------:|:------:|:------:|
| Phone numbers (+1-555-XXXX) | 4 | 6 | 0 |
| Email addresses | 10 | 5 | 0 |
| API tokens/keys | 0 | 4 | 0 |

All surface strings are unique. **Compliant.**

### Few-Shot Exemplar Leakage

- 0 ID overlap
- 0 exact text overlap
- 0 domain/service/repo name overlap
- 0 surface string overlap

**Fully clean.**

---

## Distribution Audit

### Per-Domain Shape and Target Breakdown

All six domains have similar distributions due to the round-robin generation. This is a design choice — not a bug — but it means domain identity is not predictive of shape or target. The set is balanced across domains, which is good for evaluation fairness.

### STORE Units Per Case

Active set has 232 STORE units across 150 cases = ~1.55 STORE units/case on average. This is slightly lower than old gold (~2.2 STORE/case) because gold_v2 has more STORE/SKIP-only cases with 2-3 units each.

### READ Selectivity

Of the 28 READ-only cases, 15 have `read_selectivity` tags, meaning not all non-stale memories are read. The remaining 13 read all non-stale memories. This provides variation in READ difficulty.

---

## Sensitive / Boundary Label Audit

### Sensitive Cases (30 active)

| Subtype | Count |
|---------|:-----:|
| Phone | 6 |
| Email | 5 |
| ID (SSN, employee ID) | 5 |
| Payment (credit card) | 4 |
| Credential (API key, token) | 3 |
| Address | 1 |
| **Unaccounted** | **6** |

Note: 6 sensitive cases tag as `sensitive_boundary` in case-level tags but have no specific sensitive subtype tag on any unit. These are edge cases where the sensitive unit tagging may be incomplete. All 30 cases correctly place the sensitive unit in `skip`, so this is a metadata issue, not a label quality issue.

**Label quality:** In all 30 sensitive cases, the sensitive unit is correctly placed in `skip` (0 false STOREs). The subtypes cover all required categories: phone, email, address, credential, payment, ID.

### Boundary Cases (45 active)

Sampled 5 boundary cases for manual label plausibility check:

| Case | Boundary Type | Assessment |
|------|---------------|------------|
| v05e_gold_active_0018 | svc vs task_state vs user vs proj all in one case | ✅ Reasonable |
| v05e_gold_active_0021 | proj vs payment SKIP | ✅ Clear case |
| v05e_gold_active_0022 | user_profile vs payment SKIP | ✅ Clear case |
| v05e_gold_active_0024 | svc (SLA) labeled as boundary | ⚠️ Weak — SLA text is clearly service_memory, boundary tag may be overly applied |
| v05e_gold_active_0027 | svc vs proj | ✅ Reasonable |

**Concern:** Some `target_boundary` tags seem mechanically applied (every case flagged `is_bnd=True` gets the tag, regardless of whether a genuine boundary exists). For example, case 0024 has a straightforward service_memory SLA unit tagged as boundary with no competing alternative. This inflates the boundary count.

### User Profile STORE Audit (19 units)

All 19 user_profile STORE units are legitimate preferences:
- Dashboard preferences (line charts, heatmaps, gauges): 10
- Error format preferences (runbook link): 5
- Timestamp format preferences: 2
- CR comment preferences: 2

**0 false positives.** No PII, credentials, or sensitive content stored as user_profile. This is a critical safety property that gold_v2 correctly enforces.

---

## Template / Diversity Audit

### Template Inventory

| Template | Instances (active) | % of units |
|----------|:------------------:|:----------:|
| "SLA requires X% uptime with Yms p95" | 85 | 19.5% |
| "Root cause of X: connection pool exhaustion" | 49 | 11.3% |
| "Run `make test-X`..." | 29 | 6.7% |
| "X project requires all PRs to pass security scan" | 22 | 5.1% |
| "X CI pipeline must run integration tests" | 20 | 4.6% |
| "services must use shared logging lib" | 12 | 2.8% |
| **Total fill-in-the-blank** | **217** | **49.9%** |

**Nearly half of all units (49.9%) are fill-in-the-blank templates** where only the service/repo/project name changes.

### Unit Duplication

- Total unit instances: 435
- Unique unit texts: 168 (38.6%)
- Duplicate unit texts (same text in ≥2 cases): 91

Most egregious examples:
- "Root cause of cart-service issue: connection pool exhaustion in DB layer..." appears 12 times
- "Root cause of alert-manager issue: connection pool exhaustion..." appears 11 times
- Same SLA text variants appear dozens of times with only numeric differences (99.9 vs 99.95 vs 99.99)

### Memory Template Recycling

- Total memory instances: 586
- Unique memory texts: 138 (23.5%)
- Only 47 unique templates when service names are masked

The same 8 service_memory templates are reused across all 6 domains ("The X processes requests synchronously," "The X caches results for 5 min in Redis," etc.). The same 8 repo_memory templates, 4 project_memory templates, and 4 user_profile templates are recycled identically.

### Assessment

This is a **severe template diversity problem.** gold_v2 is not a set of 150 independently constructed cases — it is a set of ~15-20 template patterns with slots filled by a cartesian product of 6 domains × N templates. The "Root cause...connection pool" text appears 49 times with only the service name varying; a model that learns the pattern "if text contains 'root cause' AND mentions current service, target=task_state" will get dozens of free correct answers.

This inflates measured performance for all systems and reduces the statistical value of n=150. The effective sample size for distinguishing systems is closer to the number of distinct template patterns (~20) than the number of cases (150), because cases sharing the same template are not independent observations.

**Recommendation:** For future gold sets, templates should be diversified. At minimum, "Root cause" cases should have varied root causes (not all "connection pool exhaustion"), SLA cases should have varied SLA descriptions, and project/repo templates should have different phrasings.

---

## Concerns

### 1. BLOCKER: train_500 domain name leakage

`ecommerce-platform`, `shopengine`, and `cart-service` appear in both train_500 and gold_v2. This violates the pre-registered independent-construction constraint and gives LoRA systems an unfair advantage over the few-shot baseline. **24/150 (16%) of active cases are affected.**

### 2. SIGNIFICANT: Protocol distribution deviations

Sensitive (30) exceeds protocol max (27) by 3. Boundary (45) exceeds protocol max (38) by 7. user_profile (8.2%) at the upper edge of the ±3pp tolerance. These deviations were pre-registered; exceeding them without amendment undermines the pre-registration.

### 3. SIGNIFICANT: Critical template diversity shortage

Only 38.6% of unit texts are unique. Nearly 50% of units are fill-in-the-blank templates. The effective sample size for distinguishing systems is much smaller than n=150. This inflates all performance metrics and reduces the statistical power of the paired bootstrap.

### 4. MODERATE: Mechanical boundary tagging

Some `target_boundary` tags appear to be mechanically applied during generation rather than reflecting genuine classification difficulty. This inflates the boundary count (45 vs protocol 30-38) without adding real difficulty.

### 5. MODERATE: Service name confusion across domains

Memory texts frequently reference services from other domains (e.g., an edu-platform case has memories about "reorder-engine" and "shopengine"). While this is a legitimate difficulty feature (testing whether models are distracted by cross-domain memories), the systematic pattern makes it predictable rather than natural.

### 6. MINOR: Sensitive subtype tagging gaps

6 sensitive cases tagged at the case level (`sensitive_boundary`) lack unit-level sensitive subtype tags. This is a metadata quality issue that does not affect label correctness.

### 7. MINOR: SFT system prompt re-encodes labeling policy

The SFT system prompt includes detailed rules about SKIP vs STORE. While this is appropriate for SFT training, it means the SFT messages are not just supervision — they encode the labeling policy in the system prompt. This makes the SFT format slightly different from what few-shot evaluation uses.

---

## Required Fixes Before Evaluation

### Must-Fix (Blockers)

1. **Replace ecommerce-platform domain**: Regenerate the 24 active and 5 holdout cases that use `ecommerce-platform` / `shopengine` / `cart-service` with a genuinely new domain not present in train_500 (or any other existing dataset). Verify the new domain name, repo name, and service name have zero overlap with train_500. Candidate: `healthcare-scheduling`, `energy-trading`, `agriculture-iot`, `logistics-routing`, or any domain absent from train_500's 17 domains.

2. **Re-lock after fix**: Update lock manifest with new hashes after regeneration. Increment lock version to `v05e_gold_v2_002`.

### Should-Fix (Protocol Compliance)

3. **Either adjust distributions or amend protocol**: Either reduce sensitive count to ≤27 and boundary count to ≤38, or formally amend the pre-registration to accept 30/45 as the new protocol ranges with explicit justification.

4. **Improve template diversity**: For the "Root cause" template, vary the root cause beyond "connection pool exhaustion" (e.g., "memory leak in worker pool," "race condition in distributed lock," "N+1 query in ORM," "thread starvation from synchronous I/O"). For SLA templates, vary the phrasing (e.g., "SLO for X is 99.9%," "X must respond within 200ms at p95," "availability target for X is four nines").

### Consider-Fixing (Quality)

5. **Diversify memory templates**: The same 8 service_memory templates across all 6 domains is artificial. Consider varying memory types: some services have rate limits, others have circuit breaker configs, others have feature flags, etc.

6. **Fix unit-level sensitive subtype tags**: Ensure all 30 sensitive cases have appropriate subtype tags on the sensitive unit(s), not just case-level `sensitive_boundary`.

7. **Audit mechanical boundary tags**: Review the 45 boundary-tagged cases to ensure each represents a genuine classification ambiguity, not just a generation-time flag.

---

## Final Recommendation

**Do not run evaluation on the current gold_v2.**

The domain name leakage with train_500 is a genuine independence violation that compromises the primary comparison (r=16 vs r=8 vs few-shot). The fix is straightforward: replace the 24 affected cases with a new domain.

The template diversity issue is structural (comes from programmatic generation) and harder to fix completely, but the "Root cause" template can be diversified with minimal changes to the build script. Even partial diversification would meaningfully improve the set's quality.

After fixes:
1. Re-verify all hashes
2. Re-run leakage checks against train_500 (confirm zero domain overlap)
3. Re-verify distributions are within protocol range (or amend protocol)
4. Re-lock as v05e_gold_v2_002
5. Then proceed with evaluation

The gold_v2 construction methodology (programmatic generation with controlled distributions) is sound in principle. The issues found are execution-level: a domain name collision with train_500 and overly aggressive template reuse. Both are fixable within the existing build script.

**Estimated fix effort:** Low. Change one domain definition, re-diversify ~3 templates, re-run build script, re-validate.

---

*End of Independent Review.*
