# replay_learned_router Selector Design

## Goal

Add a harness selector that replays saved offline learned-router predictions without loading a model. This makes learned-router READ behavior comparable to existing selectors in the Applied Memory Harness.

No implementation is included in this context.

## Prediction Input

Expected prediction rows should follow `src/v05/eval_lora_router.py` output:

```json
{
  "case_id": "hard_read_v2_001",
  "interface": "unit_json",
  "adapter_path": "results/v05g_bf16_lora/qwen35_json_r16_1000_4090/adapter",
  "raw_output": "{\"read\":[\"m201\",\"m202\"],\"store\":[],\"skip\":[\"u1\",\"u2\",\"u3\"]}",
  "error": null
}
```

The selector should use only `raw_output.read` for memory selection.

## Selector Behavior

Proposed backend name:

```text
replay_learned_router
```

Behavior:

1. Load prediction JSONL once into `case_id -> prediction`.
2. For each scenario/case, find matching prediction by `case_id` or `scenario_id`.
3. Parse `raw_output` as JSON.
4. Extract `read` as a list of memory IDs.
5. Filter to IDs present in the current candidate set.
6. Preserve candidate order in the returned `selected_memory_ids`.
7. Record diagnostics:
   - prediction found/missing;
   - parse success/failure;
   - raw read IDs;
   - invalid read IDs;
   - duplicate read IDs;
   - selected read IDs after candidate filtering;
   - prediction `error`, if present.

## Harness Integration Points

Current selector registry:

```text
apps/memory_harness/backends/read_selectors.py
```

Current strategy names:

```text
no_memory
all_candidates
budgeted_candidate_order
keyword_top_k
random_k
oracle_selected
replay_router_selected
```

`replay_learned_router` should be added beside `replay_router_selected`, but should not rely on `scenario.fixture_router_read_ids`. It should take a prediction file argument either through the CLI or eval runner.

## CLI/Eval Changes Needed

Minimal changes:

- Add optional `--learned-router-predictions` to `apps/memory_harness/eval_hard_read.py`.
- Add `replay_learned_router` to the strategy list only when a prediction file is supplied.
- Pass a loaded prediction map into `run_read_selector`.
- Keep existing deterministic baselines unchanged.

Optional CLI trace support:

- Add `--learned-router-predictions` to `apps/memory_harness/cli.py`.
- Include `replay_learned_router` in `--compare-all` only if predictions are supplied.

## Metric Treatment

Use the same hard READ metrics already used for other selectors:

- required recall;
- helpful count;
- avoid count;
- stale count;
- contradictory count;
- wrong-scope count;
- sensitive-boundary count;
- context chars after budget.

Add learned-router-specific diagnostics:

- parse success rate;
- invalid read ID rate;
- missing prediction count;
- empty read count;
- over-budget omitted required count.

## Failure Policy

If `replay_learned_router` performs poorly:

- keep the results;
- report parse/invalid/missing cases explicitly;
- do not change fixture order;
- do not relax labels;
- do not exclude hard negatives after seeing results;
- do not tune the learned-router prompt against the expanded fixture unless a later experiment is pre-registered as prompt adaptation.

The purpose is gap closure, not forcing a favorable result.

