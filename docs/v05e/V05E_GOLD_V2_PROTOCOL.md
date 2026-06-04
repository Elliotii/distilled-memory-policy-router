# V0.5e gold_v2 Protocol

> Pre-registration for r=16 final validation

## Why gold_v2

Old gold evaluated 3 times (v0.5/v0.5b/v0.5c) — not fully blind for r=16. Fresh 150-case gold set for clean r=16 vs r=8 comparison.

## What's Pre-Registered

- **150 active cases** + 30 optional holdout
- **4 systems** evaluated on identical cases: r=16, r=8, few-shot, Qwen3-4B r=8
- **Primary metric:** Paired exact difference with bootstrap 95% CI
- **Success:** CI lower bound > 0 → r=16 better
- **Safety gate:** r=16 sensitive failures ≤ r=8
- **Shape distribution:** READ-only 18%, STORE/SKIP-only 39%, READ+STORE 43%
- **Stress axes:** 18-27 sensitive SKIP, 30-38 hard target-boundary
- **New domains:** 6+ (no old-gold overlap)

## Statistical Rigor

- Paired bootstrap 10K iterations for 95% CI
- Effect size in pp and raw counts
- McNemar-style table if feasible
- No "better" claim without CI support

---

See `reports/v05e/v05e_gold_v2_protocol.md` for full protocol.
