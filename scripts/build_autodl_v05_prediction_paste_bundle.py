#!/usr/bin/env python3
"""Build a paste-only AutoDL shell bundle for v0.5g offline prediction."""

from __future__ import annotations

import argparse
import base64
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", required=True)
    parser.add_argument("--inputs", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def wrap_b64(value: str, width: int = 76) -> str:
    return "\n".join(value[i : i + width] for i in range(0, len(value), width))


def build_bundle(runner_path: Path, inputs_path: Path) -> str:
    runner_b64 = wrap_b64(b64_file(runner_path))
    inputs_b64 = wrap_b64(b64_file(inputs_path))
    return f"""#!/usr/bin/env bash
set -euo pipefail

WORKDIR="${{HOME}}/dmpr_v05_offline_prediction"
cd "${{HOME}}"
mkdir -p "${{WORKDIR}}/scripts" "${{WORKDIR}}/data/v10/learned_router_eval" "${{WORKDIR}}/reports/v10"
cd "${{WORKDIR}}"

cat > scripts/run_v05_router_offline_predictions.py.b64 <<'DMPR_RUNNER_B64'
{runner_b64}
DMPR_RUNNER_B64
python3 - <<'PY'
import base64
from pathlib import Path
Path("scripts/run_v05_router_offline_predictions.py").write_bytes(
    base64.b64decode(Path("scripts/run_v05_router_offline_predictions.py.b64").read_text())
)
Path("scripts/run_v05_router_offline_predictions.py.b64").unlink()
PY
chmod +x scripts/run_v05_router_offline_predictions.py

cat > data/v10/learned_router_eval/hard_read_v2_expanded_v05_router_inputs.jsonl.b64 <<'DMPR_INPUTS_B64'
{inputs_b64}
DMPR_INPUTS_B64
python3 - <<'PY'
import base64
from pathlib import Path
Path("data/v10/learned_router_eval/hard_read_v2_expanded_v05_router_inputs.jsonl").write_bytes(
    base64.b64decode(Path("data/v10/learned_router_eval/hard_read_v2_expanded_v05_router_inputs.jsonl.b64").read_text())
)
Path("data/v10/learned_router_eval/hard_read_v2_expanded_v05_router_inputs.jsonl.b64").unlink()
PY

PROBE_REPORT="reports/v10/autodl_probe_report.md"
BLOCKER_REPORT="reports/v10/v0_5g_offline_prediction_blocker_report.md"
RUN_REPORT="reports/v10/v0_5g_offline_prediction_run_report.md"
PREDICTIONS="data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl"

write_blocker() {{
  local reason="$1"
  {{
    echo "# v0.5g Offline Prediction Blocker Report"
    echo
    echo "- blocker: ${{reason}}"
    echo "- base_model_env_set: ${{DMPR_BASE_MODEL:+yes}}"
    echo "- adapter_env_set: ${{DMPR_V05G_ADAPTER:+yes}}"
    echo "- checked_on: AutoDL paste-only bundle"
    echo
    echo "Next action: manually export DMPR_BASE_MODEL and DMPR_V05G_ADAPTER with local AutoDL paths, then rerun this paste bundle. If model prediction remains blocked, run the minimal TF-IDF baseline while this path is unresolved."
  }} > "${{BLOCKER_REPORT}}"
}}

emit_result() {{
  local result_tar="dmpr_autodl_result.tar.gz"
  local files=()
  [[ -f "${{PREDICTIONS}}" ]] && files+=("${{PREDICTIONS}}")
  [[ -f "${{RUN_REPORT}}" ]] && files+=("${{RUN_REPORT}}")
  [[ -f "${{BLOCKER_REPORT}}" ]] && files+=("${{BLOCKER_REPORT}}")
  [[ -f "${{PROBE_REPORT}}" ]] && files+=("${{PROBE_REPORT}}")
  if [[ ${{#files[@]}} -eq 0 ]]; then
    write_blocker "no safe result files were produced"
    files=("${{BLOCKER_REPORT}}")
  fi
  tar -czf "${{result_tar}}" "${{files[@]}}"
  echo "BEGIN_DMPR_AUTODL_RESULT_B64"
  if base64 --help 2>&1 | grep -q -- "-w"; then
    base64 -w 76 "${{result_tar}}"
  else
    base64 "${{result_tar}}" | fold -w 76
  fi
  echo "END_DMPR_AUTODL_RESULT_B64"
}}

{{
  echo "# AutoDL Probe Report"
  echo
  echo "## GPU"
  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi || true
  else
    echo "nvidia-smi not found"
  fi
  echo
  echo "## Python Packages"
  python3 - <<'PY' || true
import importlib
for name in ("torch", "transformers", "peft"):
    try:
        mod = importlib.import_module(name)
        print(f"{{name}}={{getattr(mod, '__version__', 'unknown')}}")
    except Exception as exc:
        print(f"{{name}} unavailable: {{exc}}")
try:
    import torch
    print(f"cuda_available={{torch.cuda.is_available()}}")
    print(f"cuda_device_count={{torch.cuda.device_count()}}")
except Exception:
    pass
PY
}} > "${{PROBE_REPORT}}"

nvidia-smi || true
python3 - <<'PY' || true
import importlib
for name in ("torch", "transformers", "peft"):
    mod = importlib.import_module(name)
    print(name, getattr(mod, "__version__", "unknown"))
PY

discover_adapters() {{
  find /root "$HOME" /workspace /data /mnt /autodl-tmp /tmp -maxdepth 8 -type f -name adapter_config.json 2>/dev/null \\
    | while IFS= read -r cfg; do
        dir="$(dirname "$cfg")"
        [[ -f "$dir/adapter_model.safetensors" ]] && printf '%s\\n' "$dir"
      done \\
    | sort -u
}}

discover_bases() {{
  find /root "$HOME" /workspace /data /mnt /autodl-tmp /tmp -maxdepth 8 -type f -name config.json 2>/dev/null \\
    | while IFS= read -r cfg; do
        dir="$(dirname "$cfg")"
        if [[ -f "$dir/tokenizer_config.json" || -f "$dir/tokenizer.model" || -f "$dir/tokenizer.json" ]]; then
          printf '%s\\n' "$dir"
        fi
      done \\
    | grep -Ei 'qwen|Qwen|QWEN' \\
    | sort -u
}}

if [[ -n "${{DMPR_V05G_ADAPTER:-}}" ]]; then
  if [[ ! -d "${{DMPR_V05G_ADAPTER}}" ]]; then
    write_blocker "DMPR_V05G_ADAPTER is set but does not point to a directory"
    emit_result
    exit 0
  fi
else
  mapfile -t ADAPTER_CANDIDATES < <(discover_adapters)
  if [[ ${{#ADAPTER_CANDIDATES[@]}} -eq 1 ]]; then
    export DMPR_V05G_ADAPTER="${{ADAPTER_CANDIDATES[0]}}"
  elif [[ ${{#ADAPTER_CANDIDATES[@]}} -eq 0 ]]; then
    write_blocker "no LoRA adapter candidate found"
    emit_result
    exit 0
  else
    write_blocker "multiple LoRA adapter candidates found; set DMPR_V05G_ADAPTER manually"
    {{
      echo
      echo "## Adapter Candidates"
      printf '%s\\n' "${{ADAPTER_CANDIDATES[@]}}" | sed 's#^#- #'
    }} >> "${{BLOCKER_REPORT}}"
    emit_result
    exit 0
  fi
fi

if [[ -n "${{DMPR_BASE_MODEL:-}}" ]]; then
  if [[ ! -d "${{DMPR_BASE_MODEL}}" ]]; then
    write_blocker "DMPR_BASE_MODEL is set but does not point to a directory"
    emit_result
    exit 0
  fi
else
  mapfile -t BASE_CANDIDATES < <(discover_bases)
  if [[ ${{#BASE_CANDIDATES[@]}} -eq 1 ]]; then
    export DMPR_BASE_MODEL="${{BASE_CANDIDATES[0]}}"
  elif [[ ${{#BASE_CANDIDATES[@]}} -eq 0 ]]; then
    write_blocker "no Qwen-like base model candidate found"
    emit_result
    exit 0
  else
    write_blocker "multiple Qwen-like base model candidates found; set DMPR_BASE_MODEL manually"
    {{
      echo
      echo "## Base Model Candidates"
      printf '%s\\n' "${{BASE_CANDIDATES[@]}}" | sed 's#^#- #'
    }} >> "${{BLOCKER_REPORT}}"
    emit_result
    exit 0
  fi
fi

set +e
python3 scripts/run_v05_router_offline_predictions.py \\
  --inputs data/v10/learned_router_eval/hard_read_v2_expanded_v05_router_inputs.jsonl \\
  --out-predictions "${{PREDICTIONS}}" \\
  --out-report "${{RUN_REPORT}}" \\
  --base-model "${{DMPR_BASE_MODEL}}" \\
  --adapter "${{DMPR_V05G_ADAPTER}}" \\
  --max-new-tokens 256 \\
  --temperature 0
RUN_EXIT=$?
set -e
if [[ ${{RUN_EXIT}} -ne 0 ]]; then
  write_blocker "offline prediction runner exited with code ${{RUN_EXIT}}"
fi

emit_result
"""


def main() -> int:
    args = parse_args()
    runner_path = Path(args.runner)
    inputs_path = Path(args.inputs)
    out_path = Path(args.out)
    if not runner_path.exists():
        raise FileNotFoundError(runner_path)
    if not inputs_path.exists():
        raise FileNotFoundError(inputs_path)
    bundle = build_bundle(runner_path, inputs_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(bundle, encoding="utf-8")
    out_path.chmod(0o755)
    print(f"Wrote paste bundle to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
