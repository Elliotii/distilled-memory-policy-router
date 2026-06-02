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

- Cases: 5
- Candidate memories: 5
- Current units: 13
- Gold READ IDs: 3
- Gold STORE units: 10
- Gold SKIP units: 3
- Source: `data/v05/model_predictions/v05_smoke_dev_cases.jsonl`
- Predictions: `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 1 |
| `READ-only` | 1 |
| `STORE/SKIP-only` | 3 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 2 |
| `repo_memory` | 1 |
| `service_memory` | 3 |
| `task_state` | 4 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `project_memory_vs_task_state` | 1 |
| `project_vs_repo` | 1 |
| `read_only` | 1 |
| `read_selectivity` | 1 |
| `read_store_joint` | 1 |
| `repo_convention` | 1 |
| `sensitive_boundary` | 1 |
| `service_invariant` | 3 |
| `service_vs_task_state` | 1 |
| `stale_memory` | 1 |
| `store_skip_only` | 3 |
| `target_boundary` | 1 |
| `task_progress` | 2 |
| `temporary_request` | 1 |

## Systems

- `qwen3-4b_unit_dsl_fewshot` from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`.
- `qwen3-4b_unit_dsl_zero_shot` from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`.
- `qwen3-4b_unit_json_fewshot` from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`.
- `qwen3-4b_unit_json_zero_shot` from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`.
- `qwen3.5_unit_dsl_fewshot` from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`.
- `qwen3.5_unit_dsl_zero_shot` from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`.
- `qwen3.5_unit_json_fewshot` from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`.
- `qwen3.5_unit_json_zero_shot` from `data/v05/model_predictions/qwen_v05_smoke_retry_merged_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3-4b_unit_dsl_fewshot | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 63.6 | 2.4 |
| unit_dsl | qwen3-4b_unit_dsl_zero_shot | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 68.4 | 3.0 |
| unit_dsl | qwen3.5_unit_dsl_fewshot | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 60.6 | 1.8 |
| unit_dsl | qwen3.5_unit_dsl_zero_shot | 80.0% | 0.0% | 0.0% | 0.0% | 0.0% | 67.6 | 2.0 |
| unit_json | qwen3-4b_unit_json_fewshot | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 113.6 | 1.8 |
| unit_json | qwen3-4b_unit_json_zero_shot | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 150.6 | 2.4 |
| unit_json | qwen3.5_unit_json_fewshot | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 113.6 | 1.8 |
| unit_json | qwen3.5_unit_json_zero_shot | 80.0% | 37.5% | 0.0% | 0.0% | 0.0% | 150.6 | 2.8 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3-4b_unit_dsl_fewshot | 20.0% | 0.857 | 0.900 | 66.7% | 0.667 | 10.0% | 25.0% | 0.0% |
| unit_dsl | qwen3-4b_unit_dsl_zero_shot | 0.0% | 0.750 | 0.900 | 11.1% | 0.667 | 10.0% | 40.0% | 0.0% |
| unit_dsl | qwen3.5_unit_dsl_fewshot | 40.0% | 0.857 | 1.000 | 80.0% | 1.000 | 0.0% | 25.0% | 0.0% |
| unit_dsl | qwen3.5_unit_dsl_zero_shot | 20.0% | 0.667 | 0.952 | 40.0% | 0.500 | 9.1% | 33.3% | 0.0% |
| unit_json | qwen3-4b_unit_json_fewshot | 40.0% | 0.750 | 0.947 | 77.8% | 0.857 | 0.0% | 40.0% | 0.0% |
| unit_json | qwen3-4b_unit_json_zero_shot | 20.0% | 0.750 | 0.909 | 40.0% | 0.500 | 16.7% | 40.0% | 0.0% |
| unit_json | qwen3.5_unit_json_fewshot | 40.0% | 0.750 | 0.947 | 77.8% | 0.857 | 0.0% | 40.0% | 0.0% |
| unit_json | qwen3.5_unit_json_zero_shot | 0.0% | 0.750 | 0.737 | 42.9% | 0.500 | 22.2% | 40.0% | 0.0% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
