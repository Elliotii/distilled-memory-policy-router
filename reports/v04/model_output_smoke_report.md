# v0.4 P5.5-A Model Output Smoke Report

Date: 2026-05-31  
Status: 5-case DeepSeek V4 Flash A/B/C smoke completed

## Scope

This checkpoint collected real raw model outputs for a small Context 4.5-A smoke run only:

- Model path: DeepSeek V4 Flash-compatible API.
- Role: strong baseline.
- Cases: 5 representative v0.4 pilot cases.
- Interfaces: `legacy_span_json`, `unit_json`, `unit_dsl`.
- Model calls: 15 total.

This is not a 30-50 case subset, not a full 200-case run, not training evidence, and not a v0.5 data-lock decision.

No API keys, tokens, headers, or secret values were printed or written.

## .env Audit

`.env` exists: true

Variable names found:

- `PACKY_API_KEY`
- `PACKY_BASE_URL`
- `PACKY_MODEL`
- `PACKY_TIMEOUT_SECONDS`
- `PACKY_TEMPERATURE`
- `PACKY_MAX_TOKENS`
- `PACKY_REASONING_EFFORT`
- `MEMORY_ROUTER_API_KEY`
- `MEMORY_ROUTER_BASE_URL`
- `MEMORY_ROUTER_MODEL`

Resolved DeepSeek-compatible config:

| Item | Available | Source |
| --- | ---: | --- |
| API key | true | `MEMORY_ROUTER_API_KEY` |
| Base URL | true | `MEMORY_ROUTER_BASE_URL` |
| Model | true | `MEMORY_ROUTER_MODEL` |
| Model deepseek-like | true | model name contains `deepseek` |

Used model name: `deepseek-v4-flash`

Qwen3-4B / Qwen3.5 were not attempted in this retry. Local Qwen smoke and later LoRA work should be handled on the 4070 Super desktop, as planned.

## Smoke Subset

Case ID file:

```text
data/v04/model_predictions/p5_smoke_case_ids.txt
```

Smoke case JSONL:

```text
data/v04/model_predictions/p5_smoke_cases.jsonl
```

Selected cases:

| Case ID | Coverage reason |
| --- | --- |
| `v04_pilot_0001` | READ-only parser/repo lookup with two useful memories and one skipped lookup unit. |
| `v04_pilot_0038` | STORE/SKIP-only target-boundary case: project-level decisions vs skipped local sandbox noise. |
| `v04_pilot_0039` | STORE/SKIP-only user-profile and sensitive-boundary case: stable preference stored, phone number and one-off instruction skipped. |
| `v04_pilot_0081` | READ + STORE joint case with service/repo stores and sensitive API-key dummy unit skipped. |
| `v04_pilot_0137` | Related-but-useless memory case: broad-domain distractor should not be read; task-state unit is stored. |

Subset validation:

- `data/v04/model_predictions/p5_smoke_cases.jsonl`: valid, 5 records.
- `data/v04/pilot_cases.jsonl`: valid, 200 records, unchanged.

## Prediction JSONL

Prediction file:

```text
data/v04/model_predictions/p5_smoke_predictions.jsonl
```

Rows:

| Interface | Rows | Empty model outputs |
| --- | ---: | ---: |
| `legacy_span_json` | 5 | 3 |
| `unit_json` | 5 | 2 |
| `unit_dsl` | 5 | 2 |

Total rows: 15  
Total empty model outputs: 7  
HTTP/API exception rows: 0

Empty outputs were preserved as `raw_output: ""` and marked with non-secret metadata `error: "empty model output"`.

## Eval Runner

Command used:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.eval_runner \
  --cases data/v04/model_predictions/p5_smoke_cases.jsonl \
  --predictions data/v04/model_predictions/p5_smoke_predictions.jsonl \
  --report reports/v04/model_output_smoke_interface_report.md \
  --error-report reports/v04/model_output_smoke_error_analysis.md
```

The 5-case smoke case file was used intentionally. Passing the full 200-case pilot file with only 15 prediction rows would count 195 unpredicted cases as empty outputs and would not represent this smoke run.

## Smoke Eval Results

| Interface | Parse success | Exact match | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 | Invalid memory | Invalid unit/span | Invalid target |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 40.0% | 20.0% | 0.444 | 0.286 | 100.0% | 0.600 | 0.0% | 0.0% | 0.0% |
| `unit_json` | 40.0% | 40.0% | 0.444 | 0.286 | 100.0% | 0.667 | 0.0% | 0.0% | 0.0% |
| `unit_dsl` | 60.0% | 20.0% | 0.400 | 0.667 | 66.7% | 0.800 | 0.0% | 0.0% | 0.0% |

Additional generated reports:

- `reports/v04/model_output_smoke_interface_report.md`
- `reports/v04/model_output_smoke_error_analysis.md`

## Typical Raw Output Issues

Observed in this 5-case smoke:

- Empty model output: 7/15 rows. These are the dominant structural failures.
- Invalid JSON from truncation or empty response:
  - `v04_pilot_0038` / `unit_json` returned an unterminated JSON object.
  - Empty `legacy_span_json` rows parse as invalid JSON.
- Semantic READ over-selection:
  - `v04_pilot_0001` / `unit_dsl` read `m2` in addition to gold `m1,m3`.
- Target-boundary mistakes:
  - `v04_pilot_0038` / `unit_dsl` stored `u1` as `task_state` where gold is `project_memory`.
- No invalid memory IDs, invalid unit IDs, invalid STORE targets, span-copying errors, false stores, or sensitive stores were counted among parseable outputs.

## Recommendation

Do not expand to 30-50 cases yet.

Recommended next step is a small owner review of the empty-output pattern before scaling:

- Check whether `deepseek-v4-flash` via the current API wrapper has content filtering or completion-shape behavior that explains empty outputs, especially around sensitive dummy units.
- Consider one controlled retry after that diagnosis, still on the same 5 cases, before any 30-50 subset.
- Keep Qwen local testing for the planned 4070 Super desktop environment.

## Limitations

- This 5-case smoke is useful for checking environment, prompt rendering, prediction JSONL, and eval_runner behavior only.
- It is not a formal A/B/C interface conclusion.
- It is not a basis for v0.5 training.
- DeepSeek V4 Flash is reported here as a strong baseline, not as the final teacher.
