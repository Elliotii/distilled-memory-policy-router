# V0.5b Unit JSON LoRA Plan

**Date:** 2026-06-02  
**Status:** Planning / Rendering / Readiness — Do NOT train  

---

## Experiment Definition

### Question

Does Unit JSON LoRA improve target classification and safety compared with Unit DSL LoRA?

### Motivation

V0.5 final results showed:

- **Qwen3.5 JSON few-shot** was the strongest prompting system (42% exact, 0.963 STORE F1, 0 sensitive on gold).
- **Qwen3-4B LoRA (DSL)** improved action routing (+0.096 STORE F1 over DSL few-shot) but target classification and safety were bottlenecks:
  - Target accuracy: 47.5% on gold (vs 79.1% for Qwen3.5 JSON fs)
  - Sensitive: 6 failures on gold (credit card, emails, phones, addresses stored as user_profile)
  - Service memory target accuracy: 25% (model cannot distinguish svc from task_state)

The Unit JSON interface consistently generalized better than DSL across both models (Qwen3.5 JSON fs beat Qwen3.5 DSL fs; Qwen3-4B JSON fs beat Qwen3-4B DSL fs). This ablation tests whether SFT training benefits from the stronger JSON interface.

### Hypothesis

Training the router to output Unit JSON (instead of Unit DSL) may:
1. Transfer the JSON generalization advantage into supervised learning.
2. Reduce markdown/prose interference in model outputs.
3. Provide clearer structural signal for target classification.

### Controlled Variables

| Variable | Value |
|----------|-------|
| Base model | Qwen3-4B-Instruct-2507 (unchanged) |
| Train subset sizes | 125, 250, 500 (same case IDs as v0.5) |
| Dev set | Same 100 cases (unchanged) |
| Locked gold | Same 100 cases (unchanged, immutable) |
| Eval runner | Same src/v04/eval_runner.py |
| QLoRA defaults | r=8, alpha=16, 3 epochs, LR=2e-4, 4-bit nf4 |
| Seed | 42 |

### Changed Variable

| Variable | v0.5 (DSL) | v0.5b (JSON) |
|----------|------------|--------------|
| Assistant output format | DSL lines (READ/STORE/SKIP) | JSON object (read/store/skip) |
| System prompt | DSL-specific | JSON-specific |
| SFT messages | DSL assistant content | JSON assistant content |
| Eval interface | unit_dsl | unit_json |
| Output dirs | results/v05_lora/... | results/v05b_lora/... |

---

## Success Criteria (Tentative, Pre-Training)

These are aspirational; evaluation on dev only during development:

| Metric | v0.5 DSL LoRA 500 (dev) | JSON LoRA aspirational |
|--------|:-----------------------:|:----------------------:|
| Exact match | 24% | ≥ 24% |
| STORE F1 | 0.962 | ≥ 0.962 |
| Target accuracy | 54.1% | ≥ 60% |
| SKIP F1 | 0.773 | ≥ 0.800 |
| Parse success | 100% | ≥ 98% |
| Sensitive store | 6 (on gold) | ≤ 3 (on dev) |

Hard No-Go: sensitive store on gold must be ≤ v0.5 DSL LoRA 500 (6).

---

## Experiment Stages

1. **Context 5.7-A (this):** Planning, JSON SFT rendering, configs, readiness audit.
2. **Context 5.7-B:** Qwen3-4B Unit JSON LoRA 125-case smoke training + dev eval.
3. **Context 5.7-C:** 250-case training + dev eval + learning curve check.
4. **Context 5.7-D:** 500-case training + dev eval + target audit.
5. **Context 5.7-E:** Locked gold final evaluation (if 500 dev meets success bar).

---

## Risks

1. **JSON longer than DSL:** ~120 chars vs ~60 DSL — may reduce effective training context.
2. **JSON parse errors:** Model may generate invalid JSON (missing braces, trailing commas). Mitigated by SFT training on strict format.
3. **Same bottleneck:** Target classification may not improve — JSON provides structure but not content differentiation between service_memory and task_state.
4. **Safety regression:** JSON format may not help with sensitive content detection — same 500-case pool with limited sensitive examples.

---

*End of V0.5b Unit JSON LoRA Plan.*
