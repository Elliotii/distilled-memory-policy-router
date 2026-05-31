# v0.4 P5 Error Analysis

Date: 2026-05-31
Status: deterministic harness smoke analysis, not model error analysis

## Summary

The current errors come from deterministic baselines and intentionally invalid mocks. They are useful for checking metric behavior but should not be interpreted as LLM failure rates.

## Interface/System Overview

| Interface | System | Parse success | Exact | False store | Irrelevant read | Sensitive store |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| legacy_span_json | gold | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| legacy_span_json | empty | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| legacy_span_json | top1_read | 100.0% | 13.0% | 0.0% | 20.8% | 0.0% |
| legacy_span_json | heuristic | 100.0% | 33.5% | 5.6% | 21.1% | 0.0% |
| legacy_span_json | invalid_mock | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| unit_json | gold | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| unit_json | empty | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| unit_json | top1_read | 100.0% | 13.0% | 0.0% | 20.8% | 0.0% |
| unit_json | heuristic | 100.0% | 33.5% | 5.6% | 21.1% | 0.0% |
| unit_json | invalid_mock | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| unit_dsl | gold | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| unit_dsl | empty | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| unit_dsl | top1_read | 100.0% | 13.0% | 0.0% | 20.8% | 0.0% |
| unit_dsl | heuristic | 100.0% | 33.5% | 5.6% | 21.1% | 0.0% |
| unit_dsl | invalid_mock | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Empty Baseline

- READ recall: 0.000.
- STORE unit recall: 0.000.
- SKIP F1: 0.624.
- Expected behavior: it exposes the cost of never reading or storing while remaining structurally valid.

## Top-1 READ Baseline

- Irrelevant read rate: 20.8%.
- Expected behavior: it improves READ recall only when the first candidate is useful and otherwise demonstrates read pollution.

Example irrelevant reads:

- `v04_pilot_0137`: m1
- `v04_pilot_0138`: m1
- `v04_pilot_0139`: m1
- `v04_pilot_0140`: m1
- `v04_pilot_0142`: m1

## Heuristic Baseline

- Exact target match: 33.5%.
- STORE target accuracy on correctly selected STORE units: 92.9%.
- False store rate: 5.6%.
- Sensitive store rate: 0.0%.

Target confusion on correctly selected STORE units:

| Gold target | `project_memory` | `repo_memory` | `service_memory` | `task_state` | `user_profile` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `project_memory` | 7 | 4 | 5 | 1 | 0 |
| `repo_memory` | 0 | 50 | 0 | 0 | 0 |
| `service_memory` | 4 | 0 | 90 | 3 | 0 |
| `task_state` | 1 | 0 | 0 | 63 | 0 |
| `user_profile` | 0 | 0 | 0 | 0 | 27 |

Example false stores:

- `v04_pilot_0001`: u1
- `v04_pilot_0002`: u1
- `v04_pilot_0003`: u1
- `v04_pilot_0004`: u1
- `v04_pilot_0009`: u1

Example sensitive stores:

- None in this smoke run.

## Invalid Mock

- Parse success: 0.0%.
- Expected behavior: unknown memory IDs, unknown unit IDs, invalid targets, and missing assignments are counted as structural failures.

Example validation errors:

- `v04_pilot_0001`: unknown memory_id: m999
- `v04_pilot_0002`: unknown memory_id: m999
- `v04_pilot_0003`: unknown memory_id: m999
- `v04_pilot_0004`: unknown memory_id: m999
- `v04_pilot_0005`: unknown memory_id: m999

## Validation Error Examples Across Evaluated Results

- `v04_pilot_0001` (legacy_span_json/invalid_mock): unknown memory_id: m999
- `v04_pilot_0002` (legacy_span_json/invalid_mock): unknown memory_id: m999
- `v04_pilot_0003` (legacy_span_json/invalid_mock): unknown memory_id: m999
- `v04_pilot_0004` (legacy_span_json/invalid_mock): unknown memory_id: m999
- `v04_pilot_0005` (legacy_span_json/invalid_mock): unknown memory_id: m999
- `v04_pilot_0006` (legacy_span_json/invalid_mock): unknown memory_id: m999
- `v04_pilot_0007` (legacy_span_json/invalid_mock): unknown memory_id: m999
- `v04_pilot_0008` (legacy_span_json/invalid_mock): unknown memory_id: m999

## Next Error Analysis Step

After real model predictions are collected for A/B/C, replace these baseline examples with actual parse failures, span-copying errors, invalid IDs, target-boundary mistakes, false stores, and irrelevant reads.
