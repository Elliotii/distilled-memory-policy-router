# v0.5g BF16 LoRA 4090 — gold_v2_009 Result

**Date:** 2026-06-08
**Focus:** Gold v2_009 evaluation of BF16 r16 500_4090 vs 1000_4090 vs previous best systems

---

## 1. Gold Results (150 active cases, gold_v2_009)

### 1.1 500-control vs 1000-targeted

| Metric | BF16 r16 500_4090 | BF16 r16 1000_4090 | Δ |
|--------|:-----------------:|:------------------:|:--:|
| Parse success | 98.7% (148/150) | 99.3% (149/150) | +0.6pp |
| Exact match | 16.7% (25/150) | **36.0%** (54/150) | **+19.3pp** |
| READ F1 | 80.1% | **84.6%** | +4.5pp |
| STORE F1 | 89.2% | **99.0%** | **+9.8pp** |
| SKIP F1 | 84.0% | **98.1%** | **+14.1pp** |
| Target accuracy | 84.7% | **100.0%** | **+15.3pp** |
| False store rate | 10.4% | **1.2%** | −9.2pp |
| Irrelevant read rate | 10.0% | 15.5% | +5.5pp |
| Sensitive store | 0/4 (0.0%) | 0/4 (0.0%) | 0 |

**500-control gold generalization failure:** The 500-control adapter (trained on same data as v05e QLoRA r16) degrades sharply on gold: exact 16.7% (vs QLoRA r16's 22.7%), STORE F1 0.892 (vs 0.909). BF16 alone does not replicate QLoRA performance on this gold set under the 4090 config.

**1000-targeted gold generalization success:** Adding 500 targeted-balanced cases transforms gold performance: exact +19.3pp, STORE F1 +9.8pp, SKIP F1 +14.1pp, target accuracy reaches 100.0%.

### 1.2 1000-targeted vs Previous Best Systems

| System | Exact | Parse | READ F1 | STORE F1 | SKIP F1 | Target Acc | False Store | Sens Store |
|--------|:-----:|:-----:|:-------:|:--------:|:-------:|:----------:|:-----------:|:----------:|
| **BF16 r16 1000_4090** | **36.0%** | 99.3% | 84.6% | **0.990** | **0.981** | **100.0%** | 1.2% | 0/4 |
| Qwen3.5 JSON few-shot | 30.7% | 86.0% | — | 0.856 | 0.847 | 75.3% | — | 0%* |
| Qwen3.5 QLoRA r16 500 | 22.7% | 94.7% | — | 0.909 | 0.892 | 84.2% | — | 0%* |
| Qwen3.5 QLoRA r8 500 | 22.7% | 98.7% | — | 0.880 | 0.834 | 79.1% | — | 0%* |
| Qwen3-4B QLoRA r8 500 | 16.0% | 100.0% | — | 0.925 | 0.860 | 76.8% | — | 100%* |

*Note: v05e sensitive store rates used eval_runner tag-based detection. v05g uses semantic sensitive-unit detection (match against `sensitive_boundary` tag). Different methodology — not directly comparable.

## 2. Metric-by-Metric Interpretation

### Exact Match
- **1000-targeted: 36.0%** — Best of any evaluated system on gold_v2_009 (beats few-shot 30.7% by +5.3pp).
- **500-control: 16.7%** — Worst of any Qwen3.5 system. BF16 alone lost ~6pp vs QLoRA r16.
- Gap: 19.3pp between the two BF16 variants. The targeted-balanced data, not BF16 precision, drives exact improvement.

### Parse Success
- **1000-targeted: 99.3%** — 1 parse failure (invalid_unit_id_rate: 1/401 predicted).
- **500-control: 98.7%** — 2 parse failures (1 "unit in both STORE and SKIP", 1 "missing unit assignment").
- Both within normal range. 1000-targeted slightly cleaner despite generating more output.

### READ F1
- **1000-targeted: 84.6%** — Best among systems with READ F1 reported, but still the weakest metric.
- **500-control: 80.1%** — READ recall drops to 72.2% on gold (from 95.6% on dev). Major generalization failure.
- Irrelevant read rate 15.5% (1000) — model reads too many memories (414 predicted reads vs 331 for 500-control).
- READ remains the dominant exact-match bottleneck.

### STORE F1
- **1000-targeted: 0.990** — Near-perfect store-side routing. 240/242 store units correct (3 FP, 2 FN).
- **500-control: 0.892** — Significant regression; 25 false stores out of 240 predicted.
- BF16 r16 1000_4090 STORE F1 (0.990) dramatically exceeds old QLoRA r16's best (0.909).

### SKIP F1
- **1000-targeted: 0.981** — Near-perfect skip routing. Only 1 FP, 5 FN.
- **500-control: 0.840** — 23 false skips out of 154 predicted.
- SKIP was historically a weak metric (few-shot 0.847, QLoRA r16 0.892). 1000-targeted solves it almost entirely.

### Target Accuracy
- **1000-targeted: 100.0%** — Perfect. 240/240 STORE units assigned correct memory type.
- **500-control: 84.7%** — 33 of 215 units misclassified.
- Target confusion matrix for 1000-targeted is diagonal — zero off-diagonal entries. This is unprecedented in the project.
- Project_memory 32/32, repo_memory 37/37, service_memory 75/75, task_state 82/82, user_profile 14/14.

### False Store Rate
- **1000-targeted: 1.2%** — Only 3 false stores out of 243 predicted (down from 10.4% for 500-control).
- **500-control: 10.4%** — 25 false stores. Unacceptable for production-adjacent use.

### Sensitive Store
- **Both: 0/4** — No genuine sensitive units stored. Semantic check (not tag-based). Strong improvement over historical Qwen3-4B systems (which had 6 genuine failures).

## 3. Interpretation Boundaries

### What This Result Means
- Write-side routing (STORE/SKIP + target classification) is effectively solved for this dataset.
- The 1000-targeted adapter routes store/skip decisions and memory-type targets with near-perfect accuracy.
- BF16 standard LoRA + targeted-balanced data + r=16 is a viable training recipe.

### What This Result Does NOT Mean
- **READ is not solved.** READ F1 84.6% leaves significant room. Exact match (36.0%) reflects the READ bottleneck.
- **Not a production system.** Synthetic gold, template-generated training data, single-split evaluation.
- **Not pure data causality.** 1000-targeted adds both volume and domain/template-family diversity. Cannot isolate which drove improvement.
- **Not a planned larger-GPU result.** RTX 4090 fallback config used halved batch size and gradient checkpointing. Other hardware settings might differ.
- **No downstream validation.** Router predictions not tested with an actual retriever or coding agent.
- **No claim of BF16 superiority.** 500-control underperforms QLoRA r16. BF16 alone does not help.

---

*End of v0.5g BF16 LoRA 4090 gold_v2_009 Result.*
