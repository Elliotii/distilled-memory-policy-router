# V0.5e Final Experiment Summary

**Date:** 2026-06-04  

## Question
Does QLoRA r=16 improve over r=8 on a fresh gold_v2?

## Answer
**Statistically indistinguishable on exact.** r16 directionally improves write-side routing but is less parse-stable.

## gold_v2_009 Results

| System | Exact | Parse | STORE F1 | Target Acc |
|--------|:-----:|:-----:|:--------:|:----------:|
| Qwen3.5 few-shot | 30.7% | 86.0% | 0.856 | 75.3% |
| Qwen3.5 r=16 | 22.7% | 94.7% | 0.909 | 84.2% |
| Qwen3.5 r=8 | 22.7% | 98.7% | 0.880 | 79.1% |
| Qwen3-4B r=8 | 16.0% | 100.0% | 0.925 | 76.8% |

## r16 vs r8 Paired CI
Δ = 0.00pp, 95% CI [−5.33, +5.33]

## Key Numbers
- **150** gold_v2_009 active cases
- **9** construction iterations (v001→v009)
- **4** systems evaluated
- **0** exact label conflicts in gold_v2_009
- **0** READ conflicts in gold_v2_009
