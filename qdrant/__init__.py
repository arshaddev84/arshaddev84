"""Qdrant integration for FieldSyncAI.

This package provides the vector-store wrapper used by the retrieval layer.
It connects to the local Qdrant service and manages collections used for
document embeddings and semantic search.
"""

from .client import QdrantStore
from .schemas import SearchResult

__all__ = ["QdrantStore", "SearchResult"]