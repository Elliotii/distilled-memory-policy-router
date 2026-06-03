# V0.5c Qwen3.5 JSON LoRA 500 Error Analysis

**Date:** 2026-06-03  

## Parse Failures: 2/100 (2.0%)

| Case | Error | Raw |
|------|-------|-----|
| v05_dev_0005 | missing unit assignment: u1 | `{"read":["m1"],"store":[],"skip":[]}` |
| v05_dev_0014 | missing unit assignment: u1 | `{"read":["m1"],"store":[],"skip":[]}` |

Both cases: model outputs valid JSON with empty store/skip but omits the unit. The unit should be in `skip`.

## target="skip" Audit

| Size | target=skip count |
|:----:|:-----------------:|
| 125 | 0 |
| 250 | 7 |
| 500 | **0** ✅ |

The `"target":"skip"` pattern present at 250 was eliminated by 500. More data resolved this schema confusion.

## Invalid Target Audit

| Size | Invalid targets |
|:----:|:---------------:|
| 250 | 2.7% (from target=skip) |
| 500 | 0.0% |

## Structural Quality

| Issue | Count |
|-------|:-----:|
| Invalid JSON | 0 |
| Missing field | 0 |
| Wrong field type | 0 |
| Prose/markdown | 0 |
| target=skip | 0 |
| Missing unit | 2 |
| Duplicate unit | 0 |
| Memory-ID-as-unit-ID | 0 |
| Truncation | 0 |

The only remaining issue is 2 missing unit assignments — both cases where the model correctly identifies no STORE but forgets to put the unit in skip.
