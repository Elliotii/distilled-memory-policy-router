# v0.4 A/B/C Interface Pilot Report

Date: 2026-06-01
Status: P5 external prediction evaluation

## Scope

This report evaluates an external prediction JSONL file that already contains raw outputs. The runner only loads and scores those rows; it does not call models, train, retrieve, write memories, or make v0.5 locked-gold claims.

Interfaces:

- A: Legacy Span JSON (`read_hints`, `write_spans`, `ignore_spans`).
- B: Unit JSON (`read`, `store`, `skip`).
- C: Unit DSL (`READ`, `STORE`, `SKIP`).

## Dataset

- Cases: 50
- Candidate memories: 93
- Current units: 122
- Gold READ IDs: 60
- Gold STORE units: 66
- Gold SKIP units: 56
- Source: `data/v04/model_predictions/p5_subset50_cases.jsonl`
- Predictions: `data/v04/model_predictions/p5_subset50_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 17 |
| `READ-only` | 11 |
| `STORE/SKIP-only` | 22 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 11 |
| `repo_memory` | 13 |
| `service_memory` | 16 |
| `task_state` | 16 |
| `user_profile` | 10 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `evaluator_case` | 6 |
| `parser_case` | 7 |
| `project_vs_repo` | 7 |
| `read_only` | 11 |
| `read_store_joint` | 17 |
| `related_but_useless` | 6 |
| `repo_convention` | 9 |
| `repo_vs_service` | 6 |
| `sensitive_boundary` | 15 |
| `service_invariant` | 17 |
| `service_vs_task_state` | 4 |
| `sop_skill_out_of_scope` | 3 |
| `stale_memory` | 5 |
| `store_skip_only` | 7 |
| `target_boundary` | 18 |
| `task_progress` | 12 |
| `user_profile_boundary` | 10 |
| `user_profile_vs_sensitive` | 10 |

## Systems

- `deepseek_v4_flash_subset50` from `data/v04/model_predictions/p5_subset50_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | deepseek_v4_flash_subset50 | 96.0% | 0.0% | 2.5% | 0.0% | 2.5% | 284.22 | 1.5 |
| unit_dsl | deepseek_v4_flash_subset50 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 50.4 | 1.74 |
| unit_json | deepseek_v4_flash_subset50 | 96.0% | 0.0% | 0.0% | 0.0% | 0.0% | 117.78 | 1.42 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | deepseek_v4_flash_subset50 | 48.0% | 0.872 | 0.864 | 92.6% | 0.832 | 8.5% | 10.5% | 0.0% |
| unit_dsl | deepseek_v4_flash_subset50 | 42.0% | 0.839 | 0.872 | 93.1% | 0.847 | 13.4% | 18.8% | 0.0% |
| unit_json | deepseek_v4_flash_subset50 | 50.0% | 0.845 | 0.870 | 94.7% | 0.844 | 12.3% | 12.5% | 0.0% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
