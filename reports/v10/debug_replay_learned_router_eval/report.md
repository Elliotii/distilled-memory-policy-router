# Hard READ Selection Pilot Report

Context: hard READ pilot fixture selection-only evaluation.

This report evaluates memory selection only. It does not run a downstream answerer, call an API, load Qwen or LoRA, or evaluate learned router/live LoRA behavior.

Learned router/live LoRA is not evaluated because no real backend output is available for these hard-read cases.

## Run Summary

- Case count: 32
- Memory pool count: 320
- Strategies evaluated: replay_learned_router

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
| replay_learned_router | 1.00 | 1.00 | 0.02 | 0.02 | 31 | 31 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 116.31 |

## Top Case-Level Observations


## All-Candidates Contamination Examples

The all_candidates selector selects every avoid memory pre-budget. Because this strategy bypasses `top-k`, the post-budget counts below show how many avoid memories reach the injected context unless the character cap omits them.


## Keyword Top-K Failure Examples

Keyword top-k can miss required memory when a hard negative shares stronger lexical overlap with the task text. It can also select stale, contradictory, or wrong-scope memories when those candidates repeat the same service and task terms.


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
