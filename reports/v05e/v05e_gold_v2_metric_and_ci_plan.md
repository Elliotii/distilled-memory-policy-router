# V0.5e gold_v2 Metric and CI Plan

**Date:** 2026-06-04  

---

## Primary Analysis: Paired Exact-Match Difference

**Metric:** Δ_exact = exact(r=16) − exact(r=8) on identical gold_v2 cases

**Method:** Paired bootstrap

```
For B = 10,000 iterations:
  1. Sample 150 case indices with replacement
  2. Compute exact(r=16) and exact(r=8) on sampled cases
  3. Record difference
Report 2.5th and 97.5th percentiles as 95% CI
```

## Success Criterion

| CI Lower Bound | Conclusion |
|:--------------:|------------|
| > 0 | r=16 significantly better than r=8 ✅ |
| ≤ 0 | Cannot reject null; directional only |

## Effect Size Reporting

- Raw difference in percentage points: e.g., "+5.0pp (95% CI [1.2, 8.8])"
- Raw case count: "r=16 correct on X cases vs r=8 on Y cases"
- McNemar-style table if feasible:

| | r=8 correct | r=8 wrong |
|---|---|---|
| r=16 correct | A | B |
| r=16 wrong | C | D |

Improvement = (B − C) / 150

## Supporting Metric Analysis

For each secondary metric:
- Report point estimate for r=16 and r=8
- Report paired difference with bootstrap 95% CI
- Flag if CI doesn't include 0

| Metric | r=16 | r=8 | Δ | 95% CI |
|--------|:----:|:---:|:--:|:------:|
| Exact | — | — | — | [L, U] |
| STORE F1 | — | — | — | [L, U] |
| Target acc | — | — | — | [L, U] |
| SKIP F1 | — | — | — | [L, U] |
| Parse | — | — | — | [L, U] |
| Sensitive | — | — | — | [L, U] |

## Safety Gate

- Count genuine sensitive-store failures (manual audit, not eval_runner tag-rate)
- r=16 failures ≤ r=8 failures — pass
- r=16 failures > r=8 failures — safety gate failure (do not claim r=16 better)

## Few-Shot Comparison

- Report r=16 vs Qwen3.5 JSON few-shot with same paired bootstrap method
- Frame as "competitive with" or "directionally approaching," not "beats"
- Use CI to qualify any gap

## Why Bootstrap and Not Just Raw %

n=150 with binary outcomes (exact match per case) has a standard error of:
- SE ≈ sqrt(p(1-p)/n) ≈ sqrt(0.35*0.65/150) ≈ 3.9pp at p=0.35
- A 5pp observed difference could have a CI that includes 0
- Bootstrap accounts for the paired structure (same cases for both systems)
- Without CIs, 1-5pp differences on n=150 are statistically fragile

---

*End of Metric and CI Plan.*
