# V1.0 Applied Portfolio Summary

## Headline

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

## Analysis Hygiene

The downstream result is a negative/limited transfer result, not a downstream win. The 8-case downstream review had one empty response, used an integer rubric, and is too small for robust downstream superiority claims among learned_router, keyword_top_k, random_k, and budgeted_candidate_order.

The failure mechanism is two-dimensional: missed required memories and contradictory contamination. The downstream subset selection slice had required recall 0.687500, five missed-required cases, and five contradictory-injection cases.

## Supported Claim

The project demonstrates an offline learned-router path entering the applied harness, with strong selection-level transfer on hard READ and measured but limited downstream behavior on an 8-case diagnostic subset.

## Unsupported Claims

Do not claim production readiness, READ solved, real retriever performance, real cost savings, general downstream utility proof, complete MemoryOS, or guaranteed safety.
