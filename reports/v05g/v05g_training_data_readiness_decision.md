# v05g Training Data Readiness Decision

**Date:** 2026-06-05  
**Decision:** **Option A — v05g 500-control and 1000-targeted data are ready for independent audit and server-side training.**

## Rationale

### What was built
1. **500-control**: Exact copy of the existing v05b train 500 JSON SFT dataset, used by the Qwen3.5 QLoRA r16 experiment. This ensures the BF16 r16 500 variant trains on identical data to the existing QLoRA r16 baseline.

2. **Additional 500 targeted-balanced**: 500 synthetic cases across 8 new business domains, designed to shift the combined 1000 distribution toward healthier target coverage.

3. **Combined 1000**: True superset of 500-control, concatenated with additional 500. Not two unrelated datasets.

### Quality Gates (all pass)
- SFT JSON parse: 100% (1000/1000)
- Unit coverage: 100%
- Store/skip mutually exclusive: 100%
- Sensitive STORE: 0
- No invalid targets, duplicate assignments, or placeholder residues

### Distribution Achievement
All 5 target distributions and all 3 shape distributions fall within recommended ranges:
- task_state: 28.2% (25-32%)
- service_memory: 26.6% (24-32%)
- repo_memory: 19.6% (16-22%)
- project_memory: 14.9% (12-20%)
- user_profile: 10.7% (6-12%)

### Leakage (0 across all checks)
- 0 namespace overlap with dev, old gold, gold_v2_009
- 0 exact text overlap
- 0 SENSITIVE_POOL/STALE_POOL overlap (fixed from initial build)

### Gold Protection
- gold_v2_009: unchanged
- Old gold: unchanged
- Dev: unchanged
- No new gold set created

## Caveats

1. **Template-generated data**: The additional 500 is synthetic, template-generated data. While structurally clean and distributionally balanced, it has not been human-reviewed for semantic quality. The primary value is in testing the LO RA scaling hypothesis (does more data help?), not in producing a production-quality dataset.

2. **500-control inherited issues**: The 500-control contains some domain names that were rejected from gold_v2 construction. These are retained as-is because this is a control dataset — changing it would invalidate the comparison.

3. **No semantic quality review**: Data validation is structural only (parse, coverage, leakage). Semantic quality (is the target assignment correct?) is assumed from the template logic but not independently verified.

4. **BF16 training server required**: These datasets are prepared for server-side training. Local GPU (RTX 4070 12GB) cannot handle BF16 4B LoRA.

## Recommendation

**Proceed to server-side training with these exact data files.**

Training commands should reference:
- BF16 LoRA r16 500: `data/v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl`
- BF16 LoRA r16 1000: `data/v05g/json_sft/v05g_train_1000_targeted_json_sft_messages.jsonl`

Do NOT train locally. Do NOT evaluate on gold_v2_009.
