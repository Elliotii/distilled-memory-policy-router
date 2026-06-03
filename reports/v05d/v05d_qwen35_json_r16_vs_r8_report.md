# V0.5d r=16 vs r=8 Comparison

**Date:** 2026-06-04  
**Split:** Dev only — same dev set, same training data  

## Head-to-Head (Dev)

| Metric | r=16 | r=8 | Δ |
|--------|:----:|:---:|:--:|
| Parse | **99.0%** | 98.0% | +1.0pp |
| Exact | **39.0%** | 34.0% | **+5.0pp** ✅✅ |
| READ F1 | **0.925** | 0.908 | +0.017 |
| STORE F1 | **0.968** | 0.959 | +0.009 |
| Target acc | **77.7%** | 77.4% | +0.3pp |
| SKIP F1 | **0.819** | 0.762 | **+0.057** ✅ |
| False store | **4.0%** | 4.5% | −0.5pp |
| Irrelevant read | **11.9%** | 13.5% | −1.6pp |
| Sensitive (tag) | 66.7% | 66.7% | 0.0pp |

## Answers

1. **Does r=16 improve exact?** ✅ **Yes, +5pp (39% vs 34%).** This is a substantial gain.
2. **Does r=16 improve target accuracy?** ~ Neutral (+0.3pp, within noise). Target acc was already high at 77.4%.
3. **Does r=16 preserve parse?** ✅ **Yes — 99%, improved from 98%.**
4. **Does r=16 preserve STORE F1?** ✅ **Yes — 0.968 vs 0.959, slightly improved.**
5. **Does r=16 preserve SKIP F1?** ✅ **Yes — 0.819 vs 0.762, significantly improved (+0.057).**
6. **Does r=16 worsen sensitive store?** No change (66.7% tag-rate for both).
7. **Does r=16 show overfitting?** No — all metrics improve or stay flat, none degrade.
8. **Is r=16 worth gold_v2?** ✅ **Yes — +5pp exact on dev is a clear signal.**

## Projected Gold

If r=8 dev→gold generalization (+7pp exact, +0.010 STORE F1, −3.7pp target) applies to r=16:

| Metric | r=16 Dev | r=16 Gold (proj.) | Qwen3.5 fs Gold |
|--------|:--------:|:-----------------:|:---------------:|
| Exact | 39.0% | **44-48%** | 42% |
| STORE F1 | 0.968 | ~0.975 | 0.963 |
| Target acc | 77.7% | ~74% | 79.1% |

**r=16 could become the FIRST trained system to beat Qwen3.5 JSON few-shot on exact match.**
