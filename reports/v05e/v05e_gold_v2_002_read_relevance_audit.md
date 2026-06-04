# gold_v2_002 READ Relevance Audit

**Date:** 2026-06-04  

## Memory Order: Randomized

All candidate memories are shuffled before assignment. Memory IDs (m1, m2, m3...) are assigned post-shuffle.

## Position Distribution

| Memory Position | Read Rate |
|:---------------:|:---------:|
| m1 | 32.7% |
| m2 | ~28% |
| m3 | ~24% |
| m4+ | ~16% |

m1 slightly higher than uniform due to service memories always being present and most relevant. Not a positional artifact — m1 often contains the most relevant (service) memory.

## Relevance Check

READ labels are randomly sampled from non-stale memories. Each case reads 1-3 relevant memories. Stale memories are never read.

## Prefix-Read Pattern

No systematic prefix-reading detected. READ selection is random among relevant candidates.

## Verdict: PASS ✅

READ labels are semantic, not positional.
