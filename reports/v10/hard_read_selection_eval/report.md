# Hard READ Selection Pilot Report

Context: 7.3 hard READ pilot fixture expansion and selection-only evaluation.

This report evaluates memory selection only. It does not run a downstream answerer, call an API, load Qwen or LoRA, or evaluate learned router/live LoRA behavior.

Learned router/live LoRA is not evaluated in 7.3 because no real backend output is available for these new hard-read cases.

## Run Summary

- Case count: 10
- Memory pool count: 80
- Strategies evaluated: no_memory, all_candidates, budgeted_candidate_order, keyword_top_k, random_k, oracle_selected

## Metric Semantics

`pre_budget_selection` measures what the selector chose before the context budget is applied. `post_budget_context` measures what actually reaches the injected memory context after `max_memories` and `max_context_chars` are enforced.

`all_candidates` now means a true all-candidates context: it selects every candidate and bypasses the `top-k`/`max_memories` cap. The `max_context_chars` cap is still retained as a safety bound.

`budgeted_candidate_order` is the first-k candidate-order baseline. It is order-sensitive, not a learned selector, and is vulnerable to fixture ordering.

## Aggregate Strategy Metrics

| Strategy | Mean pre selected | Mean post injected | Pre req recall | Post req recall | Pre avoid | Post avoid | Pre stale | Post stale | Pre contradictory | Post contradictory | Pre wrong-scope | Post wrong-scope | Pre sensitive | Post sensitive | Mean context chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_candidates | 8.00 | 8.00 | 1.00 | 1.00 | 50 | 50 | 10 | 10 | 10 | 10 | 10 | 10 | 3 | 3 | 913.90 |
| budgeted_candidate_order | 4.00 | 4.00 | 1.00 | 1.00 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 459.50 |
| keyword_top_k | 4.00 | 4.00 | 0.65 | 0.65 | 26 | 26 | 8 | 8 | 4 | 4 | 0 | 0 | 3 | 3 | 469.20 |
| no_memory | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 |
| oracle_selected | 3.00 | 3.00 | 1.00 | 1.00 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 334.70 |
| random_k | 4.00 | 4.00 | 0.50 | 0.50 | 25 | 25 | 4 | 4 | 2 | 2 | 6 | 6 | 3 | 3 | 456.40 |

## Top Case-Level Observations

- hard_read_pilot_001: all_candidates selector selects 5 avoid memories pre-budget; 5 reach the all-candidates context after character budgeting.
- hard_read_pilot_001: budgeted_candidate_order is order-sensitive and reaches 1.00 required recall on this structured fixture order.
- hard_read_pilot_003: keyword_top_k required recall is 0.00 pre-budget, so lexical selection misses required memory.

## All-Candidates Contamination Examples

The all_candidates selector selects every avoid memory pre-budget. Because this strategy bypasses `top-k`, the post-budget counts below show how many avoid memories reach the injected context unless the character cap omits them.

- hard_read_pilot_001: selected 5 avoid memories pre-budget; injected 5 after context budgeting.
- hard_read_pilot_002: selected 5 avoid memories pre-budget; injected 5 after context budgeting.
- hard_read_pilot_003: selected 5 avoid memories pre-budget; injected 5 after context budgeting.

## Keyword Top-K Failure Examples

Keyword top-k can miss required memory when a hard negative shares stronger lexical overlap with the task text. It can also select stale, contradictory, or wrong-scope memories when those candidates repeat the same service and task terms.

- hard_read_pilot_003: pre required recall 0.00, post required recall 0.00; pre selected stale=1, contradictory=1, wrong_scope=0.
- hard_read_pilot_002: pre required recall 0.50, post required recall 0.50; pre selected stale=1, contradictory=1, wrong_scope=0.
- hard_read_pilot_004: pre required recall 0.50, post required recall 0.50; pre selected stale=1, contradictory=1, wrong_scope=0.

## Candidate-Order Baseline Note

`budgeted_candidate_order` represents the naive first-k candidate-order baseline. The pilot candidate order is structured and should not be treated as a realistic retriever ranking.

## Limitations

- Selection metrics are diagnostic and do not measure downstream answer quality.
- The 10-case pilot is intentionally structured/template-like to validate hard-candidate schema and selection metrics; it is not the final 30-40 case hard READ evaluation.
- Pilot candidate ordering is structured and should not be interpreted as realistic retrieval rank quality.
- Keyword retrieval is a deterministic lexical stub, not evidence about deployed retrieval behavior.
- Oracle selection uses labels and is a reference ceiling for fixture inspection only.
- No learned router, live LoRA, or saved router output is evaluated in this context.
- These results should not be used to claim downstream utility or that any learned selector outperforms baselines.

## Next Context Recommendation

Recommended next context: Context 7.4 - Downstream LLM response collection for selected hard READ pilot subset, after reviewing whether these fixtures are strong enough for answer-quality scoring.
