# Hard READ Selection Pilot Report

Context: hard READ pilot fixture selection-only evaluation.

This report evaluates memory selection only. It does not run a downstream answerer, call an API, load Qwen or LoRA, or evaluate learned router/live LoRA behavior.

Learned router/live LoRA is not evaluated because no real backend output is available for these hard-read cases.

## Run Summary

- Case count: 8
- Memory pool count: 80
- Strategies evaluated: no_memory, all_candidates, budgeted_candidate_order, keyword_top_k, random_k, oracle_selected

## v2 Design Intent Compared With v1

- Candidate memory order is fixed-seed shuffled rather than label-ordered, so `budgeted_candidate_order` is a stress test for order bias rather than a favorable pseudo-oracle.
- Current task notes are deliberately less answerable without memory: they define the task but omit exact commands, thresholds, deadlines, and implementation constraints that live only in memory.
- v2 is designed to reduce no_memory answerability by under-specifying task notes, but this is not verified by the selection-only eval; it must be checked in a later downstream response pilot.
- This remains an 8-case pilot fixture repair, not the final 30-40 case hard READ evaluation.
- This is selection-only and does not measure downstream answer quality.

## Metric Semantics

`pre_budget_selection` measures what the selector chose before the context budget is applied. `post_budget_context` measures what actually reaches the injected memory context after `max_memories` and `max_context_chars` are enforced.

`all_candidates` now means a true all-candidates context: it selects every candidate and bypasses the `top-k`/`max_memories` cap. The `max_context_chars` cap is still retained as a safety bound.

`budgeted_candidate_order` is the first-k candidate-order baseline. It is order-sensitive, not a learned selector, and is vulnerable to fixture ordering.

## Aggregate Strategy Metrics

| Strategy | Mean pre selected | Mean post injected | Pre req recall | Post req recall | Pre avoid | Post avoid | Pre stale | Post stale | Pre contradictory | Post contradictory | Pre wrong-scope | Post wrong-scope | Pre sensitive | Post sensitive | Mean context chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_candidates | 10.00 | 10.00 | 1.00 | 1.00 | 56 | 56 | 8 | 8 | 8 | 8 | 8 | 8 | 2 | 2 | 1177.25 |
| budgeted_candidate_order | 4.00 | 4.00 | 0.25 | 0.25 | 24 | 24 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 479.38 |
| keyword_top_k | 4.00 | 4.00 | 0.75 | 0.75 | 15 | 15 | 3 | 3 | 1 | 1 | 0 | 0 | 1 | 1 | 484.12 |
| no_memory | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 |
| oracle_selected | 3.00 | 3.00 | 1.00 | 1.00 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 348.38 |
| random_k | 4.00 | 4.00 | 0.44 | 0.44 | 23 | 23 | 2 | 2 | 2 | 2 | 4 | 4 | 2 | 2 | 473.25 |

## Top Case-Level Observations

- hard_read_v2_001: all_candidates selector selects 7 avoid memories pre-budget; 7 reach the all-candidates context after character budgeting.
- hard_read_v2_002: budgeted_candidate_order is order-sensitive and reaches 0.50 required recall on this candidate order.
- hard_read_v2_001: keyword_top_k required recall is 0.50 pre-budget, so lexical selection misses required memory.

## All-Candidates Contamination Examples

The all_candidates selector selects every avoid memory pre-budget. Because this strategy bypasses `top-k`, the post-budget counts below show how many avoid memories reach the injected context unless the character cap omits them.

- hard_read_v2_001: selected 7 avoid memories pre-budget; injected 7 after context budgeting.
- hard_read_v2_002: selected 7 avoid memories pre-budget; injected 7 after context budgeting.
- hard_read_v2_003: selected 7 avoid memories pre-budget; injected 7 after context budgeting.

## Keyword Top-K Failure Examples

Keyword top-k can miss required memory when a hard negative shares stronger lexical overlap with the task text. It can also select stale, contradictory, or wrong-scope memories when those candidates repeat the same service and task terms.

- hard_read_v2_001: pre required recall 0.50, post required recall 0.50; pre selected stale=1, contradictory=0, wrong_scope=0.
- hard_read_v2_002: pre required recall 0.50, post required recall 0.50; pre selected stale=1, contradictory=0, wrong_scope=0.
- hard_read_v2_003: pre required recall 1.00, post required recall 1.00; pre selected stale=0, contradictory=1, wrong_scope=0.

## Candidate-Order Baseline Note

`budgeted_candidate_order` represents the naive first-k candidate-order baseline. It is order-sensitive and should not be treated as a realistic retriever ranking.

## Limitations

- Selection metrics are diagnostic and do not measure downstream answer quality.
- This pilot is intentionally small and fixture-like to validate hard-candidate schema and selection metrics; it is not the final 30-40 case hard READ evaluation.
- Candidate ordering is a fixture property and should not be interpreted as realistic retrieval rank quality.
- Keyword retrieval is a deterministic lexical stub, not evidence about deployed retrieval behavior.
- Oracle selection uses labels and is a reference ceiling for fixture inspection only.
- No learned router, live LoRA, or saved router output is evaluated in this context.
- These results should not be used to claim downstream utility or that any learned selector outperforms baselines.

## Next Context Recommendation

Recommended next context: Context 7.4-E — v2 downstream prompt-pack scaffold and manual prompt inspection.
