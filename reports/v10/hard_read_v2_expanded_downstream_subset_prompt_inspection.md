# Hard READ v2 Expanded Downstream Subset Prompt Inspection

Context: 7.5-B prompt-pack inspection before any API execution.

## Row Counts

| Artifact | Rows |
| --- | ---: |
| Prompt pack | 48 |
| Response template | 48 |
| Manual review template | 48 |

Case coverage: `hard_read_v2_009`, `hard_read_v2_011`, `hard_read_v2_013`, `hard_read_v2_014`, `hard_read_v2_020`, `hard_read_v2_026`, `hard_read_v2_031`, `hard_read_v2_032`.
Strategy coverage: `all_candidates`, `budgeted_candidate_order`, `keyword_top_k`, `no_memory`, `oracle_selected`, `random_k`.
Redacted prompts: 0.

## no_memory Prompt Inspection

`no_memory` has 8 rows and no injected memory IDs. Each prompt states `No prior memory context is available.` The current task notes are under-specified and omit exact commands, thresholds, keys, deadlines, or implementation constraints, so no-memory responses should miss memory-only details.

## all_candidates Prompt Inspection

`all_candidates` has 8 rows with 10 injected memories per selected case. These prompts expose required memories along with avoid, stale, contradictory, wrong-scope, near-duplicate, same-entity irrelevant, and sensitive-boundary memories where present, so they preserve the intended contamination-risk diagnostic.

## budgeted_candidate_order Prompt Inspection

`budgeted_candidate_order` has 8 rows with 4 injected memories per case. All selected cases have zero required recall for this strategy, preserving the repaired candidate-order failure mode.

## keyword_top_k Prompt Inspection

`keyword_top_k` has 8 rows with 4 injected memories per case. Missing-required cases: `hard_read_v2_011`, `hard_read_v2_014`, `hard_read_v2_031`, `hard_read_v2_032`. Risky lexical hard-negative cases: `hard_read_v2_009`, `hard_read_v2_026`, `hard_read_v2_011`, `hard_read_v2_020`, `hard_read_v2_013`, `hard_read_v2_014`, `hard_read_v2_031`, `hard_read_v2_032`. Reasonable keyword case: `hard_read_v2_009`.

## random_k Prompt Inspection

`random_k` has 8 rows with 4 injected memories per case. It provides a fixed-seed baseline for missing-required and contamination comparison against keyword_top_k.

## oracle_selected Prompt Inspection

`oracle_selected` has 8 rows with 3 injected memories per case: required plus helpful memory IDs only. It remains a labeled reference context for prompt inspection, not a deployable strategy.

## Prompt Leakage Checks

- Result: pass.
- No prompt text contains local label field names, oracle/gold wording, benchmark strategy wording, or `[u#]` current-unit citations under the corrected leakage check.
- Every non-no_memory prompt includes bracketed citations for each injected memory ID.
- Every no_memory prompt has no injected memory IDs and includes the required no-memory sentence.

## Under-Specification Check

The prompt-facing task notes identify the task and validation need but omit exact validation commands, thresholds, keys, deadlines, logging fields, and implementation constraints. This is sufficient for later testing whether no_memory responses miss memory-only details.

## Contamination and Hard-Negative Diagnostics

- all_candidates contamination risk is present across all 8 cases; sensitive-boundary cases include `hard_read_v2_011`, `hard_read_v2_020`, `hard_read_v2_013`, `hard_read_v2_014`.
- keyword_top_k and random_k contain useful hard-negative diagnostics because the selected subset includes lexical misses, stale/contradictory/wrong-scope selected memories, and a reasonable keyword case for contrast.

## Prompts Needing Manual Repair Before API

None identified by scaffold inspection. Sensitive-boundary prompts should still receive human review before any API context because they intentionally include redacted or should-not-use distractor memories.

## Final Recommendation

Pass for prompt scaffold inspection. Do not run an API in this context. A later context can run a small response micro-pilot only after explicit approval.
