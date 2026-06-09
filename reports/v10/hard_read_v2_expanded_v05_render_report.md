# Hard READ v2 Expanded v05 Router Render Report

## Summary

- Row count: 32
- Memory pool count: 320
- Max model input chars: 1589
- Max candidate count: 10
- Output JSONL: `data/v10/learned_router_eval/hard_read_v2_expanded_v05_router_inputs.jsonl`

## Input-Format Mapping Summary

- `runtime_context` is preserved as v05 `RUNTIME_CONTEXT`.
- `candidate_memory_ids` are resolved through the hard READ expanded memory pool and inlined as v05 `candidate_memories` in fixture order.
- Memory `flags` are mapped to v05-compatible `tags` in the local case object.
- `current_units` are preserved exactly.
- Evaluation-only `gold.read` is required plus helpful memory IDs; `gold.store` is empty; `gold.skip` contains every current unit.

## Label Leakage Check

- Model-input leakage case count: 0
- Labels, candidate labels, expected answer requirements, oracle/gold wording, API keys, and local model paths are not included in `model_input`.
- Labels are retained only under `eval_only` for local scoring and must not be sent to the model.

## Known Mismatches From v0.5g Format

- The hard READ fixture uses 10 candidates per case, which may be outside common v0.5g training examples.
- These are READ-focused cases; STORE is intentionally empty and all current units are marked as skip for format compatibility.
- Hard negatives are stronger than ordinary entity-matching training examples.

## Limitations

- This render step does not load a model or adapter.
- This render step does not create learned-router predictions.
- This render step does not claim learned-router performance.

## Next Step

After the v0.5g adapter and local `QWEN35_MODEL_PATH` are available, run offline batch prediction with `src/v05/eval_lora_router.py --interface unit_json` against the rendered v05 router case rows or an equivalent case-only projection.
