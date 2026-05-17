from decimal import Decimal

from craclx.application.calculate_quote import CalculateQuoteInput, CarDetails
from craclx.bootstrap.use_cases import create_calculate_quote_use_case
from craclx.infrastructure.settings import Settings


def test_create_calculate_quote_use_case_from_settings() -> None:
    use_case = create_calculate_quote_use_case(
        Settings(
            age_rate_increment=Decimal("0.005"),
            age_unit_years=1,
            coverage_percentage=Decimal("1.00"),
            reference_year=2026,
            value_rate_increment=Decimal("0.005"),
            value_rate_unit=Decimal("10000.00"),
        )
    )

    result = use_case.execute(
        data=CalculateQuoteInput(
            broker_fee=Decimal("50.00"),
            car=CarDetails(
                make="Toyota",
                model="Corolla",
                value=Decimal("100000.00"),
                year=2016,
            ),
            deductible_percentage=Decimal("0.10"),
        )
    )

    assert result.applied_rate == Decimal("0.100")
