"""Core schemas for memory policy router decision cases."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class MemoryType(str, Enum):
    """Allowed labels for memory-worthy write spans."""

    SOP = "sop"
    FACT = "fact"
    DECISION = "decision"
    TASK_STATE = "task_state"


class Category(str, Enum):
    """MVP capability categories used for balanced analysis."""

    SIMPLE_WRITE = "simple_write"
    MULTI_WRITE = "multi_write"
    READ_RELEVANT_MEMORY = "read_relevant_memory"
    IGNORE_NOISE = "ignore_noise"
    CORRECTION_OR_REVISION = "correction_or_revision"
    CONTEXT_DEPENDENT_REFERENCE = "context_dependent_reference"
    CONFLICTING_MEMORY = "conflicting_memory"
    MIXED_WRITE_AND_IGNORE = "mixed_write_and_ignore"
    NO_ACTION_NEEDED = "no_action_needed"
    DISTRACTOR_MEMORY_SELECTION = "distractor_memory_selection"


REQUIRED_CATEGORIES: tuple[Category, ...] = tuple(Category)


class Difficulty(str, Enum):
    """Coarse case difficulty for analysis and stratified sampling."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ReviewStatus(str, Enum):
    """Review state for generated or curated cases."""

    SYNTHETIC = "synthetic"
    LLM_REVIEWED = "llm_reviewed"
    HUMAN_REVIEWED = "human_reviewed"


class Split(str, Enum):
    """Dataset split label."""

    SEED = "seed"
    TRAIN = "train"
    DEV = "dev"
    GOLD_EVAL = "gold_eval"


class Role(str, Enum):
    """Allowed recent-context speaker roles."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class StrictModel(BaseModel):
    """Base model that rejects unexpected fields."""

    model_config = ConfigDict(extra="forbid")


class ContextTurn(StrictModel):
    """A short recent-context turn shown to the router."""

    role: Role
    content: str = Field(min_length=1)


class CandidateMemory(StrictModel):
    """A candidate memory supplied by the harness or retriever."""

    id: str = Field(min_length=1)
    type: MemoryType
    content: str = Field(min_length=1)


class WriteSpan(StrictModel):
    """A memory-worthy span copied exactly from current_user_input."""

    span: str = Field(min_length=1)
    type: MemoryType


class RouterTarget(StrictModel):
    """Gold target or model prediction for one decision case."""

    read_hints: list[str] = Field(default_factory=list)
    write_spans: list[WriteSpan] = Field(default_factory=list)
    ignore_spans: list[str] = Field(default_factory=list)

    @field_validator("read_hints")
    @classmethod
    def read_hints_are_unique(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("read_hints must not contain duplicate IDs")
        return value

    @field_validator("ignore_spans")
    @classmethod
    def ignore_spans_are_unique(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("ignore_spans must not contain duplicate spans")
        return value


class DecisionCase(StrictModel):
    """One supervised memory-policy decision case."""

    case_id: str = Field(min_length=1)
    split: Split
    family_id: str = Field(min_length=1)
    category: Category
    tags: list[str] = Field(default_factory=list)
    domain: str = Field(min_length=1)
    difficulty: Difficulty
    generator_prompt_id: str = Field(min_length=1)
    review_status: ReviewStatus
    gold_notes: Optional[str] = None

    current_user_input: str = Field(min_length=1)
    recent_context: list[ContextTurn] = Field(default_factory=list, max_length=4)
    candidate_memories: list[CandidateMemory] = Field(default_factory=list, max_length=8)
    target: RouterTarget

    @field_validator("tags")
    @classmethod
    def tags_are_non_empty(cls, value: list[str]) -> list[str]:
        empty_tags = [tag for tag in value if not tag]
        if empty_tags:
            raise ValueError("tags must not contain empty strings")
        return value

    @model_validator(mode="after")
    def validate_case_constraints(self) -> "DecisionCase":
        memory_ids = [memory.id for memory in self.candidate_memories]
        if len(memory_ids) != len(set(memory_ids)):
            raise ValueError("candidate_memories IDs must be unique within a case")

        unknown_read_hints = [
            memory_id
            for memory_id in self.target.read_hints
            if memory_id not in set(memory_ids)
        ]
        if unknown_read_hints:
            raise ValueError(f"read_hints reference missing candidate IDs: {unknown_read_hints}")

        write_seen: set[str] = set()
        for write_span in self.target.write_spans:
            if write_span.span in write_seen:
                raise ValueError(f"duplicate write span: {write_span.span!r}")
            write_seen.add(write_span.span)
            if write_span.span not in self.current_user_input:
                raise ValueError(
                    "write_spans must be exact substrings of current_user_input: "
                    f"{write_span.span!r}"
                )

        for ignore_span in self.target.ignore_spans:
            if ignore_span not in self.current_user_input:
                raise ValueError(
                    "ignore_spans must be exact substrings of current_user_input: "
                    f"{ignore_span!r}"
                )

        return self
