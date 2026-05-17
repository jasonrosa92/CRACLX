from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient
from pytest import MonkeyPatch

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
    payload = response.json()

    assert Decimal(payload["applied_rate"]) == Decimal("0.100")
    assert Decimal(payload["calculated_premium"]) == Decimal("9050.0000000")
    assert payload["car"] == {
        "make": "Toyota",
        "model": "Corolla",
        "value": "100000.00",
        "year": 2016,
    }
    assert Decimal(payload["deductible_value"]) == Decimal("10000.000000")
    assert Decimal(payload["policy_limit"]) == Decimal("90000.000000")


@pytest.mark.anyio
async def test_quote_endpoint_rejects_invalid_payload() -> None:
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
                    "value": "-1.00",
                    "year": 2016,
                },
                "deductible_percentage": "0.10",
            },
        )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_quote_endpoint_uses_configured_calculation_parameters(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv("AGE_RATE_INCREMENT", "0.010")
    monkeypatch.setenv("AGE_UNIT_YEARS", "2")
    monkeypatch.setenv("COVERAGE_PERCENTAGE", "0.80")
    monkeypatch.setenv("REFERENCE_YEAR", "2026")
    monkeypatch.setenv("VALUE_RATE_INCREMENT", "0.020")
    monkeypatch.setenv("VALUE_RATE_UNIT", "5000.00")
    get_settings.cache_clear()
    transport = ASGITransport(app=create_app())

    async with AsyncClient(base_url="http://testserver", transport=transport) as client:
        response = await client.post(
            "/quotes",
            json={
                "broker_fee": "0.00",
                "car": {
                    "make": "Honda",
                    "model": "Fit",
                    "value": "15000.00",
                    "year": 2020,
                },
                "deductible_percentage": "0.20",
            },
        )

    payload = response.json()

    assert response.status_code == 200
    assert Decimal(payload["applied_rate"]) == Decimal("0.090")
    assert Decimal(payload["calculated_premium"]) == Decimal("1080.0000000")
    assert Decimal(payload["deductible_value"]) == Decimal("2400.000000")
    assert Decimal(payload["policy_limit"]) == Decimal("9600.000000")
