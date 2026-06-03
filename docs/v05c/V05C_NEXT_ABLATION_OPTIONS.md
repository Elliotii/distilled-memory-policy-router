# V0.5c Next Ablation Options

> Advisory only — do not start without explicit authorization.

## Option 1: Standard LoRA / BF16 LoRA

Close the 1pp exact gap to few-shot by removing 4-bit quantization.

- **Expected:** +2-5pp exact
- **Risk:** 12GB VRAM may not fit BF16 4B model
- **Feasibility:** Needs gradient checkpointing verification

## Option 2: r=16 QLoRA

Double LoRA capacity while staying within VRAM budget.

- **Expected:** +1-3pp exact
- **Risk:** Minimal (still QLoRA)
- **Feasibility:** Safe

## Option 3: Safety-Focused Training

Eliminate the 5 PII storage failures.

- **Approach:** Oversample sensitive cases, add SKIP loss penalty
- **Expected:** 5 → 0-2 failures
- **Risk:** May reduce STORE F1

## Option 4: Target-Balanced Training

Improve weak targets (repo_memory, project_memory).

- **Approach:** Oversample underrepresented targets
- **Expected:** +3-5pp target accuracy

## Option 5: gold_v2

New gold set for clean evaluation of future tuned variants.

- **Why:** Current gold evaluated 3 times — not fully blind
- **Timing:** Before any hyperparameter tuning

## Recommended Order

1. gold_v2
2. r=16 QLoRA (safest capacity increase)
3. Safety-focused training
4. Standard LoRA (VRAM permitting)

---

*See `reports/v05c/v05c_next_ablation_decision_memo.md` for full analysis.*
