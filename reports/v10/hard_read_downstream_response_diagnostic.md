# Hard READ Downstream Response Diagnostic

Context: 7.4-B-S hard READ downstream DeepSeek micro-pilot token-budget repair.

## Issue And Repair Summary

- Context 7.4-B produced 24 API OK rows, 14 nonempty responses, and 10 empty OK responses.
- Context 7.4-B-R added sanitized row-level diagnostics and retry-on-empty. It improved coverage to 18 usable responses, but 6 empty OK rows remained.
- B-R diagnosed the remaining empty OK rows as `finish_reason: length` with `content_length: 0` and `reasoning_tokens: 220`, meaning the configured 220-token completion budget was exhausted before final content appeared.
- Context 7.4-B-S strengthened the system instruction to request only final answers and reran the same 24 prompt pack with `max_tokens=600` and `retry_empty=2`.
- The prompt pack, labels, metadata, cases, and scoring script were not changed.

## Final API Counts

- Total rows: 24
- API OK rows: 24
- API error rows: 0
- Usable nonempty responses: 24
- Empty OK responses: 0
- Rows retried at least once: 2

## Response Diagnostics

| Finish reason | Rows |
| --- | ---: |
| `length` | 1 |
| `stop` | 23 |

| Retry count | Rows |
| ---: | ---: |
| 0 | 22 |
| 1 | 1 |
| 2 | 1 |

No empty OK rows remain after the B-S rerun.

Some usable responses still ended with `finish_reason: length`, so manual review should still check whether those answers are truncated:

| Prompt | Retry count | Content length | Reasoning tokens |
| --- | ---: | ---: | ---: |
| `hard_read_pilot_009__keyword_top_k` | 1 | 225 | 552 |

## Strategy-Level Citation Metrics

These are automatic citation diagnostics only. They do not measure complete answer quality, required fact coverage, stale fact use, or usefulness to a downstream agent.

| Strategy | Prompts | Coverage | E2E required recall | Conditional required recall | Avoid avg | Stale avg | Contradictory avg | Wrong-scope avg | Hallucinated avg | Bare refs avg | Current-unit citations avg | No response |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `all_candidates` | 4 | 1.00 | 1.00 | 1.00 | 2.00 | 0.75 | 0.75 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| `budgeted_candidate_order` | 4 | 1.00 | 1.00 | 1.00 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| `keyword_top_k` | 4 | 1.00 | 0.50 | 0.62 | 1.75 | 0.50 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| `no_memory` | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| `oracle_selected` | 4 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| `random_k` | 4 | 1.00 | 0.50 | 0.75 | 1.25 | 0.50 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |

## Diagnostic Observations

- Increasing `max_tokens` from 220 to 600 and strengthening the final-answer-only system instruction repaired usable response coverage from 18/24 to 24/24.
- Citation formatting remains clean in the automatic scorer: no hallucinated memory citations, no bare memory references, and no current-unit citations were detected.
- `oracle_selected` and `budgeted_candidate_order` reached full required-memory citation recall in this automatic citation pass.
- `all_candidates`, `keyword_top_k`, and `random_k` show avoid/stale/contradictory citation contamination, which is expected to be important for hard-negative READ diagnosis.
- The automatic metrics are sensitive to citation behavior and do not establish answer quality or task utility.

## Claim Boundaries

- This is a 24-response micro-pilot only.
- Metrics are automatic citation diagnostics only.
- Manual or rubric-based review is still required before making answer-quality claims.
- The run did not evaluate learned router or live LoRA behavior.
- The run does not prove downstream utility.
- The run makes no claim that any router or selector outperforms alternatives.
