# Learned-Router Downstream Subset Next Step Plan

## Scope

This is a plan for the next context only. Do not run downstream API calls, prompt-response evaluation, new AutoDL inference, model loading, training, live serving, or UI work in this context.

## Design

Add `learned_router` as a seventh strategy to the existing expanded downstream 8-case subset.

The existing subset had:

- 8 cases
- 6 strategies
- 48 prompts

Adding `learned_router` creates:

- 56 prompts if rebuilding the full prompt pack from scratch
- or 8 additional learned-router prompts if extending the existing pack

Use the imported replay predictions from:

```text
data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl
```

Inject the memories selected by `replay_learned_router` and compare against:

- `no_memory`
- `all_candidates`
- `budgeted_candidate_order`
- `keyword_top_k`
- `random_k`
- `oracle_selected`
- `learned_router`

## Key Questions

- Does learned-router high selection recall translate into better downstream response quality?
- Does contradictory contamination hurt answer quality?
- Are clean full-recall learned-router cases reliably better than no-memory and keyword/random baselines?
- Are miss-plus-contradiction cases visibly worse, or can the downstream answerer still follow the required memories?

## Suggested Case Mix

Use the existing 8-case expanded downstream subset if continuity is more important than targeted audit coverage. If replacing or adding cases is allowed, include:

- clean full-recall/no-avoid examples such as `hard_read_v2_002` and `hard_read_v2_003`;
- miss cases such as `hard_read_v2_005`, `hard_read_v2_011`, `hard_read_v2_031`, and `hard_read_v2_032`;
- a full-recall but contaminated case such as `hard_read_v2_030`.

## Stop Condition

Run the 8-case downstream subset with learned-router injection, perform rubric review, then package regardless of positive or negative result.

## Claim Boundary

The downstream subset will be a small controlled response-quality check. It should not be used to claim general retrieval quality, production readiness, or that READ is solved.
