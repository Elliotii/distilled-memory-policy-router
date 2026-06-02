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

- Cases: 500
- Candidate memories: 700
- Current units: 1185
- Gold READ IDs: 561
- Gold STORE units: 1042
- Gold SKIP units: 143
- Source: `data/v05/train/subsets/v05_train_500_cases.jsonl`
- Predictions: `data/v05/model_predictions/qwen3_4b_lora_500_train500_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 213 |
| `READ-only` | 105 |
| `STORE/SKIP-only` | 182 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 122 |
| `repo_memory` | 201 |
| `service_memory` | 323 |
| `task_state` | 338 |
| `user_profile` | 58 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `project_vs_repo` | 127 |
| `read_only` | 105 |
| `read_store_joint` | 213 |
| `related_but_useless` | 38 |
| `repo_convention` | 123 |
| `repo_memory` | 1 |
| `repo_vs_service` | 53 |
| `sensitive_boundary` | 30 |
| `service_invariant` | 236 |
| `service_memory` | 1 |
| `service_vs_task_state` | 69 |
| `sop_skill_out_of_scope` | 3 |
| `stale_memory` | 72 |
| `store_skip_only` | 182 |
| `target_boundary` | 100 |
| `task_progress` | 250 |
| `task_state` | 1 |
| `temporary_request` | 106 |
| `user_profile_boundary` | 51 |

## Systems

- `qwen3_4b_lora_500_train500` from `data/v05/model_predictions/qwen3_4b_lora_500_train500_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_500_train500 | 99.4% | 0.0% | 0.0% | 0.0% | 0.0% | 67.23 | 1.968 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_500_train500 | 34.0% | 0.941 | 0.977 | 56.7% | 0.827 | 3.4% | 8.7% | 88.9% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
