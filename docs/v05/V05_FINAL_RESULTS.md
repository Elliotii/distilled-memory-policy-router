# V0.5 Final Results

## Locked Gold Comparison

| System | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON few-shot | **42%** | **0.963** | **79.1%** | **0.851** | **0** |
| Qwen3.5 DSL few-shot | 36% | 0.959 | 77.6% | 0.795 | 0 |
| Qwen3-4B JSON few-shot | 26% | 0.923 | 57.5% | 0.766 | 0 |
| Qwen3-4B LoRA 500 | 16% | 0.946 | 47.5% | 0.718 | 6 fails |
| Qwen3-4B DSL few-shot | 7% | 0.850 | 60.5% | 0.422 | 0 |

## Dev LoRA Learning Curve

| | 125 | 250 | 500 |
|---|:---:|:---:|:---:|
| Exact | 12% | 14% | 24% |
| STORE F1 | 0.867 | 0.944 | 0.962 |
| Target acc | 60% | 55.7% | 54.1% |

## Verdict

LoRA improves action routing but does not beat Qwen3.5 prompting. Target classification and safety are unresolved.

## Detailed reports

See `reports/v05/v05_final_*.md`.
