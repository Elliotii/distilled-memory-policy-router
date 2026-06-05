# V0.5e Final r16 vs r8 Decision

**Date:** 2026-06-04  

## Decision: r16 Is Directionally Promising; r8 Is the Conservative Choice

### Primary Metric
r16 and r8 are **statistically indistinguishable** on paired exact match (CI includes 0).

### Directional Evidence

| Factor | Favors | Margin |
|--------|:------:|:------:|
| Store/skip-exact | r16 | +8.7pp |
| STORE F1 | r16 | +0.029 |
| Target accuracy | r16 | +5.1pp |
| SKIP F1 | r16 | +0.058 |
| Parse stability | **r8** | +4.0pp |

### Use Cases

| Priority | Recommendation |
|----------|:-------------:|
| Routing accuracy | **r16** (better STORE/target/SKIP) |
| Parse reliability | **r8** (98.7% vs 94.7%) |
| Conservative/mixed | **r8** (no regression, proven) |

### Future

If parse can be stabilized (output-constrained decoding, JSON repair), r16 would be the clear winner. Without parse stabilization, r8 is safer.
