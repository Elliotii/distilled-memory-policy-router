# Applied Memory Harness Skeleton

This is a minimal stdlib-only skeleton for replaying small memory-policy fixture scenarios through deterministic READ selectors and WRITE policy previews.

It does:

- load JSONL scenario and memory-pool fixtures;
- create current units from fixtures or a deterministic unitizer stub;
- run deterministic READ selector baselines;
- run fixture or disabled WRITE policy;
- build a budgeted memory context;
- emit JSON audit traces;
- keep STORE output as review-only preview.

It does not:

- call APIs;
- run external LLMs;
- load Qwen or LoRA adapters;
- train models;
- provide production safety;
- implement a production retrieval stack;
- write durable memory.

## List Scenarios

```bash
python3 apps/memory_harness/cli.py \
  --scenario-file apps/memory_harness/fixtures/scenarios.jsonl \
  --memory-pool apps/memory_harness/fixtures/memory_pool.jsonl \
  --list-scenarios
```

## Run One Selector

```bash
python3 apps/memory_harness/cli.py \
  --scenario-file apps/memory_harness/fixtures/scenarios.jsonl \
  --memory-pool apps/memory_harness/fixtures/memory_pool.jsonl \
  --scenario-id hard_read_demo_001 \
  --read-selector keyword_top_k \
  --write-policy fixture \
  --max-memories 4 \
  --max-context-chars 1600 \
  --trace-out reports/v10/harness_traces/smoke_trace_keyword.json
```

## Run Compare-All

```bash
python3 apps/memory_harness/cli.py \
  --scenario-file apps/memory_harness/fixtures/scenarios.jsonl \
  --memory-pool apps/memory_harness/fixtures/memory_pool.jsonl \
  --scenario-id hard_read_demo_001 \
  --compare-all \
  --write-policy fixture \
  --max-memories 4 \
  --max-context-chars 1600 \
  --trace-out reports/v10/harness_traces/smoke_trace_compare_all.json
```

## Reading Trace Files

Each trace records:

- scenario and current units;
- retrieval candidates and keyword scores;
- `read_selector_backend`;
- `write_policy_backend`;
- budgeted context builder output;
- downstream response backend set to `none`;
- STORE/SKIP preview;
- diagnostic evaluation counts where labels exist.

The trace is an audit artifact, not an answer-quality result.

## Current 7.2 Scope

Context 7.2 uses JSONL fixtures to keep the first implementation small and auditable. SQLite memory store, live LoRA backend, Streamlit trace viewer, and broader hard READ evaluation are planned for later contexts.
