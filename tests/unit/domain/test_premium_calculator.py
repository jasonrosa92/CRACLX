from decimal import Decimal

from craclx.domain.quote_calculator import PremiumCalculator


def test_calculates_premium_with_deductible_discount_and_broker_fee() -> None:
    calculator = PremiumCalculator()

    premium = calculator.calculate(
        applied_rate=Decimal("0.10"),
        broker_fee=Decimal("50.00"),
        car_value=Decimal("100000.00"),
        deductible_percentage=Decimal("0.10"),
    )

    assert premium == Decimal("9050.0000")


def test_calculates_premium_with_zero_deductible() -> None:
    calculator = PremiumCalculator()

    premium = calculator.calculate(
        applied_rate=Decimal("0.02"),
        broker_fee=Decimal("25.00"),
        car_value=Decimal("20000.00"),
        deductible_percentage=Decimal("0.00"),
    )

    assert premium == Decimal("425.0000")


def test_calculates_premium_with_zero_broker_fee() -> None:
    calculator = PremiumCalculator()

    premium = calculator.calculate(
        applied_rate=Decimal("0.05"),
        broker_fee=Decimal("0.00"),
        car_value=Decimal("50000.00"),
        deductible_percentage=Decimal("0.20"),
    )

    assert premium == Decimal("2000.0000")
