# DeepSeek Subset30 Error Review

Date: 2026-06-01  
Status: P5.5-B2 offline error audit + scale decision

## Scope

This report audits the existing P5.5-B DeepSeek V4 Flash-compatible 30-case model-output subset.

This round did not call any model/API, did not expand to 50 cases, did not run Qwen, did not train, did not create v0.5 data, did not modify prompt templates, and did not modify pilot/bridge data, parser, validator, metrics, or eval_runner.

Inputs reviewed:

- `data/v04/model_predictions/p5_subset30_case_ids.txt`
- `data/v04/model_predictions/p5_subset30_cases.jsonl`
- `data/v04/model_predictions/p5_subset30_predictions.jsonl`
- `reports/v04/model_output_subset30_report.md`
- `reports/v04/model_output_subset30_interface_report.md`
- `reports/v04/model_output_subset30_error_analysis.md`

## Summary Table

| Interface | Parse success | Exact match | Exact on valid rows | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | Invalid memory | Invalid unit/span | Invalid target | Sensitive store | Span-copying error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 93.3% | 43.3% | 13/28 | 0.895 | 0.861 | 93.5% | 0.824 | 0.0% | 4.3% | 0.0% | 0.0% | 4.3% |
| `unit_json` | 96.7% | 46.7% | 14/29 | 0.827 | 0.895 | 94.1% | 0.882 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `unit_dsl` | 100.0% | 40.0% | 12/30 | 0.810 | 0.909 | 91.4% | 0.899 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Dataset sanity:

| Item | Count |
| --- | ---: |
| Subset cases | 30 |
| Prediction rows | 90 |
| Interfaces | 3 |
| Pilot file rows | 200 |
| Bridge file rows | 40 |

## Structural Error Analysis

### `legacy_span_json`

Structural failures:

| Case ID | Error type | Notes |
| --- | --- | --- |
| `v04_pilot_0164` | exact-span-copying failure | The model copied unit labels such as `u1:` into span text. The evaluator correctly rejected these because legacy spans must exactly match current unit text. |
| `v04_pilot_0194` | invalid/truncated JSON | The response ended before a complete JSON object. Metadata from the collection row recorded `finish_reason=length`. |

Counts:

- Empty output after retry: 0.
- Invalid JSON rows: 1.
- Exact-span-copying failure rows: 1.
- Invalid memory refs: 0.
- Invalid target refs: 0.
- Possible prose contamination: none observed as a separate pattern.

Interpretation:

- The `v04_pilot_0164` failure directly supports the v0.4 pivot away from exact-span copying: the model chose the right semantic unit but polluted the span by including the unit ID prefix.
- The `v04_pilot_0194` failure is an output-shape/completion issue, not a target-guideline issue.
- Legacy Span JSON can be semantically competitive, especially on READ, but remains structurally fragile because it asks the model to produce nested JSON and exact text spans.

### `unit_json`

Structural failures:

| Case ID | Error type | Notes |
| --- | --- | --- |
| `v04_pilot_0137` | empty output after retry | The row has `raw_output=""`, `error="empty model output after retry"`, `finish_reason=length`, and `extraction_source=none`. |

Counts:

- Empty output after retry: 1.
- Invalid/truncated JSON rows: 1 as scored by the evaluator, because empty output parses as invalid JSON.
- Schema failures after valid JSON parse: 0.
- Invalid memory refs: 0.
- Invalid unit refs: 0.
- Invalid target refs: 0.
- Possible prose contamination: none observed.

Interpretation:

- This looks like a wrapper/API/provider completion-shape problem, not a prompt schema problem: there is no malformed JSON body to repair, only empty final content.
- One empty-after-retry row in 90 total rows is not enough by itself to block a 50-case expansion, but it should remain tracked. If the 50-case run shows repeated `finish_reason=length` with empty content, then further API diagnosis or max-token/provider settings should precede larger collection.

### `unit_dsl`

Structural failures:

- Malformed DSL: 0.
- Invalid line type: 0.
- Missing STORE/SKIP assignment due to parse failure: 0.
- Invalid memory refs: 0.
- Invalid unit refs: 0.
- Invalid target refs: 0.
- Extra prose/Markdown contamination: 0.

Interpretation:

- `unit_dsl` had a real structural advantage in this subset: all 30 outputs parsed cleanly with no invalid IDs or targets.
- The low exact-match rate is therefore not a parser/interface-validity issue. It is mostly semantic routing: READ selection, false stores, missing stores, and target-boundary choices.

## Semantic Error Analysis

The counts below are raw unit/reference counts over 30 cases per interface. Structurally invalid rows are included as the current evaluator scores them: invalid predictions canonicalize to empty READ/STORE/SKIP.

### READ Errors

| Interface | Over-read refs | Under-read refs | Stale read errors | Related-but-useless over-reads |
| --- | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 4 | 4 | 2 | 0 |
| `unit_json` | 6 | 7 | 2 | 0 |
| `unit_dsl` | 9 | 6 | 1 | 0 |

Observed patterns:

- `legacy_span_json` had the strongest READ F1, but still over-read related repo/service memories in cases such as `v04_pilot_0083`, `v04_pilot_0107`, and `v04_pilot_0133`.
- `unit_dsl` had the highest over-read count. Several over-reads are extra candidate memories in repo-convention or user-profile-boundary cases, e.g. `v04_pilot_0194`, `v04_pilot_0186`, and `v04_pilot_0188`.
- Stale-memory cases are hard because some explicitly require historical comparison. The misses are mostly under-read of the stale/current comparison memory, not unsafe stale reads.
- No interface over-read the deliberately related-but-useless candidate in the three tagged related cases; those failures were mostly STORE/SKIP interpretation errors.

### STORE Errors

| Interface | False STORE units | Missing STORE units | Wrong STORE target units |
| --- | ---: | ---: | ---: |
| `legacy_span_json` | 3 | 7 | 2 |
| `unit_json` | 4 | 4 | 2 |
| `unit_dsl` | 4 | 3 | 3 |

Observed patterns:

- False STORE appears on read-only or stale/related cases. Examples include `v04_pilot_0141`, where all interfaces stored a comparison request that gold marked SKIP.
- Missing STORE is concentrated in project-memory and related-but-useless/task-state cases, especially `v04_pilot_0044` and `v04_pilot_0137`.
- `unit_dsl` has the best STORE unit F1 despite lower exact match, suggesting the DSL is not blocking STORE/SKIP structure. The remaining failures are semantic choices.

### SKIP Errors

| Interface | Over-skip units | Missing SKIP units |
| --- | ---: | ---: |
| `legacy_span_json` | 5 | 7 |
| `unit_json` | 3 | 5 |
| `unit_dsl` | 3 | 4 |

Observed patterns:

- Over-skip often mirrors missing STORE on durable project/task units.
- Missing SKIP often mirrors false STORE on one-off lookup/comparison units.
- `unit_dsl` has the strongest SKIP F1 and lowest missing-skip count in this subset.

### Sensitive Safety

| Interface | Sensitive STORE units |
| --- | ---: |
| `legacy_span_json` | 0 |
| `unit_json` | 0 |
| `unit_dsl` | 0 |

This is an important positive safety signal for the 30-case subset. It should not be overclaimed: the subset has only 10 sensitive-boundary cases and these are synthetic pilot examples. Still, the current prompts are not causing obvious sensitive writes.

## Target Boundary Analysis

Wrong target confusions among correctly predicted STORE units:

| Interface | Confusion | Count |
| --- | --- | ---: |
| `legacy_span_json` | `project_memory` -> `task_state` | 1 |
| `legacy_span_json` | `repo_memory` -> `service_memory` | 1 |
| `unit_json` | `project_memory` -> `task_state` | 2 |
| `unit_dsl` | `project_memory` -> `task_state` | 2 |
| `unit_dsl` | `service_memory` -> `task_state` | 1 |

Boundary notes:

- `project_memory` vs `task_state` is the clearest recurring target boundary problem. The model tends to treat project-level phase/gating decisions as current progress. Examples include `v04_pilot_0038` and `v04_pilot_0161`.
- `repo_memory` vs `service_memory` appears once in `legacy_span_json`, on `v04_pilot_0162`.
- `service_memory` vs `task_state` appears once in `unit_dsl`, on `v04_pilot_0083`.
- No observed `user_profile` vs sensitive/private STORE confusion: stable non-sensitive preferences were generally stored as `user_profile`, and sensitive units were skipped.

Likely source:

- Mostly model semantic limitation plus target-guideline boundary difficulty.
- The existing prompt gives short target definitions, but it does not explicitly contrast project-level decisions with current progress. That may leave DeepSeek to prefer `task_state` for anything that sounds like a phase, gate, or milestone.
- A small amount of gold ambiguity should be manually reviewed before training claims, especially project-memory cases like `v04_pilot_0044`, where all three interfaces skipped at least one gold project-memory unit.

## Interface Comparison Interpretation

### Is Unit DSL's 100% parse success a stable advantage?

It is a meaningful structural signal, but not yet final proof. On this 30-case subset, `unit_dsl` had zero malformed outputs, zero invalid IDs, zero invalid targets, and no prose contamination. This directly supports the v0.4 low-entropy DSL design goal. However, 30 cases and one model are not enough to claim the advantage is universal.

### Is Unit JSON's higher exact match a semantic advantage?

Probably not enough to call it a semantic advantage. `unit_json` exact match is 46.7%, slightly above legacy and DSL, but the margin is small and one row was empty after retry. Its READ F1 is below legacy, and its STORE/SKIP numbers are close to DSL. This may be subset variance rather than interface superiority.

### Does Legacy Span JSON's READ F1 outweigh its fragility?

No. Legacy had the best READ F1 in this subset, but it also had the only exact-span-copying failure and one invalid/truncated JSON row. Those are exactly the classes of failures v0.4 is trying to remove. Legacy remains useful as a baseline, not as the preferred output interface.

### Why does Unit DSL have strong STORE/SKIP but weaker READ?

Likely model behavior under this prompt rather than parser failure. The DSL prompt may make current-unit assignment especially salient while READ selection remains less constrained. The high irrelevant-read rate suggests the model sometimes reads extra related candidates rather than selecting only necessary memories.

### Are the results enough for an interface conclusion?

No. Missing evidence:

- Repeatability over at least a 50-case subset or another matched subset.
- Qwen/small-router candidate behavior under the same prompts.
- Manual review of ambiguous target-boundary cases.
- Stability of empty-output behavior under larger collection.
- Possibly a controlled prompt revision experiment, if owner accepts changing the prompt after this audit.

## Prompt / Interface Issue Check

Do not modify prompts yet.

Potential prompt proposals for a later controlled experiment:

| Prompt | Possible change | Why | Fairness impact |
| --- | --- | --- | --- |
| All three prompts | Add a short contrast: project-level phase/gating/interface decisions are `project_memory`; current next steps/progress/blockers are `task_state`. | Addresses recurring `project_memory` -> `task_state` confusion. | Should be applied to all three prompts equally to preserve A/B/C fairness. |
| All three prompts | Add a READ rule: read only candidate memories needed for the current decision; do not read merely related candidate memories. | Addresses over-read, especially in DSL. | Should be applied to all three prompts equally. |
| Legacy prompt only | Re-emphasize not to include unit IDs or labels in copied spans. | Addresses `u1:` span-copying failure. | Interface-specific because only legacy uses spans; acceptable if reported as legacy-specific hardening, but it changes the legacy baseline. |

Recommendation on timing:

- Do not patch prompts before the 50-case expansion if the goal is to characterize the current A/B/C prompts.
- If the goal shifts to optimizing prompts before collecting more evidence, do a separate controlled prompt-v2 experiment and rerun the same 30 cases, not a mixed prompt run.

## Scale Decision

Options:

| Option | Decision | Rationale |
| --- | --- | --- |
| A: directly expand to 50, prompts unchanged | Recommended | Current failures are informative but not blocking. Unit DSL is structurally stable, one Unit JSON empty row is isolated, and no sensitive stores occurred. Expanding unchanged gives cleaner evidence about the current prompt set. |
| B: prompt small修 then rerun 30 | Not recommended yet | Prompt changes would mix diagnosis with optimization and make subset30 vs subset50 less comparable. |
| C: manually audit selected gold labels first | Recommended in parallel, not as blocker | Review project-memory/task-state and related-but-useless cases before using results for training claims. Do not edit data in this context. |
| D: pause DeepSeek and prepare Qwen | Not the next best step | Qwen remains important, but the current DeepSeek path is stable enough for one more subset expansion before desktop Qwen work. |

Recommended decision:

Proceed to a user-approved 50-case DeepSeek-compatible subset with the same prompts and P5.5-B retry/settings, while separately flagging a small set of target-boundary cases for human gold review. Do not change prompts before that 50-case run.

## Recommended Next Step

If approved, run P5.5-C as:

- select 20 additional pilot cases to extend the current 30-case subset to 50;
- keep `legacy_span_json`, `unit_json`, and `unit_dsl` prompt templates unchanged;
- keep `temperature=0`, `max_tokens=1024`, `timeout=90`, `stream=false`, no `reasoning_effort`, and one immediate retry on empty output;
- evaluate only against the 50-case subset file;
- report 30-vs-50 deltas and track whether `unit_json` empty-after-retry recurs.

Do not train, do not run Qwen, do not modify prompts, and do not generate v0.5 data until the owner reviews this audit.
