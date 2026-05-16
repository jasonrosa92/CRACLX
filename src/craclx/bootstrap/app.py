from fastapi import FastAPI

from craclx.infrastructure.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version)

    @app.get("/health", tags=["system"])
    async def health_check() -> dict[str, str]:
        return {
            "app": settings.app_name,
            "environment": settings.app_env,
            "status": "ok",
            "version": settings.app_version,
        }

    return app
