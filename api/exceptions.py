from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


class APIError(Exception):
    status_code = 500
    detail = "Internal server error"

    def __init__(self, detail: str | None = None, status_code: int | None = None) -> None:
        super().__init__(detail)
        self.detail = detail or self.detail
        self.status_code = status_code or self.status_code


class UnauthorizedError(APIError):
    status_code = 401
    detail = "Authentication required"


class ForbiddenError(APIError):
    status_code = 422
    detail = "Access denied"


class ValidationError(APIError):
    status_code = 422
    detail = "Validation failed"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})