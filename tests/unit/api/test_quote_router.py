from decimal import Decimal

import pytest
from fastapi import APIRouter, FastAPI
from httpx import ASGITransport, AsyncClient

from craclx.api.quote_router import create_quote_router
from craclx.application.calculate_quote import CalculateQuoteUseCase
from craclx.application.gis_adjustment import NoGeographicRiskAdjustmentProvider
from craclx.domain.quote_calculator import CalculationParameters, QuoteCalculator


def test_create_quote_router_returns_api_router() -> None:
    use_case = _create_use_case()

    router = create_quote_router(use_case=use_case)

    assert isinstance(router, APIRouter)


@pytest.mark.anyio
async def test_quote_router_calculates_quote_successfully() -> None:
    app = FastAPI()
    app.include_router(create_quote_router(use_case=_create_use_case()))
    transport = ASGITransport(app=app)

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
    assert Decimal(payload["calculated_premium"]) == Decimal("9050.00000")
    assert payload["car"] == {
        "make": "Toyota",
        "model": "Corolla",
        "value": "100000.00",
        "year": 2016,
    }
    assert Decimal(payload["deductible_value"]) == Decimal("10000.0000")
    assert Decimal(payload["policy_limit"]) == Decimal("90000.0000")


def _create_use_case() -> CalculateQuoteUseCase:
    return CalculateQuoteUseCase(
        calculator=QuoteCalculator(
            parameters=CalculationParameters(
                age_rate_increment=Decimal("0.005"),
                age_unit_years=1,
                coverage_percentage=Decimal("1.00"),
                value_rate_increment=Decimal("0.005"),
                value_rate_unit=Decimal("10000.00"),
            )
        ),
        geographic_risk_adjustment_provider=NoGeographicRiskAdjustmentProvider(),
        reference_year=2026,
    )
