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
- Predictions: `data/v05/model_predictions/qwen3_4b_lora_500_gold_predictions.jsonl`

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

- `qwen3_4b_lora_500_unit_dsl` from `data/v05/model_predictions/qwen3_4b_lora_500_gold_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_500_unit_dsl | 99.0% | 0.0% | 0.0% | 0.0% | 0.0% | 66.86 | 2.5 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_dsl | qwen3_4b_lora_500_unit_dsl | 16.0% | 0.923 | 0.946 | 47.5% | 0.718 | 6.9% | 12.6% | 50.0% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
