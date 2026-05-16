from decimal import Decimal

from craclx.domain.quote_calculator import CalculationParameters, QuoteCalculator


def test_calculates_challenge_example_quote() -> None:
    calculator = QuoteCalculator(
        parameters=CalculationParameters(
            age_rate_increment=Decimal("0.005"),
            age_unit_years=1,
            coverage_percentage=Decimal("1.00"),
            value_rate_increment=Decimal("0.005"),
            value_rate_unit=Decimal("10000.00"),
        )
    )

    quote = calculator.calculate(
        broker_fee=Decimal("50.00"),
        car_value=Decimal("100000.00"),
        deductible_percentage=Decimal("0.10"),
        geographic_adjustment=Decimal("0.00"),
        reference_year=2026,
        vehicle_year=2016,
    )

    assert quote.applied_rate == Decimal("0.100")
    assert quote.calculated_premium == Decimal("9050.00000")
    assert quote.deductible_value == Decimal("10000.0000")
    assert quote.policy_limit == Decimal("90000.0000")


def test_calculates_configured_coverage_policy_limit() -> None:
    calculator = QuoteCalculator(
        parameters=CalculationParameters(
            age_rate_increment=Decimal("0.005"),
            age_unit_years=1,
            coverage_percentage=Decimal("0.80"),
            value_rate_increment=Decimal("0.005"),
            value_rate_unit=Decimal("10000.00"),
        )
    )

    quote = calculator.calculate(
        broker_fee=Decimal("0.00"),
        car_value=Decimal("50000.00"),
        deductible_percentage=Decimal("0.20"),
        geographic_adjustment=Decimal("0.00"),
        reference_year=2026,
        vehicle_year=2021,
    )

    assert quote.deductible_value == Decimal("8000.0000")
    assert quote.policy_limit == Decimal("32000.0000")


def test_calculates_zero_deductible_quote() -> None:
    calculator = QuoteCalculator(
        parameters=CalculationParameters(
            age_rate_increment=Decimal("0.005"),
            age_unit_years=1,
            coverage_percentage=Decimal("1.00"),
            value_rate_increment=Decimal("0.005"),
            value_rate_unit=Decimal("10000.00"),
        )
    )

    quote = calculator.calculate(
        broker_fee=Decimal("25.00"),
        car_value=Decimal("20000.00"),
        deductible_percentage=Decimal("0.00"),
        geographic_adjustment=Decimal("0.00"),
        reference_year=2026,
        vehicle_year=2024,
    )

    assert quote.applied_rate == Decimal("0.020")
    assert quote.calculated_premium == Decimal("425.00000")
    assert quote.deductible_value == Decimal("0.0000")
    assert quote.policy_limit == Decimal("20000.0000")


def test_includes_geographic_adjustment_in_applied_rate() -> None:
    calculator = QuoteCalculator(
        parameters=CalculationParameters(
            age_rate_increment=Decimal("0.005"),
            age_unit_years=1,
            coverage_percentage=Decimal("1.00"),
            value_rate_increment=Decimal("0.005"),
            value_rate_unit=Decimal("10000.00"),
        )
    )

    quote = calculator.calculate(
        broker_fee=Decimal("0.00"),
        car_value=Decimal("30000.00"),
        deductible_percentage=Decimal("0.00"),
        geographic_adjustment=Decimal("0.015"),
        reference_year=2026,
        vehicle_year=2023,
    )

    assert quote.applied_rate == Decimal("0.045")
