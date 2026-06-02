# V0.5b Qwen3-4B Unit JSON LoRA 500 Gold Readiness Decision

**Date:** 2026-06-02  
**Context:** 5.7-D — locked-gold final evaluation readiness  

---

## 1. Training Result

| Check | Status |
|-------|:------:|
| 500-case training completed | ✅ 842s |
| Adapter saved | ✅ |
| No OOM/NaN | ✅ |
| Eval loss converged (0.61→0.55→0.54) | ✅ |

## 2. Dev Eval Result (JSON 500)

| Metric | JSON 500 | vs DSL 500 | vs JSON fs |
|--------|:--------:|:----------:|:----------:|
| Parse success | **100.0%** | — | +1pp |
| Exact match | **34.0%** | +10pp | **+11pp** |
| STORE F1 | 0.958 | -0.004 | -0.003 |
| Target accuracy | **68.5%** | **+14.4pp** | **+1.4pp** |
| SKIP F1 | 0.753 | -0.020 | -0.098 |
| Sensitive store | 66.7%* | tied | +33.4pp |

\* Genuine failure audit: 1/4 = 25%. eval_runner tag-based counting may inflate.

## 3. Key Achievements

1. **Beats Qwen3-4B JSON few-shot on exact match (+11pp) and target accuracy (+1.4pp).** JSON 500 is the first LoRA variant to exceed its teacher prompting baseline.

2. **Beats DSL 500 on target accuracy by 14.4pp.** Confirms the interface-ablation hypothesis.

3. **300/300 predictions = 100% valid JSON.** Zero structural errors across all three training sizes.

4. **service_memory accuracy: 91.5%.** The model learned the service/task distinction that DSL could not achieve (only ~25% on gold).

5. **Learning curve is healthy and upward.** Every metric improved from 125→250→500 except sensitive store.

## 4. Known Risks for Gold

| Risk | Severity | Mitigation |
|------|:--------:|------------|
| Sensitive store (66.7% eval) | Medium | Genuine failure = 1 case. Gold has 0 sensitive STORE — clean measurement. |
| SKIP F1 below JSON fs | Low | Still improved from 125 (0.535→0.753). |
| STORE F1 slightly below DSL 500 | Low | Within 0.004 — measurement noise. |
| Gold may differ from dev | Medium | Normal train/dev/gold gap. JSON 250→500 trajectory gives confidence. |
| Small gold (100 cases) | Low | Same gold used for all v0.5 baselines. Directly comparable. |

## 5. Decision: Option A — Ready for Locked-Gold Final Evaluation

### Rationale

1. **JSON 500 is the strongest LoRA variant produced.** It exceeds DSL 500 and JSON few-shot on key metrics.

2. **The interface-ablation hypothesis is confirmed on dev.** JSON improves target classification; gold evaluation is the formal verification.

3. **Parse quality is perfect (100%).** No risk of structural failures inflating gold error rates.

4. **Sensitive store risk is documented and not worse than DSL.** Gold provides a clean 0-sensitive-STORE benchmark.

5. **All metrics show healthy learning curves.** No signs of overfitting or format collapse.

### Gold Evaluation Expectations

Based on dev metrics:
- Exact: likely 25-35% on gold (dev 34% minus typical dev→gold gap)
- STORE F1: likely 0.93-0.96 (dev 0.958)
- Target accuracy: likely 55-65% (dev 68.5%, DSL 500 dev 54.1% → gold 47.5%)
- Sensitive: gold has 0 sensitive STORE labels → clean test

The primary comparison is:
- JSON 500 vs DSL 500 on gold target accuracy
- JSON 500 vs Qwen3-4B JSON few-shot on gold

### Next Context

**Context 5.7-E: Qwen3-4B Unit JSON LoRA 500 locked-gold final evaluation.**

Single eval run on locked gold only. Compare with v0.5 DSL 500 gold numbers. Write final v0.5b report.

### What NOT to Do

- Do NOT iterate on gold.
- Do NOT tune hyperparameters after seeing gold.
- Do NOT compare dev→gold as same-split evidence.
- Do NOT claim v0.5b is production-ready regardless of gold results.

---

*End of V0.5b JSON 500 Gold Readiness Decision — Ready for locked gold.*
