# v0.5g BF16 LoRA 4090 — Claims and Limitations

**Date:** 2026-06-08
**Purpose:** Separate allowed claims, forbidden claims, limitations, and resume-safe wording for v0.5g results

---

## Allowed Claims

### General
- ✅ BF16 standard LoRA r=16 1000-targeted is the best evaluated system on locked gold_v2_009 by exact match and write-side routing metrics among the compared systems. READ F1 was not available for older v0.5e anchors.
- ✅ 1000-targeted improves over 500-control on both dev and gold across all primary metrics.
- ✅ The largest gold gains are on write-side routing: STORE F1, SKIP F1, and target classification.
- ✅ Target accuracy on gold_v2_009 reaches 100.0% for the 1000-targeted variant.
- ✅ False store rate on gold drops from 10.4% (500) to 1.2% (1000).
- ✅ Sensitive store rate on locked gold_v2_009 is 0/4 for both variants under the semantic sensitive-store metric. Dev still shows 2/3 sensitive stores, so this is a promising signal, not a safety guarantee.
- ✅ BF16 standard LoRA training is feasible on RTX 4090 24GB with gradient checkpointing.
- ✅ The 1000-targeted training strategy (500-control + 500 domain-diverse targeted-balanced) is effective for write-side routing.

### Comparison
- ✅ 1000-targeted beats all v05e systems on exact, STORE F1, SKIP F1, and target accuracy.
- ✅ 1000-targeted beats Qwen3.5 JSON few-shot on exact (+5.3pp) and target accuracy (+24.7pp).
- ✅ 500-control with BF16 does NOT outperform old QLoRA r16 on gold — BF16 alone is not sufficient to improve results at small data scales.

### Data
- ✅ v0.5g training data locks are recorded in `data/v05g/v05g_training_data_lock.json`.
- ✅ gold_v2_009 was not modified during v0.5g training or evaluation.
- ✅ gold_v2_009 SHA-256 unchanged: `f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72`.

### Provenance
- ✅ Server version: `v0.5g-bf16-lora-4090-ready / 7e40f02bbb34c2c5ecf8f7468a066cba0105db4d`.
- ✅ Artifacts extracted from `v05g_bf16_lora_4090_final_artifacts.tar.gz` and verified.

---

## Forbidden Claims

Do NOT claim any of the following:

### Safety & Production
- ❌ "Production-safe memory router"
- ❌ "Ready for deployment"
- ❌ "Solves sensitive data handling" (dev set still shows 2/3 sensitive store)
- ❌ "Complete Memory OS component"
- ❌ "Downstream LLM utility proven"

### READ
- ❌ "READ selection is solved" (84.6% F1, 36.0% exact)
- ❌ "Full-exact memorization"
- ❌ "Read the right memories every time"

### Benchmarking
- ❌ Claims that this used the originally planned larger-GPU setting — this was an RTX 4090 fallback config.
- ❌ "Beats all baselines on all metrics" — Few-shot has better READ? Not compared for READ F1.
- ❌ "Statistically significant improvement" — No CI computed for 500 vs 1000.
- ❌ "Generalizes to real-world tasks"
- ❌ "Live retrieval performance"

### Causality
- ❌ "BF16 caused the improvement" — 500-control disproves this.
- ❌ "Data volume alone caused the improvement" — Domain diversity and target balance confound.
- ❌ "Pure data-size causality established"
- ❌ "r=16 optimal rank" — Not tested against r=8 or r=32.

---

## Limitations

### Methodological
1. **RTX 4090 fallback config** — Batch size 2, gradient checkpointing enabled. Not directly comparable to the originally planned larger-GPU configs.
2. **No paired CI** — 500 vs 1000 not evaluated with bootstrap CI (different data, not paired). Cannot claim statistical significance.
3. **Single gold evaluation** — No holdout set evaluated. gold_v2_009 holdout (30 cases) remains unused.
4. **Template-generated data** — Both training data (additional 500) and gold_v2_009 are synthetic templates. No human semantic review.
5. **Single random seed** — Training seed fixed at 42 (via data sampling). No seed robustness assessment.

### Data
6. **Training READ = entity matching** — READ labels in training data are based on domain name matching, not semantic relevance. Model learns a heuristic, not true context selection.
7. **Prefix shortcut** — Training data 3-word-prefix accuracy 90.9%. Model may rely on shallow patterns.
8. **1000-vs-500 confound** — Cannot separate data volume from domain/template diversity effects.

### Evaluation
9. **No retriever integration** — Router predictions not tested with actual memory retrieval.
10. **No downstream agent task** — Router output not fed into a coding agent to measure task completion.
11. **Sensitive store methodology** — v05g uses semantic detection (unit-level `sensitive_boundary` tag). v05e used eval_runner case-level tag detection. Not directly comparable across versions.

### Scope
12. **Single model family** — Qwen3.5-4B only. No other base models tested with this recipe.
13. **English only** — All data in English.
14. **Synthetic domain** — All cases are synthetic business-domain scenarios. No real-world code or conversation data.

---

## Resume-Safe Wording

For portfolio, resume, or public-facing summary:

> **Memory Policy Router v0.5g** — Built a LoRA-fine-tuned Qwen3.5-4B router that predicts READ / STORE / SKIP memory-policy decisions for coding-agent contexts. Achieved 100% target accuracy and 99% store-side F1 on locked gold_v2_009 using a targeted-balanced training strategy. Identified READ (memory selection) as the primary remaining bottleneck, with F1 of 84.6%. Under the semantic sensitive-store metric, 0/4 sensitive units were stored on locked gold_v2_009, while dev still shows 2/3 sensitive stores, so this is a promising signal rather than a safety guarantee.

---

*End of v0.5g BF16 LoRA 4090 Claims and Limitations.*
