# Offline Learned-Router READ Evaluation Feasibility Audit

## Scope

This audit checks whether the trained v0.5g router can be evaluated offline on the hard READ v2 expanded fixture, saved as prediction JSONL, and replayed inside the Applied Memory Harness as a learned-router strategy.

No API was called. No model was loaded. No Qwen or LoRA inference was run. No training, live serving, UI work, or tag creation was performed.

## Feasibility Summary

Offline learned-router READ evaluation is feasible in design, but not immediately runnable from this checkout alone.

The blocking issue is artifact availability: the v0.5g reports document the adapter directories under `results/v05g_bf16_lora/.../adapter`, but this checkout currently has no adapter files under `results/`. The documented final adapter to use is:

```text
results/v05g_bf16_lora/qwen35_json_r16_1000_4090/adapter
```

The config also requires a local base model path:

```text
${QWEN35_MODEL_PATH}
```

Once the adapter artifact and local base model are available, the remaining work is ordinary offline batch prediction plumbing.

## v0.5g Artifact Availability

| Item | Evidence | Current audit status |
| --- | --- | --- |
| Best v0.5g config | `configs/v05g/qwen35_bf16_lora_json_r16_1000_4090.yaml` | Present. |
| Best adapter path | `results/v05g_bf16_lora/qwen35_json_r16_1000_4090/adapter` | Documented but not present in this checkout. |
| Adapter manifest | `reports/v05g/v05g_bf16_lora_4090_artifact_manifest.md` | Present; says adapter directory is about 57 MB and includes `adapter_model.safetensors`. |
| Training data lock | `data/v05g/v05g_training_data_lock.json` | Present. |
| Saved predictions | `data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl` | Present. |
| Metrics | `reports/v05g/server_runs/v05g_bf16_r16_1000_4090_gold_v2_009_metrics.json` | Present. |
| Inference script | `src/v05/eval_lora_router.py` | Present; loads local base model and PEFT adapter. |
| Metrics bridge | `src/v05/evaluate_lora_predictions.py` | Present; evaluates `raw_output` unit JSON predictions. |

## Known v0.5g Result Boundary

The best documented v0.5g system is BF16 LoRA r16 plus 1000 targeted-balanced training data under RTX 4090 fallback settings.

Locked `gold_v2_009` metrics:

| Metric | Value |
| --- | ---: |
| Exact match | 36.0% |
| Parse success | 99.3% |
| READ F1 | 84.6% |
| STORE F1 | 99.0% |
| SKIP F1 | 98.1% |
| STORE target accuracy | 100.0% |
| False store rate | 1.2% |
| Irrelevant read rate | 15.5% |

The strong learned result is write-side routing. READ remains the main gap. The hard READ expanded fixture is exactly the right place to test that gap, but the result may be negative.

## Input Compatibility

`src/v05/eval_lora_router.py` expects v05-style case rows with:

- `case_id`
- `runtime_context`
- inline `candidate_memories`
- `current_units`
- optional `gold` for later evaluation

It renders prompts through `src/v05/render_sft_messages.py::render_user_input` and uses the Unit JSON system prompt from `src/v05/render_json_sft_messages.py`.

The hard READ v2 expanded fixture currently has:

- `case_id`
- `runtime_context`
- `user_input`
- `current_units`
- `candidate_memory_ids`
- `labels`
- separate memory rows in `data/v10/hard_read_v2_expanded/hard_read_v2_expanded_memory_pool.jsonl`

Therefore a renderer/converter is required before inference. The conversion is straightforward because all required semantic fields exist, but it must inline memory records and create a v05-compatible `gold` object.

## Proposed Offline Batch Prediction Design

1. Build converted case JSONL:
   - Input: expanded hard READ cases and memory pool.
   - Output: `data/v10/hard_read_v2_expanded_learned_router/hard_read_v2_expanded_router_cases.jsonl`.
   - Each row should inline `candidate_memories` in fixture candidate order.
   - Each row should include `gold.read = required_memory_ids + helpful_memory_ids`, `gold.store = []`, and `gold.skip = all current unit IDs`.

2. Run offline inference only after adapter/base model availability is confirmed:
   - Use `src/v05/eval_lora_router.py`.
   - Use `--interface unit_json`.
   - Use adapter `results/v05g_bf16_lora/qwen35_json_r16_1000_4090/adapter`.
   - Save predictions under `data/v10/hard_read_v2_expanded_learned_router/`.

3. Evaluate learned READ selection:
   - Parse `raw_output` JSON.
   - Use only `read` for the hard READ selector comparison.
   - Treat `store` and `skip` as diagnostics; do not tune the fixture around them.
   - Compute required/helpful/avoid/stale/contradictory/wrong-scope/sensitive injection metrics using the existing hard READ metric semantics.

## Replay Strategy Feasibility

Replay inside the harness is feasible with a new selector backend:

```text
replay_learned_router
```

It should load saved predictions by `case_id`, parse `raw_output.read`, filter IDs to available candidates, preserve candidate order for context building, and emit diagnostics for parse errors, invalid IDs, empty reads, and omitted IDs.

This keeps inference and harness evaluation decoupled: expensive model execution happens once, then all downstream comparisons can replay saved predictions without loading Qwen or LoRA.

## Negative-Result Policy

If learned-router READ fails on hard distractor pools, report that directly.

Do not:

- tune fixture order to help learned-router output;
- remove hard negatives to improve learned-router metrics;
- rewrite labels around model predictions;
- hide parse failures or invalid IDs;
- claim learned-router downstream advantage from oracle or deterministic baseline results.

Acceptable conclusions include:

- v0.5g is strong for write-side policy but weak on hard READ selection;
- hard READ likely needs retrieval/reranking or a different objective;
- learned-router output may still be useful as one diagnostic condition, not as the winning condition.

## Recommendation

Proceed with a gap-closure experiment only after restoring the adapter and confirming `QWEN35_MODEL_PATH`. The next implementation should be:

1. render hard READ expanded cases into v05 Unit JSON input format;
2. add a prediction parser and `replay_learned_router` selector;
3. run one small no-model dry validation over converted cases;
4. only then request explicit approval for offline inference.

