# gold_v2_009 Final Decision

**Date:** 2026-06-04  

## Primary Result

**r=16 is statistically indistinguishable from r=8 on paired exact match.** 95% CI [−5.33, +5.33] includes 0.

## Directional Evidence Favors r=16

| Metric | r16 Advantage |
|--------|:------------:|
| Store/skip-exact | **+8.7pp** |
| STORE F1 | +0.029 |
| Target accuracy | **+5.1pp** |
| SKIP F1 | +0.058 |
| Parse | −4.0pp (r8 better) |

## Decision: r=16 is Directionally Promising

Per pre-registration fallback:
> "r=16 is directionally promising / statistically indistinguishable from r=8 on gold_v2_009."

r=16 does NOT regress on any routing metric (STORE F1, target accuracy, SKIP F1 all improve). Parse is slightly worse (94.7% vs 98.7%) but within acceptable range. Safety gate passes.

## r=8 Remains the Conservative Choice

For applications where parse reliability is paramount (98.7% vs 94.7%), r=8 is safer. For applications prioritizing routing accuracy (STORE F1, target acc), r=16 offers improvements.

## Qwen3.5 Few-Shot on v009

Few-shot leads on exact (30.7%) but has poor parse (86%). This may be a tooling issue (enable_thinking). For fair comparison, few-shot should be re-run with the same enable_thinking=False used for LoRA eval.

## Claim Boundaries (Same as Pre-Registration)

- Do NOT claim r=16 significantly beats r=8 on exact
- Do NOT claim production safety
- Do NOT claim boundary-sliced superiority
- Do NOT compare v009 metrics to old gold as same-split
