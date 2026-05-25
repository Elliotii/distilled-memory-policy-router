"""Provider interface for synthetic case generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ProviderMetadata:
    """Metadata every generation provider should expose."""

    name: str
    version: str
    api_provider: str | None = None
    model_name: str | None = None


class GenerationProvider(Protocol):
    """Common interface for mock and future teacher-model providers."""

    metadata: ProviderMetadata

    def generate(
        self,
        *,
        count: int,
        template_names: list[str],
        run_id: str,
    ) -> list[dict[str, Any]]:
        """Generate raw JSON-serializable decision-case records."""
        ...
