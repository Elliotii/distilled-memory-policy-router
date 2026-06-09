# v1.0 Applied Reproducibility Guide

## Boundary

This guide reproduces the documented applied-harness artifacts from committed files. It does not require API calls, new AutoDL runs, Qwen/LoRA loading, or training for the analysis-hygiene additions.

## Key Inputs

- `reports/v10/hard_read_v2_expanded_learned_router_selection_eval/by_case.jsonl`
- `reports/v10/hard_read_v2_expanded_learned_router_selection_eval/metrics.json`
- `data/v10/hard_read_v2_expanded_downstream_subset/selected_cases.json`
- `data/v10/hard_read_v2_expanded_downstream_subset/hard_read_v2_expanded_downstream_subset_learned_router_manual_review.jsonl`
- `reports/v10/hard_read_v2_expanded_downstream_subset_with_learned_router_manual_comparison.json`

## Recomputed Reports

- `reports/v10/v1_0_applied_downstream_empty_response_sensitivity.md`
- `reports/v10/v1_0_applied_downstream_subset_selection_slice.md`
- `reports/v10/v1_0_applied_downstream_subset_selection_slice.json`

## Interpretation Checks

Confirm the final reports state that learned_router did not beat no_memory and did not beat all_candidates downstream. The high-confidence result is selection-level; the downstream 8-case result is diagnostic and not conclusive.
