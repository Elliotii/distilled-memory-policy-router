# V0.5b Project Narrative

## What We Tested

V0.5 DSL LoRA training improved action routing but failed target classification. The Unit JSON few-shot prompting baseline consistently outperformed Unit DSL prompting across both Qwen3-4B and Qwen3.5 models. V0.5b asked: **Does the stronger JSON interface transfer this advantage to supervised fine-tuning?**

## Experiment Design

A clean single-variable ablation. Same base model (Qwen3-4B), same data splits, same hyperparameters. Changed only the output format: DSL lines → JSON objects.

## Key Finding: JSON Target Accuracy Increases While DSL Decreases

**DSL target accuracy:** 60.0% (125) → 55.7% (250) → 54.1% (500) — *decreasing with more data*

**JSON target accuracy:** 55.7% (125) → 63.8% (250) → 68.5% (500) — *increasing with more data*

On locked gold, the gap is stark:
- **JSON LoRA 500 target accuracy: 67.3%**
- **DSL LoRA 500 target accuracy: 47.5%**
- **+19.8pp improvement from interface change alone**

## Why JSON Works Better

DSL's positional format (`STORE service_memory u1`) creates confusion: the model mixes up target words with unit IDs, producing errors like `STORE service_memory m1` (memory ID in unit position). JSON's structured format (`{"target": "service_memory", "unit_id": "u1"}`) cleanly separates label from reference, eliminating 100% of parse errors.

## What We Achieved

1. **JSON beats DSL** on exact (+15pp) and target accuracy (+19.8pp)
2. **JSON beats its teacher** — first LoRA to exceed Qwen3-4B JSON few-shot
3. **Perfect structural quality** — 400/400 valid JSON predictions
4. **Service/task distinction learned** — service memory accuracy 70% on gold (DSL: ~25%)

## What Remains

1. **Safety:** 6 sensitive failures (credit card, tokens, PII) — same as DSL
2. **Qwen3.5:** Still strongest system overall (+11pp exact, 0 sensitive)
3. **repo_memory:** 50% accuracy — weakest class

## Next: V0.5c Safety-Focused Training

The JSON format is now proven superior. The next bottleneck is safety. V0.5c will oversample sensitive cases and add loss penalties to target zero sensitive failures while preserving JSON's target accuracy gains.

---

*End of V0.5b Project Narrative.*
