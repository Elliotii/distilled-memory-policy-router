# V0.5c Final Artifact Manifest

**Date:** 2026-06-04  

---

## 1. Reports to Commit

### v0.5c Planning (Context 5.9-A)
| File |
|------|
| `reports/v05c/v05c_qwen35_json_lora_plan.md` |
| `reports/v05c/v05c_qwen35_model_feasibility_report.md` |
| `reports/v05c/v05c_qwen35_json_lora_config_report.md` |
| `reports/v05c/v05c_train_dev_gold_usage_policy.md` |
| `reports/v05c/v05c_qwen35_json_lora_readiness_report.md` |

### v0.5c 125 Smoke (Context 5.9-B)
| File |
|------|
| `reports/v05c/v05c_qwen35_lora_json_125_train_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_125_dev_eval_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_125_error_analysis.md` |
| `reports/v05c/v05c_qwen35_lora_json_125_vs_qwen3_4b_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_125_smoke_decision.md` |

### v0.5c 250 (Context 5.9-C)
| File |
|------|
| `reports/v05c/v05c_qwen35_lora_json_250_train_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_250_dev_eval_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_250_error_analysis.md` |
| `reports/v05c/v05c_qwen35_lora_json_250_vs_125_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_250_vs_qwen3_4b_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_250_decision.md` |

### v0.5c 500 Dev (Context 5.9-D)
| File |
|------|
| `reports/v05c/v05c_qwen35_lora_json_500_train_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_dev_eval_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_error_analysis.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_parse_regression_audit.md` |
| `reports/v05c/v05c_qwen35_lora_json_learning_curve_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_vs_qwen3_4b_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_target_confusion_audit.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_sensitive_store_audit.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_gold_readiness_decision.md` |

### v0.5c Gold + Final (Context 5.9-E + 5.10-A)
| File |
|------|
| `reports/v05c/v05c_qwen35_lora_json_500_gold_eval_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_gold_error_analysis.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_gold_baseline_comparison.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_gold_parse_audit.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_gold_target_confusion_audit.md` |
| `reports/v05c/v05c_qwen35_lora_json_500_gold_sensitive_store_audit.md` |
| `reports/v05c/v05c_qwen35_lora_json_dev_vs_gold_delta_report.md` |
| `reports/v05c/v05c_qwen35_lora_json_final_result_decision.md` |
| `reports/v05c/v05c_best_combo_selection_report.md` |
| `reports/v05c/v05c_final_project_report.md` |
| `reports/v05c/v05c_final_experiment_summary.md` |
| `reports/v05c/v05c_final_claims_and_limitations.md` |
| `reports/v05c/v05c_final_error_analysis.md` |
| `reports/v05c/v05c_final_artifact_manifest.md` |
| `reports/v05c/v05c_next_ablation_decision_memo.md` |
| `reports/v05c/v05c_git_handoff_checklist.md` |
| `reports/v05c/v05c_final_report_consistency_check.md` |

**Total: 42 reports**

## 2. Docs to Commit

| File |
|------|
| `docs/v05c/V05C_QWEN35_JSON_LORA_PLAN.md` |
| `docs/v05c/V05C_FINAL_RESULTS.md` |
| `docs/v05c/V05C_PROJECT_NARRATIVE.md` |
| `docs/v05c/V05C_NEXT_ABLATION_OPTIONS.md` |
| `docs/status/CURRENT_STATE.md` (updated) |

## 3. Configs to Commit

| File |
|------|
| `configs/v05c/qwen35_lora_json_125.yaml` |
| `configs/v05c/qwen35_lora_json_250.yaml` |
| `configs/v05c/qwen35_lora_json_500.yaml` |

## 4. Scripts Modified (Commit)

| File | Change |
|------|--------|
| `src/v05/train_lora_router.py` | +1 line: `processing_class=tokenizer` for Qwen3.5 multimodal bypass |
| `src/v05/eval_lora_router.py` | +8/−5 lines: `enable_thinking=False`, incremental write support |

## 5. Predictions (Commit if small)

| File | Rows | Size |
|------|:----:|------|
| `data/v05c/model_predictions/qwen35_lora_json_125_dev_predictions.jsonl` | 100 | ~30KB |
| `data/v05c/model_predictions/qwen35_lora_json_250_dev_predictions.jsonl` | 100 | ~30KB |
| `data/v05c/model_predictions/qwen35_lora_json_500_dev_predictions.jsonl` | 100 | ~30KB |
| `data/v05c/model_predictions/qwen35_lora_json_500_gold_predictions.jsonl` | 100 | ~30KB |

## 6. Training Outputs (DO NOT commit)

| Path | Size |
|------|------|
| `results/v05c_lora/qwen35_json_125/` | ~25MB |
| `results/v05c_lora/qwen35_json_250/` | ~25MB |
| `results/v05c_lora/qwen35_json_500/` | ~25MB |

## 7. Never Commit

- `results/v05c_lora/` — training outputs and checkpoints
- `.venv/`, `__pycache__/`, `.DS_Store`
- `checkpoints/`, `models/`, `outputs/`, `wandb/`
- `*.log`, `*.pyc`
- `.env`
