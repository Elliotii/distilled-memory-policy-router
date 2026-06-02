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

- Cases: 250
- Candidate memories: 352
- Current units: 599
- Gold READ IDs: 287
- Gold STORE units: 526
- Gold SKIP units: 73
- Source: `data/v05/train/subsets/v05_train_250_cases.jsonl`
- Predictions: `data/v05/model_predictions/qwen3_4b_lora_250_train250_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 106 |
| `READ-only` | 52 |
| `STORE/SKIP-only` | 92 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 65 |
| `repo_memory` | 108 |
| `service_memory` | 148 |
| `task_state` | 174 |
| `user_profile` | 31 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `project_vs_repo` | 70 |
| `read_only` | 52 |
| `read_store_joint` | 106 |
| `related_but_useless` | 19 |
| `repo_convention` | 68 |
| `repo_memory` | 1 |
| `repo_vs_service` | 25 |
| `sensitive_boundary` | 16 |
| `service_invariant` | 112 |
| `service_memory` | 1 |
| `service_vs_task_state` | 37 |
| `sop_skill_out_of_scope` | 3 |
| `stale_memory` | 31 |
| `store_skip_only` | 92 |
| `target_boundary` | 51 |
| `task_progress` | 124 |
| `task_state` | 1 |
| `temporary_request` | 54 |
| `user_profile_boundary` | 28 |

## Systems

- `qwen3_4b_lora_250_train250` from `data/v05/model_predictions/qwen3_4b_lora_250_train250_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_250_train250 | 98.4% | 0.0% | 0.0% | 0.2% | 0.0% | 67.268 | 2.328 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_250_train250 | 21.6% | 0.920 | 0.952 | 50.4% | 0.619 | 5.8% | 9.7% | 50.0% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
