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
- Candidate memories: 156
- Current units: 264
- Gold READ IDs: 114
- Gold STORE units: 220
- Gold SKIP units: 44
- Source: `data/v05/dev/v05_dev_cases.jsonl`
- Predictions: `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 43 |
| `READ-only` | 18 |
| `STORE/SKIP-only` | 39 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 26 |
| `repo_memory` | 37 |
| `service_memory` | 71 |
| `task_state` | 74 |
| `user_profile` | 12 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `project_memory_vs_task_state` | 1 |
| `project_vs_repo` | 28 |
| `read_only` | 18 |
| `read_selectivity` | 19 |
| `read_store_joint` | 43 |
| `related_but_useless` | 15 |
| `repo_convention` | 29 |
| `repo_vs_service` | 6 |
| `sensitive_boundary` | 10 |
| `service_invariant` | 67 |
| `service_vs_task_state` | 3 |
| `stale_memory` | 16 |
| `store_skip_only` | 39 |
| `target_boundary` | 1 |
| `task_progress` | 63 |
| `temporary_request` | 31 |
| `user_profile_boundary` | 9 |
| `user_profile_vs_sensitive_private` | 1 |

## Systems

- `qwen35_4b_unit_dsl_fewshot` from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`.
- `qwen35_4b_unit_dsl_zero_shot` from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`.
- `qwen35_4b_unit_json_fewshot` from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`.
- `qwen35_4b_unit_json_zero_shot` from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`.
- `qwen3_4b_unit_dsl_fewshot` from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`.
- `qwen3_4b_unit_dsl_zero_shot` from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`.
- `qwen3_4b_unit_json_fewshot` from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`.
- `qwen3_4b_unit_json_zero_shot` from `data/v05/model_predictions/qwen_v05_dev_merged_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen35_4b_unit_dsl_fewshot | 99.0% | 0.0% | 0.4% | 0.0% | 0.0% | 69.4 | 1.76 |
| unit_dsl | qwen35_4b_unit_dsl_zero_shot | 47.0% | 0.0% | 4.1% | 0.0% | 0.0% | 75.98 | 1.89 |
| unit_dsl | qwen3_4b_unit_dsl_fewshot | 96.0% | 0.0% | 0.0% | 0.0% | 0.0% | 68.28 | 2.29 |
| unit_dsl | qwen3_4b_unit_dsl_zero_shot | 43.0% | 82.0% | 0.0% | 0.0% | 0.0% | 71.68 | 2.27 |
| unit_json | qwen35_4b_unit_json_fewshot | 98.0% | 0.0% | 0.8% | 0.0% | 0.0% | 127.06 | 1.87 |
| unit_json | qwen35_4b_unit_json_zero_shot | 97.0% | 0.0% | 0.0% | 0.9% | 0.0% | 166.9 | 2.28 |
| unit_json | qwen3_4b_unit_json_fewshot | 99.0% | 0.0% | 0.0% | 0.0% | 0.0% | 126.97 | 2.3 |
| unit_json | qwen3_4b_unit_json_zero_shot | 97.0% | 0.0% | 2.6% | 0.0% | 0.0% | 185.29 | 2.43 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen35_4b_unit_dsl_fewshot | 41.0% | 0.912 | 0.975 | 74.8% | 0.864 | 2.3% | 12.8% | 33.3% |
| unit_dsl | qwen35_4b_unit_dsl_zero_shot | 3.0% | 0.271 | 0.682 | 42.5% | 0.204 | 9.1% | 5.3% | 0.0% |
| unit_dsl | qwen3_4b_unit_dsl_fewshot | 22.0% | 0.871 | 0.936 | 71.1% | 0.690 | 5.6% | 17.3% | 33.3% |
| unit_dsl | qwen3_4b_unit_dsl_zero_shot | 5.0% | 0.051 | 0.587 | 41.9% | 0.568 | 4.1% | 25.0% | 33.3% |
| unit_json | qwen35_4b_unit_json_fewshot | 37.0% | 0.891 | 0.965 | 73.9% | 0.903 | 1.0% | 14.5% | 33.3% |
| unit_json | qwen35_4b_unit_json_zero_shot | 23.0% | 0.840 | 0.941 | 71.0% | 0.787 | 2.4% | 25.7% | 33.3% |
| unit_json | qwen3_4b_unit_json_fewshot | 23.0% | 0.882 | 0.961 | 67.1% | 0.851 | 1.9% | 17.6% | 33.3% |
| unit_json | qwen3_4b_unit_json_zero_shot | 18.0% | 0.888 | 0.925 | 67.6% | 0.571 | 7.7% | 12.7% | 33.3% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
