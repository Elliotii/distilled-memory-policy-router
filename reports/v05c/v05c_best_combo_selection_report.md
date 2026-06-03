# V0.5c Best Combo Selection Report

**Date:** 2026-06-04  
**Split:** Locked gold  

## Best Trained Small Router

**Qwen3.5 + Unit JSON QLoRA r=8 500**

| Metric | Value |
|--------|:-----:|
| Exact | 41% |
| STORE F1 | 0.969 |
| Target acc | 73.7% |
| SKIP F1 | 0.847 |

Beats Qwen3-4B JSON LoRA 500 by +10pp exact, +6.4pp target acc, +0.028 STORE F1. The clear winner among trained systems.

## Best Prompting Baseline

**Qwen3.5 + Unit JSON few-shot**

| Metric | Value |
|--------|:-----:|
| Exact | 42% |
| STORE F1 | 0.963 |
| Target acc | 79.1% |
| SKIP F1 | 0.851 |
| Sensitive | 0 |

Remains the strongest overall system. Zero sensitive failures.

## Best Overall System

**Qwen3.5 JSON few-shot** — leads on exact (42% vs 41%), target accuracy (79.1% vs 73.7%), and safety (0 vs 5). However, Qwen3.5 JSON LoRA 500 leads on STORE F1 (0.969 vs 0.963).

## Best Future Training Interface

**Unit JSON** — confirmed by three experiments:
- v0.5b: JSON SFT > DSL SFT (+19.8pp target acc on Qwen3-4B)
- v0.5c: JSON SFT on Qwen3.5 achieves 41% exact, 100% parse
- JSON format eliminates parse errors, enables learnable target classification

## Best Candidate for Scaling

**Qwen3.5 + Unit JSON + Standard LoRA/BF16 + r=16 + more data** — the most promising direction for future improvement. Qwen3.5 QLoRA r=8 already achieves 41% exact on gold. Higher-rank LoRA or full BF16 training could close the remaining 1pp gap to few-shot.

## Summary Table

| Category | Winner | Detail |
|----------|--------|--------|
| Best trained router | Qwen3.5 JSON LoRA 500 | 41% exact, #2 overall |
| Best prompting | Qwen3.5 JSON few-shot | 42% exact, #1 overall |
| Best overall | Qwen3.5 JSON few-shot | Clean safety |
| Best interface | Unit JSON | Proven across 2 models |
| Best base model for SFT | Qwen3.5 | +10pp over Qwen3-4B |
| Next to scale | Qwen3.5 + Standard LoRA | 1pp gap to close |
