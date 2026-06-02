# V0.5 Qwen Full Dev Selection Report

**Date:** 2026-06-02  
**Context:** 5.4-D — model/interface selection recommendation for locked gold  

---

## 1. Recommended System for Locked Gold

### Primary: Qwen3.5 Unit DSL Few-Shot

| Metric | Value | Rank |
|--------|:-----:|:----:|
| Parse success | 99.0% | #1 |
| Exact match | 41.0% | #1 |
| STORE unit F1 | 0.975 | #1 |
| STORE target accuracy | 74.8% | #1 |
| SKIP F1 | 0.864 | #2 |
| READ F1 | 0.912 | #1 |
| False store rate | 2.3% | #2 |

**Qwen3.5 DSL few-shot leads on 5 of 7 primary metrics.** It is the recommended system for locked gold baseline evaluation.

### Secondary: Qwen3.5 Unit JSON Few-Shot

Best SKIP F1 (0.903), lowest false store rate (1.0%). JSON parsability is 98.0%. Recommended as the JSON interface baseline for locked gold.

### DSL vs JSON Decision

**Unit DSL remains primary.** Despite JSON having slightly better structural metrics in some areas, DSL is the interface our LoRA/SFT training uses, making it the natural comparison point.

**Unit JSON should be included as a fallback baseline** on locked gold to verify the DSL advantage is real.

## 2. Recommended LoRA Base Model

### Qwen3-4B remains the LoRA base candidate

Reasons:
- Qwen3-4B few-shot performs competitively (0.936 STORE F1, 71.1% target acc)
- Already integrated with existing SFT training pipeline
- Smaller disk footprint (7.6 GB vs 8.8 GB)
- Faster inference (~0.7s vs ~1.2s)
- The LoRA training should close the gap between Qwen3-4B and Qwen3.5

**Qwen3.5 LoRA is a future experiment** if Qwen3-4B LoRA underperforms or if resources permit.

## 3. Zero-Shot vs Few-Shot

| Variant | Qwen3-4B Parse | Qwen3.5 Parse | Recommendation |
|---------|:-------------:|:-------------:|----------------|
| DSL zero-shot | 43.0% | 47.0% | **Skip for locked gold** — too low |
| DSL few-shot | 96.0% | 99.0% | **Primary for locked gold** |
| JSON zero-shot | 97.0% | 97.0% | Optional fallback |
| JSON few-shot | 99.0% | 98.0% | Secondary for locked gold |

**Zero-shot DSL should NOT be run on locked gold** — parse success too low. Few-shot is the viable approach for both models.

## 4. Recommended Gold Baseline Systems

For locked gold evaluation (Context 5.4-E), run:

| # | System | Priority |
|---|--------|:--------:|
| 1 | Qwen3.5 DSL few-shot | **Primary** |
| 2 | Qwen3.5 JSON few-shot | Secondary |
| 3 | Qwen3-4B DSL few-shot | Comparison |
| 4 | Qwen3-4B JSON few-shot | Comparison |
| 5 | empty baseline | Floor |
| 6 | topk_read baseline | Retrieval floor |
| 7 | heuristic baseline | Rule-based comparison |

DeepSeek teacher reference: Defer to when API is available.

## 5. Sensitive Store Warning

All model systems show 33.3% sensitive store rate on dev. This means ~3-4 sensitive units are being incorrectly stored across 10 sensitive_boundary cases.

| Implication | Action |
|-------------|--------|
| Zero/few-shot models don't consistently SKIP sensitive content | Monitor on locked gold |
| LoRA training expected to improve this | Priority for training |
| Locked gold sensitive store = 0 is a hard go/no-go gate | Validate after training |

## 6. Risks and Caveats

1. **Dev selection bias:** Choosing Qwen3.5 based on dev may not translate to locked gold. Gold is the final arbiter.
2. **Sensitive store:** 33.3% on dev is concerning but not blocking — dev is for selection, gold for evaluation.
3. **Small N:** 100 dev cases is sufficient for selection but not for final statistical claims.
4. **No DeepSeek teacher:** Teacher ceiling comparison deferred.
5. **Dev metrics are diagnostics only** — do not report as final results.

---

*End of V0.5 Qwen Full Dev Selection Report.*
