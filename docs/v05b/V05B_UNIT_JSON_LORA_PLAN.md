# V0.5b — Unit JSON LoRA Ablation

Follow-up to v0.5. Tests whether Unit JSON SFT training improves target classification and safety compared with Unit DSL SFT training.

**Status:** Planning / Readiness complete (Context 5.7-A). Training not yet started.

## Quick Reference

| Item | Path |
|------|------|
| Plan | `reports/v05b/v05b_unit_json_lora_plan.md` |
| JSON SFT 125 | `data/v05b/json_sft/v05b_train_125_json_sft_messages.jsonl` |
| JSON SFT 250 | `data/v05b/json_sft/v05b_train_250_json_sft_messages.jsonl` |
| JSON SFT 500 | `data/v05b/json_sft/v05b_train_500_json_sft_messages.jsonl` |
| JSON SFT dev | `data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl` |
| Config 125 | `configs/v05b/qwen3_4b_lora_json_125.yaml` |
| Config 250 | `configs/v05b/qwen3_4b_lora_json_250.yaml` |
| Config 500 | `configs/v05b/qwen3_4b_lora_json_500.yaml` |
| Render script | `src/v05/render_json_sft_messages.py` |
| Usage policy | `reports/v05b/v05b_train_dev_gold_usage_policy.md` |
| Readiness | `reports/v05b/v05b_unit_json_lora_readiness_report.md` |

## Key Constraint

Same train subset IDs, dev, and gold as v0.5. Only the assistant output format changes (DSL → JSON).

---

*See reports/v05b/ for detailed documentation.*
