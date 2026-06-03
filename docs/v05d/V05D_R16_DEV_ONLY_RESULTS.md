# V0.5d r=16 Dev-Only Results

> Qwen3.5 Unit JSON QLoRA r=16 — Capacity Ablation

## Key Result

**r=16 improves dev exact over r=8 by +5pp (39% vs 34%).**

All metrics improve. No degradation. r=16 is the best dev-performing QLoRA setting.

## Dev Metrics

| Metric | r=16 | r=8 | Δ |
|--------|:----:|:---:|:--:|
| Exact | **39.0%** | 34.0% | +5.0pp |
| Parse | **99.0%** | 98.0% | +1.0pp |
| STORE F1 | **0.968** | 0.959 | +0.009 |
| SKIP F1 | **0.819** | 0.762 | +0.057 |

## Status

- ✅ Dev-only: complete
- ⚠ Gold: NOT evaluated
- 🎯 Next: gold_v2 recommended for final r=16 claim

## Current Best

- **Best gold-verified trained:** Qwen3.5 r=8 (41% exact on gold)
- **Best dev performer:** Qwen3.5 r=16 (39% exact on dev)
- **Best overall:** Qwen3.5 JSON few-shot (42% exact on gold)

---

See `reports/v05d/v05d_final_dev_only_summary.md`.
