# LLM Downstream-Lite Pilot Scores

These are partial automatic citation metrics. They do not judge task response quality, answer usefulness, contradiction handling, or uncited hallucinations.

## Summary

- Prompt rows: 14
- Response rows: 14
- No-response rows: 0

## Strategy Aggregates

| Strategy | Prompts | Response coverage | End-to-end required citation recall | Conditional required citation recall | Avg irrelevant citations | Avg hallucinated citations | Avg current-unit citations | Avg bare memory refs | Avg format violations | No responses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_candidates | 2 | 1.000 | 0.667 | 0.667 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| no_memory | 2 | 1.000 | 0.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| oracle_selected | 2 | 1.000 | 0.500 | 0.500 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| random_k | 2 | 1.000 | 0.667 | 0.833 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| router_selected | 2 | 1.000 | 0.667 | 0.833 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| shuffled_top_k | 2 | 1.000 | 0.667 | 0.833 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| top_k_naive | 2 | 1.000 | 0.500 | 0.583 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 |

## Interpretation Boundary

Citation recall is a proxy for whether a response cites required memory IDs. Bare references like `m2` do not count as citations. Bracketed current-unit references like `[u2]` are diagnosed as invalid current-unit citations, not memory citations. These metrics are not full memory-fact coverage, and a response can be useful or flawed in ways this script cannot detect.
