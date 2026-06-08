"""Deterministic current-unit stub.

This is deliberately simple. It is not a semantic unitizer; it only creates
small auditable current units for harness fixtures.
"""

from __future__ import annotations

import re
from typing import Dict, List


def _sentence_split(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(parts) <= 1:
        parts = re.split(r";\s+|\.\s*", text.strip())
    return [part.strip() for part in parts if part.strip()]


def unitize_text(input_text: str) -> List[Dict[str, object]]:
    """Split text into deterministic unit dictionaries.

    Newlines are preferred because fixture authors can control them exactly.
    If the input has only one non-empty line, the function falls back to basic
    sentence-boundary splitting.
    """

    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    fragments = lines if len(lines) > 1 else _sentence_split(input_text)
    return [
        {
            "unit_id": f"u{index}",
            "text": fragment,
            "source": "unitizer_stub",
            "flags": [],
        }
        for index, fragment in enumerate(fragments, 1)
    ]

