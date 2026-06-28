from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "FieldSyncAI"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    api_prefix: str = "/api/v1"

    allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
    )

    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_issuer: str | None = None
    jwt_audience: str | None = None

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:1b"

    embedding_model: str = "all-MiniLM-L6-v2"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "fieldsyncai_docs"

    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "sqlite:///./fieldsyncai.db"

    vector_top_k: int = Field(default=5, ge=1, le=20)
    chunk_size: int = Field(default=800, ge=100, le=5000)
    chunk_overlap: int = Field(default=100, ge=0, le=1000)

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()