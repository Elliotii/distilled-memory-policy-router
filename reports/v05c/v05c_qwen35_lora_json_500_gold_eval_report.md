# V0.5c Qwen3.5 JSON LoRA 500 — Locked Gold Eval

**Date:** 2026-06-04  
**Context:** 5.9-E — Final locked-gold evaluation  

## Gold Dataset

- Cases: 100 (70 core + 30 hard)
- Gold hash: `56e16078...`
- STORE units: 210, SKIP units: 44, READ IDs: 92

## Structural Metrics (Gold)

| Metric | Value |
|--------|:-----:|
| Parse success | **100.0%** ✅ |
| Invalid memory ID | 0 |
| Invalid unit/span | 0 |
| Invalid target | 0 |
| target="skip" | 0 |
| Truncated JSON | 0 |
| Prose/markdown | 0 |
| Avg chars | 124.3 |

## Semantic Metrics (Gold)

| Metric | Qwen3.5 500 Gold | Qwen3.5 500 Dev | Δ |
|--------|:----------------:|:---------------:|:--:|
| Exact | **41.0%** | 34.0% | +7.0pp |
| READ F1 | **0.938** | 0.908 | +0.030 |
| STORE unit F1 | **0.969** | 0.959 | +0.010 |
| Target accuracy | **73.7%** | 77.4% | −3.7pp |
| SKIP F1 | **0.847** | 0.762 | +0.085 |
| False store | 3.8% | 4.5% | −0.7pp |
| Irrelevant read | 10.0% | 13.5% | −3.5pp |
| Sensitive (eval tag) | 75.0% | 66.7% | +8.3pp |

## Key Findings

1. **100% parse on gold** — perfect structural validity. Zero errors of any kind.
2. **41% exact** — exceeds dev by 7pp, within 1pp of Qwen3.5 JSON few-shot (42%).
3. **0.969 STORE F1** — the HIGHEST of any system in this study (including few-shot).
4. **73.7% target accuracy** — modest decline from dev (−3.7pp) but still strong.
5. **0.847 SKIP F1** — within 0.004 of Qwen3.5 JSON few-shot (0.851).
6. **Dev→gold generalization is excellent** — most metrics improved on gold.
