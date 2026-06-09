# Next Experiment Execution Order

## Principle

Close the learned-router READ gap before any v1.0-applied packaging. Keep the work offline, reproducible, and honest about negative results.

## Ordered Steps

1. Restore artifacts check
   - Confirm `results/v05g_bf16_lora/qwen35_json_r16_1000_4090/adapter` exists.
   - Confirm local `${QWEN35_MODEL_PATH}` exists.
   - Do not run inference during this check.

2. Build conversion script
   - Input hard READ expanded cases and memory pool.
   - Output v05-compatible Unit JSON case rows.
   - Preserve candidates, hard negatives, and labels.

3. Converter validation
   - JSONL parse and row count.
   - Candidate ID coverage.
   - `gold.read` ID validity.
   - Rendered prompt audit.
   - Prompt length summary.

4. Add prediction parser and replay selector
   - Add `replay_learned_router`.
   - Load saved predictions by case ID.
   - Filter invalid IDs and emit diagnostics.
   - No model loading in replay path.

5. Dry-run harness evaluation without learned predictions
   - Verify existing baselines still reproduce expanded selection metrics.
   - Verify the new selector fails closed when prediction file is absent.

6. Request explicit approval for offline inference
   - Run `src/v05/eval_lora_router.py` only after approval.
   - Use `--interface unit_json`.
   - Save predictions under a new v10 learned-router directory.

7. Replay learned-router predictions
   - Add `replay_learned_router` to strategy comparison.
   - Produce metrics and case-level diagnostics.

8. Optional semantic baseline
   - Add local embeddings only if already available.
   - Otherwise use TF-IDF fallback or defer.

9. Gap-closure report
   - Compare learned-router against baselines.
   - Include negative-result policy.
   - Recommend whether packaging can resume or whether READ architecture needs another step.

10. Packaging decision
   - Resume v1.0-applied packaging only after the learned-router gap closure report exists.
   - Do not create a tag unless explicitly requested.

## v1.1 Future Work

Live serving, real retriever integration, and trace viewer/UI work should remain v1.1 future work until offline replay results are understood.

