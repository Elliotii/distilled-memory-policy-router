# v1.0 Applied Downstream Subset Selection Slice

This report computes learned_router selection metrics only for the 8 case IDs used in the downstream subset. It uses existing replay evaluation artifacts and does not rerun models or APIs.

## Aggregate Slice Metrics

| metric | value |
| --- | ---: |
| case count | 8 |
| mean required recall | 0.687500 |
| mean injected count | 3.125 |
| total avoid injected | 8 |
| total contradictory injected | 5 |
| total stale injected | 1 |
| total wrong_scope injected | 0 |
| total sensitive_boundary injected | 0 |

## Missed Required And Contradictory Cases

- Cases with missed required memories: hard_read_v2_026, hard_read_v2_011, hard_read_v2_020, hard_read_v2_031, hard_read_v2_032
- Cases with contradictory injections: hard_read_v2_009, hard_read_v2_026, hard_read_v2_011, hard_read_v2_013, hard_read_v2_031

## By Case

| case | required recall | injected | avoid | contradictory | stale | wrong_scope | sensitive_boundary |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hard_read_v2_009` | 1.00 | 4 | 1 | 1 | 0 | 0 | 0 |
| `hard_read_v2_026` | 0.50 | 3 | 1 | 1 | 0 | 0 | 0 |
| `hard_read_v2_011` | 0.50 | 4 | 2 | 1 | 1 | 0 | 0 |
| `hard_read_v2_020` | 0.50 | 3 | 1 | 0 | 0 | 0 | 0 |
| `hard_read_v2_013` | 1.00 | 3 | 1 | 1 | 0 | 0 | 0 |
| `hard_read_v2_014` | 1.00 | 2 | 0 | 0 | 0 | 0 | 0 |
| `hard_read_v2_031` | 0.50 | 3 | 1 | 1 | 0 | 0 | 0 |
| `hard_read_v2_032` | 0.50 | 3 | 1 | 0 | 0 | 0 | 0 |

## Interpretation

The full 32-case selection-level result is high-confidence for selection transfer: learned_router required recall is 0.890625, compared with keyword_top_k 0.453125, random_k 0.4375, and budgeted_candidate_order 0.0625. The 8-case downstream slice is lower at 0.6875 required recall and concentrates both missed required memories and contradictory contamination. This explains why downstream answer utility did not robustly follow from the full-slice selection advantage.

Failure mechanism is two-dimensional: missed required memories and contradictory memory contamination. When the downstream reader is strong, extra non-contradictory noise may be less damaging than missing required facts or injecting contradictions. This explains why all_candidates can outperform learned_router despite much higher avoid-memory injection.
