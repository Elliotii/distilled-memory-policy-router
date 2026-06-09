# Learned READ Gap Closure Experiment Plan

## Objective

Evaluate whether the v0.5g learned router can select useful hard READ memories from the expanded v2 fixture when run offline and replayed inside the Applied Memory Harness.

This plan does not implement or run inference. It defines the next experiment.

## Experiment Inputs

- Cases: `data/v10/hard_read_v2_expanded/hard_read_v2_expanded_cases.jsonl`
- Memory pool: `data/v10/hard_read_v2_expanded/hard_read_v2_expanded_memory_pool.jsonl`
- Converted router cases: planned under `data/v10/hard_read_v2_expanded_learned_router/`
- Adapter: `results/v05g_bf16_lora/qwen35_json_r16_1000_4090/adapter`
- Base model: local `${QWEN35_MODEL_PATH}`

Adapter/base model availability must be confirmed before inference.

## Experiment Conditions

Required selection strategies:

- `no_memory`
- `all_candidates`
- `budgeted_candidate_order`
- `keyword_top_k`
- `random_k`
- `oracle_selected`
- `replay_learned_router`

Optional:

- `tfidf_top_k`
- `semantic_embedding_top_k`, only if local embeddings are already available.

## Procedure

1. Convert hard READ expanded cases into v05 Unit JSON case format.
2. Validate converted cases structurally and by rendered prompt audit.
3. Run offline learned-router prediction only after explicit approval and local artifact availability.
4. Save predictions JSONL.
5. Parse predictions and compute learned-router READ diagnostics.
6. Replay learned-router reads in the harness as `replay_learned_router`.
7. Compare against existing deterministic baselines and oracle.
8. Produce a gap-closure report with both aggregate and case-level failure analysis.

## Primary Metrics

- post-budget required recall;
- required selected count;
- avoid injected count;
- stale injected count;
- contradictory injected count;
- wrong-scope injected count;
- sensitive-boundary injected count;
- mean context chars.

## Learned-Router Diagnostics

- prediction row count;
- missing prediction count;
- JSON parse success;
- invalid memory ID count/rate;
- duplicate read ID count;
- empty read count;
- over-budget omitted required count;
- raw output examples for failures.

## Expected Outcomes

Possible positive result:

- learned-router required recall is meaningfully above `keyword_top_k`/`random_k` while injecting fewer hard negatives than `all_candidates`.

Possible mixed result:

- learned-router beats first-k order bias but still misses required memories or selects stale near-duplicates.

Possible negative result:

- learned-router behaves like entity matching and fails on hard distractor pools.

All three outcomes are valid. Negative results should be reported honestly and used to guide READ-specific architecture changes.

## No-Tuning Rule

Do not tune the expanded fixture, labels, prompt, or candidate order after seeing learned-router output. If prompt adaptation is desired, define it as a separate future experiment with pre-run criteria.

## Claim Boundary

This experiment can close the immediate learned-router evidence gap for the controlled expanded fixture. It still would not prove downstream utility, production behavior, or real retriever performance.

