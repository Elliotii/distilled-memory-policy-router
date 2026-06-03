# V0.5c Qwen3.5 Unit JSON LoRA — Experiment Plan

**Date:** 2026-06-02  
**Context:** 5.9-A — Feasibility and planning  
**Status:** Plan  

---

## 1. Motivation from v0.5b

V0.5b Unit JSON LoRA produced the following locked-gold results on Qwen3-4B:

| System | Exact | STORE F1 | Target Acc | Sensitive |
|--------|:-----:|:--------:|:----------:|:---------:|
| Qwen3.5 JSON fs | 42% | 0.963 | 79.1% | 0 |
| JSON LoRA 500 (Qwen3-4B) | 31% | 0.941 | 67.3% | 6 |
| Qwen3-4B JSON fs | 26% | 0.923 | 57.5% | 0 |

Key findings from v0.5b:
- **Unit JSON SFT is clearly superior to Unit DSL SFT** (+19.8pp target accuracy on gold).
- **Qwen3-4B JSON LoRA 500 beats its teacher** (Qwen3-4B JSON few-shot) on exact, STORE F1, and target accuracy.
- **Qwen3-4B JSON LoRA 500 still trails Qwen3.5 JSON few-shot** by 11pp exact and 11.8pp target accuracy.
- **Safety remains unsolved** (6 sensitive failures, tied with DSL).
- **Unit JSON is the preferred training interface** for all future work.

The gap between Qwen3-4B JSON LoRA and Qwen3.5 JSON few-shot raises a natural question: how much of the gap is due to base model capacity, and can Qwen3.5 + JSON SFT close or beat Qwen3.5 JSON few-shot?

## 2. Hypothesis

**Qwen3.5 + Unit JSON QLoRA can close or beat the Qwen3.5 JSON few-shot prompting baseline on locked gold**, because:
1. Qwen3.5 is a stronger base model than Qwen3-4B (demonstrated by +16pp exact advantage in few-shot prompting).
2. JSON SFT beats JSON few-shot on the SAME base model (demonstrated on Qwen3-4B: LoRA 500 beats Qwen3-4B JSON fs by +5pp exact).
3. If the same SFT advantage holds for Qwen3.5, Qwen3.5 JSON LoRA should reach ~37-47% exact on gold, potentially beating Qwen3.5 JSON few-shot (42%).

## 3. Experiment Definition

**Question:** Can Qwen3.5 + Unit JSON QLoRA close the gap to Qwen3.5 JSON few-shot prompting, or beat it?

### Controlled Variables
| Variable | Value |
|----------|-------|
| Training interface | Unit JSON (same as v0.5b) |
| Train subsets | 125 ⊂ 250 ⊂ 500 (same case IDs as v0.5b) |
| Dev set | 100 cases (same as v0.5/v0.5b) |
| Locked gold | 100 cases (same as v0.5/v0.5b) |
| SFT format | Chat messages (same as v0.5b JSON) |
| Eval runner | Same `eval_lora_router.py --interface unit_json` |
| Metrics | Same: parse, exact, READ F1, STORE F1, target acc, SKIP F1, sensitive |
| QLoRA defaults | r=8, alpha=16, 3 epochs, 4-bit nf4, LR=2e-4 |

### Changed Variable
| Variable | v0.5b | v0.5c |
|----------|-------|-------|
| Base model | Qwen3-4B-Instruct-2507 | **Qwen3.5-4B** |
| LoRA target modules | q/k/v/o_proj | q/k/v/o_proj + in_proj_qkv + out_proj |

The LoRA target_modules change is forced by architectural differences: Qwen3.5 has 24 linear_attn + 8 self_attn layers vs Qwen3-4B's 36 self_attn layers. The expanded modules provide coverage of both attention types.

## 4. Expected Metrics

Based on Qwen3-4B JSON LoRA results and the Qwen3.5 few-shot advantage:

| System | Exact (est.) | STORE F1 (est.) | Target Acc (est.) |
|--------|:------------:|:---------------:|:-----------------:|
| Qwen3.5 JSON fs (gold) | 42% | 0.963 | 79.1% |
| Qwen3.5 JSON LoRA 500 (target) | **37-47%** | **0.950-0.965** | **75-82%** |
| Qwen3-4B JSON LoRA 500 (gold) | 31% | 0.941 | 67.3% |

## 5. Success Criteria

| Tier | Criterion | Threshold |
|------|-----------|:---------:|
| **A — Breakthrough** | Qwen3.5 JSON LoRA beats Qwen3.5 JSON fs on STORE F1 AND target accuracy | Both > fs |
| **B — Positive** | Qwen3.5 JSON LoRA beats Qwen3-4B JSON LoRA 500 on exact AND target accuracy | Exact > 31%, Target > 67.3% |
| **C — Partial** | Qwen3.5 JSON LoRA beats Qwen3-4B JSON LoRA on some metrics but not all | Mixed |
| **D — Negative** | Qwen3.5 JSON LoRA does not beat Qwen3-4B JSON LoRA | Below v0.5b |
| **F — Failed** | Training crashes, OOM, NaN loss, or parse < 80% | Technical failure |

## 6. Gold-Use Policy

| Rule | Status |
|------|:------:|
| Gold is locked (v05_gold_001, SHA-256: `56e16078...`) | ✅ |
| Gold only for predeclared final eval after 500 training | ✅ |
| No gold used during 125/250/500 training or dev eval | ✅ |
| No gold used for model selection or hyperparameter tuning | ✅ |
| Gold already evaluated once (v0.5 DSL LoRA 500, v0.5b JSON LoRA 500) | ⚠ Not fully blind for v0.5c |
| Gold_v2 consideration deferred until after safety/target improvements | N/A |

Since gold has been evaluated twice (v0.5 DSL 500 and v0.5b JSON 500), it is not fully blind for v0.5c. However, the v0.5c experiment is a *model-capacity ablation* — the base model changes while the data, interface, and eval protocol stay the same. The risk of gold overfitting from prior evaluations is low because:
1. No hyperparameter tuning was done on gold.
2. The train subsets (125/250/500) are derived from the train-pool, not gold.
3. The dev set handles all development decisions.

## 7. Experiment Phases

| Phase | Context | Description |
|-------|---------|-------------|
| 1 — Planning | 5.9-A (this) | Feasibility, configs, readiness |
| 2 — Smoke | 5.9-B | Train Qwen3.5 JSON LoRA 125, dev eval, decide |
| 3 — Scale | 5.9-C | Train 250 if smoke passes |
| 4 — Scale | 5.9-D | Train 500 if 250 passes |
| 5 — Gold | 5.9-E | Locked-gold final eval of Qwen3.5 JSON LoRA 500 |

## 8. Relationship to Other Planned Work

| Work | Priority | Relationship |
|------|:--------:|--------------|
| Safety-focused training (v0.5c original plan) | Deferred | Separate ablation; Qwen3.5 run uses same data |
| Target-balanced training | Deferred | Separate ablation |
| Qwen3.5 JSON LoRA (this) | **Current** | Model-capacity ablation after interface ablation |
| gold_v2 | Future | New gold set for final multi-ablation claims |

---

*End of V0.5c Qwen3.5 JSON LoRA Experiment Plan.*
