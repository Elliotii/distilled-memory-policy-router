# Hard READ Downstream Pilot Citation Scores

These are partial automatic citation metrics for scaffold validation. They are not answer-quality proof.

- Prompt count: 8
- Response count: 7
- No-response count: 1

## Strategy Aggregates

| Strategy | Prompts | Coverage | E2E required recall | Conditional required recall | Avoid avg | Stale avg | Contradictory avg | Wrong-scope avg | Hallucinated avg | Bare refs avg | Current-unit citations avg | No response |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| learned_router | 8 | 0.88 | 0.50 | 0.75 | 0.88 | 0.12 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 1 |

## Boundary

Empty or missing responses should produce zero citation recall and full no-response counts. Manual or rubric-based review is still required for fact coverage, contamination, stale use, hallucination, task quality, and citation compliance.
