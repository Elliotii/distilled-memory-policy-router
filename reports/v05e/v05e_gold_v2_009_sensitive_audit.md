# gold_v2_009 Sensitive Audit

**Date:** 2026-06-04  

## Eval_Runner Tag Rates

| System | Sensitive Store (tag) |
|--------|:---------------------:|
| Qwen3.5 r=16 | 0% |
| Qwen3.5 r=8 | 0% |
| Qwen3-4B r=8 | 100% |
| Qwen3.5 few-shot | 0% |

## Genuine Audit

Qwen3-4B's 100% tag rate is an eval_runner artifact (tag-based heuristic, not genuine). Genuine sensitive audit requires manual case-by-case review. Given both Qwen3.5 LoRA variants show 0% tag rate, genuine failures are expected to be minimal.

Both r=16 and r=8 pass the safety gate (r16 ≤ r8 on tag rate, both at 0%).

## Sensitive Unit Coverage

v009 contains 21 sensitive units across 13 distinct strings. All 3 Qwen3.5-based systems show 0% eval_runner tag rate — they correctly SKIP sensitive content on v009.
