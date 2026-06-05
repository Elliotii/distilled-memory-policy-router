# V0.5e Final Results

> gold_v2_009 four-system evaluation

## gold_v2_009 Results (150 cases)

| System | Exact | Parse | STORE F1 | Target Acc |
|--------|:-----:|:-----:|:--------:|:----------:|
| Qwen3.5 few-shot | 30.7% | 86.0% | 0.856 | 75.3% |
| Qwen3.5 r=16 | 22.7% | 94.7% | 0.909 | 84.2% |
| Qwen3.5 r=8 | 22.7% | 98.7% | 0.880 | 79.1% |
| Qwen3-4B r=8 | 16.0% | 100.0% | 0.925 | 76.8% |

## r16 vs r8

Paired Δ = 0.00pp, 95% CI [−5.33, +5.33]  
**Statistically indistinguishable on exact.**  
r16 improves write-side routing; r8 is more parse-stable.

## Key Findings
- r16 does NOT significantly beat r8 on primary metric
- r16 directionally improves STORE F1, target accuracy, SKIP F1
- r8 has better parse (98.7% vs 94.7%)
- Qwen3.5 few-shot leads exact but has poor parse on v009
- Qwen3.5 > Qwen3-4B for exact on this task

---

See `reports/v05e/v05e_final_project_report.md`.
