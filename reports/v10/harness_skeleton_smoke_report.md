# Applied Memory Harness Skeleton Smoke Report

Context: 7.2 Applied Memory Harness skeleton implementation.

This report covers deterministic fixture replay only. No API, external LLM, Qwen, LoRA, training, UI, or full hard READ evaluation was run.

## Scope

Implemented a minimal standard-library harness under `apps/memory_harness/` with:

- JSONL fixture loading and validation.
- Current-user-input unitization.
- JSONL memory-pool store abstraction.
- Deterministic keyword retrieval stub.
- READ selector backends: `no_memory`, `all_candidates`, `keyword_top_k`, `random_k`, `oracle_selected`, `replay_router_selected`.
- WRITE policy backends: `disabled`, `fixture`.
- Budgeted memory context builder.
- Preview-only STORE/SKIP write preview.
- JSON audit trace emission with separate `read_selector_backend` and `write_policy_backend`.
- CLI smoke commands for listing scenarios, running one selector, and comparing all selectors.

## Fixture Scenarios

The fixture pack contains 3 scenarios and 22 memory records.

- `hard_read_demo_001`: checkout-api retry handling with required memories, same-entity irrelevant memory, legacy resolved memory, contradictory memory, and scope-mismatch memory.
- `hard_read_demo_002`: analytics-worker privacy export with sensitive-boundary current input and distractor memories.
- `hard_read_demo_003`: renderer-service accessibility checks with repo command selection and legacy resolved incident distractor.

Case-specific relevance and hard-negative labels live in `apps/memory_harness/fixtures/scenarios.jsonl`. The shared memory pool keeps only intrinsic memory fields plus intrinsic flags.

## Smoke Commands

Compiled harness modules:

```bash
PYTHONPYCACHEPREFIX=/tmp/dmpr_pycache python3 -m py_compile apps/memory_harness/*.py apps/memory_harness/backends/*.py
```

Listed scenarios:

```bash
python3 apps/memory_harness/cli.py --scenario-file apps/memory_harness/fixtures/scenarios.jsonl --list-scenarios
```

Created a single-selector trace:

```bash
python3 apps/memory_harness/cli.py --scenario-file apps/memory_harness/fixtures/scenarios.jsonl --memory-pool apps/memory_harness/fixtures/memory_pool.jsonl --scenario-id hard_read_demo_001 --read-selector keyword_top_k --write-policy fixture --max-memories 3 --max-context-chars 1200 --trace-out reports/v10/harness_traces/smoke_trace_keyword.json
```

Created a selector comparison trace:

```bash
python3 apps/memory_harness/cli.py --scenario-file apps/memory_harness/fixtures/scenarios.jsonl --memory-pool apps/memory_harness/fixtures/memory_pool.jsonl --scenario-id hard_read_demo_001 --write-policy fixture --max-memories 3 --max-context-chars 1200 --compare-all --trace-out reports/v10/harness_traces/smoke_trace_compare_all.json
```

## Trace Outputs

Created:

- `reports/v10/harness_traces/smoke_trace_keyword.json`
- `reports/v10/harness_traces/smoke_trace_compare_all.json`

Single-selector trace check:

- `read_selector_backend`: `keyword_top_k`
- `write_policy_backend`: `fixture`
- selected/context memory ids: `m001`, `m004`, `m002`
- STORE preview count: 2
- SKIP preview count: 1
- downstream response backend: `none`

Compare-all trace check:

- scenario: `hard_read_demo_001`
- run count: 6
- selectors: `no_memory`, `all_candidates`, `keyword_top_k`, `random_k`, `oracle_selected`, `replay_router_selected`
- all runs used `write_policy_backend = fixture`
- all runs used `downstream_response.backend = none`

## Validation

Passed:

- `py_compile` for `apps/memory_harness/*.py` and `apps/memory_harness/backends/*.py`.
- Scenario listing CLI command.
- Single-selector trace generation.
- Compare-all trace generation.
- JSON parse and required-field checks for both trace files.
- JSONL row-count check for scenario and memory-pool fixtures.
- Grep confirmed `read_selector_backend` and `write_policy_backend` are present in the trace.
- Grep confirmed `relevance_category` and `hard_negative_type` are absent from the shared memory pool.

## Known Limitations

- Retrieval is a deterministic keyword stub, not a production retriever.
- WRITE behavior is preview-only and does not mutate a memory store.
- Fixture and oracle backends are audit scaffolds, not deployed router behavior.
- The skeleton does not run downstream answer generation or quality judging.
- The smoke test exercises one comparison scenario, not the full planned hard READ suite.
- Live LoRA routing, SQLite persistence, baseline evaluation summaries, and Streamlit trace viewing remain future work.

## Next Context

Next context should be 7.3: hard-candidate fixture expansion or hard READ evaluation harness, depending on whether the next step is data expansion or metric wiring.
