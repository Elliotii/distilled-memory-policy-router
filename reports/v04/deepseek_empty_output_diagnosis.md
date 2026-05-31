# DeepSeek Empty Output Diagnosis

Date: 2026-05-31  
Status: P5.5-A2 diagnosis + controlled retry completed

## Scope

This checkpoint diagnoses the 7 empty outputs from the previous 5-case DeepSeek V4 Flash-compatible A/B/C smoke run and performs one controlled retry on the same 5 cases.

This is still only a 5-case smoke. It is not a 30-50 case subset, not a full 200-case run, not a formal A/B/C conclusion, and not a basis for v0.5 training.

No API keys, tokens, headers, Authorization values, or raw API responses were printed or written.

## Prior Empty Output Distribution

Prior prediction file:

```text
data/v04/model_predictions/p5_smoke_predictions.jsonl
```

Summary:

| Item | Count |
| --- | ---: |
| Total rows | 15 |
| Empty rows | 7 |
| HTTP/API exception rows | 0 |
| Whitespace-only non-empty rows | 0 |

Empty rows by interface:

| Interface | Empty rows |
| --- | ---: |
| `legacy_span_json` | 3 |
| `unit_json` | 2 |
| `unit_dsl` | 2 |

Empty rows by case:

| Case ID | Empty rows |
| --- | ---: |
| `v04_pilot_0001` | 1 |
| `v04_pilot_0038` | 1 |
| `v04_pilot_0081` | 3 |
| `v04_pilot_0137` | 2 |

Sensitive-boundary concentration:

- Empty rows from sensitive-boundary cases: 3/7.
- Sensitive-boundary empty rows all came from `v04_pilot_0081`.
- Empty rows were not exclusive to sensitive-boundary cases.

Latency:

| Group | Avg ms | Min ms | Max ms |
| --- | ---: | ---: | ---: |
| All prior rows | 5875.0 | 3515 | 7612 |
| Empty prior rows | 6518.7 | 5666 | 7612 |
| Non-empty prior rows | 5311.8 | 3515 | 7607 |

Prior run limitation: response shape metadata was not captured in `p5_smoke_predictions.jsonl`, so prior empty rows cannot be attributed to `finish_reason`, reasoning-only content, or alternate text fields with certainty.

## API Config Availability

Only boolean/source-name information was recorded.

| Item | Available | Source |
| --- | ---: | --- |
| `.env` file | true | repo root |
| API key | true | `MEMORY_ROUTER_API_KEY` |
| Base URL | true | `MEMORY_ROUTER_BASE_URL` |
| Model | true | `MEMORY_ROUTER_MODEL` |
| DeepSeek-like model name | true | `deepseek-v4-flash` |

The retry did not print or store the base URL value, API key value, headers, or Authorization header.

## Runner Changes

Updated `src/v04/model_output_runner.py` with narrowly scoped diagnostics:

- robust final-output extraction from common OpenAI-compatible fields:
  - `choices[0].message.content`
  - `choices[0].text`
  - top-level `output_text`
  - top-level `text`
  - `output[*].content[*].text`
- sanitized response metadata:
  - `http_status`
  - `top_level_keys`
  - `choices_count`
  - `finish_reason`
  - `message_keys`
  - `content_length`
  - `has_content`
  - `has_text`
  - `has_output_text`
  - `has_reasoning_content`
  - `reasoning_content_length`
  - `usage_keys`
  - `extraction_source`
- `stream: false` in the request payload.
- default `max_tokens` raised to 1024.
- configurable empty-output error message for retry rows.

The runner still does not use `reasoning_content` as `raw_output`; it records only whether reasoning content exists and its length.

## Controlled Retry Settings

Retry prediction file:

```text
data/v04/model_predictions/p5_smoke_retry_predictions.jsonl
```

Settings:

| Setting | Value |
| --- | --- |
| Cases | same 5-case subset |
| Interfaces | same `legacy_span_json`, `unit_json`, `unit_dsl` |
| Model | `deepseek-v4-flash` |
| System | `deepseek_v4_flash_smoke_retry` |
| Temperature | 0 |
| Max tokens | 1024 |
| Timeout | 90 seconds |
| Stream | false |
| Reasoning effort | not sent |
| Prompt templates | unchanged |

## Sanitized Retry Metadata

Retry rows:

| Item | Count |
| --- | ---: |
| Total rows | 15 |
| Empty rows | 0 |
| HTTP/API exception rows | 0 |
| Rows with response metadata | 15 |
| `finish_reason=stop` | 15 |
| `extraction_source=message.content` | 15 |
| Rows with reasoning content present | 15 |

Content-length range from sanitized metadata:

| Min content chars | Max content chars |
| ---: | ---: |
| 29 | 393 |

## Retry Eval Results

Eval command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.eval_runner \
  --cases data/v04/model_predictions/p5_smoke_cases.jsonl \
  --predictions data/v04/model_predictions/p5_smoke_retry_predictions.jsonl \
  --report reports/v04/model_output_smoke_retry_interface_report.md \
  --error-report reports/v04/model_output_smoke_retry_error_analysis.md
```

Retry metrics:

| Interface | Parse success | Exact match | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 100.0% | 40.0% | 1.000 | 0.833 | 80.0% | 0.833 |
| `unit_json` | 100.0% | 60.0% | 1.000 | 0.833 | 80.0% | 0.833 |
| `unit_dsl` | 100.0% | 40.0% | 0.923 | 0.923 | 83.3% | 0.909 |

Invalid memory, invalid unit/span, invalid target, and span-copying error rates were all 0.0% in the retry report.

Generated retry reports:

- `reports/v04/model_output_smoke_retry_interface_report.md`
- `reports/v04/model_output_smoke_retry_error_analysis.md`

## Retry Before/After

| Interface | Initial parse | Retry parse | Initial exact | Retry exact | Initial empty | Retry empty |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 40.0% | 100.0% | 20.0% | 40.0% | 3 | 0 |
| `unit_json` | 40.0% | 100.0% | 40.0% | 60.0% | 2 | 0 |
| `unit_dsl` | 60.0% | 100.0% | 20.0% | 40.0% | 2 | 0 |

## Likely Cause Assessment

Most likely:

- The prior empty outputs were not caused by HTTP/API failures.
- The prior run lacked response metadata, so the exact cause is not provable.
- The controlled retry eliminated empty outputs with `max_tokens=1024`, `stream=false`, no `reasoning_effort`, and robust extraction.
- Since retry extraction always used `message.content`, alternate-field extraction was not needed in the successful retry.

Possible but not proven:

- Prior empty rows may have been intermittent provider behavior.
- Prior empty rows may have been affected by response-shape or reasoning/content behavior; retry metadata shows reasoning content was present in all rows, but final `message.content` was also present in all retry rows.
- Prior truncation or insufficient completion budget may have contributed, especially since one prior `unit_json` row was unterminated.
- Sensitive-boundary content may contribute to instability for `v04_pilot_0081`, but the pattern was not exclusive to sensitive cases.

Less likely after retry:

- A pure wrapper extraction bug. Robust extraction was added, but every retry row used `message.content`, the same primary field the previous runner expected.

## Recommendation

Do not treat this as a formal A/B/C conclusion and do not enter v0.5 training.

It is now reasonable to consider a 30-50 case smoke only after owner review, because:

- API path is available.
- Empty outputs were eliminated in controlled retry.
- eval_runner accepts and scores external model outputs.
- The 5-case retry still shows semantic errors and false stores, so a larger subset is useful for failure characterization, not for claims.

Recommended next step:

- If the owner accepts this diagnosis, run a 30-50 case subset with the retry settings and the same metadata logging.
- Keep Qwen local testing for the planned 4070 Super desktop environment.
