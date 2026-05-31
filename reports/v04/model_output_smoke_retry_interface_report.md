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

- Cases: 5
- Candidate memories: 10
- Current units: 12
- Gold READ IDs: 7
- Gold STORE units: 6
- Gold SKIP units: 6
- Source: `data/v04/model_predictions/p5_smoke_cases.jsonl`
- Predictions: `data/v04/model_predictions/p5_smoke_retry_predictions.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 2 |
| `READ-only` | 1 |
| `STORE/SKIP-only` | 2 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 2 |
| `repo_memory` | 1 |
| `service_memory` | 1 |
| `task_state` | 1 |
| `user_profile` | 1 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `evaluator_case` | 1 |
| `parser_case` | 2 |
| `project_vs_repo` | 1 |
| `read_only` | 1 |
| `read_store_joint` | 2 |
| `related_but_useless` | 1 |
| `repo_convention` | 2 |
| `sensitive_boundary` | 2 |
| `service_invariant` | 2 |
| `store_skip_only` | 2 |
| `target_boundary` | 1 |
| `task_progress` | 1 |
| `user_profile_boundary` | 1 |
| `user_profile_vs_sensitive` | 1 |

## Systems

- `deepseek_v4_flash_smoke_retry` from `data/v04/model_predictions/p5_smoke_retry_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | deepseek_v4_flash_smoke_retry | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 298.2 | 1.8 |
| unit_dsl | deepseek_v4_flash_smoke_retry | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 51.0 | 1.8 |
| unit_json | deepseek_v4_flash_smoke_retry | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 117.6 | 1.2 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | deepseek_v4_flash_smoke_retry | 40.0% | 1.000 | 0.833 | 80.0% | 0.833 | 16.7% | 0.0% | 0.0% |
| unit_dsl | deepseek_v4_flash_smoke_retry | 40.0% | 0.923 | 0.923 | 83.3% | 0.909 | 14.3% | 0.0% | 0.0% |
| unit_json | deepseek_v4_flash_smoke_retry | 60.0% | 1.000 | 0.833 | 80.0% | 0.833 | 16.7% | 0.0% | 0.0% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
