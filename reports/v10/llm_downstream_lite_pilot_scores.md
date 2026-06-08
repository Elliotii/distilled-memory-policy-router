# LLM Downstream-Lite Pilot Scores

These are partial automatic citation metrics. They do not judge task response quality, answer usefulness, contradiction handling, or uncited hallucinations.

## Summary

- Prompt rows: 42
- Response rows: 42
- No-response rows: 42

## Strategy Aggregates

| Strategy | Prompts | Response coverage | End-to-end required citation recall | Conditional required citation recall | Avg irrelevant citations | Avg hallucinated citations | No responses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_candidates | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6 |
| no_memory | 6 | 0.000 | 0.000 | n/a | 0.000 | 0.000 | 6 |
| oracle_selected | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6 |
| random_k | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6 |
| router_selected | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6 |
| shuffled_top_k | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6 |
| top_k_naive | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6 |

## Interpretation Boundary

Citation recall is a proxy for whether a response cites required memory IDs. It is not full memory-fact coverage, and a response can be useful or flawed in ways this script cannot detect.
