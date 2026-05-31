# v0.4 P5.1 Compliance Audit

Date: 2026-05-31  
Status: P5.1 compliance audit + minimal gap fix  
Scope: A/B/C evaluation harness only; no model calls, training, pilot data edits, parser edits, validator edits, retriever, writer, MemoryOS, or v0.5 data generation.

## Summary

P5 harness v1 substantially met the steering/spec/eval-plan requirements. The main gap found in P5.1 was that `src/v04/eval_runner.py` could run deterministic systems but could not yet load future external prediction JSONL files. P5.1 fixed this with minimal support for `--predictions path/to/predictions.jsonl`, using the row shape documented in `docs/v04_spec/PREDICTION_FORMAT.md`.

P5.1 also made two small report-support fixes:

- `reports/v04/interface_pilot_report.md` now includes tag distribution, matching the eval plan reporting requirement.
- `reports/v04/error_analysis.md` now includes an interface/system overview and generic validation-error examples, so it remains useful for both deterministic smoke runs and future external prediction files.

## 1. Prompt Templates

Files checked:

- `prompts/v04/legacy_span_json.txt`
- `prompts/v04/unit_json.txt`
- `prompts/v04/unit_dsl.txt`

Compliance result: pass.

| Check | Result | Notes |
| --- | --- | --- |
| Same case information | Pass | All three prompts consume `RUNTIME_CONTEXT`, `CANDIDATE_MEMORIES`, and `CURRENT_UNITS`. |
| Only output interface changes | Pass | Task content is aligned: choose READ candidates, STORE durable current units, and SKIP/IGNORE non-durable current units. |
| Legacy exact span copying | Pass | Legacy prompt requires exact copy of one `CURRENT_UNITS` text value for `write_spans[*].span` and `ignore_spans[*]`. |
| Unit JSON uses unit IDs | Pass | Unit JSON prompt forbids spans and requires `unit_id`. |
| Unit DSL grammar alignment | Pass | Unit DSL prompt matches allowed parser forms: `READ <list|NONE>`, `STORE <target> <unit_id>`, `STORE NONE`, `SKIP <list|NONE>`. |
| Legal STORE targets listed | Pass | All prompts list exactly `user_profile`, `project_memory`, `repo_memory`, `service_memory`, `task_state`. |
| Every current unit assigned | Pass | All prompts require each current unit to appear exactly once in STORE/write or SKIP/ignore. |
| No explanatory output | Pass | All prompts forbid Markdown, comments, prose, explanations, confidence, reasons, offsets, rewritten memories, and downstream actions. |

No prompt changes were needed in P5.1.

## 2. Prediction Format

File checked:

- `docs/v04_spec/PREDICTION_FORMAT.md`

Compliance result: pass after minimal update.

| Check | Result | Notes |
| --- | --- | --- |
| Required row fields | Pass | Requires `case_id`, `interface`, `system`, and `raw_output`. |
| Interface enum | Pass | Documents only `legacy_span_json`, `unit_json`, and `unit_dsl`. |
| Raw output retention | Pass | `raw_output` stores the raw text to parse/score. |
| Optional metadata ignored | Pass | Optional fields such as `run_id`, `model_id`, `created_at`, `latency_ms`, and token counts are allowed but not required. |
| Future model-output collection | Pass | P5.1 added CLI usage for evaluating an existing prediction JSONL without calling models. |

Minimal P5.1 fix:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.eval_runner \
  --cases data/v04/pilot_cases.jsonl \
  --predictions path/to/predictions.jsonl \
  --report reports/v04/interface_pilot_report.md \
  --error-report reports/v04/error_analysis.md
```

The runner groups rows by `(interface, system)` and evaluates supplied `raw_output` only.

## 3. Metrics Coverage

Files checked:

- `src/v04/metrics.py`
- `reports/v04/interface_pilot_report.md`
- `reports/v04/error_analysis.md`

Compliance result: pass.

Structural metrics:

| Metric | Implemented | Notes |
| --- | --- | --- |
| `parse_success` | Yes | Valid canonical prediction rate after interface-specific parsing/validation. |
| `invalid_memory_id_rate` | Yes | Counts invalid predicted READ memory IDs. |
| `invalid_unit_or_span_rate` | Yes | Reported as `invalid_unit_id_rate`; legacy span failures also increment unit/span invalid counts. |
| `invalid_target_rate` | Yes | Counts illegal STORE targets or legacy `type` values. |
| `span_copy_error_rate` | Yes | Applies to Legacy Span JSON; zero for unit interfaces unless span refs exist. |
| `output_length` | Yes | Reports average/max chars, lines, and approximate tokens. |
| `human_repair_cost_proxy` | Yes | Deterministic proxy with levels 0-3. |

Semantic metrics:

| Metric | Implemented | Notes |
| --- | --- | --- |
| READ precision / recall / F1 | Yes | Set comparison on memory IDs. |
| STORE unit precision / recall / F1 | Yes | Set comparison on stored unit IDs. |
| STORE target accuracy | Yes | Among correctly predicted STORE units. |
| SKIP precision / recall / F1 | Yes | Set comparison on skipped unit IDs. |
| `false_store_rate` | Yes | Units predicted STORE where gold is SKIP divided by predicted STORE units. |
| `irrelevant_read_rate` | Yes | Predicted READ IDs not in gold divided by predicted READ IDs. |
| `sensitive_store_rate` | Yes | Explicit sensitive/private marker proxy over `sensitive_boundary` cases. |
| Exact target match | Yes | Requires parse success and exact READ/STORE/SKIP canonical match. |
| Target confusion | Yes | Implemented for correctly selected STORE units. |

Known limitation: P5.1 reports exact unit/ID metrics for v0.4 interfaces. The older project-wide v0.3 normalized span matching requirement is not implemented here because P5 v0.4 scoring maps all interfaces to unit-level canonical labels; this is acceptable for the P5 interface harness, but should be revisited if legacy span partial-overlap model outputs become a formal comparison target.

## 4. Interface-Specific Adapters

Compliance result: pass.

### Legacy Span JSON

| Check | Result | Notes |
| --- | --- | --- |
| JSON parse failure recorded | Pass | Invalid JSON returns invalid canonical prediction with errors. |
| Schema failure recorded | Pass | Missing/extra keys and wrong field types are errors. |
| `read_hints` constrained | Pass | READ IDs must be present candidate memories. |
| Exact current-unit span match | Pass | `write_spans` and `ignore_spans` must exactly match one `current_units[*].text`. |
| No semantic repair | Pass | Invalid spans do not get matched by fuzzy/paraphrase repair. |
| Legacy `type` as v0.4 target | Pass | `type` is checked against the five legal v0.4 targets only for fair comparison. |

### Unit JSON

| Check | Result | Notes |
| --- | --- | --- |
| JSON parse failure recorded | Pass | Invalid JSON returns invalid canonical prediction with errors. |
| Unit ID validation | Pass | STORE/SKIP unit IDs must appear in current units. |
| Target validation | Pass | STORE target must be one of the five legal v0.4 targets. |
| STORE/SKIP coverage | Pass | Every current unit must appear exactly once in STORE or SKIP. |
| No semantic repair | Pass | Invalid rows score as invalid/empty canonical predictions. |

### Unit DSL

| Check | Result | Notes |
| --- | --- | --- |
| Strict parser used | Pass | Calls `src.v04.parser.parse_policy_dsl`. |
| Invalid output clears canonical labels | Pass | Parser invalid results use empty READ/STORE/SKIP. |
| No semantic repair | Pass | Parser validates structure/IDs/targets only. |
| Grammar aligned with prompt | Pass | Prompt line forms match parser line forms. |

## 5. Eval Runner

File checked:

- `src/v04/eval_runner.py`

Compliance result: pass after minimal external JSONL support fix.

| Requirement | Result | Notes |
| --- | --- | --- |
| Load pilot cases | Pass | `load_cases` reads the selected JSONL after `validate_jsonl_file`. |
| Run deterministic systems | Pass | Supports `gold`, `empty`, `topk_read`, `heuristic`, `invalid_mock`. |
| Parse three interfaces | Pass | Uses `src.v04.metrics.parse_prediction` adapters. |
| Output summary metrics | Pass | Writes structural and semantic tables to `interface_pilot_report.md`. |
| Output per-case/error report | Pass | `case_details` are produced and `error_analysis.md` includes examples. |
| Gold sanity 100% | Pass | Gold-as-prediction is 100% parse success and exact match for all interfaces. |
| Invalid mock triggers errors | Pass | Invalid mock is 0% parse success and records unknown IDs / invalid targets / legacy span-copying errors. |
| External prediction JSONL | Pass after P5.1 fix | Added `--predictions`, row validation, optional metadata ignoring, and grouping by `(interface, system)`. |

External prediction JSONL support:

- CLI: `python3 -m src.v04.eval_runner --cases data/v04/pilot_cases.jsonl --predictions path/to/predictions.jsonl --report ... --error-report ...`
- Rows must include `case_id`, `interface`, `system`, and `raw_output`.
- Optional metadata is ignored.
- The runner does not call models or repair outputs.
- Test coverage: `tests/v04/test_eval_runner.py::test_external_prediction_jsonl_loads_and_evaluates` uses a temporary JSONL prediction file.

## 6. Reports

Files checked:

- `reports/v04/interface_pilot_report.md`
- `reports/v04/error_analysis.md`

Compliance result: pass after minimal report-support fixes.

| Check | Result | Notes |
| --- | --- | --- |
| Deterministic smoke disclaimer | Pass | Report states results are deterministic smoke only and not real model evidence. |
| No "DSL beats JSON" model conclusion | Pass | Report explicitly says real A/B/C claims require model outputs. |
| Case mix / tag distribution | Pass after P5.1 | Report now includes gold shapes, STORE targets, and tag distribution. |
| Structural and semantic metrics | Pass | Both tables present. |
| Target confusion | Pass | Error analysis includes target confusion for heuristic baseline. |
| Error examples | Pass after P5.1 | Error analysis includes generic validation-error examples across evaluated results. |
| Next step | Pass | Recommendation is model-output collection / owner review, not v0.5 training. |

## Smoke Results Rechecked

P5.1 deterministic smoke rerun:

- 200 pilot cases.
- 3 interfaces.
- 5 deterministic systems.
- Gold-as-prediction: 100% parse success and 100% exact target match across Legacy Span JSON, Unit JSON, and Unit DSL.
- Invalid mock: 0% parse success across all three interfaces.
- Heuristic baseline:
  - Exact target match: 33.5%.
  - READ F1: 0.529.
  - STORE unit F1: 0.948.
  - STORE target accuracy: 92.9%.
  - SKIP F1: 0.937.
  - False store rate: 5.6%.
  - Sensitive store rate: 0.0%.

These remain smoke-test numbers only and are not real model results.

## Files Audited

- `docs/status/CURRENT_STATE.md`
- `docs/v04_planning/V04_TO_V10_STEERING_PLAN.md`
- `docs/v04_planning/CODEX_WORKFLOW_RULES.md`
- `docs/v04_spec/V04_SPEC.md`
- `docs/v04_spec/EVAL_PLAN.md`
- `docs/v04_spec/CASE_SCHEMA.md`
- `docs/v04_spec/TARGET_GUIDELINE.md`
- `docs/v04_spec/PREDICTION_FORMAT.md`
- `prompts/v04/legacy_span_json.txt`
- `prompts/v04/unit_json.txt`
- `prompts/v04/unit_dsl.txt`
- `src/v04/metrics.py`
- `src/v04/eval_runner.py`
- `tests/v04/test_metrics.py`
- `tests/v04/test_eval_runner.py`
- `reports/v04/interface_pilot_report.md`
- `reports/v04/error_analysis.md`
- `data/v04/pilot_cases.jsonl`

## Conclusion

P5.1 finds the P5 harness compliant for its current checkpoint after the minimal external prediction JSONL fix. The harness is ready for owner review and future model-output collection. It is not a basis for v0.5 training by itself, and no deterministic smoke result should be presented as an A/B/C model-interface conclusion.
