# V0.5 Final Project Report

**Date:** 2026-06-02  
**Status:** v0.5 experiment complete  

---

## Executive Summary

v0.5 built an end-to-end memory policy router pipeline. 700 labeled cases (500 train, 100 dev, 100 locked gold), 12+ baseline comparisons, and a QLoRA learning curve (125→250→500). Qwen3.5 JSON few-shot (42% exact, 0.963 STORE F1, 0% sensitive) is the strongest system. LoRA improves action routing but target classification and safety remain bottlenecks. v0.5 is a successful diagnostic experiment with clear next steps for v0.5b.

## Problem

A memory policy router decides which candidate memories to READ and which current user input units to STORE or SKIP. Output is Unit DSL: `READ m1,m2 / STORE service_memory u1 / SKIP u2`. Five legal targets: user_profile, project_memory, repo_memory, service_memory, task_state. Sensitive content (credentials, PII) must always be SKIPped.

## Data

| Split | Cases | Source | Usage |
|-------|:-----:|--------|-------|
| Train | 500 | Corrected batch500 | LoRA/SFT training |
| Dev | 100 | Independent generation | Model selection |
| Gold | 100 | Independent generation, locked | Final eval only |

No ID overlap, no exact text overlap, 0 hard leakage blockers.

## Baselines

12 systems evaluated: empty, topk_read, heuristic, Qwen3-4B DSL/JSON zero/few-shot, Qwen3.5 DSL/JSON zero/few-shot, and LoRA 125/250/500. DeepSeek teacher deferred.

## LoRA

Qwen3-4B Unit DSL QLoRA (rank-8, alpha-16, 3 epochs, 4-bit nf4). Nested subsets: 125 ⊂ 250 ⊂ 500.

**Dev learning curve:**

| | 125 | 250 | 500 |
|---|:---:|:---:|:---:|
| Exact | 12% | 14% | 24% |
| STORE F1 | 0.867 | 0.944 | 0.962 |
| Target acc | 60% | 55.7% | 54.1% |

**Final gold comparison:**

| System | Exact | STORE F1 | Target Acc | Sensitive |
|--------|:-----:|:--------:|:----------:|:---------:|
| Qwen3.5 JSON fs | **42%** | **0.963** | **79.1%** | **0** |
| Qwen3.5 DSL fs | 36% | 0.959 | 77.6% | 0 |
| Qwen3-4B JSON fs | 26% | 0.923 | 57.5% | 0 |
| LoRA 500 | 16% | 0.946 | 47.5% | 6 failures |
| Qwen3-4B DSL fs | 7% | 0.850 | 60.5% | 0 |

## Findings

1. **LoRA improves action routing** (+0.096 STORE F1 over Qwen3-4B DSL few-shot) but doesn't match Qwen3.5
2. **Target classification is the bottleneck** — service_memory at 25% accuracy on gold
3. **Safety degrades with training** — credit card, email, phone stored as user_profile
4. **JSON generalized better than DSL** across both models

## Limitations

Small data (500 cases), target class imbalance, safety not explicitly trained, QLoRA rank-8 may be insufficient.

## v0.5b

Unit JSON LoRA, target-balanced data, safety-weighted loss, larger LoRA rank, more epochs.

---

*End of V0.5 Final Project Report.*
