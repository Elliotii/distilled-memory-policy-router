# Hard READ Downstream Pilot Citation Scores

These are partial automatic citation metrics for scaffold validation. They are not answer-quality proof.

- Prompt count: 30
- Response count: 30
- No-response count: 0

## Strategy Aggregates

| Strategy | Prompts | Coverage | E2E required recall | Conditional required recall | Avoid avg | Stale avg | Contradictory avg | Wrong-scope avg | Hallucinated avg | Bare refs avg | Current-unit citations avg | No response |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_candidates | 5 | 1.00 | 0.90 | 0.90 | 1.80 | 0.40 | 0.80 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| budgeted_candidate_order | 5 | 1.00 | 0.20 | 0.40 | 1.80 | 0.20 | 0.20 | 0.20 | 0.00 | 0.00 | 0.00 | 0 |
| keyword_top_k | 5 | 1.00 | 0.80 | 1.00 | 1.40 | 0.60 | 0.20 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| no_memory | 5 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| oracle_selected | 5 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 |
| random_k | 5 | 1.00 | 0.40 | 0.80 | 2.20 | 0.40 | 0.00 | 0.20 | 0.00 | 0.00 | 0.00 | 0 |

## Boundary

Empty or missing responses should produce zero citation recall and full no-response counts. Manual or rubric-based review is still required for fact coverage, contamination, stale use, hallucination, task quality, and citation compliance.
