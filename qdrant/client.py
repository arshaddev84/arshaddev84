from __future__ import annotations

from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, PointStruct, VectorParams

from config.settings import get_settings

from .schemas import SearchResult


class QdrantStore:
    """Thin wrapper around the Qdrant client for FieldSyncAI.

    Note:
    - The repo-local `qdrant_storage/` directory is intended for the persistent
      storage mount when Qdrant is run in Docker or another local container.
    - The Python client connects to the service endpoint defined by
      `settings.qdrant_url` (for example, `http://localhost:6333`).
    """

    def __init__(self, url: str | None = None, collection_name: str | None = None) -> None:
        settings = get_settings()
        self.client = QdrantClient(url=url or settings.qdrant_url)
        self.collection_name = collection_name or settings.qdrant_collection

    def ensure_collection(self, vector_size: int = 384) -> None:
        """Create the collection if it does not exist."""
        try:
            self.client.get_collection(collection_name=self.collection_name)
        except UnexpectedResponse as exc:
            if exc.status_code != 404:
                raise
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size,distance=Distance.COSINE)
            )

        def upsert_points(self, points: list[dict[str, Any]]) -> None:
            """Upsert a batch of points into Qdrant.

            Each point should contain:
            - "id": unique point identifier
            - "vector": embedding vector
            - "payload": metadata to store with the point
            """
            qdrant_points = [
                PointStruct(
                    id=item["id"],
                    vector=item["vector"],
                    payload=item["payload"]
                )
                for item in points
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=qdrant_points
            )

        def search(
            self,
            vector: list[float],
            *,
            limit: int = 5,
            with_payload: bool = True
        ) -> list[SearchResult]:
            """Search the collection for the nearest vectors."""
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=limit,
                with_payload=with_payload
            )

            return [
                SearchResult(
                    id=str(result.id),
                    score=float(result.score),
                    payload=dict(result.payload or {})
                )
                for result in results
            ]
