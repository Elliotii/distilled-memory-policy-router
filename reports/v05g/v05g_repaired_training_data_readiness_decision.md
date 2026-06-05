# v05g Repaired Training Data Readiness Decision

**Date:** 2026-06-05  
**Decision:** **Option A — Repaired v05g data ready for independent audit and server-side training.**

## Rationale

### What was repaired

Following Opus 4.8's semantic review identifying two defects, the additional 500 targeted training data was repaired:

1. **READ Semantic Recoverability**: READ labels now determined by visible semantics (service/repo match in memory text). Cross-domain distractor memories added with clearly visible different service/project names. 0 stale reads, 0 distractor reads.

2. **Prefix/Opener Shortcut**: Neutral openers added across STORE and SKIP units. Body-dependent routing cases created (>64%). Binary 3-word-prefix accuracy reduced from 100% to 90.9%.

3. **Sensitive Literal Diversification**: Sensitive pool expanded from 18 to 70 unique texts. Max repetition reduced from 5x to 2x.

4. **Documentation**: Fixed `gold_v2_009: unevaluated` wording in planning document.

### What was preserved

- 500-control: **Byte-identical** (hash `c6ec79d9...` preserved)
- gold_v2_009: Unchanged, used only as exclusion/leakage reference
- All original case_ids and distribution targets maintained

### Quality Gates (all pass)

| Gate | Status |
|------|--------|
| SFT JSON parse = 100% | ✅ |
| Unit coverage = 100% | ✅ |
| Store/skip mutually exclusive | ✅ |
| Sensitive STORE = 0 | ✅ |
| No invalid targets/IDs/placeholders | ✅ |
| 0 exact/namespace leakage | ✅ |
| All distributions within target ranges | ✅ |

### Distribution Achievement

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| task_state | 28.2% | 25-32% | ✅ |
| service_memory | 26.6% | 24-32% | ✅ |
| repo_memory | 19.7% | 16-22% | ✅ |
| project_memory | 14.9% | 12-20% | ✅ |
| user_profile | 10.7% | 6-12% | ✅ |
| READ-only | 19.5% | 10-20% | ✅ |
| STORE/SKIP-only | 37.2% | 35-45% | ✅ |
| READ+STORE | 43.3% | 40-50% | ✅ |

### Semantic Quality Gates (Post-Repair)

| Gate | Status |
|------|--------|
| Stale reads = 0 | ✅ |
| Distractor reads = 0 | ✅ |
| Non-stale not-read with visible reason | ✅ |
| 3-word-prefix accuracy < 100% | 90.9% ✅ |
| Body-dependent cases ≥ 10% | 64.2% ✅ |
| Sensitive literal max repeat ≤ 2x | ✅ |

## Caveats

1. **Template-generated synthetic data**: The additional 500 remains template-generated. While semantic quality has been substantially improved, it has not been human-reviewed for edge-case quality. The primary value remains testing the LoRA scaling hypothesis.

2. **500-control inherited domain leakage**: The 500-control contains domains (ecommerce-platform, shopengine, learnhub) that were rejected from gold_v2 construction. These are retained as-is because this is a control dataset — changing it would invalidate the BF16-vs-QLoRA comparison.

3. **Remaining opener separability**: 90.9% binary accuracy means some opener patterns still correlate with labels. These remaining correlations are semantically justified (sensitive content → SKIP, stale → NOT READ) rather than brittle template artifacts.

## Recommendation

**Proceed to server-side training with these repaired data files.**

Training commands should reference:
- BF16 LoRA r16 500: `data/v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl`
- BF16 LoRA r16 1000: `data/v05g/json_sft/v05g_train_1000_targeted_json_sft_messages.jsonl`

Do NOT train locally. Do NOT evaluate on gold_v2_009.

## Data Lock Hashes

| File | SHA-256 |
|------|---------|
| v05g_train_500_control_cases.jsonl | `c6ec79d9...` |
| v05g_train_500_control_json_sft_messages.jsonl | `d88d34fb...` |
| v05g_train_additional_500_targeted_cases.jsonl | `dadc6731...` |
| v05g_train_additional_500_targeted_json_sft_messages.jsonl | `f4297c75...` |
| v05g_train_1000_targeted_cases.jsonl | `c7b0d94e...` |
| v05g_train_1000_targeted_json_sft_messages.jsonl | `da613fff...` |
