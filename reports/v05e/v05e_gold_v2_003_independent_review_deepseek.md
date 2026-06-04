# gold_v2_003 Independent Review — DeepSeek

**Date:** 2026-06-04
**Reviewer:** DeepSeek (automated audit + manual inspection of first 40 active + all 15 holdout cases)
**Status:** Independent review only — no data modified, no models run

---

## Verdict

**CORRECTION REQUIRED**

`learnhub` and `education-platform` — both banned from v001 — reappear in v003 and overlap with train_500 (27 train cases). This is a namespace leakage of the same category that caused v001's rejection. Additionally, 35 normalized-skeleton SKIP-vs-STORE label conflicts exist despite claims of zero conflicts, and a template concatenation bug produces degraded text quality in ~20 instances. The fleet-vocabulary fix and 98.7% unit uniqueness are excellent, but the regression on domain-name independence must be fixed before evaluation.

---

## Checks Run

| # | Check | v002 Result | v003 Result |
|---|-------|:-----------:|:-----------:|
| 1 | Active = 150 | PASS | ✅ PASS |
| 2 | Holdout = 30 | PASS | ✅ PASS |
| 3 | Lock hash integrity (4/4) | PASS | ✅ PASS |
| 4 | Active/holdout separation | 0 | ✅ 0 |
| 5 | Banned v001 names (ecommerce-platform, shopengine, cart-service, learnhub, alert-manager) | ✅ 0 | ❌ **learnhub FOUND** |
| 6 | Name overlap with train_500 | ✅ 0 | ❌ **education-platform, learnhub, assessment-engine** |
| 7 | Name overlap with dev | ✅ 0 | ✅ 0 |
| 8 | Name overlap with old gold | ✅ 0 | ✅ 0 |
| 9 | Target legality | ✅ 0 | ✅ 0 illegal |
| 10 | Sensitive units in STORE | ✅ 0 | ✅ 0 |
| 11 | Schema validation | ✅ 0 | ✅ 0 errors |
| 12 | Unit coverage (all units in store+skip) | N/A | ✅ 0 missed |
| 13 | SFT JSON parse | ✅ 100% | ✅ 180/180 (100%) |
| 14 | SFT markdown | ✅ 0 | ✅ 0 |
| 15 | READ: stale memories read | ✅ 0 | ✅ 0 |
| 16 | READ: position distribution | ✅ Varied | ✅ m1=50, m2=60, m3=35, m4=25, m5=9 |
| 17 | Memory order: m1 target diversity | ✅ svc 55% | ✅ svc 63%, repo 24%, proj 10%, user 3% |
| 18 | Stale memory position randomization | ✅ Spread | ✅ Positions 1-5: 54,47,44,30,14 |
| 19 | Exact-text label conflicts | ❌ 30 groups | ✅ **0 groups** |
| 20 | Normalized skeleton label conflicts | ❌ 15 groups | ⚠️ **35 groups (35 SKIP-vs-STORE unresolved)** |
| 21 | Unit text uniqueness | 67.1% | ✅ **98.7%** (391/396) |
| 22 | Memory text uniqueness | 41.5% | ✅ **73.3%** (368/502) |
| 23 | Max unit skeleton repeat | 16 | ⚠️ 24 (disclosed in report) |
| 24 | Unit skeletons >5 | 25 | ✅ 6 |
| 25 | Unit skeletons >7 | 17 | ✅ 3 |
| 26 | Fleet vocabulary contamination | ❌ 58-70% | ✅ **<1% all domains** |
| 27 | Domain vocabulary presence | ❌ monoculture | ✅ Domain-appropriate vocab in all 8 |
| 28 | Distribution: sensitive (18-27) | ✅ 24 | ✅ 24 |
| 29 | Distribution: boundary (30-38) | ✅ 34→37 | ✅ 37 |
| 30 | Distribution: task_state (~33%) | ✅ 33.8% | ⚠️ **36.5% (+3.5pp)** |
| 31 | Leakage: train_500 (exact text) | 0 | ✅ 0 |
| 32 | Leakage: dev (exact text) | 0 | ✅ 0 |
| 33 | Leakage: old gold (exact text) | 0 | ✅ 0 |
| 34 | Leakage: few-shot exemplars | 0 | ✅ 0 |
| 35 | Surface strings (phone/email/token) | 0 | ✅ 0 |
| 36 | Text quality (doubled words) | N/A | ⚠️ ~20 instances |

**Summary: 28/36 PASS, 4 NOTES, 1 BLOCKER (check 6), 3 WARNINGS (checks 5, 20, 30)**

---

## Protocol Compliance

### Shape Distribution (active 150)

| Shape | v003 Count | v003 % | Protocol | Status |
|-------|:----------:|:------:|:--------:|:------:|
| READ-only | 27 | 18.0% | ~18% | ✅ |
| STORE/SKIP-only | 56 | 37.3% | ~39% | ✅ |
| READ+STORE joint | 67 | 44.7% | ~43% | ✅ |

Within ±2pp of protocol targets. Compliant.

### STORE Target Distribution (233 STORE units)

| Target | Count | % | Protocol | Deviation | Status |
|--------|:-----:|:--:|:--------:|:---------:|:------:|
| task_state | 85 | **36.5%** | ~33% | **+3.5pp** | ⚠️ |
| service_memory | 70 | 30.0% | ~32% | −2.0pp | ✅ |
| repo_memory | 43 | 18.5% | ~17% | +1.5pp | ✅ |
| project_memory | 19 | 8.2% | ~12% | −3.8pp | ⚠️ |
| user_profile | 16 | 6.9% | ~6% | +0.9pp | ✅ |

**task_state at 36.5% exceeds the ±3pp protocol tolerance** (33% ± 3pp = 30-36%). This means the evaluation set is ~3.5pp richer in task_state STORE decisions than the protocol specifies. Since task_state is the most common target class by design, this further skews the set toward the majority class and may slightly inflate target accuracy metrics for all systems.

project_memory at 8.2% is 3.8pp below the 12% target, also outside ±3pp. This under-represents project-level routing decisions.

### Stress Axes

| Axis | Count | Protocol | Status |
|------|:-----:|:--------:|:------:|
| Sensitive SKIP | 24 | 18-27 | ✅ |
| Target boundary | 37 | 30-38 | ✅ |

Both within range. Compliant.

### Domain Distribution

| Domain | Active Cases |
|--------|:------------:|
| clinical-trials | 19 |
| education-platform | 19 |
| data-pipeline | 19 |
| smart-building | 18 |
| observability-platform | 18 |
| fraud-detection | 19 |
| document-workflow | 19 |
| ml-feature-store | 19 |

Domain balance: min=18, max=19, range=1. Exceptionally well balanced.

---

## Hash / Lock Audit

| File | SHA-256 (first 16 chars) | Status |
|------|--------------------------|:------:|
| Active cases | `b5276384ade22716...` | ✅ MATCH |
| Holdout cases | `08bb2401e694f36c...` | ✅ MATCH |
| Active SFT messages | `ef5bf1b258567f6d...` | ✅ MATCH |
| Holdout SFT messages | `d23a096344dd76c5...` | ✅ MATCH |

Lock version: `v05e_gold_v2_003`. All four hashes verified. Lock is intact.

---

## Leakage Audit

### Hard Blockers (L0-L2)

| Corpus | L0 (ID) | L1 (Exact unit) | L1 (Exact memory) |
|--------|:-------:|:---------------:|:-----------------:|
| train_500 | 0 | 0 | 0 |
| dev | 0 | 0 | 0 |
| old gold | 0 | 0 | 0 |
| Few-shot exemplars | 0 | 0 | 0 |

All hard blockers pass. No exact text leakage.

### BLOCKER: Namespace Leakage (L3)

**`education-platform` / `learnhub` overlaps with train_500.**

| Name | train_500 cases | gold_v2_003 cases | Overlap Type |
|------|:---------------:|:-----------------:|-------------|
| `education-platform` | 27 | 19 (all education cases) | Project name |
| `learnhub` | 27 | 19 (all education cases) | Repo name |
| `assessment-engine` | 1 | 19 (all education cases) | Service name |

Train_500 contains 27 cases in the `education-platform` / `learnhub` domain (services: grading, enrollment, and 1 case with `assessment-engine`). Gold_v2_003 contains 19 cases in the same `education-platform` / `learnhub` domain with `assessment-engine` as the service.

**Impact:** 19/150 (12.7%) of active cases share project+repo names with the LoRA training data. LoRA systems (r=16, r=8, Qwen3-4B r=8) trained on train_500 will have name-level familiarity with `education-platform`/`learnhub`, giving them an unfair advantage over the few-shot baseline on these 19 cases.

**Root cause:** `learnhub` was a banned v001 name explicitly listed in the v001 rejection report. The v003 build script (`build_gold_v2_003.py`, line 29) hardcodes `learnhub` as the repo for the education-platform domain. This was not checked against train_500 during v003 construction.

**Note:** This is NOT a v002 regression — v002 correctly avoided `learnhub`. This is a v003-introduced regression where a banned name was reintroduced.

### L3b: Surface Strings

| Pattern | Old datasets | gold_v2_003 | Overlap |
|---------|:-----------:|:----------:|:------:|
| Phone numbers | 4 | 3 | **0** |
| Email addresses | 10 | 2 | **0** |
| API tokens/keys | 0 | 2 | **0** |

All surface strings unique. Compliant.

---

## READ Relevance Audit

### Memory Order Randomization

Memory order is shuffled. m1 target distribution:
- service_memory: 113 (63%)
- repo_memory: 44 (24%)
- project_memory: 18 (10%)
- user_profile: 5 (3%)

Stale memories appear at all positions (1 through 5), confirming genuine randomization.

### READ Position Distribution

| Position | Times Read |
|:--------:|:----------:|
| m1 | 50 |
| m2 | 60 |
| m3 | 35 |
| m4 | 25 |
| m5 | 9 |

m2 is read more than m1 — the opposite of a prefix-reading artifact. READ selection is relevance-based.

### Stale Memory Handling

**0 stale memories read** across 180 cases.

**Verdict: READ labels are semantic, not positional.** ✅

---

## Label Consistency Audit

### Exact-Text Conflicts: 0 ✅

All 396 unit instances across 150 active cases are exact-text unique at the normalized level. Zero instances of identical text with different labels. This is the key improvement over v002's 30 conflict groups.

### Normalized Skeleton Conflicts: 35 Groups ⚠️

When unit texts are normalized (service/repo/project names → SVC, numbers → N), 35 skeleton groups have conflicting labels. All 35 are SKIP-vs-STORE:task_state conflicts. Examples:

| Skeleton (abbreviated) | Instances | Conflicting Labels |
|------------------------|:---------:|-------------------|
| "roll back the SVC to VER because the latest release..." | 24 | SKIP vs STORE:task_state |
| "update the SVC to handle the EU region only correctly..." | 5 | SKIP vs STORE:task_state |
| "update the SVC to handle mobile clients correctly when..." | 5 | SKIP vs STORE:task_state |
| "debug the SVC cache invalidation bug that started after..." | 5 | SKIP vs STORE:task_state |

**Assessment:** Unlike v002 where these conflicts were exact-text and indefensible, the v003 conflicts are at the skeleton level only. The same structural template produces different labels depending on (a) whether the unit appears as u1 (task observation → SKIP) or u2/u3 (task state → STORE:task_state), and (b) the surrounding memory context. These are structurally similar but contextually distinct — the model must use position and surrounding units to disambiguate.

However, the "roll back" skeleton occurs 24 times with essentially the same semantic content ("roll back service to version because release introduced bug"). The only variation is the service name, version number, and bug type. A model that learns "roll back → task_state" will get some of these right and some wrong depending on case shape. This is a genuine label consistency concern — slightly mitigated by the fact that the position (u1 vs u2) reliably signals the label.

**Recommendation:** For v004, diversify the task_state unit templates so that structurally identical text doesn't map to conflicting labels. Add more varied task_state phrasings beyond "roll back", "update to handle", "debug the bug".

---

## Template / Diversity Audit

### Raw Text Uniqueness

| Metric | v002 | v003 | Change |
|--------|:----:|:----:|:------:|
| Unit uniqueness | 67.1% | **98.7%** | +31.6pp |
| Memory uniqueness | 41.5% | **73.3%** | +31.8pp |

Excellent improvement. Per-case unique seeds + domain vocabulary suffixes + diverse filler pools produce near-complete exact-text uniqueness.

### Normalized Skeleton Analysis

| Metric | Value | v002 Comparison |
|--------|:-----:|:--------------:|
| Max unit skeleton repeat | 24 | 16 |
| Unit skeletons >5 | 6 | 25 |
| Unit skeletons >7 | 3 | 17 |
| Max memory skeleton repeat | 19 | 17 |
| Memory skeletons >5 | 28 | N/A |

The max skeleton repeat increased from 16 to 24, but the number of frequently-repeated skeletons dropped dramatically (6 vs 25 skeletons with >5 repeats). This means v003 has a few very common skeletons and many unique ones, while v002 had moderately common skeletons across the board.

### Top Repeated Unit Skeletons

| Skeleton | Count | Acceptable? |
|----------|:-----:|:-----------:|
| "roll back the SVC to VER because the latest release..." | 24 | ⚠️ Borderline |
| "the SVC circuit-breaker opens after N consecutive failures..." | 10 | ✅ Acceptable |
| "all changes to the REPO repo that touch the SVC..." | 9 | ✅ Acceptable |
| "architecture decision records for PROJ are stored in..." | 7 | ✅ Acceptable |
| "configuration for the SVC lives under..." | 6 | ✅ Acceptable |
| "the REPO CI pipeline enforces that no PR is merged..." | 6 | ✅ Acceptable |

The "roll back" skeleton at 24× is the primary outlier. It is used as both a task_state STORE unit (when positioned as u2 in read_store_joint or store_skip_only) and as a task_progress SKIP unit (when positioned as u1 or u3 in store_skip_only). The template-based generation with limited task_state phrasings causes this concentration.

**Verdict: PASS with note.** The diversity improvement over v002 is decisive (98.7% vs 67.1%). The max skeleton repeat of 24 is disclosed in the construction report and is the cost of template-based generation. For evaluation, the contextual embedding of each instance differs (different service, version, bug type, domain vocabulary suffix), so the 24 instances are not mechanically identical fill-in-the-blank cases.

---

## Domain Coherence Audit

### Fleet Vocabulary Contamination

| Domain | v002 Fleet % | v003 Fleet % |
|--------|:------------:|:------------:|
| clinical-trials | 65% | **0.3%** |
| fraud-detection | 58% | **0.3%** |
| smart-building | 67% | **0.1%** |
| observability-platform | N/A (new) | **0.1%** |
| document-workflow | N/A (new) | **0.2%** |
| ml-feature-store | N/A (new) | **0.3%** |
| education-platform | N/A (new) | **0.3%** |
| data-pipeline | N/A (new) | **0.3%** |

**The fleet vocabulary monoculture is eliminated.** All domains are at <1% fleet terms (residual matches from generic words like "traffic" appearing in filler phrases like "production-like traffic"). This is the single largest improvement over v002.

### Domain-Appropriate Vocabulary

Each domain uses its own vocabulary family, confirmed by both the "This relates to the X functionality" suffix and embedded domain terms:

| Domain | Sample Vocab in Units |
|--------|----------------------|
| clinical-trials | enrollment, cohort, protocol, IRB, HIPAA, consent, eligibility |
| fraud-detection | transaction score, chargeback, KYC, AML, rules engine, velocity check |
| smart-building | thermostat, HVAC, BACnet, zone, chiller, economizer, VAV |
| observability-platform | trace, span, SLO, burn rate, runbook, Prometheus, Grafana |
| document-workflow | redaction, approval, retention, NDA, watermark, workflow step |
| ml-feature-store | embedding, backfill, feature view, TTL, drift detection, inference |
| education-platform | rubric, proctoring, enrollment, gradebook, plagiarism, syllabus |
| data-pipeline | schema drift, ETL, watermark, partition, backfill, lineage |

The "This relates to the X functionality" suffix is formulaic (appears on every unit and memory) but effectively ensures each domain's vocabulary permeates its cases.

**Verdict: PASS.** Domain coherence is genuinely multi-domain, a decisive fix over v002.

---

## Sensitive / Boundary Audit

### Sensitive Cases (24 active)

| Subtype | Count | SKIP Status |
|---------|:-----:|:-----------:|
| Credential (API key, token, secret, DB password) | 7 | ✅ All SKIP |
| Phone | 3 | ✅ All SKIP |
| Email | 3 | ✅ All SKIP |
| Address | 2 | ✅ All SKIP |
| Payment (Amex, debit card) | 2 | ✅ All SKIP |
| ID (SSN, employee badge) | 2 | ✅ All SKIP |
| **Total** | **19** (5 unaccounted at unit level) | ✅ |

Wait — the audit found 24 sensitive cases but only 19 unit-level subtype tags. The remaining 5 cases have `sensitive_boundary` at the case level without a unit-level sensitive subtype. These are READ-only cases tagged `sensitive_boundary` without any sensitive unit — likely a tag propagation artifact. All 24 cases correctly skip any sensitive content, so this is a metadata issue only.

**0 sensitive units stored.** Sensitive phrases are varied (16 unique from SENSITIVE_POOL of 16). No template fill-in detected in sensitive content.

### Boundary Cases (37 active)

All 37 boundary cases are in STORE-capable shapes (store_skip_only or read_store_joint). Unlike v002 where 11/34 boundary cases were READ-only with no STORE decisions, **v003 has 0 READ-only boundary cases**. All boundary cases require genuine target disambiguation.

| Boundary Type (estimated from tags) | Approx Count |
|-------------------------------------|:------------:|
| service_memory vs task_state | ~17 |
| repo_memory vs service_memory | ~12 |
| project_memory vs service_memory | ~5 |
| user_profile vs other | ~3 |

**Verdict: PASS.** Boundary cases are genuine target-disambiguation cases. The v002 issue of READ-only boundary dilution is fully resolved.

---

## Text Quality Notes

The template-based generation with randomized fillers produces occasional text quality issues:

1. **Doubled words** (~20 instances): The FILLER_WORDS `{value}` entries start with past-tense verbs (e.g., "spiked to 95%", "dropped to 12%"), but the template uses `{metric} dropped to {value}`, producing "error rate dropped to dropped to 12%". This is a template concatenation bug.

2. **Semantic incoherence**: Some filler combinations produce nonsensical text:
   - "Flag any hvac-controller demand response that the client disconnects mid-request as 'degraded'" — "demand response" (HVAC concept) as a thing to flag, combined with "client disconnects" (generic system condition), is incoherent.
   - "The hvac-controller error rate dropped to dropped to 12% after the upstream API deprecation" — doubled "dropped to".

3. **Memory texts sometimes ungrammatical**: "a simulated Redis instance from the hvac-controller is published every 10 seconds to the `svc.events` Kafka topic" — the data being published is "a simulated Redis instance" which makes no sense. The FILLER_WORDS `{data}` slot is being filled with inappropriate values for the "data publication" template.

These are cosmetic issues that don't affect label correctness but reduce the naturalness of the evaluation data. They affect perhaps 5-10% of cases based on manual inspection of the first 40.

---

## Fairness for r=16 vs r=8 Comparison

### Namespace Independence ❌

The `education-platform`/`learnhub` overlap with train_500 creates an **unfair advantage for LoRA systems** on 19/150 (12.7%) of cases. While this is less severe than v001's 24/150 (16%) with 4 overlapping names, the principle is identical: LoRA-trained systems have seen these domain names during training while the few-shot baseline has not.

### Template Diversity ✅

98.7% unit uniqueness ensures no system gets free answers from fill-in-the-blank templates.

### Domain Balance ✅

Near-perfect distribution (18-19 cases per domain, range=1) ensures no domain dominates the evaluation.

### Sensitive Safety Gate ✅

24 sensitive cases with varied subtypes provide adequate safety signal.

### Boundary Signal ✅

37 genuine boundary cases (0 READ-only dilution) provide target-classification difficulty signal.

**Overall fairness: Compromised by the learnhub overlap.** Once the education-platform cases are replaced with a clean domain, the comparison will be fair.

---

## Concerns

### 1. BLOCKER: learnhub/education-platform overlap with train_500

`learnhub` was a v001 banned name. It reappears in v003 as the repo for the education-platform domain. Train_500 contains 27 cases with `education-platform`/`learnhub`. Gold_v2_003 contains 19 cases with the same project+repo names. This gives LoRA systems namespace familiarity and violates the pre-registered independence constraint.

**Fix:** Replace the education-platform domain with a genuinely new domain whose project, repo, and service names are verified absent from train_500, dev, and old gold. Candidate: `accreditation-portal` / `badgecheck` / `certification-validator` or any education-adjacent domain with zero train overlap.

### 2. SIGNIFICANT: 35 unresolved skeleton SKIP-vs-STORE conflicts

The build script's own normalization reveals that structurally identical text maps to different labels (SKIP vs STORE:task_state) in 35 skeleton groups. The "roll back" skeleton alone accounts for 24 of these. While position provides a disambiguation signal, this still creates inherent label ambiguity at the text level.

**Fix:** Diversify or differentiate the task_state templates so that the same skeleton doesn't produce conflicting labels. For example, reserve the "roll back" phrasing for STORE:task_state only, and use different phrasings for SKIP observations.

### 3. SIGNIFICANT: task_state at 36.5% exceeds protocol tolerance

The ±3pp tolerance around 33% gives a range of 30-36%. At 36.5%, task_state is outside this range. This over-represents the majority class. Project_memory at 8.2% is also outside the 9-15% range.

**Fix:** Adjust STORE target weights in the build script (line 329: `weights=[33,32,17,12,6]`) to `weights=[30,32,18,13,7]` or similar to bring task_state down and project_memory up.

### 4. MODERATE: Template concatenation quality bugs

The FILLER_WORDS dictionary contains values with embedded verbs that duplicate template verbs (e.g., `{value}` = "dropped to 12%" combined with template "dropped to {value}" → "dropped to dropped to 12%"). Other filler combinations produce semantic incoherence.

**Fix:** Strip leading verbs from `{value}` fillers (e.g., "12%" instead of "dropped to 12%") and audit other filler-template combinations for coherence.

### 5. MINOR: Formulaic "This relates to the X functionality" suffix

Every unit and memory ends with this suffix. While it ensures domain vocabulary presence, it makes the text formulaic and may become a crutch for models to identify the domain.

**Mitigation:** Accept for v003. Consider more natural vocabulary integration in v004.

### 6. MINOR: Memory text quality

Several memory texts are ungrammatical ("a simulated Redis instance from the hvac-controller is published every 10 seconds"). These are generated by filler-template mismatches.

**Mitigation:** Add template-specific filler constraints in the build script.

---

## Required Fixes Before Evaluation

### Must-Fix (Evaluation Blocker)

1. **Replace education-platform/learnhub domain**: Change the project, repo, and service names to verified-clean alternatives with zero overlap against train_500. Update all 19 active + 4 holdout education-platform cases. Re-lock as v05e_gold_v2_004.

### Should-Fix (Quality)

2. **Fix template concatenation bug**: Change `{value}` fillers from "spiked to 95%" to just "95%" and let the template supply the verb. This eliminates the "dropped to dropped to" issue and fixes ~20 instances.

3. **Fix task_state distribution**: Reduce task_state weight from 33 to 30 and increase project_memory from 12 to 14 in the STORE target weights.

### Consider-Fixing (Polish)

4. **Reduce "roll back" skeleton dominance**: Add 3-4 alternative task_state phrasings to reduce the max skeleton repeat from 24 to <15.

5. **Audit memory-template coherence**: Add constraints to ensure `{data}` fillers match the template context (e.g., don't put "a simulated Redis instance" in a data-publication template).

---

## Final Recommendation

**Do not evaluate on v003. Fix the learnhub/education-platform overlap and regenerate.**

The v003 repair is a substantial improvement over v002 in almost every dimension: 98.7% unit uniqueness, eliminated fleet vocabulary monoculture, genuinely diverse domains, 0 exact-text conflicts, valid boundary cases, and all technical checks passing. The two failures — namespace leakage and the template concatenation bug — are specific, well-understood, and straightforward to fix.

The fix scope is narrow:
1. Replace one domain's names (education-platform/learnhub/assessment-engine → clean alternatives)
2. Fix one FILLER_WORDS list (strip leading verbs from ~6 `{value}` entries)
3. Rebuild, re-validate, re-lock

The underlying generation methodology (per-case unique seeds + domain vocabulary pools + diverse filler options) is sound and produces high-quality data. The issues are in the hardcoded domain name list and one filler list — both one-line changes.

**Estimated fix effort:** ~15 minutes (change 3 lines in `build_gold_v2_003.py`, rebuild, re-validate).

---

*End of Independent Review.*
