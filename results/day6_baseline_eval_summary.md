# Day 6 Baseline Evaluation Summary

This run establishes the offline intrinsic baselines for the MVP router task
under the v0.3 spec. Metrics are reported in both raw exact form and normalized
span-overlap form using the frozen marker list in
`src/evaluation/normalizer_markers.txt`.

## Files

- Deterministic baseline generator: `src/evaluation/baselines.py`
- LLM prediction harness: `src/evaluation/llm_predict.py`
- Evaluator: `src/evaluation/evaluate_predictions.py`
- Span normalizer: `src/evaluation/span_normalizer.py`
- Frozen markers: `src/evaluation/normalizer_markers.txt`
- Prediction files: `results/eval/predictions/`
- Run logs: `results/eval/runlogs/`
- Metric reports: `results/eval/reports/`

## Baselines Completed

- `empty`: predicts no reads, writes, or ignores.
- `all-read`: selects every candidate memory as a read hint and predicts no
  writes or ignores.
- `rule-based`: deterministic lexical heuristics.
- `deepseek-v4-flash-router`: DeepSeek V4 Flash predicts router targets from
  the same router prompt. This is a strong LLM router baseline, not the source
  teacher.

## Raw Results

| split | baseline | read F1 | write F1 | typed write F1 | ignore F1 | exact match |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| dev | empty | 0.000 | 0.000 | 0.000 | 0.000 | 0.100 |
| dev | all-read | 0.489 | 0.000 | 0.000 | 0.000 | 0.072 |
| dev | rule-based | 0.796 | 0.107 | 0.100 | 0.569 | 0.240 |
| dev | V4 Flash router | 0.779 | 0.473 | 0.426 | 0.602 | 0.396 |
| gold | empty | 0.000 | 0.000 | 0.000 | 0.000 | 0.100 |
| gold | all-read | 0.596 | 0.000 | 0.000 | 0.000 | 0.020 |
| gold | rule-based | 0.885 | 0.145 | 0.101 | 0.963 | 0.307 |
| gold | V4 Flash router | 0.961 | 0.523 | 0.443 | 0.861 | 0.553 |

## Normalized Results

| split | baseline | read F1 | write F1 | typed write F1 | ignore F1 | exact match |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| dev | empty | 0.000 | 0.000 | 0.000 | 0.000 | 0.100 |
| dev | all-read | 0.489 | 0.000 | 0.000 | 0.000 | 0.072 |
| dev | rule-based | 0.796 | 0.294 | 0.274 | 0.586 | 0.300 |
| dev | V4 Flash router | 0.779 | 0.824 | 0.734 | 0.662 | 0.540 |
| gold | empty | 0.000 | 0.000 | 0.000 | 0.000 | 0.100 |
| gold | all-read | 0.596 | 0.000 | 0.000 | 0.000 | 0.020 |
| gold | rule-based | 0.885 | 0.377 | 0.327 | 0.978 | 0.393 |
| gold | V4 Flash router | 0.961 | 0.869 | 0.718 | 0.931 | 0.737 |

## V4 Flash Cost and Reliability

| split | rows | parse errors after repair | total tokens | reasoning tokens | avg latency ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| dev | 250 | 0 | 463,714 | 246,576 | 13,330.2 |
| gold | 300 | 0 | 519,083 | 260,748 | 13,679.5 |

Notes:

- V4 Flash appears to run with reasoning enabled; the run logs include large
  `reasoning_tokens` counts.
- Low `max_tokens` caused empty outputs because reasoning consumed the output
  budget. The final clean runs use repaired rows from higher-budget retries.
- The final V4 Flash router prediction files are:
  - `results/eval/predictions/dev_deepseek_v4flash_router_repaired.predictions.jsonl`
  - `results/eval/predictions/gold_deepseek_v4flash_router_repaired.predictions.jsonl`

## Interpretation

V4 Flash is a strong router baseline, especially on normalized write spans. It
beats deterministic rules on write extraction by a large margin, while
rule-based remains competitive on explicit ignore spans. This sets the Day 7
target for the small router: approach V4 Flash routing quality while being much
cheaper and faster.
