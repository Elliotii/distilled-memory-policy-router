# DeepSeek 50-Case Model-Output Subset Report

Date: 2026-06-01  
Status: P5.5-C completed

## Scope

This checkpoint expands the DeepSeek V4 Flash-compatible A/B/C model-output subset from 30 cases to 50 total cases.

This run:

- kept the existing prompt templates unchanged;
- reused all 30-case prediction rows from P5.5-B;
- selected 20 additional pilot cases;
- called the model only for the 20 additional cases;
- evaluated the merged 50-case prediction file with the existing eval_runner.

This is not a 100-case or full 200-case run, not Qwen testing, not training, and not v0.5 data generation.

No API keys, tokens, auth headers, request headers, raw provider responses, or secret-bearing URLs were printed or written.

## Model Path

| Item | Value |
| --- | --- |
| Model role | Strong baseline |
| Model ID | `deepseek-v4-flash` |
| Merged system name | `deepseek_v4_flash_subset50` |
| New20 run ID | `p5_subset50_new20_20260601_0010` |
| Temperature | 0 |
| Max tokens | 1024 |
| Timeout | 90 seconds per call |
| Stream | false |
| Reasoning effort | not sent |
| Empty-output retry | at most 1 immediate retry |

## Subset50 Case IDs

```text
v04_pilot_0001
v04_pilot_0003
v04_pilot_0005
v04_pilot_0017
v04_pilot_0027
v04_pilot_0136
v04_pilot_0141
v04_pilot_0038
v04_pilot_0039
v04_pilot_0043
v04_pilot_0044
v04_pilot_0063
v04_pilot_0161
v04_pilot_0162
v04_pilot_0163
v04_pilot_0164
v04_pilot_0168
v04_pilot_0170
v04_pilot_0194
v04_pilot_0081
v04_pilot_0083
v04_pilot_0090
v04_pilot_0107
v04_pilot_0133
v04_pilot_0137
v04_pilot_0143
v04_pilot_0153
v04_pilot_0186
v04_pilot_0188
v04_pilot_0190
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

## New20 Case IDs

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

Selection rationale:

- Kept all P5.5-B subset30 cases for continuity.
- Added project/task boundary cases after B2 identified `project_memory -> task_state` as the main target confusion.
- Added stale and related-but-useless cases to stress READ precision and false STORE behavior.
- Added repo/service and service/task-state cases for target-boundary coverage.
- Added user-profile/sensitive cases to keep sensitive-store monitoring active.
- Added SOP/skill out-of-scope examples and one READ-only repo-convention/distractor case.

## Coverage Distribution

Gold output shape:

| Shape | Count |
| --- | ---: |
| READ-only | 11 |
| STORE/SKIP-only | 22 |
| READ + STORE joint | 17 |

Key tag coverage:

| Tag | Count |
| --- | ---: |
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

Gold STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 11 |
| `repo_memory` | 13 |
| `service_memory` | 16 |
| `task_state` | 16 |
| `user_profile` | 10 |

## Prediction JSONL

Files:

- Case IDs: `data/v04/model_predictions/p5_subset50_case_ids.txt`
- Cases: `data/v04/model_predictions/p5_subset50_cases.jsonl`
- New20 IDs: `data/v04/model_predictions/p5_subset50_new20_case_ids.txt`
- New20 cases: `data/v04/model_predictions/p5_subset50_new20_cases.jsonl`
- New20 predictions: `data/v04/model_predictions/p5_subset50_new20_predictions.jsonl`
- Merged predictions: `data/v04/model_predictions/p5_subset50_predictions.jsonl`

Call and merge summary:

| Item | Count |
| --- | ---: |
| Model calls this round | 60 |
| New20 prediction rows | 60 |
| Reused subset30 rows | 90 |
| Merged subset50 rows | 150 |
| Unique case_id x interface rows | 150 |
| Empty-after-retry rows in new20 | 1 |
| Empty-after-retry rows in merged subset50 | 2 |
| Rows retried in new20 | 2 |
| Rows retried in merged subset50 | 4 |
| Rows with `finish_reason=stop` in merged subset50 | 147 |
| Rows with `finish_reason=length` in merged subset50 | 3 |

Empty/retry details:

| Case ID | Interface | Source | Result |
| --- | --- | --- | --- |
| `v04_pilot_0137` | `unit_json` | subset30 reused | still empty after retry |
| `v04_pilot_0145` | `unit_json` | subset50 new20 | still empty after retry |
| `v04_pilot_0190` | `legacy_span_json` | subset30 reused | retry succeeded |
| `v04_pilot_0139` | `legacy_span_json` | subset50 new20 | retry succeeded |

## Eval Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.eval_runner \
  --cases data/v04/model_predictions/p5_subset50_cases.jsonl \
  --predictions data/v04/model_predictions/p5_subset50_predictions.jsonl \
  --report reports/v04/model_output_subset50_interface_report.md \
  --error-report reports/v04/model_output_subset50_error_analysis.md
```

Generated eval reports:

- `reports/v04/model_output_subset50_interface_report.md`
- `reports/v04/model_output_subset50_error_analysis.md`

## 50-Case Metrics

| Interface | Parse success | Exact match | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store | Invalid memory | Invalid unit/span | Invalid target | Span-copying error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 96.0% | 48.0% | 0.872 | 0.864 | 92.6% | 0.832 | 8.5% | 10.5% | 0.0% | 0.0% | 2.5% | 0.0% | 2.5% |
| `unit_json` | 96.0% | 50.0% | 0.845 | 0.870 | 94.7% | 0.844 | 12.3% | 12.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `unit_dsl` | 100.0% | 42.0% | 0.839 | 0.872 | 93.1% | 0.847 | 13.4% | 18.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## 30-vs-50 Delta

Percentage-point deltas are shown for rate metrics. F1/accuracy values are raw score deltas.

| Interface | Parse pp | Exact pp | READ F1 | STORE F1 | Target acc pp | SKIP F1 | False store pp | Irrelevant read pp | Sensitive store pp |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | +2.7 | +4.7 | -0.023 | +0.003 | -1.0 | +0.008 | -0.3 | +0.0 | +0.0 |
| `unit_json` | -0.7 | +3.3 | +0.018 | -0.025 | +0.6 | -0.038 | +1.8 | -3.7 | +0.0 |
| `unit_dsl` | +0.0 | +2.0 | +0.029 | -0.037 | +1.7 | -0.052 | +3.2 | -3.2 | +0.0 |

## Typical Raw Output Issues

- `unit_json` still has empty-after-retry failures: `v04_pilot_0137` and `v04_pilot_0145`.
- `legacy_span_json` still has JSON/span fragility:
  - `v04_pilot_0194`: invalid/truncated JSON.
  - `v04_pilot_0164`: exact-span-copying failure from including unit labels in copied spans.
- `unit_dsl` still has no structural failures, invalid IDs, invalid targets, or prose contamination.
- False STORE errors increased in `unit_json` and `unit_dsl` after adding harder stale/related cases.
- `unit_dsl` still over-reads more than the other interfaces, though its irrelevant-read rate improved from subset30.

## Target-Boundary Findings

Target confusion among correctly predicted STORE units:

| Interface | Main confusions |
| --- | --- |
| `legacy_span_json` | `project_memory -> task_state` x2; `repo_memory -> service_memory` x2 |
| `unit_json` | `project_memory -> task_state` x2; `project_memory -> service_memory` x1 |
| `unit_dsl` | `project_memory -> task_state` x3; `service_memory -> task_state` x1 |

Interpretation:

- `project_memory` vs `task_state` remains the primary target-boundary issue.
- `repo_memory` vs `service_memory` remains present but secondary.
- `service_memory` vs `task_state` is still occasional, especially in Unit DSL.
- `user_profile` vs sensitive/private remains clean in this subset: sensitive store is still 0.0% across all interfaces.

## A/B/C Preliminary Observation

This is still not a final interface conclusion.

Current 50-case answers to the重点 questions:

- Unit DSL parse success remains highest: yes, `unit_dsl` stayed at 100.0%.
- Unit DSL READ F1 remains weaker than Legacy and Unit JSON: yes, `unit_dsl` READ F1 is 0.839 versus 0.872 legacy and 0.845 unit JSON.
- Unit JSON exact advantage remains: yes, `unit_json` exact is 50.0%, highest of the three.
- Legacy Span JSON fragility remains: yes, legacy still has invalid/truncated JSON and exact-span-copying failure.
- `project_memory` vs `task_state` remains the main target confusion: yes.
- Sensitive store remains 0.0%: yes.
- Empty-after-retry remains low: yes, 2/150 rows, but both are `unit_json`, so the pattern should be tracked.

Overall:

- `unit_dsl` is the cleanest structural interface and remains the best evidence for v0.4's low-entropy output direction.
- `unit_json` looks strongest on exact match in this DeepSeek subset, but the margin is modest and it has the recurring empty-output issue.
- Legacy remains a useful baseline but not a preferred interface because its failures are exactly the v0.3 span/JSON failure class.

## Limitations

- 50 cases are stronger than 30 but still not final proof.
- This is one model path only; it does not tell us how Qwen3-4B or Qwen3.5 will behave.
- The subset was intentionally enriched with harder boundary cases, so absolute rates should not be treated as pilot-wide prevalence.
- Reused subset30 rows preserve prior model outputs; this run did not repeat those 30 cases.
- These results should not be used directly for v0.5 training decisions.

## Recommendation

Stop expanding DeepSeek for now and move to matched Qwen comparison when the 4070 Super desktop environment is ready.

Recommended next steps:

1. Run Qwen3-4B / Qwen3.5 on the same 50-case subset with the same A/B/C prompts and eval flow.
2. Keep prompts unchanged for Qwen matched comparison, so DeepSeek and Qwen are comparable.
3. Track whether `unit_json` empty-after-retry is provider/model-specific or prompt/interface-specific.
4. Do a small manual review of `project_memory` vs `task_state` gold labels before any v0.5 training step.
5. Defer prompt-v2 changes until after matched Qwen results, unless the project owner explicitly chooses a prompt optimization branch.
