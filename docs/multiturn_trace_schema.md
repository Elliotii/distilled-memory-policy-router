# Multi-Turn Trace Schema

This document defines the small MVP trace format used after the single-turn
train/dev/gold datasets are complete. The trace format is for demonstration and
workflow evaluation only. It is not a full coding-agent trace and it does not
extend the router output contract.

## Purpose

Multi-turn traces test whether the same memory-policy decisions stay coherent
over a short conversation:

- reading relevant candidate memories after context accumulates;
- writing durable facts, decisions, SOPs, and task states;
- ignoring temporary noise and corrected mistakes;
- resolving stale or conflicting memories over multiple turns.

## File Layout

Authoritative MVP trace file:

- `data/traces/multiturn_traces_8.jsonl`

Companion files:

- `data/traces/multiturn_traces_8.metadata.json`
- `data/traces/multiturn_traces_8.validation_report.txt`

## JSONL Record Shape

Each JSONL line is one trace:

```json
{
  "trace_id": "trace_001",
  "split": "trace_eval",
  "domain": "backend",
  "tags": ["multi_turn", "correction"],
  "review_status": "synthetic_reviewed",
  "trace_goal": "Short description of the behavior being tested.",
  "turns": [
    {
      "turn_id": "trace_001_t1",
      "current_user_input": "User message for this router decision.",
      "recent_context": [],
      "candidate_memories": [],
      "target": {
        "read_hints": [],
        "write_spans": [],
        "ignore_spans": []
      },
      "notes": "Optional human-readable note for trace review."
    }
  ]
}
```

## Constraints

Trace-level constraints:

- `trace_id` must be unique.
- `turns` must contain 2-5 decision turns.
- Content must be English and ASCII.

Turn-level constraints:

- `current_user_input` is required.
- `recent_context` contains 0-4 turns.
- `candidate_memories` contains 0-8 items.
- `candidate_memories[*].id` must be unique within the turn.
- `target.read_hints` may reference only IDs present in
  `candidate_memories`.
- Every `target.write_spans[*].span` must be an exact substring of
  `current_user_input`.
- Every `target.ignore_spans[*]` must be an exact substring of
  `current_user_input`.
- `target.write_spans[*].type` must be one of `fact`, `decision`, `sop`, or
  `task_state`.

## Boundary

The trace file may include notes for review, but the router target remains only:

- `read_hints`
- `write_spans`
- `ignore_spans`

The trace format does not ask the router to produce final memory rewrites,
project IDs, confidence scores, update/delete operations, or downstream agent
actions.
