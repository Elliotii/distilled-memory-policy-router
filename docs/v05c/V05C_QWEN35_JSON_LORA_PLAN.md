# V0.5c Qwen3.5 Unit JSON LoRA Plan

> 文件定位：v0.5c experiment plan — Qwen3.5 Unit JSON LoRA（模型容量消融实验）
> 作用：给后续 Codex contexts 作为实验路线参考
> 状态：Plan — 可行性验证完成，等待 125-case 冒烟训练

---

## 1. 实验动机

V0.5b Unit JSON LoRA 在 Qwen3-4B 上证明了：
- JSON SFT > DSL SFT（目标准确率 +19.8pp on gold）
- JSON SFT > JSON few-shot on same model（精确匹配 +5pp）
- 但仍落后于 Qwen3.5 JSON few-shot（精确匹配差 11pp）

核心问题：更强的基座模型 + Unit JSON SFT 能否缩小甚至超越 Qwen3.5 few-shot？

## 2. 实验定义

| 维度 | 内容 |
|------|------|
| 研究问题 | Qwen3.5 + Unit JSON QLoRA 能否缩小与 Qwen3.5 JSON few-shot 的差距，或超越？ |
| 控制变量 | Unit JSON 接口、125/250/500 训练子集、dev/gold 数据、QLoRA 超参数 |
| 改变变量 | 基座模型：Qwen3-4B → Qwen3.5-4B |
| 评估指标 | parse, exact, READ F1, STORE F1, target acc, SKIP F1, sensitive |
| 成功标准 | Tier A: 超越 Qwen3.5 JSON fs；Tier B: 超越 Qwen3-4B JSON LoRA 500 |

## 3. 当前可行性状态

- ✅ 模型存在：`/home/abc16/hf_models/Qwen3.5-4B` (8.8 GB)
- ✅ GPU 足够：RTX 4070 12GB，4-bit QLoRA 预估 8-10 GB
- ✅ transformers 5.9.0 原生支持 qwen3_5
- ✅ 配置文件已创建：`configs/v05c/qwen35_lora_json_{125,250,500}.yaml`
- ✅ 训练/评估脚本兼容（AutoModel + trust_remote_code）
- ✅ gold 锁定且未损坏（hash: `56e16078...`）
- ✅ 单元测试 77/77 通过

## 4. 架构差异注意事项

Qwen3.5-4B 与 Qwen3-4B 的架构差异较大：
- 混合注意力：24 层 linear_attn + 8 层 full_attn（Qwen3-4B: 36 层全 full_attn）
- LoRA 目标模块需要扩展：增加了 `in_proj_qkv` 和 `out_proj` 以覆盖 linear_attn 层
- 总可训练参数略少：~3.2M vs ~5.8M（因层数更少且 linear_attn 合并了 QKV 投影）

## 5. 数据策略

- 训练数据：复用 v0.5b 的 JSON SFT 文件（不重新标注、不重新生成）
- Dev 数据：复用 v0.5b dev JSON SFT（所有开发决策用 dev）
- Gold 数据：锁定，仅最终评估用（已评估过 2 次，非完全盲测）
- 数据不修改、不扩展、不重新标注

## 6. 实验阶段

| 阶段 | Context | 内容 |
|------|---------|------|
| 1 — 规划 | 5.9-A（本轮） | 可行性、配置、就绪报告 |
| 2 — 冒烟 | 5.9-B | 训练 125，dev 评估，决策 |
| 3 — 扩展 | 5.9-C | 若冒烟通过，训练 250 |
| 4 — 扩展 | 5.9-D | 若 250 通过，训练 500 |
| 5 — 金标 | 5.9-E | locked-gold 最终评估 |

## 7. 相关文档

- `reports/v05c/v05c_qwen35_json_lora_plan.md` — 详细实验计划
- `reports/v05c/v05c_qwen35_model_feasibility_report.md` — 模型可行性报告
- `reports/v05c/v05c_qwen35_json_lora_config_report.md` — 配置报告
- `reports/v05c/v05c_train_dev_gold_usage_policy.md` — 数据使用策略
- `reports/v05c/v05c_qwen35_json_lora_readiness_report.md` — 就绪报告

---

*End of V0.5c Qwen3.5 Unit JSON LoRA Plan.*
