"""Deterministic keyword/BM25-lite retrieval stubs."""

from __future__ import annotations

import re
from typing import Dict, Iterable, List, Tuple

from apps.memory_harness.schemas import JsonDict


TOKEN_RE = re.compile(r"[a-z0-9_]+")


def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text.lower())


def _context_bonus(query_tokens: set[str], memory: JsonDict) -> float:
    bonus = 0.0
    for field in ("project", "repo", "service"):
        value = str(memory.get(field, "")).lower()
        if value and value in query_tokens:
            bonus += 2.0
        elif value and any(part in query_tokens for part in tokenize(value)):
            bonus += 1.0
    return bonus


def score_memory(query: str, memory: JsonDict) -> Tuple[float, List[str]]:
    query_tokens = set(tokenize(query))
    memory_tokens = set(tokenize(" ".join([
        str(memory.get("text", "")),
        str(memory.get("project", "")),
        str(memory.get("repo", "")),
        str(memory.get("service", "")),
        str(memory.get("target", "")),
    ])))
    matched = sorted(query_tokens & memory_tokens)
    if not query_tokens:
        return 0.0, matched
    overlap_score = len(matched) / max(len(query_tokens), 1)
    score = overlap_score + _context_bonus(query_tokens, memory)
    return round(score, 6), matched


def retrieve_top_k(query: str, memories: Iterable[JsonDict], k: int) -> List[JsonDict]:
    candidates = []
    for memory in memories:
        score, matched_tokens = score_memory(query, memory)
        candidates.append({
            "memory_id": memory["memory_id"],
            "score": score,
            "matched_tokens": matched_tokens,
            "memory": memory,
        })
    candidates.sort(key=lambda item: (-item["score"], item["memory_id"]))
    return candidates[: max(k, 0)]

