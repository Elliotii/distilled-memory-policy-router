# V0.5e Final Error Analysis

**Date:** 2026-06-04  

## Parse Failures (gold_v2_009)

| System | Parse | Failures | Primary Issue |
|--------|:-----:|:--------:|---------------|
| Qwen3.5 r=8 | 98.7% | 2 | Missing unit coverage |
| Qwen3.5 r=16 | 94.7% | 8 | JSON formatting + missing units |
| Qwen3-4B r=8 | 100.0% | 0 | None |
| Qwen3.5 few-shot | 86.0% | 21 | enable_thinking not fully suppressed |

## Exact Match Decomposition

| System | Full Exact | Store/Skip-Exact | READ-Only Errors |
|--------|:----------:|:----------------:|:----------------:|
| r16 | 22.7% | 62.0% | ~39% of cases |
| r8 | 22.7% | 53.3% | ~31% of cases |

READ accounts for most of the exact-match deficit. v009's deterministic READ convention (READ all non-stale service/repo/project memories) requires the model to learn this pattern from training data alone.

## Few-Shot Parse Issue

Qwen3.5 few-shot's 86% parse on gold_v2 is significantly below its performance on old gold (100% parse). This likely stems from the few-shot runner not applying `enable_thinking=False` consistently on v009. The 30.7% exact may be an underestimate.

## r16 Parse Deficit

r16's higher LoRA rank (4.9M → 9.8M params) may introduce slight instability in JSON generation, causing 6 additional parse failures vs r8. Output-constrained decoding or JSON repair could mitigate this.

## Sensitive

All Qwen3.5-based systems show 0% eval_runner tag rate on v009. No sensitive failures detected by automated audit.
