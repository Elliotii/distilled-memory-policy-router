# V0.5e gold_v2 Readiness Decision

**Date:** 2026-06-04  

---

## Decision: Option A — Ready to Generate gold_v2 Cases

### Protocol Summary

| Aspect | Detail |
|--------|--------|
| Active cases | 150 |
| Optional holdout | 30 |
| New domains | 6+ (no overlap with old gold) |
| Evaluated systems | r=16, r=8, few-shot, Qwen3-4B r=8 |
| Primary metric | Paired exact difference with bootstrap 95% CI |
| Success criterion | CI lower bound > 0 for "r=16 better" |
| Safety gate | r=16 sensitive failures ≤ r=8 |
| Statistical method | Paired bootstrap, 10K iterations |
| Leakage checks | L0-L5 against all existing data |
| Label review | Targeted: sensitive + boundary + flagged |

### Why Ready

1. ✅ **Protocol complete** — size, distribution, metrics, CIs, claims all pre-registered
2. ✅ **Opus review addressed** — blinding, n-size, CIs, re-evaluation
3. ✅ **Leakage policy defined** — 5-level check against all source corpora
4. ✅ **Distribution blueprinted** — shapes, targets, stress axes quantified
5. ✅ **Claims bounded** — allowed and forbidden claims pre-registered
6. ✅ **Old gold protected** — not used, not modified
7. ✅ **No data generated yet** — true pre-registration

### What Remains

1. Generate 150 (+30) gold_v2 cases (next context)
2. Run leakage checks against all existing data
3. Targeted label review for sensitive + boundary cases
4. Lock gold_v2 before any model evaluation
5. Evaluate all 4 systems on locked gold_v2
6. Compute paired bootstrap CIs
7. Report final r=16 vs r=8 decision

### Gate Checklist

| Gate | Status |
|------|:------:|
| Protocol documented | ✅ 8 reports |
| Pre-registration complete | ✅ Systems, metrics, criteria locked |
| Distribution blueprint | ✅ Shapes, targets, stress axes |
| Leakage policy | ✅ 5-level check defined |
| CI plan | ✅ Paired bootstrap, 95% CI |
| Claims bounded | ✅ Allowed/forbidden |
| Opus review addressed | ✅ |
| No data generated | ✅ True pre-registration |

---

*End of Readiness Decision.*
