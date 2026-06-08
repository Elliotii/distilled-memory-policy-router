# Hard READ Downstream Pilot Citation Scores

These are partial automatic citation metrics for scaffold validation. They are not answer-quality proof.

- Prompt count: 48
- Response count: 48
- No-response count: 0

## Strategy Aggregates

| Strategy | Prompts | Coverage | E2E required recall | Conditional required recall | Avoid avg | Stale avg | Contradictory avg | Wrong-scope avg | Hallucinated avg | Bare refs avg | Current-unit citations avg | No response |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_candidates | 8 | 1.00 | 0.81 | 0.81 | 1.12 | 0.38 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| budgeted_candidate_order | 8 | 1.00 | 0.00 | 0.00 | 2.62 | 0.00 | 0.00 | 0.75 | 0.00 | 0.00 | 0.00 | 0 |
| keyword_top_k | 8 | 1.00 | 0.31 | 0.50 | 2.38 | 0.50 | 0.62 | 0.38 | 0.00 | 0.00 | 0.00 | 0 |
| no_memory | 8 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| oracle_selected | 8 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| random_k | 8 | 1.00 | 0.31 | 0.56 | 2.38 | 0.50 | 0.25 | 0.25 | 0.00 | 0.00 | 0.00 | 0 |

## Boundary

Empty or missing responses should produce zero citation recall and full no-response counts. Manual or rubric-based review is still required for fact coverage, contamination, stale use, hallucination, task quality, and citation compliance.
