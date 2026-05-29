# Day 7 Input Freeze

Date: 2026-05-29

Day 7 starts from these frozen inputs. Do not train from draft folders,
review-intermediate files, or unrepaired V4 Flash outputs.

## Canonical Data Files

| split | path | rows | category balance | sha256 |
| --- | --- | ---: | --- | --- |
| train | `data/processed/synthetic_train_5000.jsonl` | 5000 | 500 per category | `09a577abd19684372a12abf5322321a6b7f143c5fc68ddc1ad51f672cd0cd443` |
| dev | `data/dev/dev_250.jsonl` | 250 | 25 per category | `899e4325c5d5e83b09b41a41076414378c417e755b595f824fd1faf98d229ed5` |
| gold | `data/gold/gold_eval_300.jsonl` | 300 | 30 per category | `214504da9441bcad7cfeaa862021b21be0d28629efc47c342d6d43e498a24f53` |

Gold training/evaluation should use `data/gold/gold_eval_300.jsonl`, not
`gold_eval_300.review.jsonl` or `gold_eval_300.review.before_opus_repair.jsonl`.

## Frozen Evaluation Assets

| asset | path | sha256 |
| --- | --- | --- |
| normalizer markers | `src/evaluation/normalizer_markers.txt` | `3e7dc84001b5270cc31d31659fa084855020b5d86232d810a252dddb9b38c70c` |
| evaluator | `src/evaluation/evaluate_predictions.py` | tracked in repo |
| prediction validator | `src/evaluation/validate_predictions.py` | tracked in repo |

The normalizer marker list is frozen before student evaluation. Do not edit it
after seeing student results.

## V4 Flash Router Baseline

Use only the repaired V4 Flash prediction files for Day 7 comparisons.

| split | predictions | sha256 | metrics |
| --- | --- | --- | --- |
| dev | `results/eval/predictions/dev_deepseek_v4flash_router_repaired.predictions.jsonl` | `0310fdb4d924f6827ed274ecab945022c6dc4a18d78383bbcb477b3164156fdd` | `results/eval/reports/dev_deepseek_v4flash_router_repaired.metrics.json` |
| gold | `results/eval/predictions/gold_deepseek_v4flash_router_repaired.predictions.jsonl` | `81e6b0ec65c333b90bef745986b48f0ca3736ef8110fd9488bd33ebc062c2510` | `results/eval/reports/gold_deepseek_v4flash_router_repaired.metrics.json` |

Final normalized V4 Flash router metrics:

| split | read F1 | write F1 | typed write F1 | ignore F1 | exact match |
| --- | ---: | ---: | ---: | ---: | ---: |
| dev | 0.779 | 0.824 | 0.734 | 0.662 | 0.540 |
| gold | 0.961 | 0.869 | 0.718 | 0.931 | 0.737 |

## Validation Completed

Commands were run with bundled Python:

```text
/Users/elliot/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
```

Checks completed:

- `validate_cases` passed for train with `--min-per-category 500`.
- `validate_cases` passed for dev with `--min-per-category 25`.
- `validate_cases` passed for gold with `--min-per-category 30`.
- `validate_predictions` passed for repaired dev V4 Flash predictions.
- `validate_predictions` passed for repaired gold V4 Flash predictions.
- V4 Flash metric JSON values match the Day 6 summary.

## Day 7 Next Inputs

Day 7-2 should create instruction-format training/evaluation files from the
frozen train/dev/gold files above. The student target remains only:

```json
{
  "read_hints": [],
  "write_spans": [],
  "ignore_spans": []
}
```

The selected student should be evaluated as:

- `student-zero-shot` before fine-tuning;
- `student-finetuned` after LoRA/QLoRA;
- both reported with the same raw and normalized evaluator used for V4 Flash.

## Day 7-2 Student Instruction Files

Created by:

```text
/Users/elliot/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m src.training.prepare_student_data
```

Output directory:

```text
results/day7_student_data/
```

| file | rows | purpose |
| --- | ---: | --- |
| `results/day7_student_data/train_sft_messages.jsonl` | 5000 | SFT/QLoRA training data; messages contain system, user, assistant |
| `results/day7_student_data/dev_prompt_messages.jsonl` | 250 | zero-shot and fine-tuned dev inference prompts; target retained for scoring |
| `results/day7_student_data/gold_prompt_messages.jsonl` | 300 | final offline gold inference prompts; target retained for scoring |
| `results/day7_student_data/dev_smoke_20_prompt_messages.jsonl` | 20 | first desktop/GPU smoke run; 2 cases per category |
| `results/day7_student_data/manifest.json` | 1 | source paths, output paths, counts, and category counts |

The SFT file uses this shape:

```text
messages = [system, user, assistant]
assistant.content = compact JSON router target only
```

The prompt files use this shape:

```text
messages = [system, user]
target = retained locally for validation/scoring only
```

Format validation passed for all four JSONL outputs.
