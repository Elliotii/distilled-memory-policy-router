# V0.5d r=16 Dev Eval Report

**Date:** 2026-06-04  

## Metrics

| Metric | r=16 Dev | r=8 Dev | Δ |
|--------|:--------:|:-------:|:--:|
| Parse | **99.0%** | 98.0% | +1.0pp |
| Exact | **39.0%** | 34.0% | **+5.0pp** ✅✅ |
| READ F1 | **0.925** | 0.908 | +0.017 |
| STORE F1 | **0.968** | 0.959 | +0.009 |
| Target acc | **77.7%** | 77.4% | +0.3pp |
| SKIP F1 | **0.819** | 0.762 | +0.057 ✅ |
| False store | 4.0% | 4.5% | −0.5pp |
| Irrelevant read | 11.9% | 13.5% | −1.6pp |
| Sensitive (tag) | 66.7% | 66.7% | 0.0pp |

## r=16 Dev vs r=8 Gold (reference only)

| Metric | r=16 Dev | r=8 Gold | Δ |
|--------|:--------:|:--------:|:--:|
| Exact | 39.0% | 41.0% | −2pp |
| STORE F1 | 0.968 | 0.969 | −0.001 |
| Target acc | 77.7% | 73.7% | +4.0pp |

**Note:** Dev vs gold comparison is cross-split — not same-split evidence. For reference only.

r=16 dev (39%) is close to r=8 gold (41%). If r=8's dev→gold generalization (+7pp exact) holds for r=16, r=16 gold could reach ~46% — potentially beating Qwen3.5 few-shot (42%).

## Parse: 1 failure (99%)

1 missing unit assignment — edge case where model correctly identifies no STORE but forgets to put the unit in skip. No `"target":"skip"`, no truncated JSON, no invalid targets.
