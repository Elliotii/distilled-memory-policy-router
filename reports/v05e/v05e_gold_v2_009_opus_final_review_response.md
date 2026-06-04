# gold_v2_009 Opus Final Review Response

**Date:** 2026-06-04  

## Opus Verdict: CORRECTION REQUIRED, but data regeneration NOT warranted

Opus confirmed v009 fixed all prior blockers. Required corrections are pre-evaluation documentation/harness items only.

## Accepted Corrections

1. ✅ **Harness compatibility**: Patched `render_user_input` to support `m['text']` fallback; patched validator to accept `text` as memory content fallback and empty `dsl` when structured fields present
2. ✅ **Reporting addendum**: Store/skip-exact, McNemar table, READ-component failure rate added
3. ✅ **Claim boundaries**: No boundary-sliced claims, READ F1 not semantic, template-generated limitations documented
4. ✅ **Sensitive reporting**: Both raw (21 units) and deduplicated (13 strings) counts

## v009 Data Unchanged
v009 SHA-256: `f5cf7be1d06f085e...` (matches lock manifest). No regeneration needed.

## Rationale for Not Creating v010
Remaining issues are documentation/harness, not data quality. v009 is fair for r=16 vs r=8 paired comparison.
