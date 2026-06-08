# LLM Downstream-Lite Micro-Pilot Diagnostic

This report summarizes the completed C1-R2 DeepSeek V4 Flash micro-pilot for the downstream-lite prompt pack. It is a diagnostic execution report only: it checks pipeline feasibility and automatic citation behavior, not downstream task utility.

## Run Status

- Prompt rows: 14
- Response rows: 14
- API statuses: 14/14 OK
- Errors: 0
- Model recorded in responses: `deepseek-v4-flash`
- Temperature recorded in responses: `0.0`

## Citation Repair Status

Citation formatting was repaired in the current scored micro-pilot:

- Current-unit citations: 0 average invalid current-unit citations for every strategy.
- Bare memory references: 0 average bare memory references for every strategy.
- Hallucinated memory citations: 0 average hallucinated citations for every strategy.

The C1-R2 prompt repair hides current-unit IDs from LLM-facing prompt text while keeping memory IDs visible in the provided memory context. This leaves bracketed memory IDs such as `[m2]` as the only valid citation targets.

## Strategy Aggregate Citation Metrics

These metrics come from `reports/v10/llm_downstream_lite_micro_pilot_scores.json` and `reports/v10/llm_downstream_lite_micro_pilot_scores.md`.

| Strategy | Prompts | Response coverage | End-to-end required citation recall | Conditional required citation recall | Avg irrelevant citations | Avg hallucinated citations | Avg current-unit citations | Avg bare memory refs | Avg format violations | No responses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `all_candidates` | 2 | 1.000 | 0.667 | 0.667 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| `no_memory` | 2 | 1.000 | 0.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| `oracle_selected` | 2 | 1.000 | 0.500 | 0.500 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| `random_k` | 2 | 1.000 | 0.667 | 0.833 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| `router_selected` | 2 | 1.000 | 0.667 | 0.833 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| `shuffled_top_k` | 2 | 1.000 | 0.667 | 0.833 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| `top_k_naive` | 2 | 1.000 | 0.500 | 0.583 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |

## Interpretation Boundary

Citation recall is not full task quality. It only measures whether required memory IDs were cited in bracket form, and whether the response avoided diagnosed citation-format failures. It does not judge whether the answer chose the right action, used a cited fact correctly, over-weighted stale context, ignored important non-cited facts, or produced a useful task update.

This micro-pilot proves execution and scoring pipeline feasibility. It does not prove downstream utility.

## Case-Level Observations

### `v05e_gold_active_0002`

This case is mostly a sanity-check case because strategies converge. All memory-injecting strategies cite `m1` and `m2`, miss `m3`, and receive the same automatic citation recall. The `no_memory` condition correctly has no memory citations and serves mainly as the floor check for no-context citation behavior.

The convergence is useful for verifying stable prompt execution, response parsing, and citation scoring, but it is not very informative about strategy separation.

### `v05e_gold_active_0006`

This case is more informative because the injected memory sets and cited memory IDs differ by strategy.

- `no_memory` uses only current context and correctly avoids bracketed citations. It may over-attend to the hypothetical/current note about MLS data because no durable memory context is available.
- `router_selected` injects and cites `m2` and `m4`, giving full conditional recall over the memories it selected, but it misses required memory `m3` at the end-to-end level.
- `oracle_selected` injects `m2`, `m3`, and `m4`, but the response cites only `m2`. This shows that even oracle injection does not guarantee that the downstream model cites every gold memory.
- `shuffled_top_k` cites `m3` and `m4`, covering a different subset of required memory than `router_selected`.
- `top_k_naive` cites only `m2` and misses `m3` and `m4`.
- `all_candidates` cites `m2` and `m4` while avoiding the known irrelevant memory citation.

These differences are useful for selecting examples for manual review, because automatic citation recall alone cannot determine whether the memory use improved the task answer.

## Recommendation

Do not run the full 42-prompt pilot yet. Add manual scoring, or an explicitly scoped LLM-judge scoring pass, before expanding execution. The next review step should score required fact coverage, irrelevant memory contamination, hallucinated or stale fact use, task response quality, and citation compliance on the 14-row micro-pilot first.

The micro-pilot is ready for manual diagnostic review. It is not yet ready to support downstream utility claims.
