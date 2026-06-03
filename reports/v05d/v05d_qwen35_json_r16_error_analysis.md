# V0.5d r=16 Error Analysis

**Date:** 2026-06-04  

## Parse: 1/100 failure (99%)

| Case | Error |
|------|-------|
| v05_dev_0014 | Missing unit assignment: u1 |

Single unit omitted from both store and skip. Model output: `{"read":[...],"store":[],"skip":[]}` — valid JSON but missing unit coverage. Same case also failed at r=8 500.

## Structural Quality

| Issue | r=16 | r=8 |
|-------|:----:|:---:|
| target=skip | 0 ✅ | 0 ✅ |
| Truncated JSON | 0 | 0 |
| Invalid JSON | 0 | 0 |
| Invalid target | 0 | 0 |
| Missing unit | 1 | 2 |

r=16 has 1 fewer missing-unit error than r=8 on dev.

## Comparison with r=8 Error Profile

Both r=8 and r=16 have the same failure pattern: occasional missing-unit edge cases with otherwise perfect JSON structure. No `"target":"skip"` regression. r=16 is slightly cleaner (1 vs 2 failures).
