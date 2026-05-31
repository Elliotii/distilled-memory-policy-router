# v0.4 A/B/C Interface Pilot Report

Date: 2026-05-31
Status: P5 deterministic harness smoke test

## Scope

This report exercises the A/B/C evaluation harness on pilot data using deterministic baselines only. It does not contain real model outputs, model calls, training, retrieval, writing, or v0.5 locked-gold claims.

Interfaces:

- A: Legacy Span JSON (`read_hints`, `write_spans`, `ignore_spans`).
- B: Unit JSON (`read`, `store`, `skip`).
- C: Unit DSL (`READ`, `STORE`, `SKIP`).

## Dataset

- Cases: 200
- Candidate memories: 445
- Current units: 490
- Gold READ IDs: 244
- Gold STORE units: 268
- Gold SKIP units: 222
- Source: `data/v04/pilot_cases.jsonl`

Gold output shapes:

| Shape | Count |
| --- | ---: |
| `READ + STORE joint` | 73 |
| `READ-only` | 50 |
| `STORE/SKIP-only` | 77 |

STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 20 |
| `repo_memory` | 50 |
| `service_memory` | 100 |
| `task_state` | 71 |
| `user_profile` | 27 |

Tag distribution:

| Tag | Count |
| --- | ---: |
| `evaluator_case` | 15 |
| `parser_case` | 8 |
| `project_vs_repo` | 13 |
| `read_only` | 50 |
| `read_store_joint` | 73 |
| `related_but_useless` | 10 |
| `repo_convention` | 45 |
| `repo_vs_service` | 18 |
| `sensitive_boundary` | 48 |
| `service_invariant` | 120 |
| `service_vs_task_state` | 5 |
| `sop_skill_out_of_scope` | 12 |
| `stale_memory` | 15 |
| `store_skip_only` | 45 |
| `target_boundary` | 32 |
| `task_progress` | 66 |
| `user_profile_boundary` | 27 |
| `user_profile_vs_sensitive` | 27 |

## Systems

- `gold`: gold-as-prediction smoke test.
- `empty`: no READ, no STORE, SKIP all current units.
- `top1_read`: read the first 1 candidate memory/memories, STORE none, SKIP all units.
- `heuristic`: deterministic lexical read/store/skip heuristic.
- `invalid_mock`: intentionally invalid raw output for parser/schema smoke testing.

## Structural Metrics

| Interface | System | Parse success | Invalid memory ID | Invalid unit/span | Invalid target | Span copy error | Avg chars | Repair cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | gold | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 246.73 | 0.0 |
| legacy_span_json | empty | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 200.19 | 3.0 |
| legacy_span_json | top1_read | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 202.79 | 2.61 |
| legacy_span_json | heuristic | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 244.305 | 1.995 |
| legacy_span_json | invalid_mock | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 121.0 | 2.0 |
| unit_json | gold | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 96.49 | 0.0 |
| unit_json | empty | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 43.25 | 3.0 |
| unit_json | top1_read | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 45.85 | 2.61 |
| unit_json | heuristic | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 94.115 | 1.995 |
| unit_json | invalid_mock | 0.0% | 100.0% | 100.0% | 100.0% | 0.0% | 78.0 | 2.0 |
| unit_dsl | gold | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 50.51 | 0.0 |
| unit_dsl | empty | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 32.35 | 3.0 |
| unit_dsl | top1_read | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 31.05 | 2.61 |
| unit_dsl | heuristic | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 49.815 | 1.995 |
| unit_dsl | invalid_mock | 0.0% | 100.0% | 100.0% | 100.0% | 0.0% | 35.0 | 2.0 |

## Semantic Metrics

| Interface | System | Exact | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | gold | 100.0% | 1.000 | 1.000 | 100.0% | 1.000 | 0.0% | 0.0% | 0.0% |
| legacy_span_json | empty | 0.0% | 0.000 | 0.000 | 0.0% | 0.624 | 0.0% | 0.0% | 0.0% |
| legacy_span_json | top1_read | 13.0% | 0.551 | 0.000 | 0.0% | 0.624 | 0.0% | 20.8% | 0.0% |
| legacy_span_json | heuristic | 33.5% | 0.529 | 0.948 | 92.9% | 0.937 | 5.6% | 21.1% | 0.0% |
| legacy_span_json | invalid_mock | 0.0% | 0.000 | 0.000 | 0.0% | 0.000 | 0.0% | 0.0% | 0.0% |
| unit_json | gold | 100.0% | 1.000 | 1.000 | 100.0% | 1.000 | 0.0% | 0.0% | 0.0% |
| unit_json | empty | 0.0% | 0.000 | 0.000 | 0.0% | 0.624 | 0.0% | 0.0% | 0.0% |
| unit_json | top1_read | 13.0% | 0.551 | 0.000 | 0.0% | 0.624 | 0.0% | 20.8% | 0.0% |
| unit_json | heuristic | 33.5% | 0.529 | 0.948 | 92.9% | 0.937 | 5.6% | 21.1% | 0.0% |
| unit_json | invalid_mock | 0.0% | 0.000 | 0.000 | 0.0% | 0.000 | 0.0% | 0.0% | 0.0% |
| unit_dsl | gold | 100.0% | 1.000 | 1.000 | 100.0% | 1.000 | 0.0% | 0.0% | 0.0% |
| unit_dsl | empty | 0.0% | 0.000 | 0.000 | 0.0% | 0.624 | 0.0% | 0.0% | 0.0% |
| unit_dsl | top1_read | 13.0% | 0.551 | 0.000 | 0.0% | 0.624 | 0.0% | 20.8% | 0.0% |
| unit_dsl | heuristic | 33.5% | 0.529 | 0.948 | 92.9% | 0.937 | 5.6% | 21.1% | 0.0% |
| unit_dsl | invalid_mock | 0.0% | 0.000 | 0.000 | 0.0% | 0.000 | 0.0% | 0.0% | 0.0% |

## Interpretation

- Gold-as-prediction verifies that all three adapters can represent the pilot labels without loss.
- The invalid mock verifies that schema, ID, target, and span-copying failures are counted instead of repaired.
- Deterministic baselines are task sanity checks, not evidence that one raw model interface is better than another.
- A real A/B/C interface claim still requires model outputs collected with the three prompt templates under identical cases and settings.
- External prediction files are evaluated as supplied; optional metadata is ignored and raw outputs are not repaired.

## Recommendation

The P5 harness is ready for owner review and future model-output collection. Do not proceed to v0.5 training from these smoke-test numbers alone.
