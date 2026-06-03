# V0.5c Qwen3.5 JSON LoRA 500 Gold Readiness Decision

**Date:** 2026-06-03  
**Context:** 5.9-D  

---

## Decision: Option A — Ready for Locked-Gold Eval

### Gate Checklist

| Gate | Threshold | Actual | Status |
|------|:---------:|:------:|:------:|
| Training completes | — | 2982s, no OOM/NaN | ✅ |
| Adapter saved | — | ✅ | ✅ |
| Parse ≥ 95% | 95% | **98.0%** | ✅ |
| target=skip eliminated | 0 | **0** | ✅ |
| No post-processing repair | — | Strict only | ✅ |
| Exact ≥ Qwen3-4B 500 | 34% | **34% (tie)** | ✅ |
| Target acc > Qwen3-4B 500 | 68.5% | **77.4% (+8.9pp)** | ✅✅ |
| STORE F1 ≥ 0.95 | — | **0.959** | ✅ |
| Parse stable (no regression) | — | Recovered from 90%→98% | ✅ |
| Gold hash unchanged | — | `56e16078...` | ✅ |

### Dev Metrics Summary

| Metric | Qwen3.5 500 Dev | Qwen3.5 few-shot Gold |
|--------|:---------------:|:---------------------:|
| Exact | 34.0% | 42% |
| STORE F1 | 0.959 | 0.963 |
| Target acc | 77.4% | 79.1% |
| SKIP F1 | 0.762 | 0.851 |

Qwen3.5 LoRA 500 is within striking distance of Qwen3.5 few-shot on target accuracy (1.7pp gap) and STORE F1 (0.004 gap). Exact and SKIP F1 remain behind but are competitive.

### Why Option A (Not B/C/D)

- **Not B**: Parse recovered to 98%, target=skip eliminated. No postmortem needed.
- **Not C**: No config/prompt fix needed. The 250 parse dip was transient.
- **Not D**: Qwen3.5 500 decisively beats Qwen3-4B 500 on target accuracy and ties on exact.

### Expected Gold Result

Based on Qwen3-4B dev→gold delta (target acc −1.2pp, exact −3pp):

| Metric | Dev (actual) | Gold (projected) |
|--------|:------------:|:----------------:|
| Exact | 34.0% | 31-34% |
| STORE F1 | 0.959 | 0.940-0.955 |
| Target acc | 77.4% | 75-77% |
| Sensitive | 66.7% | 6/10 failures (est.) |

If these projections hold, Qwen3.5 LoRA 500 would rank #2 or #3 overall behind Qwen3.5 JSON few-shot (#1, 42% exact) but ahead of Qwen3-4B JSON LoRA 500 (#3, 31% exact).

### Known Caveats for Gold

1. **Parse not 100%**: 2 missing-unit failures may also appear on gold.
2. **Sensitive store**: Expected 6+ failures (untrained on safety).
3. **Gold not fully blind**: Third evaluation on same gold set.
4. **Dev→gold gap**: Qwen3.5 may generalize differently than Qwen3-4B.

---

*End of Gold Readiness Decision.*
