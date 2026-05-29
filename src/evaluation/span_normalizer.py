"""Deterministic span normalization for router evaluation.

The normalizer is a scoring aid only. It must not mutate gold labels,
prediction files, or downstream memory entries.
"""

from __future__ import annotations

import re
import string
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

DEFAULT_MARKERS_PATH = Path(__file__).with_name("normalizer_markers.txt")
DEFAULT_TOKEN_F1_THRESHOLD = 0.8

_TOKEN_RE = re.compile(r"[a-z0-9]+(?:[-_'][a-z0-9]+)?")
_WHITESPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class NormalizerConfig:
    write_leading_markers: tuple[str, ...]
    ignore_leading_markers: tuple[str, ...]
    token_f1_threshold: float = DEFAULT_TOKEN_F1_THRESHOLD


def load_marker_config(path: Path = DEFAULT_MARKERS_PATH) -> NormalizerConfig:
    sections: dict[str, list[str]] = {
        "write_leading_markers": [],
        "ignore_leading_markers": [],
    }
    current_section: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            if current_section not in sections:
                raise ValueError(f"unknown marker section: {current_section}")
            continue
        if current_section is None:
            raise ValueError(f"marker outside section: {line}")
        sections[current_section].append(canonical_text(line))

    return NormalizerConfig(
        write_leading_markers=tuple(
            sorted(set(sections["write_leading_markers"]), key=len, reverse=True)
        ),
        ignore_leading_markers=tuple(
            sorted(set(sections["ignore_leading_markers"]), key=len, reverse=True)
        ),
    )


@lru_cache(maxsize=1)
def default_marker_config() -> NormalizerConfig:
    return load_marker_config(DEFAULT_MARKERS_PATH)


def canonical_text(value: str) -> str:
    """Normalize casing and whitespace without removing semantic words."""

    text = value.strip()
    text = text.strip(string.whitespace + "\"'`“”‘’.,;:!?()[]{}")
    text = _WHITESPACE_RE.sub(" ", text)
    return text.lower()


def strip_leading_marker(value: str, markers: tuple[str, ...]) -> str:
    text = canonical_text(value)
    for marker in markers:
        if text == marker:
            return text
        for separator in (" ", ": ", ", ", " - "):
            prefix = f"{marker}{separator}"
            if text.startswith(prefix):
                return canonical_text(text[len(prefix) :])
    return text


def normalize_span(value: str, *, kind: str, config: NormalizerConfig | None = None) -> str:
    """Normalize a write or ignore span for scoring-time matching."""

    marker_config = config or default_marker_config()
    if kind == "write":
        return strip_leading_marker(value, marker_config.write_leading_markers)
    if kind == "ignore":
        return strip_leading_marker(value, marker_config.ignore_leading_markers)
    raise ValueError(f"unsupported span kind: {kind}")


def tokens(value: str) -> set[str]:
    return set(_TOKEN_RE.findall(value))


def token_set_f1(left: str, right: str) -> float:
    left_tokens = tokens(left)
    right_tokens = tokens(right)
    if not left_tokens and not right_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    true_positive = len(left_tokens & right_tokens)
    precision = true_positive / len(right_tokens)
    recall = true_positive / len(left_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def span_similarity(
    gold_span: str,
    predicted_span: str,
    *,
    kind: str,
    config: NormalizerConfig | None = None,
) -> float:
    return token_set_f1(
        normalize_span(gold_span, kind=kind, config=config),
        normalize_span(predicted_span, kind=kind, config=config),
    )


def greedy_span_matches(
    gold_spans: list[str],
    predicted_spans: list[str],
    *,
    kind: str,
    config: NormalizerConfig | None = None,
    threshold: float | None = None,
) -> list[tuple[int, int, float]]:
    """Return one-to-one span matches sorted by best normalized token F1."""

    marker_config = config or default_marker_config()
    min_score = threshold if threshold is not None else marker_config.token_f1_threshold
    candidates: list[tuple[float, int, int]] = []
    for gold_index, gold_span in enumerate(gold_spans):
        for pred_index, predicted_span in enumerate(predicted_spans):
            score = span_similarity(gold_span, predicted_span, kind=kind, config=marker_config)
            if score >= min_score:
                candidates.append((score, gold_index, pred_index))

    matches: list[tuple[int, int, float]] = []
    used_gold: set[int] = set()
    used_pred: set[int] = set()
    for score, gold_index, pred_index in sorted(candidates, reverse=True):
        if gold_index in used_gold or pred_index in used_pred:
            continue
        used_gold.add(gold_index)
        used_pred.add(pred_index)
        matches.append((gold_index, pred_index, score))
    return sorted(matches)
