# V0.5c Project Narrative

## The Story So Far

### v0.5 (Qwen3-4B Unit DSL LoRA)
We trained Qwen3-4B with Unit DSL (text-based READ/STORE/SKIP). It improved action routing (+0.096 STORE F1 over few-shot) but failed target classification (47.5% on gold) and had 6 sensitive failures. Qwen3.5 JSON few-shot was clearly superior.

### v0.5b (Qwen3-4B Unit JSON LoRA)
We switched the training interface from DSL to JSON. This was a breakthrough: +19.8pp target accuracy on gold. JSON eliminated parse errors and enabled learnable target classification. But Qwen3.5 few-shot was still #1, and 6 sensitive failures persisted.

### v0.5c (Qwen3.5 Unit JSON LoRA) — THIS EXPERIMENT
**Question:** If JSON SFT works better on Qwen3-4B, what happens with a stronger base model?

**Answer:** Qwen3.5 + JSON SFT achieves 41% exact on gold — within 1pp of Qwen3.5 JSON few-shot. It has the highest STORE F1 (0.969) of any system. It beats Qwen3-4B JSON LoRA by +10pp exact.

**But:** Qwen3.5 JSON few-shot remains #1 overall (42% exact, 79.1% target, 0 sensitive). The trained system still has 5 PII storage failures.

## What We Learned

1. **Interface matters more than we thought.** JSON SFT is dramatically better than DSL SFT (+19.8pp target accuracy).

2. **Base model matters next.** Qwen3.5 gives +10pp exact over Qwen3-4B with the same training setup.

3. **QLoRA r=8 with 500 cases is very close to few-shot.** The 1pp exact gap suggests standard LoRA or r=16 could close it.

4. **Safety is the hardest problem.** Neither interface change nor base model upgrade solves PII storage. This requires dedicated safety training.

## The 1pp Gap

| What | Exact |
|------|:-----:|
| Qwen3.5 JSON few-shot | 42% |
| Qwen3.5 JSON LoRA 500 | 41% |
| Gap | **1pp** |

We are ONE percentage point from having a trained small router that matches the strongest few-shot baseline on exact match — and already beats it on STORE F1. This is within reach of modest capacity increases (r=16, standard LoRA).

## Remaining Work

- Standard LoRA / r=16 to close the 1pp exact gap
- Safety-focused training to eliminate PII storage
- gold_v2 for clean evaluation of tuned variants

---

*See `reports/v05c/v05c_final_project_report.md` for full details.*
