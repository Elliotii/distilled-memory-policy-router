# Mac To Desktop Sync Manifest

Status: Context 4.5 Mac closeout  
Purpose: files that must be pushed from Mac and pulled on desktop WSL before Qwen matched comparison

## Sync Rule

Desktop Qwen work should start only after the desktop WSL repo has the same v0.4 files produced on Mac.

Do not commit secrets or local runtime artifacts:

- Do not commit `.env`.
- Do not commit API keys, tokens, credentials, auth headers, or secret-bearing URLs.
- Do not commit local model directories such as `/home/abc16/hf_models/...`.
- Do not commit `.venv/`.
- Do not commit caches, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, or `*.pyc`.
- Do not commit large model weights.
- Do not commit run logs that may contain secrets.

## 1. Planning / Steering Docs

Required for desktop readiness:

- `docs/planning/lightweight_memory_policy_router_project_spec.md`
- `docs/v04_planning/CODEX_WORKFLOW_RULES.md`
- `docs/v04_planning/V04_TO_V10_STEERING_PLAN.md`
- `docs/v04_planning/DESKTOP_QWEN_HANDOFF.md`
- `docs/v04_planning/MAC_TO_DESKTOP_SYNC_MANIFEST.md`

Optional reference:

- `docs/v04_planning/PROJECT_CONTEXT_FOR_CODEX.md`
- `docs/v04_planning/README.md`
- `docs/v04_planning/V03_TO_V04_DECISION_RECORD.md`
- `docs/v04_planning/V04_EXECUTION_PLAN.md`

## 2. v0.4 Spec Docs

Required for desktop readiness and Qwen inference:

- `docs/v04_spec/V04_SPEC.md`
- `docs/v04_spec/PREDICTION_FORMAT.md`
- `docs/v04_spec/EVAL_PLAN.md`
- `docs/v04_spec/CASE_SCHEMA.md`
- `docs/v04_spec/TARGET_GUIDELINE.md`

These define the schema, output format, legal targets, eval behavior, and scope boundaries. Do not alter them during desktop readiness.

## 3. Prompts

Required for Qwen inference:

- `prompts/v04/legacy_span_json.txt`
- `prompts/v04/unit_json.txt`
- `prompts/v04/unit_dsl.txt`

Important:

- Do not edit prompts before Qwen matched comparison.
- Qwen results must be comparable with DeepSeek results, so prompt text must stay unchanged.

## 4. src/v04 Code

Required for desktop readiness and Qwen evaluation:

- `src/v04/__init__.py`
- `src/v04/parser.py`
- `src/v04/case_validator.py`
- `src/v04/eval_runner.py`
- `src/v04/metrics.py`
- `src/v04/model_output_runner.py`

Notes:

- `eval_runner.py` and `metrics.py` are required to score Qwen prediction JSONL.
- `model_output_runner.py` contains prompt rendering, `.env` loading, OpenAI-compatible call support, and prior DeepSeek metadata behavior. For local Qwen, desktop may need a separate local inference wrapper, but it should preserve the same prediction JSONL schema.
- Do not change parser / validator / metrics / eval_runner for Qwen comparison unless a concrete bug is found and reported first.

## 5. tests/v04

Required for desktop readiness:

- `tests/v04/__init__.py`
- `tests/v04/test_parser.py`
- `tests/v04/test_case_validator.py`
- `tests/v04/test_eval_runner.py`
- `tests/v04/test_metrics.py`
- `tests/v04/test_model_output_runner.py`

Expected desktop readiness command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

Do not treat failing tests as a reason to edit data or prompts automatically. Diagnose first.

## 6. Data: v0.4 Pilot / Bridge / Subset50

Required for desktop readiness:

- `data/v04/bridge_cases.jsonl`
- `data/v04/bridge_cases_template.jsonl`
- `data/v04/pilot_cases.jsonl`

Required for Qwen inference:

- `data/v04/model_predictions/p5_subset50_case_ids.txt`
- `data/v04/model_predictions/p5_subset50_cases.jsonl`

Required reference from DeepSeek run:

- `data/v04/model_predictions/p5_subset50_predictions.jsonl`

Optional reference:

- `data/v04/model_predictions/p5_smoke_case_ids.txt`
- `data/v04/model_predictions/p5_smoke_cases.jsonl`
- `data/v04/model_predictions/p5_smoke_predictions.jsonl`
- `data/v04/model_predictions/p5_smoke_retry_predictions.jsonl`
- `data/v04/model_predictions/p5_subset30_case_ids.txt`
- `data/v04/model_predictions/p5_subset30_cases.jsonl`
- `data/v04/model_predictions/p5_subset30_predictions.jsonl`
- `data/v04/model_predictions/p5_subset50_new20_case_ids.txt`
- `data/v04/model_predictions/p5_subset50_new20_cases.jsonl`
- `data/v04/model_predictions/p5_subset50_new20_predictions.jsonl`

Expected desktop readiness checks:

```bash
wc -l data/v04/model_predictions/p5_subset50_case_ids.txt
wc -l data/v04/model_predictions/p5_subset50_cases.jsonl
python3 - <<'PY'
from src.v04.case_validator import validate_jsonl_file
print(validate_jsonl_file("data/v04/model_predictions/p5_subset50_cases.jsonl"))
PY
```

Expected counts:

- `p5_subset50_case_ids.txt`: 50 lines.
- `p5_subset50_cases.jsonl`: 50 records.
- `p5_subset50_predictions.jsonl`: 150 records.

## 7. Reports: DeepSeek / Harness

Required for desktop readiness:

- `reports/v04/model_output_subset50_report.md`
- `reports/v04/model_output_subset50_interface_report.md`
- `reports/v04/model_output_subset50_error_analysis.md`

Required context for interpreting DeepSeek baseline:

- `reports/v04/model_output_subset30_report.md`
- `reports/v04/model_output_subset30_interface_report.md`
- `reports/v04/model_output_subset30_error_analysis.md`
- `reports/v04/model_output_subset30_error_review.md`
- `reports/v04/deepseek_empty_output_diagnosis.md`

Optional reference:

- `reports/v04/model_output_smoke_report.md`
- `reports/v04/model_output_smoke_interface_report.md`
- `reports/v04/model_output_smoke_error_analysis.md`
- `reports/v04/model_output_smoke_retry_interface_report.md`
- `reports/v04/model_output_smoke_retry_error_analysis.md`
- `reports/v04/interface_pilot_report.md`
- `reports/v04/error_analysis.md`
- `reports/v04/p5_compliance_audit.md`
- `reports/v04/pilot_data_report.md`
- `reports/v04/pilot_semantic_audit.md`
- `reports/v04/bridge_report.md`

## 8. Status Docs

Required for desktop readiness:

- `docs/status/CURRENT_STATE.md`

The desktop context should read this first, then read:

- `docs/v04_planning/V04_TO_V10_STEERING_PLAN.md`
- `docs/v04_planning/CODEX_WORKFLOW_RULES.md`
- `docs/v04_planning/DESKTOP_QWEN_HANDOFF.md`

## 9. Files Not To Sync Through Git

Do not commit or push:

- `.env`
- `.env.*` files containing secrets
- API keys or token dumps
- local model folders
- `/home/abc16/hf_models/`
- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.DS_Store`
- `*.pyc`
- large model weights
- checkpoints
- local run logs with secrets
- temporary scratch outputs

Before commit, check:

```bash
git status --short --untracked-files=all
```

Review any new file paths carefully. Generated prediction JSONL and reports may be committed if they are intentionally small and contain no secrets.

## 10. Desktop Expected Next Artifacts

After Context 4.6-A readiness:

- no prediction files expected;
- no model calls expected;
- readiness report only.

After Context 4.6-B Qwen3-4B inference:

- `data/v04/model_predictions/qwen3_4b_subset50_predictions.jsonl`
- `reports/v04/qwen3_4b_subset50_report.md`
- `reports/v04/qwen3_4b_subset50_interface_report.md`
- `reports/v04/qwen3_4b_subset50_error_analysis.md`

These names are suggestions; if changed, keep them under `data/v04/model_predictions/` and `reports/v04/`, and document the exact paths.
