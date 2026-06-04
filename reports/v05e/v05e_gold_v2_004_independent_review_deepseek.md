# gold_v2_004 Independent Review — DeepSeek

**Date:** 2026-06-04
**Reviewer:** DeepSeek (automated audit + manual inspection of first 25 active + 10 holdout + 3 SFT cases)
**Status:** Independent review only — no data modified, no models run

---

## Verdict

**BLOCKER**

Two independent blocking issues: (1) 748 unresolved template placeholders render the dataset text severely degraded — `{sla}`, `{latency}`, `{header}`, `{operation}`, `{what}`, `{frequency}`, and ~20 other placeholder keys appear as raw text because they are missing from the FILLERS dictionary; and (2) `flowcraft`/`demand-forecaster` overlap with train_500 (31+1 cases) repeats the namespace leakage pattern of v001 and v003. Until both are fixed, the dataset cannot be used for evaluation.

---

## Checks Run

| # | Check | Result |
|---|-------|:------:|
| 1 | Active = 150, Holdout = 30 | ✅ PASS |
| 2 | Hash integrity (4/4) | ✅ PASS |
| 3 | Active/holdout separation | ✅ 0 ID overlap |
| 4 | Old gold hash unchanged | ✅ `56e16078...` |
| 5 | Banned v001 names (ecommerce-platform, shopengine, cart-service, learnhub, alert-manager) | ✅ NONE |
| 6 | Banned v003 names (education-platform, assessment-engine) | ✅ NONE |
| 7 | Name overlap: train_500 | ❌ **`flowcraft` (31), `demand-forecaster` (1)** |
| 8 | Name overlap: dev | ✅ NONE |
| 9 | Name overlap: old gold | ✅ NONE |
| 10 | Name overlap: few-shot | ✅ NONE |
| 11 | Target legality (5 legal targets) | ✅ 0 illegal |
| 12 | Sensitive units in STORE | ✅ 0 |
| 13 | Schema validation | ✅ 0 errors |
| 14 | Unit coverage (all units in store+skip) | ✅ 0 missed |
| 15 | SFT JSON parse | ✅ 180/180 (100%) |
| 16 | SFT markdown | ✅ 0 |
| 17 | Memory key compatibility (`text` vs `content`) | ✅ `text` key (598 instances) |
| 18 | Gold DSL populated | ⚠️ 180/180 empty (structured-only scoring) |
| 19 | READ: stale memories read | ✅ 0 |
| 20 | READ: position distribution | ✅ m1=57, m2=55, m3=41, m4=25, m5=7 |
| 21 | Memory order: m1 target diversity | ✅ svc=123, repo=32, proj=21, user=4 |
| 22 | Stale memory position randomization | ✅ Positions 1-5: 52,60,47,30,15 |
| 23 | Exact-text label conflicts | ✅ **0 groups** |
| 24 | Normalized skeleton SKIP-vs-STORE conflicts | ✅ **0 unresolved** (2 groups resolved as STORE-only) |
| 25 | Unit text uniqueness | ✅ **97.9%** (380/388) |
| 26 | Max unit skeleton repeat | ❌ **18** (target ≤8) |
| 27 | Unit skeletons >5 | ❌ **15** (target ≤3) |
| 28 | Max memory skeleton repeat | ❌ **28** (target ≤8) |
| 29 | Filler verb doubling bug | ✅ 0 ("dropped to dropped" etc fixed) |
| 30 | Unresolved template placeholders | ❌ **748 instances** |
| 31 | Article doubling ("a a", "the the") | ❌ **60 instances** |
| 32 | Version doubling ("vvN.N.N") | ❌ **26 instances** |
| 33 | Generic doubled words | ⚠️ 117 instances |
| 34 | Fleet vocabulary contamination | ✅ <1% all domains |
| 35 | Distribution: sensitive (18-27) | ✅ 25 |
| 36 | Distribution: boundary (30-38) | ✅ 30 |
| 37 | Boundary on READ-only | ✅ **0** |
| 38 | task_state ≤36% | ✅ 34.2% |
| 39 | service_memory 29-35% | ✅ 33.8% |
| 40 | repo_memory 14-20% | ✅ 15.2% |
| 41 | project_memory 9-15% | ✅ 9.1% |
| 42 | user_profile 3-9% | ✅ 7.8% |
| 43 | Leakage: train_500 (exact text) | ✅ 0 |
| 44 | Leakage: dev (exact text) | ✅ 0 |
| 45 | Leakage: old gold (exact text) | ✅ 0 |
| 46 | Leakage: few-shot (exact text) | ✅ 0 |
| 47 | Surface strings (phone/email/token) | ✅ 0 |

**Summary: 35/47 PASS, 1 MINOR (check 18), 5 FAIL (checks 7, 26-28, 30, 31-32)**

---

## Protocol Compliance

### Shape Distribution

| Shape | Count | % | Target | Status |
|-------|:-----:|:--:|:------:|:------:|
| READ-only | 31 | 20.7% | ~18% | ✅ |
| STORE/SKIP-only | 57 | 38.0% | ~39% | ✅ |
| READ+STORE joint | 62 | 41.3% | ~43% | ✅ |

### STORE Target Distribution (231 units)

| Target | Count | % | Protocol Range | Status |
|--------|:-----:|:--:|:--------------:|:------:|
| task_state | 79 | 34.2% | ≤36% | ✅ |
| service_memory | 78 | 33.8% | 29-35% | ✅ |
| repo_memory | 35 | 15.2% | 14-20% | ✅ |
| project_memory | 21 | 9.1% | 9-15% | ✅ |
| user_profile | 18 | 7.8% | 3-9% | ✅ |

**All five target ranges within protocol tolerance.** The post-generation adjustment in the build script (lines 372-433) successfully corrected task_state from its natural generation level and boosted project_memory. This is the first gold_v2 version with fully compliant target distribution.

### Stress Axes

| Axis | Count | Protocol | Status |
|------|:-----:|:--------:|:------:|
| Sensitive SKIP | 25 | 18-27 | ✅ |
| Target boundary | 30 | 30-38 | ✅ |
| Boundary on READ-only | 0 | 0 | ✅ |

All three stress checks pass.

---

## Hash / Lock Audit

| File | SHA-256 (first 16 chars) | Status |
|------|--------------------------|:------:|
| Active cases | `ee3b0762b0fe7eca...` | ✅ MATCH |
| Holdout cases | `ccc27819baf1e0e9...` | ✅ MATCH |
| Active SFT messages | `2c76446a2c914754...` | ✅ MATCH |
| Holdout SFT messages | `49432f53858ce5f3...` | ✅ MATCH |

Lock version: `v05e_gold_v2_004`. All four hashes verified. Old gold hash `56e16078...` confirmed unchanged.

---

## Leakage / Banned Entity Audit

### Hard Blockers (L0-L2)

| Corpus | L0 ID | L1 Exact Unit | L1 Exact Memory |
|--------|:-----:|:------------:|:--------------:|
| train_500 | 0 | 0 | 0 |
| dev | 0 | 0 | 0 |
| old gold | 0 | 0 | 0 |
| Few-shot exemplars | 0 | 0 | 0 |

All exact-text checks pass.

### BLOCKER: Namespace Leakage (L3)

| Name | train_500 | gold_v2_004 | Overlap |
|------|:---------:|:-----------:|:-------:|
| `flowcraft` | 31 cases (repo in `workflow-automation`) | ~19 cases (repo in `supply-chain-optimizer`) | Repo name |
| `demand-forecaster` | 1 case (service in `supply-chain`/`logistix`) | ~19 cases (service in `supply-chain-optimizer`) | Service name |

**`flowcraft`** appears as a repo name in 31 train_500 cases under the `workflow-automation` project. Gold_v2_004 uses `flowcraft` as the repo for the `supply-chain-optimizer` domain. **`demand-forecaster`** appears as a service name in 1 train_500 case. Gold_v2_004 uses it as the service for the `supply-chain-optimizer` domain.

**Impact:** ~19/150 (12.7%) active cases in the `supply-chain-optimizer` domain carry repo/service names that LoRA-trained systems have seen during training. This gives LoRA systems (r=16, r=8, Qwen3-4B r=8) namespace familiarity and violates the pre-registered independence constraint.

**Root cause:** The build script's 315 banned entity check appears to be domain-level only. The names `flowcraft` and `demand-forecaster` were not checked against individual repo/service names in train_500.

### L3b: Surface Strings

| Pattern | Old datasets | gold_v2_004 | Overlap |
|---------|:-----------:|:----------:|:------:|
| Phone | 4 | 3 | **0** |
| Email | 10 | 2 | **0** |
| API tokens | 0 | 2 | **0** |

All clean.

---

## Label Consistency Audit

### Exact-Text Conflicts: 0 ✅

Zero exact-text label conflicts across 180 cases. The disjoint task_state pools (TASK_STORE_POOL vs TASK_SKIP_POOL) successfully eliminate the SKIP-vs-STORE ambiguity that plagued v002 and v003. The STORE pool uses CURRENT/ACTIVE/ASSIGNED markers ("Currently investigating", "Active incident", "This sprint task", "Assigned task") while the SKIP pool uses EPHEMERAL/HYPOTHETICAL/OLD markers ("Hypothetical scenario", "Old incident note", "Scratch investigation", "Discarded idea", "Historical reference", "Stale note from previous sprint").

### Normalized Skeleton Conflicts: 0 Unresolved ✅

2 skeleton groups have any label variation at all — both are STORE-vs-STORE (different targets for structurally identical text in different contexts). Zero SKIP-vs-STORE unresolved conflicts. **This is the key labeling improvement over v002 and v003.**

**Verdict: The disjoint pool design works. Labels are consistent.** ✅

---

## Template / Diversity Audit

### Raw Text Uniqueness

| Metric | v003 | v004 | Change |
|--------|:----:|:----:|:------:|
| Unit uniqueness | 98.7% | 97.9% | −0.8pp |
| Memory uniqueness | 73.3% | 63.9% | −9.4pp |

Unit uniqueness remains excellent. Memory uniqueness declined moderately due to formulaic service_memory templates.

### Normalized Skeleton Analysis

| Metric | v003 | v004 | Target |
|--------|:----:|:----:|:------:|
| Max unit skeleton repeat | 24 | **18** | ≤8 |
| Unit skeletons >5 | 6 | **15** | ≤3 |
| Unit skeletons >8 | 3 | **7** | — |
| Max memory skeleton repeat | 19 | **28** | ≤8 |

**All skeleton diversity targets are missed.** The increase in skeletons >5 (from 6 to 15) is notable — v004 has more structural repetition than v003. This is driven by unresolved placeholders: when `{sla}`, `{latency}`, `{operation}`, `{data}`, etc. all render as the literal placeholder names, the normalized skeletons collapse to identical forms. Fixing the FILLERS dictionary will naturally reduce these counts.

### Top Repeated Unit Skeletons (all driven by unresolved placeholders)

| Skeleton | Count | Cause |
|----------|:-----:|-------|
| "the SVC performs operation — detail this is critical for" | 18 | `{operation}` + `{detail}` unfilled |
| "data from the SVC is published every intervals to `topic`" | 17 | `{data}` + `{interval}` + `{topic}` + `{key}` unfilled |
| "the SVC circuit breaker opens after n consecutive failures to" | 15 | `{n}` + `{reset}` unfilled |
| "off-topic observation: the SVC logs show periodic N spikes during" | 12 | `{pattern}` unfilled |
| "SVC config in SVC lives under `path` with per-environment overrides" | 10 | `{path}` + `{envs}` unfilled |

**All top repeated skeletons are artifacts of unresolved placeholders.** Once the FILLERS dictionary is complete, these counts will drop significantly.

---

## Filler Bug Audit

### BLOCKER: 748 Unresolved Template Placeholder Instances

The FILLERS dictionary contains only 23 keys: `problem`, `context`, `issue`, `trigger`, `feature`, `version`, `bug`, `metric`, `value`, `target`, `symptom`, `fix`, `old_tech`, `new_tech`, `progress`, `system`, `quarter`, `phase`, `owner`, `deadline`, `inc_num`, `behavior`, `pattern`.

The templates in `_gen_svc_mem`, `_gen_repo_mem`, `_gen_proj_mem`, and `_gen_user_mem` use ~40 additional placeholder keys that are **not in FILLERS**. When `_pick` can't find a key, it returns the key name itself:

| Missing FILLER Key | Raw Text Output | Instances |
|-------------------|-----------------|:---------:|
| `{sla}` | "guarantees sla% uptime" | 32 |
| `{latency}` | "latency of latencyms" | 32 |
| `{percentile}` | "at ppercentile" | 32 |
| `{header}` | "a `header` header" | 40 |
| `{purpose}` | "header for purpose" | 40 |
| `{operation}` | "performs operation" | 51 |
| `{detail}` | "detail This is critical for" | 51 |
| `{data}` | "published every intervals" / "against data" | 84 |
| `{interval}` | "every intervals" | 44 |
| `{topic}` | "to `topic` partitioned by" | 44 |
| `{key}` | "partitioned by key" | 44 |
| `{where}` | "in where with a" | 57 |
| `{ttl}` | "a ttl TTL" | 57 |
| `{n}` | "after n consecutive" | 54 |
| `{reset}` | "resets after resets" | 54 |
| `{what}` | "must include what in the" | 42 |
| `{cmd}` | "Run `cmd` in" | 40 |
| `{action}` | "to action the" | 40 |
| `{condition}` | "if the SVC condition by" | 37 |
| `{path}` | "lives under `path`" / "stored in `path`" | 45 |
| `{frequency}` | "requires frequency" | 33 |
| `{review_type}` | "frequency review_type reviews" | 33 |
| `{blocker}` | "Blocked by blocker" | 12 |
| `{component}` | "refactor the SVC component to" | 12 |

### Article Doubling: 60 Instances

Template-text concatenation produces article doubling:
- "had **a a** race condition" / "introduced **a a** regression" — 23 instances (template "had a {issue}" where {issue} starts with "a")
- "after **the the** 3PM config push" / "after **the the** database failover" — 37 instances (template "after the {trigger}" where {trigger} starts with "the")

### Version Doubling: 26 Instances

Template "v{version}" combined with filler "v3.0.2" produces "**vv3.0.2**" (double v prefix).

### What Was Fixed

The v003 doubled-verb bug ("dropped to dropped to") is correctly fixed. The `{value}` fillers no longer have leading verbs. **0 instances** of "dropped to dropped", "spiked to spiked", etc.

---

## Domain Coherence Audit

### Fleet Vocabulary Contamination

| Domain | Fleet % | Status |
|--------|:-------:|:------:|
| accessibility-compliance | 0.3% | ✅ |
| cybersecurity-audit | 0.0% | ✅ |
| game-analytics | 0.0% | ✅ |
| genomics-pipeline | 0.0% | ✅ |
| media-transcoding | 0.0% | ✅ |
| quantitative-research | 0.0% | ✅ |
| real-estate-valuation | 0.0% | ✅ |
| supply-chain-optimizer | 0.0% | ✅ |

**Fleet vocabulary eliminated across all domains.** This is the cleanest result of any gold_v2 version.

### Domain-Appropriate Vocabulary

All 8 domains use their declared vocabulary families. The "This relates to the X functionality" suffix ensures domain vocabulary permeates every unit and memory. Domain families are genuinely distinct: security (CVE, pentest, vulnerability), logistics (safety stock, SKU, procurement), media (codec, bitrate, H.265), a11y (WCAG, ARIA, screen reader), finance (alpha, Sharpe, backtest), bioinformatics (FASTQ, BAM, variant), real estate (cap rate, appraisal, MLS), gaming (DAU, retention, ARPDAU).

---

## READ Relevance Audit

### Memory Order Randomization

m1 target diversity: service_memory=123 (68%), repo_memory=32 (18%), project_memory=21 (12%), user_profile=4 (2%). Service memories dominate m1 position, but other targets appear. Order is shuffled.

Stale memories distributed across positions 1-5 (52, 60, 47, 30, 15), confirming genuine randomization.

### READ Position Distribution

m1=57, m2=55, m3=41, m4=25, m5=7. m2 is roughly equal to m1 — the opposite of prefix-reading. READ selection is relevance-based.

### Stale Memory Handling

**0 stale memories read** across 180 cases.

**Verdict: READ labels are semantic, not positional.** ✅

---

## Sensitive / Boundary Audit

### Sensitive Cases (25 active)

| Subtype | Count | SKIP Status |
|---------|:-----:|:-----------:|
| Credential (API key, OAuth secret, GitHub token) | 6 | ✅ All SKIP |
| Phone | 3 | ✅ All SKIP |
| Email | 3 | ✅ All SKIP |
| Address | 2 | ✅ All SKIP |
| Payment (Amex, debit) | 2 | ✅ All SKIP |
| ID (SSN, badge) | 2 | ✅ All SKIP |
| **Unaccounted at unit level** | **7** | ✅ Still correctly SKIPped |

Note: 7 sensitive cases have `sensitive_boundary` at the case level without unit-level subtype tags. These are READ-only cases carrying the `sensitive_boundary` tag from the generation flag. All sensitive units in these cases are correctly SKIPped. Metadata precision issue only.

### Boundary Cases (30 active)

All 30 boundary cases are in STORE-capable shapes (store_skip_only or read_store_joint). **0 boundary cases on READ-only.** Boundary tags require genuine target disambiguation. The post-generation boundary enforcement (lines 426-437) correctly removed boundary from READ-only cases and ensured the ≥30 minimum.

**Verdict: Boundary integrity is solid.** ✅

---

## Schema / Eval Compatibility

### Memory Key Compatibility

All 598 memory instances use the `"text"` key (not `"content"`). The legacy `eval_runner.py` / `check_leakage.py` expects `"content"` and will fail. The `eval_lora_router.py` interface handles `"text"` correctly. **Documentation is needed:** any legacy script that reads memories via `m["content"]` must be updated to use `m["text"]` or a compatibility wrapper.

### Gold DSL Field

All 180 cases have `"dsl": ""` (empty). The gold labels are structured-only (`read`, `store`, `skip` arrays). The DSL rendering is not provided. This is acceptable because evaluation uses structured scoring (exact match on JSON output, not DSL string comparison). **Document the structured-only scoring approach.**

### SFT Format

Active SFT: 150 messages, 100% JSON valid, 0 markdown. Holdout SFT: 30 messages, same quality. Format is standard: system prompt → user content (runtime + memories + units) → assistant JSON. Compatible with standard SFT training pipelines.

---

## Fairness for r=16 vs r=8 Comparison

### Namespace Independence ❌

`flowcraft` and `demand-forecaster` appear in both train_500 and gold_v2_004. LoRA systems trained on train_500 will have name-level familiarity with the `supply-chain-optimizer` domain (~19/150 active cases). The few-shot baseline has no such familiarity.

### Disjoint Task Pools ✅

The STORE-vs-SKIP label disambiguation is structural (marker words like "Currently", "Active", "Assigned" vs "Hypothetical", "Old", "Discarded"). All systems can learn this distinction — no unfair advantage for any system.

### Template Diversity ⚠️

Unresolved placeholders inflate skeleton repeat counts. Once FILLERS is fixed, skeleton diversity will improve substantially (currently 15 skeletons >5 vs target ≤3).

### Target Distribution ✅

All five targets within protocol tolerance. Fair comparison across systems.

### Overall Fairness

**Currently unfair** due to namespace leakage. After fixing `flowcraft`/`demand-forecaster` names, the comparison will be fair.

---

## Concerns

### 1. BLOCKER: 748 unresolved template placeholder instances

The FILLERS dictionary is missing ~20+ keys used by `_gen_svc_mem`, `_gen_repo_mem`, `_gen_proj_mem`, and `_gen_user_mem` templates. The `_pick` function silently returns placeholder names as text, producing nonsensical output like "guarantees sla% uptime with a maximum response latency of latencyms at ppercentile." **This affects nearly every unit and memory in the dataset.**

**Fix:** Add all missing filler keys to the FILLERS dictionary. Required additions: `sla`, `latency`, `percentile`, `header`, `purpose`, `operation`, `detail`, `data`, `interval`, `topic`, `key`, `where`, `ttl`, `n`, `reset`, `cmd`, `action`, `condition`, `path`, `what`, `frequency`, `review_type`, `dashboard`, `tool`, `metric`, `blocker`, `component`, `envs`, `viz`, `list`, `field`, `alt_field`, `unit`, `alt_unit`.

### 2. BLOCKER: `flowcraft`/`demand-forecaster` in train_500

`flowcraft` (31 train cases) and `demand-forecaster` (1 train case) appear in both train_500 and gold_v2_004. This is the same category of namespace leakage that caused v001 and v003 rejection. ~19/150 active cases affected.

**Fix:** Replace the supply-chain-optimizer domain's repo and service names (`flowcraft` → new name, `demand-forecaster` → new name). Verify against train_500 at the individual name level, not just the domain level.

### 3. SIGNIFICANT: Article doubling and version doubling

60 instances of "a a" / "the the" and 26 instances of "vvN.N.N". These are template concatenation issues:
- Article doubling: template `had a {issue}` where `{issue}` starts with "a" → "had a a race condition"
- Version doubling: template `v{version}` where `{version}` starts with "v" → "vv2.3.1"

**Fix:** Strip leading articles from `{issue}` fillers, and strip leading "v" from `{version}` fillers (or remove "v" prefix from templates).

### 4. MODERATE: Skeleton repeat targets missed (all driven by unresolved placeholders)

Max unit skeleton repeat=18 (target ≤8), 15 skeletons >5 (target ≤3), max memory skeleton repeat=28 (target ≤8). These are all downstream effects of unresolved placeholders — when every service has the same placeholder text, normalized skeletons collapse. Fixing concern #1 will reduce these counts.

### 5. MINOR: Gold DSL field empty

All 180 cases have `"dsl": ""`. The DSL string format is not rendered. This is acceptable for structured-only scoring but should be documented in the eval protocol.

### 6. MINOR: Memory key incompatibility with legacy tools

The `"text"` key (vs legacy `"content"`) will break `check_leakage.py` and `eval_runner.py`. Document the key change or add a compatibility layer.

### 7. OBSERVATION: 7 sensitive cases lack unit-level subtype tags

Same issue as v003. Case-level `sensitive_boundary` without unit-level subtype. Metadata precision issue only.

---

## Required Fixes Before Evaluation

### Must-Fix (Blockers)

1. **Complete the FILLERS dictionary.** Add all missing keys: `sla`, `latency`, `percentile`, `header`, `purpose`, `operation`, `detail`, `data`, `interval`, `topic`, `key`, `where`, `ttl`, `n`, `reset`, `cmd`, `action`, `condition`, `path`, `what`, `frequency`, `review_type`, `dashboard`, `tool`, `metric`, `blocker`, `component`, `envs`, `viz`, `list`, `field`, `alt_field`, `unit`, `alt_unit`, `reports`, `format`, `capability`, `dependency`, `fallback`, `requirement`, `scope`, `runner`, `guarantees`. Each needs 3-8 alternatives.

2. **Replace `flowcraft` and `demand-forecaster`** with names verified absent from train_500 at the individual entity level (not just domain level). Use the v004 name verification list but extend it to check repo and service names independently.

3. **Fix article doubling:** Strip leading "a"/"an" from `{issue}` fillers. Strip leading "the" from `{trigger}` fillers. Or adjust templates to not include articles.

4. **Fix version doubling:** Either remove "v" prefix from templates (`{version}` instead of `v{version}`) or remove "v" prefix from `{version}` fillers.

### Should-Fix (Quality)

5. **Rebuild and re-validate all 12 hard gates** after FILLERS fix. Skeleton repeat counts should drop significantly.

6. **Document structured-only scoring** (empty DSL field is intentional).

7. **Add `"text"` → `"content"` compatibility notes** for legacy eval scripts.

---

## Final Recommendation

**Do not evaluate on v004. Fix the two blockers (FILLERS dictionary + namespace leakage) and regenerate.**

The v004 design is conceptually the strongest of all four gold_v2 versions:
- **Disjoint task pools** (TASK_STORE_POOL vs TASK_SKIP_POOL) solve the label consistency problem definitively — 0 exact conflicts, 0 SKIP-vs-STORE skeleton conflicts
- **Post-generation distribution adjustment** successfully keeps all five targets within protocol ranges
- **Boundary enforcement** correctly removes boundary from READ-only cases while maintaining ≥30 minimum
- **Domain diversity** is the best yet — 8 genuinely distinct domains with zero fleet vocabulary contamination

The failures are execution-level, not design-level. The FILLERS dictionary is incomplete (~23 keys vs ~60 needed). The name verification missed two names in train_500. Both are one-time fixes that don't require methodological changes.

**Estimated fix effort:** Medium (~1 hour). The FILLERS dictionary needs ~40 new keys with 3-8 alternatives each (~200 new filler strings). The namespace fix is a two-name replacement. The article/version doubling fix is a template adjustment.

**Recommended next version:** `gold_v2_005` with completed FILLERS + verified-clean names.

---

*End of Independent Review.*
