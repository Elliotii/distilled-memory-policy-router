# V0.5e Project Narrative

## The gold_v2 Journey

v0.5e set out to answer a simple question: does doubling LoRA rank (r=8→r=16) improve routing performance?

To answer it rigorously, we built a fresh gold set (gold_v2) under pre-registered protocol with paired bootstrap CIs. The construction took 9 iterations of independent review, each catching real issues: namespace leakage, label conflicts, template monoculture, placeholder bugs, random READ labels, phantom sensitive tags, and a vocab_item literal bug.

The final gold_v2_009 passed all 15 automated hard gates and two independent audits (ClaudeCode/DeepSeek APPROVE, Opus CORRECTION REQUIRED for documentation only).

## What We Found

r=16 does NOT significantly beat r=8 on exact match (both 22.7%, CI includes 0). The McNemar table shows perfectly balanced discordant pairs (8 vs 8).

But r=16 shows consistent directional improvement on write-side routing: +8.7pp store/skip-exact, +5.1pp target accuracy, +0.029 STORE F1. The catch: r=16 is less parse-stable (94.7% vs 98.7%).

Qwen3.5 few-shot still leads on exact (30.7%), but its parse is poor on gold_v2 (86%) — likely a tooling issue.

## The Bigger Picture

Across v0.5→v0.5b→v0.5c→v0.5e, we've established:
1. Unit JSON > Unit DSL for SFT training
2. Qwen3.5 > Qwen3-4B as base model
3. 500 training cases with QLoRA r=8 achieves 41% exact on old gold
4. r=16 is directionally promising but not significantly better than r=8
5. Parse stability is the main bottleneck for higher-rank adapters

## What's Next

Package v0.5e, then decide: parse stabilization, standard LoRA, or v1.0 downstream benchmark.
