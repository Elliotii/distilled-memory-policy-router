# Learned-Router Downstream Rubric Synthesis

## Direct Answers

**Did learned_router outperform keyword_top_k, random_k, and budgeted_candidate_order in manual response quality?**

Partially yes. `learned_router` mean utility was 7.125, above `keyword_top_k` (6.500), `budgeted_candidate_order` (6.500), and `random_k` (6.875). The margin over random_k is small.

**Did learned_router outperform no_memory?**

No. `no_memory` scored 8.000. It missed memory-only facts, but it avoided the empty-response and contradiction failures that hurt learned_router.

**Was learned_router less contaminated than all_candidates?**

Not in the final manual utility result. learned_router had fewer average avoid citations automatically, but manual review found material contradiction/contamination in three rows. `all_candidates` scored higher overall at 8.750 despite its broader contamination exposure.

**How far is learned_router from oracle_selected?**

`oracle_selected` scored 12.000. `learned_router` scored 7.125, a 4.875-point gap on a 12-point rubric.

**Did contradictory injected memories materially hurt learned_router responses?**

Yes. Contradictory memories materially hurt `hard_read_v2_026`, `hard_read_v2_013`, and `hard_read_v2_031`. `hard_read_v2_011` cited stale/contradictory memories only to reject them, so that case was treated as minor/harmless rather than material harmful use.

**Did the one empty API response affect the conclusion?**

Yes. `hard_read_v2_009__learned_router` was empty after retries and scored 6 only because it had no harmful content; it contributed no required facts, no useful answer, and no compliant citations. Without the empty response, learned_router would still have visible contradiction failures, but the mean utility would be higher.

**Is this enough for final v1.0-applied packaging?**

Yes, for packaging a bounded applied-harness result with clear limitations. The result is not uniformly positive, but the learned-router path has now been run through selection replay, API response collection, automatic citation scoring, and manual rubric review.

## Supported Claims

- learned_router entered the applied harness downstream subset.
- learned_router has strong selection-level recall on 32 hard READ cases.
- learned_router shows measured downstream behavior on 8 hard READ subset cases.
- On this 8-case manual review, learned_router outperformed keyword_top_k, budgeted_candidate_order, and random_k in mean utility, but did not outperform no_memory, all_candidates, or oracle_selected.
- Contradictory hard-negative injection remains a real limitation for learned_router.

## Unsupported Claims

- production readiness;
- READ solved;
- real retriever performance;
- real cost savings;
- general downstream utility proof;
- complete MemoryOS;
- guaranteed safety.

## Packaging Note

Proceed to 7.6-G final v1.0-applied packaging with these limitations explicit. Do not tune the fixture or labels to improve learned_router results.
