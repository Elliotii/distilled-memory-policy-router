# V04_TO_V10_STEERING_PLAN

> 文件定位：这是 Memory Policy Router 项目从 v0.4 bridge 之后到 v1.0 简历级交付的总控计划。  
> 作用：给后续 Codex contexts 作为路线基石，防止 scope drift（范围漂移）、过度工程化、提前训练或把项目重新做成 MemoryOS。  
> 使用方式：每次新开 Codex context 前，先阅读 `docs/status/CURRENT_STATE.md`，再阅读本文件，然后只执行当前 context 对应阶段。  
> 当前建议路径：`docs/v04_planning/V04_TO_V10_STEERING_PLAN.md`

---

## 0. 当前状态快照

截至 P3 bridge checkpoint，项目已经完成：

```text
P0：v0.3 freeze & v0.4 setup
P1：v0.4 spec / target guideline / eval plan
P2：strict DSL parser + parser tests
P2.5：case schema + case validator + bridge template
P3：40 条正式 bridge cases + bridge report
```

当前已经具备的核心能力：

```text
1. v0.4 planning docs
2. v0.4 interface spec
3. 5 target annotation guideline
4. eval plan
5. case schema
6. strict READ / STORE / SKIP DSL parser
7. case validator
8. parser tests
9. validator tests
10. bridge_cases_template.jsonl
11. formal bridge_cases.jsonl，40 条
12. bridge_report.md
```

当前 P3 结果摘要：

```text
Total bridge cases: 40
Candidate memories: 75
Current units: 96
Gold READ IDs: 45
Gold STORE units: 65
Gold SKIP units: 31

Gold output shapes:
- READ-only: 10
- STORE/SKIP-only: 15
- READ + STORE joint: 15

STORE target counts:
- task_state: 26
- service_memory: 16
- repo_memory: 13
- user_profile: 6
- project_memory: 4

Validator:
- validate_jsonl_file(data/v04/bridge_cases.jsonl) passed
- record_count = 40
- errors = 0

Tests:
- python3 -m unittest discover -s tests
- 36 tests passed
```

当前重要判断：

```text
P3 bridge set accepted for interface/guideline validation.
It is not locked gold.
It is not the final pilot dataset.
It should be reviewed semantically before scaling.
```

---

## 1. 项目最终定位

本项目不做完整 MemoryOS，不做大而全 agent memory platform。

最终定位是：

```text
面向 Coding / Business Agent 的轻量 Memory Policy Router。
```

更具体地说：

```text
在候选 memory 已经给定、当前输入已经切成 current units 的前提下，
训练 / 评估一个小模型 router，
让它输出 READ / STORE / SKIP，
决定哪些旧记忆该读入上下文、哪些当前信息该进入长期记忆管道、哪些应该跳过。
```

核心流程：

```text
Fixed Candidate Memories
+ Current Units
→ Small Policy Router
→ READ / STORE / SKIP DSL
→ Strict Parser
→ Canonical JSON
→ Eval / Later Training
```

项目含金量来自：

```text
1. 真实 agent memory 场景；
2. v0.3 JSON/span prototype 暴露问题；
3. v0.4 unit-based DSL 接口重构；
4. A/B/C interface comparison；
5. parser / validator / data / eval 闭环；
6. v0.5 小模型 LoRA/SFT 训练；
7. 清楚边界：不做 MemoryOS，只做 policy layer。
```

---

## 2. 不变量：后续所有阶段都必须遵守

### 2.1 主线不变量

```text
1. v0.4 主线是 unit-based READ / STORE / SKIP DSL。
2. 小模型原始输出低熵 DSL。
3. 系统内部消费 canonical JSON。
4. parser strict，不做 semantic repair。
5. 当前候选 memory 是 fixed candidates，不研究 retriever。
6. current units 已经给定，不研究 LLM unitizer。
7. STORE target 保持 5 类。
```

### 2.2 合法 STORE targets

只允许：

```text
user_profile
project_memory
repo_memory
service_memory
task_state
```

不要新增：

```text
fact
decision
preference
sop
team_memory
team_sop
entity_memory
reason
confidence
ADD
UPDATE
DELETE
MERGE
```

### 2.3 5 target 简要定义

```text
user_profile：
用户长期、稳定、非敏感、跨项目复用的偏好。

project_memory：
项目级目标、项目决策、全局共识、跨 repo / service 的约定。

repo_memory：
代码仓库开发方式、命令、目录结构、测试方式、代码规范。

service_memory：
某个服务 / 模块 / 组件自身的长期事实、接口、依赖、行为、约束。

task_state：
当前任务进度、下一步、阻塞、已完成事项、当前阶段临时约束。
```

### 2.4 关键边界规则

```text
1. project_memory 不能当垃圾桶。
2. task_state 只用于当前进度 / 下一步 / 阻塞 / 临时约束。
3. repo_memory 用于文件路径、命令、测试、目录、仓库规范。
4. service_memory 用于 parser / evaluator / validator / prompt_builder 等组件行为。
5. user_profile 只存长期稳定、非敏感用户偏好。
6. 敏感 / 私密 / token / password / private key 一律 SKIP。
```

### 2.5 绝对 out of scope

后续所有 context 都不应主动实现：

```text
完整 MemoryOS
真实 retriever
BM25 / vector DB / RRF
memory DB
writer canonical rewrite
ADD / UPDATE / DELETE / MERGE
entity resolution
SOP / skill 系统
profile evolution
LLM unitizer
agentic retrieval
完整 downstream agent benchmark
复杂前端 / dashboard
```

如果 Codex 认为必须做其中任何一项，必须先停止并向用户说明，不得擅自执行。

---

## 3. Codex Context 总体规划

当前已完成：

```text
Context 1：v0.4 Foundation Context
- P0 / P1 / P2 / P2.5

Context 2：Bridge Cases Context
- P3
```

后续建议：

```text
Context 3：Pilot Dataset Context
- P4：200–300 pilot cases

Context 4：A/B/C Eval Context
- P5：prompts + metrics + eval runner + interface comparison

Context 5：v0.5 Training Context
- small model LoRA/SFT

Context 6：v1.0 Packaging Context
- README / reports / demo / resume framing
```

每个 context 必须：

```text
1. 只做当前阶段；
2. 结束前更新 docs/status/CURRENT_STATE.md；
3. 输出 files changed / tests run / risks / next step；
4. 停在 checkpoint；
5. 回到 ChatGPT 做 steering review；
6. 不跨阶段自动推进。
```

---

## 4. Context 3：P4 Pilot Dataset Context

### 4.1 Context 3 目标

从 P3 的 40 条 bridge cases 扩展到 200–300 条 v0.4 pilot cases。

推荐目标：

```text
data/v04/pilot_cases.jsonl
reports/v04/pilot_data_report.md
```

建议规模：

```text
200–300 cases
```

推荐先做：

```text
200 cases
```

如果质量稳定，再扩到 250 或 300。

### 4.2 Context 3 输入文件

Codex Context 3 必须先读取：

```text
docs/status/CURRENT_STATE.md
docs/v04_planning/V04_TO_V10_STEERING_PLAN.md
docs/v04_spec/V04_SPEC.md
docs/v04_spec/TARGET_GUIDELINE.md
docs/v04_spec/EVAL_PLAN.md
docs/v04_spec/CASE_SCHEMA.md
src/v04/case_validator.py
data/v04/bridge_cases.jsonl
reports/v04/bridge_report.md
```

### 4.3 Context 3 允许做什么

允许：

```text
1. 创建 data/v04/pilot_cases.jsonl；
2. 创建 reports/v04/pilot_data_report.md；
3. 使用 bridge cases 作为风格和边界参考；
4. 用 case_validator 校验 pilot_cases.jsonl；
5. 统计 case type / tag / target / READ-STORE-SKIP 分布；
6. 根据 bridge_report 的 Human Review Points 强化边界；
7. 更新 CURRENT_STATE.md。
```

### 4.4 Context 3 禁止做什么

禁止：

```text
1. 不要写 A/B/C eval runner；
2. 不要写 prompts；
3. 不要调用模型；
4. 不要训练；
5. 不要改 parser，除非发现明确 bug 并先报告；
6. 不要修改 v0.3 数据；
7. 不要扩到 5000 条；
8. 不要实现 retriever / writer / MemoryOS；
9. 不要新增 target / type / reason / entity；
10. 不要把 P3 bridge template 当正式 pilot；
11. 不要把 project_memory 当不确定项垃圾桶。
```

### 4.5 Pilot 数据建议分布

如果生成 200 条：

```text
READ-only：35–40
STORE/SKIP-only：45–55
READ + STORE joint：55–65
stale / related-but-useless memories：25–30
target-boundary cases：25–30
user_profile / sensitive boundary cases：15–20
```

如果生成 250 条：

```text
READ-only：45–50
STORE/SKIP-only：55–65
READ + STORE joint：70–80
stale / related-but-useless memories：30–35
target-boundary cases：30–35
user_profile / sensitive boundary cases：20–25
```

如果生成 300 条：

```text
READ-only：50–60
STORE/SKIP-only：70–80
READ + STORE joint：70–80
stale / related-but-useless memories：30–40
target-boundary cases：30–40
user_profile / sensitive boundary cases：20–30
```

注意：case tags 可重叠，分布不是互斥总和。  
pilot_report 需要统计实际 gold output shape，而不是只统计 curation block。

### 4.6 Context 3 必须继承的 P3 经验

来自 P3 bridge report 的经验必须显式进入 P4：

```text
1. report / validator / evaluator 规则类 unit：
   如果是可复用组件行为，标 service_memory；
   如果是当前 checkpoint 下一步 / 临时约束，标 task_state。

2. project_memory：
   只用于项目方向、范围、全局决策；
   不用作不确定项 fallback。

3. stale memory：
   默认不 READ，除非当前任务需要历史对比。

4. sensitive/private：
   必须 SKIP，即使用 synthetic placeholders 也要审查。

5. SOP/skill：
   不新增 sop target；
   repo/project/service convention 可以分别进入 repo_memory / project_memory / service_memory；
   skill-system expansion 仍 out of scope，通常 SKIP。
```

### 4.7 Context 3 完成标准

Context 3 完成需要满足：

```text
1. pilot_cases.jsonl 存在；
2. 记录数在 200–300 之间，推荐先 200；
3. validate_jsonl_file 通过；
4. pilot_data_report.md 存在；
5. report 包含 case mix、tag distribution、target counts、READ/STORE/SKIP shape、known ambiguities；
6. 没有写 eval runner；
7. 没有训练；
8. 没有修改 v0.3；
9. CURRENT_STATE.md 更新；
10. 停止，等待 review。
```

### 4.8 Context 3 Go / No-Go

通过后才能进入 Context 4。

Go 条件：

```text
1. pilot data 结构全部通过；
2. 5 target 没有大面积混乱；
3. task_state / service_memory 边界可解释；
4. project_memory 没有变成 catch-all；
5. sensitive cases 都 SKIP；
6. 数据难度足以支持 A/B/C eval。
```

No-Go 条件：

```text
1. target 大面积混乱；
2. case 太模板化；
3. READ-only / STORE/SKIP / joint 分布严重失衡；
4. bridge 中暴露的边界问题在 pilot 中放大；
5. validator 通过但语义质量明显不足。
```

---

## 5. Context 4：P5 A/B/C Eval Context

### 5.1 Context 4 目标

在 pilot cases 上实现并运行 A/B/C interface comparison。

A/B/C：

```text
A. Legacy Span JSON
B. Unit JSON
C. Unit DSL
```

目标不是训练模型，而是验证接口：

```text
1. Unit ID 是否减少 span-copying 问题；
2. DSL 是否减少 JSON schema / parse 错误；
3. READ / STORE / SKIP 指标是否能稳定评估。
```

### 5.2 Context 4 输入文件

必须先读取：

```text
docs/status/CURRENT_STATE.md
docs/v04_planning/V04_TO_V10_STEERING_PLAN.md
docs/v04_spec/V04_SPEC.md
docs/v04_spec/EVAL_PLAN.md
docs/v04_spec/CASE_SCHEMA.md
docs/v04_spec/TARGET_GUIDELINE.md
data/v04/pilot_cases.jsonl
reports/v04/pilot_data_report.md
src/v04/parser.py
src/v04/case_validator.py
```

### 5.3 Context 4 允许做什么

允许：

```text
1. 创建 prompts/v04/legacy_span_json.txt；
2. 创建 prompts/v04/unit_json.txt；
3. 创建 prompts/v04/unit_dsl.txt；
4. 创建 src/v04/metrics.py；
5. 创建 src/v04/eval_runner.py 或等价轻量脚本；
6. 创建 reports/v04/interface_pilot_report.md；
7. 创建 reports/v04/error_analysis.md；
8. 实现 deterministic baselines；
9. 可实现 teacher / small model output loading 接口，但不一定实际调用模型；
10. 更新 CURRENT_STATE.md。
```

### 5.4 Context 4 禁止做什么

禁止：

```text
1. 不要训练 LoRA；
2. 不要扩数据到 5000；
3. 不要实现真实 retriever；
4. 不要实现 writer；
5. 不要新增 target；
6. 不要改变 DSL grammar，除非 P4 review 明确要求；
7. 不要引入复杂实验平台；
8. 不要做完整 downstream agent benchmark。
```

### 5.5 必须实现的 metrics

Structural：

```text
parse_success
invalid_memory_id_rate
invalid_unit_id_rate
invalid_target_rate
output_length
human_repair_cost
```

Semantic：

```text
READ precision / recall / F1
STORE unit F1
STORE target accuracy
SKIP F1
false_store_rate
irrelevant_read_rate
```

A/B/C 特殊注意：

```text
A Legacy Span JSON 需要 span validity / schema validity / span copying error；
B Unit JSON 需要 JSON parse/schema validity；
C Unit DSL 使用 strict parser。
```

### 5.6 推荐 baselines

```text
empty / no-action
top-k READ
heuristic
teacher LLM output if available
zero-shot small model output if available
Unit DSL prompt
```

如果当前没有模型 API 或本地推理，不要卡住。可以先实现：

```text
1. output file format；
2. metric computation；
3. deterministic baselines；
4. manual / mocked predictions for smoke test。
```

### 5.7 Context 4 完成标准

```text
1. A/B/C prompt files 存在；
2. metrics.py 存在；
3. eval runner 跑通；
4. 至少 deterministic baselines 跑通；
5. 有 interface_pilot_report.md；
6. 有 error_analysis.md 或 error section；
7. 可以明确是否进入 v0.5 training；
8. CURRENT_STATE.md 更新；
9. 停止等待 review。
```

### 5.8 Context 4 Go / No-Go

Go to v0.5 条件：

```text
1. Unit DSL parse success 明显优于 Legacy Span JSON；
2. Unit DSL semantic metrics 不低于 Unit JSON；
3. Unit DSL invalid ID / invalid target 可控；
4. target guideline 不需要大改；
5. strict parser 不依赖 semantic repair；
6. false store / irrelevant read 可解释；
7. A/B/C 结果能支撑训练。
```

No-Go 条件：

```text
1. Unit DSL 没有结构优势；
2. Unit JSON 明显优于 DSL；
3. target 混乱导致 STORE target accuracy 无意义；
4. parser 必须靠语义修复；
5. A/B/C 无法公平比较；
6. sensitive store 风险明显。
```

---

## 6. Context 5：v0.5 Mini Training Context

### 6.1 Context 5 目标

基于 v0.4 稳定接口，构建训练数据并训练小模型 router。

这是求职含金量的重要阶段，覆盖：

```text
Hugging Face
PyTorch
LoRA / QLoRA
SFT
small model router
evaluation
bad case analysis
```

### 6.2 进入条件

只有 Context 4 review 后明确通过，才能进入。

必须满足：

```text
1. DSL 接口稳定；
2. target guideline 稳定；
3. parser/eval 稳定；
4. pilot 数据质量可接受；
5. A/B/C 支持 Unit DSL 作为主接口。
```

### 6.3 推荐数据规模

```text
800–1200 train
100 dev
100 locked gold
```

如果时间紧：

```text
500 train
80 dev
100 locked gold
```

但最终简历版建议接近 1000 train。

### 6.4 Context 5 允许做什么

```text
1. 创建 data/v05/train.jsonl；
2. 创建 data/v05/dev.jsonl；
3. 创建 data/v05/gold.jsonl；
4. 创建 SFT message format；
5. 创建 train/train_lora.py；
6. 创建 train/infer.py；
7. 创建 train/configs/*.yaml；
8. 使用 Hugging Face + PEFT；
9. 跑 LoRA/SFT；
10. 跑 eval；
11. 生成 reports/v05/training_report.md；
12. 生成 reports/v05/bad_case_analysis.md。
```

### 6.5 Context 5 禁止做什么

```text
1. 不要改 DSL；
2. 不要新增 target；
3. 不要做 MemoryOS；
4. 不要接真实 retriever；
5. 不要做 writer update/merge；
6. 不要把训练数据从 v0.3 机械转换；
7. 不要只看 loss，不做 routing metrics；
8. 不要把训练失败包装成成功。
```

### 6.6 推荐 baseline

```text
heuristic
top-k READ
zero-shot small model
few-shot small model
teacher LLM
LoRA small router
```

### 6.7 v0.5 完成标准

```text
1. training pipeline 跑通；
2. inference 输出可被 strict parser 消费；
3. dev/gold eval 跑通；
4. 有 baseline comparison；
5. 有 error analysis；
6. 有训练配置记录；
7. 有可写进简历的结果表；
8. CURRENT_STATE.md 更新。
```

---

## 7. Context 6：v1.0 Packaging Context

### 7.1 Context 6 目标

把项目整理成简历级、GitHub 可展示、面试可讲的 research-engineering 项目。

### 7.2 允许做什么

```text
1. 整理 README.md；
2. 整理 docs；
3. 整理 reports；
4. 做 demo_cli；
5. 写 limitations；
6. 写 future work；
7. 写 resume bullets；
8. 写 interview notes；
9. 清理不必要临时文件；
10. 保留 v0.3 archive 叙事。
```

### 7.3 禁止做什么

```text
1. 不要在 packaging 阶段重新设计核心接口；
2. 不要临时加新 target；
3. 不要为了 demo 做假结果；
4. 不要隐藏失败案例；
5. 不要把项目包装成完整 MemoryOS；
6. 不要删掉 v0.3 作为历史证据。
```

### 7.4 v1.0 最终交付

```text
README.md
docs/
data samples
src/v04/
train/
reports/v04/
reports/v05/
demo/
resume bullets
interview notes
```

---

## 8. 后续阶段总检查点

每个 checkpoint 必须回来给 ChatGPT 做 steering review。

### Checkpoint P4

提交：

```text
pilot_cases.jsonl
pilot_data_report.md
validator result
CURRENT_STATE.md
git status
known ambiguity
```

审查重点：

```text
pilot 是否质量稳定；
是否可以进入 eval；
target 是否失控；
case 是否模板化。
```

### Checkpoint P5

提交：

```text
prompts
metrics.py
eval_runner
interface_pilot_report
error_analysis
CURRENT_STATE.md
git status
```

审查重点：

```text
A/B/C 是否公平；
指标是否正确；
Unit DSL 是否有证据；
是否进入 v0.5。
```

### Checkpoint v0.5 data before training

提交：

```text
train/dev/gold split
SFT format
prompt template
data distribution
sample records
```

审查重点：

```text
数据是否泄漏；
target 分布是否合理；
SFT 格式是否正确；
gold 是否锁定。
```

### Checkpoint v0.5 result

提交：

```text
training report
baseline comparison
eval metrics
bad cases
model config
```

审查重点：

```text
是否真的有提升；
是否过拟合；
是否能写进简历；
是否需要补实验。
```

### Checkpoint v1.0

提交：

```text
README
reports
demo
resume bullets
interview notes
```

审查重点：

```text
叙事是否可信；
是否夸大；
项目是否清晰；
是否贴岗位。
```

---

## 9. 后续 prompt 设计原则

给 Codex 的每个新 prompt 都必须包含：

```text
1. 当前 context 编号和唯一职责；
2. 必须先读哪些文件；
3. 本轮允许做什么；
4. 本轮禁止做什么；
5. 完成标准；
6. 必须更新 CURRENT_STATE.md；
7. 最终报告格式；
8. 明确停止点。
```

不要给 Codex 模糊任务，例如：

```text
继续做下一步。
帮我完善项目。
把 v0.4 做完。
```

应该写：

```text
本 context 只做 P4 pilot dataset。
不要写 eval runner。
完成后停止。
```

---

## 10. 重点风险清单

后续最容易跑偏的地方：

```text
1. Codex 顺手写 eval runner / prompts / training；
2. pilot 数据扩得太快，语义质量下降；
3. target 混淆但 validator 看不出来；
4. project_memory 被用成 catch-all；
5. service_memory 和 task_state 边界变模糊；
6. sensitive/private 内容被误 STORE；
7. v0.3 数据被机械转换；
8. parser 被改成会 semantic repair；
9. A/B/C 比较变量不干净；
10. v0.5 只做训练 loss，不做 routing eval；
11. README 夸大成 MemoryOS。
```

对应控制方法：

```text
1. 每阶段必须暂停 review；
2. 数据扩展前先看分布和人工样例；
3. report 中必须列 target ambiguity；
4. parser strict 不变；
5. v0.3 只做历史证据和 hard case inspiration；
6. 训练前必须锁 dev/gold；
7. 最终报告保留 limitations。
```

---

## 11. 求职叙事保护

最终简历项目应表达为：

```text
面向 Coding / Business Agent 的轻量 Memory Policy Router：
在 fixed candidate memories 和 current units 下，
训练小模型输出 READ / STORE / SKIP DSL，
用于筛选上下文记忆、控制长期记忆写入并减少无关 memory 污染。
```

不要表达成：

```text
我做了一个 MemoryOS。
我做了完整 agent 记忆系统。
我做了完整 RAG 系统。
```

推荐简历 bullet：

```text
- 设计并实现面向 Coding/Business Agent 的轻量 Memory Policy Router，将旧 JSON/span 输出重构为 unit-based READ/STORE/SKIP DSL，并通过 strict parser 转换为 canonical JSON。
- 构建 v0.4 interface pilot，对比 Legacy Span JSON、Unit JSON、Unit DSL 三种接口，评估 parse success、invalid ID rate、READ F1、STORE target accuracy、false store rate 等指标。
- 基于 Hugging Face + PyTorch + LoRA/SFT 微调小模型 router，与 heuristic、zero-shot、teacher LLM baseline 对比，并完成 bad case analysis。
```

---

## 12. Self-Check

本计划自检如下：

```text
[OK] 明确承认 P0–P3 已完成。
[OK] 明确 P3 bridge set 是 accepted bridge，不是 locked gold。
[OK] 明确后续 Codex contexts 分工。
[OK] 每个 context 都有允许 / 禁止 / 完成标准。
[OK] 保持 5 个 target，不新增 taxonomy。
[OK] 保持 strict parser，不做 semantic repair。
[OK] 明确不做 MemoryOS / retriever / writer / LLM unitizer。
[OK] 把 P3 发现的 service_memory vs task_state 边界写入后续规则。
[OK] 保护 v0.3 作为历史资产和设计证据。
[OK] 明确后续必须回 ChatGPT 做 steering review。
[OK] 兼顾求职目标：v0.5 需要 LoRA/SFT 和 eval 结果。
[OK] 没有要求 Codex 一口气做完 v0.4/v0.5/v1.0。
```

如果后续阶段与本计划冲突，以最新人工 review 结论为准，并应更新本文件。
