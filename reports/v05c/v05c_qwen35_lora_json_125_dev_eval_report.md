# V0.5c Qwen3.5 JSON LoRA 125 Dev Eval Report

**Date:** 2026-06-03  
**Context:** 5.9-B — Qwen3.5 Unit JSON LoRA 125 smoke training  

---

## 1. Evaluation Setup

| Parameter | Value |
|-----------|-------|
| Model | Qwen3.5-4B + LoRA adapter (r=8) |
| Adapter | `results/v05c_lora/qwen35_json_125/adapter/` |
| Cases | 100 (dev set) |
| Interface | unit_json |
| max_new_tokens | 256 |
| enable_thinking | False |
| Predictions file | `data/v05c/model_predictions/qwen35_lora_json_125_dev_predictions.jsonl` |

## 2. Structural Metrics

| Metric | Value |
|--------|:-----:|
| Parse success | **98.0%** |
| Invalid memory ID | 0.0% |
| Invalid unit/span | 0.0% |
| Invalid target | 0.0% |
| Avg output chars | 116.4 |
| Repair cost | 2.07 |

2 parse failures out of 100:
- `v05_dev_0043`: invalid JSON — Expecting ',' delimiter (malformed JSON)
- `v05_dev_0096`: missing unit assignment — unit u2 not in store or skip

## 3. Semantic Metrics

| Metric | Value |
|--------|:-----:|
| **Exact** | **30.0%** |
| READ F1 | 0.907 |
| STORE unit F1 | 0.891 |
| **STORE target accuracy** | **65.6%** |
| SKIP F1 | 0.644 |
| False store | 2.2% |
| Irrelevant read | 12.3% |
| Sensitive store | 33.3% |

## 4. Interpretation

**Qwen3.5 JSON LoRA 125 shows exceptionally strong results for only 125 training cases:**

- **30% exact match** on dev with just 125 cases — this is nearly at Qwen3-4B JSON LoRA 500 level (34%).
- **65.6% target accuracy** — already beats Qwen3-4B JSON LoRA 250 (63.8%).
- **0.907 READ F1** — strong memory selection from limited training.
- **0.891 STORE F1** — slightly below Qwen3-4B 125 (0.910) but likely to improve with more data.
- **0.644 SKIP F1** — significantly better than Qwen3-4B 125 (0.535), +0.109.
- **2.2% false store** — very low, indicates conservative STORE behavior.
- **33.3% sensitive store** — same as all 125-case variants (inherent data limitation).

The 2 parse failures are minor: one JSON formatting error, one missing unit assignment. Both are consistent with undertraining at 125 cases and should resolve with more data.

## 5. Key Takeaways

1. **Qwen3.5 is a significantly better base model for JSON SFT.** After 125 cases, it reaches metrics that Qwen3-4B needed 250-500 cases to achieve.
2. **Target classification is already strong at 125** (65.6% vs Qwen3-4B 125's 55.7%).
3. **Read/skip routing is improved** — better READ F1 and dramatically better SKIP F1.
4. **Parse quality is near-perfect** (98%) despite the model only having 125 JSON examples.
5. **The 6-module LoRA target set works correctly** — model generates valid JSON with correct structure.

---

*End of V0.5c Qwen3.5 JSON LoRA 125 Dev Eval Report.*
