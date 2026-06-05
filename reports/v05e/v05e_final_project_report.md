# V0.5e Final Project Report

**Date:** 2026-06-04  
**Status:** Complete — gold_v2_009 four-system evaluation done  

---

## Executive Summary

**V0.5e gold_v2:** A fresh 150-case gold set built under pre-registered protocol to evaluate Qwen3.5 JSON QLoRA r=16 vs r=8. After 9 iterations of independent review and repair, gold_v2_009 passed all gates and was used for final four-system evaluation.

**Primary result:** r=16 and r=8 are statistically indistinguishable on paired exact match (both 22.7%, 95% CI [−5.33, +5.33]). r=16 directionally improves write-side routing metrics (+8.7pp store/skip-exact, +5.1pp target accuracy) but has lower parse stability (94.7% vs 98.7%).

**Qwen3.5 JSON few-shot** leads on exact (30.7%) but has poor parse (86%) on gold_v2_009.

---

## 1. Experiment Timeline

| Phase | Contexts | Result |
|-------|----------|--------|
| Protocol & pre-registration | P5.24-A | 150 cases, paired CI, pre-registered |
| Construction (v001→v009) | P5.24-B through B9 | 9 iterations, independent reviews |
| Harness & corrections | P5.24-B10 | Opus review, renderer patches |
| Four-system evaluation | P5.12-C | r16, r8, few-shot, Qwen3-4B anchor |

## 2. gold_v2_009 Final Results

| # | System | Exact | Parse | STORE F1 | Target Acc | SKIP F1 |
|:-:|--------|:-----:|:-----:|:--------:|:----------:|:-------:|
| 1 | Qwen3.5 JSON few-shot | **30.7%** | 86.0% | 0.856 | 75.3% | 0.847 |
| 2 | Qwen3.5 r=16 LoRA | 22.7% | 94.7% | **0.909** | **84.2%** | **0.892** |
| 3 | Qwen3.5 r=8 LoRA | 22.7% | **98.7%** | 0.880 | 79.1% | 0.834 |
| 4 | Qwen3-4B r=8 LoRA | 16.0% | 100.0% | 0.925 | 76.8% | 0.860 |

## 3. Primary Analysis: r16 vs r8

| Statistic | Value |
|-----------|-------|
| r16 exact | 22.7% |
| r8 exact | 22.7% |
| Paired Δ | 0.00pp |
| Bootstrap 95% CI | [−5.33, +5.33] |
| CI > 0? | No |
| McNemar r16-only | 8 cases |
| McNemar r8-only | 8 cases |

## 4. Directional Evidence

| Metric | r16 | r8 | Δ |
|--------|:---:|:---:|:--:|
| Store/skip-exact | **62.0%** | 53.3% | **+8.7pp** |
| STORE F1 | **0.909** | 0.880 | +0.029 |
| Target accuracy | **84.2%** | 79.1% | **+5.1pp** |
| SKIP F1 | **0.892** | 0.834 | +0.058 |
| Parse | 94.7% | **98.7%** | −4.0pp |

## 5. Conclusion

**r=16 does not significantly beat r=8 on the pre-registered primary metric.** It is directionally promising on write-side routing but less parse-stable. r=8 remains the safer choice for applications prioritizing reliability. Both are viable; the choice depends on whether routing accuracy or parse stability is more valued.

**Qwen3.5 JSON few-shot** remains the best full-exact baseline, but its parse instability (86%) on gold_v2 may be a tooling issue.

---

*End of V0.5e Final Project Report.*
