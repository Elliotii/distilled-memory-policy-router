# V1.0 Applied Artifact Map

## Project Thesis

This repository studies a narrow memory-policy router for coding/business-agent contexts. The router decides which fixed candidate memories to read and which current units to store or skip. It is not a retriever, MemoryOS, database, writer, or production agent.

## Final Headline

learned_router showed strong selection-level transfer on 32 hard READ cases, but downstream utility did not beat no_memory or all_candidates in the 8-case manual review. The downstream failure mechanism is two-dimensional: missed required memories plus contradictory contamination. Selection advantage did not robustly transfer into downstream answer utility.

## Confidence-Tiered Result

High-confidence selection-level result on 32 cases:

| strategy | required recall |
| --- | ---: |
| learned_router | 0.890625 |
| keyword_top_k | 0.453125 |
| random_k | 0.4375 |
| budgeted_candidate_order | 0.0625 |

Low-confidence diagnostic downstream result on 8 cases:

| strategy | manual utility |
| --- | ---: |
| oracle_selected | 12.000 |
| all_candidates | 8.750 |
| no_memory | 8.000 |
| learned_router | 7.125 |

Excluding the empty response raises learned_router to 7.286, still below no_memory. The downstream 8-case selection slice had required recall 0.6875, avoid injected 8, contradictory injected 5, stale injected 1, and wrong_scope/sensitive_boundary 0.

## Ordered Reading Path

1. Thesis/design docs.
2. v0.5g locked eval.
3. Applied harness skeleton.
4. Hard READ expanded fixture.
5. Offline learned_router prediction.
6. 32-case selection comparison.
7. 8-case downstream auto/manual review.
8. Empty-response sensitivity and downstream-slice selection analysis.
9. Final claim boundary.

## Artifact Table

| artifact path | purpose | key result | safe claim supported | claim not supported |
| --- | --- | --- | --- | --- |
| `docs/planning/lightweight_memory_policy_router_project_spec.md` | Project scope and MVP boundary | Defines the router as a narrow policy layer | Scope is fixed to memory policy routing | Complete agent or MemoryOS |
| `docs/V1_0_APPLIED_PORTFOLIO_SUMMARY.md` | Short portfolio-facing summary | Selection success but negative/limited downstream transfer | Applied-harness diagnostic result | downstream win or robust downstream superiority |
| `reports/v10/v1_0_applied_final_report.md` | Final applied report | learned_router 7.125 below no_memory 8.000 and all_candidates 8.750 | Selection-level transfer plus bounded downstream diagnostic | General downstream utility proof |
| `reports/v10/v1_0_applied_claim_boundary.md` | Explicit supported/unsupported claims | Fine ordering among learned_router/keyword/random/order is diagnostic, not conclusive | Conservative claim language | READ solved or production readiness |
| `reports/v10/v1_0_applied_reproducibility_guide.md` | How to inspect committed evidence | Analysis can be reviewed without secrets or GPU | Reproducible artifact inspection | Re-running model training or inference |
| `reports/v10/v1_0_applied_final_readiness_checklist.md` | Final readiness checklist | Confirms negative/limited downstream interpretation | Packaging readiness with limits | Product release readiness |
| `reports/v10/v0_5g_offline_prediction_run_report.md` | Offline prediction provenance | 32 v0.5g offline prediction rows, parse OK | Real offline learned_router predictions were materialized | Live serving or API-backed router |
| `data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl` | Saved learned_router predictions | Source is `v0.5g_offline_batch_prediction` | Replay can be audited without model weights | New inference or model-weight availability |
| `reports/v10/hard_read_v2_expanded_learned_router_selection_eval_report.md` | 32-case selection comparison | learned_router recall 0.890625 vs keyword_top_k 0.453125 | High-confidence selection-level success | Downstream answer utility |
| `reports/v10/hard_read_v2_expanded_downstream_subset_with_learned_router_manual_comparison.md` | 7-strategy manual downstream comparison | learned_router 7.125, no_memory 8.000, all_candidates 8.750, oracle_selected 12.000 | Measured 8-case downstream behavior | Robust downstream ranking |
| `reports/v10/hard_read_v2_expanded_downstream_subset_learned_router_rubric_synthesis.md` | Manual-review synthesis | Contradictions materially hurt several responses | Failure diagnosis | Broad utility proof |
| `reports/v10/v1_0_applied_downstream_empty_response_sensitivity.md` | Empty-response sensitivity | Excluding empty response gives 7.286, still below no_memory | Empty response is not the sole explanation | Replacing the primary audited metric |
| `reports/v10/v1_0_applied_downstream_subset_selection_slice.md` | 8-case selection slice | Required recall 0.6875 with missed required and contradictory injections | Downstream slice was harder than aggregate | Treating 32-case recall as downstream-slice recall |
| `reports/v10/v1_0_applied_downstream_subset_selection_slice.json` | Machine-readable slice metrics | Same slice metrics in JSON | Programmatic consistency check | New experiment |

## Packaging Boundary

Model weights/adapters are not packaged. AutoDL inference has already been materialized into saved prediction JSONL. Reviewing the committed evidence does not require secrets, API keys, SSH credentials, GPU access, Qwen/LoRA loading, or new external API calls.

## Final Interpretation

The v1.0-applied package is ready as a research-engineering artifact with a conservative conclusion: selection-level transfer is strong, downstream transfer is negative/limited, and the main downstream failure modes are missed required memories and contradictory contamination.
