from dataclasses import dataclass
from decimal import Decimal


class DomainValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class CalculationParameters:
    age_rate_increment: Decimal
    age_unit_years: int
    coverage_percentage: Decimal
    value_rate_increment: Decimal
    value_rate_unit: Decimal

    def __post_init__(self) -> None:
        _ensure_positive(name="age_unit_years", value=Decimal(self.age_unit_years))
        _ensure_positive(name="value_rate_unit", value=self.value_rate_unit)
        _ensure_non_negative(
            name="age_rate_increment",
            value=self.age_rate_increment,
        )
        _ensure_non_negative(
            name="coverage_percentage",
            value=self.coverage_percentage,
        )
        _ensure_non_negative(
            name="value_rate_increment",
            value=self.value_rate_increment,
        )


@dataclass(frozen=True, slots=True)
class QuoteCalculation:
    applied_rate: Decimal
    calculated_premium: Decimal
    deductible_value: Decimal
    policy_limit: Decimal


class DynamicRateCalculator:
    def __init__(self, parameters: CalculationParameters) -> None:
        self._parameters = parameters

    def calculate(
        self,
        car_value: Decimal,
        geographic_adjustment: Decimal,
        reference_year: int,
        vehicle_year: int,
    ) -> Decimal:
        age_units = (reference_year - vehicle_year) // self._parameters.age_unit_years
        value_units = car_value // self._parameters.value_rate_unit

        age_rate = Decimal(age_units) * self._parameters.age_rate_increment
        value_rate = value_units * self._parameters.value_rate_increment

        return age_rate + value_rate + geographic_adjustment


class PremiumCalculator:
    def calculate(
        self,
        applied_rate: Decimal,
        broker_fee: Decimal,
        car_value: Decimal,
        deductible_percentage: Decimal,
    ) -> Decimal:
        base_premium = car_value * applied_rate
        deductible_discount = base_premium * deductible_percentage

        return base_premium - deductible_discount + broker_fee


class QuoteCalculator:
    def __init__(self, parameters: CalculationParameters) -> None:
        self._parameters = parameters
        self._premium_calculator = PremiumCalculator()
        self._rate_calculator = DynamicRateCalculator(parameters=parameters)

    def calculate(
        self,
        broker_fee: Decimal,
        car_value: Decimal,
        deductible_percentage: Decimal,
        geographic_adjustment: Decimal,
        reference_year: int,
        vehicle_year: int,
    ) -> QuoteCalculation:
        self._validate_calculation_input(
            broker_fee=broker_fee,
            car_value=car_value,
            deductible_percentage=deductible_percentage,
            reference_year=reference_year,
            vehicle_year=vehicle_year,
        )
        applied_rate = self._calculate_applied_rate(
            car_value=car_value,
            geographic_adjustment=geographic_adjustment,
            reference_year=reference_year,
            vehicle_year=vehicle_year,
        )
        calculated_premium = self._premium_calculator.calculate(
            applied_rate=applied_rate,
            broker_fee=broker_fee,
            car_value=car_value,
            deductible_percentage=deductible_percentage,
        )

        base_policy_limit = car_value * self._parameters.coverage_percentage
        deductible_value = base_policy_limit * deductible_percentage
        policy_limit = base_policy_limit - deductible_value

        return QuoteCalculation(
            applied_rate=applied_rate,
            calculated_premium=calculated_premium,
            deductible_value=deductible_value,
            policy_limit=policy_limit,
        )

    def _calculate_applied_rate(
        self,
        car_value: Decimal,
        geographic_adjustment: Decimal,
        reference_year: int,
        vehicle_year: int,
    ) -> Decimal:
        return self._rate_calculator.calculate(
            car_value=car_value,
            geographic_adjustment=geographic_adjustment,
            reference_year=reference_year,
            vehicle_year=vehicle_year,
        )

    def _validate_calculation_input(
        self,
        broker_fee: Decimal,
        car_value: Decimal,
        deductible_percentage: Decimal,
        reference_year: int,
        vehicle_year: int,
    ) -> None:
        _ensure_non_negative(name="broker_fee", value=broker_fee)
        _ensure_non_negative(name="car_value", value=car_value)
        _ensure_non_negative(
            name="deductible_percentage",
            value=deductible_percentage,
        )

        if vehicle_year > reference_year:
            raise DomainValidationError(
                "vehicle_year must be less than or equal to reference_year"
            )


def _ensure_non_negative(name: str, value: Decimal) -> None:
    if value < Decimal("0"):
        raise DomainValidationError(f"{name} must be non-negative")


def _ensure_positive(name: str, value: Decimal) -> None:
    if value <= Decimal("0"):
        raise DomainValidationError(f"{name} must be positive")
