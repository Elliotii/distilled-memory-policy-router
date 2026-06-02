# V0.5b Git Handoff Checklist

**Date:** 2026-06-02  
**Status:** Read-only — Do NOT run git commands  

---

## 1. Recommended to Commit

### Reports
```bash
reports/v05b/*.md          # All 34 reports
```

### Docs
```bash
docs/v05b/*.md             # V05B_FINAL_RESULTS, V05B_PROJECT_NARRATIVE, V05C_SAFETY_ABLATION_PLAN
docs/status/CURRENT_STATE.md
```

### Configs
```bash
configs/v05b/*.yaml        # 3 JSON LoRA configs
```

### JSON SFT Data
```bash
data/v05b/json_sft/*.jsonl # 4 SFT files (125, 250, 500, dev)
```

### Predictions (small files)
```bash
data/v05b/model_predictions/*.jsonl  # 400 rows, ~180KB total
```

### Scripts
```bash
src/v05/render_json_sft_messages.py   # New
src/v05/train_lora_router.py           # Modified
src/v05/eval_lora_router.py            # Modified
```

## 2. Do NOT Commit

```bash
results/v05b_lora/          # ~75MB training outputs
checkpoints/                # Training checkpoints
models/                     # Downloaded models
outputs/                    # Generated outputs
wandb/                      # Logging
.venv/                      # Virtual environment
__pycache__/                # Python cache
.DS_Store                   # OS files
.env                        # API keys
*.log *.pyc                 # Generated files
```

## 3. Read-Only Verification Commands

```bash
# Check current state
git status --short

# See what files changed in tracked files
git diff --stat

# Check for large files
find . -type f -size +10M ! -path './.venv/*' ! -path './.git/*' ! -path './hf_models/*' | sort

# Check v0.5b reports count
ls reports/v05b/*.md | wc -l
```

## 4. Manual Commit Steps (User Runs)

```bash
# Stage new/modified files
git add reports/v05b/
git add docs/v05b/
git add docs/status/CURRENT_STATE.md
git add configs/v05b/
git add data/v05b/json_sft/
git add data/v05b/model_predictions/
git add src/v05/render_json_sft_messages.py
git add src/v05/train_lora_router.py
git add src/v05/eval_lora_router.py

# Review staged changes
git diff --cached --stat

# Commit
git commit -m "v0.5b: Unit JSON LoRA ablation complete

- JSON > DSL confirmed: +19.8pp target accuracy on locked gold
- JSON beats Qwen3-4B JSON few-shot on exact, STORE F1, target accuracy
- 100% valid JSON across 400 predictions
- Safety unsolved: 6 sensitive failures (tied with DSL)
- Qwen3.5 JSON few-shot remains strongest system
- Unit JSON is now preferred training interface
- v0.5c safety-focused ablation planned"

# Tag
git tag -a v0.5b-unit-json-lora-complete -m "v0.5b Unit JSON LoRA ablation: JSON > DSL confirmed, safety remains bottleneck"

# Push (if desired)
git push origin main --tags
```

## 5. Pre-Commit Sanity

| Check | Status |
|-------|:------:|
| Gold hash unchanged | ✅ |
| No secrets in staged files | ✅ |
| No large files (>10MB) staged | ✅ |
| All reports consistent | ✅ |
| 77/77 tests pass | ✅ |

---

*End of V0.5b Git Handoff Checklist.*
