#!/usr/bin/env python3
"""Import a copied AutoDL base64 result block into the local repo."""

from __future__ import annotations

import argparse
import base64
import io
import json
import re
import tarfile
from pathlib import Path


BEGIN = "BEGIN_DMPR_AUTODL_RESULT_B64"
END = "END_DMPR_AUTODL_RESULT_B64"
SOURCE = "v0.5g_offline_batch_prediction"
ALLOWED_PATHS = {
    "data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl",
    "reports/v10/v0_5g_offline_prediction_run_report.md",
    "reports/v10/v0_5g_offline_prediction_blocker_report.md",
    "reports/v10/autodl_probe_report.md",
}
FORBIDDEN_NAME_RE = re.compile(
    r"(safetensors|adapter_model|pytorch_model|model-\d+|\.bin$|\.pt$|\.pth$|\.gguf$|\.env$|id_rsa|known_hosts)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-b64", required=True)
    parser.add_argument("--repo-root", required=True)
    return parser.parse_args()


def extract_payload(text: str) -> bytes:
    if BEGIN not in text or END not in text:
        raise ValueError("Missing AutoDL result base64 markers")
    payload = text.split(BEGIN, 1)[1].split(END, 1)[0]
    compact = "".join(line.strip() for line in payload.splitlines() if line.strip())
    if not compact:
        raise ValueError("Empty AutoDL result payload")
    return base64.b64decode(compact, validate=True)


def validate_member(member: tarfile.TarInfo) -> str:
    name = member.name.lstrip("./")
    path = Path(name)
    if member.isdir():
        raise ValueError(f"Directory entries are not expected: {member.name}")
    if member.issym() or member.islnk():
        raise ValueError(f"Refusing archive link: {member.name}")
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe archive path: {member.name}")
    if name not in ALLOWED_PATHS:
        raise ValueError(f"Unexpected archive path: {member.name}")
    if FORBIDDEN_NAME_RE.search(name):
        raise ValueError(f"Forbidden model or secret artifact path: {member.name}")
    return name


def validate_predictions(path: Path) -> None:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 32:
        raise ValueError(f"Expected 32 prediction rows, found {len(rows)}")
    required = {"case_id", "selected_memory_ids", "parse_status", "rendered_input_hash"}
    for index, row in enumerate(rows, 1):
        missing = sorted(required - set(row))
        if missing:
            raise ValueError(f"Prediction row {index} missing keys: {missing}")
        if row.get("source") != SOURCE:
            raise ValueError(f"Prediction row {index} has unexpected source: {row.get('source')}")
        if not isinstance(row.get("selected_memory_ids"), list):
            raise ValueError(f"Prediction row {index} selected_memory_ids is not a list")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    block_path = Path(args.input_b64)
    archive_bytes = extract_payload(block_path.read_text(encoding="utf-8"))
    extracted: list[str] = []

    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
        members = tar.getmembers()
        if not members:
            raise ValueError("Archive is empty")
        safe_members: list[tuple[tarfile.TarInfo, str]] = []
        for member in members:
            safe_members.append((member, validate_member(member)))
        for member, name in safe_members:
            target = repo_root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            source = tar.extractfile(member)
            if source is None:
                raise ValueError(f"Could not read archive member: {member.name}")
            target.write_bytes(source.read())
            extracted.append(name)

    predictions = repo_root / "data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl"
    if predictions.exists() and "data/v10/learned_router_eval/hard_read_v2_expanded_v05_learned_router_predictions.jsonl" in extracted:
        validate_predictions(predictions)
        print("OK predictions imported and validated: 32 rows")
    else:
        print("No predictions imported; blocker/probe report import is allowed")
    for name in extracted:
        print(f"imported {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
