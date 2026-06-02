# V0.5 Resume / Interview Narrative

**Date:** 2026-06-02  

---

## 2-Sentence Resume Bullet

Built a memory-policy router distillation pipeline with locked gold evaluation: compared Qwen3/Qwen3.5 model baselines, trained a QLoRA learning curve (125→250→500 cases), improved action-level routing but identified target-classification and sensitive-content safety bottlenecks. Qwen3.5 JSON few-shot emerged as the strongest system; QLoRA training on small data proved insufficient for fine-grained target routing and safety.

## 30-Second Explanation

"For my v0.5 project, I built an evaluation pipeline for a memory policy router — a component that decides which memories to read and which new information to store in a coding assistant's context. I created 700 labeled cases with locked gold evaluation, compared multiple model baselines including Qwen3-4B and the newer Qwen3.5, and trained a QLoRA adapter on 125, 250, and 500 cases. The LoRA improved action-level routing — deciding WHAT to store — but failed on target classification and had safety issues with storing contact info as user preferences. The biggest finding was that Qwen3.5 few-shot prompting actually outperformed fine-tuned Qwen3-4B, suggesting that for small-data tasks, prompting a larger model can beat training a smaller one."

## 2-Minute Interview Explanation

"The project goal was to build a memory policy router for coding-agent contexts. Given a set of candidate memories and current user input, the router predicts which memories to read and which pieces of new information to store or skip. The output is a structured DSL with specific storage targets like service_memory, task_state, repo_memory, project_memory, or user_profile.

I built the entire pipeline from scratch: 700 labeled cases with train/dev/locked-gold splits, leakage protection, deterministic baselines, and multi-model comparison. I compared Qwen3-4B against Qwen3.5 across Unit DSL and Unit JSON interfaces under zero-shot and few-shot conditions.

The most surprising result was that Qwen3.5 JSON few-shot achieved 42% exact match on locked gold with zero safety failures — beating everything else including my QLoRA-trained model. The QLoRA learning curve showed that supervised training improves STORE/SKIP decisions, but target classification (especially service_memory vs task_state) remains the bottleneck at 25% accuracy on gold.

The safety issue was concerning: the trained model stored sensitive information like credit cards and personal emails as user_profile preferences. This revealed that small-data training without explicit safety weighting can actually make models less safe than prompting alone.

Key lessons: (1) Locked gold evaluation is essential — dev metrics were overly optimistic. (2) Prompting a larger model can beat training a smaller one when data is limited. (3) Target classification is harder than action routing. (4) Safety must be explicitly baked into training, not expected to emerge from general data."

## What Went Wrong

1. Target accuracy plateaued at 54% — more generic data didn't help. The model defaults to task_state.
2. Sensitive content stored as user_profile — 6 genuine failures including credit card on gold.
3. Qwen3.5 prompting was stronger than expected — 42% vs LoRA's 16% on gold.
4. 500 cases of QLoRA rank-8 was insufficient for fine-grained target distinction.

## Why Negative Result Is Valuable

The experiment successfully characterized the problem: action routing is learnable with small data, but target classification and safety require different approaches. This is valuable diagnostic information that informs the next iteration (v0.5b).

## How To Improve Next

1. Target-balanced training data (oversample rare targets)
2. Safety-weighted loss (penalize sensitive storage heavily)
3. Larger LoRA rank (r=16 or r=32)
4. Unit JSON training (best-performing prompting format)
5. More epochs (5-10 instead of 3)
6. Two-stage architecture: action classifier → target classifier

---

*End of V0.5 Resume / Interview Narrative.*
