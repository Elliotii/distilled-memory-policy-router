# Hard READ v2 Expanded Downstream Subset Synthesis

## Scope

This synthesis combines four v2 expanded hard READ artifacts:

- Context 7.5-A: the 32-case expanded selection fixture and fixture audit.
- Context 7.5-B: the 8-case, 48-row downstream subset prompt scaffold.
- Context 7.5-C: the 48-response API micro-pilot and automatic citation diagnostics.
- Context 7.5-D: the internal rubric review of the 48 generated responses.

This is diagnostic evidence only. It is not a downstream utility proof, does not evaluate learned router/live LoRA behavior, does not establish production memory-system behavior, and does not support a claim that any routing approach is better than alternatives.

## Selection Fixture Result

The expanded fixture preserves reduced candidate-order bias. In the 32-case selection evaluation, `budgeted_candidate_order` has mean post-selection required recall of 0.0625, while `oracle_selected` and `all_candidates` are both 1.0000. The first-four required-recall distribution is also concentrated at zero: 28 of 32 cases have 0.00 first-four required recall and only 4 reach 0.50.

That means candidate order is no longer a reliable accidental shortcut for required memories. The expanded fixture is therefore a stronger diagnostic surface for hard READ behavior than the earlier candidate-order-friendly setup.

## Response Quality Result

The 48-row response review confirms that `no_memory` is insufficient for memory-only details. It remains clean on contamination and citation behavior, but every reviewed row misses the required memory-only facts. Its average required-fact score is 0.00 and all 8 rows are flagged as generic no-memory responses.

`oracle_selected` remains a clean upper-bound reference at response quality level. It averages 12.00 manual utility, 2.00 required-fact coverage, 2.00 task response quality, and has zero missing-required, irrelevant-contamination, stale/contradictory, hallucinated-memory, or citation flags across the 8 reviewed cases.

`all_candidates` exposes contamination risk at response quality level. It has the second-highest average manual utility at 8.75 and often recovers required facts, but it also has 3 missing-required flags, 3 irrelevant-contamination flags, 4 stale/contradictory flags, and 2 citation issues. The strongest failures are cases where required evidence is present but stale or contradictory memories alter the actual instruction.

`keyword_top_k` and `random_k` expose hard-negative and missing-required failures. `keyword_top_k` averages 6.50 utility with 7 missing-required flags, 7 irrelevant-contamination flags, and 7 stale/contradictory flags. `random_k` averages 6.875 utility with 7 missing-required flags, 6 irrelevant-contamination flags, and 6 stale/contradictory flags. Both strategies can produce useful individual responses when the selected set happens to contain enough required evidence, but the expanded subset shows frequent failure modes.

`budgeted_candidate_order` remains weak in the expanded setting. It averages 6.50 utility, has 8 missing-required flags, and has 8 irrelevant-contamination flags. This is consistent with the expanded fixture's intentionally reduced candidate-order required recall.

## Automatic Citation Diagnostics

The 48-response API run was operationally clean: 48 usable responses, 0 empty OK responses, and 0 errors. Automatic citation hygiene remained clean: hallucinated memory citations, current-unit citations, and bare memory references all averaged 0.00 across strategies.

Automatic citation scoring was still not sufficient by itself. Several responses cited real memory IDs cleanly while using stale, contradictory, or unrelated facts incorrectly. The manual review is therefore needed to interpret whether cited facts were used in an aligned way.

## Strategy Utility Summary

| Strategy | Rows | Avg manual utility | Avg required-fact coverage | Missing-required flags | Contamination flags |
| --- | ---: | ---: | ---: | ---: | ---: |
| `oracle_selected` | 8 | 12.00 | 2.00 | 0 | 0 |
| `all_candidates` | 8 | 8.75 | 1.625 | 3 | 3 |
| `no_memory` | 8 | 8.00 | 0.00 | 8 | 0 |
| `random_k` | 8 | 6.875 | 0.875 | 7 | 6 |
| `budgeted_candidate_order` | 8 | 6.50 | 0.625 | 8 | 8 |
| `keyword_top_k` | 8 | 6.50 | 0.625 | 7 | 7 |

## Packaging Readiness

The expanded artifacts are sufficient for v1.0-applied packaging as diagnostic evidence. The package can now include:

- A 32-case expanded hard READ fixture with reduced candidate-order bias.
- A representative 8-case, 48-row downstream subset scaffold.
- A successful 48-response API micro-pilot run report.
- Automatic citation diagnostics.
- A filled internal rubric review and generated aggregate report.
- Clear claim boundaries and limitations.

Further downstream expansion would improve confidence and error characterization, but it is not necessary before packaging the current diagnostic evidence. Live LoRA/backend integration and UI trace tooling should remain out of scope for this packaging step.

## Recommendation

Recommendation: A. package v1.0-applied evidence now.

Reason: Contexts 7.5-A through 7.5-D now cover the key evidence chain requested for the applied package: expanded selection behavior, prompt scaffold, successful 48-response run, automatic citation diagnostics, and response-level rubric review. The remaining gaps are well understood and documented as limitations rather than blockers for a bounded diagnostic package.

Recommended next context: prepare the v1.0-applied packaging summary and release checklist from the existing v10 artifacts, without creating a git tag unless explicitly requested.
