"""JSONL-backed fixture memory store for Context 7.2.

SQLite is planned for a later context. This store keeps the first skeleton
small, inspectable, and stdlib-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

from apps.memory_harness.schemas import JsonDict, validate_memory_record


class JsonlMemoryStore:
    def __init__(self, memories: Iterable[JsonDict]):
        self._memories: Dict[str, JsonDict] = {}
        for memory in memories:
            validate_memory_record(memory)
            memory_id = memory["memory_id"]
            if memory_id in self._memories:
                raise ValueError(f"duplicate memory_id: {memory_id}")
            self._memories[memory_id] = memory

    def get_all_memories(self) -> List[JsonDict]:
        return list(self._memories.values())

    def get_by_ids(self, ids: Iterable[str]) -> List[JsonDict]:
        missing = [memory_id for memory_id in ids if memory_id not in self._memories]
        if missing:
            raise KeyError(f"missing memory ids: {', '.join(missing)}")
        return [self._memories[memory_id] for memory_id in ids]


def load_memory_pool(path: str) -> JsonlMemoryStore:
    rows: List[JsonDict] = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL") from exc
    return JsonlMemoryStore(rows)

