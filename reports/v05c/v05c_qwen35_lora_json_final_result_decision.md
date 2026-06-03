# V0.5c Qwen3.5 JSON LoRA — Final Result Decision

**Date:** 2026-06-04  
**Context:** 5.9-E — Locked-gold final eval  

---

## Decision: Result B+ — Qwen3.5 JSON LoRA ultra-competitive, best trained system, but Qwen3.5 prompting still #1 overall

### What "B+" means

"B" because Qwen3.5 JSON LoRA does not beat Qwen3.5 JSON few-shot overall. "+" because it achieves:
- Highest STORE F1 of ANY system (0.969)
- Within 1pp of few-shot on exact (41% vs 42%)
- Within 0.004 of few-shot on SKIP F1 (0.847 vs 0.851)
- Perfect parse on gold (100%)
- Best trained system by a wide margin

### Evidence

| Claim | Evidence |
|-------|----------|
| Best STORE F1 overall | 0.969 vs Qwen3.5 fs 0.963 |
| Beats Qwen3-4B LoRA decisively | +10pp exact, +6.4pp target |
| Beats Qwen3-4B few-shot | +15pp exact, +0.046 STORE F1 |
| Ultra-close to few-shot | 1pp exact gap (narrowest of any LoRA) |
| Perfect parse on gold | 100% — 0 structural errors |
| Better credential safety | 0 credential stores (vs Qwen3-4B's 2) |

### Limitations

| Limitation | Detail |
|------------|--------|
| Target acc trails few-shot | 73.7% vs 79.1% (−5.4pp) |
| 5 sensitive failures | PII stored as user_profile |
| Not production-safe | Phones, addresses, emails stored |
| QLoRA only | Standard LoRA/BF16 not tested |

### Ranking

1. **Qwen3.5 JSON few-shot** — Best overall (42% exact, 0 sensitive)
2. **Qwen3.5 JSON LoRA 500** — Best trained (41% exact, 0.969 STORE F1)
3. Qwen3.5 DSL few-shot — Strong baseline (36% exact, 0 sensitive)
4. Qwen3-4B JSON LoRA 500 — Previous best trained (31% exact)
5+ others...

### What This Experiment Achieved

1. ✅ **Base-model ablation complete** — Qwen3.5 is clearly better than Qwen3-4B for JSON SFT
2. ✅ **Interface ablation confirmed** — Unit JSON SFT is the preferred training interface
3. ✅ **Qwen3.5 LoRA is ultra-competitive with few-shot** — 1pp exact gap
4. ✅ **Credential safety improved** — No token/credit card storage
5. ⚠ **PII safety unsolved** — Phones/addresses/emails still stored
6. ❌ **Few-shot not beaten** — Qwen3.5 prompting remains #1 overall
