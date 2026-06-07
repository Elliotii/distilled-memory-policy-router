# v1.0 Mac Handoff Preflight

Date: 2026-06-08
Context: 6.0 clean Mac handoff / v1.0 packaging preflight
Status: PASS with packaging issues to address in later contexts

## Scope

This preflight verifies that the clean Mac workspace is ready to start v1.0 portfolio packaging. It does not modify README, data, metrics, predictions, model weights, existing reports, or source code.

The project remains a lightweight Memory Policy Router for coding/business-agent contexts. It is not a MemoryOS, not a retriever, not a memory database, and not a memory writer/update system.

## Git Gate

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| Active repo root | `/Users/elliot/new-systems/dmpr-v1/distilled-memory-policy-router` | `/Users/elliot/new-systems/dmpr-v1/distilled-memory-policy-router` | PASS |
| Branch | `codex/v10-packaging` | `codex/v10-packaging` | PASS |
| HEAD tag | `v0.5g-bf16-lora-4090-complete` | `v0.5g-bf16-lora-4090-complete` | PASS |
| Worktree before preflight docs | clean | clean | PASS |
| Nested git repo / superproject | none | none | PASS |

Recent commits:

```text
fed6cb0 Complete v0.5g BF16 LoRA 4090 final synthesis
7e40f02 Prepare v0.5g BF16 LoRA server runbook
6efc878 Complete v0.5e gold_v2 evaluation synthesis
```

## Required Reading Completed

Canonical and status:

- `docs/planning/lightweight_memory_policy_router_project_spec.md`
- `docs/status/CURRENT_STATE.md`
- `docs/v04_planning/V04_TO_V10_STEERING_PLAN.md`

v0.5g result documents:

- `docs/v05g/V05G_BF16_LORA_4090_FINAL_RESULTS.md`
- `reports/v05g/v05g_bf16_lora_4090_final_report.md`
- `reports/v05g/v05g_bf16_lora_4090_gold_v2_result.md`
- `reports/v05g/v05g_bf16_lora_4090_error_analysis.md`
- `reports/v05g/v05g_bf16_lora_4090_claims_and_limitations.md`
- `reports/v05g/v05g_bf16_lora_4090_artifact_manifest.md`

v0.5e comparison documents:

- `reports/v05e/v05e_final_project_report.md`
- `reports/v05e/v05e_final_experiment_summary.md`
- `reports/v05e/v05e_gold_v2_009_four_system_eval_report.md`

Artifact folders inspected:

- `configs/v05g/`
- `data/v05g/model_predictions/`
- `reports/v05g/server_runs/`
- `.gitignore`

README status:

- `README.md` is missing.
- Packaging state: missing, not draft/outdated/ready.

External handoff folders:

- No matching `../dmpr_v05g_v10_handoff_*` directory was present.
- No external adapters were copied into the repo.

## v0.5g Final Result Confirmed

Locked gold set: `gold_v2_009`, 150 active cases.

Best evaluated system: BF16 standard LoRA r16 1000-targeted under RTX 4090 fallback settings.

| Metric | BF16 r16 500_4090 | BF16 r16 1000_4090 |
| --- | ---: | ---: |
| Gold exact | 16.7% | 36.0% |
| Gold parse | 98.7% | 99.3% |
| Gold READ F1 | 80.1% | 84.6% |
| Gold STORE F1 | 89.2% | 99.0% |
| Gold SKIP F1 | 84.0% | 98.1% |
| Gold target accuracy | 84.7% | 100.0% |
| Gold false store rate | 10.4% | 1.2% |
| Gold sensitive store | 0/4 | 0/4 |

Important interpretation:

- BF16 alone is not sufficient: BF16 r16 500_4090 gold exact is 16.7%.
- The strong result is BF16 standard LoRA r16 plus 1000 targeted-balanced data.
- Main gains are write-side routing: STORE, SKIP, and target classification.
- READ remains the full-exact bottleneck.
- This is an RTX 4090 fallback result, not an A100 result.
- No downstream utility has been measured yet.
- No production safety claim is supported.

## Mechanical Checks

### Final Report Presence

All requested v0.5g and v0.5e report files are present.

### Prediction Row Counts

| File | Expected rows | Observed rows | Result |
| --- | ---: | ---: | --- |
| `data/v05g/model_predictions/bf16_r16_500_4090_dev_predictions.jsonl` | 100 | 100 | PASS |
| `data/v05g/model_predictions/bf16_r16_1000_4090_dev_predictions.jsonl` | 100 | 100 | PASS |
| `data/v05g/model_predictions/bf16_r16_500_4090_gold_v2_009_predictions.jsonl` | 150 | 150 | PASS |
| `data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl` | 150 | 150 | PASS |

### Metrics JSON Parse

| File | Result |
| --- | --- |
| `reports/v05g/server_runs/v05g_bf16_r16_500_4090_dev_metrics.json` | PASS |
| `reports/v05g/server_runs/v05g_bf16_r16_1000_4090_dev_metrics.json` | PASS |
| `reports/v05g/server_runs/v05g_bf16_r16_500_4090_gold_v2_009_metrics.json` | PASS |
| `reports/v05g/server_runs/v05g_bf16_r16_1000_4090_gold_v2_009_metrics.json` | PASS |

Note: `python` is not available on PATH in this Mac workspace. JSON parse checks passed with `python3`.

### Gold Hash

Expected:

```text
f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72
```

Observed for `data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl`:

```text
f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72
```

Result: PASS.

### Ignored Runtime Artifacts

| Path | Ignore rule | Result |
| --- | --- | --- |
| `results/v05g_bf16_lora/` | `.gitignore:44` | PASS |
| `logs/v05g/` | `.gitignore:45` | PASS |

The ignored runtime artifact directories were not present in the working tree during this preflight.

## Packaging Issues Found

1. `README.md` is missing. Context 6.1 should create it from the existing evidence, with explicit limitations.
2. There is a schema-story reconciliation issue for packaging: the canonical v0.3 project spec describes `{read_hints, write_spans, ignore_spans}`, while the later v0.4/v0.5 artifacts use unit-based READ / STORE / SKIP with five STORE targets. v1.0 docs should explain this as project evolution, not silently mix the schemas.
3. v0.5g reports document strong write-side metrics, but no downstream-lite benchmark exists yet. Any README or resume language must avoid claiming downstream utility until Context 6.4 measures an efficiency proxy.
4. The strongest result is RTX 4090 fallback BF16 LoRA r16 1000-targeted. Packaging must not call it an A100 result or imply BF16 alone caused the gain.
5. The repo has no external handoff folder available for checksum comparison in this workspace.

## Docs Needed for v1.0

Recommended v1.0 documentation set:

- `README.md`: concise portfolio entry, result table, quickstart, scope limits.
- `docs/v10/ARCHITECTURE_AND_TASK_FORMULATION.md`: router task, unit schema, target definitions, boundary against MemoryOS/RAG/retriever.
- `docs/v10/V10_PACKAGING_EXECUTION_PLAN.md`: context-by-context execution plan.
- `docs/v10/RELATED_WORK_NOTES.md`: short positioning against agent memory, policy routing, small-model distillation.
- `docs/v10/DEMO_GUIDE.md`: demo CLI usage and fixture explanation, after Context 6.3.
- `reports/v10/v10_downstream_lite_efficiency_proxy.md`: after Context 6.4, if built and run.
- `docs/v10/RESUME_BULLETS_AND_INTERVIEW_NOTES.md`: after Context 6.5.
- `reports/v10/v10_final_audit.md`: final audit before tagging.

## Preflight Decision

v1.0 packaging can start.

Recommended next context: Context 6.1, README plus project/results narrative.

Stop point: Context 6.0 only. Do not proceed to Context 6.1 in this turn.

