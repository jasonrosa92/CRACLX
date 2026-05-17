from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from craclx.bootstrap.app import create_app
from craclx.infrastructure.settings import get_settings


@pytest.mark.anyio
async def test_app_exposes_quote_endpoint() -> None:
    get_settings.cache_clear()
    transport = ASGITransport(app=create_app())

    async with AsyncClient(base_url="http://testserver", transport=transport) as client:
        response = await client.post(
            "/quotes",
            json={
                "broker_fee": "50.00",
                "car": {
                    "make": "Toyota",
                    "model": "Corolla",
                    "value": "100000.00",
                    "year": 2016,
                },
                "deductible_percentage": "0.10",
            },
        )

    assert response.status_code == 200
    assert Decimal(response.json()["calculated_premium"]) > Decimal("0")
