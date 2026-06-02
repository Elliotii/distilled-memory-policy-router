# CURRENT_STATE

## Last Updated
2026-06-02  CST

## Current Milestone
P5.21-A: v0.5b final report consolidation and snapshot readiness

## Completed

### P5.21-A (This Context)
- Created v0.5b final consolidated reports:
  - `reports/v05b/v05b_final_project_report.md` — Executive summary + full results
  - `reports/v05b/v05b_final_experiment_summary.md` — Concise tables
  - `reports/v05b/v05b_final_claims_and_limitations.md` — Allowed/forbidden claims
  - `reports/v05b/v05b_final_error_analysis.md` — What JSON fixed/didn't fix
  - `reports/v05b/v05b_final_artifact_manifest.md` — What to commit
  - `reports/v05b/v05b_v05c_safety_ablation_plan.md` — v0.5c plan (not run)
  - `reports/v05b/v05b_git_handoff_checklist.md` — Commit commands
  - `reports/v05b/v05b_final_report_consistency_check.md` — Cross-report audit
- Created v0.5b docs:
  - `docs/v05b/V05B_FINAL_RESULTS.md` — Concise results page
  - `docs/v05b/V05B_PROJECT_NARRATIVE.md` — Story of the experiment
  - `docs/v05b/V05C_SAFETY_ABLATION_PLAN.md` — Mirror of safety plan
- **Final consistency check: All 34 reports present, gold hash unchanged, no forbidden claims**
- Large file scan: only .venv (virtual env), no project files >50MB
- Secret scan: docs/reports/prompts/configs/src clean (no real secrets)
- Gold hash unchanged: `56e16078...`
- Unit tests: 77/77 OK
- **v0.5b ready for manual review and git snapshot**

### P5.20-A (Previous)
- Verified gold hash before and after: `56e16078...` unchanged
- Evaluated Qwen3-4B Unit JSON LoRA 500 on locked gold (100 cases)
  - 100 predictions generated, 100% JSON valid, 0 structural errors
- **JSON LoRA 500 gold metrics:**
  - Parse success: **100.0%** (400/400 across all predictions)
  - Exact: **31.0%** (↑15pp vs DSL 500, ↑5pp vs Qwen3-4B JSON fs)
  - READ F1: **0.919**
  - STORE F1: **0.941** (vs DSL 500 0.946, within 0.005)
  - Target accuracy: **67.3%** (↑19.8pp vs DSL 500, ↑9.8pp vs Qwen3-4B JSON fs)
  - SKIP F1: 0.706 (vs DSL 500 0.718)
  - Sensitive store: 6 genuine failures (credit card, 2 tokens, 2 phones, 1 address)
    - Tied with DSL 500 (also 6 failures)
    - Qwen3.5 JSON fs: 0 failures — safety gap remains
- **Gold baseline comparison:**
  - JSON 500 ranks #3 overall behind Qwen3.5 JSON fs (#1) and Qwen3.5 DSL fs (#2)
  - JSON 500 beats DSL 500 on exact (+15pp), target acc (+19.8pp)
  - JSON 500 beats Qwen3-4B JSON fs on exact (+5pp), STORE F1 (+0.018), target acc (+9.8pp)
- **Dev→gold delta:** target acc -1.2pp (excellent generalization), exact -3pp
- **Target confusion audit:** service_memory 70% on gold (DSL: ~25%), repo_memory weakest (50%)
- **Sensitive store audit:** 6/10 failures catalogued with case-level detail
- Created 9 reports: gold eval, error analysis, baseline comparison, dev vs gold delta, sensitive store audit, target confusion audit, final learning curve, final result decision, ablation summary
- **Final v0.5b decision: Result B — Unit JSON LoRA improves target routing but still trails Qwen3.5 prompting**
  - JSON > DSL confirmed (+19.8pp target acc on gold)
  - JSON SFT > JSON prompting confirmed (beats teacher on exact + STORE + target)
  - Qwen3.5 JSON fs remains strongest overall
  - Safety not solved (6 failures, same as DSL)
- **Recommended next:** safety-focused training, target-balanced training, Qwen3.5 JSON LoRA
- **Unit JSON is now the preferred training interface** for all future work
- Gold hash unchanged, 77/77 tests pass
- **v0.5b Unit JSON LoRA ablation complete**

### P5.19-D (Previous)
- Preflight passed: all checks OK
- Trained Qwen3-4B Unit JSON QLoRA on 500 JSON SFT cases
  - Duration: 842s (14m 2s), no OOM/NaN
  - Eval loss: 0.611 → 0.548 → **0.544** (lowest of all LoRA variants)
  - Mean token accuracy: 86.5% → 87.1% → **87.2%**
  - Adapter saved to `results/v05b_lora/qwen3_4b_json_500/adapter/`
- Evaluated on dev: 100 predictions, 100% JSON valid
- **JSON 500 dev metrics:**
  - Parse success: **100.0%** (300/300 across all sizes)
  - Exact: **34.0%** (↑23pp from 125, ↑10pp vs DSL 500)
  - READ F1: **0.902**
  - STORE F1: **0.958** (within 0.003 of JSON fs 0.961)
  - Target accuracy: **68.5%** (↑12.8pp from 125, **↑14.4pp vs DSL 500**)
  - SKIP F1: **0.753** (↑0.218 from 125)
  - Sensitive store: 66.7% eval; genuine audit: 1/4 = 25% (1 phone number as user_profile)
- **JSON 500 beats Qwen3-4B JSON few-shot on exact (+11pp) and target accuracy (+1.4pp)**
- **JSON 500 beats DSL 500 on target accuracy by 14.4pp**
- **target confusion audit:** service_memory 91.5% accurate (↑from 55% at 125); service→task_state confusion reduced from 42% to 4%
- **Learning curve confirmed:** all metrics improve 125→250→500 except sensitive store
- Created 8 reports: train, dev eval, error analysis, learning curve, vs DSL 500, sensitive store audit, target confusion audit, gold readiness
- **Gold readiness decision: Option A — Ready for locked-gold final evaluation**
- Gold hash unchanged: `56e16078...`
- Unit tests: 77/77 OK
- **v0.5b Unit JSON LoRA learning curve complete — JSON is a clear winner over DSL for SFT**

### P5.19-C (Previous)
- Preflight passed: all checks OK
- Trained Qwen3-4B Unit JSON QLoRA on 250 JSON SFT cases
  - Duration: 367s, no OOM/NaN
  - Eval loss: 1.326 → 0.659 → **0.608** (very strong convergence)
  - Mean token accuracy: 72.7% → 85.5% → **86.5%**
  - Adapter saved to `results/v05b_lora/qwen3_4b_json_250/adapter/`
- Evaluated on dev: 100 predictions, 100% JSON valid, 0 structural errors
- **JSON 250 dev metrics:**
  - Parse success: 100% (maintained)
  - Exact: **20.0%** (↑9pp from JSON 125, ↑6pp vs DSL 250)
  - STORE F1: **0.947** (↑0.037 from 125, exceeds DSL 250's 0.944)
  - Target accuracy: **63.8%** (↑8.1pp from 125, ↓ vs JSON fs 67.1%)
  - SKIP F1: **0.747** (↑0.212 from 125 — dramatic improvement)
  - Sensitive store: 66.7% (↑33.4pp — matches DSL 250; inherent data limitation)
- **Critical finding: JSON target accuracy INCREASES with data (55.7%→63.8%) while DSL DECREASES (60.0%→55.7%→54.1%).**
  - JSON 250 (63.8%) already exceeds DSL 500 (54.1%) by 9.7pp on target accuracy
- JSON 250 dominates DSL 250 on 5 of 5 primary metrics
- Created 6 reports: train, dev eval, error analysis, vs JSON 125, vs DSL, smoke decision
- Smoke decision: **Option A — Proceed to JSON LoRA 500 unchanged**
- Gold hash unchanged: `56e16078...`
- Unit tests: 77/77 OK
- **JSON format is a clear winner over DSL for SFT training — target classification is the killer differentiator**

### P5.19-B (Previous)
- Preflight passed: all 12 checks OK (config, data, CUDA, gold hash)
- Trained Qwen3-4B Unit JSON QLoRA on 125 JSON SFT cases
  - Duration: 217s, no OOM/NaN
  - Eval loss: 1.919 → 1.424 → 1.300 (strong convergence)
  - Adapter saved to `results/v05b_lora/qwen3_4b_json_125/adapter/`
- Evaluated on dev: 100 predictions, 100% JSON valid, 0 structural errors
- JSON parse success: **100%** vs DSL LoRA 125 86% (+14pp)
- STORE F1: **0.910** vs DSL LoRA 125 0.867 (+0.043)
- READ F1: **0.889** vs DSL LoRA 125 0.822 (+0.067)
- SKIP F1: **0.535** vs DSL LoRA 125 0.492 (+0.043)
- Target accuracy: 55.7% vs DSL LoRA 125 60.0% (-4.3pp, small-N effect)
- Sensitive store: 33.3% unchanged (inherent data limitation)
- 0 invalid IDs, 0 invalid targets, 0 markdown, 0 empty outputs
- Created 5 reports: train, dev eval, error analysis, vs DSL 125, smoke decision
- Smoke decision: **Option A — Proceed to JSON LoRA 250 unchanged**
- Gold hash unchanged: `56e16078...`
- Unit tests: 77/77 OK
- **v0.5b Unit JSON LoRA 125 smoke complete — JSON format is a clean structural win**

### P5.19-A (Previous)
- Created v0.5b experiment definition: Unit JSON LoRA ablation
- Created `src/v05/render_json_sft_messages.py` — JSON SFT rendering script
- Rendered 4 JSON SFT files: 125, 250, 500 train + dev (975 total rows)
- All validations pass: JSON parse 100%, canonical consistency 0 mismatches, unit coverage 100%, 0 illegal targets, 0 markdown/prose
- Created 3 v0.5b JSON LoRA configs (125/250/500) based on v0.5 DSL configs
- Updated `eval_lora_router.py` with `--interface` parameterization (unit_dsl / unit_json)
- Updated `train_lora_router.py` preflight with interface-aware logging
- Script compatibility audit complete: train/eval/eval_runner all support unit_json
- Created 6 v0.5b reports: plan, SFT rendering, SFT validation, config, usage policy, readiness
- Updated `docs/v05b/V05B_UNIT_JSON_LORA_PLAN.md`
- Gold hash unchanged: `56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d`
- Unit tests: 77/77 OK
- **No training, no inference, no gold use — readiness only**
- **v0.5b Unit JSON LoRA ready for 125-case smoke training**

### P5.18-A (Previous)
- Created README_v05.md — public-facing project summary
- Created docs/v05/V05_FINAL_RESULTS.md — concise results page
- Created docs/v05/V05_REPRODUCIBILITY_GUIDE.md — commands and splits
- Created docs/v05/V05_REPO_ARTIFACT_POLICY.md — git inclusion guidance
- Created reports/v05/v05_git_handoff_checklist.md — manual commit checklist
- Large file scan: only .venv (virtual env), no project files >50MB
- Secret scan: docs/reports/prompts/configs clean, .env not tracked
- Gold hash unchanged
- **v0.5 complete and packaged for portfolio**

### P5.17-B (Previous)
- Completed 4 missing final reports (project, LoRA vs prompting, error analysis, artifact manifest)
- All 8 final reports present and consistent
- Consistency QA: gold hash verified, no metric mixing, forbidden claims appear only in "Do NOT claim" context
- v0.5b ablation plan documents 6 candidate experiments with priority ordering
- Final status: **v0.5 experiment complete** — negative but informative result
- Strongest system: Qwen3.5 JSON few-shot (42% exact, 0.963 STORE F1, 0 sensitive)
- v0.5b recommended priority: Unit JSON LoRA → target-balanced → safety-weighted

### P5.17-A (Previous)
- Created final consolidated reports: experiment summary, claims/limitations, resume narrative, ablation plan
- Final v0.5 result: LoRA improves action routing but not competitive overall
- Strongest system: Qwen3.5 JSON few-shot (42% exact, 0.963 STORE F1, 0% sensitive on gold)
- LoRA 500: 16% exact, 0.946 STORE F1, 6 sensitive failures including credit card
- Main bottleneck: target classification (service_memory 25% accuracy on gold)
- Safety issue: model stores sensitive info as user_profile
- v0.5b plan: 6 candidate ablations (JSON, target-balanced, safety, r16, epochs, two-stage)
- All claims and limitations documented
- Gold hash unchanged

### P5.16-A (Previous)
- Evaluated LoRA 500 on locked gold: 16% exact, 0.946 STORE F1, 47.5% target acc, 0.718 SKIP F1
- Gold STORE F1 (0.946) beats Qwen3-4B DSL fs (0.850) but not Qwen3.5 JSON fs (0.963)
- Sensitive: 6 failures including credit card stored as user_profile — safety-critical
- Service memory target accuracy: 25% — model cannot distinguish svc from task_state
- Decision: Result D — LoRA 500 not competitive with prompting baselines
- Honest result: SFT improves STORE/SKIP but fails on target classification and safety
- Qwen3.5 JSON few-shot remains the strongest system for v0.5
- Gold hash unchanged before and after

### P5.15-F (Previous)
- Train500 eval: 34% exact, 0.977 STORE F1, 56.7% target acc
- Train target acc (56.7%) only +2.6pp over dev (54.1%) — model at ceiling, not overfitting
- Per-target accuracy: user_profile 100%, task_state 65%, service_memory 47%, repo_memory 41%, project_memory 42%
- Dominant confusion: service_memory→task_state (30 cases). Model defaults to task_state.
- More of same data won't help target accuracy; target-balanced training is future ablation
- Sensitive: 6 genuine failures (contacts→user_profile)
- Decision: **Option A — Ready for locked-gold final eval** (STORE F1 strong, target acc caveated)
- Gold hash unchanged

### P5.15-E (Previous)
- Trained 500-case QLoRA: 573s, eval loss 0.69→0.63→0.62, strong convergence
- **Dev eval: 24% exact, 0.962 STORE F1, 54.1% target acc, 0.773 SKIP F1**
- STORE F1 (0.962) nearly matches Qwen3.5 JSON few-shot (0.963 on gold)
- Exact (24%) beats Qwen3-4B DSL few-shot (22%)
- Learning curve confirms STORE/SKIP improves with data; target classification plateaus at 54%
- 6 genuine sensitive failures (contacts stored as user_profile), no credentials stored
- Decision: Proceed to locked gold final eval (STORE F1 strong, target acc caveated)
- Gold hash unchanged

### P5.15-D (Previous)
- Audited 250 LoRA: STORE F1 0.944 beats few-shot, target acc 55.7% lagging
- Target confusion: model overuses task_state (most common class), needs more data for rare targets
- Sensitive store: 3 genuine failures (phone+2 emails), eval_runner 66.7% inflated by tag-based false positives
- Train250 target acc (50.4%) lower than dev (55.7%) — model underfitting targets, not overfitting
- 125→250: STORE F1 +0.077, exact +2pp, parse +10pp — all improving
- Decision: Proceed to 500 unchanged (STORE F1 crossed baseline, target accuracy needs more data)
- Gold hash unchanged

### P5.15-C (Previous)
- Trained 250-case QLoRA: 326s, eval loss 1.54→0.73→0.68, strong convergence
- Dev eval: 14% exact, **0.944 STORE F1 (beats few-shot 0.936!)**, 55.7% target acc, 0.684 SKIP F1
- STORE F1 crossed few-shot baseline — model learning WHAT to store but needs more target accuracy
- 125→250 learning curve: STORE F1 +0.077, exact +2pp, target acc -4.3pp (target classification lags)
- Decision: Proceed to 500 (STORE F1 already beats few-shot, more data needed for target accuracy)
- Gold hash unchanged

### P5.15-B (Previous)
- Audited 125 LoRA artifacts: adapter loads correctly, 23.6MB, PEFT LoRA
- Dev eval: 25% parse failures (memory-ID-as-unit-ID), 10% exact
- Train125 eval: 13.6% exact — no overfitting, model undertrained
- Found eval prompt mismatch: eval_lora_router used different prompt than SFT training
- Fixed eval_lora_router to use SFT system prompt (SYSTEM_PROMPT from render_sft_messages)
- Retested dev: 12% exact (↑2pp), 0.867 STORE F1 (↑0.074)
- Decision: Proceed to 250 unchanged (eval prompt fix applied, model undertrained, more data needed)
- Created postmortem, adapter sanity, next-step decision reports
- Gold hash unchanged

### P5.15-A (Previous)
- Created 3 missing reports to complete status documentation
- Created training script (train_lora_router.py) and eval script (eval_lora_router.py)
- Preflight passed: train 125, eval 100, CUDA OK, no gold leaks
- Training completed: 239s, eval loss 2.30→1.67→1.52, no OOM/NaN
- Dev eval: 10% exact, 0.793 STORE F1 (below few-shot baseline 22%/0.936)
- 125-case LoRA does NOT beat few-shot — expected for small training set
- Decision: PROCEED to 250-case training (pipeline works, learning curve should improve)
- Gold hash unchanged, no gold used

### P5.14-B (Previous)
- Addressed ClaudeCode independent training-readiness review findings
- Fixed QLoRA configs: eval/save changed from steps→epoch (125/250 now get checkpoints)
- Created 7 missing/requested reports: train subset manifest, split integrity, LoRA config, pretraining decision, gold baseline artifact audit, training readiness cleanup, 125 smoke runbook
- Documented eval_loss caveat, LR fallback plan, cross-batch duplicate status
- Created QLoRA 125 smoke runbook with exact command, success criteria, failure handling
- Gold hash unchanged, all SFT validated, unittest 77/77
- No training, no inference

### P5.14-A (Previous)
- Audited gold baseline artifacts: 800 preds, 8 systems, all have prompt hashes, gold unchanged
- Created final train pool: 500 cases + 500 SFT messages under data/v05/train/
- Created nested subsets: 125 ⊂ 250 ⊂ 500 with stratified random sampling (seed=42)
- All SFT messages validated (assistant==gold.dsl), nesting verified, splits disjoint
- Leakage: train↔dev 0 hard blockers, train↔gold 0 hard blockers
- Train environment: PyTorch 2.6, CUDA 12.4, PEFT 0.19, TRL 1.5, bitsandbytes 0.49, accelerate 1.13 — all ready
- Created 3 QLoRA config files (125/250/500) for Qwen3-4B Unit DSL
- Created pretraining decision report: Qwen3-4B Unit DSL QLoRA, target beat Qwen3.5 JSON fs
- Gold hash unchanged, unittest 77/77
- No training, no inference

### P5.13-E (Previous)
- First use of locked gold for final baseline evaluation
- Qwen3-4B: 400 gold predictions, 0 errors
- Qwen3.5: 400 gold predictions, 0 errors
- Evaluated 800 predictions on locked gold
- **Best system: Qwen3.5 JSON few-shot (42% exact, 0.963 STORE F1, 100% parse)**
- Qwen3.5 DSL few-shot: 36% exact, 0.959 STORE F1, 98% parse
- Qwen3-4B DSL few-shot: 7% exact (dropped from 22% on dev — significant negative transfer)
- **Sensitive store: 0% on all few-shot gold systems** ✅
- JSON generalized better than DSL across both models
- Gold hash unchanged before and after
- Recommended Qwen3-4B as LoRA base (practical, smaller, faster)
- LoRA target: beat Qwen3.5 JSON fs (42% exact, 0.963 STORE F1)

### P5.13-D (Previous)
- Updated runner to load prompts from files, record SHA-256 hashes
- Qwen3-4B: 400 predictions (100 cases × 4 variants), 0 errors, ~8.5 min
- Qwen3.5: 400 predictions (100 cases × 4 variants), 0 errors, ~13 min
- Evaluated 800 predictions on dev: Qwen3.5 DSL few-shot leads (41% exact, 0.975 STORE F1, 99% parse)
- Selected Qwen3.5 DSL few-shot as primary locked-gold baseline
- Selected Qwen3-4B as LoRA base candidate (competitive, smaller, faster)
- Created 4 dev reports: run, comparison, selection, prompt hash
- Sensitive store warning: 33.3% on dev — LoRA training expected to improve
- Gold NOT used — all evaluation on dev only

### P5.13-C (Previous)
- Root cause audit: 3 causes identified (non-canonical interfaces, single-message prompt, Qwen3.5 thinking)
- Fixed runner: SFT-style chat roles, canonical interface names, thinking suppression
- Fixed prompt: comma-separated READ, system+user role separation, few-shot as conversation turns
- Qwen3-4B retry: 20/20 predictions, 100% DSL parse, 100% JSON parse
- Qwen3.5 retry: 20/20 predictions, 100% DSL few-shot parse, 80% DSL zero-shot, 100% JSON few-shot
- Qwen3.5 latency dropped from 19s → 1-3s after thinking suppression
- Best performer: Qwen3.5 DSL few-shot (40% exact, 1.000 STORE F1, 80% target acc)
- Full dev baseline criteria met — both models cleared for 100-case dev run
- Gold NOT used — all smoke on dev only

### P5.13-B (Previous)
- Downloaded Qwen3.5-4B (8.8 GB, 2 safetensors) to `/home/abc16/hf_models/Qwen3.5-4B` via HF mirror
- Created 4 v0.5 prompt templates under `prompts/v05/` (DSL zs/fs, JSON zs/fs)
- 5 few-shot examples from train-pool: v05_sample_0001, 0005, 0009, 0010, 0004 (no dev/gold used)
- Selected 5 dev smoke cases: v05_dev_0001, 0019, 0058, 0020, 0037
- Built v0.5 runner: `src/v05/qwen_v05_output_runner.py`
- Ran Qwen3-4B smoke: 5×4=20 preds, 0 errors, ~500ms avg latency, empty outputs
- Ran Qwen3.5 smoke: 5×4=20 preds, 0 errors, ~19s avg latency, verbose prose outputs
- Evaluated with eval_runner: 0% parse success — prompt format needs revision
- Created 6 smoke reports + prompt README
- Gold NOT used — all smoke on dev only

### P5.13-A (Previous)

### P5.12-E (Previous)
- Verified all 4 prelock SHA-256 hashes match expected values
- Ran full prelock validation suite (structural, DSL, canonical, coverage, sensitive, SFT, leakage, tests)
- All validations pass: 100/100 DSL parse, 100/100 canonical, 0 sensitive STORE, 0 hard blockers
- Created lock manifest: `data/v05/gold/v05_gold_lock.json` with full metadata
- Created lock report: `reports/v05/v05_gold_lock_report.md`
- Created eval usage guide: `reports/v05/v05_gold_locked_eval_usage.md`
- Gold is now LOCKED — immutable for final evaluation only

### P5.12-D (Previous)
- Applied Opus lightweight final review metadata cleanup
- Regenerated 24 damaged notes (fixed uu1 typo, removed truncation, added policy rationale)
- Rewrote 10 service_memory u2 units from project-style to service-style wording
- Fixed fixes report typo (hard_0014 Group C incorrectly said SKIP u2,u3)
- Zero label changes; zero DSL structural changes
- Regenerated SFT messages with corrected metadata
- Ran all validations: 100/100 DSL parse, unit coverage, canonical consistency, leakage
- Created 3 new reports: metadata cleanup, prelock validation, prelock hash manifest
- Updated 2 existing reports: review readiness, semantic audit
- All validations pass; train↔gold: 0 hard blockers; dev↔gold: 0 hard blockers; unittest: 77/77 OK
- Gold remains DRAFT — NOT locked, NOT for training
- Recommended next step: two-pass self-review adjudication → lock gold

### P5.12-C (Previous)
- Applied all 12 Opus advisory review fixes across 5 groups (A-E)
- Rolled back 8 distribution-driven svc→proj changes to service_memory
- Reclassified 1 false user_profile (v05_gold_core_0021 u1 → svc)
- Changed work email to SKIP (v05_gold_hard_0014 u2)
- Fixed phone number collision (v05_gold_hard_0015 u3 +1-555-0198 → +1-555-0147)
- Replaced too-easy gold_hard_0013 with genuine repo-vs-service boundary case
- Reviewed 5 borderline cases: 2 changed (0062, 0069 → svc), 3 kept (0045, 0048, 0049)
- Synchronized notes for all 23 post-processing adjusted cases
- Created corrected gold files: combined (100), core (70), hard (30), SFT (100)
- Created 7 reports: fixes, corrected data, corrected semantic audit, corrected SFT validation, corrected review readiness, corrected hash manifest, train/dev leakage
- All validations pass; train↔gold: 0 hard blockers; dev↔gold: 0 hard blockers; unittest: 77/77 OK
- Gold remains DRAFT — NOT locked, NOT for training

### P5.12-B (Previous)
- Created comprehensive gold review packet with full expansion of all 30 gold_hard cases
- Documented all 25 post-processing target adjustments in detail
- Fixed 2 text errors from post-processing (v05_gold_core_0055 u2, v05_gold_core_0056 u2)
- Created 9 reports for Opus advisory review
- Re-validated all cases, regenerated SFT, reran leakage checks
- All validations pass; leakage: 0 hard blockers; unittest: 77/77 OK
- Sent gold draft to Opus/ClaudeCode advisory review; Opus returned Correction Required
- Gold remains DRAFT — not locked, not for training

### P5.12-A (Previous)
- Generated 100-case gold draft: 70 gold_core + 30 gold_hard
- Gold constructed independently from both train-pool (batch500) and dev set
- Six new project domains (ci-pipeline, content-platform, financial-reporting, health-monitor, shipping-logistics, compliance-audit)
- All structural/DSL/canonical validations pass
- Distribution post-processed to target ranges (svc 32.7%, task 33.6%, repo 17.1%, proj 11.8%, user 4.7%)
- Train↔gold leakage: 0 hard blockers, 1 warning (phone number pattern, score 0.533, accepted)
- Dev↔gold leakage: 0 hard blockers, 0 warnings
- SFT messages generated: 100 rows, all valid
- Gold is DRAFT only — NOT locked, NOT for training, NOT for model selection
- Created render_gold_draft.py as frozen-data writer (loads from canonical JSONL)
- No training, no model inference, no API calls

### P5.11-B (Previous)
- Rewrote render_dev.py as frozen-data writer (reads canonical JSONL, validates, writes SFT)
- Fixed 5 case notes to match post-processed target labels
- Full medium-risk review of v05_dev_0060 and v05_dev_0061 — both accepted
- Reviewed leakage warning — confirmed natural domain overlap, no replacement needed
- Created acceptance report, medium-risk review, reproducibility report, hash manifest
- All validations pass; leakage: 0 hard blockers; unittest: 77/77 OK
- Dev set formally accepted for model-selection use
- No gold generated, no training, no model inference

### P5.11-A (Previous)
- Generated 100 independent dev cases with balanced target/shape distributions
- Created dev JSONL (`data/v05/dev/v05_dev_cases.jsonl`) and SFT messages (`data/v05/dev/v05_dev_sft_messages.jsonl`)
- Implemented `src/v05/render_dev.py` for dev case generation
- Ran leakage checker: 0 hard blockers, 1 medium warning (natural domain overlap)
- Created 5 reports: construction, data, leakage, semantic audit, SFT validation
- All validations pass (structural, DSL parse, canonical consistency, sensitive=0)
- Unittest status: 77/77 OK
- No gold generated, no training, no model inference

### P5.10-B (Previous)

### P5.10-A (Previous)
- Created 9 planning documents for dev/gold construction, provenance, leakage, evaluation
- Established policy distillation framing — honest reporting of LLM-assisted labels
- Documented label provenance: LLM-assisted generation + validation + LLM-based independent review
- Defined human adjudication protocol for gold (two-pass self-review as fallback)
- Planned dev/gold as independently constructed held-out sets (NOT mechanically split from batch500)
- Defined 5-level leakage/near-duplicate detection (exact → embedding similarity → human review)
- Planned gold structure: 70 gold_core + 30 gold_hard
- Defined 12-system baseline comparison inventory
- Planned statistical reporting: bootstrap CI, learning curve, error analysis taxonomy
- Established sensitive store = 0 as hard No-Go gate
- Retired subset50 from final eval
- Updated CURRENT_STATE.md

### P5.10-B (This Context)
- Applied 10 Opus second-round review methodology inline patches to existing docs
- Implemented leakage / near-duplicate checking tool: `src/v05/check_leakage.py`
- Added 28 unit tests: `tests/v05/test_check_leakage.py`
- Ran leakage checker smoke self-check on corrected batch500
- Created methodology patch report: `reports/v05/v05_methodology_inline_patch_report.md`
- Created smoke report: `reports/v05/v05_leakage_checker_smoke_report.md`
- Updated CURRENT_STATE.md
- No dev/gold generated, no training, no model inference

## Methodology Patches Applied

| # | Patch | Files Updated |
|---|-------|--------------|
| 1 | Dev generation method resolved — independently LLM-generated, separate prompt seed | V05_DEV_GOLD_PLAN.md, v05_dev_gold_planning_report.md |
| 2 | Gold construction method — gold_core LLM draft+review, gold_hard manually curated, project-owner adjudication | V05_DEV_GOLD_PLAN.md |
| 3 | exact_match demoted from primary to secondary strict metric | V05_EVAL_PROTOCOL.md |
| 4 | Teacher ceiling clarification — DeepSeek on gold is policy reference, primary comparison is each system vs gold | V05_EVAL_PROTOCOL.md, V05_BASELINE_EVAL_PLAN.md |
| 5 | qwen_few_shot_json baseline added | V05_BASELINE_EVAL_PLAN.md |
| 6 | qwen_lora_dsl_shuffled_labels optional sanity baseline added | V05_BASELINE_EVAL_PLAN.md |
| 7 | Paired bootstrap for system comparison, nested learning curve subsets (125 ⊂ 250 ⊂ 500), fixed seed | V05_STATISTICAL_REPORTING_PLAN.md |
| 8 | Short-text token Jaccard fallback, scenario collision trigger, exact=reject, near-dup=review | V05_LEAKAGE_AND_NEAR_DUP_PLAN.md |
| 9 | Honest gold review wording — LLM advisors are advisory, no IAA blocker, don't block on second human | V05_GOLD_REVIEW_GUIDE.md, V05_LABEL_PROVENANCE_AND_DISTILLATION.md |
| 10 | No more planning loop — next step is dev construction | v05_dev_gold_planning_report.md, CURRENT_STATE.md |

## Leakage Checker Status

| Item | Status |
|------|--------|
| Implementation | ✅ `src/v05/check_leakage.py` (350 lines) |
| Unit tests | ✅ 28/28 pass (77 total with v04 tests) |
| Smoke self-check | ✅ Run on corrected batch500 → expected exact overlaps |
| Functions | normalize_text, token_ngrams, token_set, jaccard, extract_case_texts, check_leakage, write_markdown_report |
| Checks | L0 (dup case_id), L1 (exact unit/memory), L2 (normalized), L3 (n-gram + token fallback), L3b (scenario collision), L5 (candidate-internal repeats) |
| Hard blockers | duplicate case_id, exact unit overlap, exact memory overlap → exit nonzero |
| Warnings | near-duplicate (review/warn), normalized overlap, scenario collision, candidate-internal repeats |
| CLI | `python3 -m src.v05.check_leakage --train ... --candidate ... --out ...` |
| Ready for dev | ✅ |

## Files Changed (P5.12-D)

### Created
- `src/v05/cleanup_gold_metadata.py` — Metadata cleanup script
- `reports/v05/v05_gold_final_metadata_cleanup_report.md` — Cleanup summary
- `reports/v05/v05_gold_final_prelock_validation_report.md` — Prelock validation
- `reports/v05/v05_gold_final_prelock_hash_manifest.md` — Prelock SHA-256 hashes

### Updated
- `data/v05/gold/v05_gold_corrected_cases.jsonl` — 24 notes and 10 u2 texts fixed
- `data/v05/gold/v05_gold_core_corrected_cases.jsonl` — Regenerated from combined
- `data/v05/gold/v05_gold_corrected_sft_messages.jsonl` — Regenerated
- `reports/v05/v05_gold_opus_review_fixes_report.md` — Typo fix (hard_0014)
- `reports/v05/v05_gold_corrected_review_readiness_report.md` — Added D2 section
- `reports/v05/v05_gold_corrected_semantic_audit.md` — Added metadata cleanup section
- `reports/v05/v05_gold_corrected_train_leakage_report.md` — Rerun after text changes
- `reports/v05/v05_gold_corrected_dev_leakage_report.md` — Rerun after text changes
- `docs/status/CURRENT_STATE.md` — this file

### Unchanged
- `data/v05/gold/v05_gold_hard_corrected_cases.jsonl` — No hard cases modified by cleanup
- All train-pool, dev, v0.4 files

## Files Changed (P5.12-C)

### Created
- `src/v05/apply_gold_review_fixes.py` — Opus review fix application script
- `data/v05/gold/v05_gold_corrected_cases.jsonl` — 100 corrected gold cases
- `data/v05/gold/v05_gold_core_corrected_cases.jsonl` — 70 corrected gold_core cases
- `data/v05/gold/v05_gold_hard_corrected_cases.jsonl` — 30 corrected gold_hard cases
- `data/v05/gold/v05_gold_corrected_sft_messages.jsonl` — 100 corrected SFT messages
- `reports/v05/v05_gold_opus_review_fixes_report.md` — Fixes applied report
- `reports/v05/v05_gold_corrected_data_report.md` — Corrected data distribution
- `reports/v05/v05_gold_corrected_semantic_audit.md` — Corrected semantic audit
- `reports/v05/v05_gold_corrected_sft_validation_report.md` — SFT validation
- `reports/v05/v05_gold_corrected_review_readiness_report.md` — Readiness assessment
- `reports/v05/v05_gold_corrected_hash_manifest.md` — SHA-256 manifest
- `reports/v05/v05_gold_corrected_train_leakage_report.md` — Train↔corrected gold leakage
- `reports/v05/v05_gold_corrected_dev_leakage_report.md` — Dev↔corrected gold leakage

### Updated
- `docs/status/CURRENT_STATE.md` — this file
- `data/v05/gold/v05_gold_corrected_sft_messages.jsonl` — Metadata corrected post-generation

### Modified Cases (from gold draft)
- v05_gold_core_0021 u1: user_profile → service_memory
- v05_gold_core_0044 u2: project_memory → service_memory
- v05_gold_core_0047 u2: project_memory → service_memory
- v05_gold_core_0050 u2: project_memory → service_memory
- v05_gold_core_0051 u2: project_memory → service_memory
- v05_gold_core_0056 u2: project_memory → service_memory
- v05_gold_core_0057 u2: project_memory → service_memory
- v05_gold_core_0058 u2: project_memory → service_memory
- v05_gold_core_0062 u2: project_memory → service_memory (borderline)
- v05_gold_core_0066 u2: project_memory → service_memory
- v05_gold_core_0069 u2: project_memory → service_memory (borderline)
- v05_gold_hard_0013: entirely replaced (too easy → genuine boundary)
- v05_gold_hard_0014 u2: repo_memory → SKIP
- v05_gold_hard_0015 u3: phone +1-555-0198 → +1-555-0147

### Preserved (unchanged)
- All original gold draft files (`*_draft_*.jsonl`)
- All `data/v05/batches/*` files
- All `data/v05/dev/*` files
- All `data/v04/*` files
- All `src/v04/*` files
- `src/v05/check_leakage.py`
- `src/v05/render_sft_messages.py`

### Created
- `src/v05/check_leakage.py` — offline leakage checker (350 lines)
- `tests/v05/__init__.py` — test package init
- `tests/v05/test_check_leakage.py` — 28 unit tests (330 lines)
- `reports/v05/v05_methodology_inline_patch_report.md` — patch summary
- `reports/v05/v05_leakage_checker_smoke_report.md` — self-check report

### Updated
- `docs/v05/V05_DEV_GOLD_PLAN.md` — patches 1, 2 (dev/gold construction method)
- `docs/v05/V05_EVAL_PROTOCOL.md` — patches 3, 4 (exact_match demotion, teacher ceiling)
- `docs/v05/V05_BASELINE_EVAL_PLAN.md` — patches 4b, 5, 6 (teacher, qwen_few_shot_json, shuffled)
- `docs/v05/V05_STATISTICAL_REPORTING_PLAN.md` — patch 7 (paired bootstrap, nested subsets)
- `docs/v05/V05_LEAKAGE_AND_NEAR_DUP_PLAN.md` — patch 8 (token fallback, scenario collision)
- `docs/v05/V05_GOLD_REVIEW_GUIDE.md` — patch 9 (honest wording, no IAA blocker)
- `docs/v05/V05_LABEL_PROVENANCE_AND_DISTILLATION.md` — patch 9 (no IAA blocker)
- `reports/v05/v05_dev_gold_planning_report.md` — patch 10 (open questions resolved)
- `docs/status/CURRENT_STATE.md` — this file

### Preserved (unchanged)
- All `data/v05/batches/*` files
- All `data/v04/*` files
- All `src/v04/*` files
- `src/v05/render_sft_messages.py`
- All `src/v05/validate_*.py`, `render_*.py`, `gather_*.py`, `repair_*.py`
- All existing tests in `tests/v04/`

## Tests / Commands Run

```bash
# Compile check
python3 -m py_compile src/v05/check_leakage.py  # OK

# Full test suite
python3 -m unittest discover -s tests  # 77/77 OK (49 v04 + 28 v05)

# Leakage checker CLI
python3 -m src.v05.check_leakage \
  --train data/v05/batches/v05_batch500_corrected_cases.jsonl \
  --candidate data/v05/batches/v05_batch500_corrected_cases.jsonl \
  --out reports/v05/v05_leakage_checker_smoke_report.md
# Train: 500 | Candidate: 500 | Hard blockers: 2385 (expected, self-check) | Warnings: 2415

# wc -l on updated docs
# See methodology patch report for exact counts
```

## Open Issues

- Gold is LOCKED — immutable for final evaluation
- No training conducted
- Cross-batch duplicate in train-pool not yet addressed
- project_memory at 7.1% (under 10-16% target, honest tradeoff)
- user_profile at 4.3% (under 5-10% target, honest tradeoff)
- Qwen3/Qwen3.5 baseline comparison not yet run
- LoRA training not yet conducted

## Risks / Scope Drift Watch

- Do not modify locked gold
- Do not train until baselines established
- Watch for target distribution drift in gold (proj 7.1%, user 4.3% — honest)
- Do not add new domains, targets, types, or subtypes
- Do not modify v0.4 data
- Do not modify corrected batch500
- Do not modify dev
- Do not use gold for model selection or prompt tuning
- Do not create more methodology docs unless a blocker appears
- Do not open gold during training or development
- Gold is evaluation-only — dev is for all development decisions

## Dev Acceptance Status (P5.11-B)

| Criterion | Status |
|-----------|:------:|
| Dev accepted for model-selection use | ✅ |
| render_dev.py reproduces canonical | ✅ (frozen-data writer) |
| Medium-risk cases reviewed | ✅ (2 cases, both accepted) |
| Leakage warning reviewed | ✅ (natural domain overlap) |
| Hash manifest created | ✅ |
| All validations pass | ✅ |

## Gold Lock Status (P5.12-E)

| Property | Value |
|----------|-------|
| Lock status | ✅ LOCKED |
| Lock version | v05_gold_001 |
| Lock file | `data/v05/gold/v05_gold_lock.json` |
| Cases | 100 (70 core + 30 hard) |
| Combined SHA-256 | `56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d` |
| Core SHA-256 | `9acdd6a795b0a18d5c369253be8bb64e26a9af96e2aea31b4ef6c98adb598db2` |
| Hard SHA-256 | `5f4a5d552f76033c6a9a5443581a2dc2dc7ea0eeabdf99481fc1ec2c49f819b2` |
| SFT SHA-256 | `d9f215af282d6c90b65612c575d9a5827520a953d47f807e586b79ec94635c22` |
| Adjudicator | project-owner |
| Second reviewer | none (single-human research with LLM advisory) |
| Train↔gold leakage | 0 hard blockers, 0 warnings |
| Dev↔gold leakage | 0 hard blockers, 0 warnings |
| Sensitive STORE | 0 |
| Usage | Final evaluation only |

## Files Changed (P5.12-E)

### Created
- `data/v05/gold/v05_gold_lock.json` — Gold lock manifest
- `reports/v05/v05_gold_lock_report.md` — Lock report
- `reports/v05/v05_gold_locked_eval_usage.md` — Eval usage guide

### Updated
- `docs/status/CURRENT_STATE.md` — this file

### Unmodified (locked, must not change)
- `data/v05/gold/v05_gold_corrected_cases.jsonl`
- `data/v05/gold/v05_gold_core_corrected_cases.jsonl`
- `data/v05/gold/v05_gold_hard_corrected_cases.jsonl`
- `data/v05/gold/v05_gold_corrected_sft_messages.jsonl`

## Files Changed (P5.13-A)

### Created
-  — Full model comparison plan
-  — Baseline run configuration
-  — Qwen3.5 acquisition plan
-  — LoRA training experiment plan
-  — Environment readiness
-  — Gold usage verification
-  — Qwen3.5 status

### Updated
-  — this file

## Recommended Next Step

**User action required:**
1. **Manual review:** Review the v0.5b final reports and claims.
2. **Manual git snapshot:** Stage and commit v0.5b files, tag `v0.5b-unit-json-lora-complete`.
   - See `reports/v05b/v05b_git_handoff_checklist.md` for exact commands.
3. **Future: v0.5c safety-focused training**
   - See `reports/v05b/v05b_v05c_safety_ablation_plan.md`.
   - Train only after v0.5b is committed/tagged.

Do NOT train v0.5c from this context. This context is consolidation only.

## Files Changed (P5.12-D)

| Property | Value |
|----------|-------|
| Cases | 100 |
| READ-only | 18 (18%) |
| STORE/SKIP-only | 39 (39%) |
| READ+STORE joint | 43 (43%) |
| service_memory STORE | 71 (32.3%) |
| task_state STORE | 74 (33.6%) |
| repo_memory STORE | 37 (16.8%) |
| project_memory STORE | 26 (11.8%) |
| user_profile STORE | 12 (5.5%) |
| Coverage (12/12) | All met |
| Leakage hard blockers | 0 |
| Leakage warnings | 1 (natural domain overlap, score 0.500, accepted) |
| Sensitive STORE | 0 |
| Validation errors | 0 |
| Unittests | 77/77 OK |
| Acceptance | Accepted for model-selection use |

## Files Changed (P5.11-A + P5.11-B)

### Created (P5.11-A)
- `src/v05/render_dev.py` — Dev case generation script (rewritten in P5.11-B)
- `data/v05/dev/v05_dev_cases.jsonl` — 100 independent dev cases
- `data/v05/dev/v05_dev_sft_messages.jsonl` — 100 dev SFT messages
- `reports/v05/v05_dev_construction_report.md` — Construction summary
- `reports/v05/v05_dev_data_report.md` — Data distribution and examples
- `reports/v05/v05_dev_leakage_report.md` — Leakage check results
- `reports/v05/v05_dev_semantic_audit.md` — Per-case semantic audit
- `reports/v05/v05_dev_sft_validation_report.md` — SFT validation results

### Created (P5.11-B)
- `reports/v05/v05_dev_acceptance_report.md` — Dev acceptance report
- `reports/v05/v05_dev_medium_risk_review.md` — Medium-risk case review
- `reports/v05/v05_dev_reproducibility_report.md` — Reproducibility cleanup report
- `reports/v05/v05_dev_hash_manifest.md` — SHA-256 hash manifest

### Updated (P5.11-B)
- `src/v05/render_dev.py` — Rewritten as frozen-data writer
- `data/v05/dev/v05_dev_cases.jsonl` — Updated 5 case notes to match targets
- `data/v05/dev/v05_dev_sft_messages.jsonl` — Regenerated after note updates
- `docs/status/CURRENT_STATE.md` — this file

### Preserved (unchanged)
- All `data/v05/batches/*` files (corrected batch500)
- All `data/v04/*` files
- All `src/v04/*` files
- `src/v05/check_leakage.py`
- `src/v05/render_sft_messages.py`
- All tests in `tests/`
