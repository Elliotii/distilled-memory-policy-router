# V0.5d r=16 Decision

**Date:** 2026-06-04  

---

## Decision: Option A — r=16 is promising; consider gold_v2 before final claim

### Evidence

| Metric | r=8 Dev | r=16 Dev | Δ |
|--------|:-------:|:--------:|:--:|
| Exact | 34.0% | **39.0%** | **+5.0pp** |
| Parse | 98.0% | **99.0%** | +1.0pp |
| STORE F1 | 0.959 | **0.968** | +0.009 |
| SKIP F1 | 0.762 | **0.819** | +0.057 |
| Target acc | 77.4% | 77.7% | +0.3pp |

All metrics improved or stayed flat. No degradation. r=16 meets all Option A criteria (exact +5pp ≥ 2pp threshold, parse ≥ 98%).

### Why Not "Best Trained" Yet

r=16 is dev-only. The r=8 result showed +7pp exact from dev→gold — if r=16 generalizes similarly, it could reach 44-48% on gold and potentially beat Qwen3.5 JSON few-shot (42%). But this MUST be confirmed on gold_v2, not the old gold (already evaluated 3 times).

### Next Step

1. **gold_v2** — create new 100-case gold set using same methodology
2. **r=16 gold_v2 eval** — final evaluation of r=16 on fresh gold
3. **r=8 gold_v2 eval** — re-baseline r=8 on new gold for clean comparison

### What r=16 Means

- ✅ r=16 is a **clear improvement** over r=8 on dev (+5pp exact)
- ✅ Doubling LoRA rank provides meaningful additional capacity
- ✅ No downside: parse improves, no metric degrades
- 🎯 If r=16 gold generalizes like r=8 did, it could **beat Qwen3.5 JSON few-shot**
- ⚠️ Old gold is not blind enough for this claim — need gold_v2

---

*End of Decision.*
