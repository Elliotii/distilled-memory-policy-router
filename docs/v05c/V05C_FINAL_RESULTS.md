# V0.5c Final Results

> Qwen3.5 Unit JSON LoRA — Base-Model Ablation

## Locked-Gold Ranking

| # | System | Exact | STORE F1 | Target Acc | Sensitive |
|:-:|--------|:-----:|:--------:|:----------:|:---------:|
| 1 | Qwen3.5 JSON few-shot | 42% | 0.963 | 79.1% | 0 |
| **2** | **Qwen3.5 JSON LoRA 500** | **41%** | **0.969** | 73.7% | 5 |
| 3 | Qwen3.5 DSL few-shot | 36% | 0.959 | 77.6% | 0 |
| 4 | Qwen3-4B JSON LoRA 500 | 31% | 0.941 | 67.3% | 6 |

## Best Trained Router

**Qwen3.5 + Unit JSON QLoRA r=8 500 cases**

- 41% exact (1pp behind few-shot)
- 0.969 STORE F1 (highest of ANY system)
- 100% parse on gold
- +10pp exact over Qwen3-4B LoRA

## Key Findings

- ✅ Unit JSON is the best training interface
- ✅ Qwen3.5 is a stronger base model than Qwen3-4B for SFT
- ✅ 500-case QLoRA achieves near-few-shot exact match
- ⚠ PII safety unsolved (5 failures)
- 🎯 1pp exact gap to few-shot

---

See `reports/v05c/v05c_final_project_report.md` for full details.
