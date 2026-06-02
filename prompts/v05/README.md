# v0.5 Prompt Templates

Version: v0.5
Date: 2026-06-02
Context: 5.4-B

## Files

| File | Format | Mode | Few-Shot Source |
|------|--------|------|-----------------|
| `unit_dsl_zero_shot.txt` | Unit DSL | Zero-shot | None |
| `unit_dsl_fewshot.txt` | Unit DSL | Few-shot (5 examples) | Train-pool (v05_sample_0001, 0005, 0009, 0010, 0004) |
| `unit_json_zero_shot.txt` | Unit JSON | Zero-shot | None |
| `unit_json_fewshot.txt` | Unit JSON | Few-shot (5 examples) | Train-pool (same 5 cases) |

## Few-Shot Example Cases

All from `data/v05/batches/v05_batch500_corrected_cases.jsonl`:
- v05_sample_0001: READ-only + stale memory
- v05_sample_0005: STORE/SKIP-only + sensitive + repo_vs_service
- v05_sample_0009: READ+STORE joint
- v05_sample_0010: Sensitive boundary + stale
- v05_sample_0004: Service vs task boundary

No dev or gold cases used.

## Known Issues (from 5.4-B smoke)

- Qwen3-4B zero-shot: outputs empty defaults (READ NONE / STORE NONE / SKIP NONE)
- Qwen3-4B few-shot: template-matches wrong unit IDs from examples
- Qwen3.5 all modes: outputs verbose thinking prose, not DSL/JSON
- Prompt format uses single user message; may need system+user role separation

## Next Steps

Fix prompt format before full dev baseline run. See V05_QWEN_BASELINE_RUN_PLAN.md for details.
