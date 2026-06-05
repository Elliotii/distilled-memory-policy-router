# gold_v2_009 Error Analysis

**Date:** 2026-06-04  

## Parse Failures

| System | Parse | Failures |
|--------|:-----:|:--------:|
| Qwen3.5 r=8 | 98.7% | 2 |
| Qwen3.5 r=16 | 94.7% | 8 |
| Qwen3-4B r=8 | 100.0% | 0 |
| Qwen3.5 few-shot | 86.0% | 21 |

r=16 has more parse failures than r=8 (8 vs 2). Most are likely unit coverage issues or JSON formatting. r=16's higher rank may cause slight instability in JSON generation.

## Exact Match Breakdown

Among parseable cases:
- r=16: 22.7% / 94.7% = 24.0% of parseable
- r=8: 22.7% / 98.7% = 23.0% of parseable

r=16 has slightly higher exact rate among valid outputs but more failures reduce overall rate.

## Few-Shot Parse Issue

Qwen3.5 few-shot has 86% parse — 21 failures. This likely stems from enable_thinking not being consistently applied. The few-shot exact (30.7%) may be underestimated. For fair comparison, few-shot should be re-run with enable_thinking=False on v009.

## READ Component

READ accounts for most of the exact match deficit: store/skip-exact rates (53-62%) are much higher than full exact (16-23%). This reflects v009's deterministic READ convention — the model must learn to READ all non-stale service/repo/project memories.
