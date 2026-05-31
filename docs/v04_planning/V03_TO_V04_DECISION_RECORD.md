# V03_TO_V04_DECISION_RECORD

> 决策记录：是否从 v0.3 JSON/span router pivot 到 v0.4 unit-based READ/STORE/SKIP DSL。  
> 结论：正式 pivot，但保留 v0.3 作为 prototype、baseline 和设计证据。

---

## 1. Decision

```text
Status: Accepted
Decision date: 2026-05-31
Decision owner: project author
Main decision: freeze v0.3 JSON/span router as prototype and pivot mainline to v0.4 unit-based READ/STORE/SKIP DSL.
```

本项目后续主线不再继续扩展 v0.3 JSON/span schema，也不优先训练 v0.3 LoRA。

后续路线：

```text
v0.3 = frozen prototype / baseline / motivation
v0.4 = interface pilot
v0.5 = small model LoRA/SFT training
v1.0 = resume-ready research-engineering deliverable
```

---

## 2. Original v0.3 Design

v0.3 的 router 输出是：

```json
{
  "read_hints": [],
  "write_spans": [],
  "ignore_spans": []
}
```

模型需要预测：

```text
1. read_hints：哪些 candidate memory IDs 应该读；
2. write_spans：当前用户输入中哪些 exact spans 应该写入 memory；
3. ignore_spans：当前用户输入中哪些 exact spans 应该忽略；
4. write_span type：fact / decision / sop / task_state。
```

这个设计可以运行，也积累了很多工程资产，但它越来越像：

```text
candidate selector + span extractor + type classifier
```

而不是最终产品所需的 memory policy layer。

---

## 3. v0.3 已完成资产

v0.3 不是失败品，应完整保留。

已完成资产包括：

```text
1. synthetic_train_5000.jsonl
2. dev_250.jsonl
3. gold_eval_300.jsonl
4. validators
5. normalizers
6. baseline evaluation
7. DeepSeek V4 Flash baseline
8. prediction validation
9. cost / latency logging
10. Qwen3-4B zero-shot smoke
11. generation / repair workflow
12. report-writing workflow
```

这些资产后续用于：

```text
1. v0.4 设计动机；
2. A/B/C 对比中的 Legacy Span JSON baseline；
3. hard case 来源；
4. final report 中的 project evolution 叙事；
5. evaluator / logging / report 代码迁移参考。
```

---

## 4. v0.3 主要成果

v0.3 证明了：

```text
1. 可以稳定生成和校验结构化 memory-policy 数据；
2. 可以建立 train/dev/gold split；
3. 可以实现 hard validators 和 semantic audits；
4. 可以跑 deterministic baselines 和 LLM router baseline；
5. 可以记录 cost / latency；
6. 可以基于外部审查修复 gold set；
7. 可以为小模型训练准备 instruction-format data。
```

这些能力对 v0.4/v0.5 仍然有价值。

---

## 5. v0.3 主要问题

v0.3 暴露的问题不是“不能跑”，而是“接口可能不适合最终目标”。

### 5.1 exact span labeling 脆弱

模型必须复制用户输入中的 exact substring。  
这带来：

```text
1. span 漏字、多字、边界不一致；
2. 自动校验困难；
3. 人工审核成本高；
4. 多个语义混在一句话时难标；
5. 小模型输出时容易出现近似但不完全匹配的 span。
```

### 5.2 complex JSON schema 对小模型不友好

Qwen-family 3B–4B smoke test 表明，小模型经常输出语义上接近但 schema 不合格的内容。

典型问题：

```text
模型输出 write_spans: ["..."]
而不是 write_spans: [{"span": "...", "type": "fact"}]
```

这说明模型可能知道该写什么，但 JSON/span schema 太脆。

### 5.3 fact/decision/sop/task_state 不能回答“写到哪里”

v0.3 的 write type 回答：

```text
这条信息是什么性质？
```

但真实 memory policy 还需要回答：

```text
这条信息应该写到哪个 memory bucket？
```

例如：

```text
用户长期偏好 → user_profile
项目设计决策 → project_memory
代码仓库命令 → repo_memory
业务服务事实 → service_memory
当前任务进度 → task_state
```

### 5.4 ignore_spans 不如 SKIP unit 自然

v0.3 的 ignore_spans 要模型复制不该记的原文片段。  
v0.4 的 SKIP unit 更自然：

```text
u3: 顺便帮我查天气
→ SKIP u3
```

### 5.5 hard validation 不等于 semantic quality

v0.3 经验表明：

```text
0 invalid JSON
0 invalid spans
0 schema errors
```

并不保证语义标签完全正确。

例如：

```text
ignore_noise 可能隐藏真实 durable memory；
no_action_needed 可能包含低价值但仍可记的信息；
conflicting_memory 可能结构合法但写了错误事实。
```

---

## 6. Why v0.4 Better Matches the Goal

v0.4 直接建模 memory policy decision：

```text
READ：哪些 candidate memories 应该注入主模型上下文；
STORE：哪些 current units 应进入 memory write pipeline；
target：STORE 到 user/project/repo/service/task 哪个 memory bucket；
SKIP：哪些 current units 应跳过。
```

v0.4 输入：

```text
RUNTIME_CONTEXT
CANDIDATE_MEMORIES
CURRENT_UNITS
```

v0.4 输出：

```text
READ m1,m3
STORE task_state u1
STORE repo_memory u2
SKIP u3
```

这个接口的优势：

```text
1. 小模型不需要复制 exact span；
2. 输出 DSL 比 JSON 更低熵；
3. STORE target 更贴近真实 memory owner；
4. SKIP unit 比 ignore span 更自然；
5. parser 可以严格校验而不做语义修复；
6. 更适合 3B–4B 小模型训练和部署。
```

---

## 7. Alternatives Considered

### Option A：继续 v0.3 并训练 LoRA

优点：

```text
1. 已有 5000 train；
2. 可较快跑出一个训练结果；
3. 能证明小模型可学习旧 schema。
```

问题：

```text
1. 会强化旧接口的 sunk cost；
2. 训练结果不一定解决产品目标；
3. 仍需面对 exact span 和 complex JSON；
4. 不能回答 memory 应写到哪里；
5. 后续仍可能要迁移到 v0.4。
```

结论：不作为主线。

---

### Option B：直接重做 5000 条 v0.4 并训练

优点：

```text
1. 快速进入新主线；
2. 看起来进度大。
```

问题：

```text
1. v0.4 DSL / target / unit / parser 还没验证；
2. 如果 guideline 之后改，数据会返工；
3. 没有 A/B/C 证据支撑 pivot；
4. 风险过高。
```

结论：不建议。

---

### Option C：正式 pivot，但先做 v0.4 bridge pilot

优点：

```text
1. 保留 v0.3 成果；
2. 用小规模实验验证接口；
3. 避免直接重做大数据；
4. 能产出清晰 research narrative；
5. 成功后再进入 v0.5 训练。
```

结论：采纳。

---

## 8. Accepted Plan

正式计划：

```text
1. Freeze v0.3 as prototype and baseline evidence.
2. Create v0.4 planning/spec/status files.
3. Implement v0.4 DSL parser and canonical JSON validator.
4. Build 30–50 bridge cases.
5. Compare Legacy Span JSON, Unit JSON, Unit DSL.
6. If bridge passes, expand to 200–300 pilot cases.
7. If v0.4 pilot passes, proceed to v0.5 LoRA/SFT small-router training.
```

---

## 9. v0.3 Assets: Preserve / Reuse / Abandon

### 9.1 Preserve

```text
data/processed/synthetic_train_5000.jsonl
data/dev/dev_250.jsonl
data/gold/gold_eval_300.jsonl
results/day7_student_data/
validation reports
distribution reports
cost / latency logs
baseline evaluation reports
Qwen3 smoke outputs
```

### 9.2 Reuse

```text
evaluation harness structure
validation pattern
cost / latency logging
report templates
generation / repair workflow
hard-case examples
some prompts as contrastive baseline
```

### 9.3 Do not directly reuse without review

```text
v0.3 5000 train labels
v0.3 category labels
span-normalization metrics
fact/decision/sop/task_state typed-write metrics
```

### 9.4 Explicitly abandon as final mainline concepts

```text
exact write_spans as primary STORE output
ignore_spans as primary SKIP output
fact/decision/sop/task_state as primary write target
complex JSON as model raw output
```

---

## 10. How to Frame the Pivot

Final report / README should describe the pivot as:

```text
We first built a JSON/span-based memory router prototype (v0.3) with synthetic train/dev/gold data, validators, baselines, and small-model smoke tests. The prototype revealed that exact-span labeling is expensive to audit and that complex JSON schemas are brittle for 3B–4B local models. Since the real agent-memory problem is closer to read/store/skip policy routing than span extraction, we redesigned the interface into a unit-based READ/STORE/SKIP DSL and evaluated it with a controlled interface pilot.
```

中文面试表达：

```text
我不是一开始就拍脑袋设计 DSL。先做了 v0.3 JSON/span prototype，跑通数据、校验和 baseline。后来在小模型 smoke test 里发现复杂 JSON 和 exact span 对 3B–4B 模型不稳定，而且 fact/decision 这些 type 不能回答“写到哪里”。所以我把项目 pivot 成 unit-based READ/STORE/SKIP DSL，用 v0.4 小规模实验去比较旧方案和新方案。
```

---

## 11. Consequences

### Positive

```text
1. 项目研究问题更清楚；
2. 更贴近 coding/business agent memory control；
3. 更适合小模型；
4. 可以把历史踩坑变成实验对比；
5. 简历叙事更强；
6. v0.5 训练风险更低。
```

### Negative / Cost

```text
1. v0.3 5000 train 不能直接当最终训练集；
2. 需要重新定义 case schema；
3. 需要重新写 parser / metrics；
4. 需要做新的 30–50 bridge 和 200–300 pilot；
5. 短期看似绕路。
```

### Why the cost is acceptable

因为 v0.3 已经证明旧接口存在风险。  
如果现在继续训练旧接口，后续可能会更大规模返工。

---

## 12. Final Decision Statement

```text
The project should officially pivot from v0.3 JSON/span routing to v0.4 unit-based READ/STORE/SKIP DSL before small-model training.

v0.3 will be preserved as prototype, baseline, and empirical motivation.
v0.4 will first run a controlled interface pilot.
v0.5 training will only start after v0.4 validates the interface.
```
