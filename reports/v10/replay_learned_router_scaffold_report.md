# replay_learned_router Scaffold Report

## Scope

This context implemented model-free scaffold for later offline learned-router READ evaluation. No API was called, no model was loaded, no Qwen or LoRA adapter was loaded, no inference was run, no training was run, and no learned-router metric is claimed.

The debug replay run is plumbing only.

## What Was Implemented

- Added `scripts/render_hard_read_v2_expanded_for_v05_router.py`.
- Rendered 32 hard READ v2 expanded cases into v05-compatible Unit JSON router input rows.
- Added `replay_learned_router` to `apps/memory_harness/backends/read_selectors.py`.
- Added `--replay-predictions` support to `apps/memory_harness/eval_hard_read.py`.
- Created a debug prediction fixture for replay validation only.
- Ran `eval_hard_read` with the debug replay strategy to verify scoring works.

## Render Summary

| Field | Value |
| --- | ---: |
| Rendered rows | 32 |
| Memory pool rows | 320 |
| Max candidate count | 10 |
| Max model input chars | 1589 |
| Model-input label leakage cases | 0 |

Rendered output:

```text
data/v10/learned_router_eval/hard_read_v2_expanded_v05_router_inputs.jsonl
```

Render report:

```text
reports/v10/hard_read_v2_expanded_v05_render_report.md
```

## Replay Prediction Schema

The replay selector accepts saved prediction rows shaped like:

```json
{
  "case_id": "hard_read_v2_001",
  "selected_memory_ids": ["m201"],
  "raw_prediction": "{\"read\":[\"m201\"],\"store\":[],\"skip\":[\"u1\"]}",
  "parse_status": "ok",
  "parse_error": null,
  "model_id": "v0.5g-bf16-lora",
  "adapter_id": "missing-or-external",
  "rendered_input_hash": "...",
  "source": "offline_batch_prediction"
}
```

For compatibility with future `src/v05/eval_lora_router.py` output, the selector can also parse `raw_output` when `selected_memory_ids` is absent.

## Debug Fixture Warning

The file below is not learned-router output:

```text
data/v10/learned_router_eval/debug_replay_predictions.jsonl
```

Every row is marked:

```text
debug_fixture_not_model_output
```

The fixture deterministically selects the first candidate memory for each case. It exists only to verify replay plumbing and metric wiring. It is not learned-router performance and must not be reported as a model result.

## Debug Eval Metrics

Command output directory:

```text
reports/v10/debug_replay_learned_router_eval
```

Aggregate metrics for the debug fixture:

| Strategy | Cases | Mean pre selected | Mean post injected | Post required recall | Post avoid injected | Post stale injected | Post contradictory injected | Mean context chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `replay_learned_router` | 32 | 1.00 | 1.00 | 0.015625 | 31 | 0 | 1 | 116.3125 |

These numbers reflect the first-candidate debug fixture only. They are intentionally not a learned-router metric.

## Validation Summary

- Python compile passed for the renderer, selector backend, and hard READ evaluator.
- Renderer produced 32 rows.
- Rendered model inputs passed row count and leakage checks.
- Debug replay predictions produced 32 rows and all rows have `source = debug_fixture_not_model_output`.
- `eval_hard_read` scored `replay_learned_router` with the debug predictions.
- Debug eval JSON and by-case outputs parse.

## Exact Next Step For Real Offline Batch Predictions

After the v0.5g adapter is restored and local `QWEN35_MODEL_PATH` is available:

1. Project the rendered JSONL rows to v05 case rows, using each row's `v05_router_case`.
2. Run `src/v05/eval_lora_router.py --interface unit_json` with adapter:

```text
results/v05g_bf16_lora/qwen35_json_r16_1000_4090/adapter
```

3. Save raw offline predictions under `data/v10/learned_router_eval/`.
4. Convert or directly replay predictions with `--replay-predictions`.
5. Run hard READ selection metrics with `replay_learned_router` alongside deterministic baselines.

## Claim Boundary

- No model loaded.
- No learned-router metric claimed.
- Debug replay is plumbing only.
- Adapter availability remains the blocker for real learned-router evaluation.
- Live serving and UI remain future work.

