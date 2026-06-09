# Learned-Router Baseline Comparison

This comparison is selection-level only. It combines the existing expanded baseline metrics with the real AutoDL-produced v0.5g prediction replay under `replay_learned_router`.

| strategy | mean post required recall | mean post injected count | total avoid injected | total stale injected | total contradictory injected | total wrong-scope injected | total sensitive-boundary injected | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `no_memory` | 0.000000 | 0.0000 | 0 | 0 | 0 | 0 | 0 | No contamination, but no required-memory recall. |
| `all_candidates` | 1.000000 | 10.0000 | 224 | 32 | 32 | 32 | 13 | Full recall by injecting every candidate; heavy contamination. |
| `budgeted_candidate_order` | 0.062500 | 4.0000 | 96 | 2 | 2 | 25 | 1 | Shows candidate-order stress failure, especially wrong-scope injection. |
| `keyword_top_k` | 0.453125 | 4.0000 | 73 | 14 | 14 | 6 | 4 | Lexical baseline misses many required memories and still injects hard negatives. |
| `random_k` | 0.437500 | 4.0000 | 90 | 14 | 10 | 14 | 7 | Random budgeted context performs near keyword recall but with broad contamination. |
| `oracle_selected` | 1.000000 | 3.0000 | 0 | 0 | 0 | 0 | 0 | Label ceiling for fixture inspection, not a deployable selector. |
| `replay_learned_router` | 0.890625 | 3.1875 | 25 | 2 | 19 | 0 | 0 | High recall with compact context, but contradictory contamination remains a downstream risk. |

The learned router is materially stronger than `keyword_top_k`, `random_k`, and `budgeted_candidate_order` for required-memory recall, and it avoids the broad contamination of `all_candidates`. It is still below `oracle_selected`, and the 19 contradictory injections are the main risk to inspect in downstream response evaluation.

Boundary: this table does not prove downstream answer quality, production readiness, or end-to-end retrieval quality.
