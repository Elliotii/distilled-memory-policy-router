# v1.0-applied 中文面试讲稿

## 30 秒版本

我做的是一个 memory policy router，不是完整 agent，也不是 RAG。它接收当前任务、若干候选记忆，决定哪些 memory 应该 READ 进上下文，哪些当前信息应该 STORE 或 SKIP。v1.0-applied 的核心结果是：learned_router 在 32 个 hard READ case 上 selection-level recall 很强，required recall 是 0.890625，明显高于 keyword_top_k 的 0.453125、random_k 的 0.4375 和 candidate-order baseline 的 0.0625。但 downstream 8-case 手工评审里没有稳定转化成答案质量优势，learned_router utility 是 7.125，低于 no_memory 8.000 和 all_candidates 8.750。所以我的结论不是“READ 已解决”，而是定位出了下一步要解决的 failure mechanism：missed required memories 和 contradictory contamination。

## 1 分钟版本

这个项目研究的是 agent memory pipeline 里的一个很窄但关键的控制层：memory routing。给定固定候选 memories 和当前任务，它决定哪些 memory 应该注入上下文，哪些当前 units 应该写入长期记忆或跳过。它不做 retrieval、不改写 memory，也不是 MemoryOS。

我训练并评估了一个小模型 learned_router，并把它接进一个 applied harness。高置信度结果在 selection level：32 个 hard READ case 上，learned_router required recall 是 0.890625；作为对比，keyword_top_k 是 0.453125，random_k 是 0.4375，budgeted_candidate_order 是 0.0625。

但 downstream 结果是有限甚至偏负面的：8-case 手工 rubric review 中，learned_router manual utility 是 7.125，低于 no_memory 8.000 和 all_candidates 8.750，oracle_selected 是 12.000。去掉一个 empty response 后 learned_router 到 7.286，仍低于 no_memory。我的解释是：selection 好不等于 downstream 答案好，因为 downstream slice 上 required recall 只有 0.6875，并且有 missed required memories 与 contradictory contamination。

## 3 分钟版本

这个项目的背景是：长期运行的 coding/business agent 会需要记忆，但记忆系统如果不加控制，会把无关、过期、矛盾或敏感信息注入上下文，或者把临时噪声写成长期记忆。我的项目只研究其中一个 control-plane component：memory policy router。

输入是当前任务、当前分解后的 units、以及最多一组候选 memories。输出是 READ / STORE / SKIP 决策。这里 READ 是选择哪些候选 memory 进上下文；STORE/SKIP 是决定当前信息是否值得长期保存。它不是普通 retrieval，因为 retrieval 是从大库里找候选，而这里是在候选已经给定后做 policy selection 和污染控制。

模型方面，我训练的是 Qwen-family 约 4B 规模的 LoRA router。v0.5g 的重点是 BF16 LoRA 的 Unit JSON 输出格式。写侧指标很好，但 READ 仍然是瓶颈，所以 v1.0-applied 专门做 hard READ fixture 和 applied harness。

结果分两层看。第一层是 high-confidence selection-level：在 32 个 hard READ case 上，learned_router required recall 0.890625，明显高于 keyword_top_k 0.453125、random_k 0.4375、budgeted_candidate_order 0.0625。这说明 learned router 确实学到了一些 hard READ selection 能力。

第二层是 downstream diagnostic：把 learned_router 接入 8-case downstream subset，让固定的 DeepSeek-compatible answerer 根据注入 memory 回答。人工 rubric 结果并不好：learned_router utility 7.125，低于 no_memory 8.000、all_candidates 8.750，oracle_selected 12.000。这个不是 downstream win。进一步分析发现，8-case slice 本身更难：selection required recall 只有 0.6875，avoid injected 8，contradictory injected 5，stale injected 1。失败机制不是单一的“噪声太多”，而是 missed required memories 加 contradictory contamination。强 answerer 可能能忍受一些非矛盾噪声，但 missing required facts 或注入 contradiction 会直接伤害答案。

所以我会把这个项目包装成一个诚实的 research-engineering result：我完成了从训练、离线预测、harness replay、downstream API response、automatic scoring 到 manual rubric review 的闭环；同时明确说明 selection advantage 没有稳定转化为 downstream utility。

## 技术深挖版本

系统分四层：

1. 数据与任务格式：current units、candidate memories、runtime context，输出 READ / STORE / SKIP。
2. 模型层：v0.5g learned_router，Unit JSON 输出，离线 LoRA prediction，不在线 serving。
3. Selection harness：把 saved prediction JSONL replay 成 `replay_learned_router` strategy，和 no_memory、all_candidates、keyword_top_k、random_k、oracle_selected 等 baseline 对比。
4. Downstream harness：用同一批 8 个 hard READ case 构造 prompt，让固定 answerer 生成答案，再做 automatic citation scoring 和 manual rubric review。

最关键的 design choice 是把 learned_router prediction 和 downstream answer generation 分离。这样可以避免把模型加载、API 调用、retrieval、answerer 行为混在一起。AutoDL 上只做离线 prediction，Mac harness 只 replay saved JSONL，downstream 只测固定 answerer 在不同 memory injection strategy 下的表现。

最终发现 selection 和 downstream 有 gap。32-case selection aggregate 很强，但 8-case downstream slice 的 selection recall 降到 0.6875，并且 contradictory injected 是 5。这解释了为什么 all_candidates 虽然注入很多 avoid memory，却可能因为没有 missed required facts 而在人工 utility 上高于 learned_router。

## Q&A

### 这个项目解决什么问题？

解决 agent memory pipeline 中“该读哪些 memory、该写哪些信息、该跳过哪些噪声”的 policy 问题。目标是减少上下文污染和长期记忆污染，但不是做完整 agent 或生产级 memory system。

### 为什么 memory routing 不是普通 retrieval？

Retrieval 是从大规模 memory store 里找候选。Memory routing 是候选已经给定后，判断哪些候选在当前任务中应该用、哪些会造成 stale/contradictory/wrong-scope contamination。它更像一个 policy controller，而不是向量检索器。

### 你训练了什么模型？

训练的是 Qwen-family 约 4B 规模的小型 router，使用 LoRA/BF16 LoRA，输出 Unit JSON 的 READ / STORE / SKIP 决策。v1.0-applied 里使用的是已保存的 v0.5g offline predictions，不在线加载 Qwen 或 LoRA。

### harness 怎么设计？

harness 分 selection 和 downstream 两层。Selection harness 对比不同 memory selection strategies 的 required recall 和 contamination。Downstream harness 固定 answerer，只改变注入的 memory context，再看 response quality 和 citation behavior。

### 最重要的实验结果是什么？

最重要的是双层结果：selection-level 成功，downstream transfer 有限。32-case selection learned_router required recall 是 0.890625，显著高于 keyword/random/order baselines。但 8-case downstream manual utility 是 7.125，低于 no_memory 8.000 和 all_candidates 8.750。

### 为什么 downstream 没赢 no_memory？

因为 learned_router 在 downstream slice 上漏掉了 required memories，并且注入了 contradictory memories。no_memory 虽然答得泛、缺少 memory-only facts，但不会被错误 memory 带偏。learned_router 的一部分回答被 contradiction 直接伤害，另有一个 empty response。

### 这个结果是不是失败？

不是工程失败，但也不是 downstream win。它是一个有价值的 negative/limited transfer result：证明了 selection-level 学到了东西，也证明了只优化 READ recall 不够，必须处理 contradiction-aware selection 和 missed required facts。

### 下一步怎么改？

v1.1 应该做 contradiction-aware READ：retrieve -> relevance -> contradiction check -> budget select。具体包括 hard-negative READ training、pairwise memory consistency check、abstention/confidence threshold、contradiction-aware reranker，以及扩大 downstream-aware eval。不要先做 UI，也不要在 contradiction labels 没定义前盲目重训。
