# v1.0-Eval Checkpoint Manifest

## Checkpoint Identity

| Field | Value |
| --- | --- |
| Name | `v1.0-eval checkpoint` |
| Branch | `codex/v10-packaging` |
| Purpose | Freeze the current evaluation, benchmark, documentation, and portfolio stage before starting Applied Memory Harness work. |
| Status | Evaluation checkpoint only. This is not final v1.0. |

This manifest records the current v1.0-facing evaluation state. It does not start Applied Memory Harness implementation, does not create a git tag, and does not change locked gold, saved predictions, v05 reports, configs, source, adapters, results, logs, or demo artifacts.

## Included In This Checkpoint

- v0.5g LoRA router training and evaluation synthesis.
- Locked `gold_v2_009` intrinsic router results.
- No-inference replay demo.
- Downstream-lite proxy benchmark.
- LLM downstream-lite prompt pack.
- DeepSeek 14-response micro-pilot.
- Citation scoring and rubric-based internal qualitative review.
- v10 benchmark synthesis.
- Chinese portfolio and interview HTML draft.

## Best Current Router Result

Best current evaluated router:

- System: BF16 LoRA r16 + 1000 targeted-balanced data.
- Setting: RTX 4090 fallback settings.
- Evaluation: locked `gold_v2_009`.

| Metric | Value |
| --- | ---: |
| Exact match | 36.0% |
| Parse success | 99.3% |
| READ F1 | 84.6% |
| STORE F1 | 99.0% |
| SKIP F1 | 98.1% |
| STORE target accuracy | 100.0% |
| False store rate | 1.2% |
| Sensitive store | 0/4 on locked gold under semantic metric |

## Honest Interpretation

- Write-side routing is the strongest learned result. STORE, SKIP, and STORE target classification are the clearest wins in the current controlled benchmark.
- READ remains unresolved. The best gold run still has READ errors, and READ is the dominant reason full exact match remains at 36.0%.
- The downstream-lite proxy and 14-response micro-pilot do not establish router-specific downstream superiority over baseline memory-injection strategies.
- The current benchmark does not fully test hard READ selection. Candidate ordering and entity-matching patterns remain important confounds.
- This stage is an evaluation checkpoint, not an applied memory-agent system.

## Why Final v1.0 Continues

Final v1.0-applied should add an Applied Memory Harness layer before claiming an applied system shape. Planned additions:

- Applied Memory Harness.
- Hard-candidate READ evaluation.
- Audit trace.
- Baseline comparison.
- Optional live LoRA.
- Optional Streamlit trace viewer.

These are future applied-harness tasks and are not included in this checkpoint.

## Do-Not-Claim List

Do not claim:

- Downstream utility proof.
- Production safety.
- Real retriever performance.
- Real cost savings.
- Complete MemoryOS.
- That the router beats all baselines.
- That READ is solved.

## Next Phase Pointer

Next context should be:

```text
Context 7.1 — Thesis reframe and Applied Memory Harness design docs.
```

## Source References

- `README.md`
- `docs/PROJECT_OVERVIEW.md`
- `docs/RESULTS.md`
- `docs/ARCHITECTURE.md`
- `docs/TASK_FORMULATION.md`
- `docs/DOWNSTREAM_LITE_BENCHMARK.md`
- `docs/LLM_DOWNSTREAM_LITE_BENCHMARK.md`
- `reports/v10/v10_benchmark_synthesis.md`
- `reports/v10/llm_downstream_lite_micro_pilot_diagnostic.md`
- `reports/v10/llm_downstream_lite_micro_pilot_manual_review_report.md`
- `reports/v05g/v05g_bf16_lora_4090_final_report.md`
- `reports/v05g/v05g_bf16_lora_4090_claims_and_limitations.md`
- `docs/portfolio_zh/index.html`
- `docs/portfolio_zh/resume_bullets.html`
- `docs/portfolio_zh/interview_notes.html`
- `docs/portfolio_zh/v1_1_roadmap.html`
