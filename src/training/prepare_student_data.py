"""Prepare student-router instruction data from frozen decision cases."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.llm_predict import build_messages
from src.schemas import DecisionCase, RouterTarget


DEFAULT_OUTPUT_DIR = Path("results/day7_student_data")


def compact_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))


def read_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            DecisionCase.model_validate(payload)
            cases.append(payload)
    return cases


def sft_record(case: dict[str, Any], source_path: Path) -> dict[str, Any]:
    messages = build_messages(case)
    messages.append({"role": "assistant", "content": compact_json(case["target"])})
    return {
        "case_id": case["case_id"],
        "split": case["split"],
        "category": case["category"],
        "domain": case["domain"],
        "difficulty": case["difficulty"],
        "source_path": str(source_path),
        "messages": messages,
        "target": case["target"],
    }


def prompt_record(case: dict[str, Any], source_path: Path) -> dict[str, Any]:
    return {
        "case_id": case["case_id"],
        "split": case["split"],
        "category": case["category"],
        "domain": case["domain"],
        "difficulty": case["difficulty"],
        "source_path": str(source_path),
        "messages": build_messages(case),
        "target": case["target"],
    }


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(compact_json(record) + "\n")


def stratified_smoke(records: list[dict[str, Any]], per_category: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen: dict[str, int] = defaultdict(int)
    for record in records:
        category = record["category"]
        if seen[category] >= per_category:
            continue
        selected.append(record)
        seen[category] += 1
    return selected


def category_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(record["category"] for record in records).items()))


def validate_sft_records(path: Path) -> tuple[int, Counter[str]]:
    count = 0
    categories: Counter[str] = Counter()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            record = json.loads(line)
            messages = record.get("messages")
            if not isinstance(messages, list) or len(messages) != 3:
                raise ValueError(f"{path}:{line_number}: expected 3 messages")
            if [message.get("role") for message in messages] != ["system", "user", "assistant"]:
                raise ValueError(f"{path}:{line_number}: unexpected message roles")
            assistant_payload = json.loads(messages[-1]["content"])
            RouterTarget.model_validate(assistant_payload)
            if assistant_payload != record["target"]:
                raise ValueError(f"{path}:{line_number}: assistant target differs from target")
            categories[record["category"]] += 1
            count += 1
    return count, categories


def validate_prompt_records(path: Path) -> tuple[int, Counter[str]]:
    count = 0
    categories: Counter[str] = Counter()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            record = json.loads(line)
            messages = record.get("messages")
            if not isinstance(messages, list) or len(messages) != 2:
                raise ValueError(f"{path}:{line_number}: expected 2 messages")
            if [message.get("role") for message in messages] != ["system", "user"]:
                raise ValueError(f"{path}:{line_number}: unexpected message roles")
            RouterTarget.model_validate(record["target"])
            categories[record["category"]] += 1
            count += 1
    return count, categories


def build_manifest(
    *,
    train_path: Path,
    dev_path: Path,
    gold_path: Path,
    output_paths: dict[str, Path],
    train_cases: list[dict[str, Any]],
    dev_cases: list[dict[str, Any]],
    gold_cases: list[dict[str, Any]],
    smoke_cases: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "purpose": "Day7 student-router instruction data",
        "source_files": {
            "train": str(train_path),
            "dev": str(dev_path),
            "gold": str(gold_path),
        },
        "output_files": {key: str(path) for key, path in sorted(output_paths.items())},
        "format": {
            "sft": "messages = system,user,assistant; assistant content is compact router target JSON",
            "prompt": "messages = system,user; target retained only for local scoring",
            "router_target_only": ["read_hints", "write_spans", "ignore_spans"],
        },
        "counts": {
            "train_sft": len(train_cases),
            "dev_prompt": len(dev_cases),
            "gold_prompt": len(gold_cases),
            "dev_smoke_prompt": len(smoke_cases),
        },
        "category_counts": {
            "train": category_counts(train_cases),
            "dev": category_counts(dev_cases),
            "gold": category_counts(gold_cases),
            "dev_smoke": category_counts(smoke_cases),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare SFT and prompt JSONL files for the Day7 student router."
    )
    parser.add_argument("--train", type=Path, default=Path("data/processed/synthetic_train_5000.jsonl"))
    parser.add_argument("--dev", type=Path, default=Path("data/dev/dev_250.jsonl"))
    parser.add_argument("--gold", type=Path, default=Path("data/gold/gold_eval_300.jsonl"))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--smoke-per-category", type=int, default=2)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    train_cases = read_cases(args.train)
    dev_cases = read_cases(args.dev)
    gold_cases = read_cases(args.gold)

    train_sft = [sft_record(case, args.train) for case in train_cases]
    dev_prompt = [prompt_record(case, args.dev) for case in dev_cases]
    gold_prompt = [prompt_record(case, args.gold) for case in gold_cases]
    smoke_prompt = stratified_smoke(dev_prompt, args.smoke_per_category)

    output_paths = {
        "train_sft": args.output_dir / "train_sft_messages.jsonl",
        "dev_prompt": args.output_dir / "dev_prompt_messages.jsonl",
        "gold_prompt": args.output_dir / "gold_prompt_messages.jsonl",
        "dev_smoke_prompt": args.output_dir / "dev_smoke_20_prompt_messages.jsonl",
        "manifest": args.output_dir / "manifest.json",
    }

    write_jsonl(output_paths["train_sft"], train_sft)
    write_jsonl(output_paths["dev_prompt"], dev_prompt)
    write_jsonl(output_paths["gold_prompt"], gold_prompt)
    write_jsonl(output_paths["dev_smoke_prompt"], smoke_prompt)

    manifest = build_manifest(
        train_path=args.train,
        dev_path=args.dev,
        gold_path=args.gold,
        output_paths=output_paths,
        train_cases=train_cases,
        dev_cases=dev_cases,
        gold_cases=gold_cases,
        smoke_cases=smoke_prompt,
    )
    output_paths["manifest"].write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    validations = {
        "train_sft": validate_sft_records(output_paths["train_sft"]),
        "dev_prompt": validate_prompt_records(output_paths["dev_prompt"]),
        "gold_prompt": validate_prompt_records(output_paths["gold_prompt"]),
        "dev_smoke_prompt": validate_prompt_records(output_paths["dev_smoke_prompt"]),
    }

    print(f"wrote Day7 student data to {args.output_dir}")
    for name, (count, categories) in validations.items():
        print(f"{name}: {count} records; categories={dict(sorted(categories.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
