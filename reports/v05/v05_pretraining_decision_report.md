# V0.5 Pretraining Decision Report

**Date:** 2026-06-02  

## First LoRA Target

Qwen3-4B Unit DSL. This is the established v0.5 training interface from the spec, parser, and SFT format. Not chosen based on gold results.

## Why Not JSON Training

JSON few-shot won on locked gold (42% exact vs DSL 36%). However:
- DSL is the original spec target
- JSON training is a future ablation
- Not gold-driven pivoting

## 125→250→500 Plan

Nested subsets, fixed seed 42. Train each, eval on dev, select best checkpoint on dev task metrics.

## Success Criteria

Beat Qwen3.5 JSON fs on gold (42% exact, 0.963 STORE F1) at final 500 checkpoint.

## No Gold Until Final Eval

Gold not used for training, checkpoint selection, or tuning.
