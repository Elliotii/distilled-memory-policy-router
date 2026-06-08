"""Lightweight schema helpers for the Applied Memory Harness.

The harness intentionally uses stdlib dictionaries and dataclasses instead of
runtime-heavy validation libraries. Validation here is structural only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


JsonDict = Dict[str, Any]


@dataclass
class CurrentUnit:
    unit_id: str
    text: str
    source: str = "fixture"
    flags: List[str] = field(default_factory=list)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class MemoryRecord:
    memory_id: str
    text: str
    target: str
    project: str = ""
    repo: str = ""
    service: str = ""
    flags: List[str] = field(default_factory=list)
    created_at: str = ""
    source: str = "fixture"

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class Scenario:
    scenario_id: str
    user_input: str
    runtime_context: JsonDict = field(default_factory=dict)
    current_units: List[JsonDict] = field(default_factory=list)
    candidate_memory_ids: List[str] = field(default_factory=list)
    labels: JsonDict = field(default_factory=dict)
    fixture_router_read_ids: List[str] = field(default_factory=list)
    fixture_store_units: List[JsonDict] = field(default_factory=list)
    fixture_skip_unit_ids: List[str] = field(default_factory=list)
    expected_answer_requirements: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class RetrievalCandidate:
    memory_id: str
    score: float
    memory: JsonDict
    matched_tokens: List[str] = field(default_factory=list)

    def to_dict(self) -> JsonDict:
        return {
            "memory_id": self.memory_id,
            "score": self.score,
            "matched_tokens": self.matched_tokens,
            **self.memory,
        }


@dataclass
class ReadSelection:
    selected_memory_ids: List[str]
    backend: str
    diagnostics: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class WritePreview:
    store_previews: List[JsonDict]
    skip_previews: List[JsonDict]
    diagnostics: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class AuditTrace:
    trace_id: str
    created_at: str
    scenario_id: str
    user_input: str
    current_units: List[JsonDict]
    retrieval: JsonDict
    read_selection: JsonDict
    write_policy: JsonDict
    context_builder: JsonDict
    downstream_response: JsonDict
    write_preview: JsonDict
    evaluation: JsonDict

    def to_dict(self) -> JsonDict:
        return asdict(self)


def require_keys(row: JsonDict, keys: List[str], label: str) -> None:
    missing = [key for key in keys if key not in row]
    if missing:
        raise ValueError(f"{label} missing required keys: {', '.join(missing)}")


def validate_memory_record(row: JsonDict) -> None:
    require_keys(row, ["memory_id", "text", "target"], "memory record")
    forbidden = {"relevance_category", "hard_negative_type"}
    present = sorted(forbidden & row.keys())
    if present:
        raise ValueError(
            "memory record contains case-specific relevance fields: "
            + ", ".join(present)
        )


def validate_scenario(row: JsonDict) -> None:
    require_keys(row, ["scenario_id", "user_input", "candidate_memory_ids"], "scenario")


def normalize_current_unit(row: JsonDict, index: Optional[int] = None) -> JsonDict:
    if "unit_id" not in row:
        if index is None:
            raise ValueError("current unit missing unit_id")
        row = {**row, "unit_id": f"u{index}"}
    if "text" not in row:
        raise ValueError(f"current unit {row.get('unit_id')} missing text")
    row.setdefault("source", "fixture")
    row.setdefault("flags", [])
    return row

