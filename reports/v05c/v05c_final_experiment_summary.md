# V0.5c Final Experiment Summary

**Date:** 2026-06-04  

## Experiment: Qwen3.5 Unit JSON LoRA (Base-Model Ablation)

**Question:** Can Qwen3.5 + Unit JSON QLoRA close the gap to Qwen3.5 JSON few-shot?

**Answer:** Ultra-competitive but not yet. 41% exact (1pp gap), 0.969 STORE F1 (beats few-shot). Qwen3.5 JSON few-shot remains #1 on exact, target accuracy, and safety.

---

## Locked-Gold Results

| System | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | 42% | 0.963 | 79.1% | 0.851 | 0 |
| **Qwen3.5 JSON LoRA 500** | **41%** | **0.969** | 73.7% | 0.847 | 5 |
| Qwen3.5 DSL fs | 36% | 0.959 | 77.6% | 0.795 | 0 |
| Qwen3-4B JSON LoRA 500 | 31% | 0.941 | 67.3% | 0.706 | 6 |

---

## Qwen3.5 Dev Learning Curve

| Metric | 125 | 250 | 500 |
|--------|:---:|:---:|:---:|
| Parse | 98% | 90% | 98% |
| Exact | 30% | 17% | 34% |
| Target acc | 65.6% | 73.1% | 77.4% |
| STORE F1 | 0.891 | 0.913 | 0.959 |

---

## vs Qwen3-4B (at 500 cases, gold)

| Metric | Qwen3.5 | Qwen3-4B | Δ |
|--------|:-------:|:--------:|:--:|
| Exact | 41% | 31% | **+10pp** |
| Target acc | 73.7% | 67.3% | **+6.4pp** |
| STORE F1 | 0.969 | 0.941 | +0.028 |
| Sensitive | 5 | 6 | −1 |

---

## Key Numbers

- **100%** parse on gold (0 structural errors)
- **41%** exact — within 1pp of few-shot
- **0.969** STORE F1 — highest of ALL systems
- **+10pp** exact over Qwen3-4B LoRA
- **5** sensitive failures (PII only, 0 credentials)
- **500** training cases
- **r=8** LoRA rank, 4-bit QLoRA
