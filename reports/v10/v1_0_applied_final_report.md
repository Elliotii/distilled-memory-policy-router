# v1.0 Applied Final Report

## Headline Result

learned_router showed strong selection-level transfer on 32 hard READ cases, but in the 8-case downstream manual review it scored below no_memory and all_candidates; therefore selection advantage did not robustly transfer into downstream answer utility.

## Core Metrics

High-confidence selection-level result on 32 cases:

| strategy | required recall |
| --- | ---: |
| learned_router | 0.890625 |
| keyword_top_k | 0.453125 |
| random_k | 0.437500 |
| budgeted_candidate_order | 0.062500 |

Low-confidence diagnostic downstream result on 8 cases:

| strategy | manual utility |
| --- | ---: |
| oracle_selected | 12.000 |
| all_candidates | 8.750 |
| no_memory | 8.000 |
| learned_router | 7.125 |
| random_k | 6.875 |
| keyword_top_k | 6.500 |
| budgeted_candidate_order | 6.500 |

On the 8-case downstream subset, learned_router landed in the same low-to-mid utility band as keyword/random/order, with a slight mean advantage but no robust separation at this sample size. learned_router did not beat no_memory and did not beat all_candidates.

## Downstream Sensitivity

The primary learned_router manual utility is 7.125 including all 8 rows. Excluding the empty response (`hard_read_v2_009__learned_router` / `hard_read_v2_009`) raises learned_router to 7.286, still below no_memory at 8.000. This sensitivity does not replace the audited all-row metric.

## Downstream Slice Selection

The downstream 8-case slice is harder than the full 32-case selection set for learned_router. Slice required recall is 0.687500; mean injected count is 3.125; avoid injected is 8; contradictory injected is 5; stale injected is 1; wrong_scope and sensitive_boundary are both 0.

Missed required cases: hard_read_v2_026, hard_read_v2_011, hard_read_v2_020, hard_read_v2_031, hard_read_v2_032. Contradictory injection cases: hard_read_v2_009, hard_read_v2_026, hard_read_v2_011, hard_read_v2_013, hard_read_v2_031.

## Interpretation

Selection-level transfer is the high-confidence result: 32 cases, clear recall separation over keyword_top_k, random_k, and budgeted_candidate_order. Downstream transfer is low-confidence and diagnostic: 8 cases, one empty response, integer rubric, and close low-to-mid utility scores among learned_router/keyword/random/order.

The downstream weakness is not only contradictory contamination. It is missed required memories plus contradictory memory contamination. When the downstream reader is strong, extra non-contradictory noise may be less damaging than missing required facts or injecting contradictions. This explains why all_candidates can outperform learned_router despite much higher avoid-memory injection.

## Claim Boundary

This report supports only a bounded applied-harness diagnostic claim. It does not support production readiness, READ solved, real retriever performance, real cost savings, broad downstream utility proof, complete MemoryOS, or guaranteed safety.
