from decimal import Decimal

from craclx.domain.quote_calculator import (
    CalculationParameters,
    DynamicRateCalculator,
)


def test_calculates_dynamic_rate_from_vehicle_age_and_value() -> None:
    calculator = DynamicRateCalculator(
        parameters=CalculationParameters(
            age_rate_increment=Decimal("0.005"),
            age_unit_years=1,
            coverage_percentage=Decimal("1.00"),
            value_rate_increment=Decimal("0.005"),
            value_rate_unit=Decimal("10000.00"),
        )
    )

    applied_rate = calculator.calculate(
        car_value=Decimal("100000.00"),
        geographic_adjustment=Decimal("0.00"),
        reference_year=2026,
        vehicle_year=2016,
    )

    assert applied_rate == Decimal("0.100")


def test_calculates_dynamic_rate_with_configured_units() -> None:
    calculator = DynamicRateCalculator(
        parameters=CalculationParameters(
            age_rate_increment=Decimal("0.010"),
            age_unit_years=2,
            coverage_percentage=Decimal("1.00"),
            value_rate_increment=Decimal("0.020"),
            value_rate_unit=Decimal("5000.00"),
        )
    )

    applied_rate = calculator.calculate(
        car_value=Decimal("15000.00"),
        geographic_adjustment=Decimal("0.00"),
        reference_year=2026,
        vehicle_year=2020,
    )

    assert applied_rate == Decimal("0.090")


def test_includes_geographic_adjustment_in_dynamic_rate() -> None:
    calculator = DynamicRateCalculator(
        parameters=CalculationParameters(
            age_rate_increment=Decimal("0.005"),
            age_unit_years=1,
            coverage_percentage=Decimal("1.00"),
            value_rate_increment=Decimal("0.005"),
            value_rate_unit=Decimal("10000.00"),
        )
    )

    applied_rate = calculator.calculate(
        car_value=Decimal("30000.00"),
        geographic_adjustment=Decimal("-0.010"),
        reference_year=2026,
        vehicle_year=2023,
    )

    assert applied_rate == Decimal("0.020")
