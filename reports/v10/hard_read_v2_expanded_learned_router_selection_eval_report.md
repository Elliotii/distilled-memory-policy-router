# Hard READ v2 Expanded Learned-Router Selection Eval Report

## Run Boundary

This report formalizes a selection-level result only.

- Real v0.5g offline batch prediction ran on AutoDL.
- The Mac harness replayed those saved predictions using `replay_learned_router`.
- This context did not call a downstream API.
- This context did not run DeepSeek or any external LLM.
- This context did not run new AutoDL inference, load Qwen/LoRA locally, train, serve a live backend, or build UI.

## Prediction Provenance

- Prediction source: `v0.5g_offline_batch_prediction`
- Prediction rows: 32
- Debug fixture used: no
- Run report: `reports/v10/v0_5g_offline_prediction_run_report.md`
- Replay eval output: `reports/v10/hard_read_v2_expanded_learned_router_selection_eval/`

The imported prediction JSONL contains one row per hard READ v2 expanded case. The replay selector used the saved `selected_memory_ids` only; it did not call a model.

## Parse Summary

| item | value |
| --- | ---: |
| prediction rows | 32 |
| `parse_status=ok` | 32 |
| empty selected-memory predictions | 0 |
| selected count = 2 | 3 |
| selected count = 3 | 20 |
| selected count = 4 | 7 |
| selected count = 5 | 2 |

## Learned-Router Selection Metrics

| metric | value |
| --- | ---: |
| case count | 32 |
| mean pre required recall | 0.90625 |
| mean post required recall | 0.890625 |
| mean pre selected count | 3.25 |
| mean post injected count | 3.1875 |
| mean context chars | 362.84375 |
| total post avoid injected | 25 |
| total post stale injected | 2 |
| total post contradictory injected | 19 |
| total post wrong-scope injected | 0 |
| total post sensitive-boundary injected | 0 |

The slight pre/post recall difference comes from the harness context budget stage after replay selection.

## Baseline Comparison

| strategy | mean post required recall | mean post injected count | total avoid injected | total stale injected | total contradictory injected | total wrong-scope injected | total sensitive-boundary injected |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 0.000000 | 0.0000 | 0 | 0 | 0 | 0 | 0 |
| `all_candidates` | 1.000000 | 10.0000 | 224 | 32 | 32 | 32 | 13 |
| `budgeted_candidate_order` | 0.062500 | 4.0000 | 96 | 2 | 2 | 25 | 1 |
| `keyword_top_k` | 0.453125 | 4.0000 | 73 | 14 | 14 | 6 | 4 |
| `random_k` | 0.437500 | 4.0000 | 90 | 14 | 10 | 14 | 7 |
| `oracle_selected` | 1.000000 | 3.0000 | 0 | 0 | 0 | 0 | 0 |
| `replay_learned_router` | 0.890625 | 3.1875 | 25 | 2 | 19 | 0 | 0 |

## Interpretation

At selection level, `replay_learned_router` is much stronger than `keyword_top_k`, `random_k`, and `budgeted_candidate_order` on required-memory recall. It is also much less contaminated than `all_candidates`, which reaches full recall only by injecting every avoid memory as well.

The learned router is still below `oracle_selected`. It misses one required memory in 7 cases and injects contradictory memories in 19 cases. That contradictory contamination is nontrivial and must be checked in downstream response tests before making any answer-quality claim.

## Claim Boundary

- This is selection-level evidence only.
- This is not downstream utility proof.
- READ is not solved.
- This is not a production claim.
- This is not a real retriever claim.
- Negative downstream results must be reported directly if contradictory contamination hurts answer quality.
