from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import get_settings

from .models import Base

_engine = None
_SessionLocal = None


def init_db() -> None:
    global _engine, _SessionLocal

    settings = get_settings()
    _engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    )
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    Base.metadata.create_all(bind=_engine)


def get_db_session() -> Generator[Session, None, None]:
    global _SessionLocal

    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    session = _SessionLocal()
    try:
        yield session
    finally:
        session.close()