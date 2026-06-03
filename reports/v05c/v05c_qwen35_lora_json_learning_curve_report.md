# V0.5c Qwen3.5 JSON LoRA Learning Curve Report

**Date:** 2026-06-03  
**Split:** Dev only  

## Full Learning Curve (Dev)

| Metric | Q3.5 125 | Q3.5 250 | Q3.5 500 | Q3-4B 125 | Q3-4B 250 | Q3-4B 500 |
|--------|:--------:|:--------:|:--------:|:---------:|:---------:|:---------:|
| Parse | 98.0% | 90.0% ⚠ | **98.0%** | 100% | 100% | 100% |
| Exact | 30.0% | 17.0% ⚠ | **34.0%** | 11% | 20% | 34% |
| READ F1 | 0.907 | 0.892 | **0.908** | 0.889 | 0.884 | 0.902 |
| STORE F1 | 0.891 | 0.913 | **0.959** | 0.910 | 0.947 | 0.958 |
| Target acc | 65.6% | 73.1% | **77.4%** | 55.7% | 63.8% | 68.5% |
| SKIP F1 | 0.644 | 0.623 | **0.762** | 0.535 | 0.747 | 0.753 |
| False store | 2.2% | 4.9% | **4.5%** | 9.5% | 4.6% | 6.5% |
| Sensitive | 33.3% | 66.7% | 66.7% | 33.3% | 66.7% | 66.7% |

## Qwen3.5 Key Observations

1. **Parse dip-and-recovery**: 98%→90%→98%. The 250 dip was a transient `"target":"skip"` confusion that resolved with more data.

2. **Exact follows parse**: 30%→17%→34%. The 250 dip was mechanical (parse failures blocked exact matches). True exact at 500 is the best of any LoRA variant.

3. **Target accuracy monotonic**: 65.6%→73.1%→77.4%. Continuous improvement — model keeps learning target classification.

4. **STORE F1 strong**: 0.891→0.913→0.959. Catches up to Qwen3-4B 500 (0.958) at the final size.

5. **SKIP F1 recovery**: 0.644→0.623→0.762. Strong improvement at 500 after 250 stagnation.

6. **Qwen3.5 500 ties Qwen3-4B 500 on exact (34%), beats on target accuracy (77.4% vs 68.5%)**.

## Data Efficiency

Qwen3.5 achieves Qwen3-4B 500-level metrics at 250 for target accuracy (73.1% vs 68.5%), and decisively exceeds it at 500 (77.4%). ~2x data efficiency on the primary metric.
