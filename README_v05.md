# Memory Policy Router — v0.5 Unit DSL Distillation

Built an evaluation and training pipeline for a memory policy router in coding-agent contexts. Compared Unit DSL and Unit JSON prompt interfaces across Qwen3-4B and Qwen3.5, trained a QLoRA learning curve (125→250→500 cases), and evaluated on a locked gold set.

---

## Task

Given runtime context, candidate memories, and current user input units, the router predicts:

```
READ m1,m2
STORE service_memory u1
STORE repo_memory u2
SKIP u3
```

Five legal STORE targets: `user_profile`, `project_memory`, `repo_memory`, `service_memory`, `task_state`. Sensitive content (credentials, PII) must always be SKIPped.

## Dataset

| Split | Cases | Usage |
|-------|:-----:|-------|
| Train | 500 | LoRA/SFT training |
| Dev | 100 | Model selection |
| Locked Gold | 100 | Final evaluation only |

Independently constructed. No ID/text overlap across splits. Gold is locked and immutable.

## Methods

- **Prompt baselines:** Unit DSL and Unit JSON zero/few-shot, Qwen3-4B and Qwen3.5
- **Deterministic baselines:** empty, top-k read, heuristic
- **LoRA:** Qwen3-4B QLoRA (rank-8, 4-bit nf4), nested subsets 125 ⊂ 250 ⊂ 500

## Key Results (Locked Gold)

| System | Exact | STORE F1 | Target Acc | Sensitive |
|--------|:-----:|:--------:|:----------:|:---------:|
| Qwen3.5 JSON few-shot | **42%** | **0.963** | **79.1%** | **0** |
| Qwen3.5 DSL few-shot | 36% | 0.959 | 77.6% | 0 |
| Qwen3-4B JSON few-shot | 26% | 0.923 | 57.5% | 0 |
| Qwen3-4B LoRA 500 | 16% | 0.946 | 47.5% | 6 failures |
| Qwen3-4B DSL few-shot | 7% | 0.850 | 60.5% | 0 |

**Dev learning curve:** STORE F1: 0.867 (125) → 0.944 (250) → 0.962 (500).

## Main Findings

- LoRA improved action-level routing (+0.096 STORE F1 over Qwen3-4B DSL few-shot) but did not beat Qwen3.5 JSON prompting
- Target classification (service_memory vs task_state) remains the bottleneck
- Sensitive safety degrades with training — credit cards, emails, phones stored as user_profile
- JSON generalized better than DSL across both models

## Limitations

Not production-safe. Target routing and sensitive safety not solved. 500 cases insufficient for 5-way target classification with class imbalance.

## Next Steps (v0.5b)

Unit JSON LoRA, target-balanced training, safety-weighted loss, larger LoRA rank, two-stage router.

## Reports

See `reports/v05/` for full experiment documentation.

---

*End of v0.5 README.*
