# V0.5d Consistency Check

**Date:** 2026-06-04  

## Cross-Report Audit

| Check | Result |
|-------|:------:|
| r=16 exact: 39.0% dev | ✅ Consistent |
| r=8 exact: 34.0% dev | ✅ Consistent |
| Δ exact: +5.0pp | ✅ Consistent |
| r=16 parse: 99.0% | ✅ Consistent |
| r=16 STORE F1: 0.968 | ✅ Consistent |
| r=16 config: lora_r=16, alpha=32 | ✅ Consistent |
| No gold used | ✅ All reports dev-only |
| Gold hash unchanged | ✅ `56e16078...` |

## Forbidden Claims Check

| Claim | Present? | Status |
|-------|:--------:|:------:|
| "r=16 is final best" | No | ✅ |
| "r=16 beats few-shot" | No | ✅ |
| "r=16 gold-verified" | No | ✅ |
| "Production-safe" | No | ✅ |

## File Count

- Reports: 13
- Docs: 2
- Configs: 1
- Predictions: 1

---

**Consistency: PASSED.**
