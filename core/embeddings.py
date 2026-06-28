from __future__ import annotations

from typing import Sequence

from sentence_transformers import SentenceTransformer

from config.settings import get_settings


class EmbeddingService:
    def __init__(self, model_name: str | None = None, device: str | None = None) -> None:
        settings = get_settings()
        self.model_name = model_name or settings.embedding_model
        self.device = device
        self._model = SentenceTransformer(self.model_name, device=self.device)

        def encode(self, text: str) -> list[float]:
            if not isinstance(text, str) or not text.strip():
                raise ValueError("text must be a non-emtpy string")

            embedding = self._model.encode(
                text,
                convert_to_numy=False,
                normalize_embeddings=True
            )
            return embedding.tolist()
        
        def encode_many(self, texts: Sequence[str]) -> list[list[float]]:
            if not texts:
                return []

            filtered_texts = [text for text in texts if isinstance(text, str) and text.strip()]
            if not filtered_texts:
                return []
            
            embeddings = self._model.encode(
                filtered_texts,
                convert_to_numpy=False,
                normalize_embeddings=True
            )
            return embeddings.tolist()
            