# V0.5c Git Handoff Checklist

**Date:** 2026-06-04  

---

## Pre-Commit Verification

```bash
# 1. Verify gold hash unchanged
sha256sum data/v05/gold/v05_gold_corrected_cases.jsonl
# Expected: 56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d

# 2. Verify all reports present
ls reports/v05c/*.md | wc -l
# Expected: 42

# 3. Run unit tests
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests
# Expected: 77/77 OK

# 4. Compile check modified scripts
PYTHONDONTWRITEBYTECODE=1 python -m py_compile src/v05/train_lora_router.py src/v05/eval_lora_router.py
# Expected: OK

# 5. Check no large files staged
find . -not -path './.venv/*' -not -path './results/*' -type f -size +50M
# Expected: none

# 6. Git status review
git status
```

## Files to Stage

```bash
# Configs
git add configs/v05c/

# Docs
git add docs/v05c/
git add docs/status/CURRENT_STATE.md

# Reports (42 files)
git add reports/v05c/

# Scripts (modified)
git add src/v05/train_lora_router.py
git add src/v05/eval_lora_router.py

# Predictions (small JSONL files)
git add data/v05c/model_predictions/
```

## Files to EXCLUDE

```bash
# Training outputs (large)
echo "results/v05c_lora/" >> .gitignore  # if not already

# Never commit
# .venv/, __pycache__/, .DS_Store, checkpoints/, models/, outputs/, wandb/, *.log, *.pyc, .env
```

## Commit Commands

```bash
# Review staged changes
git diff --cached --stat

# Commit
git commit -m "v0.5c: Qwen3.5 Unit JSON LoRA — best trained router (41% exact, 0.969 STORE F1)

- Base-model ablation: Qwen3.5 vs Qwen3-4B for JSON SFT
- 125/250/500 dev learning curve complete
- Locked-gold final eval: 41% exact, 100% parse, 0.969 STORE F1
- Beats Qwen3-4B JSON LoRA 500 by +10pp exact
- Qwen3.5 JSON few-shot remains #1 overall
- 42 reports, 4 prediction files, 3 configs, 2 script changes"

# Tag
git tag -a v0.5c-qwen35-json-lora-complete -m "v0.5c: Qwen3.5 Unit JSON LoRA complete"
```

## Post-Commit Verification

```bash
# Verify tag
git show v0.5c-qwen35-json-lora-complete --stat

# Verify gold hash still unchanged
sha256sum data/v05/gold/v05_gold_corrected_cases.jsonl
```

---

*End of Git Handoff Checklist.*
