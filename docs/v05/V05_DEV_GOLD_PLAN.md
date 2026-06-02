# V0.5 Dev/Gold Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — dev and gold construction strategy
Context: 5.3-A — dev/gold + provenance + leakage planning

---

## 1. Scope

This document defines the **construction strategy** for v0.5 development and gold evaluation sets. It does not generate data. It does not split corrected batch500.

### 1.1 Corrected Batch500 Is Training-Pool Candidate

The corrected batch500 (500 cases) is a **training-pool candidate**, not a final train/dev/gold split.

Dev and gold must be constructed as **held-out sets** — independently generated or curated, not mechanically sliced from the train pool.

### 1.2 Rationale Against Mechanical Splitting

Mechanical random splitting of corrected batch500 into train/dev/gold would:

- Share the same generation process, prompt templates, and LLM annotation style across all splits.
- Hide label-style artifacts that might inflate eval scores.
- Use the same LLM-annotator's decision patterns for training and evaluation, making eval less diagnostic of real generalization.
- Fail to test whether the router works on independently constructed cases that the label-generating LLM has not seen.

Instead, dev and gold should be:

- Generated independently (different prompts, different batches, different construction passes).
- Or curated from scratch with explicit attention to schema compliance, target boundaries, and diversity.
- Human-adjudicated for gold.

---

## 2. Proposed Data Roles

| Role | Cases | Source | Construction | Review Level |
|------|:-----:|--------|-------------|:------------:|
| **Train pool** | 500 | Corrected batch500 candidate | LLM-assisted generation + review fixes | LLM-based independent review ✓ |
| **Dev** | 80–100 | Independent generation or curation | Same schema/taxonomy, separate drafts | Spot-check + high-risk full review |
| **Gold** | 100 | Independent generation or curation | Same schema/taxonomy, separate drafts | Full human adjudication |
| **Total** | ~700 | — | — | — |

### 2.1 Train Pool Role

- Used for LoRA/SFT training.
- Source: corrected batch500 (after promotion prerequisites met).
- May be adjusted before training (borderline case adjudication, final filtering).
- Must not overlap with dev or gold.

### 2.2 Dev Set Role

Dev is used ONLY for:

1. **Checkpoint selection** — choosing the best training epoch/step.
2. **Prompt / training setting comparison** — comparing system prompt variants, LoRA ranks, etc.
3. **LoRA hyperparameter choice** — rank, alpha, learning rate.
4. **Early error analysis** — catching overfitting, target collapse, or parse degradation during training.

Dev is NOT used for:

- Final model comparison claims.
- Resume or project performance claims.
- Published results.
- Claims of "our model achieves X on held-out data."

Dev metrics are **development diagnostics only**.

### 2.3 Gold Set Role

Gold is used ONLY for:

1. **Final model comparison** — comparing trained router against all baselines.
2. **Final report** — the sole evaluation standard for v0.5 claims.
3. **Resume / project claims** — any reported metric must come from gold, not dev.
4. **Baseline comparison** — all baselines evaluated on the same gold set.

Gold MUST:

- Be locked before any training begins.
- Never be used for prompt tuning, training, or hyperparameter choice.
- Never be used for checkpoint selection.
- Never be inspected during training (no "let's peek at gold to see if we're improving").
- Be opened only for final evaluation, after training is complete and final checkpoint selected.

---

## 3. Dev Set Construction

### 3.1 Size

| Metric | Value |
|--------|:-----:|
| Target size | 80–100 cases |
| Minimum | 80 (enough for stable checkpoint selection) |
| Maximum | 100 (leave more cases for gold if needed) |

### 3.2 Distribution Requirements

Dev should closely resemble the expected train distribution for effective model selection:

| Target | Range |
|--------|:-----:|
| service_memory | 28–34% of STORE units |
| task_state | 28–34% of STORE units |
| repo_memory | 16–22% of STORE units |
| project_memory | 10–16% of STORE units |
| user_profile | 5–10% of STORE units |

Shape distribution should loosely match train:
- READ+STORE joint: 35–45%
- STORE/SKIP-only: 30–40%
- READ-only: 18–25%

### 3.3 Tag Coverage

Dev should cover all major tag categories, with emphasis on common patterns:

| Tag | Priority |
|-----|:--------:|
| service_invariant | Required |
| task_progress | Required |
| repo_convention | Required |
| stale_memory | Required |
| related_but_useless | Required |
| target_boundary | Required |
| sensitive_boundary | Required |
| service_vs_task_state | Required |
| project_vs_repo | Recommended |
| repo_vs_service | Recommended |
| user_profile_boundary | Recommended |
| temporary_request | Recommended |

### 3.4 Source

Dev cases will be **independently LLM-generated** with a **different construction pass and prompt seed** from the train-pool generation. They will NOT be mechanically split from corrected batch500.

**Method:**
1. Generate 80–100 fresh cases using the same schema/taxonomy but a distinct prompt variant and generation batch.
2. Run structural + DSL validation on all candidates.
3. Run leakage checks against the train pool (exact, normalized, n-gram Jaccard) before acceptance.
4. Reject any candidate with exact text overlap or high Jaccard similarity to the train pool.
5. Accept only cases that pass all checks.

**Purpose:** Dev is for checkpoint selection, hyperparameter comparison, and prompt-setting comparison only. It is NOT used for final claims — those come from gold.

Dev cases should be:

- Generated independently from train pool (separate batch, different prompts).
- NOT mechanically copied or paraphrased from corrected batch500.
- NOT cherry-picked "easy" cases to inflate dev scores — this defeats checkpoint selection.

### 3.5 Review Level

| Review Type | Scope |
|-------------|-------|
| Structural validation | All 80–100 cases (automated) |
| DSL parse + canonical consistency | All cases (automated) |
| Spot-check semantic review | 20% random sample (16–20 cases) |
| Full semantic review | All high-risk / boundary cases |
| Human review | Not required for dev; spot-check + audit is sufficient |

Dev does NOT require full human adjudication. Its purpose is model selection, not final claims. A structural + spot-check review is sufficient.

---

## 4. Gold Set Construction

### 4.1 Size

| Metric | Value |
|:-------|:-----:|
| Total gold | 100 cases |
| Gold core | 70 cases |
| Gold hard | 30 cases |

### 4.2 Gold Core (70 cases)

Purpose: Representative evaluation of natural-distribution routing.

| Target | Range |
|--------|:-----:|
| service_memory | 28–34% of STORE units |
| task_state | 28–34% of STORE units |
| repo_memory | 16–22% of STORE units |
| project_memory | 10–16% of STORE units |
| user_profile | 5–10% of STORE units |

Shape distribution:
- READ+STORE joint: 35–45%
- STORE/SKIP-only: 30–40%
- READ-only: 18–25%

Gold core should feel like natural coding-agent interactions — representative of the target task, not artificially balanced or adversarially constructed.

### 4.3 Gold Hard (30 cases)

Purpose: Stress-test routing on the most challenging boundary decisions.

| Boundary | Cases | Description |
|----------|:-----:|-------------|
| service_vs_task_state | 5 | Durable behavior vs implementation action |
| project_memory_vs_task_state | 4 | Project scope vs version-specific config |
| repo_vs_service | 4 | File location vs component behavior |
| related_but_useless | 4 | Plausible but irrelevant candidate memories |
| stale_memory | 3 | Outdated memories that should not be READ |
| sensitive_boundary | 4 | Units with sensitive content → SKIP |
| user_profile_vs_sensitive | 3 | User preference vs private data |
| repo_vs_project | 3 | Repo convention vs project-wide policy |

Gold hard cases should:

- Include notes explaining why the boundary is hard.
- Be independently validated by a second reviewer before inclusion.
- NOT be used for training, prompt design, or checkpoint selection under any circumstances.
- Test specific failure modes observed in earlier experiments.

### 4.4 Source

Gold remains an **independent held-out evaluation set**, not split from train or dev.

**Gold core (70 cases):** Can be independently LLM-generated as a draft, then fully reviewed and adjudicated by the project owner. The LLM generation pass must be separate from both train-pool and dev generation.

**Gold hard (30 cases):** Should be manually curated or heavily rewritten when feasible. These boundary stress cases benefit from intentional adversarial design that LLM generation alone may not achieve.

**Advisory review:** Opus/ClaudeCode can provide advisory review comments, but **final acceptance is project-owner adjudication**. Do not overstate this as multi-human annotation — it is a single-human adjudication with LLM advisory input.

Gold cases should be:

- Generated independently from train pool AND dev (separate batch, different prompts).
- Enriched with explicit boundary-targeting designs for gold hard subset.
- Representative of the coding-agent task domain.
- NOT mechanically copied or paraphrased from any other split.

### 4.5 Review Level

| Review Type | Scope |
|-------------|-------|
| Structural validation | All 100 cases (automated) |
| DSL parse + canonical consistency | All 100 cases (automated) |
| **Full project-owner adjudication** | **All 100 cases** |
| LLM advisory review (Opus/ClaudeCode) | Advisory suggestions, not binding |
| Two-pass self-review (fallback) | All 100 cases, ≥24h gap |

Gold MUST receive full project-owner adjudication. Every unit, every READ decision, every STORE target, every SKIP must be reviewed and accepted by the project owner. LLM reviewers provide advisory input only.

### 4.6 Gold Locking

After all 100 gold cases are human-adjudicated and accepted:

1. Create a lock file: `data/v05/gold/v05_gold_lock.json`
2. Record:
   - SHA-256 hash of `v05_gold_cases.jsonl`
   - Timestamp of lock
   - Human adjudicator name
   - Number of cases (100)
   - Changelog from generation to lock

3. The gold file must never be modified after locking. If a serious error is discovered:
   - Document the error.
   - If fix is critical, unlock with explicit process, fix, re-lock, and record in changelog.
   - If fix is non-critical, note in error analysis but do not change gold.

---

## 5. Do-Not Rules

### 5.1 Absolute Prohibitions

| Rule | Rationale |
|------|-----------|
| ❌ No train cases copied into dev or gold | Leakage — inflates eval scores |
| ❌ No dev cases copied into gold | Gold must be independent of all tuning |
| ❌ No gold cases used for model selection | Defeats purpose of holdout |
| ❌ No gold cases used in system prompt | Prompt must not memorize gold |
| ❌ No few-shot examples from dev or gold | Few-shot must be train-sourced only |
| ❌ No prompt examples from gold | Prompt design must not peek at gold |
| ❌ No gold used for hyperparameter tuning | Inflates gold scores |
| ❌ No subset50 cases in train/dev/gold | Subset50 was used for A/B/C development — not a clean holdout |
| ❌ No v0.4 pilot cases mechanically copied | Different generation era, different label quality |
| ❌ No bridge cases mechanically copied | Bridge was boundary reference, not eval-standard data |

### 5.2 Recommended Cautions

| Rule | Rationale |
|------|-----------|
| ⚠ Avoid same domain + same scenario across splits | Even without text overlap, conceptual leakage can inflate scores |
| ⚠ Avoid same structural pattern across splits | Model may learn pattern rather than routing |
| ⚠ Avoid same target-boundary pattern across splits | Especially for gold hard — boundary patterns should be novel |
| ⚠ Verify dev ↔ gold independence | Ensure dev and gold don't share hidden patterns |

---

## 6. Construction Timeline (Proposed)

| Step | Context | Description |
|------|---------|-------------|
| 1 | 5.3-A | Plan (this document) |
| 2 | 5.3-B | Generate dev cases (80–100), validate |
| 3 | 5.3-C | Generate gold cases (100), validate |
| 4 | 5.3-D | Human adjudicate gold |
| 5 | 5.3-E | Lock gold, run leakage checks |
| 6 | 5.3-F | Finalize train pool, run all validations |
| 7 | 5.4 | Begin training |

---

## 7. Changelog

| Date | Change |
|------|--------|
| 2026-06-02 | Initial creation (Context 5.3-A) |

---

*End of V0.5 Dev/Gold Plan.*
