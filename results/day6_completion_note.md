# Day 6 Completion Note

Date: 2026-05-29

Day 6 is complete. The project now has a v0.3 evaluation substrate and a clean
DeepSeek V4 Flash router baseline on both dev and gold.

## Scope Completed

- Archived the old v0.2 project spec and updated the canonical spec to v0.3.
- Clarified model roles:
  - DeepSeek V4 Pro/Max is the synthetic label source / source teacher.
  - DeepSeek V4 Flash is a router baseline, downstream self-routing baseline,
    and fixed downstream main agent. It is not the teacher.
  - The fine-tuned small router is the proposed memory-policy controller.
- Added the minimal downstream agent harness boundary to the spec.
- Implemented raw and normalized span scoring.
- Froze the normalization marker list and records its SHA256 in metrics files.
- Added cost/latency run logs for LLM prediction runs.
- Ran deterministic baselines on dev and gold.
- Ran and repaired DeepSeek V4 Flash router baselines on dev and gold.

## Final Baseline Files

Use these repaired prediction files for comparisons:

- Dev V4 Flash router predictions:
  `results/eval/predictions/dev_deepseek_v4flash_router_repaired.predictions.jsonl`
- Gold V4 Flash router predictions:
  `results/eval/predictions/gold_deepseek_v4flash_router_repaired.predictions.jsonl`

Use these metric files for reported scores:

- Dev V4 Flash router metrics:
  `results/eval/reports/dev_deepseek_v4flash_router_repaired.metrics.json`
- Gold V4 Flash router metrics:
  `results/eval/reports/gold_deepseek_v4flash_router_repaired.metrics.json`

Use these run logs for cost and latency:

- Dev V4 Flash router run log:
  `results/eval/runlogs/dev_deepseek_v4flash_router_repaired.runlog.jsonl`
- Gold V4 Flash router run log:
  `results/eval/runlogs/gold_deepseek_v4flash_router_repaired.runlog.jsonl`

Intermediate files without `_repaired` are retained for audit/debugging but
should not be used as the final baseline.

## Final V4 Flash Router Results

Raw metrics:

| split | read F1 | write F1 | typed write F1 | ignore F1 | exact match |
| --- | ---: | ---: | ---: | ---: | ---: |
| dev | 0.779 | 0.473 | 0.426 | 0.602 | 0.396 |
| gold | 0.961 | 0.523 | 0.443 | 0.861 | 0.553 |

Normalized metrics:

| split | read F1 | write F1 | typed write F1 | ignore F1 | exact match |
| --- | ---: | ---: | ---: | ---: | ---: |
| dev | 0.779 | 0.824 | 0.734 | 0.662 | 0.540 |
| gold | 0.961 | 0.869 | 0.718 | 0.931 | 0.737 |

Cost and reliability:

| split | rows | parse errors after repair | total tokens | reasoning tokens | avg latency ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| dev | 250 | 0 | 463,714 | 246,576 | 13,330.2 |
| gold | 300 | 0 | 519,083 | 260,748 | 13,679.5 |

## Day 7 Inputs

- Train data: `data/processed/synthetic_train_5000.jsonl`
- Dev data: `data/dev/dev_250.jsonl`
- Gold data: `data/gold/gold_eval_300.jsonl`
- Frozen normalizer markers: `src/evaluation/normalizer_markers.txt`
- Evaluator: `src/evaluation/evaluate_predictions.py`
- V4 Flash baseline: the repaired dev/gold prediction and metric files listed
  above.

## Day 7 Goal

Train and evaluate the selected 3B-4B student router. The student should beat
empty, all-read, rule-based, and zero-shot student baselines, and should aim to
approach the V4 Flash router baseline at much lower routing cost and latency.
