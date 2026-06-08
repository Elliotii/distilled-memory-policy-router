"""Budgeted memory context builder."""

from __future__ import annotations

from typing import List

from apps.memory_harness.schemas import JsonDict


def _memory_line(memory: JsonDict) -> str:
    return f"{memory['memory_id']} [{memory.get('target', 'memory')}]: {memory.get('text', '')}"


def build_context(
    selected_memories: List[JsonDict],
    max_memories: int,
    max_context_chars: int,
) -> JsonDict:
    lines: List[str] = []
    kept_ids: List[str] = []
    omitted_ids: List[str] = []
    used_chars = 0

    for memory in selected_memories:
        memory_id = memory["memory_id"]
        if len(kept_ids) >= max_memories:
            omitted_ids.append(memory_id)
            continue
        line = _memory_line(memory)
        extra_chars = len(line) + (1 if lines else 0)
        if used_chars + extra_chars > max_context_chars:
            omitted_ids.append(memory_id)
            continue
        lines.append(line)
        kept_ids.append(memory_id)
        used_chars += extra_chars

    return {
        "context_text": "\n".join(lines),
        "selected_memory_ids": kept_ids,
        "omitted_memory_ids": omitted_ids,
        "context_chars": len("\n".join(lines)),
        "max_memories": max_memories,
        "max_context_chars": max_context_chars,
    }

