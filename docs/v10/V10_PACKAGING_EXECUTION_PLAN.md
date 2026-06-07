# v1.0 Packaging Execution Plan

Date: 2026-06-08
Status: Context 6.0 plan, ready for Context 6.1

## Packaging Principles

The v1.0 package should present the project as a lightweight Memory Policy Router for coding/business-agent contexts.

Hard boundaries:

- Do not present the project as MemoryOS.
- Do not present it as a retriever, memory database, writer, update system, or complete coding agent.
- Do not train models unless explicitly requested in a future context.
- Do not run model inference unless explicitly requested in a future context.
- Do not change locked gold, metrics, predictions, or existing result reports.
- Do not copy adapter weights into git.
- Do not claim production safety, real downstream utility, real retriever performance, or A100 results.

Packaging should preserve the project history:

- v0.3: original JSON/span router contract in the canonical spec.
- v0.4: unit-based READ / STORE / SKIP interface and five STORE targets.
- v0.5: model training and evaluation.
- v0.5g: best evaluated result using BF16 standard LoRA r16 plus 1000 targeted-balanced data under RTX 4090 fallback settings.

## Context 6.1: README + Project/Results Narrative

Objective:

Create the public-facing project README and concise result narrative for v1.0 packaging.

Input files:

- `docs/planning/lightweight_memory_policy_router_project_spec.md`
- `docs/status/CURRENT_STATE.md`
- `docs/v05g/V05G_BF16_LORA_4090_FINAL_RESULTS.md`
- `reports/v05g/v05g_bf16_lora_4090_final_report.md`
- `reports/v05g/v05g_bf16_lora_4090_gold_v2_result.md`
- `reports/v05g/v05g_bf16_lora_4090_claims_and_limitations.md`
- `reports/v10/v10_mac_handoff_preflight.md`

Allowed actions:

- Create `README.md`.
- Create or update concise v1.0 narrative docs under `docs/v10/`.
- Summarize existing metrics from committed reports.
- Explain the v0.3 to v0.4/v0.5 interface evolution clearly.
- Add quickstart commands only if they use existing scripts and lightweight local checks.

Forbidden actions:

- Do not create demo code.
- Do not create downstream-lite benchmark code.
- Do not run training or model inference.
- Do not modify data, gold, predictions, or metrics.
- Do not claim downstream utility or production readiness.
- Do not hide READ as the main bottleneck.

Output files:

- `README.md`
- Optional: `docs/v10/PROJECT_RESULTS_NARRATIVE.md`

Completion criteria:

- README has scope, task formulation, result table, limitations, artifact map, and reproducibility notes.
- README names the best result accurately: BF16 standard LoRA r16 1000-targeted, RTX 4090 fallback.
- README states that READ remains the bottleneck and downstream utility is not yet proven.
- `git status --short` shows only expected packaging docs.

Stop point:

- Stop after README/narrative creation and report files changed, commands run, validation, problems, and next context.

## Context 6.2: Architecture + Task Formulation + Related Work

Objective:

Create durable technical documentation explaining the router architecture, task formulation, schema evolution, and concise related-work positioning.

Input files:

- `docs/planning/lightweight_memory_policy_router_project_spec.md`
- `docs/v04_planning/V04_TO_V10_STEERING_PLAN.md`
- Existing v0.4 spec/guideline docs if present.
- `README.md`
- `reports/v10/v10_mac_handoff_preflight.md`

Allowed actions:

- Create architecture and task-formulation docs under `docs/v10/`.
- Create related-work notes if they remain short and scoped.
- Include diagrams in Markdown or Mermaid.
- Clarify that fixed candidate memories are assumed; retrieval is out of scope.

Forbidden actions:

- Do not redesign the router schema.
- Do not add targets.
- Do not implement retrievers, memory DBs, writers, update/delete/merge, or MemoryOS features.
- Do not make claims that depend on downstream experiments.

Output files:

- `docs/v10/ARCHITECTURE_AND_TASK_FORMULATION.md`
- Optional: `docs/v10/RELATED_WORK_NOTES.md`

Completion criteria:

- Docs explain inputs, outputs, five STORE targets, parser/evaluator role, and out-of-scope boundaries.
- Docs reconcile the historical v0.3 span schema with the v0.4/v0.5 unit-based artifacts.
- Docs are consistent with README and claims/limitations.

Stop point:

- Stop after docs are created and report status.

## Context 6.3: Demo CLI / Readable Fixtures

Objective:

Create a lightweight, readable demo that shows router input/output shape without model inference.

Input files:

- `README.md`
- `docs/v10/ARCHITECTURE_AND_TASK_FORMULATION.md`
- Existing parser/validator/demo-adjacent source files.
- Small committed examples or safe sample records.

Allowed actions:

- Create small demo fixtures.
- Create a demo CLI that renders fixed examples and optionally validates/parses deterministic sample output.
- Add tests for demo parsing if using existing local test patterns.
- Document demo usage.

Forbidden actions:

- Do not run model inference.
- Do not download models.
- Do not fake new metrics.
- Do not build UI.
- Do not create a full downstream agent.
- Do not change gold or training data.

Output files:

- `demo/` files, exact names to be chosen from repo conventions.
- Optional: `docs/v10/DEMO_GUIDE.md`
- Optional tests if demo logic is nontrivial.

Completion criteria:

- Demo runs locally without API keys, model weights, or network access.
- Demo output is clearly labeled as fixture/demo output, not an evaluation result.
- Tests or smoke command pass.

Stop point:

- Stop after demo and docs are verified.

## Context 6.4: Downstream-Lite Efficiency Proxy Benchmark

Objective:

Create a small offline proxy benchmark that estimates routing efficiency and pollution behavior without real API calls or full downstream agent evaluation.

Input files:

- `README.md`
- `docs/v10/ARCHITECTURE_AND_TASK_FORMULATION.md`
- Existing prediction JSONL files in `data/v05g/model_predictions/`
- Existing metrics JSON/summary files in `reports/v05g/server_runs/`
- Existing evaluator utilities, if suitable.

Allowed actions:

- Build a lightweight offline analysis script over existing predictions and labels.
- Measure proxy quantities such as injected-memory count, irrelevant reads, missed reads, false stores, and estimated token savings if computable from existing records.
- Create a report under `reports/v10/`.
- Add focused tests if the script has parsing or aggregation logic.

Forbidden actions:

- Do not call DeepSeek or any real API.
- Do not run model inference.
- Do not train.
- Do not create a full downstream-lite agent or scenario benchmark unless explicitly requested.
- Do not modify existing metrics.
- Do not claim true downstream utility from proxy results.

Output files:

- Optional script under an appropriate existing source or analysis directory.
- `reports/v10/v10_downstream_lite_efficiency_proxy.md`

Completion criteria:

- Proxy benchmark is reproducible from committed predictions and gold.
- Report clearly distinguishes proxy analysis from downstream agent validation.
- Any changed data-like output is small, committed only if useful, and documented.

Stop point:

- Stop after proxy report and verification commands.

## Context 6.5: Resume Bullets + Interview Notes

Objective:

Create concise portfolio, resume, and interview materials that accurately reflect measured results and limitations.

Input files:

- `README.md`
- `reports/v05g/v05g_bf16_lora_4090_claims_and_limitations.md`
- `reports/v10/v10_mac_handoff_preflight.md`
- `reports/v10/v10_downstream_lite_efficiency_proxy.md`, if created.

Allowed actions:

- Create resume bullets.
- Create interview notes.
- Create a concise project story covering problem, approach, metrics, failure modes, and next work.

Forbidden actions:

- Do not exaggerate production readiness.
- Do not claim real downstream utility unless a later measured result supports it.
- Do not describe the project as MemoryOS.
- Do not omit READ bottleneck or synthetic-data limitations.

Output files:

- `docs/v10/RESUME_BULLETS_AND_INTERVIEW_NOTES.md`

Completion criteria:

- Materials include short, medium, and detailed versions.
- Claims match the allowed-claims document.
- Limitations are interview-ready and not buried.

Stop point:

- Stop after interview notes are created.

## Context 6.6: Final Audit + v1.0 Tag

Objective:

Audit the final v1.0 package, verify no forbidden artifacts are staged, then create the v1.0 tag only if explicitly requested or approved.

Input files:

- `README.md`
- `docs/v10/`
- `reports/v10/`
- `.gitignore`
- `git status --short`
- Relevant test and validation commands from prior contexts.

Allowed actions:

- Run final local tests and validators that do not require external services.
- Verify ignored paths and absence of large/generated/model artifacts.
- Create final audit report.
- Stage, commit, and tag only if the user explicitly requests those git operations.

Forbidden actions:

- Do not train, infer, or call APIs.
- Do not modify data/gold/metrics/predictions.
- Do not copy adapters into git.
- Do not create a tag without explicit user approval.
- Do not proceed beyond final audit without reporting.

Output files:

- `reports/v10/v10_final_audit.md`
- Optional git commit/tag only after explicit approval.

Completion criteria:

- Final audit lists files changed, commands run, validation results, ignored artifact checks, and remaining limitations.
- README and docs are internally consistent.
- `git status --short` contains only intended packaging files before any requested commit.

Stop point:

- Stop after final audit, or after approved commit/tag operations are complete.

