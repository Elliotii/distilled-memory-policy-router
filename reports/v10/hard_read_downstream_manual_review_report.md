# Hard READ Downstream Internal Rubric Review

## Review Method

This is an internal rubric review of the 24 DeepSeek responses collected for the hard READ downstream micro-pilot. It is useful for diagnosis, but it is not a formal benchmark and should not be described as a human evaluation.

Each response was scored on six 0/1/2 dimensions: required fact coverage, irrelevant-memory contamination, stale or contradictory use, hallucinated memory use, task response quality, and citation compliance. `manual_utility` is the sum of those six fields.

## Strategy Aggregates

| Strategy | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Halluc clean | Quality | Citation | Auto req recall | Auto avoid avg | Auto stale avg | Auto contradictory avg | Strong | Missing req | Irrelevant flags | Stale/contrad flags |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `all_candidates` | 4 | 7.50 | 2.00 | 0.25 | 0.50 | 2.00 | 0.75 | 2.00 | 1.00 | 2.00 | 0.75 | 0.75 | 0 | 0 | 4 | 4 |
| `budgeted_candidate_order` | 4 | 11.75 | 2.00 | 1.75 | 2.00 | 2.00 | 2.00 | 2.00 | 1.00 | 0.25 | 0.00 | 0.00 | 3 | 0 | 1 | 0 |
| `keyword_top_k` | 4 | 7.50 | 1.00 | 0.75 | 1.00 | 2.00 | 0.75 | 2.00 | 0.50 | 1.75 | 0.50 | 0.50 | 0 | 3 | 3 | 2 |
| `no_memory` | 4 | 10.25 | 1.00 | 2.00 | 2.00 | 2.00 | 1.25 | 2.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 4 | 0 | 0 |
| `oracle_selected` | 4 | 12.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 1.00 | 0.00 | 0.00 | 0.00 | 4 | 0 | 0 | 0 |
| `random_k` | 4 | 8.00 | 1.00 | 0.75 | 1.25 | 2.00 | 1.00 | 2.00 | 0.50 | 1.25 | 0.50 | 0.25 | 0 | 3 | 3 | 3 |

## Case Aggregates

| Case | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Quality | Strong | Missing req |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hard_read_pilot_001` | 6 | 10.00 | 1.83 | 1.00 | 1.67 | 1.50 | 1 | 1 |
| `hard_read_pilot_002` | 6 | 9.17 | 1.50 | 1.17 | 1.17 | 1.33 | 2 | 3 |
| `hard_read_pilot_003` | 6 | 9.00 | 1.33 | 1.33 | 1.33 | 1.00 | 2 | 3 |
| `hard_read_pilot_009` | 6 | 9.83 | 1.33 | 1.50 | 1.67 | 1.33 | 2 | 3 |

## Notable Observations

- `oracle_selected` is the cleanest reference condition in this micro-pilot: it has full rubric utility and no contamination flags.
- `budgeted_candidate_order` is strong on these four selected cases, but the selection report notes that candidate order is structured and should not be treated as a realistic retriever ranking.
- `all_candidates` recovers required facts but exposes contamination risk by giving the answerer stale, contradictory, and irrelevant memories.
- `keyword_top_k` shows the hard-negative failure mode most clearly: lexical overlap can retrieve stale or contradictory memories while missing required ones.
- `no_memory` responses are usually clean but under-specified when important details live only in prior memory context.

## Examples

### Strong oracle_selected response

- Prompt: `hard_read_pilot_001__oracle_selected`
- Utility: 12
- Notes: Cleanly covers backoff, the exact test command, and helpful logging detail without irrelevant contamination.

```text
- Use exponential backoff with jitter for payment-gateway retries [m001].  
- Run `make test-checkout` in the shopflow repo before opening the PR [m002].  
- Add `retry_count` and `payment_gateway_status` fields to retry logs [m003].
```

### All-candidates contamination example

- Prompt: `hard_read_pilot_002__all_candidates`
- Utility: 6
- Notes: Covers required retention and test facts, but adopts the contradictory instruction to keep bundles indefinitely and cites stale/token-related avoid memories.

```text
- Enforce the EU retention deadline of 30 days [m009].  
- Include deletion audit logging for generated bundles [m011] and keep bundles indefinitely for audit convenience [m014].  
- Run `python -m pytest tests/privacy_export` before merging [m010].  
- Do not store or reuse the sample token from the old incident note [m013][m016].
```

### Keyword top-k failure example

- Prompt: `hard_read_pilot_003__keyword_top_k`
- Utility: 4
- Notes: Misses the required aria-label and exact visual test facts and uses the contradictory hide-focus-rings memory as if it were valid. It mostly demonstrates hard-negative contamination.

```text
- Use the repo command to run visual regression tests for the updated accessibility checks, ensuring no unintended visual changes.  
- Implement the requirement to hide keyboard focus rings in the accessibility checks, aligning with the old visual spec [m022].  
- Note that the previous contrast incident [m021] is resolved and should not influence these updates. Additionally, earlier accessibility discussions [m024] applied only to a deprecated theme and are not relevant.
```

### No-memory under-specified example

- Prompt: `hard_read_pilot_002__no_memory`
- Utility: 11
- Notes: Uses current task notes well and avoids token reuse, but misses the required pytest command supplied only by memory.

```text
- Prepare the analytics-worker service for the privacy export job, ensuring all configurations support the export.
- Keep the EU retention deadline prominently visible in the plan to ensure compliance.
- The sample token from the incident note must not be stored or reused in any part of the worker.
```

## Limitations

- This is an internal rubric review, not a formal benchmark.
- The review covers only 24 responses from four hard READ cases and six strategies.
- The response review does not evaluate learned router/live LoRA behavior.
- The review does not prove downstream utility or production safety.
- The automatic citation metrics and internal rubric scores should be used as diagnostic evidence only.
