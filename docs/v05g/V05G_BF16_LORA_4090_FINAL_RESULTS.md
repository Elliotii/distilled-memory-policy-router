# V0.5G BF16 LoRA 4090 Final Results

**Date:** 2026-06-08
**Status:** Complete — Final synthesis for v0.5g

---

## Quick Summary

v0.5g evaluated BF16 standard LoRA r=16 on Qwen3.5-4B (RTX 4090 24GB) with two data variants:

| Variant | Data | Purpose |
|---------|------|---------|
| 500-control | Same 500 as v05e QLoRA r16 | BF16 vs QLoRA comparison |
| 1000-targeted | 500-control + 500 targeted-balanced | Data scaling test |

**Bottom line:** 1000-targeted is the best evaluated system. BF16 alone does not help — the win comes from targeted-balanced training data.

## Key Results (gold_v2_009, 150 cases)

| Metric | BF16 500_4090 | BF16 1000_4090 | Best Previous |
|--------|:-------------:|:--------------:|:-------------:|
| Exact | 16.7% | **36.0%** | 30.7% (few-shot) |
| Parse | 98.7% | **99.3%** | 100.0% (Qwen3-4B) |
| READ F1 | 80.1% | **84.6%** | — |
| STORE F1 | 89.2% | **0.990** | 0.925 (Qwen3-4B) |
| SKIP F1 | 84.0% | **0.981** | 0.892 (QLoRA r16) |
| Target Acc | 84.7% | **100.0%** | 84.2% (QLoRA r16) |
| False Store | 10.4% | **1.2%** | — |
| Sens Store | 0/4 | 0/4 | — |

## Dev Results (100 cases)

| Metric | BF16 500_4090 | BF16 1000_4090 |
|--------|:-------------:|:--------------:|
| Exact | 49.0% | **59.0%** |
| Parse | 100.0% | 100.0% |
| READ F1 | 92.0% | **93.3%** |
| STORE F1 | 96.7% | **97.1%** |
| Target Acc | 85.3% | **89.5%** |

## Main Findings

1. **Write-side routing near-solved:** STORE F1 0.990, SKIP F1 0.981, target accuracy 100.0% on gold.
2. **READ is the bottleneck:** READ F1 84.6%, exact match only 36.0%. 64 irrelevant reads, 63 missed reads.
3. **BF16 alone insufficient:** 500-control underperforms QLoRA r16 on gold (16.7% vs 22.7%).
4. **Targeted-balanced data is the differentiator:** 1000-targeted's write-side gains (+19.3pp exact, +9.8pp STORE F1, +15.3pp target acc vs 500-control).
5. **Safety improved:** 0/4 sensitive store on gold for both variants.

## Artifacts

- **Server snapshot:** `v0.5g-bf16-lora-4090-ready / 7e40f02bbb34c2c5ecf8f7468a066cba0105db4d`
- **Adapters:** `results/v05g_bf16_lora/qwen35_json_r16_500_4090/adapter/` and `qwen35_json_r16_1000_4090/adapter/`
- **Predictions:** `data/v05g/model_predictions/bf16_r16_*_4090_*.jsonl`
- **Metrics:** `reports/v05g/server_runs/v05g_bf16_r16_*_4090_*.json`
- **gold_v2_009 hash:** `f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72` (unchanged)

## Full Reports

- `reports/v05g/v05g_bf16_lora_4090_final_report.md` — Complete synthesis
- `reports/v05g/v05g_bf16_lora_4090_gold_v2_result.md` — Gold-focused analysis
- `reports/v05g/v05g_bf16_lora_4090_error_analysis.md` — Error patterns
- `reports/v05g/v05g_bf16_lora_4090_claims_and_limitations.md` — Claim boundaries

## Next Steps

- No further v0.5 experiments recommended
- Post-result audit and v1.0 packaging
- READ-focused research for v1.0 (retrieval augmentation, graded relevance, multi-turn context)

---

*See `reports/v05g/v05g_bf16_lora_4090_final_report.md` for complete details.*
