# Desktop Qwen Handoff

Status: Context 4.5 Mac closeout  
Audience: WSL / Pi agent on the RTX 4070 SUPER desktop  
Scope: prepare and run a later Qwen matched comparison for v0.4 A/B/C prompts

## 1. 当前项目阶段

当前主线仍是：

```text
v0.4 unit-based READ / STORE / SKIP DSL interface pilot
```

已完成阶段：

- P0-P2.5 foundation:
  - v0.4 spec / planning docs;
  - strict DSL parser;
  - case schema;
  - case validator;
  - parser / validator tests.
- P3 bridge cases:
  - formal 40-case bridge set;
  - bridge report.
- P4 / P4.1 pilot dataset:
  - 200 pilot cases;
  - semantic audit and pilot reports.
- P5 / P5.1 evaluation harness:
  - A/B/C interfaces;
  - external prediction JSONL support;
  - metrics and error reports.
- P5.5 DeepSeek model-output collection:
  - 5-case smoke and retry diagnosis;
  - 30-case DeepSeek-compatible subset;
  - subset30 error audit;
  - 50-case DeepSeek-compatible subset.

P5.5 当前产物的核心文件：

- `data/v04/model_predictions/p5_subset50_case_ids.txt`
- `data/v04/model_predictions/p5_subset50_cases.jsonl`
- `data/v04/model_predictions/p5_subset50_predictions.jsonl`
- `reports/v04/model_output_subset50_report.md`
- `reports/v04/model_output_subset50_interface_report.md`
- `reports/v04/model_output_subset50_error_analysis.md`

## 2. 当前结论

- DeepSeek V4 Flash-compatible line 先停在 50-case subset。
- 下一步不是 v0.5 training。
- 下一步是台式机 Qwen matched comparison。
- Pilot data 仍不是 training locked gold。
- Qwen comparison 应使用同一 50-case subset、同一 A/B/C prompts、同一 eval_runner。
- 不要把 DeepSeek 50-case 或后续 Qwen 50-case 结果直接写成最终正式结论。

DeepSeek 50-case 简表：

| Interface | Parse success | Exact match | READ F1 | STORE unit F1 | STORE target acc | SKIP F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `legacy_span_json` | 96.0% | 48.0% | 0.872 | 0.864 | 92.6% | 0.832 |
| `unit_json` | 96.0% | 50.0% | 0.845 | 0.870 | 94.7% | 0.844 |
| `unit_dsl` | 100.0% | 42.0% | 0.839 | 0.872 | 93.1% | 0.847 |

Key observations:

- `unit_dsl` continued to have the strongest structural stability.
- `unit_json` had the highest exact match in the DeepSeek 50-case subset, but it also had recurring empty-after-retry rows.
- `legacy_span_json` still showed JSON/span-copying fragility.
- `project_memory` vs `task_state` remains the main target-boundary issue.
- Sensitive store stayed at 0.0% across all three interfaces.

## 3. 台式机已知环境

Known desktop information:

| Item | Value |
| --- | --- |
| Windows user | `C:\Users\abc16` |
| WSL user | `abc16` |
| WSL | Ubuntu 24.04.4 LTS / WSL2 |
| WSL repo | `/home/abc16/distilled-memory-policy-router` |
| WSL venv | `/home/abc16/distilled-memory-policy-router/.venv` |
| GPU | RTX 4070 SUPER, about 12GB VRAM |
| Qwen3-4B local model | `/home/abc16/hf_models/Qwen3-4B-Instruct-2507` |

旧 smoke 经验：

- Qwen3-4B 在 v0.3 JSON/span schema 上 parse success 6/20。
- 语义有时合理，但 schema 输出脆弱。
- v0.4 A/B/C comparison 应重点验证 Unit JSON / Unit DSL 是否改善小模型结构稳定性。

## 4. Desktop Context 4.6-A 职责

Context 4.6-A 只做 readiness check，不跑模型。

必须检查：

- repo sync:
  - `git status`
  - `git pull` or equivalent sync confirmation, if owner allows;
  - confirm Mac-generated v0.4 files exist after sync.
- v0.4 files:
  - planning docs;
  - v0.4 specs;
  - prompts;
  - `src/v04`;
  - `tests/v04`;
  - subset50 case files;
  - DeepSeek reports.
- Python environment:
  - `.venv` exists at `/home/abc16/distilled-memory-policy-router/.venv`;
  - Python executable is from the venv;
  - no accidental system Python run.
- GPU:
  - `nvidia-smi`;
  - CUDA visible from WSL;
  - GPU is RTX 4070 SUPER.
- Python packages:
  - `torch`;
  - CUDA availability through torch;
  - `transformers`;
  - tokenizer/model loading dependencies already present.
- Local model path:
  - `/home/abc16/hf_models/Qwen3-4B-Instruct-2507` exists;
  - contains expected Hugging Face files;
  - do not download during readiness unless owner explicitly approves.
- Data/eval:
  - can read `data/v04/model_predictions/p5_subset50_cases.jsonl`;
  - can run `src.v04.eval_runner` on an existing prediction file or deterministic harness without model inference.

4.6-A 禁止：

- 不要调用 Qwen。
- 不要生成 prediction JSONL。
- 不要训练。
- 不要下载大模型。
- 不要安装大型依赖，除非 owner 明确确认。
- 不要改 prompts / pilot / bridge / parser / validator / metrics / eval_runner。

## 5. Desktop Context 4.6-B 职责

Only after 4.6-A passes:

- Run Qwen3-4B local inference.
- Use the same 50-case subset:
  - `data/v04/model_predictions/p5_subset50_case_ids.txt`
  - `data/v04/model_predictions/p5_subset50_cases.jsonl`
- Use the same three prompt templates:
  - `prompts/v04/legacy_span_json.txt`
  - `prompts/v04/unit_json.txt`
  - `prompts/v04/unit_dsl.txt`
- Generate a Qwen external prediction JSONL, for example:
  - `data/v04/model_predictions/qwen3_4b_subset50_predictions.jsonl`
- Use the same required prediction fields:
  - `case_id`
  - `interface`
  - `system`
  - `raw_output`
- Suggested system name:
  - `qwen3_4b_subset50`
- Evaluate with the existing eval_runner:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m src.v04.eval_runner \
  --cases data/v04/model_predictions/p5_subset50_cases.jsonl \
  --predictions data/v04/model_predictions/qwen3_4b_subset50_predictions.jsonl \
  --report reports/v04/qwen3_4b_subset50_interface_report.md \
  --error-report reports/v04/qwen3_4b_subset50_error_analysis.md
```

Generate a report such as:

```text
reports/v04/qwen3_4b_subset50_report.md
```

The report should compare Qwen against the DeepSeek 50-case baseline without treating either as final proof.

4.6-B 禁止：

- 不训练。
- 不生成 v0.5 train/dev/gold。
- 不改 prompts。
- 不改 pilot/bridge data。
- 不改 parser / validator / metrics / eval_runner。
- 不把 Qwen 结果直接写成最终结论。

## 6. 后续 Qwen3.5

- Qwen3.5 同级小模型只在 Qwen3-4B subset50 跑通后再考虑。
- Readiness 阶段不要下载大模型。
- 不要自动安装大型依赖。
- 如果需要 Qwen3.5 模型下载或依赖安装，先停下并向 owner 明确说明：
  - model size;
  - disk use;
  - expected VRAM;
  - dependency changes;
  - exact command;
  - rollback/cleanup expectation.

## 7. 重要边界

严格禁止：

- 不要训练。
- 不要生成 v0.5 train/dev/gold。
- 不要改 prompts。
- 不要改 `data/v04/pilot_cases.jsonl`。
- 不要改 `data/v04/bridge_cases.jsonl`。
- 不要改 parser / validator / metrics / eval_runner。
- 不要实现 retriever / writer / MemoryOS。
- 不要新增 STORE target。
- 不要新增 type / subtype / reason / entity。
- 不要把 Qwen 结果直接写成最终正式结论。
- 不要把 pilot data 当成 locked training gold。

Allowed target set remains exactly:

```text
user_profile
project_memory
repo_memory
service_memory
task_state
```

## 8. 必须复用的文件

Desktop Qwen comparison must reuse:

- `data/v04/model_predictions/p5_subset50_case_ids.txt`
- `data/v04/model_predictions/p5_subset50_cases.jsonl`
- `prompts/v04/legacy_span_json.txt`
- `prompts/v04/unit_json.txt`
- `prompts/v04/unit_dsl.txt`
- `docs/v04_spec/PREDICTION_FORMAT.md`
- `src/v04/model_output_runner.py`
- `src/v04/eval_runner.py`
- `src/v04/metrics.py`
- `reports/v04/model_output_subset50_report.md`

Also useful:

- `reports/v04/model_output_subset50_interface_report.md`
- `reports/v04/model_output_subset50_error_analysis.md`
- `reports/v04/model_output_subset30_error_review.md`
- `reports/v04/deepseek_empty_output_diagnosis.md`

## 9. Agent 使用建议

- Qwen / CUDA / Python / eval_runner commands should run inside WSL.
- 推荐使用 WSL 内 Pi agent 执行 Context 4.6-A / 4.6-B。
- Windows Claude Code 只适合外层辅助、查看文件、整理文本。
- 如果使用 Windows Claude Code，所有项目命令必须通过 WSL shell 执行。
- 不要从 Windows path 直接混跑 Python、CUDA、venv 或 model loading。
- Keep outputs in repo-relative v0.4 paths under WSL.
- Do not copy secrets, `.env`, model weights, venv, or caches into git.

## 10. Context 4.6-A Suggested Closeout

4.6-A 完成后应报告：

- repo sync status;
- venv status;
- torch/CUDA status;
- transformers status;
- local Qwen model path status;
- subset50 file existence and row counts;
- eval_runner dry-run or import status;
- blockers;
- whether 4.6-B model-output collection is safe to start.
