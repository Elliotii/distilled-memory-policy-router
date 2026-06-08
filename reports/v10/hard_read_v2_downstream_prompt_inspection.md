# Hard READ v2 Downstream Prompt Inspection

Context: 7.4-E prompt-pack inspection before any API execution.

## Row Counts

| Artifact | Rows |
| --- | ---: |
| Prompt pack | 30 |
| Response template | 30 |
| Manual review template | 30 |

Case coverage: `hard_read_v2_001`, `hard_read_v2_002`, `hard_read_v2_003`, `hard_read_v2_005`, `hard_read_v2_008`.

Strategy coverage: `no_memory`, `all_candidates`, `budgeted_candidate_order`, `keyword_top_k`, `random_k`, `oracle_selected`.

Redaction was applied to 3 prompt rows: `hard_read_v2_008__all_candidates`, `hard_read_v2_008__budgeted_candidate_order`, and `hard_read_v2_008__random_k`.

## no_memory Prompt Inspection

`no_memory` prompts include the current task notes and the explicit sentence `No prior memory context is available.` They do not include any injected memory IDs. The prompt asks for a concise implementation-oriented response and instructs the model not to include bracketed memory citations.

The no-memory prompts appear less answerable than v1 because the current notes request the task and validation step but omit exact commands and memory-only constraints. This is still a prompt inspection judgment only; actual no-memory answerability must be checked in a later downstream response pilot.

## all_candidates Prompt Inspection

`all_candidates` prompts include all 10 post-budget candidate memories for each selected case. This exposes the answerer to required memories, helpful memories, same-entity irrelevant memories, stale notes, contradictory notes, wrong-scope notes, and sensitive-boundary notes where present. These prompts are suitable for testing contamination risk in a later downstream response pilot.

## budgeted_candidate_order Prompt Inspection

`budgeted_candidate_order` prompts use the first four shuffled candidates from the v2 selection eval. They now visibly differ from oracle contexts: for example, `hard_read_v2_001__budgeted_candidate_order` includes no required memory and includes avoid memories. This preserves the intended repair from v1, where candidate order was too favorable.

## keyword_top_k Prompt Inspection

`keyword_top_k` prompts include lexical hard-negative behavior. The selected contexts sometimes include stale or same-entity irrelevant memories while missing at least one required memory. This is useful for inspecting whether lexical overlap can contaminate downstream responses.

## Prompt Leakage Checks

Prompt text was checked for:

- local label field names;
- `candidate_labels`;
- oracle/gold wording;
- benchmark strategy wording;
- current-unit citation IDs such as `[u1]`;
- missing injected memory citations for non-no-memory prompts;
- missing no-memory sentence for no-memory prompts.

No prompt-text leakage was found in the generated pack under the corrected leakage checks.

## Manual Review Before API

Prompts that deserve manual review before any API execution:

- `hard_read_v2_002__all_candidates`, because it includes privacy export, stale, contradictory, and sensitive-boundary context.
- `hard_read_v2_008__all_candidates`, because it includes auth-gateway sensitive-boundary and contradictory distractors.
- `hard_read_v2_001__budgeted_candidate_order`, because it demonstrates the repaired order-bias condition with no required memories.
- `hard_read_v2_003__budgeted_candidate_order`, because it includes a contradiction in the first four candidates.

## Final Recommendation

Pass for manual prompt inspection. Do not run an API until the selected sensitive-boundary and all-candidates prompts are manually inspected. If manual inspection passes, the next context can run a small v2 downstream API micro-pilot under Context 7.4-F.
