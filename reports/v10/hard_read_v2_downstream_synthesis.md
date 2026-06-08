# Hard READ v2 Downstream Micro-Pilot Synthesis

Context: 7.4-G v2 downstream internal rubric review and synthesis.

## Scope

This synthesis combines four diagnostic steps:

- 7.4-D fixture repair and v2 selection-only evaluation.
- 7.4-E v2 downstream prompt scaffold and prompt inspection.
- 7.4-F v2 DeepSeek V4 Flash response collection and automatic citation diagnostics.
- 7.4-G internal rubric review of the 30 collected responses.

This remains a micro-pilot. It does not prove downstream utility, does not evaluate learned router/live LoRA behavior, does not establish production memory-system behavior, and does not show that any learned routing approach outperforms alternatives.

## v2 Fixture Repair from 7.4-D

v2 was created because v1 exposed two fixture risks: high `no_memory` answerability and favorable candidate ordering for `budgeted_candidate_order`. The v2 repair changed the fixture shape:

- Candidate memories are fixed-seed shuffled instead of label ordered.
- Current task notes are under-specified and omit exact commands, thresholds, and implementation constraints that live only in memory.
- Each case has 10 candidate memories with required, helpful, irrelevant, stale, contradictory, wrong-scope, and sensitive-boundary distractors where applicable.
- v1 artifacts were not overwritten.

Selection-only metrics indicate that v2 reduced candidate-order bias: `budgeted_candidate_order` post-budget required recall fell to 0.25, while `oracle_selected` remained at 1.00. `budgeted_candidate_order` also injected 24 avoid memories, 2 stale memories, and 2 contradictory memories across the eight-case selection fixture.

## v2 Prompt Scaffold from 7.4-E

The v2 downstream prompt scaffold selected five cases and six strategies for 30 prompts:

- Cases: `hard_read_v2_001`, `hard_read_v2_002`, `hard_read_v2_003`, `hard_read_v2_005`, `hard_read_v2_008`.
- Strategies: `no_memory`, `all_candidates`, `budgeted_candidate_order`, `keyword_top_k`, `random_k`, `oracle_selected`.
- Labels, strategy names, oracle/gold wording, and current-unit IDs were not exposed in prompt text.
- Sensitive-boundary rows were redacted where needed.

Prompt inspection found the scaffold suitable for a response micro-pilot. In particular, `no_memory` prompts were visibly less answerable than v1 because exact commands and implementation constraints were absent from current task notes.

## v2 API Response Collection from 7.4-F

The API micro-pilot collected 30 DeepSeek V4 Flash responses:

| Field | Value |
| --- | ---: |
| Prompt count | 30 |
| API OK count | 30 |
| Usable response count | 30 |
| Empty OK response count | 0 |
| Error count | 0 |
| Retry count summary | 29 rows at 0; 1 row at 1 |

The payload boundary was preserved: only the system instruction and each row's `prompt_text` were sent. Local labels, strategy names, expected requirements, oracle/gold fields, and scoring metadata were not sent.

Automatic citation diagnostics were clean for citation format: hallucinated memory citations, current-unit citations, and bare memory references all averaged 0.00 across strategies. The automatic metrics still showed the intended hard-negative shape:

| Strategy | E2E required recall | Avoid avg | Stale avg | Contradictory avg |
| --- | ---: | ---: | ---: | ---: |
| `no_memory` | 0.00 | 0.00 | 0.00 | 0.00 |
| `all_candidates` | 0.90 | 1.80 | 0.40 | 0.80 |
| `budgeted_candidate_order` | 0.20 | 1.80 | 0.20 | 0.20 |
| `keyword_top_k` | 0.80 | 1.40 | 0.60 | 0.20 |
| `random_k` | 0.40 | 2.20 | 0.40 | 0.00 |
| `oracle_selected` | 1.00 | 0.00 | 0.00 | 0.00 |

## v2 Rubric Review from 7.4-G

The internal rubric review scored each response on six 0/1/2 fields and summed them into `manual_utility`.

| Strategy | Avg utility | Req facts | Irrelevant clean | Stale/contrad clean | Quality | Strong | Missing req |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_memory` | 8.80 | 0.20 | 2.00 | 2.00 | 1.00 | 0 | 5 |
| `all_candidates` | 7.60 | 2.00 | 0.80 | 0.40 | 0.40 | 1 | 0 |
| `budgeted_candidate_order` | 7.00 | 1.00 | 0.80 | 1.40 | 0.80 | 0 | 5 |
| `keyword_top_k` | 8.80 | 1.60 | 1.20 | 1.20 | 0.80 | 1 | 2 |
| `random_k` | 8.80 | 1.00 | 1.00 | 2.00 | 1.00 | 0 | 5 |
| `oracle_selected` | 12.00 | 2.00 | 2.00 | 2.00 | 2.00 | 5 | 0 |

Rubric observations:

- `oracle_selected` behaved like a clean upper-bound reference: every reviewed oracle response scored 12/12.
- `no_memory` was less sufficient at response level than in v1: all five no-memory responses missed required memory-only details, with average required fact coverage of 0.20.
- `all_candidates` recovered required facts but exposed contamination risk: four of five rows had irrelevant-contamination flags and four of five had stale/contradictory-contamination flags.
- `budgeted_candidate_order` no longer behaved like a pseudo-oracle: all five rows missed required facts and average utility was the lowest among strategies at 7.00.
- `keyword_top_k` was mixed: it sometimes recovered enough memory to produce a strong answer, but it still showed hard-negative failures such as repeating stale cache-invalidation guidance.
- `random_k` exposed missing-required behavior in all five rows while staying cleaner than `all_candidates` on stale/contradictory use in this five-case subset.

## Required Questions

Did v2 reduce candidate-order bias at selection level?

Yes, for this diagnostic fixture. `budgeted_candidate_order` dropped to 0.25 post-budget required recall in selection metrics and 0.20 response-level required citation recall, while `oracle_selected` stayed at 1.00. The manual review also found all five budgeted responses missing required facts.

Did v2 make `no_memory` less sufficient at response level?

Yes. `no_memory` produced clean but generic answers. It had 0.20 average required fact coverage and 5/5 missing-required flags. This is materially different from the v1 concern where current task notes often carried enough answer content.

Did `oracle_selected` behave like a clean upper bound?

Yes. It had full selection required recall, full response required citation recall, no automatic contamination citations, 12.00 average manual utility, and 5/5 strong-answer flags.

Did `all_candidates` expose contamination risk?

Yes. It had high required fact coverage but mixed correct details with stale, contradictory, or irrelevant memories. The clearest example is `hard_read_v2_001__all_candidates`, which cites the required retry policy and test command while also instructing disabling payment retries from contradictory memory.

Did `keyword_top_k` and `random_k` expose hard-negative or missing-required failures?

Yes. `keyword_top_k` had good response citation recall on average but still selected hard negatives and produced stale-use failures, including the catalog-search row that repeats stale Solr-era cache guidance. `random_k` had lower required recall and missed required facts in all five reviewed responses.

Is v2 strong enough to expand to 30-40 cases?

Yes, as a diagnostic fixture. The v2 pilot now separates oracle, no-memory, all-candidates, lexical, random, and candidate-order behaviors more clearly than v1. Expansion should preserve the same safeguards: shuffled candidate order, under-specified task notes, hidden labels, redaction checks, automatic citation diagnostics, and internal rubric review.

## Recommendation

Recommendation: **A. expand v2 hard READ to 30-40 cases.**

Reasoning:

- The main v1 blockers were addressed well enough for a larger diagnostic set: candidate-order bias is reduced and `no_memory` is no longer sufficient for memory-only details.
- The v2 response pilot produced stable operational artifacts: 30 usable responses, no empty OK rows, clean citation formatting, and reproducible rubric aggregation.
- A larger 30-40 case set is the most direct next step before live LoRA/backend integration, because the current evidence is still fixture-level and small-sample.
- A Streamlit/CLI trace viewer can wait until the larger fixture exists; revising the v2 fixture again is not necessary before expansion unless the user wants stricter manual rubric calibration.

Recommended next context: expand v2 hard READ to 30-40 cases while preserving the current prompt, scoring, and review boundaries.

## Claim Boundary

This synthesis supports only a small diagnostic expansion decision. It does not prove downstream utility, does not evaluate a learned router/live LoRA backend, does not establish production readiness, does not measure retrieval quality outside this fixture, and does not support a claim that any routing approach outperforms alternatives.
