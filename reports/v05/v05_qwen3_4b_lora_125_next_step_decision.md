# V0.5 Qwen3-4B LoRA 125 Next-Step Decision

**Date:** 2026-06-02  
**Context:** 5.5-B2 — postmortem decision  

---

## Recommended Next Step

**Option A: Proceed to 250 unchanged** (with eval prompt fix applied).

## Rationale

1. **Eval prompt fix improved metrics:** 12% exact (was 10%), 0.867 STORE F1 (was 0.793). Distribution between training and eval aligned.

2. **Model is undertrained, not overfit:** Train125 eval (13.6%) is only marginally higher than dev (12%). The model hasn't converged — eval loss was still decreasing strongly (2.30→1.52). 250 cases will provide 48 steps (vs 24 for 125), giving the optimizer more opportunity.

3. **Parse failures are format confusion, not model collapse:** 25% parse failures are memory-ID-as-unit-ID errors, not garbled output. More training data should help the model learn the distinction.

4. **Sensitive store unchanged:** 33.3% — same as baseline. Not caused by LoRA.

5. **Adapter, loading, rendering all verified correct:** No code bugs found.

## Changes Made

- `eval_lora_router.py`: Fixed to use SFT training system prompt via `render_sft_messages.SYSTEM_PROMPT` and `render_user_input`. This aligns eval format with training format.
- `qwen_v05_output_runner.py`: Should be similarly updated in next context for LoRA eval consistency.

## Config Recommendations for 250

- Keep epochs: 3 (eval loss still decreasing, don't extend yet)
- Keep LR: 2e-4 (stable, no divergence)
- Eval prompt: Use SFT system prompt

## Cross-Batch Duplicate

Non-blocking for 250. Document and resolve before final 500 training.

---

*End of V0.5 Qwen3-4B LoRA 125 Next-Step Decision.*
