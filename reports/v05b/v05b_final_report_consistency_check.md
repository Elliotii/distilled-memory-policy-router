# V0.5b Final Report Consistency Check

**Date:** 2026-06-02  

---

## 1. File Existence

| Report | Status |
|--------|:------:|
| `v05b_final_project_report.md` | ✅ |
| `v05b_final_experiment_summary.md` | ✅ |
| `v05b_final_claims_and_limitations.md` | ✅ |
| `v05b_final_error_analysis.md` | ✅ |
| `v05b_final_artifact_manifest.md` | ✅ |
| `v05b_v05c_safety_ablation_plan.md` | ✅ |
| `v05b_git_handoff_checklist.md` | ✅ |
| `v05b_final_report_consistency_check.md` | ✅ (this file) |
| `v05b_unit_json_lora_ablation_summary.md` | ✅ |
| `v05b_unit_json_lora_final_result_decision.md` | ✅ |
| Gold eval reports (5 files) | ✅ |
| Dev per-size reports (12 files) | ✅ |
| Planning reports (4 files) | ✅ |

**All 34 v0.5b reports present.**

## 2. Gold Hash

| Check | Value |
|-------|-------|
| Expected | `56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d` |
| Current | `56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d` |
| Match | ✅ |

## 3. Final Gold Metrics Consistency

All reports reporting the same JSON LoRA 500 gold metrics:

| Metric | Value | Consistent? |
|--------|:-----:|:-----------:|
| Parse | 100% | ✅ All reports |
| Exact | 31% | ✅ All reports |
| READ F1 | 0.919 | ✅ All reports |
| STORE F1 | 0.941 | ✅ All reports |
| Target acc | 67.3% | ✅ All reports |
| SKIP F1 | 0.706 | ✅ All reports |
| Sensitive | 6 failures | ✅ All reports |

## 4. Dev vs Gold Split Labels

All reports clearly distinguish:
- Dev: 100 cases for model selection
- Gold: 100 cases for final evaluation
- Dev→gold gaps explicitly labeled as cross-split comparisons
- No report claims dev and gold are same split

✅ All clear.

## 5. Production Safety Claims

Checked all v0.5b reports for forbidden claims:
- "production-safe": **0 occurrences** ✅
- "production ready": **0 occurrences** ✅
- "safety solved": **0 occurrences** ✅

## 6. JSON Beats Qwen3.5 Claims

- "JSON beats Qwen3.5": **0 occurrences** ✅
- All reports correctly note JSON 500 ranks #3 behind Qwen3.5 systems.
- Where "beats" is used, it refers to JSON vs DSL or JSON vs Qwen3-4B prompting.

## 7. Sensitive Failures

- **Treated as real failures, not soft failures.** ✅
- **6 failures catalogued individually** with case IDs and types. ✅
- **Credit card explicitly flagged as critical.** ✅

## 8. v0.5c Status

- **Described as future work only.** ✅
- **No training commands given.** ✅
- **No data generated for v0.5c.** ✅

## 9. Data and Prediction Integrity

| Check | Status |
|-------|:------:|
| v0.5 train/dev/gold cases unchanged | ✅ |
| Locked gold hash unchanged | ✅ |
| JSON SFT labels unchanged | ✅ |
| Predictions not modified after generation | ✅ |

## 10. Overall Verdict

**All consistency checks pass.** V0.5b reports are internally consistent, gold-protected, and ready for snapshot.

---

*End of V0.5b Final Report Consistency Check.*
