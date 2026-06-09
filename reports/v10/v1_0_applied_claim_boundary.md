# v1.0 Applied Claim Boundary

## Supported

- learned_router entered the applied harness downstream subset.
- learned_router showed strong selection-level transfer on 32 hard READ cases: required recall 0.890625 versus keyword_top_k 0.453125, random_k 0.4375, and budgeted_candidate_order 0.0625.
- learned_router shows measured downstream behavior on an 8-case diagnostic subset.
- The downstream result is negative/limited: learned_router manual utility was 7.125, below no_memory 8.000 and all_candidates 8.750, and far below oracle_selected 12.000.
- Selection advantage did not robustly transfer into downstream answer utility.

## Diagnostic Interpretation

On the 8-case downstream subset, learned_router landed in the same low-to-mid utility band as keyword/random/order, with a slight mean advantage but no robust separation at this sample size. Fine ordering among these strategies is diagnostic, not conclusive.

The failure mechanism is two-dimensional: missed required memories and contradictory contamination. The subset slice had five missed-required cases and five contradictory-injection cases.

## Unsupported

- production readiness;
- READ solved;
- real retriever performance;
- real cost savings;
- general downstream utility proof;
- complete MemoryOS;
- guaranteed safety.

## Wording To Avoid

Avoid “downstream win,” “robust downstream superiority,” and any framing that buries the fact that learned_router did not beat no_memory and did not beat all_candidates.
