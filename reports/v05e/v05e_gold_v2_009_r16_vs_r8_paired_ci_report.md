# r16 vs r8 Paired CI Report (gold_v2_009)

**Date:** 2026-06-04  

## Primary Metric

| Statistic | Value |
|-----------|-------|
| r16 exact | 22.7% |
| r8 exact | 22.7% |
| Mean paired difference | 0.00pp |
| Bootstrap 95% CI | [−5.33, +5.33] pp |
| CI lower bound > 0? | **No** |

## Conclusion (Pre-Registered)

**r=16 is statistically indistinguishable from r=8 on the primary paired exact metric.** The CI includes 0.

## Secondary Metrics (Directional)

| Metric | r16 | r8 | Δ |
|--------|:---:|:---:|:--:|
| Store/skip-exact | **62.0%** | 53.3% | **+8.7pp** |
| STORE F1 | **0.909** | 0.880 | +0.029 |
| Target accuracy | **84.2%** | 79.1% | **+5.1pp** |
| SKIP F1 | **0.892** | 0.834 | +0.058 |
| Parse | 94.7% | **98.7%** | −4.0pp |

## McNemar Discordant Pairs

| | r8 correct | r8 wrong |
|---|---|---|
| r16 correct | 26 | 8 |
| r16 wrong | 8 | 108 |

Net r16 advantage: 0 cases (perfectly balanced).

## Safety Gate

Both r16 and r8 show 0% sensitive store (eval_runner tag rate). Genuine audit deferred to sensitive audit report.

## Interpretation

Per pre-registration fallback:
> "r=16 is directionally promising / statistically indistinguishable from r=8 on gold_v2_009. All supporting routing metrics are non-regressing; store/skip-exact favors r=16 by +8.7pp."
