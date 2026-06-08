# Applied Memory Harness Design

## Purpose

The Applied Memory Harness is the planned final v1.0-applied layer. It should turn the current evaluation package into an auditable, small memory-policy harness without building a complete agent runtime.

This document is design-only. The commands and layout below are planned, not implemented in this context.

## System Boundary

Inside the harness:

- controlled user input fixture;
- current-unit extraction stub;
- small SQLite memory store;
- BM25/keyword candidate retriever stub;
- router/backend selection interface;
- budgeted context builder;
- STORE/SKIP preview;
- sensitive, stale, and contradiction flags;
- JSON audit trace.

Outside the harness:

- autonomous planning;
- production retrieval stack;
- final memory writing without review;
- memory merge/update/delete lifecycle;
- tool execution;
- production safety policy;
- large-scale UI or service deployment.

## Non-Goals

- Do not build a full coding agent.
- Do not build a comprehensive memory operating system.
- Do not claim live retrieval quality.
- Do not claim deployment readiness.
- Do not run new model training.
- Do not require live LoRA for the minimum v1.0-applied harness.

## Data Flow

```text
user input
  -> unitizer
  -> memory store
  -> retriever
  -> selector/router backend
  -> budgeted context builder
  -> downstream LLM
  -> STORE/SKIP preview
  -> audit trace
```

The downstream LLM step can be mocked or run later under a fixed model setting. The v1.0 must-have is the traceable harness path and selection comparison, not live generation.

## Components

### Unitizer Stub

Splits user input or scenario text into current units. For v1.0-applied, this can be rule-based or fixture-provided. The unitizer is not the research target.

### SQLite Memory Store

Stores memory records with IDs, text, target/type, timestamps or fixture metadata, and optional flags. SQLite keeps the harness inspectable and avoids committing large external systems.

### BM25/Keyword Retriever Stub

Returns a bounded candidate set from the memory store. This is a candidate generator, not a production retrieval claim. It exists to create realistic candidate pools for the selector/router layer.

### RouterBackend Interface

Planned interface:

```text
select(input) -> {
  read_memory_ids,
  store_units,
  skip_unit_ids,
  diagnostics
}
```

All backends should consume the same current units, candidate memories, and budget settings.

### Decoupled READ Selector And WRITE Policy

The harness should allow READ selection to be separated from WRITE policy:

- READ selector backends can be BM25, embedding, `random_k`, `all_candidates`, replay, or live LoRA.
- WRITE policy backends can be replayed router output, live LoRA, fixture labels, or disabled.
- This supports a hybrid practical architecture: READ can use a simple scorer and budgeted selector if it beats learned READ, while WRITE can still use learned STORE/SKIP/target policy when available.
- Audit traces should record both `read_selector_backend` and `write_policy_backend` when they differ.

This separation keeps the design honest: learned routing does not need to own READ if simple retrieval or reranking baselines perform better on hard candidate pools.

### ReplayBackend

Uses saved predictions or fixture labels. This supports no-inference reproducibility and is the safest baseline for demonstrations.

### HeuristicBaselineBackend

Implements simple transparent selection rules:

- no memory;
- all candidates;
- keyword top-k;
- random k with fixed seed;
- stale/sensitive flag filtering.

### LiveLoRABackend Placeholder

Optional future backend that loads the LoRA adapter in a controlled local environment. It is not required for the initial harness skeleton and should be isolated from the CLI trace path.

### Context Builder

Builds a budgeted memory context from selected memory IDs:

- maximum memory count;
- maximum character or token proxy budget;
- stable ordering;
- citation IDs preserved;
- omitted-memory diagnostics.

### Write Gate / STORE Preview

Displays STORE decisions and targets as a preview. It should not write new durable memory by default. Human or policy review remains required.

### Sensitive/Stale/Contradiction Flags

Flags should be carried through memory records and current units:

- `sensitive_boundary`;
- `stale_or_resolved`;
- `hypothetical`;
- `contradiction_risk`;
- `wrong_scope`;
- `needs_review`.

These are audit aids, not safety guarantees.

### Audit Trace Emitter

Emits one JSON trace per run. This is the v1.0 must-have because it makes decisions inspectable and allows baseline comparison without adding a large UI.

## Why CLI + JSON Trace Is Required

The CLI plus JSON trace is the smallest useful applied harness:

- easy to run in review;
- no API key requirement;
- no UI dependency;
- deterministic baseline comparison;
- traceable inputs, selections, and omitted candidates;
- supports later Streamlit or web views.

## Why Streamlit Is Optional

Streamlit is useful for interview demos and visual trace review, but it should sit on top of the JSON trace format. If the trace is good, the UI is replaceable.

## Why FastAPI + React Is Not v1.0

FastAPI + React adds service and frontend scope before the core harness is proven. That stack is appropriate after the CLI trace, hard READ eval, and baseline comparisons are stable.

## Audit Trace JSON Schema

Planned schema:

```json
{
  "trace_id": "string",
  "created_at": "iso8601 timestamp",
  "scenario_id": "string",
  "user_input": "string",
  "current_units": [
    {
      "unit_id": "u1",
      "text": "string",
      "source": "unitizer_stub|fixture",
      "flags": ["hypothetical", "stale_or_resolved"]
    }
  ],
  "retrieval": {
    "backend": "keyword|bm25|fixture",
    "query": "string",
    "candidate_count": 10,
    "candidates": [
      {
        "memory_id": "m1",
        "target": "repo_memory",
        "text": "string",
        "score": 0.0,
        "flags": ["wrong_scope"],
        "source": "sqlite_memory_store"
      }
    ]
  },
  "router": {
    "read_selector_backend": "BM25|embedding|random_k|all_candidates|ReplayBackend|LiveLoRABackend",
    "write_policy_backend": "disabled|fixture|ReplayBackend|LiveLoRABackend",
    "model_or_rule": "string",
    "read_memory_ids": ["m1"],
    "store_units": [
      {
        "unit_id": "u2",
        "target": "task_state"
      }
    ],
    "skip_unit_ids": ["u1"],
    "diagnostics": {
      "parse_ok": true,
      "budget_reason": "string",
      "warnings": []
    }
  },
  "context_builder": {
    "max_memories": 4,
    "max_context_chars": 1600,
    "selected_memory_ids": ["m1"],
    "omitted_candidate_ids": ["m2"],
    "context_text": "string"
  },
  "downstream_response": {
    "backend": "none|fixed_llm|mock",
    "response_text": "string",
    "citations": ["m1"]
  },
  "write_preview": {
    "store_units": [
      {
        "unit_id": "u2",
        "target": "task_state",
        "text": "string",
        "review_required": true
      }
    ],
    "skip_unit_ids": ["u1"]
  },
  "evaluation": {
    "required_memory_ids": ["m1"],
    "avoid_memory_ids": ["m3"],
    "required_selected_recall": 1.0,
    "avoid_selected_count": 0,
    "notes": "string"
  }
}
```

## Planned Repo Layout

Planned layout, not created in this context:

```text
apps/memory_harness/
  README.md
  cli.py
  schemas.py
  unitizer.py
  memory_store.py
  retrievers.py
  backends/
    __init__.py
    replay.py
    heuristic.py
    live_lora.py
  context_builder.py
  write_preview.py
  audit_trace.py
  fixtures/
    scenarios.jsonl
    memory_pool.jsonl
  traces/
    .gitkeep
```

## Planned CLI Examples

These commands are planned examples and are not implemented in this context:

```bash
python3 apps/memory_harness/cli.py \
  --scenario apps/memory_harness/fixtures/scenarios.jsonl \
  --memory-pool apps/memory_harness/fixtures/memory_pool.jsonl \
  --backend replay \
  --trace-out /tmp/dmpr_trace_replay.json
```

```bash
python3 apps/memory_harness/cli.py \
  --scenario-id hard_read_001 \
  --backend keyword_top_k \
  --max-memories 4 \
  --trace-out /tmp/dmpr_trace_keyword.json
```

```bash
python3 apps/memory_harness/cli.py \
  --scenario-id hard_read_001 \
  --backend live_lora \
  --trace-out /tmp/dmpr_trace_live_lora.json
```

## Minimum v1.0-Applied Acceptance

- Can run a fixture scenario through all planned stages except optional live generation.
- Can compare at least replay, no-memory, all-candidates, keyword/BM25, and random-k selection.
- Emits complete JSON traces.
- Keeps STORE as preview only.
- Records hard READ misses, stale selections, and avoid-memory selections.
