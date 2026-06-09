# Expanded Downstream Subset Automatic Comparison With Learned Router

This report combines the existing six-strategy automatic citation scores with the new 8-prompt `learned_router` response run. It is automatic scoring only; rubric review is required next.

## Scope

- Existing 48 prompts were not rerun.
- Only 8 new learned_router prompts were sent to the configured DeepSeek-compatible API.
- The learned_router prompts used real v0.5g offline predictions replayed through the Mac harness.
- This report does not claim downstream utility proof.

## Strategy Table

| strategy | response coverage | e2e required citation recall | conditional required citation recall | avg avoid citations | avg stale citations | avg contradictory citations | avg wrong-scope citations | no response | selection post required recall | selection avoid injected | selection contradictory injected |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.000 | 0 | 0 |
| `all_candidates` | 1.000 | 0.812 | 0.812 | 1.125 | 0.375 | 0.250 | 0.000 | 0 | 1.000 | 224 | 32 |
| `budgeted_candidate_order` | 1.000 | 0.000 | 0.000 | 2.625 | 0.000 | 0.000 | 0.750 | 0 | 0.062 | 96 | 2 |
| `keyword_top_k` | 1.000 | 0.312 | 0.500 | 2.375 | 0.500 | 0.625 | 0.375 | 0 | 0.453 | 73 | 14 |
| `random_k` | 1.000 | 0.312 | 0.562 | 2.375 | 0.500 | 0.250 | 0.250 | 0 | 0.438 | 90 | 10 |
| `oracle_selected` | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 1.000 | 0 | 0 |
| `learned_router` | 0.875 | 0.500 | 0.750 | 0.875 | 0.125 | 0.500 | 0.000 | 1 | 0.891 | 25 | 19 |

## Learned-Router Automatic Citation Metrics

- Prompt count: 8
- Response coverage: 0.875
- E2E required citation recall: 0.500
- Conditional required citation recall: 0.750
- Average avoid citations: 0.875
- Average stale citations: 0.125
- Average contradictory citations: 0.500
- No-response count: 1

## Selection-vs-Downstream Automatic Comparison

Selection replay for learned_router had high mean post required recall (0.890625) with compact context (3.1875 memories on average). The automatic downstream citation score is directionally better than keyword/random/order for required citations, but it is below oracle and all_candidates on this 8-case subset.

## Contradictory Contamination Caution

Selection-level learned_router injected 19 contradictory memories across the 32-case fixture. In this 8-case API extension, automatic citation scoring found contradictory citations in 4 learned_router rows. This is the key issue for rubric review because automatic citation metrics cannot tell whether the final answer followed the contradictory fact or merely cited it while correcting it.

## Why Rubric Review Is Required Next

Automatic scoring can count citations and obvious citation hygiene failures, but it cannot judge whether the answer actually satisfies the task, rejects stale or contradictory guidance, or balances conflicting memories correctly. Context 7.6-F should perform manual/rubric review before any packaging claim.

## Claim Boundary

- Automatic citation metrics only.
- No rubric review yet.
- No downstream utility proof yet.
- READ is not solved.
- No production claim.
