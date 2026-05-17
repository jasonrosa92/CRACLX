from fastapi import FastAPI

from craclx.api.quote_router import create_quote_router
from craclx.bootstrap.use_cases import create_calculate_quote_use_case
from craclx.infrastructure.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.include_router(
        create_quote_router(use_case=create_calculate_quote_use_case(settings=settings))
    )

    @app.get("/health", tags=["system"])
    async def health_check() -> dict[str, str]:
        return {
            "app": settings.app_name,
            "environment": settings.app_env,
            "status": "ok",
            "version": settings.app_version,
        }

    return app
