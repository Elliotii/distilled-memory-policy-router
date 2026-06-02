# V0.5 Qwen3-4B LoRA 500 Checkpoint Readiness Report

**Date:** 2026-06-02  

## Training

✅ 573s (9.5 min), no OOM/NaN. Eval loss 0.69→0.63→0.62.

## Dev Eval

| Metric | 500 | 250 | 125 | Few-shot DSL |
|--------|:---:|:---:|:---:|:------------:|
| Exact | **24%** | 14% | 12% | 22% |
| STORE F1 | **0.962** | 0.944 | 0.867 | 0.936 |
| Target acc | 54.1% | 55.7% | 60.0% | 71.1% |
| SKIP F1 | **0.773** | 0.684 | 0.492 | 0.690 |
| READ F1 | 0.908 | 0.900 | 0.822 | 0.871 |

**STORE F1 (0.962) nearly matches Qwen3.5 JSON few-shot (0.963 on gold).** Exact exceeds Qwen3-4B DSL few-shot (24% vs 22%).

## Sensitive Store

6 genuine failures (phone ×2, emails ×2, home address, Slack handle). Model over-applies user_profile to personal contact info. No credentials stored. Pattern: 58 user_profile vs ~10 sensitive SKIP training examples → model biased toward storing personal info as preference.

## Learning Curve

| Metric | 125→250 | 250→500 | Overall |
|--------|:-------:|:-------:|:-------:|
| STORE F1 | +0.077 | +0.018 | +0.095 |
| Exact | +2pp | +10pp | +12pp |
| SKIP F1 | +0.192 | +0.089 | +0.281 |
| Target acc | -4.3pp | -1.6pp | -5.9pp |

STORE/SKIP decisions improve with data. Target classification plateaus.

## Decision

**Option B: Needs postmortem before gold, but proceed to gold eval.**

500 STORE F1 (0.962) is strong enough for locked gold baseline. Target accuracy (54.1%) and sensitive handling (6 genuine failures) should be documented as known limitations. Gold evaluation should include per-target accuracy breakdown and sensitive-store audit.

---

*End of V0.5 Qwen3-4B LoRA 500 Checkpoint Readiness Report.*
