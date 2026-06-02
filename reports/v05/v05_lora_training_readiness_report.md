# V0.5 LoRA Training Readiness Report

**Date:** 2026-06-02  
**Context:** 5.5-A — training pipeline readiness  

---

## 1. Environment

| Component | Version | Status |
|-----------|---------|:------:|
| Python | 3.12.3 | ✅ |
| PyTorch | 2.6.0+cu124 | ✅ |
| CUDA | 12.4 | ✅ |
| GPU | RTX 4070 SUPER (11GB) | ✅ |
| transformers | 5.9.0 | ✅ |
| peft | 0.19.1 | ✅ |
| trl | 1.5.1 | ✅ |
| bitsandbytes | 0.49.2 | ✅ |
| accelerate | 1.13.0 | ✅ |

**All required libraries installed.**

## 2. Data Readiness

| File | Rows | SFT Valid |
|------|:----:|:---------:|
| train_pool_500 | 500 | ✅ |
| train_125 subset | 125 | ✅ |
| train_250 subset | 250 | ✅ |
| train_500 subset | 500 | ✅ |
| dev (eval) | 100 | N/A |
| gold (final) | 100 | N/A |

Nesting: 125 ⊂ 250 ⊂ 500 ✅
Train∩dev = 0 ✅
Train∩gold = 0 ✅

## 3. Leakage

| Check | Hard Blockers | Warnings |
|-------|:------------:|:--------:|
| Train↔Dev | 0 | 1 (natural overlap) |
| Train↔Gold | 0 | 0 |

## 4. LoRA Config

QLoRA on Qwen3-4B:
- 4-bit quantization (nf4)
- LoRA rank 8, alpha 16
- Target: q_proj, k_proj, v_proj, o_proj
- 3 epochs, batch 4 × grad_accum 4 = effective 16
- LR 2e-4, cosine scheduler
- Dev eval every 50 steps, save best

## 5. Gold Baseline Target

| Metric | Qwen3.5 JSON fs | LoRA Target |
|--------|:---------------:|:-----------:|
| Exact | 42% | > 42% |
| STORE F1 | 0.963 | > 0.963 |
| Target acc | 79.1% | > 79.1% |
| SKIP F1 | 0.851 | > 0.851 |
| Parse | 100% | ≥ 96% |
| Sensitive | 0% | = 0% |

## 6. Next Step

Run 125-case QLoRA smoke training on dev only. Evaluate on dev to verify training works before scaling to 250/500.

---

*End of V0.5 LoRA Training Readiness Report.*
