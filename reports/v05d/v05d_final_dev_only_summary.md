# V0.5d Final Dev-Only Summary

**Date:** 2026-06-04  
**Status:** Dev-only complete — no gold evaluation  

---

## Experiment: Qwen3.5 Unit JSON QLoRA r=16 (Capacity Ablation)

**Question:** Does doubling LoRA rank from r=8 to r=16 improve dev performance?

**Answer:** Yes — +5pp exact, +0.057 SKIP F1, +0.009 STORE F1. All metrics improve or stay flat.

## Dev Results

| Metric | r=16 Dev | r=8 Dev | Δ |
|--------|:--------:|:-------:|:--:|
| Parse | 99.0% | 98.0% | +1.0pp |
| Exact | **39.0%** | 34.0% | **+5.0pp** |
| READ F1 | 0.925 | 0.908 | +0.017 |
| STORE F1 | 0.968 | 0.959 | +0.009 |
| Target acc | 77.7% | 77.4% | +0.3pp |
| SKIP F1 | 0.819 | 0.762 | +0.057 |
| False store | 4.0% | 4.5% | −0.5pp |

## Trainable Params

| Rank | Params | % of 4.2B |
|:----:|:------:|:---------:|
| r=8 | 4,915,200 | 0.12% |
| r=16 | 9,830,400 | 0.23% |

## Key Finding

**Increasing adapter capacity from r=8 to r=16 provides meaningful improvement (+5pp exact) without any downside.** Parse improves, STORE/SKIP improve, false store decreases. r=16 is the best dev-performing QLoRA setting tested.

## Current Best Systems

| Category | System | Status |
|----------|--------|:------:|
| Best gold-verified trained | Qwen3.5 r=8 500 | ✅ Gold |
| Best dev-performing trained | **Qwen3.5 r=16 500** | ⚠ Dev-only |
| Best overall | Qwen3.5 JSON few-shot | ✅ Gold |

r=16 has not been evaluated on gold. r=8 remains the best **gold-verified** trained system.

## Projected Gold

If r=8's dev→gold generalization (+7pp exact) holds for r=16:
- r=16 gold: ~44-48% exact (could beat Qwen3.5 few-shot at 42%)
- But this MUST be confirmed on fresh gold (gold_v2)

---

*End of Summary.*
