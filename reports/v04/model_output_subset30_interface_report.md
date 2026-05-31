# v0.4 A/B/C Interface Pilot Report

Date: 2026-05-31
Status: P5 external prediction evaluation

## Scope

This report evaluates an external prediction JSONL file that already contains raw outputs. The runner only loads and scores those rows; it does not call models, train, retrieve, write memories, or make v0.5 locked-gold claims.

Interfaces:

- A: Legacy Span JSON (`read_hints`, `write_spans`, `ignore_spans`).
- B: Unit JSON (`read`, `store`, `skip`).
- C: Unit DSL (`READ`, `STORE`, `SKIP`).

## Dataset

- Cases: 30
- Candidate memories: 62
- Current units: 73
- Gold READ IDs: 38
- Gold STORE units: 38
- Gold SKIP units: 35
- Source: `data/v04/model_predictions/p5_subset30_cases.jsonl`
- Predictions: `data/v04/model_predictions/p5_subset30_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 11 |
| `READ-only` | 7 |
| `STORE/SKIP-only` | 12 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 5 |
| `repo_memory` | 7 |
| `service_memory` | 10 |
| `task_state` | 9 |
| `user_profile` | 7 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `evaluator_case` | 5 |
| `parser_case` | 6 |
| `project_vs_repo` | 3 |
| `read_only` | 7 |
| `read_store_joint` | 11 |
| `related_but_useless` | 3 |
| `repo_convention` | 7 |
| `repo_vs_service` | 3 |
| `sensitive_boundary` | 10 |
| `service_invariant` | 12 |
| `service_vs_task_state` | 2 |
| `sop_skill_out_of_scope` | 1 |
| `stale_memory` | 2 |
| `store_skip_only` | 5 |
| `target_boundary` | 8 |
| `task_progress` | 7 |
| `user_profile_boundary` | 7 |
| `user_profile_vs_sensitive` | 7 |

## Systems

- `deepseek_v4_flash_subset30` from `data/v04/model_predictions/p5_subset30_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | deepseek_v4_flash_subset30 | 93.3% | 0.0% | 4.3% | 0.0% | 4.3% | 281.533 | 1.6 |
| unit_dsl | deepseek_v4_flash_subset30 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 50.1 | 1.8 |
| unit_json | deepseek_v4_flash_subset30 | 96.7% | 0.0% | 0.0% | 0.0% | 0.0% | 117.867 | 1.533333 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | deepseek_v4_flash_subset30 | 43.3% | 0.895 | 0.861 | 93.5% | 0.824 | 8.8% | 10.5% | 0.0% |
| unit_dsl | deepseek_v4_flash_subset30 | 40.0% | 0.810 | 0.909 | 91.4% | 0.899 | 10.3% | 22.0% | 0.0% |
| unit_json | deepseek_v4_flash_subset30 | 46.7% | 0.827 | 0.895 | 94.1% | 0.882 | 10.5% | 16.2% | 0.0% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
