# V0.5c Qwen3.5 JSON LoRA 500 Target Confusion Audit

**Date:** 2026-06-03  
**Split:** Dev only  

## Overall

| Metric | Qwen3.5 500 | Qwen3-4B 500 |
|--------|:-----------:|:------------:|
| Target accuracy | **77.4%** | 68.5% |
| Error rate | 22.6% | 31.5% |

Qwen3.5 reduces target errors by ~28% relative (22.6% vs 31.5%).

## Qwen3.5 Target Accuracy Progression

| Size | Target Acc |
|:----:|:----------:|
| 125 | 65.6% |
| 250 | 73.1% |
| 500 | **77.4%** |

Monotonic improvement — model continues learning target classification through 500.

## Comparison to Few-Shot Baselines (Gold)

| System | Target Acc |
|--------|:----------:|
| Qwen3.5 JSON few-shot gold | 79.1% |
| **Qwen3.5 LoRA 500 dev** | **77.4%** |
| Qwen3.5 DSL few-shot gold | 77.6% |
| Qwen3-4B JSON few-shot gold | 57.5% |

Qwen3.5 LoRA 500 dev (77.4%) is approaching Qwen3.5 few-shot gold (79.1%) — only 1.7pp gap. This is the closest any LoRA variant has come to the few-shot baseline.

## Expected Confusion Patterns

Based on v0.5b analysis, dominant confusions are:
1. service_memory ↔ task_state (most common)
2. repo_memory → project_memory
3. user_profile confusions

Detailed per-target breakdown deferred to locked-gold evaluation where per-case analysis is possible.
