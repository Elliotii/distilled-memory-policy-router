# Memory Policy Router Demo

This is a no-inference replay demo for the Lightweight Memory Policy Router. It reads small JSON fixtures extracted from locked `gold_v2_009` cases and saved BF16 r16 1000_4090 prediction artifacts.

The demo shows:

```text
candidate memories + current units -> READ / STORE / SKIP decisions + targets
```

It does not run a live model. It does not load Qwen, use a GPU, train, retrieve from a memory store, write memory, prove downstream task success, or provide production safety evidence.

## Run

List available fixture cases:

```bash
python3 demo/run_demo.py --list
```

Replay one case:

```bash
python3 demo/run_demo.py --case demo/cases/case_001.json
python3 demo/run_demo.py --case demo/cases/case_002.json
python3 demo/run_demo.py --case demo/cases/case_003.json
```

Optionally write the comparison metrics to a chosen path:

```bash
python3 demo/run_demo.py --case demo/cases/case_001.json --json-out /tmp/dmpr_demo_case_001.json
```

## Cases

| Fixture | Source case | Purpose |
| --- | --- | --- |
| `demo/cases/case_001.json` | `v05e_gold_active_0002` | Exact-match READ + STORE/SKIP example. |
| `demo/cases/case_002.json` | `v05e_gold_active_0006` | READ bottleneck example with STORE/SKIP still correct. |
| `demo/cases/case_003.json` | `v05e_gold_active_0030` | STORE target routing across service and project targets. |

The fixture text is summarized from the original locked cases to keep the demo readable and avoid carrying incidental sensitive-looking literals. IDs and policy structures are preserved.

## Related Docs

- [Project README](../README.md)
- [Task formulation](../docs/TASK_FORMULATION.md)
- [Router example](../docs/ROUTER_EXAMPLE.md)
- [Results](../docs/RESULTS.md)

