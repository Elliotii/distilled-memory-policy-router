# PROJECT_CONTEXT_FOR_CODEX

> 用途：这是给 Codex 新 context 的主上下文文件。  
> Codex 每次开始 v0.4 相关工作前，应先阅读本文件，再阅读 `V03_TO_V04_DECISION_RECORD.md`、`V04_EXECUTION_PLAN.md` 和 `CODEX_WORKFLOW_RULES.md`。  
> 本文件的目标不是重新设计项目，而是帮助 Codex 在已有历史和当前共识基础上执行。

---

## 0. 当前一句话结论

本项目从 v0.3 JSON/span router 正式 pivot 到 v0.4 unit-based `READ / STORE / SKIP` DSL，但不推倒重来。

```text
v0.3 = 已完成的 prototype / baseline / 设计证据
v0.4 = 当前新主线：interface pilot
v0.5 = 后续小模型 LoRA/SFT 训练
v1.0 = 简历级 research-engineering 交付版
```

v0.4 开始后，**不要继续把 v0.3 JSON/span schema 当主线**，也不要马上训练 LoRA 或重做 5000 条数据。  
下一步是先完成 v0.4 的最小 interface pilot。

---

## 1. 项目原始目标

原始业务目标是：

> 帮助 AI coding/business agent 可靠记住业务进度、稳定事实、项目/用户偏好，同时避免临时、噪声、敏感、过期或无关内容污染 memory。

项目不是要做完整 agent，不是做 retriever，不是做 vector database，也不是做完整 MemoryOS。

真正研究对象是一个窄的 memory policy layer（记忆策略层）：

```text
1. 什么时候读 memory；
2. 已经检索出来的 candidate memories 中哪些该注入上下文；
3. 当前输入中哪些信息应该写入 durable memory pipeline；
4. 如果要写，应该写到哪个 memory target；
5. 哪些当前信息应该跳过。
```

---

## 2. 当前 repo 的 v0.3 状态

当前已有主线是 v0.3 JSON/span router。

v0.3 输出格式大致是：

```json
{
  "read_hints": [],
  "write_spans": [],
  "ignore_spans": []
}
```

v0.3 任务要求模型：

```text
1. 预测要读的 candidate memory IDs；
2. 从当前用户输入中复制 exact text spans 作为 write_spans；
3. 从当前用户输入中复制 exact text spans 作为 ignore_spans；
4. 给 write_spans 标注 type，例如 fact / decision / sop / task_state。
```

v0.3 已经完成了大量资产：

```text
- synthetic_train_5000.jsonl
- dev_250.jsonl
- gold_eval_300.jsonl
- validators
- prediction validation
- baseline evaluation
- V4 Flash router baseline
- Qwen3-4B zero-shot smoke
- cost / latency logging
- report generation workflow
```

这些成果要保留，但 v0.3 不再作为最终主线继续扩展。

---

## 3. v0.3 的核心经验

v0.3 有价值，不是废弃物。

它证明了：

```text
1. 项目能生成和校验结构化 memory-policy 数据；
2. 已经建立 train/dev/gold 和 eval 思维；
3. 已经有 validator / normalizer / baseline / cost logging；
4. V4 Flash 可以作为强 baseline；
5. Qwen-family 3B–4B 小模型在复杂 JSON/span schema 上存在明显脆弱性；
6. exact-span labeling 生成和人工审核成本较高；
7. hard validation 不等于 semantic quality；
8. category definitions 容易 drift，需要 strict guideline。
```

v0.3 最重要的研究证据是：

```text
小模型不一定完全不会判断 memory policy；
但 v0.3 的 JSON/span 输出接口对 3B–4B 小模型过于脆弱。
```

---

## 4. 为什么 pivot 到 v0.4

v0.3 的问题不是“没做完”，而是接口和最终业务目标不够匹配。

v0.3 关注：

```text
read_hints + exact write_spans + exact ignore_spans + write type
```

但真实 agent memory policy 更接近：

```text
READ：哪些候选 memory 应该读入上下文；
STORE：当前哪些输入 unit 应进入长期记忆管道；
target：写到 user/project/repo/service/task 哪个 memory bucket；
SKIP：哪些 unit 应该跳过。
```

因此 v0.4 采用：

```text
unit-based READ / STORE / SKIP DSL
+ strict parser
+ canonical JSON
+ fixed candidate memories
+ current units
```

v0.4 的关键思想：

```text
小模型输出低熵 DSL；
系统内部再转换为 canonical JSON；
parser 只做解析和校验，不做语义修复。
```

---

## 5. v0.4 的核心输入输出

### 5.1 输入示例

```text
RUNTIME_CONTEXT
project: memory-router
repo: memory-router
service: parser
task: v0.4 interface pilot

CANDIDATE_MEMORIES
m1 [project_memory]: 当前项目决定先做 v0.4 interface pilot，不训练正式 LoRA。
m2 [repo_memory]: 本 repo 的 parser 测试命令是 pytest tests/parser。
m3 [task_state]: strict parser 已完成，target guideline 还没写。
m4 [service_memory]: parser module 只负责 DSL 解析和校验，不做语义修复。

CURRENT_UNITS
u1: 我们先别训练 LoRA，继续把 v0.4 pilot 做扎实。
u2: parser 已经差不多完成了。
u3: 顺便帮我查一下今天吉隆坡天气。
```

### 5.2 模型输出 DSL 示例

```text
READ m1,m3,m4
STORE task_state u1
STORE task_state u2
SKIP u3
```

空值写法：

```text
READ NONE
STORE NONE
SKIP u1,u2
```

### 5.3 canonical JSON 示例

```json
{
  "schema_version": "memory_policy.v0.4",
  "read": [
    {"memory_id": "m1"},
    {"memory_id": "m3"}
  ],
  "store": [
    {"target": "task_state", "unit_id": "u1"},
    {"target": "task_state", "unit_id": "u2"}
  ],
  "skip": [
    {"unit_id": "u3"}
  ],
  "validation": {
    "valid": true,
    "errors": []
  }
}
```

---

## 6. v0.4 的 5 个 STORE target

v0.4 保留 5 类 target：

```text
user_profile
project_memory
repo_memory
service_memory
task_state
```

### user_profile

用户长期、稳定、非敏感、跨项目复用的偏好。

例：

```text
用户希望技术解释默认用中文。
用户喜欢先讲结论，再讲原因。
```

### project_memory

整个项目级事实、目标、设计决策、跨 repo / service 的共识。

例：

```text
当前项目不做完整 MemoryOS，只做轻量 policy router。
v0.4 目标是 interface pilot，不训练正式 LoRA。
```

### repo_memory

代码仓库开发相关信息：命令、目录结构、测试方式、代码规范。

例：

```text
这个 repo 的测试命令是 pytest tests/。
parser 代码放在 src/parser.py。
```

### service_memory

某个业务服务 / 模块 / 系统组件自身的长期稳定事实、行为、依赖、接口、约束。

例：

```text
payments service 每天 02:00 UTC 导出 invoices。
parser module 只负责解析 DSL，不做语义修复。
```

### task_state

当前任务进度、下一步、阻塞、已完成事项。

例：

```text
strict parser 已完成。
target guideline 还没写。
下一步要做 30–50 条 bridge cases。
```

---

## 7. 明确 out of scope

v0.4 不做：

```text
完整 MemoryOS
真实 retriever
BM25 / vector DB / RRF 实现
memory DB
writer canonical rewrite
ADD / UPDATE / DELETE / MERGE
entity resolution
SOP / skill 系统
profile evolution
LLM unitizer
agentic retrieval
复杂 type × target taxonomy
ignore reason 分类
confidence scores
完整 downstream agent benchmark
```

v0.4 只做 interface pilot，不做正式 LoRA 训练。

v0.5 才考虑小模型 LoRA/SFT。

---

## 8. v0.4 最小研究问题

v0.4 不是为了堆功能，而是验证三个设计判断：

```text
1. Unit ID 是否比 exact span 更适合小模型？
2. DSL 是否比 JSON 更适合小模型原始输出？
3. READ / STORE / SKIP 是否能更贴近 agent memory policy？
```

因此需要比较：

```text
A. Legacy Span JSON
B. Unit JSON
C. Unit DSL
```

### A. Legacy Span JSON

```json
{
  "read_hints": ["m1"],
  "write_spans": [
    {"span": "parser is almost complete", "type": "task_state"}
  ],
  "ignore_spans": ["check today's weather"]
}
```

### B. Unit JSON

```json
{
  "read": ["m1"],
  "store": [
    {"target": "task_state", "unit_id": "u2"}
  ],
  "skip": ["u3"]
}
```

### C. Unit DSL

```text
READ m1
STORE task_state u2
SKIP u3
```

---

## 9. v0.4 执行原则

从现在开始，Codex 应遵循：

```text
1. 保留原 repo，不新建独立 repo；
2. 新建 v0.4 branch 或至少明确 v0.4 工作区；
3. v0.3 文件只读归档，不 silent-edit 旧数据；
4. v0.4 先做 30–50 curated bridge cases；
5. bridge 通过后再扩到 200–300 pilot cases；
6. pilot 通过后再进入 v0.5 training；
7. 每个阶段结束更新 CURRENT_STATE.md；
8. 每个阶段结束前跑测试 / smoke eval；
9. 任何 scope expansion 必须先询问用户。
```

---

## 10. 推荐新目录

建议新增：

```text
docs/v04_planning/
  PROJECT_CONTEXT_FOR_CODEX.md
  V03_TO_V04_DECISION_RECORD.md
  V04_EXECUTION_PLAN.md
  CODEX_WORKFLOW_RULES.md

docs/v04_spec/
  V04_SPEC.md
  TARGET_GUIDELINE.md
  EVAL_PLAN.md

docs/status/
  CURRENT_STATE.md

data/v04/
  bridge_cases.jsonl
  pilot_cases.jsonl

prompts/v04/
  legacy_span_json.txt
  unit_json.txt
  unit_dsl.txt

reports/v04/
  bridge_report.md
  interface_pilot_report.md
  error_analysis.md
```

实际路径可根据 repo 现状微调，但不应混入旧 v0.3 主目录导致语义混乱。

---

## 11. 给 Codex 的当前任务边界

如果 Codex 读到本文件后开始工作，第一步应该是：

```text
1. 检查 git status；
2. 总结当前 repo 结构；
3. 确认 v0.3 资产位置；
4. 创建或建议 v0.4 规划目录；
5. 更新/创建 CURRENT_STATE.md；
6. 等用户确认后，再进入 V04_SPEC / parser / data 工作。
```

不要一上来写 LoRA、retriever、writer、MemoryOS 或大规模数据生成。

---

## 12. 最终项目叙事

最终简历/报告应这样讲：

```text
我先做了 v0.3 JSON/span memory router prototype，完成 5000 train、dev/gold、validator 和 baseline；
随后在小模型 smoke test 中发现复杂 JSON/span schema 对 3B–4B model 脆弱；
因此将项目 pivot 到 unit-based READ/STORE/SKIP DSL；
通过 v0.4 interface pilot 比较 Legacy Span JSON、Unit JSON 和 Unit DSL；
最终基于稳定接口进入 v0.5 小模型 LoRA/SFT 训练。
```

这不是推倒重来，而是 research-engineering 中基于实验发现的接口重构。
