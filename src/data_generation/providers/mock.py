"""Local deterministic mock generation provider.

This provider does not call a model API, read credentials, or access the network. It is
used to exercise the generation pipeline before a real teacher provider is connected.
"""

from __future__ import annotations

from typing import Any

from src.data_generation.prompt_templates import PROMPT_TEMPLATES, get_template
from src.data_generation.providers.base import ProviderMetadata
from src.schemas import Category, DecisionCase


class LocalMockProvider:
    """Deterministic provider that emits structurally valid mock cases."""

    metadata = ProviderMetadata(
        name="local_mock_generator",
        version="day3_offline_v1",
        api_provider=None,
        model_name=None,
    )

    def generate(
        self,
        *,
        count: int,
        template_names: list[str],
        run_id: str,
    ) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for index in range(count):
            template = get_template(template_names[index % len(template_names)])
            records.append(
                make_mock_case(
                    index=index,
                    template_name=template.name,
                    generator_prompt_id=template.generator_prompt_id,
                    run_id=run_id,
                )
            )
        return records


def make_mock_case(
    index: int,
    template_name: str,
    generator_prompt_id: str,
    run_id: str = "adhoc",
) -> dict[str, Any]:
    category = list(Category)[index % len(Category)].value
    case_number = index + 1

    base_payload: dict[str, Any] = {
        "case_id": f"mock_{run_id}_{template_name}_{case_number:06d}",
        "split": "train",
        "family_id": f"mock_{run_id}_{template_name}_family_{case_number:06d}",
        "category": category,
        "tags": ["mock_generation", "dry_run_safe", f"template_{template_name}"],
        "domain": "coding_workflow",
        "difficulty": "easy",
        "generator_prompt_id": generator_prompt_id,
        "review_status": "synthetic",
        "gold_notes": None,
    }

    if category == Category.SIMPLE_WRITE.value:
        payload = {
            **base_payload,
            "current_user_input": "For mock data, remember the billing export now includes archived invoices.",
            "recent_context": [],
            "candidate_memories": [],
            "target": {
                "read_hints": [],
                "write_spans": [
                    {
                        "span": "the billing export now includes archived invoices",
                        "type": "fact",
                    }
                ],
                "ignore_spans": [],
            },
        }
        if index % 40 == 0:
            payload["current_user_input"] = (
                "For mock data, always confirm billing export changes with the finance owner."
            )
            payload["target"]["write_spans"] = [
                {
                    "span": "always confirm billing export changes with the finance owner",
                    "type": "sop",
                }
            ]
    elif category == Category.MULTI_WRITE.value:
        payload = {
            **base_payload,
            "current_user_input": (
                "For mock releases, the rollout is paused until QA signs off, "
                "invoices use the v2 export path, and the next step is to verify retry metrics."
            ),
            "recent_context": [],
            "candidate_memories": [],
            "target": {
                "read_hints": [],
                "write_spans": [
                    {"span": "the rollout is paused until QA signs off", "type": "decision"},
                    {"span": "invoices use the v2 export path", "type": "fact"},
                    {"span": "the next step is to verify retry metrics", "type": "task_state"},
                ],
                "ignore_spans": [],
            },
        }
    elif category == Category.READ_RELEVANT_MEMORY.value:
        payload = {
            **base_payload,
            "current_user_input": "Before editing API retry handling, check the existing retry policy.",
            "recent_context": [],
            "candidate_memories": [
                {
                    "id": "m1",
                    "type": "decision",
                    "content": "API retries are capped at 3 attempts.",
                },
                {"id": "m2", "type": "fact", "content": "Billing exports use CSV files."},
            ],
            "target": {"read_hints": ["m1"], "write_spans": [], "ignore_spans": []},
        }
    elif category == Category.IGNORE_NOISE.value:
        payload = {
            **base_payload,
            "current_user_input": (
                "The mock terminal flickered once, but that is transient; rerun the validator."
            ),
            "recent_context": [],
            "candidate_memories": [],
            "target": {
                "read_hints": [],
                "write_spans": [],
                "ignore_spans": ["The mock terminal flickered once"],
            },
        }
    elif category == Category.CORRECTION_OR_REVISION.value:
        payload = {
            **base_payload,
            "current_user_input": (
                "Correction: the mock billing service uses Dragonfly instead of Redis for caching."
            ),
            "recent_context": [],
            "candidate_memories": [
                {
                    "id": "m1",
                    "type": "fact",
                    "content": "The mock billing service uses Redis for caching.",
                }
            ],
            "target": {
                "read_hints": ["m1"],
                "write_spans": [
                    {
                        "span": "the mock billing service uses Dragonfly instead of Redis for caching",
                        "type": "fact",
                    }
                ],
                "ignore_spans": [],
            },
        }
    elif category == Category.CONTEXT_DEPENDENT_REFERENCE.value:
        payload = {
            **base_payload,
            "current_user_input": "Use the second option and keep the worker path asynchronous.",
            "recent_context": [
                {
                    "role": "assistant",
                    "content": "The first option keeps retries in the API; the second uses the worker.",
                }
            ],
            "candidate_memories": [],
            "target": {
                "read_hints": [],
                "write_spans": [
                    {"span": "Use the second option", "type": "decision"},
                    {"span": "keep the worker path asynchronous", "type": "decision"},
                ],
                "ignore_spans": [],
            },
        }
    elif category == Category.CONFLICTING_MEMORY.value:
        payload = {
            **base_payload,
            "current_user_input": (
                "Mock source of truth is PostgreSQL now, not the old SQLite note."
            ),
            "recent_context": [],
            "candidate_memories": [
                {"id": "m1", "type": "fact", "content": "SQLite is the mock database."},
                {"id": "m2", "type": "fact", "content": "PostgreSQL is the mock database."},
            ],
            "target": {
                "read_hints": ["m1", "m2"],
                "write_spans": [
                    {"span": "PostgreSQL now, not the old SQLite note", "type": "decision"}
                ],
                "ignore_spans": [],
            },
        }
    elif category == Category.MIXED_WRITE_AND_IGNORE.value:
        payload = {
            **base_payload,
            "current_user_input": (
                "Remember that mock previews expire after 24 hours, but ignore the temporary DNS warning."
            ),
            "recent_context": [],
            "candidate_memories": [],
            "target": {
                "read_hints": [],
                "write_spans": [
                    {"span": "mock previews expire after 24 hours", "type": "fact"}
                ],
                "ignore_spans": ["the temporary DNS warning"],
            },
        }
    elif category == Category.NO_ACTION_NEEDED.value:
        payload = {
            **base_payload,
            "current_user_input": "Please show the mock validation summary again.",
            "recent_context": [],
            "candidate_memories": [
                {
                    "id": "m1",
                    "type": "task_state",
                    "content": "The validator summary was already generated.",
                }
            ],
            "target": {"read_hints": [], "write_spans": [], "ignore_spans": []},
        }
    elif category == Category.DISTRACTOR_MEMORY_SELECTION.value:
        payload = {
            **base_payload,
            "current_user_input": (
                "For mock upload retries, read the S3 upload memory; theme notes are unrelated."
            ),
            "recent_context": [],
            "candidate_memories": [
                {"id": "m1", "type": "fact", "content": "Mock uploads use S3."},
                {"id": "m2", "type": "decision", "content": "The demo UI theme was postponed."},
            ],
            "target": {"read_hints": ["m1"], "write_spans": [], "ignore_spans": []},
        }
    else:
        raise ValueError(f"unsupported mock category: {category}")

    payload["current_user_input"] = f"Mock case {case_number}: {payload['current_user_input']}"
    DecisionCase.model_validate(payload)
    return payload
