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
- Predictions: `data/v05b/model_predictions/qwen3_4b_lora_json_500_dev_predictions.jsonl`

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

- `qwen3_4b_lora_json_125_unit_json` from `data/v05b/model_predictions/qwen3_4b_lora_json_500_dev_predictions.jsonl`.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_json | qwen3_4b_lora_json_125_unit_json | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 134.11 | 1.98 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unit_json | qwen3_4b_lora_json_125_unit_json | 34.0% | 0.902 | 0.958 | 68.5% | 0.753 | 6.5% | 15.9% | 66.7% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
