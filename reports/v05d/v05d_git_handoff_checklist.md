# V0.5d Git Handoff Checklist

**Date:** 2026-06-04  

## Pre-Commit Verification

```bash
sha256sum data/v05/gold/v05_gold_corrected_cases.jsonl
# Expected: 56e16078...

ls reports/v05d/*.md | wc -l
# Expected: 13
```

## Files to Stage

```bash
git add configs/v05d/
git add reports/v05d/
git add docs/v05d/
git add data/v05d/model_predictions/
git add docs/status/CURRENT_STATE.md
```

## Files to EXCLUDE

```bash
# Training outputs
echo "results/v05d_lora/" >> .gitignore
```

## Commit

```bash
git commit -m "v0.5d: Qwen3.5 Unit JSON QLoRA r=16 dev-only ablation

- Capacity ablation: r=8 → r=16, alpha/r=2, 9.8M params
- Dev: +5pp exact (39% vs 34%), +0.057 SKIP F1, +0.009 STORE F1
- All metrics improve, no regression
- r=16 is best dev performer; needs gold_v2 for final claim
- 13 reports, 1 config, 1 prediction file"

git tag -a v0.5d-r16-dev-only-complete -m "v0.5d: r=16 QLoRA dev-only ablation complete"
```
