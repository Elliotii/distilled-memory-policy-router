# V0.5b Unit JSON LoRA Final Result Decision

**Date:** 2026-06-02  
**Context:** 5.7-E — final v0.5b locked-gold evaluation  

---

## Result: B — Unit JSON LoRA improves target routing but still trails Qwen3.5 prompting

### Supporting Evidence

1. **JSON beats DSL on gold by large margins:** exact +15pp, target accuracy +19.8pp. The interface-ablation hypothesis is confirmed.

2. **JSON beats its teacher (Qwen3-4B JSON few-shot):** exact +5pp, STORE F1 +0.018, target accuracy +9.8pp. First LoRA variant to exceed same-model prompting.

3. **JSON does NOT beat Qwen3.5 JSON few-shot:** trails by -11pp exact, -0.022 STORE F1, -11.8pp target accuracy. Qwen3.5 remains the strongest system.

4. **Safety is not improved:** 6 sensitive failures on gold (tied with DSL 500). Credentials, tokens, credit cards, and phones are stored inappropriately.

5. **Parse quality is perfect:** 100% across all 400 predictions (300 dev + 100 gold). JSON format eliminates all structural errors.

6. **Dev→gold generalization is excellent:** target accuracy gap only -1.2pp. Model is robust.

### What v0.5b Achieved

| Achievement | Evidence |
|-------------|----------|
| JSON > DSL for SFT | +19.8pp target accuracy on gold |
| JSON SFT beats JSON prompting | +5pp exact, +9.8pp target on gold |
| Perfect structural quality | 400/400 valid JSON |
| Service/task distinction learned | service_memory 70% on gold (DSL: ~25%) |
| Learning curve confirmed | All metrics improve 125→250→500 |

### What v0.5b Did NOT Achieve

| Limitation | Evidence |
|------------|----------|
| Beat Qwen3.5 prompting | -11pp exact, -0.022 STORE F1 |
| Solve sensitive safety | 6 failures (credit card, tokens, phones) |
| Perfect repo_memory | 50% accuracy — weakest class |
| Beat Qwen3.5 on SKIP F1 | 0.706 vs 0.851 |

### Why Result B (Not A)

While JSON beats DSL and beats Qwen3-4B prompting, it does not beat the overall strongest system (Qwen3.5 JSON few-shot). A "successful" interface ablation (Result A) would require JSON to be the new best system. It is a strong improvement over DSL but not the best overall.

### Why Not Result C or D

- Not C: Dev gains generalized well to gold (target acc -1.2pp gap).
- Not D: JSON clearly beats DSL and Qwen3-4B prompting — it's competitive.

---

## More-Data / Next-Experiment Decision

### Q1: Should we now add more generic data?
**No.** Target accuracy is already 67.3% with 500 cases — adding more generic cases won't fix the remaining 32.7% errors or the 6 sensitive failures. The error analysis shows specific confusion patterns and safety issues that generic data won't address.

### Q2: Should we add target/safety-focused data instead?
**Yes, as next priority.** Recommended v0.5b follow-ups:
1. **Safety-focused training** — oversample sensitive cases, add loss penalty
2. **Target-balanced training** — oversample repo_memory (weakest at 50%)
3. **Qwen3.5 JSON LoRA** — combine better base model with JSON SFT format

### Q3: Is Unit JSON now the preferred interface for future scaling?
**Yes.** JSON is clearly superior to DSL for SFT. All future training should use JSON format. The perfect parse quality alone justifies this — no more structural errors to debug.

### Q4: Should Qwen3.5 LoRA be next?
**Candidate.** Qwen3.5 JSON few-shot is 79.1% target accuracy on gold. Qwen3.5 JSON LoRA could push this higher while inheriting the JSON format benefits. But safety-focused data should come first.

### Q5: Should a gold_v2 be created before further tuned variants?
**Not yet.** Current gold is adequate for comparing JSON vs DSL (the v0.5b goal). A new gold set would be appropriate after safety/target improvements are demonstrated on dev.

### Recommended Priority

1. ✅ v0.5b Unit JSON LoRA (complete — this report)
2. Safety-focused training (sensitive case oversampling + loss penalty)
3. Target-balanced training (repo_memory oversampling)
4. Qwen3.5 JSON LoRA with safety-aware data

---

*End of V0.5b Final Result Decision.*
