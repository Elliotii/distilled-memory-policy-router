# Hard READ v2 Downstream Internal Rubric Review

## Review Method

This is an internal rubric review of the 30 v2 hard READ downstream DeepSeek V4 Flash responses. It is diagnostic only and should not be described as a human benchmark unless independently audited by the user.

Each response was scored on six 0/1/2 fields: required fact coverage, irrelevant-memory contamination, stale or contradictory use, hallucinated memory use, task response quality, and citation compliance. `manual_utility` is the sum of those fields with a maximum of 12.

## Strategy Aggregate

| Strategy | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Quality | Citation | Auto req recall | Auto avoid avg | Auto stale avg | Auto contradictory avg | Strong | Missing req | Irrelevant flags | Stale/contrad flags |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 5 | 8.80 | 0.20 | 2.00 | 2.00 | 1.00 | 2.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 5 | 0 | 0 |
| `all_candidates` | 5 | 7.60 | 2.00 | 0.80 | 0.40 | 0.40 | 2.00 | 0.90 | 1.80 | 0.40 | 0.80 | 1 | 0 | 4 | 4 |
| `budgeted_candidate_order` | 5 | 7.00 | 1.00 | 0.80 | 1.40 | 0.80 | 1.80 | 0.20 | 1.80 | 0.20 | 0.20 | 0 | 5 | 4 | 2 |
| `keyword_top_k` | 5 | 8.80 | 1.60 | 1.20 | 1.20 | 0.80 | 2.00 | 0.80 | 1.40 | 0.60 | 0.20 | 1 | 2 | 3 | 2 |
| `random_k` | 5 | 8.80 | 1.00 | 1.00 | 2.00 | 1.00 | 2.00 | 0.40 | 2.20 | 0.40 | 0.00 | 0 | 5 | 4 | 0 |
| `oracle_selected` | 5 | 12.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 1.00 | 0.00 | 0.00 | 0.00 | 5 | 0 | 0 | 0 |

## Case Aggregate

| Case | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Quality | Strong | Missing req |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hard_read_v2_001` | 6 | 8.83 | 1.17 | 1.00 | 1.67 | 1.00 | 1 | 4 |
| `hard_read_v2_002` | 6 | 9.33 | 1.17 | 1.50 | 2.00 | 1.33 | 2 | 4 |
| `hard_read_v2_003` | 6 | 8.83 | 1.33 | 1.50 | 1.33 | 0.83 | 1 | 3 |
| `hard_read_v2_005` | 6 | 8.00 | 1.33 | 0.83 | 1.17 | 0.83 | 1 | 3 |
| `hard_read_v2_008` | 6 | 9.17 | 1.50 | 1.67 | 1.33 | 1.00 | 2 | 3 |

## Selection-vs-Response Comparison

| Strategy | Selection req recall | Selection avoid injected | Selection stale injected | Selection contradictory injected | Response req citation recall | Response avoid citation avg | Manual utility |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 0.00 | 0 | 0 | 0 | 0.00 | 0.00 | 8.80 |
| `all_candidates` | 1.00 | 56 | 8 | 8 | 0.90 | 1.80 | 7.60 |
| `budgeted_candidate_order` | 0.25 | 24 | 2 | 2 | 0.20 | 1.80 | 7.00 |
| `keyword_top_k` | 0.75 | 15 | 3 | 1 | 0.80 | 1.40 | 8.80 |
| `random_k` | 0.44 | 23 | 2 | 2 | 0.40 | 2.20 | 8.80 |
| `oracle_selected` | 1.00 | 0 | 0 | 0 | 1.00 | 0.00 | 12.00 |

- v2 reduced the candidate-order artifact at the selection level: `budgeted_candidate_order` has much lower required recall than `oracle_selected` and still injects avoid memories.
- The response review shows `no_memory` is less sufficient than in the v1 pilot: it avoids contamination but repeatedly misses memory-only commands, thresholds, and implementation constraints.
- `oracle_selected` behaves as the clean upper-bound reference in both automatic citation diagnostics and internal rubric scores.
- `all_candidates` often recovers required facts but can blend them with stale or contradictory instructions.
- `keyword_top_k` and `random_k` expose missing-required and hard-negative behavior, though some individual keyword responses remain useful when the lexical set includes both required memories.

## Automatic Citation Metrics Summary

- Prompt count: 30.
- Response count: 30.
- No-response count: 0.
- Citation formatting remained clean: hallucinated memory citations, current-unit citations, and bare memory references all averaged 0.00 across strategies.
- Automatic metrics are citation diagnostics only; they do not judge whether the answer used the cited facts correctly.

## Notable Examples

### Strong oracle_selected response

- Prompt: `hard_read_v2_001__oracle_selected`
- Utility: 12
- Notes: Cleanly covers exponential backoff with jitter, exact validation command, and retry logging fields.

```text
- Implement exponential backoff with jitter for payment authorization retries in checkout-api [m201]. - Include `retry_attempt` and `authorization_status` fields in all retry logs [m203]. - Prior to handoff, run `make test-checkout-retry` in the shopflow repo to validate the patch [m202].
```

### Generic or under-specified no_memory response

- Prompt: `hard_read_v2_001__no_memory`
- Utility: 9
- Notes: Generic checkout retry guidance; misses memory-only exponential backoff with jitter, exact test command, and logging fields.

```text
- Patch the checkout-api service in the shopflow repo to modify payment retry behavior, ensuring it aligns with the current implementation rules. - Before handing off the patch, execute a repo validation step to confirm the changes are compatible and correctly applied. - Focus solely on updating retry logic; avoid scope creep into other checkout or payment features.
```

### all_candidates contamination example

- Prompt: `hard_read_v2_001__all_candidates`
- Utility: 6
- Notes: Covers required retry/test/logging facts but also adopts the contradictory disable-retries instruction and cites stale or unrelated memories.

```text
- Disable all payment retries for authorization calls per [m206] to prevent duplicate captures; this overrides the legacy fixed two-second delay from the archived branch [m210].   - Implement exponential backoff with jitter for any allowed retry calls [m201], ensuring logs capture `retry_attempt` and `authorization_status` fields [m203].   - Run `make test-checkout-retry` in the shopflow repo before merging [m202]; the April sandbox timeout incident [m205] and canceled regional rollout [m208] should not influence current behavior.
```

### keyword_top_k failure example

- Prompt: `hard_read_v2_005__keyword_top_k`
- Utility: 6
- Notes: Covers exact test and after-commit namespace rule but then repeats stale guidance to skip cache invalidation during indexing.

```text
- Run `npm run test:search-index` in the searchbox repo before merging any catalog-search indexing cache invalidation changes [m242].   - For batch indexing, ensure the `product_index` namespace is cleared only after committed writes, aligning with the current indexing path [m241].   - Cache invalidation should be skipped during the indexing phase itself, as noted in prior Solr migration guidance [m245]; the synonym refresh process does not cover cache invalidation [m244].
```

### budgeted_candidate_order failure example

- Prompt: `hard_read_v2_002__budgeted_candidate_order`
- Utility: 6
- Notes: Covers 30-day deletion but replaces the exact pytest command with an unsupported verify_privacy_export_retention command and uses uncited dashboard context.

```text
- Delete analytics-worker EU privacy export bundles within 30 days of creation, per [m211]. - The retention dashboard stores aggregate deletion counts but does not govern bundle removal; rely on the deletion logic described in the repo. - Validate cleanup by running the repo’s `verify_privacy_export_retention` test suite after deploying any retention changes.
```

## Limitations

- This is an internal rubric review, not a formal human benchmark.
- The review covers a 30-prompt micro-pilot drawn from five v2 hard READ cases.
- The review does not prove downstream utility.
- The review does not evaluate learned router/live LoRA behavior.
- The review does not establish production memory-system behavior.
- The review does not support a claim that any router is better than alternatives.
