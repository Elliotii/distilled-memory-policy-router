# Hard READ v2 Expanded Downstream Internal Rubric Review

## Review Method

This is an internal rubric review of 48 expanded v2 hard READ downstream DeepSeek V4 Flash responses. It is diagnostic only and should not be described as a human benchmark unless independently audited by the user.

Each response was scored on six 0/1/2 fields: required fact coverage, irrelevant-memory contamination, stale or contradictory use, hallucinated memory use, task response quality, and citation compliance. `manual_utility` is the sum of those fields with a maximum of 12.

## Strategy Aggregate

| Strategy | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Quality | Citation | Auto req recall | Auto avoid avg | Auto stale avg | Auto contradictory avg | Strong | Missing req | Irrelevant flags | Stale/contrad flags |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 8 | 8.00 | 0.00 | 2.00 | 2.00 | 0.00 | 2.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 8 | 0 | 0 |
| `all_candidates` | 8 | 8.75 | 1.62 | 1.38 | 1.25 | 0.88 | 1.62 | 0.81 | 1.12 | 0.38 | 0.25 | 3 | 3 | 3 | 4 |
| `budgeted_candidate_order` | 8 | 6.50 | 0.62 | 0.38 | 1.25 | 0.38 | 2.00 | 0.00 | 2.62 | 0.00 | 0.00 | 0 | 8 | 8 | 4 |
| `keyword_top_k` | 8 | 6.50 | 0.62 | 0.62 | 0.62 | 0.62 | 2.00 | 0.31 | 2.38 | 0.50 | 0.62 | 1 | 7 | 7 | 7 |
| `random_k` | 8 | 6.88 | 0.88 | 0.88 | 0.75 | 0.62 | 1.75 | 0.31 | 2.38 | 0.50 | 0.25 | 0 | 7 | 6 | 6 |
| `oracle_selected` | 8 | 12.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 1.00 | 0.00 | 0.00 | 0.00 | 8 | 0 | 0 | 0 |

## Case Aggregate

| Case | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Quality | Strong | Missing req |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hard_read_v2_009` | 6 | 8.83 | 1.00 | 1.33 | 1.50 | 1.00 | 3 | 3 |
| `hard_read_v2_011` | 6 | 8.17 | 1.00 | 1.17 | 1.17 | 1.00 | 2 | 3 |
| `hard_read_v2_013` | 6 | 7.83 | 1.00 | 1.17 | 1.33 | 0.67 | 1 | 5 |
| `hard_read_v2_014` | 6 | 7.67 | 0.83 | 1.00 | 1.50 | 0.50 | 1 | 4 |
| `hard_read_v2_020` | 6 | 8.67 | 1.00 | 1.50 | 1.67 | 0.83 | 1 | 5 |
| `hard_read_v2_026` | 6 | 7.17 | 0.83 | 1.00 | 0.83 | 0.50 | 1 | 5 |
| `hard_read_v2_031` | 6 | 6.83 | 0.83 | 1.00 | 0.67 | 0.33 | 1 | 4 |
| `hard_read_v2_032` | 6 | 9.67 | 1.17 | 1.50 | 1.83 | 1.17 | 2 | 4 |

## Selection-vs-Response Comparison

| Strategy | Selection req recall | Selection avoid injected | Selection stale injected | Selection contradictory injected | Response req citation recall | Response avoid citation avg | Manual utility |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 0.00 | 0 | 0 | 0 | 0.00 | 0.00 | 8.00 |
| `all_candidates` | 1.00 | 224 | 32 | 32 | 0.81 | 1.12 | 8.75 |
| `budgeted_candidate_order` | 0.06 | 96 | 2 | 2 | 0.00 | 2.62 | 6.50 |
| `keyword_top_k` | 0.45 | 73 | 14 | 14 | 0.31 | 2.38 | 6.50 |
| `random_k` | 0.44 | 90 | 14 | 10 | 0.31 | 2.38 | 6.88 |
| `oracle_selected` | 1.00 | 0 | 0 | 0 | 1.00 | 0.00 | 12.00 |

- The expanded fixture keeps the candidate-order artifact reduced at selection time: `budgeted_candidate_order` has low required recall while still injecting hard negatives.
- The response review shows `no_memory` avoids contamination but repeatedly misses memory-only thresholds, validation commands, and blocking constraints.
- `oracle_selected` is the clean upper-bound reference for this diagnostic: it has complete required-fact coverage and no hard-negative use in the reviewed subset.
- `all_candidates` often recovers required facts, but it sometimes blends them with stale, contradictory, or unrelated instructions.
- `keyword_top_k` and `random_k` expose hard-negative behavior; individual rows remain useful only when the selected set happens to include enough required evidence.

## Automatic Citation Metrics Summary

- Prompt count: 48.
- Response count: 48.
- No-response count: 0.
- Citation formatting remained clean: hallucinated memory citations, current-unit citations, and bare memory references all averaged 0.00 across strategies.
- Automatic metrics are citation diagnostics only; they do not judge whether the answer used the cited facts correctly.

## Notable Examples

### Strong oracle_selected response

- Prompt: `hard_read_v2_009__oracle_selected`
- Utility: 12
- Notes: Complete answer with required expiry threshold, validation test, and useful logging fields.

```text
- Patch inventory-api to expire unpaid reservations after 18 minutes of inactivity in the current reservation flow [m281].   - Before handoff, run `pytest tests/integration/inventory_reservation_expiry.py` in the stockflow repo [m282].   - Ensure expiry logs include `reservation_id` and `expiry_reason` fields to support triage [m283].
```

### Generic or under-specified no_memory response

- Prompt: `hard_read_v2_009__no_memory`
- Utility: 8
- Notes: Generic current-task response; misses the 18-minute rule, validation test path, and explicit rejection of 45-minute/manual cleanup.

```text
- Patch inventory-api's reservation expiry handling within the stockflow repo.   - Before handoff, validate the repo to ensure changes are correctly applied.   - Scoped to the current reservation flow: update expiry logic for reservations.
```

### all_candidates contamination example

- Prompt: `hard_read_v2_026__all_candidates`
- Utility: 5
- Notes: Includes the Swift test and fields, but wrongly changes the policy to first-failure quarantine and mixes in contradictory outage/one-failure memories.

```text
- Revise iOS CI to quarantine a test after its first main-branch failure, requiring a linked owner ticket, building on prior policy shifts [m451][m456]. Exclude simulator outage failures from counting as flakiness [m454][m460]. - Before handoff, run `swift test --filter FlakyQuarantinePolicyTests` to validate the new rule [m452]. - Ensure quarantine records include `owner_ticket` and `failure_window_hours` to support traceability [m453].
```

### keyword_top_k failure example

- Prompt: `hard_read_v2_011__keyword_top_k`
- Utility: 4
- Notes: Directly applies the stale behavior to export opt-in rows despite consent_revoked_at and narrows suppression to SMS only.

```text
- Revise consent-worker export suppression to include validation checks before handoff, ensuring compliance with current rules.   - Suppression audit entries must now include `subject_id` and `suppression_reason` [m303].   - Export all `opt_in=true` rows and ignore `consent_revoked_at` until the monthly cleanup job [m306]; apply suppression only to SMS rows per the marketing export patch [m308].   - Note that newsletter preference sync does not control regulated export suppression [m304].
```

### random_k failure example

- Prompt: `hard_read_v2_009__random_k`
- Utility: 4
- Notes: Uses unrelated billing and warehouse memories and explicitly rejects the 18-minute behavior needed for inventory reservations.

```text
- Patch inventory-api reservation expiry handling, scoped to the existing reservation flow; note that warehouse count refresh (tuned by batch size) does not control expiry [m284].   - Unlike billing-api's 18-minute hold expiry [m287], inventory-api's current design is not based on a fixed window; the archived 45-minute cleanup branch is obsolete [m288].   - Stock recount alerts use `reservation_id` only for dashboards and do not drive expiry decisions [m289].   - Validate the repo (`stockflow`) before handoff; ensure the patch aligns with the current flow, not legacy patterns.
```

### budgeted_candidate_order failure example

- Prompt: `hard_read_v2_009__budgeted_candidate_order`
- Utility: 5
- Notes: Misses the 18-minute rule and correct test path; imports billing/warehouse context and only partially resists the archived 45-minute guidance.

```text
- Patch `inventory-api` reservation expiry handling by moving away from the fixed 45-minute cleanup window of the archived branch [m288]. Instead, adopt `billing-api`'s pattern: expire after a configurable timeout and validate with dedicated tests (e.g., `pytest tests/billing_holds.py`) [m287].   - Log expiry events with `reservation_id` and `expiry_reason` fields to support triage [m283]. Note that warehouse count refresh is tuned by batch size only and does not control reservation expiry behavior [m284].   - Before handoff, validate the repo is `stockflow` and that changes remain scoped solely to the reservation expiry flow.
```

## Limitations

- This is an internal rubric review, not a formal human benchmark.
- The review covers a 48-response subset drawn from eight expanded v2 hard READ cases.
- The review does not prove downstream utility.
- The review does not evaluate learned router/live LoRA behavior.
- The review does not establish production memory-system behavior.
- The review does not support a claim that any routing approach is better than alternatives.
