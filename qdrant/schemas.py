from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SearchResult:
    """Respresents a single Qdrant search hit returned to the retrieval layer."""

    id: str
    score: float
    payload: dict[str, Any] = field(default_factory=dict)