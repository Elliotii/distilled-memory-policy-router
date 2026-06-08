# Hard READ Downstream Pilot Citation Scores

These are partial automatic citation metrics for scaffold validation. They are not answer-quality proof.

- Prompt count: 30
- Response count: 0
- No-response count: 30

## Strategy Aggregates

| Strategy | Prompts | Coverage | E2E required recall | Conditional required recall | Avoid avg | Stale avg | Contradictory avg | Wrong-scope avg | Hallucinated avg | Bare refs avg | Current-unit citations avg | No response |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_candidates | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 5 |
| budgeted_candidate_order | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 5 |
| keyword_top_k | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 5 |
| no_memory | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 5 |
| oracle_selected | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 5 |
| random_k | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 5 |

## Boundary

Empty or missing responses should produce zero citation recall and full no-response counts. Manual or rubric-based review is still required for fact coverage, contamination, stale use, hallucination, task quality, and citation compliance.
