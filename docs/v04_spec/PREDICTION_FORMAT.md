# PREDICTION_FORMAT

Version: v0.4 P5  
Scope: A/B/C interface comparison prediction records and raw output contracts

## Purpose

P5 compares three raw output interfaces on the same v0.4 pilot cases:

- A: Legacy Span JSON.
- B: Unit JSON.
- C: Unit DSL.

This document defines prediction files for evaluation harness smoke tests and future model-output collection. It does not define training data, a retriever, a writer, memory lifecycle operations, or a downstream agent.

## Prediction JSONL Row

Each prediction row should be one JSON object:

```json
{
  "case_id": "v04_pilot_0001",
  "interface": "unit_dsl",
  "system": "student-zero-shot",
  "raw_output": "READ m1\nSTORE service_memory u1\nSKIP u2"
}
```

Required fields:

| Field | Meaning |
| --- | --- |
| `case_id` | Case ID from the evaluated case file. |
| `interface` | One of `legacy_span_json`, `unit_json`, or `unit_dsl`. |
| `system` | System or baseline name, such as `gold`, `empty`, `top1_read`, `heuristic`, or a future model run name. |
| `raw_output` | The raw text produced by the interface prompt or deterministic baseline. |

Optional metadata may be added later if useful, such as `run_id`, `model_id`, `created_at`, `latency_ms`, or token counts. The evaluator should not require those fields for smoke tests.

## External Prediction Evaluation CLI

Existing raw outputs can be evaluated without calling any model:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.eval_runner \
  --cases data/v04/pilot_cases.jsonl \
  --predictions path/to/predictions.jsonl \
  --report reports/v04/interface_pilot_report.md \
  --error-report reports/v04/error_analysis.md
```

The runner groups rows by `(interface, system)`, ignores optional metadata, parses only `raw_output`, and scores against the selected case file. It does not invoke model inference or repair invalid outputs.

## A. Legacy Span JSON Raw Output

Raw output must be JSON:

```json
{
  "read_hints": ["m1"],
  "write_spans": [
    {"span": "The parser rejects unknown STORE targets.", "type": "service_memory"}
  ],
  "ignore_spans": ["Check tomorrow's weather after this."]
}
```

P5 interpretation:

- `read_hints` references candidate memory IDs.
- `write_spans[*].span` must exactly match one `current_units[*].text` value.
- `ignore_spans[*]` must exactly match one `current_units[*].text` value.
- `write_spans[*].type` is interpreted as the v0.4 STORE target for comparison, even though the legacy field name is `type`.
- Legal `type` values are the five v0.4 targets: `user_profile`, `project_memory`, `repo_memory`, `service_memory`, `task_state`.

The evaluator reports span-copying errors when a legacy span does not exactly map to one current unit.

## B. Unit JSON Raw Output

Raw output must be JSON:

```json
{
  "read": ["m1"],
  "store": [
    {"target": "service_memory", "unit_id": "u1"}
  ],
  "skip": ["u2"]
}
```

Rules:

- `read` may only reference candidate memory IDs.
- `store[*].unit_id` and `skip[*]` may only reference current unit IDs.
- `store[*].target` must be one of the five legal v0.4 targets.
- Every current unit must appear exactly once in `store` or `skip`.

## C. Unit DSL Raw Output

Raw output must use the strict v0.4 DSL:

```text
READ m1
STORE service_memory u1
SKIP u2
```

Empty sets use `NONE`:

```text
READ NONE
STORE NONE
SKIP u1,u2
```

The existing strict parser in `src/v04/parser.py` is the source of truth for DSL structural validity.

## Evaluator Canonical Form

All three interfaces are converted to the same canonical v0.4 shape before scoring:

```json
{
  "schema_version": "memory_policy.v0.4",
  "read": [{"memory_id": "m1"}],
  "store": [{"target": "service_memory", "unit_id": "u1"}],
  "skip": [{"unit_id": "u2"}],
  "validation": {"valid": true, "errors": []}
}
```

Invalid raw output is not semantically repaired. Invalid predictions are represented with `validation.valid = false` and empty canonical READ/STORE/SKIP lists for scoring.

## Deterministic Smoke Systems

P5 includes deterministic systems only:

- `gold`: gold-as-prediction smoke test.
- `empty`: READ none, STORE none, SKIP all current units.
- `top1_read` or `topk_read`: read first candidate memory/memories, STORE none, SKIP all current units.
- `heuristic`: simple lexical baseline.
- `invalid_mock`: intentionally invalid raw output.

These systems verify the harness and metrics. They are not model results and should not be used as evidence that one prompt interface is better for LLMs.
