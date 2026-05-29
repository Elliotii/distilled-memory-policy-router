"""Generate deterministic baseline prediction JSONL files.

The baselines are intentionally small:

- empty: never read, write, or ignore anything.
- all-read: read every supplied candidate memory, never write or ignore.
- rule-based: simple text heuristics over the router input fields.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.validate_predictions import load_gold_cases


EMPTY_TARGET = {"read_hints": [], "write_spans": [], "ignore_spans": []}

STOP_WORDS = {
    "a",
    "about",
    "after",
    "all",
    "also",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "by",
    "can",
    "do",
    "does",
    "for",
    "from",
    "going",
    "has",
    "have",
    "i",
    "in",
    "is",
    "it",
    "its",
    "just",
    "me",
    "must",
    "my",
    "new",
    "not",
    "now",
    "of",
    "on",
    "or",
    "our",
    "please",
    "should",
    "so",
    "that",
    "the",
    "this",
    "to",
    "use",
    "we",
    "with",
}

TYPE_MARKERS = {
    "sop": re.compile(
        r"\b(always|must|should|required|requires|policy|rule|every|never|from now on|going forward)\b",
        re.IGNORECASE,
    ),
    "decision": re.compile(
        r"\b(decided|choose|chose|chosen|selected|settled|agreed|picked|standardize|standardized)\b",
        re.IGNORECASE,
    ),
    "task_state": re.compile(
        r"\b(currently|still|blocked|pending|in progress|in-progress|midway|halfway|working on|debugging|tracking down|left to|not done|not resolved|complete|completed|finished|live in production)\b",
        re.IGNORECASE,
    ),
}

WRITE_PATTERNS: tuple[tuple[re.Pattern[str], str | None], ...] = (
    (re.compile(r"\bPlease remember that (?P<span>[^.?!]+)", re.IGNORECASE), None),
    (re.compile(r"\bRemember that (?P<span>[^.?!]+)", re.IGNORECASE), None),
    (re.compile(r"\bNote that (?P<span>[^.?!]+)", re.IGNORECASE), None),
    (re.compile(r"\bGoing forward,? (?P<span>[^.?!]+)", re.IGNORECASE), None),
    (re.compile(r"\bFrom now on,? (?P<span>[^.?!]+)", re.IGNORECASE), "sop"),
    (re.compile(r"\bwe decided to (?P<span>[^.?!]+)", re.IGNORECASE), "decision"),
    (re.compile(r"\bwe chose to (?P<span>[^.?!]+)", re.IGNORECASE), "decision"),
    (re.compile(r"\bwe selected (?P<span>[^.?!]+)", re.IGNORECASE), "decision"),
    (re.compile(r"\bwe picked (?P<span>[^.?!]+)", re.IGNORECASE), "decision"),
    (re.compile(r"\bI am currently (?P<span>[^.?!]+)", re.IGNORECASE), "task_state"),
    (re.compile(r"\bI'm currently (?P<span>[^.?!]+)", re.IGNORECASE), "task_state"),
    (re.compile(r"\bI am still (?P<span>[^.?!]+)", re.IGNORECASE), "task_state"),
    (re.compile(r"\bI'm still (?P<span>[^.?!]+)", re.IGNORECASE), "task_state"),
    (re.compile(r"\bstill (?P<span>[^.?!]+)", re.IGNORECASE), "task_state"),
    (re.compile(r"\bcurrently (?P<span>[^.?!]+)", re.IGNORECASE), "task_state"),
    (re.compile(r"\bthe current source of truth is (?P<span>[^.?!]+)", re.IGNORECASE), None),
    (re.compile(r"\btreat (?P<span>[^.?!]+ as the current [^.?!]+)", re.IGNORECASE), None),
    (re.compile(r"\buse (?P<span>[^.?!]+ as the current [^.?!]+)", re.IGNORECASE), None),
)

IGNORE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"\bIgnore this temporary noise:\s+(?P<span>[^.?!]+)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bIgnore these temporary notes:\s+(?P<span>[^.?!]+)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:also\s+)?(?:please\s+)?(?:ignore|disregard|skip|forget)\s+(?P<span>[^.?!]+)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:also|and)\s+(?P<span>the [^.?!]*(?:false positive|false alert|spurious|transient|brief|already|suppressed|code smell)[^.?!]*)",
        re.IGNORECASE,
    ),
)


def content_tokens(text: str) -> set[str]:
    tokens = {
        token.lower()
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text)
    }
    return {token for token in tokens if token not in STOP_WORDS}


def clean_span(span: str) -> str:
    return span.strip()


def clean_ignore_span(span: str) -> str:
    cleaned = clean_span(span)
    lowered = cleaned.lower()
    for prefix in (
        "this temporary noise:",
        "these temporary notes:",
        "temporary noise:",
        "temporary notes:",
        "this noise:",
        "these notes:",
    ):
        if lowered.startswith(prefix):
            return clean_span(cleaned[len(prefix) :])
    return cleaned


def sentence_prefix(text: str) -> str:
    match = re.match(r"(?P<span>[^.?!]+)", text.strip())
    return clean_span(match.group("span")) if match else ""


def infer_write_type(span: str, current_user_input: str) -> str:
    combined = f"{current_user_input} {span}"
    if TYPE_MARKERS["sop"].search(combined):
        return "sop"
    if TYPE_MARKERS["decision"].search(combined):
        return "decision"
    if TYPE_MARKERS["task_state"].search(combined):
        return "task_state"
    return "fact"


def add_write_span(
    writes: list[dict[str, str]],
    *,
    span: str,
    current_user_input: str,
    forced_type: str | None = None,
) -> None:
    cleaned = clean_span(span)
    if not cleaned or cleaned not in current_user_input:
        return
    if any(existing["span"] == cleaned for existing in writes):
        return
    writes.append(
        {
            "span": cleaned,
            "type": forced_type or infer_write_type(cleaned, current_user_input),
        }
    )


def predict_reads(case: dict[str, Any]) -> list[str]:
    current = case.get("current_user_input", "")
    recent = " ".join(
        turn.get("content", "")
        for turn in case.get("recent_context", [])
        if isinstance(turn, dict)
    )
    query_tokens = content_tokens(f"{current} {recent}")

    scored: list[tuple[int, int, str]] = []
    for index, memory in enumerate(case.get("candidate_memories", [])):
        memory_id = memory.get("id")
        content = memory.get("content", "")
        if not isinstance(memory_id, str) or not isinstance(content, str):
            continue
        overlap = query_tokens & content_tokens(content)
        strong_overlap = {token for token in overlap if len(token) >= 5 or "-" in token or "_" in token}
        score = len(overlap) + len(strong_overlap)
        if score >= 3 or len(strong_overlap) >= 2:
            scored.append((score, -index, memory_id))

    scored.sort(reverse=True)
    return [memory_id for _, _, memory_id in scored[:4]]


def predict_writes(case: dict[str, Any]) -> list[dict[str, str]]:
    text = case.get("current_user_input", "")
    writes: list[dict[str, str]] = []

    for pattern, forced_type in WRITE_PATTERNS:
        for match in pattern.finditer(text):
            add_write_span(
                writes,
                span=match.group("span"),
                current_user_input=text,
                forced_type=forced_type,
            )

    if not writes and re.search(r"\b(now|must|decided|chosen|selected|standardized|blocked|pending)\b", text, re.IGNORECASE):
        prefix = sentence_prefix(text)
        if prefix:
            add_write_span(writes, span=prefix, current_user_input=text)

    return writes[:4]


def predict_ignores(case: dict[str, Any]) -> list[str]:
    text = case.get("current_user_input", "")
    ignores: list[str] = []

    for pattern in IGNORE_PATTERNS:
        for match in pattern.finditer(text):
            span = clean_ignore_span(match.group("span"))
            if span and span in text and span not in ignores:
                ignores.append(span)

    return ignores[:5]


def predict_target(case: dict[str, Any], baseline: str) -> dict[str, Any]:
    if baseline == "empty":
        return {"read_hints": [], "write_spans": [], "ignore_spans": []}
    if baseline == "all-read":
        return {
            "read_hints": [
                memory["id"]
                for memory in case.get("candidate_memories", [])
                if isinstance(memory, dict) and isinstance(memory.get("id"), str)
            ],
            "write_spans": [],
            "ignore_spans": [],
        }
    if baseline == "rule-based":
        return {
            "read_hints": predict_reads(case),
            "write_spans": predict_writes(case),
            "ignore_spans": predict_ignores(case),
        }
    raise ValueError(f"unknown baseline: {baseline}")


def write_predictions(
    *,
    input_path: Path,
    output_path: Path,
    baseline: str,
    run_id: str,
    model_id: str,
) -> int:
    cases = load_gold_cases(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for case_id, case in cases.items():
            row = {
                "case_id": case_id,
                "target": predict_target(case, baseline),
                "run_id": run_id,
                "model_id": model_id,
            }
            handle.write(json.dumps(row, ensure_ascii=True, separators=(",", ":")) + "\n")
    return len(cases)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline", choices=["empty", "all-read", "rule-based"], required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model-id")
    args = parser.parse_args()

    model_id = args.model_id or f"baseline:{args.baseline}"
    count = write_predictions(
        input_path=args.input,
        output_path=args.output,
        baseline=args.baseline,
        run_id=args.run_id,
        model_id=model_id,
    )
    print(f"wrote {count} predictions to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
