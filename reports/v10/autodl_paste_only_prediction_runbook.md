# AutoDL Paste-Only v0.5g Prediction Runbook

## 边界

本流程不用 `scp`，因为当前上下文只假设可以交互式 SSH 登录，不能依赖文件复制通道可用。

本流程不用 GitHub SSH，也不依赖 AutoDL 上的仓库同步；要运行的脚本和 32 条输入已经打包进 `reports/v10/autodl_v05_prediction_paste_bundle.sh`。

密码只在 SSH 提示符里手动输入，不写入文件、不放进脚本、不放进报告。

## 登录 AutoDL

【AutoDL登录命令】

```bash
ssh -p 43824 root@connect.nmb1.seetacloud.com
```

出现密码提示时，在终端里手动输入密码。不要把密码粘贴进任何文件或脚本。

## 可选：手动指定模型路径

如果自动发现失败，先在 AutoDL 终端执行：

```bash
export DMPR_BASE_MODEL="【AutoDL上Qwen base model路径，如果自动发现失败再填】"
export DMPR_V05G_ADAPTER="【AutoDL上v0.5g LoRA adapter路径，如果自动发现失败再填】"
```

如果只找到一个合理的 Qwen base model 和一个 LoRA adapter，bundle 会自动设置这两个环境变量。找到多个候选时会停止并输出 blocker report，不会猜路径。

## 粘贴运行 bundle

在 Mac 上打开并复制整个文件内容：

```bash
reports/v10/autodl_v05_prediction_paste_bundle.sh
```

把完整内容粘贴到已登录的 AutoDL 终端并回车。bundle 会创建：

```text
~/dmpr_v05_offline_prediction
```

它只会重建 runner 和 32 条 rendered inputs，然后在 AutoDL 本地路径存在时运行离线预测。

## 带回结果

运行结束后，AutoDL 终端会打印：

```text
BEGIN_DMPR_AUTODL_RESULT_B64
...
END_DMPR_AUTODL_RESULT_B64
```

把包含 BEGIN/END 的整段文本复制回 Mac，保存到：

```text
data/v10/learned_router_eval/autodl_result_block.txt
```

然后在 Mac repo 根目录运行：

```bash
python3 scripts/import_autodl_v05_prediction_result.py \
  --input-b64 data/v10/learned_router_eval/autodl_result_block.txt \
  --repo-root .
```

## Mac 回放评估

如果导入后存在真实预测：

```text
data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl
```

运行：

```bash
python3 apps/memory_harness/eval_hard_read.py \
  --cases data/v10/hard_read_v2_expanded/hard_read_v2_expanded_cases.jsonl \
  --memory-pool data/v10/hard_read_v2_expanded/hard_read_v2_expanded_memory_pool.jsonl \
  --strategies replay_learned_router \
  --replay-predictions data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl \
  --top-k 4 \
  --max-context-chars 1600 \
  --out-dir reports/v10/hard_read_v2_expanded_learned_router_selection_eval
```

只有 `source` 字段等于 `v0.5g_offline_batch_prediction` 的导入结果才算 learned-router 回放输入。debug replay fixture 不能当成 learned-router 性能。

## 安全策略

不要复制模型权重、adapter、`.env`、SSH 文件、密码、token 或 private key。结果包只允许包含预测 JSONL、run report、blocker report 和 probe report。负面结果要如实报告，不调整 fixture 或标签来让 learned-router 胜出。
