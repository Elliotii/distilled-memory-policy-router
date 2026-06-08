# Hard READ Downstream Micro-Pilot Synthesis

Context: 7.4-C hard READ downstream rubric review and synthesis.

## Scope

This synthesis combines three diagnostic artifacts:

- 7.3 hard READ selection-only metrics.
- 7.4-B automatic citation diagnostics from the 24-response DeepSeek micro-pilot.
- 7.4-C internal rubric review of the 24 responses.

This is not a formal benchmark. It does not evaluate learned router/live LoRA behavior and should not be described as a human evaluation.

## 7.3 Selection Metrics

The 10-case selection-only pilot showed that the harness can produce strategy-specific memory contexts and expose hard-negative behavior:

| Strategy | Required recall | Mean injected | Avoid injected | Stale injected | Contradictory injected | Mean context chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `all_candidates` | 1.00 | 8.00 | 50 | 10 | 10 | 913.90 |
| `budgeted_candidate_order` | 1.00 | 4.00 | 10 | 0 | 0 | 459.50 |
| `keyword_top_k` | 0.65 | 4.00 | 26 | 8 | 4 | 469.20 |
| `no_memory` | 0.00 | 0.00 | 0 | 0 | 0 | 0.00 |
| `oracle_selected` | 1.00 | 3.00 | 0 | 0 | 0 | 334.70 |
| `random_k` | 0.50 | 4.00 | 25 | 4 | 2 | 456.40 |

Selection-level interpretation:

- `all_candidates` preserves required recall but injects all avoid, stale, and contradictory memories.
- `oracle_selected` is the clean reference context.
- `keyword_top_k` and `random_k` expose hard-negative contamination.
- `budgeted_candidate_order` looks strong on this pilot, but the fixture order is structured and should not be treated as realistic retrieval rank quality.

## 7.4-B Citation Diagnostics

The DeepSeek response collection path works on the 24-prompt subset:

- Prompt count: 24.
- API OK rows: 24.
- Usable nonempty responses after B-S token-budget repair: 24.
- Empty OK responses after B-S: 0.
- Citation formatting was clean: no hallucinated memory citations, no bare memory refs, and no current-unit citations.

Automatic citation metrics showed the expected hard-negative pattern:

| Strategy | Coverage | Required citation recall | Avoid avg | Stale avg | Contradictory avg |
| --- | ---: | ---: | ---: | ---: | ---: |
| `all_candidates` | 1.00 | 1.00 | 2.00 | 0.75 | 0.75 |
| `budgeted_candidate_order` | 1.00 | 1.00 | 0.25 | 0.00 | 0.00 |
| `keyword_top_k` | 1.00 | 0.50 | 1.75 | 0.50 | 0.50 |
| `no_memory` | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `oracle_selected` | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| `random_k` | 1.00 | 0.50 | 1.25 | 0.50 | 0.25 |

These are citation diagnostics only. They do not measure full answer quality.

## 7.4-C Internal Rubric Review

The internal rubric review scored each response on six 0/1/2 fields and summed them into `manual_utility`.

| Strategy | Avg utility | Required facts | Irrelevant clean | Stale/contrad clean | Quality | Strong answers | Missing required |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `oracle_selected` | 12.00 | 2.00 | 2.00 | 2.00 | 2.00 | 4 | 0 |
| `budgeted_candidate_order` | 11.75 | 2.00 | 1.75 | 2.00 | 2.00 | 3 | 0 |
| `no_memory` | 10.25 | 1.00 | 2.00 | 2.00 | 1.25 | 0 | 4 |
| `random_k` | 8.00 | 1.00 | 0.75 | 1.25 | 1.00 | 0 | 3 |
| `all_candidates` | 7.50 | 2.00 | 0.25 | 0.50 | 0.75 | 0 | 0 |
| `keyword_top_k` | 7.50 | 1.00 | 0.75 | 1.00 | 0.75 | 0 | 3 |

Review-level interpretation:

- `oracle_selected` provides a clean upper-bound reference for these cases.
- `budgeted_candidate_order` scored well, but its strength is tied to the structured fixture ordering.
- `no_memory` answers are clean but often miss memory-only details such as exact commands or implementation policy.
- `all_candidates` recovers required facts while creating over-noisy or contaminated answers.
- `keyword_top_k` shows the clearest lexical hard-negative failure: it can miss required memories and use contradictory distractors.

## What The Micro-Pilot Supports

- The harness can generate strategy-specific memory contexts.
- DeepSeek response collection works on 24 prompts with a clear payload boundary.
- Citation format is clean after current-unit IDs were hidden and the token budget was repaired.
- Memory context appears diagnostically meaningful in selected cases because memory-backed strategies recover details that `no_memory` misses.
- `all_candidates` exposes contamination risk when stale, contradictory, or irrelevant memories are injected.
- `oracle_selected` provides a clean upper-bound reference for fixture inspection.

## What The Micro-Pilot Does Not Support

- It does not prove downstream utility.
- It does not evaluate learned router/live LoRA behavior.
- It does not show that any router outperforms alternatives.
- It does not establish a production memory system.
- It is not the full hard READ benchmark.
- It does not resolve READ as a relevance-selection problem.

## Recommendation

Recommendation: **D. revise fixture/prompt design first.**

Reasoning:

- The current micro-pilot is useful and reproducible, but `budgeted_candidate_order` is too strong because the selected fixture order is structured.
- Before expanding to 30-40 cases, the hard READ set should randomize or adversarially vary candidate order, add more realistic retrieval-like rankings, and include cases where required memories are not front-loaded.
- The prompt and review design should preserve the successful B-S response-coverage repair: final-answer-only system instruction, larger completion budget, and explicit usable-response diagnostics.
- After fixture design is less order-sensitive, the next expansion can more fairly compare `all_candidates`, lexical/BM25, random, oracle, and any learned selector or reranker.

Recommended next context: revise the hard READ fixture and prompt design before running a larger 30-40 case evaluation or adding live LoRA.
