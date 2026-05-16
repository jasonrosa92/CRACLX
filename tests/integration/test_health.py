import pytest
from httpx import ASGITransport, AsyncClient

from craclx.bootstrap.app import create_app


@pytest.mark.anyio
async def test_health_check_returns_application_status() -> None:
    transport = ASGITransport(app=create_app())

    async with AsyncClient(base_url="http://testserver", transport=transport) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "app": "CRACLX",
        "environment": "local",
        "status": "ok",
        "version": "0.1.0",
    }
