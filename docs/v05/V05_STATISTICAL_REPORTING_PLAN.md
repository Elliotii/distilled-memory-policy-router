# V0.5 Statistical Reporting Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — confidence intervals, learning curves, and error analysis
Context: 5.3-A — dev/gold + provenance + leakage planning

---

## 1. Why Statistics Matter

### 1.1 Small Gold Set

Gold is planned at n=100 cases (70 core + 30 hard). With only 100 evaluation points:

- Small absolute differences (e.g., 2–3 pp on exact_match) may be noise.
- Per-target breakdowns on gold_hard (n=30) have wide confidence intervals.
- Per-tag breakdowns may have n < 10, making statistical comparison nearly meaningless.

**Statistical reporting is required to avoid over-interpreting small differences.**

### 1.2 What Statistics We Report

| Statistic | Purpose |
|-----------|---------|
| Point estimate | Best-guess metric value |
| 95% bootstrap confidence interval | Uncertainty around the estimate |
| Sample size (n) | How many cases the metric is computed over |
| Effect size (delta) | Difference between systems in meaningful units |
| p-value (optional, with caveats) | Whether a difference is statistically significant |

### 1.3 What We Do NOT Over-Interpret

- Do NOT claim "system A beats system B" on a 1pp difference with n=100.
- Do NOT report per-tag metrics without noting n per tag.
- Do NOT report gold_hard metrics as if they have the same precision as gold_core.
- Do NOT use p-values as binary "significant/not significant" without context.

---

## 2. Bootstrap Confidence Intervals

### 2.1 Method

For each metric and system:

1. Compute the per-case metric value (0 or 1 for exact_match; continuous for F1).
2. Resample cases with replacement 10,000 times (bootstrap).
3. Compute the metric on each bootstrap sample.
4. Report the 2.5th and 97.5th percentiles as the 95% CI.

Use **case-level bootstrap** (resample cases, not individual units) to preserve within-case dependencies.

**System comparison:** Use **paired bootstrap** for comparing two systems on the same gold cases. Compute the per-case delta (system A − system B), bootstrap the delta distribution, and report the 95% CI of the delta. If the delta CI excludes 0, the difference is statistically meaningful. This paired approach uses the same resampled cases for both systems, preserving the paired structure.

**Fixed random seed:** Use a fixed random seed (e.g., `seed=42`) for all bootstrap operations to ensure reproducibility across report generations.

### 2.2 Metrics Requiring CI

| Metric | CI Required? | Notes |
|--------|:------------:|-------|
| `exact_match` | ✓ | Binary per case |
| `read_f1` | ✓ | Per case, may be undefined if no gold READ |
| `store_unit_f1` | ✓ | Per case |
| `store_target_accuracy` | ✓ | Per case, only for cases with predicted STORE |
| `skip_f1` | ✓ | Per case |
| `false_store_rate` | ✓ | Per case |
| `parse_success` | Optional | Should be near 100% — wide CI would indicate instability |
| `sensitive_store_count` | N/A | Must be exactly 0 — CI is meaningless |

### 2.3 CI Interpretation

When comparing two systems, check whether their 95% CIs overlap:

| CI Relationship | Interpretation |
|-----------------|---------------|
| Non-overlapping CIs | Likely significant difference |
| Overlapping but point estimates separated | Inconclusive — need larger gold or effect size analysis |
| Fully overlapping | No evidence of difference |

**Do NOT claim significance solely from non-overlapping CIs.** Bootstrap CIs are approximate and can be anti-conservative.

### 2.4 Reporting Format

For each metric in the main results table:

```
Exact Match: 72.0% (95% CI: 63.1–80.2%, n=100)
```

Not:
```
Exact Match: 72.0%
```

---

## 3. Learning Curve

### 3.1 Train Subset Ablation

To understand how much training data is needed, evaluate the trained router on dev at three training sizes. Subsets must be **nested** so the learning curve reflects monotonic data addition:

| Subset | Cases | Nesting | Purpose |
|--------|:-----:|---------|---------|
| 125 cases | 25% of train pool | Base subset | Minimal training — is 125 enough? |
| 250 cases | 50% of train pool | 125 ⊂ 250 | Half data — where does the curve bend? |
| 500 cases | 100% of train pool | 125 ⊂ 250 ⊂ 500 | Full training data |

### 3.2 Procedure

1. Using a **fixed random seed** (e.g., `seed=42`), randomly sample 125 cases from the train pool (stratified by target distribution). Record the `case_id` list.
2. Train LoRA on 125 cases, evaluate on dev.
3. Using the same seed, sample an additional 125 cases from remaining pool. Combine with the first 125 to form 250 total. Record the `case_id` list.
4. Train LoRA on 250 cases, evaluate on dev.
5. Train LoRA on all 500 cases, evaluate on dev. Record the `case_id` list.
6. Plot learning curve: metric (y-axis) vs training cases (x-axis).
7. If the curve flattens at 250, expanding to 500 may have diminishing returns — document this.

**Nesting guarantee:** 125 ⊂ 250 ⊂ 500 ensures the curve shows the effect of adding more data, not the effect of sampling different data. Record the exact `case_id` lists for each subset in the final report.

### 3.3 Metrics to Track

| Metric | Why |
|--------|-----|
| `exact_match` | Overall routing quality |
| `store_unit_f1` | STORE coverage |
| `store_target_accuracy` | Target discrimination |
| `false_store_rate` | Over-storing |
| `parse_success` | Structural stability |

### 3.4 No Gold Peeking

The learning curve uses **dev only**. Do NOT evaluate on gold during data ablation — gold is for final evaluation only.

---

## 4. Breakdown Reporting

### 4.1 Per-Target Breakdown

For each system on gold, report:

| Target | Gold STORE Count | Predicted STORE Count | Target Accuracy % | 95% CI |
|--------|:----------------:|:---------------------:|:-----------------:|:------:|
| service_memory | N | N | X% | [L, U] |
| task_state | N | N | X% | [L, U] |
| repo_memory | N | N | X% | [L, U] |
| project_memory | N | N | X% | [L, U] |
| user_profile | N | N | X% | [L, U] |

Note: Gold STORE count per target may be as low as ~5 for user_profile on gold_core. Wide CIs expected.

### 4.2 Per-Tag Breakdown

For each system on gold, group cases by tag:

| Tag | Cases | Exact Match % | STORE F1 | Target Acc % | Notes |
|-----|:-----:|:-------------:|:--------:|:------------:|-------|
| service_vs_task_state | N | X% | X | X% | Boundary stress |
| sensitive_boundary | N | X% | X | X% | Must be 0 sensitive store |
| stale_memory | N | X% | X | X% | — |
| related_but_useless | N | X% | X | X% | — |
| target_boundary | N | X% | X | X% | Hardest subset |
| ... | ... | ... | ... | ... | ... |

**Important:** Per-tag n may be very small (e.g., n=5 for user_profile_boundary). Report n prominently and do not draw strong conclusions from n < 10.

### 4.3 Gold Core vs Gold Hard

| Subset | Cases | System | Exact % | STORE F1 | Target Acc % | Sensitive Store |
|--------|:-----:|--------|:-------:|:--------:|:------------:|:---------------:|
| Gold core | 70 | `qwen_lora_dsl` | X% [CI] | X [CI] | X% [CI] | 0 |
| Gold core | 70 | `qwen_few_shot_dsl` | X% [CI] | X [CI] | X% [CI] | 0 |
| Gold hard | 30 | `qwen_lora_dsl` | X% [CI] | X [CI] | X% [CI] | 0 |
| Gold hard | 30 | `qwen_few_shot_dsl` | X% [CI] | X [CI] | X% [CI] | 0 |

Gold hard is expected to have lower metrics — it's designed to stress boundaries. The gap between gold_core and gold_hard is itself a finding.

---

## 5. Sensitive Store Hard Gate

### 5.1 Zero Tolerance

`sensitive_store_count` must be exactly 0 on gold. Any positive count is a **No-Go** regardless of other metrics.

If sensitive_store_count > 0:

1. Halt evaluation.
2. List all cases where sensitive content was STOREd.
3. Analyze why: model failure, labeling error, or boundary ambiguity.
4. Fix the issue (retrain, adjust prompt, filter output) before any claims.
5. Do NOT aggregate sensitive_store_count into an average — report the exact count and case IDs.

### 5.2 Reporting

If sensitive_store_count = 0:
```
Sensitive content STOREd: 0 out of N sensitive-boundary cases (0.0%)
```

If sensitive_store_count > 0:
```
⚠️ SENSITIVE STORE DETECTED ⚠️
Count: K cases
Case IDs: v05_gold_XXXX, v05_gold_YYYY
This is a No-Go. Model must not be deployed or claimed until resolved.
```

---

## 6. Error Analysis

### 6.1 Target Confusion Matrix

For each system, construct a confusion matrix of predicted vs gold targets:

| Gold ↓ / Pred → | svc | task | repo | proj | user | SKIP |
|-----------------|:---:|:----:|:----:|:----:|:----:|:----:|
| service_memory | a | b | c | d | e | f |
| task_state | g | h | i | j | k | l |
| repo_memory | m | n | o | p | q | r |
| project_memory | s | t | u | v | w | x |
| user_profile | y | z | ... | ... | ... | ... |
| SKIP | ... | ... | ... | ... | ... | ... |

Diagonal = correct predictions. Off-diagonal = confusions.

Key confusions to watch:
- service_memory ↔ task_state (expected most-common confusion)
- project_memory ↔ repo_memory
- project_memory ↔ task_state
- Any target → SKIP (under-storing)
- SKIP → any target (over-storing / false store)

### 6.2 Over-Read Analysis

List cases where the model predicted READ for memories that gold did not.

For each case:
- case_id, memory_ids over-read.
- Candidate memory content for over-read memories.
- Why gold did not READ them (stale, related but useless, etc.).

Quantify: total irrelevant reads / total predicted reads.

### 6.3 Under-Read Analysis

List cases where the model missed READ for memories that gold did read.

For each case:
- case_id, memory_ids missed.
- Candidate memory content for missed memories.
- Impact: what context was the model missing?

### 6.4 False Store Analysis

List cases where the model STOREd units that gold marked as SKIP.

For each case:
- case_id, unit_ids falsely stored.
- Unit text.
- Why gold marked them SKIP (temporary, sensitive, unrelated, etc.).
- What target the model incorrectly assigned.

Quantify: false store rate = falsely stored / total predicted STORE.

### 6.5 Boundary Failure Taxonomy

Categorize all target-boundary failures:

| Failure Type | Count | % of Errors | Example |
|-------------|:-----:|:-----------:|---------|
| service→task_state confusion | N | X% | "Add retry wrapper" → svc instead of task |
| task_state→service confusion | N | X% | "The service deduplicates" → task instead of svc |
| project→repo confusion | N | X% | "All services must..." → repo instead of proj |
| repo→project confusion | N | X% | "Parser tests under tests/" → proj instead of repo |
| user_profile→SKIP confusion | N | X% | "I prefer..." → SKIP instead of user |
| SKIP→any target (false store) | N | X% | Temporary request stored |
| any target→SKIP (false skip) | N | X% | Durable info skipped |
| Other | N | X% | — |

---

## 7. Reporting Template

### 7.1 Final Evaluation Report Structure

The final report (`reports/v05/v05_final_eval_report.md`) should follow this structure:

1. **Executive Summary** — 3–5 bullet points
2. **Evaluation Setup** — systems, gold set description, metrics
3. **Main Results Table** — all systems, full gold, with 95% CIs
4. **Gold Core Results** — 70-case subset
5. **Gold Hard Results** — 30-case subset
6. **Per-Target Breakdown** — all systems
7. **Per-Tag Breakdown** — all systems
8. **Target Confusion Matrix** — primary system
9. **Learning Curve** — 125/250/500 on dev
10. **Error Analysis** — over-read, under-read, false store, boundary failures
11. **Sensitive Store Report** — must be 0
12. **Baseline Comparison Narrative** — what each baseline teaches
13. **Limitations** — provenance, gold size, LLM-assisted labeling
14. **Conclusions** — go/no-go, next steps
15. **Appendix** — full per-case metrics, prediction files

---

## 8. Changelog

| Date | Change |
|------|--------|
| 2026-06-02 | Initial creation (Context 5.3-A) |

---

*End of V0.5 Statistical Reporting Plan.*
