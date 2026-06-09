# Learned-Router Downstream Rubric Review Plan

## Context 7.6-F Goal

Review the 8 learned_router responses and compare them against the existing 48 responses when useful. Prefer producing either a combined 56-row manual/rubric review file or an 8-row learned_router review extension plus a combined report.

## Inputs

- Existing six-strategy prompt pack and responses under `data/v10/hard_read_v2_expanded_downstream_subset/`.
- New learned_router prompt pack and responses from Context 7.6-E.
- Existing automatic citation scores and learned_router automatic scores.

## Strategies To Compare

- `no_memory`
- `all_candidates`
- `budgeted_candidate_order`
- `keyword_top_k`
- `random_k`
- `oracle_selected`
- `learned_router`

## Review Questions

- Does learned_router outperform keyword/random/order in response quality?
- Does learned_router outperform no_memory?
- Does all_candidates still show higher contamination?
- How far is learned_router from oracle?
- Did contradictory injected memories hurt?

## Suggested Rubric Fields

- required fact coverage
- validation command coverage
- bad-memory avoidance
- contradiction handling
- citation accuracy
- concise task usefulness
- overall score
- reviewer notes

## Stop Condition

After 7.6-F rubric review, proceed to packaging regardless of positive or negative result. Negative results should be reported as limitations rather than hidden or tuned away.

## Claim Boundary

Rubric review is the next diagnostic step. Until it is complete, the 7.6-E outputs remain automatic diagnostics only with no downstream utility proof.
