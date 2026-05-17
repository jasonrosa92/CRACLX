from decimal import Decimal

from craclx.domain.quote_calculator import PolicyLimitCalculator


def test_calculates_policy_limit_with_default_coverage() -> None:
    calculator = PolicyLimitCalculator()

    result = calculator.calculate(
        car_value=Decimal("100000.00"),
        coverage_percentage=Decimal("1.00"),
        deductible_percentage=Decimal("0.10"),
    )

    assert result.deductible_value == Decimal("10000.0000")
    assert result.policy_limit == Decimal("90000.0000")


def test_calculates_policy_limit_with_configured_coverage() -> None:
    calculator = PolicyLimitCalculator()

    result = calculator.calculate(
        car_value=Decimal("50000.00"),
        coverage_percentage=Decimal("0.80"),
        deductible_percentage=Decimal("0.20"),
    )

    assert result.deductible_value == Decimal("8000.0000")
    assert result.policy_limit == Decimal("32000.0000")


def test_calculates_policy_limit_with_zero_deductible() -> None:
    calculator = PolicyLimitCalculator()

    result = calculator.calculate(
        car_value=Decimal("20000.00"),
        coverage_percentage=Decimal("1.00"),
        deductible_percentage=Decimal("0.00"),
    )

    assert result.deductible_value == Decimal("0.0000")
    assert result.policy_limit == Decimal("20000.0000")
