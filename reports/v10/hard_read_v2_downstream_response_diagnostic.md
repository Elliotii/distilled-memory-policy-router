# Hard READ v2 Downstream Response Diagnostic

Context: 7.4-F v2 downstream API micro-pilot execution.

## Run Boundary

This diagnostic covers response collection and automatic citation-level scoring only. It does not include manual/rubric review, does not evaluate learned router/live LoRA behavior, and does not establish downstream answer quality.

The API payload contained only:

- the short final-answer-only system instruction;
- each prompt row's `prompt_text`.

Local labels, strategy names, expected answer requirements, candidate labels, oracle/gold fields, and scoring metadata were not sent to the API.

## API Run Summary

| Field | Value |
| --- | ---: |
| Model | `deepseek-v4-flash` |
| Prompt count | 30 |
| Response row count | 30 |
| API OK count | 30 |
| Error count | 0 |
| Usable response count | 30 |
| Empty OK response count | 0 |
| Retry count summary | 29 rows at retry_count 0; 1 row at retry_count 1 |
| Max tokens | 600 |
| Temperature | 0 |
| Retry-empty setting | 2 |
| Payload metadata sent | false |
| API keys logged | false |

No failed prompts were dropped. No empty OK responses remain.

## Citation Hygiene Summary

| Check | Result |
| --- | ---: |
| Hallucinated memory citations | 0 average across all strategies |
| Current-unit citations like `[u1]` | 0 average across all strategies |
| Bare memory references | 0 average across all strategies |
| No-response rows | 0 |

The citation format is clean enough for later manual review. These automatic checks do not judge whether the answer used the right facts or avoided harmful content.

## Strategy-Level Highlights

| Strategy | Coverage | E2E required recall | Conditional required recall | Avoid avg | Stale avg | Contradictory avg | Wrong-scope avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `all_candidates` | 1.00 | 0.90 | 0.90 | 1.80 | 0.40 | 0.80 | 0.00 |
| `budgeted_candidate_order` | 1.00 | 0.20 | 0.40 | 1.80 | 0.20 | 0.20 | 0.20 |
| `keyword_top_k` | 1.00 | 0.80 | 1.00 | 1.40 | 0.60 | 0.20 | 0.00 |
| `random_k` | 1.00 | 0.40 | 0.80 | 2.20 | 0.40 | 0.00 | 0.20 |
| `oracle_selected` | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Selection-Expectation Comparison

- `oracle_selected` is the clean upper-bound reference in citation diagnostics: full required citation recall and no avoid/stale/contradictory/wrong-scope citations.
- `all_candidates` recovers most required citations but also cites avoid, stale, and contradictory memories, preserving the expected contamination-risk pattern.
- `budgeted_candidate_order` no longer behaves like the v1 pseudo-oracle: required citation recall is low and avoid citations remain present.
- `keyword_top_k` and `random_k` expose hard-negative or missing-required patterns through avoid/stale citations and lower end-to-end required recall than oracle.
- `no_memory` has clean citation hygiene by construction, but automatic citation metrics cannot determine whether the answers missed memory-only implementation details.

## Limitations

- Automatic citation diagnostics only.
- No manual/rubric review has been performed yet.
- No downstream utility proof is supported.
- No learned router/live LoRA behavior is evaluated.
- No production memory-system claim is supported.
- The sample is a 30-prompt micro-pilot, not the full hard READ evaluation.

## Next Recommendation

Recommended next context: Context 7.4-G — manual/rubric review of the 30 v2 downstream responses.
