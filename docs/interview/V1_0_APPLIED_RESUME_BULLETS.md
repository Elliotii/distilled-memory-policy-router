# v1.0-applied Resume And Portfolio Bullets

## English Resume Bullets

- Built a memory-policy routing benchmark and harness for coding/business-agent contexts, separating fixed-candidate READ selection from STORE/SKIP policy decisions and downstream answer evaluation.
- Trained and replay-evaluated a small Qwen-family LoRA router; on 32 hard READ cases, learned_router reached 0.890625 required-memory recall versus 0.453125 for keyword_top_k and 0.4375 for random_k.
- Ran an applied 8-case downstream diagnostic with automatic citation scoring and manual rubric review; documented a negative/limited transfer result where learned_router scored 7.125, below no_memory 8.000 and all_candidates 8.750, identifying missed required memories and contradictory contamination as key failure modes.

## 中文简历 Bullet

- 设计并实现 coding/business-agent memory policy routing benchmark 与 harness，把固定候选 memory 的 READ selection、STORE/SKIP policy 和 downstream answer evaluation 分层评估。
- 训练并 replay 评估 Qwen-family LoRA router；在 32 个 hard READ case 上，learned_router required-memory recall 达到 0.890625，高于 keyword_top_k 0.453125 和 random_k 0.4375。
- 完成 8-case applied downstream diagnostic，包括 automatic citation scoring 和 manual rubric review；如实记录 learned_router 7.125 低于 no_memory 8.000 / all_candidates 8.750，并定位 missed required memories 与 contradictory contamination 两类失败机制。

## LinkedIn / GitHub Project Summary

I built a research-engineering memory policy router for coding/business-agent contexts. The project focuses on a narrow but important control-plane problem: given fixed candidate memories and current task units, decide which memories should be read into context and which current units should be stored or skipped. I trained and evaluated a small Qwen-family LoRA router, built replay and downstream harnesses, and preserved metrics/reports for reproducibility.

The strongest result is selection-level: on 32 hard READ cases, learned_router achieved 0.890625 required-memory recall, substantially above keyword_top_k, random_k, and candidate-order baselines. The downstream result was intentionally reported conservatively: on an 8-case manual rubric review, learned_router scored 7.125, below no_memory and all_candidates. This made the project more useful as a diagnostic: it showed that selection recall alone is not enough, and that missed required memories plus contradictory contamination must be handled before broader downstream claims are justified.

## 中文项目总结

这个项目是一个面向 coding/business-agent 场景的 memory policy router。它不做完整 agent，也不做 RAG，而是专注在一个窄的控制层：给定当前任务和固定候选 memories，判断哪些 memory 应该 READ 进上下文，哪些当前信息应该 STORE 或 SKIP。

我训练并评估了 Qwen-family LoRA router，构建了 offline prediction replay、selection harness、downstream prompt/response harness、automatic citation scoring 和 manual rubric review。结果上，learned_router 在 32 个 hard READ case 上 selection-level required recall 达到 0.890625，明显高于 keyword/random/order baselines。但 downstream 8-case 手工评审中 learned_router utility 是 7.125，低于 no_memory 和 all_candidates。这个结果不是夸大成“下游胜利”，而是定位出下一步研究重点：missed required memories 和 contradictory contamination。
