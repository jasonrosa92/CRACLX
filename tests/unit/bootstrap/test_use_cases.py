from decimal import Decimal

from craclx.application.calculate_quote import CalculateQuoteInput, CarDetails
from craclx.application.gis_adjustment import Address
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


def test_create_calculate_quote_use_case_uses_configured_gis_adapter() -> None:
    use_case = create_calculate_quote_use_case(
        Settings(
            age_rate_increment=Decimal("0.005"),
            age_unit_years=1,
            coverage_percentage=Decimal("1.00"),
            gis_adjustment_max=Decimal("0.02"),
            gis_adjustment_min=Decimal("-0.02"),
            gis_high_risk_locations=("BR:SP:Sao Paulo:*",),
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
