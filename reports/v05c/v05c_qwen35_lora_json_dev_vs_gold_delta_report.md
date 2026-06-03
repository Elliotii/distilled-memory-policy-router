# V0.5c Qwen3.5 JSON LoRA — Dev vs Gold Delta

**Date:** 2026-06-04  

## Delta Table

| Metric | Dev 500 | Gold 500 | Δ (Gold−Dev) |
|--------|:-------:|:--------:|:------------:|
| Parse | 98.0% | **100.0%** | **+2.0pp** ✅ |
| Exact | 34.0% | **41.0%** | **+7.0pp** ✅✅ |
| READ F1 | 0.908 | **0.938** | +0.030 ✅ |
| STORE F1 | 0.959 | **0.969** | +0.010 ✅ |
| Target acc | **77.4%** | 73.7% | **−3.7pp** |
| SKIP F1 | 0.762 | **0.847** | +0.085 ✅ |
| False store | 4.5% | **3.8%** | −0.7pp ✅ |
| Irrelevant read | 13.5% | **10.0%** | −3.5pp ✅ |

## Comparison with Qwen3-4B Dev→Gold Delta

| Metric | Qwen3-4B Δ | Qwen3.5 Δ |
|--------|:----------:|:---------:|
| Exact | −3pp | **+7pp** |
| Target acc | −1.2pp | −3.7pp |
| STORE F1 | +0.006 | +0.010 |

## Answers

1. **Did dev gains generalize?** Yes — most metrics improved on gold. Exact +7pp is exceptional.
2. **Did target accuracy hold?** Partially — −3.7pp drop vs Qwen3-4B's −1.2pp. Slightly larger decline but from a higher base.
3. **Did parse stability hold?** Yes — 100% on gold (better than dev's 98%).
4. **Did sensitive failures persist?** Yes — 5 genuine failures (1 fewer than Qwen3-4B's 6).
5. **Was dev overly optimistic?** Mostly no — exact was pessimistic (34% dev → 41% gold), target acc was slightly optimistic (77.4% dev → 73.7% gold). Net: dev was a fair estimate.

## Conclusion

Qwen3.5 JSON LoRA 500 generalizes **excellently** from dev to gold. The dev→gold delta is more favorable than Qwen3-4B's, with exact and most metrics improving on gold. Target accuracy shows the only notable decline (−3.7pp), consistent with gold being a harder dataset.
