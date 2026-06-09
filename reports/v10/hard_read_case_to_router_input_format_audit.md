# Hard READ Case To Router Input Format Audit

## Purpose

This audit maps the hard READ v2 expanded fixture into the v0.5g Unit JSON router input format without implementing the converter.

No inference was run. No model or adapter was loaded.

## v0.5g Unit JSON Format

The v0.5g router prompt format is:

```text
RUNTIME_CONTEXT
project: ...
repo: ...
service: ...
task: ...

CANDIDATE_MEMORIES
m1 [service_memory]: ...
m2 [repo_memory]: ...

CURRENT_UNITS
u1: ...
u2: ...
```

The model output format is strict Unit JSON:

```json
{"read":["m1"],"store":[{"target":"task_state","unit_id":"u2"}],"skip":["u1"]}
```

Training/eval case rows have inline `candidate_memories` and a `gold` object:

```json
{
  "case_id": "...",
  "runtime_context": {},
  "candidate_memories": [],
  "current_units": [],
  "gold": {"read": [], "store": [], "skip": []}
}
```

## Hard READ Expanded Source Format

Expanded hard READ cases are stored in:

```text
data/v10/hard_read_v2_expanded/hard_read_v2_expanded_cases.jsonl
data/v10/hard_read_v2_expanded/hard_read_v2_expanded_memory_pool.jsonl
```

The case rows contain `candidate_memory_ids` and labels, but not inline `candidate_memories`. Memory text and targets live in the separate memory pool.

## Required Conversion

| Hard READ field | v05 Unit JSON field | Conversion rule |
| --- | --- | --- |
| `case_id` | `case_id` | Preserve exactly. |
| `runtime_context` | `runtime_context` | Preserve `project`, `repo`, `service`, `task`. |
| `candidate_memory_ids` | `candidate_memories` | Look up each ID in the memory pool and inline records in candidate order. |
| memory pool `memory_id` | candidate `memory_id` | Preserve exactly. |
| memory pool `target` | candidate `target` | Preserve exactly; values already match router targets. |
| memory pool `text` | candidate `text` | Preserve exactly. |
| memory pool `flags` | candidate `tags` | Use `tags = flags` for compatibility with v05 case examples. |
| `current_units` | `current_units` | Preserve unit IDs and text exactly. |
| `labels.required_memory_ids` + `labels.helpful_memory_ids` | `gold.read` | Use as learned READ target for evaluation. |
| current unit IDs | `gold.skip` | Use all current units as skip if no durable write target is intended. |
| `gold.store` | `gold.store` | Use empty list for hard READ-only evaluation. |
| `expected_answer_requirements` | metadata only | Do not send to the learned router. |
| `labels.candidate_labels` | metadata only | Do not send to the learned router. |

## Faithfulness Requirements

- Do not expose `expected_answer_requirements` to the learned router.
- Do not expose `labels`, `candidate_labels`, relevance categories, or hard-negative types in prompt text.
- Preserve candidate order from `candidate_memory_ids`; this lets the evaluation compare learned output to existing baselines.
- Preserve memory IDs exactly so `raw_output.read` can be replayed in the harness.
- Preserve all hard negatives. Do not remove stale, contradictory, wrong-scope, or sensitive-boundary candidates.
- Keep the evaluation READ-focused. STORE/SKIP predictions are diagnostic only for these cases.

## Format Risks

1. Candidate count shift: v05 training examples usually show fewer candidate memories; expanded hard READ has 10 candidates per case. This may stress the router beyond its familiar distribution.
2. READ label semantics shift: v05 training READ labels often reflect useful entity/context matching; hard READ requires choosing among near duplicates and stale or contradictory instructions.
3. Current-unit semantics shift: hard READ current units are task notes for answer generation, not durable memory updates. Marking all units as `skip` is format-compatible but may differ from training distribution.
4. Context length remains likely safe: hard READ expanded contexts are small enough for the configured `max_seq_length: 2048`, but the converter should measure rendered prompt length before inference.

## Validation Plan For Converter

Before any model run:

- JSONL parse converted cases.
- Assert row count is 32.
- Assert every converted row has inline `candidate_memories`.
- Assert every hard READ candidate ID appears exactly once in converted candidate memories.
- Assert no labels or expected answer requirements appear in rendered prompt text.
- Assert `gold.read` references only candidate memory IDs.
- Assert `gold.skip` covers every current unit when `gold.store` is empty.
- Render all rows through `render_user_input` and record max prompt length.

