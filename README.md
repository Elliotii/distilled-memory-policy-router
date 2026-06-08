# Lightweight Memory Policy Router for Coding/Business Agents

This project builds and evaluates a small memory-policy router for agent memory pipelines. Given fixed candidate memories and current units from a coding or business-agent context, the router predicts which memories to READ, which current units to STORE, which units to SKIP, and which memory target should receive each stored unit. The goal is a narrow policy layer that reduces memory pollution and context waste without pretending to be a retriever, memory database, writer, or complete agent framework.

## Highlights

- Unit-level READ / STORE / SKIP formulation for fixed candidate memories and current units.
- Locked `gold_v2_009` evaluation with 150 controlled cases.
- QLoRA and BF16 LoRA comparison on Qwen-family ~4B routers.
- Best evaluated system: BF16 standard LoRA r16 with 1000 targeted-balanced training cases under RTX 4090 fallback settings.
- Best gold result: 36.0% exact, 99.0% STORE F1, 98.1% SKIP F1, and 100.0% STORE target accuracy.
- Main limitation: READ selection remains the full-exact bottleneck at 84.6% F1.

## Problem

Long-running coding and business agents need durable memory, but indiscriminate memory use creates two problems:

- Context pressure: injecting every candidate memory wastes prompt budget and can distract the answerer.
- Memory pollution: storing temporary failures, stale facts, secrets, or casual chatter makes future sessions worse.

This project studies the control-plane decision before memory is injected or written. The router does not retrieve from an unbounded store and does not rewrite memories. It decides which already-supplied candidates are useful now, and which current units should be stored or skipped.

## What This Project Does

| Does | Does Not Do |
| --- | --- |
| Predict READ / STORE / SKIP policy decisions | Build a complete Memory OS |
| Route fixed candidate memories into or out of context | Implement retrieval over an unbounded memory store |
| Classify stored units into five memory targets | Implement a memory database |
| Evaluate small-model routing quality on locked data | Rewrite, merge, deduplicate, or delete memories |
| Measure memory-pollution signals such as false stores and irrelevant reads | Provide a full RAG system |
| Preserve predictions, metrics, reports, and configs for reproducibility | Provide an end-to-end agent framework |
| Document limitations and failure modes | Claim production safety |

## Architecture At A Glance

```text
candidate memories + current units
        |
        v
small memory policy router
        |
        v
READ / STORE / SKIP decisions
        |
        +--> context builder reads selected candidate memories
        |
        +--> memory writer stub receives selected STORE units
```

The v0.3 project spec explored a JSON/span contract with `read_hints`, `write_spans`, and `ignore_spans`. Later v0.4/v0.5 work converged on a unit-based READ / STORE / SKIP formulation because it gave the small model a lower-entropy output space and made evaluation more stable. The v0.5 training and evaluation artifacts use Unit JSON, not a raw-span runtime or complete DSL system.

## Task Formulation

Input:

- Fixed candidate memories, each with an ID and text.
- Current units extracted from the current task or dialogue context.

Output:

- READ: candidate memory IDs to inject into context.
- STORE: current unit IDs that should become durable memory.
- SKIP: current unit IDs that should not become durable memory.
- STORE target: one of the five target classes below for every stored unit.

Valid STORE targets:

- `task_state`: current progress, blockers, next steps, and task-local state.
- `service_memory`: durable facts about a service, module, component, or subsystem.
- `repo_memory`: repository conventions, paths, commands, tests, and codebase facts.
- `project_memory`: cross-repo project decisions, goals, and shared constraints.
- `user_profile`: stable, non-sensitive user preferences that transfer across work.

Primary metrics:

- Exact target match.
- Parse success.
- READ precision / recall / F1.
- STORE-unit precision / recall / F1.
- SKIP-unit precision / recall / F1.
- STORE target accuracy.
- False store rate, irrelevant read rate, and sensitive store rate.

## Results

The main locked evaluation is `gold_v2_009`, a controlled 150-case benchmark. The strongest v0.5g result is BF16 standard LoRA r16 with 1000 targeted-balanced training cases, run under RTX 4090 fallback settings.

### gold_v2_009 Comparison

| System | Exact | Parse | READ F1 | STORE F1 | SKIP F1 | Target Acc | False Store |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3.5 JSON few-shot | 30.7% | 86.0% | n/a | 85.6% | 84.7% | 75.3% | n/a |
| Qwen3.5 QLoRA r16 500 | 22.7% | 94.7% | n/a | 90.9% | 89.2% | 84.2% | n/a |
| BF16 r16 500_4090 | 16.7% | 98.7% | 80.1% | 89.2% | 84.0% | 84.7% | 10.4% |
| BF16 r16 1000_4090 | 36.0% | 99.3% | 84.6% | 99.0% | 98.1% | 100.0% | 1.2% |

### BF16 500 vs 1000

| Split | System | Exact | Parse | READ F1 | STORE F1 | SKIP F1 | Target Acc | Irrelevant Read | Sensitive Store |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dev | BF16 r16 500_4090 | 49.0% | 100.0% | 92.0% | 96.7% | 81.0% | 85.3% | 11.4% | 2/3 |
| Dev | BF16 r16 1000_4090 | 59.0% | 100.0% | 93.3% | 97.1% | 83.1% | 89.5% | 10.5% | 2/3 |
| Gold | BF16 r16 500_4090 | 16.7% | 98.7% | 80.1% | 89.2% | 84.0% | 84.7% | 10.0% | 0/4 |
| Gold | BF16 r16 1000_4090 | 36.0% | 99.3% | 84.6% | 99.0% | 98.1% | 100.0% | 15.5% | 0/4 |

## Key Findings

1. The 1000-targeted BF16 LoRA r16 variant is the best evaluated system on locked `gold_v2_009` by exact match and write-side routing metrics among the compared systems; READ F1 was not available for older v0.5e anchors.
2. BF16 alone is not sufficient: the 500-control BF16 run trails the older QLoRA r16 500 run on gold exact match.
3. The largest gains are write-side routing gains: STORE F1, SKIP F1, STORE target accuracy, and false-store reduction.
4. READ remains the main full-exact bottleneck: the best run still has 64 false-positive reads and 63 missed reads on gold.
5. The result supports a small policy layer for controlled memory routing research, not a deployment claim.

## Quickstart / Repository Navigation

This README does not promise live model inference. The model adapters are excluded from git and preserved in external artifact backup.

Useful entry points:

```text
docs/PROJECT_OVERVIEW.md
docs/RESULTS.md
docs/v05g/V05G_BF16_LORA_4090_FINAL_RESULTS.md
docs/v10/V10_PACKAGING_EXECUTION_PLAN.md
reports/v05g/
reports/v05g/server_runs/
data/v05g/model_predictions/
configs/v05g/
```

Useful local checks:

```bash
python3 -m json.tool reports/v05g/server_runs/v05g_bf16_r16_1000_4090_gold_v2_009_metrics.json >/dev/null
wc -l data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl
shasum -a 256 data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl
```

Expected gold hash:

```text
f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72
```

## Demo

A no-inference replay demo is available under `demo/`. It uses small fixtures extracted from locked gold and saved prediction artifacts; it does not load a model, run retrieval, call APIs, or prove downstream task success.

```bash
python3 demo/run_demo.py --list
python3 demo/run_demo.py --case demo/cases/case_001.json
```

See [demo/README.md](demo/README.md) for the fixture list and commands.

A downstream-lite context-efficiency proxy is documented in [docs/DOWNSTREAM_LITE_BENCHMARK.md](docs/DOWNSTREAM_LITE_BENCHMARK.md). A tiny LLM downstream-lite micro-pilot is documented in [docs/LLM_DOWNSTREAM_LITE_BENCHMARK.md](docs/LLM_DOWNSTREAM_LITE_BENCHMARK.md) and summarized in [reports/v10/v10_benchmark_synthesis.md](reports/v10/v10_benchmark_synthesis.md).

## Reproducibility

- Locked evaluation file: `data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl`.
- Locked gold hash: `f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72`.
- Prediction files: `data/v05g/model_predictions/bf16_r16_*_4090_*.jsonl`.
- Metrics files: `reports/v05g/server_runs/v05g_bf16_r16_*_4090_*.json`.
- Training configs: `configs/v05g/qwen35_bf16_lora_json_r16_*_4090.yaml`.
- Server snapshot: `v0.5g-bf16-lora-4090-ready / 7e40f02bbb34c2c5ecf8f7468a066cba0105db4d`.
- Adapter weights are excluded from git by `.gitignore` and preserved in external artifact backup.

## Limitations

- The benchmark is controlled and synthetic.
- Candidate memories are fixed; this project does not evaluate retrieval from a live memory store.
- The router does not rewrite, merge, deduplicate, delete, or verify memories.
- A tiny 14-response downstream-lite LLM micro-pilot has been run, but it is diagnostic only and does not prove downstream utility.
- READ selection is not solved and remains the main exact-match bottleneck.
- Sensitive-store behavior is promising on gold but not enough for a safety claim.
- Results come from a single model family and a single locked gold set.
- The v0.5g run used RTX 4090 fallback settings, so results should not be described as a different hardware setting.

## Roadmap

Next v1.0 packaging steps:

- Architecture and task-formulation documentation.
- Demo fixtures that show the input/output shape without model inference.
- Downstream-lite efficiency proxy over existing predictions and labels.
- An execution-ready LLM downstream-lite prompt pack is documented in [docs/LLM_DOWNSTREAM_LITE_BENCHMARK.md](docs/LLM_DOWNSTREAM_LITE_BENCHMARK.md).
- A 2-case, 7-strategy, 14-response DeepSeek V4 Flash micro-pilot has been executed and internally reviewed; the full 42-prompt pilot remains future work.
- Resume and interview notes with conservative claims.
- Final audit before a v1.0 tag.

## License / Status

No license file is present in this repository at the time of this v1.0 README draft. Treat the project status as research-engineering packaging in progress, not a released product.
