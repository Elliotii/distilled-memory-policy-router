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

- Cases: 125
- Candidate memories: 178
- Current units: 292
- Gold READ IDs: 141
- Gold STORE units: 254
- Gold SKIP units: 38
- Source: `data/v05/train/subsets/v05_train_125_cases.jsonl`
- Predictions: `data/v05/model_predictions/qwen3_4b_lora_125_train125_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 52 |
| `READ-only` | 28 |
| `STORE/SKIP-only` | 45 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 31 |
| `repo_memory` | 49 |
| `service_memory` | 77 |
| `task_state` | 82 |
| `user_profile` | 15 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `project_vs_repo` | 35 |
| `read_only` | 28 |
| `read_store_joint` | 52 |
| `related_but_useless` | 9 |
| `repo_convention` | 32 |
| `repo_vs_service` | 10 |
| `sensitive_boundary` | 7 |
| `service_invariant` | 60 |
| `service_vs_task_state` | 19 |
| `sop_skill_out_of_scope` | 2 |
| `stale_memory` | 17 |
| `store_skip_only` | 45 |
| `target_boundary` | 24 |
| `task_progress` | 63 |
| `temporary_request` | 30 |
| `user_profile_boundary` | 14 |

## Systems

- `qwen3_4b_lora_125_train125_unit_dsl` from `data/v05/model_predictions/qwen3_4b_lora_125_train125_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_125_train125_unit_dsl | 69.6% | 0.0% | 12.1% | 0.0% | 0.0% | 64.376 | 2.216 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_125_train125_unit_dsl | 13.6% | 0.773 | 0.753 | 60.2% | 0.136 | 11.2% | 11.8% | 33.3% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
