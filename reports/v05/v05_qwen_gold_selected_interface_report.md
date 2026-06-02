# v0.4 A/B/C Interface Pilot Report

Date: 2026-06-02
Status: P5 external prediction evaluation

## Scope

This report evaluates an external prediction JSONL file that already contains raw outputs. The runner only loads and scores those rows; it does not call models, train, retrieve, write memories, or make v0.5 locked-gold claims.

Interfaces:

- A: Legacy Span JSON (`read_hints`, `write_spans`, `ignore_spans`).
- B: Unit JSON (`read`, `store`, `skip`).
- C: Unit DSL (`READ`, `STORE`, `SKIP`).

## Dataset

- Cases: 100
- Candidate memories: 131
- Current units: 254
- Gold READ IDs: 92
- Gold STORE units: 210
- Gold SKIP units: 44
- Source: `data/v05/gold/v05_gold_corrected_cases.jsonl`
- Predictions: `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 35 |
| `READ-only` | 23 |
| `STORE/SKIP-only` | 42 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 15 |
| `repo_memory` | 35 |
| `service_memory` | 80 |
| `task_state` | 71 |
| `user_profile` | 9 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `project_memory_vs_task_state` | 4 |
| `project_vs_repo` | 22 |
| `read_only` | 23 |
| `read_selectivity` | 15 |
| `read_store_joint` | 35 |
| `related_but_useless` | 16 |
| `repo_convention` | 23 |
| `repo_vs_service` | 4 |
| `sensitive_boundary` | 10 |
| `service_invariant` | 55 |
| `service_vs_task_state` | 6 |
| `stale_memory` | 8 |
| `store_skip_only` | 42 |
| `target_boundary` | 14 |
| `task_progress` | 48 |
| `temporary_request` | 30 |
| `user_profile_boundary` | 10 |
| `user_profile_vs_sensitive_private` | 3 |

## Systems

- `qwen35_4b_unit_dsl_fewshot` from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`.
- `qwen35_4b_unit_dsl_zero_shot` from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`.
- `qwen35_4b_unit_json_fewshot` from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`.
- `qwen35_4b_unit_json_zero_shot` from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`.
- `qwen3_4b_unit_dsl_fewshot` from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`.
- `qwen3_4b_unit_dsl_zero_shot` from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`.
- `qwen3_4b_unit_json_fewshot` from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`.
- `qwen3_4b_unit_json_zero_shot` from `data/v05/model_predictions/qwen_v05_gold_selected_merged_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen35_4b_unit_dsl_fewshot | 98.0% | 0.0% | 0.0% | 0.0% | 0.0% | 66.5 | 1.88 |
| unit_dsl | qwen35_4b_unit_dsl_zero_shot | 51.0% | 0.0% | 8.0% | 0.0% | 0.0% | 74.48 | 2.0 |
| unit_dsl | qwen3_4b_unit_dsl_fewshot | 89.0% | 0.0% | 2.7% | 0.0% | 0.0% | 62.63 | 2.62 |
| unit_dsl | qwen3_4b_unit_dsl_zero_shot | 50.0% | 69.0% | 0.0% | 0.0% | 0.0% | 69.75 | 2.48 |
| unit_json | qwen35_4b_unit_json_fewshot | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 119.3 | 1.74 |
| unit_json | qwen35_4b_unit_json_zero_shot | 97.0% | 0.0% | 0.0% | 0.0% | 0.0% | 162.6 | 1.83 |
| unit_json | qwen3_4b_unit_json_fewshot | 97.0% | 3.0% | 0.0% | 0.0% | 0.0% | 114.96 | 2.19 |
| unit_json | qwen3_4b_unit_json_zero_shot | 98.0% | 0.0% | 0.8% | 0.0% | 0.0% | 184.2 | 2.56 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen35_4b_unit_dsl_fewshot | 36.0% | 0.901 | 0.959 | 77.6% | 0.795 | 3.8% | 17.3% | 0.0% |
| unit_dsl | qwen35_4b_unit_dsl_zero_shot | 1.0% | 0.357 | 0.680 | 33.6% | 0.160 | 11.5% | 0.0% | 0.0% |
| unit_dsl | qwen3_4b_unit_dsl_fewshot | 7.0% | 0.882 | 0.850 | 60.5% | 0.422 | 8.7% | 12.8% | 0.0% |
| unit_dsl | qwen3_4b_unit_dsl_zero_shot | 0.0% | 0.196 | 0.685 | 39.3% | 0.451 | 4.3% | 0.0% | 0.0% |
| unit_json | qwen35_4b_unit_json_fewshot | 42.0% | 0.911 | 0.963 | 79.1% | 0.851 | 0.5% | 16.4% | 0.0% |
| unit_json | qwen35_4b_unit_json_zero_shot | 38.0% | 0.850 | 0.935 | 81.0% | 0.690 | 5.8% | 25.4% | 25.0% |
| unit_json | qwen3_4b_unit_json_fewshot | 26.0% | 0.936 | 0.923 | 57.5% | 0.766 | 0.5% | 8.3% | 0.0% |
| unit_json | qwen3_4b_unit_json_zero_shot | 14.0% | 0.920 | 0.914 | 63.8% | 0.494 | 10.5% | 9.5% | 0.0% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
