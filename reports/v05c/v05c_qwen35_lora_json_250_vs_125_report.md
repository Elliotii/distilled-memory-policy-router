# V0.5c Qwen3.5 JSON LoRA 250 vs 125 Comparison

**Date:** 2026-06-03  
**Context:** 5.9-C — Qwen3.5 125→250 learning curve  

---

## Qwen3.5 Learning Curve

| Metric | 125 | 250 | Δ (250−125) |
|--------|:---:|:---:|:-----------:|
| Parse success | 98.0% | 90.0% | **−8.0pp ⚠** |
| Exact | 30.0% | 17.0% | **−13.0pp ⚠** |
| READ F1 | 0.907 | 0.892 | −0.015 |
| STORE unit F1 | 0.891 | 0.913 | **+0.022 ✅** |
| Target accuracy | 65.6% | 73.1% | **+7.5pp ✅✅** |
| SKIP F1 | 0.644 | 0.623 | −0.021 |
| False store | 2.2% | 4.9% | +2.7pp |
| Irrelevant read | 12.3% | 18.2% | +5.9pp |
| Sensitive store | 33.3% | 66.7% | +33.4pp |

## Interpretation

**Mixed learning curve.** Qwen3.5 shows improvement on target routing metrics (target accuracy +7.5pp, STORE F1 +0.022) but regression on structural quality (parse −8.0pp) and exact match (−13.0pp).

The exact match drop is largely mechanical — 10 parse failures remove 10 cases from exact consideration. Among the 90 parseable cases, exact is 18.9% (vs 30.0% at 125 with only 2 parse failures). So the "true" exact decline is smaller than the raw −13pp suggests.

**Qwen3.5 vs Qwen3-4B learning curve comparison:**

| Metric | Qwen3-4B 125→250 | Qwen3.5 125→250 |
|--------|:-----------------:|:-----------------:|
| Parse | 100%→100% (stable) | 98%→90% (**regression**) |
| Exact | 11%→20% (+9pp) | 30%→17% (**regression**) |
| Target acc | 55.7%→63.8% (+8.1pp) | 65.6%→73.1% (+7.5pp) |
| STORE F1 | 0.910→0.947 (+0.037) | 0.891→0.913 (+0.022) |

Both models show similar target accuracy gains (~+8pp), but Qwen3.5 has a structural regression not seen in Qwen3-4B.

## Conclusion

Qwen3.5 250's learning is **asymmetric** — strong on semantics (target routing) but unstable on syntax (JSON structure). This asymmetry is unique to Qwen3.5 and merits careful monitoring at 500.

---

*End of V0.5c Qwen3.5 JSON LoRA 250 vs 125 Comparison.*
