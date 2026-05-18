from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from craclx.domain.quote_calculator import DomainValidationError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainValidationError)
    async def handle_domain_validation_error(
        request: Request,
        exc: DomainValidationError,
    ) -> JSONResponse:
        del request

        return _error_response(
            code="domain_validation_error",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def _error_response(code: str, message: str, status_code: int) -> JSONResponse:
    content: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
        }
    }

    return JSONResponse(content=content, status_code=status_code)
