from decimal import Decimal

from fastapi import APIRouter

from craclx.api.quote_router import create_quote_router
from craclx.application.calculate_quote import CalculateQuoteUseCase
from craclx.domain.quote_calculator import CalculationParameters, QuoteCalculator


def test_create_quote_router_returns_api_router() -> None:
    use_case = CalculateQuoteUseCase(
        calculator=QuoteCalculator(
            parameters=CalculationParameters(
                age_rate_increment=Decimal("0.005"),
                age_unit_years=1,
                coverage_percentage=Decimal("1.00"),
                value_rate_increment=Decimal("0.005"),
                value_rate_unit=Decimal("10000.00"),
            )
        ),
        reference_year=2026,
    )

    router = create_quote_router(use_case=use_case)

    assert isinstance(router, APIRouter)
