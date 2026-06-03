# V0.5c Qwen3.5 JSON LoRA 500 — Gold Parse Audit

**Date:** 2026-06-04  

## Parse: 100.0% — PERFECT

| Error Type | Count |
|-----------|:-----:|
| Invalid JSON | 0 |
| target="skip" in store | 0 |
| Truncated JSON | 0 |
| Missing key | 0 |
| Missing unit | 0 |
| Duplicate unit | 0 |
| Invalid target | 0 |
| Prose/markdown | 0 |
| Memory-ID-as-unit-ID | 0 |

**Zero structural errors on 100 gold cases.** Qwen3.5 JSON LoRA 500 achieved perfect JSON schema adherence on locked gold. The transient `"target":"skip"` regression at 250 (7 cases) was fully resolved by 500 — 0 occurrences on gold.

## Comparison

| Metric | Dev 250 | Dev 500 | Gold 500 |
|--------|:-------:|:-------:|:--------:|
| Parse | 90.0% | 98.0% | **100.0%** |
| target=skip | 7 | 0 | **0** |
| Missing unit | 1 | 2 | **0** |

Gold performance exceeded dev performance — no generalization penalty on structural quality.
