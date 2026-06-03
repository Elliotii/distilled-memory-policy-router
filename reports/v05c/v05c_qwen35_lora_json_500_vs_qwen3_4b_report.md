# V0.5c Qwen3.5 500 vs Qwen3-4B 500 Comparison

**Date:** 2026-06-03  
**Split:** Dev only  

## Head-to-Head

| Metric | Qwen3.5 500 | Qwen3-4B 500 | Δ |
|--------|:-----------:|:------------:|:--:|
| Parse | 98.0% | **100.0%** | −2.0pp |
| Exact | **34.0%** | **34.0%** | **0.0pp (tie)** |
| READ F1 | **0.908** | 0.902 | +0.006 |
| STORE F1 | **0.959** | 0.958 | +0.001 |
| **Target acc** | **77.4%** | 68.5% | **+8.9pp** ✅✅ |
| SKIP F1 | **0.762** | 0.753 | +0.009 |
| False store | **4.5%** | 6.5% | −2.0pp |
| Irrelevant read | **13.5%** | 15.9% | −2.4pp |
| Sensitive store | 66.7% | 66.7% | 0.0pp |

## Q1: Does Qwen3.5 500 beat Qwen3-4B 500 on target accuracy?

**Yes — by +8.9pp (77.4% vs 68.5%).** This is a decisive margin on the primary routing metric.

## Q2: Does it beat Qwen3-4B 500 on exact?

**Tie at 34.0%.** Qwen3.5 matches Qwen3-4B despite having 2 parse failures (Qwen3-4B has 0). Among parseable cases, Qwen3.5 exact is 34/98 = 34.7% vs Qwen3-4B's 34%.

## Q3: Does it preserve parse stability?

**Yes — 98.0%, recovered from 250's 90%.** No `"target":"skip"` errors. Only 2 missing-unit failures.

## Q4: Does it preserve STORE/SKIP?

**Yes.** STORE F1 0.959 (ties Qwen3-4B 500's 0.958). SKIP F1 0.762 (beats Qwen3-4B's 0.753).

## Q5: Does it reduce false store?

**Yes.** 4.5% vs 6.5% — more conservative STORE behavior.

## Q6: Does stronger base model help under Unit JSON?

**Yes, decisively.** Qwen3.5 + JSON LoRA 500 achieves:
- Same exact match as Qwen3-4B 500
- +8.9pp target accuracy
- Better STORE F1, SKIP F1, false store, irrelevant read
- All with fewer trainable LoRA parameters (4.9M vs 5.8M)

The stronger base model provides better target classification even with a simpler LoRA adapter.
