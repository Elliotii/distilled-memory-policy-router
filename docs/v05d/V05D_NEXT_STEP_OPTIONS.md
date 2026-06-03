# V0.5d Next-Step Options

> After r=16 dev-only ablation

## Option 1: gold_v2 ✅ Recommended

Create new gold set. Evaluate r=16 vs r=8 vs few-shot head-to-head.

- **Why:** r=16 +5pp exact on dev is the strongest signal in this study
- **Benefit:** Clean final claim for r=16
- **Effort:** Medium

## Option 2: Stop and Package

Close the project with r=8 as best gold-verified, r=16 as promising dev-only.

- **Why:** Current results are already strong
- **Benefit:** Clean closure
- **Effort:** Low

## Option 3: Standard/BF16 LoRA

Remove 4-bit quantization for full-precision LoRA.

- **Why:** Could close remaining exact gap
- **Risk:** VRAM may not fit
- **Effort:** Medium-High

## Option 4: Targeted Data Scaling

Add safety-focused or target-balanced training data.

- **Why:** Fix remaining accuracy/safety bottlenecks
- **Effort:** High

---

See `reports/v05d/v05d_next_step_decision_memo.md` for full analysis.
