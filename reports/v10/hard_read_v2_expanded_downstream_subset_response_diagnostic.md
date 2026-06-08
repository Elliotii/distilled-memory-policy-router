# Hard READ v2 Expanded Downstream Subset Response Diagnostic

Context: 7.5-C expanded v2 downstream subset API micro-pilot execution.

## Run Boundary

This diagnostic covers response collection and automatic citation-level scoring for the 48-row expanded downstream subset. It does not include manual/rubric review, does not evaluate learned router/live LoRA behavior, and does not establish downstream answer quality.

The API payload contained only the short final-answer-only system instruction and each prompt row's `prompt_text`. Local labels, strategy names, expected answer requirements, candidate labels, oracle/gold fields, and scoring metadata were not sent to the API.

## API Run Summary

| Field | Value |
| --- | ---: |
| Model/API family | `deepseek-v4-flash` |
| Prompt count | 48 |
| Response row count | 48 |
| API OK count | 48 |
| Error count | 0 |
| Usable response count | 48 |
| Empty OK response count | 0 |
| Retry count summary | 46 rows at retry_count 0; 1 row at retry_count 1; 1 row at retry_count 2 |
| Max tokens | 600 |
| Temperature | 0 |
| Retry-empty setting | 2 |
| Payload metadata sent | [False] |
| API keys logged | false |

No failed prompts were dropped. No empty OK responses remain.

## Citation Hygiene Summary

| Check | Result |
| --- | ---: |
| Hallucinated memory citations | 0.00 average across strategies |
| Current-unit citations like `[u1]` | 0.00 average across strategies |
| Bare memory references | 0.00 average across strategies |
| No-response rows | 0 |

The citation format is clean enough for later manual review. These automatic checks do not judge whether the response used the right facts or avoided harmful content.

## Strategy-Level Highlights

| Strategy | Coverage | E2E required recall | Conditional required recall | Avoid avg | Stale avg | Contradictory avg | Wrong-scope avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `all_candidates` | 1.00 | 0.81 | 0.81 | 1.12 | 0.38 | 0.25 | 0.00 |
| `budgeted_candidate_order` | 1.00 | 0.00 | 0.00 | 2.62 | 0.00 | 0.00 | 0.75 |
| `keyword_top_k` | 1.00 | 0.31 | 0.50 | 2.38 | 0.50 | 0.62 | 0.38 |
| `random_k` | 1.00 | 0.31 | 0.56 | 2.38 | 0.50 | 0.25 | 0.25 |
| `oracle_selected` | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Subset-Level Interpretation

- `oracle_selected` remains the clean upper-bound reference in citation diagnostics: full required citation recall and no avoid/stale/contradictory/wrong-scope citations.
- `all_candidates` recovers many required citations but still cites avoid, stale, and contradictory memories, preserving the contamination-risk pattern.
- `budgeted_candidate_order` remains weak after the order-bias repair: required citation recall is 0.00 and avoid/wrong-scope citations are present.
- `keyword_top_k` and `random_k` expose hard-negative or missing-required behavior through low required recall and avoid/stale/contradictory/wrong-scope citations.
- `no_memory` is clean by construction in citation diagnostics, but automatic citation metrics cannot determine whether it misses memory-only details.

## Limitations

- Automatic citation diagnostics only.
- No manual/rubric review has been performed yet.
- No downstream utility proof is supported.
- No learned router/live LoRA behavior is evaluated.
- No production memory-system claim is supported.
- This is a 48-prompt subset micro-pilot, not all 32 expanded cases downstream.

## Next Recommendation

Recommended next context: internal rubric review of the 48 expanded-subset responses.
