# V0.5 Methodology Inline Patch Report

**Date:** 2026-06-02  
**Context:** 5.3-A2 — methodology inline patches + leakage checker implementation  
**Status:** Complete — patches applied, leakage checker implemented and tested  

---

## 1. Scope

This context applied **10 targeted inline patches** recommended by the Opus second-round methodology review to existing v0.5 planning docs. It also implemented the leakage / near-duplicate checking tool before dev construction. No new methodology docs were created; only inline edits to existing docs. No dev/gold data was generated, no models were trained.

---

## 2. Opus Second-Round Review Incorporated

Opus 4.8's second-round review approved the methodology quality overall but recommended several inline fixes before dev construction. The review explicitly warned against entering another planning loop. All 10 recommendations have been applied as targeted inline edits.

---

## 3. Files Updated

| # | File | Lines (approx) | Patches |
|---|------|:--------------:|---------|
| 1 | `docs/v05/V05_DEV_GOLD_PLAN.md` | ~290 | 1, 2 |
| 2 | `docs/v05/V05_EVAL_PROTOCOL.md` | ~310 | 3, 4 |
| 3 | `docs/v05/V05_BASELINE_EVAL_PLAN.md` | ~320 | 4b, 5, 6 |
| 4 | `docs/v05/V05_STATISTICAL_REPORTING_PLAN.md` | ~280 | 7 |
| 5 | `docs/v05/V05_LEAKAGE_AND_NEAR_DUP_PLAN.md` | ~300 | 8 |
| 6 | `docs/v05/V05_GOLD_REVIEW_GUIDE.md` | ~320 | 9 |
| 7 | `docs/v05/V05_LABEL_PROVENANCE_AND_DISTILLATION.md` | ~270 | 9 |
| 8 | `reports/v05/v05_dev_gold_planning_report.md` | ~100 | 10 |
| 9 | `docs/status/CURRENT_STATE.md` | ~200 | 10 |

**Total updated:** 9 docs, ~2,390 lines.

### New files created

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 10 | `src/v05/check_leakage.py` | ~350 | Leakage checker implementation |
| 11 | `tests/v05/__init__.py` | 0 | Test package init |
| 12 | `tests/v05/test_check_leakage.py` | ~330 | 28 unit tests |
| 13 | `reports/v05/v05_methodology_inline_patch_report.md` | this file | Patch summary |
| 14 | `reports/v05/v05_leakage_checker_smoke_report.md` | ~2600 | Self-check report |

---

## 4. Patch Details

### Patch 1: Dev Generation Method

**Files:** `V05_DEV_GOLD_PLAN.md` §3.4, `v05_dev_gold_planning_report.md` §11

**Change:** Dev will be independently LLM-generated with a different construction pass/prompt seed from train-pool generation. Dev generation must run leakage checks before acceptance. Dev is for checkpoint / hyperparameter / prompt-setting comparison only — not for final claims.

**Rationale:** Resolved the open question from the planning phase. Prevents same-LLM-artifact overlap between train and dev.

### Patch 2: Gold Construction Method

**Files:** `V05_DEV_GOLD_PLAN.md` §4.4–4.5

**Change:** gold_core can be independently LLM-generated draft + project-owner review. gold_hard should be manually curated or heavily rewritten when feasible. Opus/ClaudeCode can provide advisory review, but final acceptance is project-owner adjudication. Do not overstate as multi-human annotation.

**Rationale:** Practical scoping — keeps gold construction achievable for a single-human project while maintaining quality.

### Patch 3: Exact Match Demotion

**Files:** `V05_EVAL_PROTOCOL.md` §5.1–5.2

**Change:** `exact_match` demoted from primary required success metric to secondary strict metric. Primary metrics are now: STORE unit F1, STORE target accuracy, SKIP F1, READ F1, false store rate, sensitive store count = 0 hard gate, parse success.

**Rationale:** `exact_match` is overly strict — it penalizes minor differences like READ order that don't affect downstream memory quality. The primary metrics above capture real routing quality better.

### Patch 4: Teacher Ceiling Clarification

**Files:** `V05_EVAL_PROTOCOL.md` §3.2–3.3, `V05_BASELINE_EVAL_PLAN.md` §5.1

**Change:** DeepSeek teacher baseline should be evaluated against human-adjudicated gold. Teacher on gold is a policy reference / teacher ceiling estimate, not objective truth. Primary comparison should be each system vs gold, not teacher-student direct agreement.

**Rationale:** Prevents misinterpretation of teacher-student agreement as "accuracy." The gold is the evaluation standard; the teacher is an aspirational reference.

### Patch 5: qwen_few_shot_json Baseline

**Files:** `V05_BASELINE_EVAL_PLAN.md` §1, §2, §3.2, §4

**Change:** Added `qwen_few_shot_json` baseline — Qwen3-4B few-shot Unit JSON (3 examples from train). System count increased from 12 to 14.

**Rationale:** Prevents unfair DSL-vs-JSON comparison where DSL gets few-shot and JSON only gets zero-shot. If `qwen_few_shot_json` matches `qwen_few_shot_dsl`, the interface format difference is negligible.

### Patch 6: Optional Shuffled-Label Sanity Baseline

**Files:** `V05_BASELINE_EVAL_PLAN.md` §1, §2, §4

**Change:** Added `qwen_lora_dsl_shuffled_labels` — Qwen3-4B LoRA trained on Unit DSL with shuffled labels. System count increased to 14. Marked as optional — do not block training if time is limited.

**Rationale:** Sanity check that LoRA learns routing signal rather than only output format. If model achieves comparable routing metrics with shuffled labels, training is dominated by format learning.

### Patch 7: Statistical Reporting

**Files:** `V05_STATISTICAL_REPORTING_PLAN.md` §2.1, §3.1–3.2

**Change:** Use paired bootstrap for system comparison on the same gold cases. Learning curve subsets must be nested (125 ⊂ 250 ⊂ 500). Fixed random seed. Record case_id lists for each subset.

**Rationale:** Paired bootstrap preserves the paired structure of case-level comparisons. Nesting ensures the learning curve shows the effect of adding data, not sampling different subsets. Fixed seed ensures reproducibility.

### Patch 8: Leakage Plan Enhancements

**Files:** `V05_LEAKAGE_AND_NEAR_DUP_PLAN.md` §3.4–3.5, §4

**Change:** Added short-text token Jaccard / word-level fallback for texts with fewer than 3 words. Added scenario collision trigger using runtime_context tuple `(project, repo, service, task)`. Clarified thresholds: exact duplicate = reject (hard block), high near-duplicate = review, same domain alone = allowed if text/scenario differ.

**Rationale:** Short texts produce empty n-gram sets — token fallback handles this edge case. Scenario collision catches same-domain reuse even when text differs.

### Patch 9: Gold Review Honest Wording

**Files:** `V05_GOLD_REVIEW_GUIDE.md` §5.3, `V05_LABEL_PROVENANCE_AND_DISTILLATION.md` §3.2

**Change:** Clarified that LLM reviewers are advisory only. Two-pass self-review with Opus/ClaudeCode advisory is the expected path for this project. Formal IAA (Cohen's kappa) is NOT required as a blocker. Do not block dev construction waiting for a second human reviewer. Do not claim multi-human annotation.

**Rationale:** Keeps the project practically scoped. Honest about single-human adjudication with LLM advisory input. Prevents human review planning from blocking dev construction.

### Patch 10: No More Planning Loop

**Files:** `v05_dev_gold_planning_report.md` §11–12, `CURRENT_STATE.md`

**Change:** All 6 open questions from planning report resolved. Explicitly stated that the next concrete step after this patch is dev set construction. No more methodology docs to be created unless a blocker appears.

**Rationale:** Prevents planning-loop anti-pattern. Forces forward momentum toward dev construction.

---

## 5. Remaining Non-Blocking Limitations

1. **No second human reviewer** — accepted as project constraint. Two-pass self-review with Opus/ClaudeCode advisory is the protocol.
2. **Gold size = 100** — provides reasonable CIs for main metrics but wide CIs for per-target breakdowns (especially user_profile with ~5 cases).
3. **Gold hard = 30** — wide CIs expected; results are indicative, not definitive.
4. **LLM-assisted label pipeline** — labels carry LLM biases that may inflate teacher-student agreement. Transparently documented.
5. **Cross-batch duplicate memory** — low severity, affects train pool only, not dev/gold.

---

*End of V0.5 methodology inline patch report.*
