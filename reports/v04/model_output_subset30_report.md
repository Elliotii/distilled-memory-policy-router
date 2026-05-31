# DeepSeek 30-Case Model-Output Subset Report

Date: 2026-05-31  
Status: P5.5-B completed

## Scope

This checkpoint collects real DeepSeek V4 Flash-compatible raw model outputs for a representative 30-case v0.4 pilot subset across the three existing A/B/C prompt interfaces:

- A: `legacy_span_json`
- B: `unit_json`
- C: `unit_dsl`

This run is only a 30-case subset for model-output characterization. It is not a 50-case run, not a full 200-case pilot evaluation, not Qwen testing, not training, and not a v0.5 data-generation step.

No API keys, tokens, auth headers, request headers, raw provider responses, or secret-bearing URLs were printed or written.

## Model Path

| Item | Value |
| --- | --- |
| Model role | Strong baseline |
| Model ID | `deepseek-v4-flash` |
| System name | `deepseek_v4_flash_subset30` |
| Run ID | `p5_subset30_20260531_2330` |
| Temperature | 0 |
| Max tokens | 1024 |
| Timeout | 90 seconds per call |
| Stream | false |
| Reasoning effort | not sent |
| Empty-output retry | at most 1 immediate retry |

## Subset Case IDs

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
```

Files:

- Case IDs: `data/v04/model_predictions/p5_subset30_case_ids.txt`
- Subset cases: `data/v04/model_predictions/p5_subset30_cases.jsonl`

## Subset Coverage

Gold output shape:

| Shape | Count |
| --- | ---: |
| READ-only | 7 |
| STORE/SKIP-only | 12 |
| READ + STORE joint | 11 |

Required tag coverage:

| Coverage item | Count |
| --- | ---: |
| `stale_memory` | 2 |
| `related_but_useless` | 3 |
| `target_boundary` | 8 |
| `sensitive_boundary` | 10 |
| `user_profile_boundary` | 7 |
| `repo_convention` | 7 |
| `service_vs_task_state` | 2 |
| `project_vs_repo` | 3 |
| `repo_vs_service` | 3 |

Gold STORE target distribution:

| Target | Count |
| --- | ---: |
| `project_memory` | 5 |
| `repo_memory` | 7 |
| `service_memory` | 10 |
| `task_state` | 9 |
| `user_profile` | 7 |

Selection rationale:

- Kept several 5-case smoke anchors for continuity.
- Added stale and related-but-useless cases to test irrelevant READ control.
- Added target-boundary cases across project/repo, repo/service, and service/task-state distinctions.
- Added user-profile and sensitive-boundary cases to check whether sensitive material is skipped.
- Included parser/evaluator/repo-convention cases to keep the subset aligned with the project domain.

## Prediction JSONL

Prediction file:

```text
data/v04/model_predictions/p5_subset30_predictions.jsonl
```

Call summary:

| Item | Count |
| --- | ---: |
| Cases | 30 |
| Interfaces per case | 3 |
| Expected rows | 90 |
| Written rows | 90 |
| Rows with empty first output | 2 |
| Rows still empty after retry | 1 |
| Rows with error field | 1 |
| Rows with `finish_reason=stop` | 88 |
| Rows with `finish_reason=length` | 2 |
| Rows with `extraction_source=message.content` | 89 |
| Rows with `extraction_source=none` | 1 |

Empty/retry details:

| Case ID | Interface | Retry | Result |
| --- | --- | ---: | --- |
| `v04_pilot_0137` | `unit_json` | true | still empty; `empty model output after retry` |
| `v04_pilot_0190` | `legacy_span_json` | true | retry succeeded |

## Eval Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.eval_runner \
  --cases data/v04/model_predictions/p5_subset30_cases.jsonl \
  --predictions data/v04/model_predictions/p5_subset30_predictions.jsonl \
  --report reports/v04/model_output_subset30_interface_report.md \
  --error-report reports/v04/model_output_subset30_error_analysis.md
```

Generated eval reports:

- `reports/v04/model_output_subset30_interface_report.md`
- `reports/v04/model_output_subset30_error_analysis.md`

## Metrics By Interface

| Interface | Parse success | Exact match | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | False store | Irrelevant read | Sensitive store | Invalid memory | Invalid unit/span | Invalid target | Span-copying error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 93.3% | 43.3% | 0.895 | 0.861 | 93.5% | 0.824 | 8.8% | 10.5% | 0.0% | 0.0% | 4.3% | 0.0% | 4.3% |
| `unit_json` | 96.7% | 46.7% | 0.827 | 0.895 | 94.1% | 0.882 | 10.5% | 16.2% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `unit_dsl` | 100.0% | 40.0% | 0.810 | 0.909 | 91.4% | 0.899 | 10.3% | 22.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Typical Raw Output Issues

- `unit_json` had one empty final output after the allowed retry (`v04_pilot_0137`).
- `legacy_span_json` had one invalid JSON row (`v04_pilot_0194`).
- `legacy_span_json` had one exact-span-copying failure (`v04_pilot_0164`), which made several unit assignments invalid for that row.
- Semantic misses remain even when structure is valid:
  - false STORE on read-only or stale/related cases;
  - irrelevant READs on related-but-useless and user-profile boundary cases;
  - some project-level decisions predicted as `task_state`;
  - one service invariant predicted as `task_state`.
- No interface produced sensitive STOREs in this 30-case subset.

## Preliminary A/B/C Observation

This is not a formal interface conclusion.

On this subset:

- `unit_dsl` had the best structural stability: 100.0% parse success and no invalid ID/target/span errors.
- `unit_json` had the highest exact match rate, but one row remained empty after retry.
- `legacy_span_json` had stronger READ F1 in this sample, but still showed JSON and exact-span-copying fragility.
- The main residual errors are semantic routing errors, not parser/validator failures.

## Limitations

- 30 cases are useful for characterization but not final proof.
- Results should not be used directly as v0.5 training evidence.
- Interface differences and model capability are still confounded by the single-model setup.
- Qwen3-4B / Qwen3.5 local testing remains deferred to the planned 4070 Super desktop environment.
- Prompt changes should not be made from this report alone; they need owner review and a controlled follow-up.

## Recommendation

- Review this subset report and the detailed eval/error reports first.
- If more stability evidence is needed, expand to a 50-case subset with the same retry settings and the same sanitized metadata.
- Run Qwen candidates later on the 4070 Super desktop using the same subset for matched comparison.
- Do not proceed directly to v0.5 training from this 30-case subset.
