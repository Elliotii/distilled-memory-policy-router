# V0.5 Dev/Gold Planning Report

**Date:** 2026-06-02
**Context:** 5.3-A — dev/gold + provenance + leakage planning
**Status:** Planning complete — no data generated, no training

---

## 1. Summary

Context 5.3-A completed the **planning phase** for v0.5 dev/gold construction, label provenance documentation, policy distillation framing, leakage prevention, and evaluation methodology. Nine new documents were created defining the strategy for held-out set construction, human adjudication, baseline comparison, and statistical reporting. No data was generated, no splits were created, no training was conducted.

**Key outcome:** The project is now framed honestly as **memory policy routing distillation** from larger teacher models into a small Qwen3-4B router. LLM reviewers (ClaudeCode, Opus) are documented as LLM-based independent reviewers, not human ground truth. Gold will require full human adjudication.

---

## 2. Files Created

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 1 | `docs/v05/V05_LABEL_PROVENANCE_AND_DISTILLATION.md` | ~260 | Project framing, label provenance, human anchor, honest reporting, interview framing |
| 2 | `docs/v05/V05_TRAIN_POOL_MANIFEST_PLAN.md` | ~210 | Corrected batch500 status, future train file spec, file manifest, changelog rules |
| 3 | `docs/v05/V05_DEV_GOLD_PLAN.md` | ~260 | Dev/gold roles, construction strategy, gold core+hard split, do-not rules |
| 4 | `docs/v05/V05_LEAKAGE_AND_NEAR_DUP_PLAN.md` | ~270 | Leakage sources, prohibited leakage, near-dup checks (L1-L5), subset50 decision |
| 5 | `docs/v05/V05_GOLD_REVIEW_GUIDE.md` | ~310 | Per-case checklist, target-specific checklist, error patterns, adjudication protocol |
| 6 | `docs/v05/V05_EVAL_PROTOCOL.md` | ~280 | Systems to compare, teacher ceiling, metrics, success criteria, reporting |
| 7 | `docs/v05/V05_BASELINE_EVAL_PLAN.md` | ~270 | 12 baselines, rationale, same-prompt requirement, output table schema |
| 8 | `docs/v05/V05_STATISTICAL_REPORTING_PLAN.md` | ~260 | Bootstrap CI, learning curve, breakdown reporting, error analysis taxonomy |
| 9 | `reports/v05/v05_dev_gold_planning_report.md` | this file | Planning summary |
| 10 | `docs/status/CURRENT_STATE.md` | updated | Milestone, completed, open issues, next step |

**Total new documentation:** ~2,400 lines across 10 files.

No data files were created or modified.

---

## 3. Key Decisions

### 3.1 Policy Distillation Framing

The project is explicitly framed as **memory policy routing distillation**, not objective universal memory truth. This framing affects all reporting, interview answers, and evaluation claims. See `V05_LABEL_PROVENANCE_AND_DISTILLATION.md` §1.

### 3.2 Label Provenance

Train-pool labels are LLM-assisted with strict structural validation and LLM-based independent review. Gold labels will be human-adjudicated. LLM reviewers are documented as sanity checks, not human ground truth. See `V05_LABEL_PROVENANCE_AND_DISTILLATION.md` §2–4.

### 3.3 Corrected Batch500 Is Training-Pool Candidate

Corrected batch500 (500 cases) is explicitly NOT final train data. It must go through prerequisites (leakage checks, dev/gold construction, border case adjudication, source tag update) before becoming final train data. See `V05_TRAIN_POOL_MANIFEST_PLAN.md` §1.

### 3.4 Do NOT Mechanically Split Batch500

Dev and gold must be constructed independently — not mechanically sliced from corrected batch500. This prevents label-style artifacts from inflating eval scores and ensures evaluation tests generalization to independently constructed cases. See `V05_DEV_GOLD_PLAN.md` §1.2.

### 3.5 Gold Core + Hard Structure

Gold (100 cases) is split into gold_core (70, representative) and gold_hard (30, boundary stress). Gold hard covers 8 specific boundary types. See `V05_DEV_GOLD_PLAN.md` §4.

### 3.6 Gold Requires Full Human Adjudication

Gold must receive full human review — every unit, every READ, every STORE target, every SKIP. LLM reviewers provide advisory suggestions only. Two-pass self-review with ≥24h gap is the fallback if no second human reviewer is available. See `V05_GOLD_REVIEW_GUIDE.md` §5.

### 3.7 Leakage Prevention (5 Levels)

Five levels of leakage detection planned: exact text, normalized text, n-gram Jaccard, embedding similarity, and human review. Hard prohibitions on exact duplicates, gold-as-prompt-example, gold-for-tuning. See `V05_LEAKAGE_AND_NEAR_DUP_PLAN.md` §3.

### 3.8 Subset50 Retirement

Subset50 (used for A/B/C pilot) is recommended for retirement from final eval — not included in train, dev, or gold. See `V05_LEAKAGE_AND_NEAR_DUP_PLAN.md` §6.

### 3.9 12-System Baseline Comparison

Evaluation includes 12 systems: 5 deterministic baselines, 4 Qwen-based, 1 teacher (DeepSeek), 1 primary (trained LoRA), plus 1 JSON fallback. See `V05_BASELINE_EVAL_PLAN.md` §1.

### 3.10 Statistical Rigor Required

All metrics reported with 95% bootstrap CI. Learning curve (125/250/500 cases) on dev. Per-target, per-tag, gold_core vs gold_hard breakdowns. Sensitive store = 0 is a hard No-Go gate. See `V05_STATISTICAL_REPORTING_PLAN.md`.

---

## 4. How Opus Review Concerns Were Incorporated

Opus 4.8 raised a key methodology concern: the pipeline has strong mechanical validity but label provenance is LLM-heavy. The response is documented across all planning documents:

| Concern | Response | Document |
|---------|----------|----------|
| Labels are LLM-generated | Honest framing as policy distillation, not objective truth | `V05_LABEL_PROVENANCE_AND_DISTILLATION.md` §1 |
| LLM reviewers are not human ground truth | Explicitly documented as "LLM-based independent reviewers" | `V05_LABEL_PROVENANCE_AND_DISTILLATION.md` §2.2, §4 |
| Gold needs human adjudication | Full human adjudication protocol defined | `V05_GOLD_REVIEW_GUIDE.md` §5 |
| Honest reporting language required | Do/Don't say tables provided | `V05_LABEL_PROVENANCE_AND_DISTILLATION.md` §4 |
| Interview framing needed | Elevator pitch and Q&A provided | `V05_LABEL_PROVENANCE_AND_DISTILLATION.md` §5 |

---

## 5. Why Not Split Batch500 Directly

Mechanical random splitting of corrected batch500 into train/dev/gold would:

1. **Share label-generation artifacts** — the same LLM annotator's decision patterns would appear in all splits, inflating eval scores.
2. **Fail to test generalization** — eval wouldn't measure performance on independently constructed cases.
3. **Hide systematic label biases** — if the generating LLM has a systematic target bias (e.g., over-using service_memory), all splits would share this bias, making it invisible to evaluation.

Instead, dev and gold should be independently constructed while using the same schema, target taxonomy, and Unit DSL grammar. This tests whether the router generalizes beyond the specific cases and label patterns it was trained on.

---

## 6. Recommended Dev/Gold Sizes

| Split | Size | Rationale |
|-------|:----:|-----------|
| Train | 500 | Corrected batch500 (after prerequisites) |
| Dev | 80–100 | Enough for stable checkpoint selection while leaving room for gold |
| Gold core | 70 | Representative distribution, natural cases |
| Gold hard | 30 | Boundary stress — 8 specific boundary types, 3–5 cases each |
| **Gold total** | **100** | Standard for small-scale ML eval |

These sizes represent the upper bound of what's practical for this project given:
- Single human adjudicator for gold.
- LLM-assisted case generation pipeline.
- Need for leakage-free independent construction.
- Statistical constraints (n=100 gives reasonable CIs; n=30 for gold_hard gives wide but informative CIs).

---

## 7. Review Requirements

| Artifact | Review Level | Reviewer |
|----------|-------------|----------|
| Train pool (corrected batch500) | LLM-based independent review ✓ | Windows ClaudeCode |
| Train pool → final train | Leakage checks, border case adjudication | Project owner |
| Dev set | Structural + spot-check | Project owner |
| Gold set | Full human adjudication | Project owner + optional second human |
| Gold lock | Hash + timestamp | Project owner |

---

## 8. Leakage Prevention Summary

| Check | Method | When |
|-------|--------|------|
| Train↔Dev exact duplicates | L1 string match | Before training |
| Train↔Dev near-duplicates | L3 n-gram Jaccard | Before training |
| Train↔Gold exact duplicates | L1 string match | Before final eval |
| Train↔Gold near-duplicates | L3 n-gram Jaccard | Before final eval |
| Dev↔Gold exact duplicates | L1 string match | Before final eval |
| Few-shot in dev/gold | ID check | Before training |
| Prompt examples from gold | ID check | Before training |
| Subset50 in any split | ID check | Before training |

Thresholds:
- Exact duplicate (L1/L2): reject
- Jaccard ≥ 0.9: reject
- Jaccard ≥ 0.8: human review required
- Jaccard ≥ 0.5: batch review

---

## 9. Baseline and Eval Additions

Newly defined compared to v0.4:

| Addition | Description |
|----------|-------------|
| `per_target_majority` baseline | Quantifies target accuracy floor |
| `heuristic_lexical` baseline | Quantifies non-learned policy performance |
| `heuristic_read_all` baseline | Quantifies over-reading cost |
| Teacher ceiling concept | DeepSeek as policy reference, not truth |
| Bootstrap CI for all metrics | Statistical rigor for n=100 |
| Learning curve (125/250/500) | Data efficiency analysis |
| Gold core vs gold hard | Separate representative vs boundary eval |
| Target confusion matrix | Systematic error analysis |
| Boundary failure taxonomy | Categorizes and quantifies failure modes |
| Sensitive store hard gate | 0 tolerance, No-Go if violated |
| 12-system comparison table | Comprehensive baseline coverage |

---

## 10. Next Step

**Context 5.3-B: Dev Set Construction**

1. Generate 80–100 dev cases independently (separate prompt batch, different construction pass).
2. Validate structurally, DSL parse, canonical consistency.
3. Check distribution against train pool.
4. Run train↔dev leakage checks.
5. Spot-check semantic review.
6. Create `data/v05/dev/v05_dev_cases.jsonl` and `data/v05/dev/v05_dev_sft_messages.jsonl`.

Do not yet:
- Construct gold.
- Train models.
- Run inference.

---

## 11. Open Questions (Resolved)

1. **Second human reviewer availability:** Resolved — no second human available. Two-pass self-review with Opus/ClaudeCode advisory review is the accepted protocol. Formal IAA is not required.
2. **Dev generation method:** Resolved (Patch 1) — dev will be independently LLM-generated with a different construction pass/prompt seed from train-pool, with leakage checks before acceptance.
3. **Gold generation method:** Resolved (Patch 2) — gold_core can be independently LLM-generated draft + review; gold_hard should be manually curated or heavily rewritten. Final acceptance is project-owner adjudication.
4. **Subset50 retirement confirmation:** Retired from final eval. Preserved as historical evidence only.
5. **Leakage check implementation:** Implemented — `src/v05/check_leakage.py` created before dev generation (Context 5.3-A2).
6. **DeepSeek teacher evaluation timing:** After student training, to prevent any data leakage concerns. One-time measurement on gold.

## 12. No More Planning Loop

**The planning phase is complete.** The next concrete step after Context 5.3-A2 (this inline patch + leakage checker) is **Context 5.3-B: Dev Set Construction**. Do not create more methodology docs unless a blocker appears. Leakage checker is ready before dev acceptance.

---

*End of V0.5 dev/gold planning report.*
