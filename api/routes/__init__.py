from fastapi import FastAPI

from .auth import router as auth_router
from .documents import router as documents_router
from .health import router as health_router
from .query import router as query_router


def register_routes(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(documents_router)
    app.include_router(query_router)
    app.include_router(health_router)