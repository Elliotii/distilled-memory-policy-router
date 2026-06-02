# V0.5 Final Artifact Manifest

**Date:** 2026-06-02  

---

## Data

| File | Cases |
|------|:-----:|
| `data/v05/batches/v05_batch500_corrected_cases.jsonl` | 500 |
| `data/v05/train/v05_train_pool_500_cases.jsonl` | 500 |
| `data/v05/train/subsets/v05_train_{125,250,500}_cases.jsonl` | 125/250/500 |
| `data/v05/train/subsets/v05_train_{125,250,500}_sft_messages.jsonl` | SFT |
| `data/v05/dev/v05_dev_cases.jsonl` | 100 |
| `data/v05/dev/v05_dev_sft_messages.jsonl` | 100 |
| `data/v05/gold/v05_gold_corrected_cases.jsonl` | 100 |
| `data/v05/gold/v05_gold_corrected_sft_messages.jsonl` | 100 |
| `data/v05/gold/v05_gold_lock.json` | Lock manifest |

## Prompts

| File |
|------|
| `prompts/v05/unit_dsl_zero_shot.txt` |
| `prompts/v05/unit_dsl_fewshot.txt` |
| `prompts/v05/unit_json_zero_shot.txt` |
| `prompts/v05/unit_json_fewshot.txt` |
| `prompts/v05/README.md` |

## Predictions

| File | Rows |
|------|:----:|
| `data/v05/model_predictions/qwen3_4b_v05_dev_predictions.jsonl` | 400 |
| `data/v05/model_predictions/qwen35_4b_v05_dev_predictions.jsonl` | 400 |
| `data/v05/model_predictions/qwen3_4b_v05_gold_selected_predictions.jsonl` | 400 |
| `data/v05/model_predictions/qwen35_4b_v05_gold_selected_predictions.jsonl` | 400 |
| `data/v05/model_predictions/qwen3_4b_lora_125_dev_predictions.jsonl` | 100 |
| `data/v05/model_predictions/qwen3_4b_lora_250_dev_predictions.jsonl` | 100 |
| `data/v05/model_predictions/qwen3_4b_lora_500_dev_predictions.jsonl` | 100 |
| `data/v05/model_predictions/qwen3_4b_lora_500_gold_predictions.jsonl` | 100 |

## Training Outputs

| Path |
|------|
| `results/v05_lora/qwen3_4b_dsl_125/adapter/` |
| `results/v05_lora/qwen3_4b_dsl_250/adapter/` |
| `results/v05_lora/qwen3_4b_dsl_500/adapter/` |

## Configs

| File |
|------|
| `configs/v05/qwen3_4b_lora_dsl_125.yaml` |
| `configs/v05/qwen3_4b_lora_dsl_250.yaml` |
| `configs/v05/qwen3_4b_lora_dsl_500.yaml` |

## Scripts

| File |
|------|
| `src/v05/train_lora_router.py` |
| `src/v05/eval_lora_router.py` |
| `src/v05/qwen_v05_output_runner.py` |
| `src/v05/render_sft_messages.py` |
| `src/v05/check_leakage.py` |
| `src/v04/eval_runner.py` |
| `src/v04/metrics.py` |
| `src/v04/parser.py` |
| `src/v04/case_validator.py` |

## Key Reports

| File |
|------|
| `reports/v05/v05_final_project_report.md` |
| `reports/v05/v05_final_experiment_summary.md` |
| `reports/v05/v05_final_lora_vs_prompting_report.md` |
| `reports/v05/v05_final_error_analysis.md` |
| `reports/v05/v05_final_claims_and_limitations.md` |
| `reports/v05/v05_final_resume_interview_narrative.md` |
| `reports/v05/v05_final_artifact_manifest.md` |
| `reports/v05/v05_v05b_ablation_plan.md` |
| `reports/v05/v05_gold_lock_report.md` |
| `reports/v05/v05_gold_baseline_summary_for_lora.md` |

---

*End of V0.5 Final Artifact Manifest.*
