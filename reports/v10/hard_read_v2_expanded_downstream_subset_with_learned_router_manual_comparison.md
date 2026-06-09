# Hard READ v2 Expanded Manual Comparison With Learned Router

This report combines the existing six-strategy manual review with the 8-row learned_router manual review. No APIs or model inference were run in this context.

## Seven-Strategy Manual Table

| Strategy | Count | Mean utility | Req facts | Irrelevant clean | Stale/contrad clean | Hallucination clean | Quality | Citation | Missing req | Material contamination | Stale/contrad material | No response |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 8 | 8.000 | 0.000 | 2.000 | 2.000 | 2.000 | 0.000 | 2.000 | 8 | 0 | 0 | 0 |
| `all_candidates` | 8 | 8.750 | 1.625 | 1.375 | 1.250 | 2.000 | 0.875 | 1.625 | 3 | 3 | 4 | 0 |
| `budgeted_candidate_order` | 8 | 6.500 | 0.625 | 0.375 | 1.250 | 1.875 | 0.375 | 2.000 | 8 | 8 | 4 | 0 |
| `keyword_top_k` | 8 | 6.500 | 0.625 | 0.625 | 0.625 | 2.000 | 0.625 | 2.000 | 7 | 7 | 7 | 0 |
| `random_k` | 8 | 6.875 | 0.875 | 0.875 | 0.750 | 2.000 | 0.625 | 1.750 | 7 | 6 | 6 | 0 |
| `oracle_selected` | 8 | 12.000 | 2.000 | 2.000 | 2.000 | 2.000 | 2.000 | 2.000 | 0 | 0 | 0 | 0 |
| `learned_router` | 8 | 7.125 | 0.750 | 0.875 | 1.125 | 2.000 | 0.625 | 1.750 | 7 | 3 | 3 | 1 |

## Manual Interpretation

- `learned_router` scores 7.125 mean utility, above `keyword_top_k` and `budgeted_candidate_order` at 6.500 and above `random_k` at 6.875.
- `learned_router` is below `no_memory` at 8.000 because no_memory is clean but generic, while learned_router had one empty response and several harmful contradiction uses.
- `learned_router` is below `all_candidates` at 8.750 and well below `oracle_selected` at 12.000.
- Material contradiction use appears in three learned_router rows, and one additional row cites stale/contradictory memories only to reject them.

## Boundary

This is an eight-case downstream rubric comparison. It supports only a bounded diagnostic claim about these prompts and responses. It does not establish production readiness, solve READ, or prove general downstream utility.
