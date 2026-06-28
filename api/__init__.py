from fastapi import FastAPI

from .exceptions import register_exception_handlers
from .middleware import register_middleware
from .routes import register_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="FieldSyncAI API",
        version="0.1.0",
        description="Secure local RAG API for field technician assistance."
    )
    register_middleware(app)
    register_exception_handlers(app)
    register_routes(app)
    return app
