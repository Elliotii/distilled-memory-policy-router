# V04_EXECUTION_PLAN

> 用途：v0.4 interface pilot 的执行计划。  
> 原则：不做大系统，不重做 5000 条，不马上训练 LoRA。先用小规模、可控、可评估的 pilot 验证接口。

---

## 0. Executive Summary

当前路线：

```text
P0：v0.3 freeze & v0.4 setup
P1：v0.4 spec / parser / schema
P2：30–50 bridge cases
P3：200–300 interface pilot
P4：v0.4 report & go/no-go decision
P5：v0.5 training preparation（仅在 v0.4 通过后）
```

v0.4 成功后才进入 v0.5 小模型训练。

---

## 1. Global Goals

v0.4 要验证：

```text
1. Unit ID 是否比 exact span 更适合小模型；
2. DSL 是否比 JSON 更稳定、更低熵；
3. READ / STORE / SKIP 是否更贴近 memory policy；
4. 5 个 STORE target 是否可标注、可学习；
5. strict parser 是否能在不做 semantic repair 的前提下消费模型输出。
```

v0.4 不追求：

```text
1. 训练正式 LoRA；
2. 重做 5000 条；
3. 实现真实 retriever；
4. 实现 memory DB；
5. 实现 writer/update/merge；
6. 做完整 MemoryOS。
```

---

## 2. Milestone P0：Freeze & Setup

### 目标

保留 v0.3 历史，创建 v0.4 工作区，防止旧主线和新主线混乱。

### Codex 应做

```text
1. 运行 git status；
2. 总结当前 repo 结构；
3. 确认 v0.3 数据、docs、results 的位置；
4. 建议或创建 v0.4 planning/spec/status 目录；
5. 创建 docs/status/CURRENT_STATE.md 初稿；
6. 不修改旧 v0.3 数据；
7. 不删除旧结果；
8. 等用户确认。
```

### 推荐目录

```text
docs/v04_planning/
docs/v04_spec/
docs/status/
data/v04/
prompts/v04/
reports/v04/
```

### Deliverables

```text
docs/status/CURRENT_STATE.md
v0.4 目录结构
v0.3 freeze 说明
```

### Acceptance Criteria

```text
1. git status 清楚；
2. v0.3 文件未被误改；
3. v0.4 目录存在或被明确规划；
4. CURRENT_STATE.md 能让下一个 Codex context 接上。
```

---

## 3. Milestone P1：Spec / Parser / Schema

### 目标

定义 v0.4 的最小技术接口，并实现 strict parser 的基础版本。

### 需要准备的文档

```text
docs/v04_spec/V04_SPEC.md
docs/v04_spec/TARGET_GUIDELINE.md
docs/v04_spec/EVAL_PLAN.md
```

### Parser 最小功能

输入 DSL：

```text
READ m1,m3
STORE task_state u1
STORE repo_memory u2
SKIP u3
```

输出 canonical JSON：

```json
{
  "schema_version": "memory_policy.v0.4",
  "read": [{"memory_id": "m1"}, {"memory_id": "m3"}],
  "store": [
    {"target": "task_state", "unit_id": "u1"},
    {"target": "repo_memory", "unit_id": "u2"}
  ],
  "skip": [{"unit_id": "u3"}],
  "validation": {
    "valid": true,
    "errors": []
  }
}
```

### Parser 必须校验

```text
1. READ memory IDs 是否存在于 candidate_memories；
2. STORE unit IDs 是否存在于 current_units；
3. STORE target 是否属于 5 个合法 target；
4. SKIP unit IDs 是否存在于 current_units；
5. 每个 unit 必须且只能出现在 STORE 或 SKIP 中一次；
6. READ NONE / STORE NONE / SKIP NONE 的合法性；
7. 重复 ID 去重或报错的策略需明确；
8. 不允许 parser 根据文本猜 target。
```

### Deliverables

```text
src/parser.py 或现有 src 下对应 parser 文件
tests/test_parser_v04.py
docs/v04_spec/V04_SPEC.md
docs/v04_spec/TARGET_GUIDELINE.md 初稿
```

### Acceptance Criteria

```text
1. parser 能解析合法 DSL；
2. parser 能拒绝非法 target / unit / memory ID；
3. tests 覆盖正常、空值、重复、非法 ID、漏 unit、STORE/SKIP 冲突；
4. parser 不做 semantic repair。
```

---

## 4. Milestone P2：Bridge Cases 30–50

### 目标

用 30–50 条 hand-curated cases 验证：

```text
1. case schema 是否合理；
2. 5 target guideline 是否足够清楚；
3. DSL parser 和 metrics 是否能跑通；
4. A/B/C 对比是否可执行；
5. 有没有明显标注边界问题。
```

### Case 结构建议

```json
{
  "case_id": "v04_bridge_0001",
  "runtime_context": {
    "project": "memory-router",
    "repo": "memory-router",
    "service": "parser",
    "task": "v0.4 interface pilot"
  },
  "candidate_memories": [
    {
      "memory_id": "m1",
      "target": "project_memory",
      "content": "当前项目决定先做 v0.4 interface pilot，不训练正式 LoRA。"
    }
  ],
  "current_units": [
    {
      "unit_id": "u1",
      "text": "我们先别训练 LoRA，继续把 v0.4 pilot 做扎实。"
    }
  ],
  "gold": {
    "read": ["m1"],
    "store": [
      {"target": "task_state", "unit_id": "u1"}
    ],
    "skip": []
  },
  "tags": ["read_store_joint", "task_state"],
  "notes": "用于测试 project_memory read + task_state store"
}
```

### Bridge case mix

```text
READ-only：8–10
STORE/SKIP-only：10–12
READ + STORE joint：10–12
stale / related-but-useless：5–8
target-boundary：5–8
user_profile / sensitive boundary：3–5
```

### Deliverables

```text
data/v04/bridge_cases.jsonl
reports/v04/bridge_report.md
初步 target ambiguity notes
```

### Acceptance Criteria

```text
1. 30–50 cases 全部能被 schema validator 读取；
2. gold DSL / canonical JSON 能和 parser 对齐；
3. target 冲突样例被记录；
4. 能跑最小 eval；
5. 用户/项目负责人确认后再扩到 200–300。
```

---

## 5. Milestone P3：Interface Pilot 200–300

### 目标

扩展到 200–300 高质量 cases，正式比较：

```text
A. Legacy Span JSON
B. Unit JSON
C. Unit DSL
```

### 建议规模

```text
READ-only：40–50
STORE/SKIP-only：50–70
READ + STORE joint：60–80
stale / related-but-useless：30–40
target-boundary：30–40
user_profile / sensitive-boundary：20–30
```

### 数据来源

```text
1. v0.3 hard cases 改造；
2. 手工构造 coding/business agent 场景；
3. 少量参考 EverOS-style 对话风格，但不照搬 gold；
4. 专门构造 stale / related-but-useless candidate memories；
5. 专门构造 project/repo/service/task_state/user_profile 边界。
```

### Deliverables

```text
data/v04/pilot_cases.jsonl
prompts/v04/legacy_span_json.txt
prompts/v04/unit_json.txt
prompts/v04/unit_dsl.txt
src/metrics.py
src/eval_v04.py
reports/v04/interface_pilot_report.md
reports/v04/error_analysis.md
```

### Acceptance Criteria

```text
1. 数据通过 schema validation；
2. 三种接口都能跑 eval；
3. parse success / invalid ID / target accuracy 等指标可计算；
4. 至少有一版 error analysis；
5. 结果能支持 go/no-go decision。
```

---

## 6. Milestone P4：v0.4 Report & Decision

### 目标

根据 v0.4 pilot 决定是否进入 v0.5 训练。

### Report 应回答

```text
1. Unit JSON 是否减少 span-copying 问题？
2. Unit DSL 是否比 Unit JSON 更少 parse/schema 错？
3. READ / STORE / SKIP 指标是否稳定？
4. 5 target 是否可标注？
5. 哪些 target 边界最容易混？
6. parser 是否保持 strict，没有 semantic repair？
7. 是否应该进入 v0.5 训练？
```

### 推荐结果表

| Interface | Parse Success | Invalid ID Rate | READ F1 | STORE Unit F1 | STORE Target Acc | SKIP F1 | Human Repair Cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Legacy Span JSON | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Unit JSON | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Unit DSL | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

### Go Criteria

进入 v0.5 的最低条件：

```text
1. Unit DSL parse success 明显优于 Legacy Span JSON；
2. Unit DSL semantic metrics 不低于 Unit JSON；
3. target accuracy 达到可接受水平；
4. false store / irrelevant read 问题可分析；
5. guideline 不需要大改；
6. parser 不需要 semantic repair 才能工作。
```

### No-Go / Fix Criteria

如果出现以下情况，应先修 v0.4：

```text
1. target 定义大面积混乱；
2. current_units 切分经常导致一个 unit 同时应 STORE 和 SKIP；
3. DSL grammar 不稳定；
4. parser 必须靠语义修复才能通过；
5. Unit DSL 没有比 Unit JSON / Legacy JSON 更好。
```

---

## 7. Milestone P5：v0.5 Training Preparation

仅在 v0.4 通过后进入。

### 目标

准备小模型训练，但不在 v0.4 中提前实现。

### v0.5 预期

```text
800–1200 train
100 dev
100 locked gold
Hugging Face + PyTorch + LoRA/SFT
对比 heuristic / zero-shot / teacher LLM / LoRA router
```

### v0.5 前必须确认

```text
1. DSL 不再频繁变；
2. target guideline 稳定；
3. parser/eval 稳定；
4. 数据 schema 稳定；
5. v0.4 report 支持继续投入。
```

---

## 8. Suggested 10–14 Day Schedule

此处 Day 不是历史命名方式，只是实际执行节奏参考。项目正式记录仍用 milestone。

### Days 1–2：P0 + P1 setup

```text
- 冻结 v0.3
- 创建 v0.4 docs/status/data/prompts/reports 目录
- 写/整理 V04_SPEC、TARGET_GUIDELINE、EVAL_PLAN 初稿
- 实现 parser skeleton
```

### Days 3–4：Parser + tests

```text
- 完成 strict parser
- 完成 canonical JSON validator
- 完成 parser tests
- 不做 semantic repair
```

### Days 5–6：Bridge cases

```text
- 构建 30–50 bridge cases
- 跑 schema validation
- 跑 parser/eval smoke
- 记录 target ambiguity
- 生成 bridge_report.md
```

### Days 7–10：Pilot dataset + A/B/C eval

```text
- 扩到 200–300 pilot cases
- 准备 A/B/C prompts
- 实现 metrics
- 跑 baseline / model outputs
- 生成 interface_pilot_report.md
```

### Days 11–14：Review + v0.5 decision

```text
- error analysis
- target guideline 修订
- go/no-go decision
- 若通过，准备 v0.5 data/training plan
```

---

## 9. Checkpoints Requiring Human Review

每个 checkpoint 完成后，应暂停并让项目负责人审查。

```text
Checkpoint 1：P0 freeze / setup 完成
Checkpoint 2：V04_SPEC + TARGET_GUIDELINE 初稿完成
Checkpoint 3：parser + tests 完成
Checkpoint 4：30–50 bridge cases 完成
Checkpoint 5：200–300 pilot + A/B/C eval 完成
Checkpoint 6：v0.5 training 前
```

---

## 10. Red Lines

执行 v0.4 时不要做：

```text
1. 不要实现真实 retriever；
2. 不要实现 memory DB；
3. 不要实现 writer/update/merge；
4. 不要做 LLM unitizer；
5. 不要加 ADD/UPDATE/DELETE；
6. 不要加 type/subtype/reason/entity；
7. 不要扩 target 到 5 类之外；
8. 不要重做 5000 条；
9. 不要训练 v0.3 LoRA；
10. 不要在 parser 中做 semantic repair；
11. 不要 silent edit 旧数据；
12. 不要把 project_memory 当所有不确定项的垃圾桶。
```

---

## 11. Expected v0.4 End State

v0.4 结束时，项目应具备：

```text
1. 明确的 v0.4 spec；
2. 5 target guideline；
3. strict DSL parser；
4. 30–50 bridge report；
5. 200–300 pilot dataset；
6. A/B/C interface comparison；
7. metrics and error analysis；
8. go/no-go decision for v0.5；
9. 清楚说明 v0.3 如何保留、v0.4 为什么 pivot。
```
