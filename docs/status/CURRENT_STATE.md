# CURRENT_STATE

## Last Updated
2026-06-01 00:23 CST

## Current Milestone
P5.5-C: DeepSeek 50-case A/B/C model-output subset

## Completed
- Re-read required project, v0.4 planning/spec, prompt, runner, metrics, eval_runner, subset30 prediction, subset30 reports, and B2 error-review files.
- Accepted P5.5-B2 decision path:
  - prompts unchanged;
  - pilot/bridge data unchanged;
  - parser, validator, metrics, and eval_runner unchanged;
  - expand to 50 total cases, not 50 additional cases.
- Selected 20 additional representative pilot cases not present in subset30.
- Created 50-case total subset files, preserving all 30 subset30 cases.
- Validated subset50 and new20 case files.
- Called DeepSeek-compatible model only for the 20 new cases:
  - 20 cases x 3 interfaces = 60 new calls.
  - Same prompt templates.
  - Same retry/settings as P5.5-B.
- Reused existing subset30 predictions without recalling those cases.
- Merged subset30 and new20 predictions into a 150-row subset50 prediction JSONL.
- Evaluated subset50 with existing eval_runner against the 50-case subset file, not full pilot data.
- Generated subset50 interface and error reports.
- Created `reports/v04/model_output_subset50_report.md`.
- Did not run 100/200 cases, Qwen, training, v0.5 generation, prompt edits, pilot/bridge edits, parser/validator/metrics/eval_runner edits, retriever/writer/MemoryOS, or dependency/model downloads.

## Files Changed
- Added `data/v04/model_predictions/p5_subset50_case_ids.txt`.
- Added `data/v04/model_predictions/p5_subset50_cases.jsonl`.
- Added `data/v04/model_predictions/p5_subset50_new20_case_ids.txt`.
- Added `data/v04/model_predictions/p5_subset50_new20_cases.jsonl`.
- Added `data/v04/model_predictions/p5_subset50_new20_predictions.jsonl`.
- Added `data/v04/model_predictions/p5_subset50_predictions.jsonl`.
- Added `reports/v04/model_output_subset50_report.md`.
- Added `reports/v04/model_output_subset50_interface_report.md`.
- Added `reports/v04/model_output_subset50_error_analysis.md`.
- Updated `docs/status/CURRENT_STATE.md`.

## Tests / Commands Run
- Required `sed` reads for:
  - `docs/planning/lightweight_memory_policy_router_project_spec.md`
  - `docs/status/CURRENT_STATE.md`
  - `docs/v04_planning/V04_TO_V10_STEERING_PLAN.md`
  - `docs/v04_planning/CODEX_WORKFLOW_RULES.md`
  - `docs/v04_spec/PREDICTION_FORMAT.md`
  - `docs/v04_spec/EVAL_PLAN.md`
  - `docs/v04_spec/TARGET_GUIDELINE.md`
  - `docs/v04_spec/CASE_SCHEMA.md`
  - `prompts/v04/legacy_span_json.txt`
  - `prompts/v04/unit_json.txt`
  - `prompts/v04/unit_dsl.txt`
  - `src/v04/model_output_runner.py`
  - `src/v04/eval_runner.py`
  - `src/v04/metrics.py`
  - P5.5-B/B2 reports and prediction files.
- Scoped `git status --short --untracked-files=all -- ...` before writing new files.
- Generated subset50/new20 case files from `data/v04/pilot_cases.jsonl`.
- Validation:
  - `data/v04/model_predictions/p5_subset50_cases.jsonl`: valid, 50 records.
  - `data/v04/model_predictions/p5_subset50_new20_cases.jsonl`: valid, 20 records.
- Safe env check:
  - `PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.model_output_runner --check-env`
  - Result: `.env` exists; key/base/model available; model `deepseek-v4-flash`; no secret values printed.
- New20 model collection:
  - `PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.model_output_runner --case-ids data/v04/model_predictions/p5_subset50_new20_case_ids.txt --smoke-cases data/v04/model_predictions/p5_subset50_new20_cases.jsonl --output data/v04/model_predictions/p5_subset50_new20_predictions.jsonl --system deepseek_v4_flash_subset50 --run-id p5_subset50_new20_20260601_0010 --max-tokens 1024 --timeout-seconds 90 --temperature 0 --retry-empty-once --empty-output-error 'empty model output after retry'`
  - Result: 60 rows written, 1 row with error field.
- Merged predictions:
  - subset30 reused rows: 90.
  - subset50 new20 rows: 60.
  - merged subset50 rows: 150.
  - every `case_id x interface` appears exactly once.
- Eval:
  - `PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.eval_runner --cases data/v04/model_predictions/p5_subset50_cases.jsonl --predictions data/v04/model_predictions/p5_subset50_predictions.jsonl --report reports/v04/model_output_subset50_interface_report.md --error-report reports/v04/model_output_subset50_error_analysis.md`
  - Result: evaluated 50 cases across 3 interface/system groups; wrote both reports.
- Metric/delta extraction with Python over eval_runner outputs.
- Final validations:
  - `data/v04/model_predictions/p5_subset50_cases.jsonl`: valid, 50 records.
  - `data/v04/model_predictions/p5_subset50_new20_cases.jsonl`: valid, 20 records.
  - `data/v04/pilot_cases.jsonl`: valid, 200 records.
  - `data/v04/bridge_cases.jsonl`: valid, 40 records.
- Final `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile src/v04/model_output_runner.py src/v04/eval_runner.py src/v04/metrics.py`
  - Result: OK.
- Final `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`
  - Result: `Ran 49 tests in 0.003s` / `OK`.
- Final row checks:
  - `p5_subset50_new20_predictions.jsonl`: 60 rows, 60 unique `case_id x interface` keys, 20 cases.
  - `p5_subset50_predictions.jsonl`: 150 rows, 150 unique `case_id x interface` keys, 50 cases.
- Secret-leakage scan over P5.5-C generated/changed files:
  - Result: `secret leakage found: False`.
- Final scoped git status:
  - Result: P5.5-C files are present alongside pre-existing untracked v0.4 files; no prompt, pilot, bridge, parser, validator, metrics, or eval_runner edits were made in this milestone.
- `TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M %Z'`
  - Result: `2026-06-01 00:23 CST`.

## Subset50 Selection
Subset files:

- `data/v04/model_predictions/p5_subset50_case_ids.txt`
- `data/v04/model_predictions/p5_subset50_cases.jsonl`
- `data/v04/model_predictions/p5_subset50_new20_case_ids.txt`
- `data/v04/model_predictions/p5_subset50_new20_cases.jsonl`

New20 case IDs:

```text
v04_pilot_0009
v04_pilot_0050
v04_pilot_0062
v04_pilot_0166
v04_pilot_0171
v04_pilot_0138
v04_pilot_0146
v04_pilot_0151
v04_pilot_0139
v04_pilot_0145
v04_pilot_0149
v04_pilot_0165
v04_pilot_0167
v04_pilot_0175
v04_pilot_0173
v04_pilot_0178
v04_pilot_0169
v04_pilot_0187
v04_pilot_0189
v04_pilot_0088
```

Subset50 coverage:

| Item | Count |
| --- | ---: |
| READ-only shape | 11 |
| STORE/SKIP-only shape | 22 |
| READ + STORE joint shape | 17 |
| `project_vs_repo` | 7 |
| `related_but_useless` | 6 |
| `stale_memory` | 5 |
| `repo_vs_service` | 6 |
| `service_vs_task_state` | 4 |
| `user_profile_boundary` | 10 |
| `sensitive_boundary` | 15 |
| `sop_skill_out_of_scope` | 3 |
| `target_boundary` | 18 |
| `repo_convention` | 9 |

Gold STORE targets:

| Target | Count |
| --- | ---: |
| `project_memory` | 11 |
| `repo_memory` | 13 |
| `service_memory` | 16 |
| `task_state` | 16 |
| `user_profile` | 10 |

## Prediction Files
- New20 predictions: `data/v04/model_predictions/p5_subset50_new20_predictions.jsonl`.
- Merged subset50 predictions: `data/v04/model_predictions/p5_subset50_predictions.jsonl`.
- System for merged rows: `deepseek_v4_flash_subset50`.
- New20 run ID: `p5_subset50_new20_20260601_0010`.
- Merged rows:
  - 90 `subset30_reused`.
  - 60 `subset50_new20`.
  - 150 total.
- New20 collection:
  - 60 rows.
  - 2 rows retried.
  - 1 empty-after-retry row.
- Merged subset50:
  - 150 rows.
  - 4 rows retried.
  - 2 empty-after-retry rows.
  - 2 rows with error field.
  - 147 rows with `finish_reason=stop`.
  - 3 rows with `finish_reason=length`.

Empty/retry rows:

| Case ID | Interface | Source | Result |
| --- | --- | --- | --- |
| `v04_pilot_0137` | `unit_json` | subset30 reused | empty after retry |
| `v04_pilot_0145` | `unit_json` | subset50 new20 | empty after retry |
| `v04_pilot_0190` | `legacy_span_json` | subset30 reused | retry succeeded |
| `v04_pilot_0139` | `legacy_span_json` | subset50 new20 | retry succeeded |

## Model Eval Results
| Interface | Parse success | Exact match | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 96.0% | 48.0% | 0.872 | 0.864 | 92.6% | 0.832 | 8.5% | 10.5% | 0.0% |
| `unit_json` | 96.0% | 50.0% | 0.845 | 0.870 | 94.7% | 0.844 | 12.3% | 12.5% | 0.0% |
| `unit_dsl` | 100.0% | 42.0% | 0.839 | 0.872 | 93.1% | 0.847 | 13.4% | 18.8% | 0.0% |

Structural notes:

- `legacy_span_json`: invalid memory 0.0%, invalid unit/span 2.5%, invalid target 0.0%, span-copying error 2.5%.
- `unit_json`: invalid memory 0.0%, invalid unit/span 0.0%, invalid target 0.0%.
- `unit_dsl`: invalid memory 0.0%, invalid unit/span 0.0%, invalid target 0.0%.

## 30-vs-50 Delta
| Interface | Parse pp | Exact pp | READ F1 | STORE F1 | Target acc pp | SKIP F1 | False store pp | Irrelevant read pp | Sensitive store pp |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | +2.7 | +4.7 | -0.023 | +0.003 | -1.0 | +0.008 | -0.3 | +0.0 | +0.0 |
| `unit_json` | -0.7 | +3.3 | +0.018 | -0.025 | +0.6 | -0.038 | +1.8 | -3.7 | +0.0 |
| `unit_dsl` | +0.0 | +2.0 | +0.029 | -0.037 | +1.7 | -0.052 | +3.2 | -3.2 | +0.0 |

## Open Issues
- `unit_json` empty-after-retry recurred:
  - subset30: `v04_pilot_0137`.
  - new20: `v04_pilot_0145`.
- `legacy_span_json` still has JSON/span-copying fragility.
- `unit_dsl` remains structurally best but still has lower READ F1 and higher irrelevant-read rate than the other two interfaces.
- `project_memory` vs `task_state` remains the main target confusion.
- Sensitive store remains 0.0%, but the subset is still not final proof.

## Risks / Scope Drift Watch
- Do not treat the 50-case subset as a final A/B/C conclusion.
- Do not proceed directly to v0.5 training.
- Do not tune prompts based only on this run; keep matched comparison clean unless owner approves a prompt-v2 branch.
- Do not modify pilot/bridge labels based on model predictions.
- Do not run Qwen in this thread unless explicitly confirmed and the intended environment is ready.
- Do not expand DeepSeek to 100/200 in this context.

## Recommended Next Step
- Stop DeepSeek expansion at 50 for now.
- Move to Qwen3-4B / Qwen3.5 matched comparison on the same 50-case subset when the planned 4070 Super desktop environment is ready.
- Keep prompts unchanged for that matched comparison.
- In parallel, manually review selected `project_memory` vs `task_state` gold labels before any v0.5 training decision.
