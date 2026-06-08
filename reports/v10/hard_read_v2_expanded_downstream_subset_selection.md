# Hard READ v2 Expanded Downstream Subset Selection

Context: 7.5-B expanded v2 downstream prompt-scaffold subset selection.

## Why Use a Subset

The expanded fixture has 32 cases and 192 strategy rows. This context builds prompt scaffolding only, so an 8-case subset keeps manual prompt inspection tractable before any later API response run. The subset is selected to preserve domain diversity and expose the main selection behaviors observed in 7.5-A without running all 32 cases downstream.

## Selected Cases

- `hard_read_v2_009` — coding/service implementation; keyword_top_k required recall 1.00, avoid 1, stale 0, contradictory 0, wrong-scope 0; budgeted required recall 0.00; sensitive injected by all_candidates 0.
- `hard_read_v2_026` — repo validation / CI; keyword_top_k required recall 0.50, avoid 2, stale 0, contradictory 1, wrong-scope 1; budgeted required recall 0.00; sensitive injected by all_candidates 0.
- `hard_read_v2_011` — data/privacy/compliance; keyword_top_k required recall 0.00, avoid 3, stale 0, contradictory 1, wrong-scope 0; budgeted required recall 0.00; sensitive injected by all_candidates 1.
- `hard_read_v2_020` — product/business process; keyword_top_k required recall 0.50, avoid 2, stale 1, contradictory 0, wrong-scope 1; budgeted required recall 0.00; sensitive injected by all_candidates 1.
- `hard_read_v2_013` — customer-support/CRM workflow; keyword_top_k required recall 0.50, avoid 2, stale 1, contradictory 1, wrong-scope 0; budgeted required recall 0.00; sensitive injected by all_candidates 1.
- `hard_read_v2_014` — security/auth; keyword_top_k required recall 0.00, avoid 4, stale 1, contradictory 1, wrong-scope 0; budgeted required recall 0.00; sensitive injected by all_candidates 1.
- `hard_read_v2_031` — observability/SRE; keyword_top_k required recall 0.00, avoid 3, stale 1, contradictory 1, wrong-scope 0; budgeted required recall 0.00; sensitive injected by all_candidates 0.
- `hard_read_v2_032` — documentation/process-agent; keyword_top_k required recall 0.00, avoid 3, stale 1, contradictory 0, wrong-scope 1; budgeted required recall 0.00; sensitive injected by all_candidates 0.

## Domain Coverage

- coding/service implementation: `hard_read_v2_009` (Patch inventory reservation expiry handling)
- repo validation / CI: `hard_read_v2_026` (Revise flaky-test quarantine rule)
- data/privacy/compliance: `hard_read_v2_011` (Revise consent export suppression)
- product/business process: `hard_read_v2_020` (Update seller verification checklist)
- customer-support/CRM workflow: `hard_read_v2_013` (Adjust priority routing for enterprise refund cases)
- security/auth: `hard_read_v2_014` (Update MFA recovery-code rotation)
- observability/SRE: `hard_read_v2_031` (Update CDN cache purge alert)
- documentation/process-agent: `hard_read_v2_032` (Revise incident runbook owner checklist)

## Selection-Behavior Rationale

- At least two keyword_top_k missing-required cases are included: `hard_read_v2_011`, `hard_read_v2_014`, `hard_read_v2_031`, and `hard_read_v2_032` all have keyword required recall 0.00.
- At least two keyword_top_k contamination cases are included: several selected rows include stale, contradictory, wrong-scope, or avoid memories under keyword_top_k.
- Every selected case has `budgeted_candidate_order` required recall 0.00, preserving the repaired candidate-order diagnostic.
- Sensitive-boundary risk is represented by `hard_read_v2_011`, `hard_read_v2_013`, `hard_read_v2_014`, and `hard_read_v2_020`.
- `hard_read_v2_009` is included as a reasonable keyword_top_k case with full required recall, so the subset is not failure-only.

## Excluded Scope

- The subset excludes original pilot cases `hard_read_v2_001` through `hard_read_v2_008` because the new expanded cases cover all required domains and phenomena.
- This context does not run all 32 cases downstream.
- This context does not run response collection, API calls, model inference, Qwen/LoRA loading, training, live LoRA, or UI work.

## Claim Boundaries

This subset supports prompt-scaffold inspection only. It does not measure downstream answer quality, prove downstream utility, evaluate learned router/live LoRA behavior, establish production memory-system behavior, or show that any routing approach outperforms alternatives.

## Next Recommendation

Build and inspect the 48-row prompt pack for this subset. If prompt inspection passes, a later context can decide whether to run a small API micro-pilot with explicit approval.
