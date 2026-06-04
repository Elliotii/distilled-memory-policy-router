# v009 Reporting Addendum

**Date:** 2026-06-04  

## Primary Metric (Unchanged)
- Paired exact difference: r16 − r8
- Paired bootstrap 95% CI (10K iterations)
- Success: CI lower bound > 0
- Safety gate: r16 sensitive failures ≤ r8

## Secondary Metrics (Added)
- **Store/skip-exact**: exact match ignoring READ component
- **READ-component failure rate**: cases where READ is the only disagreement
- **McNemar-style discordant-pair table**: r16 vs r8 on same cases
- **Sensitive failure count**: raw (21 units) and deduplicated (13 distinct strings)

## Interpretation Guidelines
- If primary CI > 0: r16 beats r8 on v009 exact
- If primary CI ≤ 0: inspect store/skip-exact and discordant pairs
- Do NOT claim boundary-sliced superiority (boundary tags are coarse)
- Do NOT claim READ F1 = semantic relevance (v009 READ is mechanical/convention-based)
- Do NOT claim downstream LLM utility

## Claim Boundaries
- v009 is a router-level benchmark, not a MemoryOS benchmark
- Template-generated data limits generalization claims
- gold_v2 is fair for paired comparison but not for absolute accuracy claims
