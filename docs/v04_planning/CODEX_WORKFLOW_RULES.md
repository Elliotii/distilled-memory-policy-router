# CODEX_WORKFLOW_RULES

> 用途：约束 Codex 在本项目中的执行方式，防止 scope drift（范围漂移）、过度工程化和误改旧成果。  
> Codex 每次新 context 开始前必须阅读本文件。

---

## 1. 总原则

你正在协助一个已有历史的 research-engineering 项目，不是从零开始设计 MemoryOS。

当前主线是：

```text
v0.4 unit-based READ / STORE / SKIP DSL interface pilot
```

你的任务是帮助实现、整理和验证这个窄问题，而不是扩展成完整 agent memory platform。

---

## 2. 绝对不要做的事

除非用户明确要求并提供新的规划文件，否则不要做：

```text
1. 不要实现完整 MemoryOS；
2. 不要实现真实 retriever；
3. 不要实现 BM25 / vector DB / RRF；
4. 不要接 Milvus / Chroma / Elasticsearch / Redis / MongoDB；
5. 不要实现 memory writer intelligence；
6. 不要做 ADD / UPDATE / DELETE / MERGE；
7. 不要做 entity resolution；
8. 不要做 SOP / skill 系统；
9. 不要做 LLM unitizer；
10. 不要做 agentic retrieval；
11. 不要做完整 downstream agent benchmark；
12. 不要新加 target；
13. 不要新加 type / subtype / reason / entity / confidence；
14. 不要把 parser 写成会语义猜测的 repair system；
15. 不要 silent edit 旧 v0.3 数据。
```

如果你认为必须做其中之一，先停下来，向用户说明理由并等待确认。

---

## 3. 当前允许做的事

v0.4 阶段允许做：

```text
1. 创建 v0.4 planning/spec/status 目录；
2. 写或整理 markdown 规划文件；
3. 定义 v0.4 case schema；
4. 实现 READ/STORE/SKIP DSL parser；
5. 实现 canonical JSON validator；
6. 写 parser tests；
7. 创建 30–50 bridge cases；
8. 创建 200–300 pilot cases；
9. 实现 A/B/C interface evaluation；
10. 实现 metrics；
11. 生成 reports；
12. 复用 v0.3 的 validator / logging / report pattern；
13. 更新 CURRENT_STATE.md。
```

---

## 4. 工作方式

每次开始任务时，先做：

```text
1. 读取相关 planning/spec/status 文件；
2. 运行或查看 git status；
3. 简短总结当前理解；
4. 给出本次最小执行计划；
5. 明确本次不会触碰哪些范围；
6. 等用户确认后再改文件。
```

不要一上来就大规模改代码。

---

## 5. Git / 文件安全规则

### 必须

```text
1. 修改前检查 git status；
2. 不要删除旧 v0.3 数据；
3. 不要覆盖已有重要报告；
4. 新文件优先放入 v0.4 专属目录；
5. 大范围移动文件前必须询问；
6. 每个阶段结束更新 CURRENT_STATE.md；
7. 列出新增/修改文件；
8. 提醒用户 commit。
```

### 建议

```text
v0.3 freeze 后创建新 branch：
v0.4-interface-pilot
```

如果未创建 branch，至少不要直接修改旧主线数据。

---

## 6. Parser 规则

v0.4 parser 是 strict parser，不是智能修复器。

它可以做：

```text
1. parse；
2. validate memory IDs；
3. validate unit IDs；
4. validate target；
5. detect duplicate；
6. detect missing STORE/SKIP assignment；
7. sort / normalize；
8. convert to canonical JSON；
9. report errors。
```

它不能做：

```text
1. 根据 unit 文本猜 target；
2. 根据 memory 内容补 READ；
3. 把非法 target 自动改成合法 target；
4. 模型漏写 STORE 时自动补；
5. 模型漏写 SKIP 时自动判断；
6. 进行 semantic repair；
7. 为了提高 metrics 偷偷纠错。
```

如果模型输出非法，parser 应返回 validation error，而不是悄悄修。

---

## 7. Data 规则

### v0.4 数据原则

```text
1. 少量高质量优先；
2. 先 30–50 bridge cases；
3. 再 200–300 pilot cases；
4. 不直接重做 5000 条；
5. 不直接把 v0.3 labels 字段重命名成 v0.4；
6. v0.3 hard cases 可作为 inspiration，但需要人工重审；
7. 每条 case 应有明确 gold；
8. target-boundary case 要记录 notes；
9. sensitive/private content 默认 SKIP。
```

### 禁止

```text
1. 不要 silent repair data；
2. 不要用 parser 或脚本自动猜 gold target；
3. 不要把 project_memory 当所有不确定项；
4. 不要生成大量未审核数据冒充 gold；
5. 不要把 v0.3 fact/decision/sop/task_state 直接映射成 v0.4 target。
```

---

## 8. Target 规则

合法 STORE targets 只有：

```text
user_profile
project_memory
repo_memory
service_memory
task_state
```

不要新增：

```text
team_memory
team_sop
fact_memory
decision_memory
preference_memory
entity_memory
sop_memory
```

### 简要定义

```text
user_profile：用户长期、稳定、非敏感偏好。
project_memory：项目级目标、决策、共识。
repo_memory：代码仓库规则、命令、目录、测试方式。
service_memory：具体服务 / 模块 / 组件自身的长期事实。
task_state：当前任务进度、下一步、阻塞。
```

---

## 9. CURRENT_STATE.md 更新要求

每个 Codex context 结束前，必须更新或建议更新：

```text
docs/status/CURRENT_STATE.md
```

推荐格式：

```markdown
# CURRENT_STATE

## Last Updated
YYYY-MM-DD HH:MM

## Current Milestone
P0 / P1 / P2 / P3 / P4 / P5

## Completed
- ...

## Files Changed
- ...

## Tests / Commands Run
- ...

## Key Decisions
- ...

## Open Issues
- ...

## Risks / Scope Drift Watch
- ...

## Recommended Next Step
- ...
```

这样下一个 Codex context 能接上。

---

## 10. Checkpoint 规则

遇到以下阶段时，必须暂停并建议用户进行外部审查：

```text
1. v0.3 freeze / v0.4 setup 完成；
2. V04_SPEC + TARGET_GUIDELINE 初稿完成；
3. parser + tests 完成；
4. 30–50 bridge cases 完成；
5. 200–300 pilot + A/B/C eval 完成；
6. v0.5 training 前；
7. v0.5 training result 后。
```

不要跨 checkpoint 连续推进太远。

---

## 11. 思考模式建议

如果 Codex 支持不同 reasoning / thinking level，请按任务选择：

### 高思考

用于：

```text
1. schema 设计；
2. DSL grammar；
3. target guideline；
4. eval 指标；
5. pivot / scope decision；
6. error analysis；
7. training failure analysis；
8. README / final report 叙事。
```

### 中等思考

用于：

```text
1. parser 实现；
2. metrics 实现；
3. eval runner；
4. baselines；
5. tests；
6. data conversion scripts；
7. small bug fixes。
```

### 低思考

用于：

```text
1. formatting；
2. typo；
3. comments；
4. small README edits；
5. file renaming after confirmed plan。
```

不要用低思考做架构决策。

---

## 12. 与用户协作方式

用户会在 ChatGPT 中做规划和 steering。  
Codex 负责 repo 内执行。

因此：

```text
1. 不要把自己当唯一规划者；
2. 发现方向问题时先报告；
3. 不要擅自扩大 scope；
4. 阶段性输出要方便用户拿去给 ChatGPT 审查；
5. 每次输出都要明确下一步。
```

---

## 13. 输出风格

完成任务时，回复应包含：

```text
1. 完成了什么；
2. 改了哪些文件；
3. 跑了哪些测试/命令；
4. 是否有失败；
5. 当前风险；
6. 下一步建议；
7. 是否需要用户确认。
```

不要只说“done”。

---

## 14. v0.4 的成功标准

v0.4 不是以代码量为成功标准。

成功标准是：

```text
1. v0.4 spec 清楚；
2. parser 严格可靠；
3. 30–50 bridge cases 暴露并修正边界；
4. 200–300 pilot 可以比较 A/B/C；
5. Unit DSL 的接口优势有数据支持；
6. 5 target guideline 可用；
7. 可以明确决定是否进入 v0.5 training。
```

---

## 15. 最重要的一句话

```text
不要把项目做大，而是把 memory policy router 这个窄问题做深、做稳、做可评估。
```
