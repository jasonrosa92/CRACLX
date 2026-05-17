from decimal import Decimal

from craclx.application.calculate_quote import (
    CalculateQuoteInput,
    CalculateQuoteUseCase,
    CarDetails,
)
from craclx.application.gis_adjustment import Address
from craclx.domain.quote_calculator import CalculationParameters, QuoteCalculator


def test_calculate_quote_use_case_returns_car_details_and_quote_values() -> None:
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

    result = use_case.execute(
        CalculateQuoteInput(
            broker_fee=Decimal("50.00"),
            car=CarDetails(
                make="Toyota",
                model="Corolla",
                value=Decimal("100000.00"),
                year=2016,
            ),
            deductible_percentage=Decimal("0.10"),
            geographic_adjustment=Decimal("0.00"),
        )
    )

    assert result.applied_rate == Decimal("0.100")
    assert result.calculated_premium == Decimal("9050.00000")
    assert result.car == CarDetails(
        make="Toyota",
        model="Corolla",
        value=Decimal("100000.00"),
        year=2016,
    )
    assert result.deductible_value == Decimal("10000.0000")
    assert result.policy_limit == Decimal("90000.0000")


def test_calculate_quote_use_case_uses_geographic_adjustment_provider() -> None:
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
        geographic_risk_adjustment_provider=FixedGeographicRiskAdjustmentProvider(
            adjustment=Decimal("0.020")
        ),
        reference_year=2026,
    )

    result = use_case.execute(
        CalculateQuoteInput(
            broker_fee=Decimal("50.00"),
            car=CarDetails(
                make="Toyota",
                model="Corolla",
                value=Decimal("100000.00"),
                year=2016,
            ),
            deductible_percentage=Decimal("0.10"),
            registration_location=Address(
                city="Sao Paulo",
                country="BR",
                postal_code="01000-000",
                state="SP",
                street="Avenida Paulista",
            ),
        )
    )

    assert result.applied_rate == Decimal("0.120")
    assert result.calculated_premium == Decimal("10850.00000")


class FixedGeographicRiskAdjustmentProvider:
    def __init__(self, adjustment: Decimal) -> None:
        self._adjustment = adjustment

    def calculate_adjustment(self, address: Address) -> Decimal:
        return self._adjustment
