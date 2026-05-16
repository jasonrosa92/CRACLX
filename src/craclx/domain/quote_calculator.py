from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class CalculationParameters:
    age_rate_increment: Decimal
    age_unit_years: int
    coverage_percentage: Decimal
    value_rate_increment: Decimal
    value_rate_unit: Decimal


@dataclass(frozen=True, slots=True)
class QuoteCalculation:
    applied_rate: Decimal
    calculated_premium: Decimal
    deductible_value: Decimal
    policy_limit: Decimal


class QuoteCalculator:
    def __init__(self, parameters: CalculationParameters) -> None:
        self._parameters = parameters

    def calculate(
        self,
        broker_fee: Decimal,
        car_value: Decimal,
        deductible_percentage: Decimal,
        geographic_adjustment: Decimal,
        reference_year: int,
        vehicle_year: int,
    ) -> QuoteCalculation:
        applied_rate = self._calculate_applied_rate(
            car_value=car_value,
            geographic_adjustment=geographic_adjustment,
            reference_year=reference_year,
            vehicle_year=vehicle_year,
        )
        base_premium = car_value * applied_rate
        deductible_discount = base_premium * deductible_percentage
        calculated_premium = base_premium - deductible_discount + broker_fee

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
        age_units = (reference_year - vehicle_year) // self._parameters.age_unit_years
        value_units = car_value // self._parameters.value_rate_unit

        age_rate = Decimal(age_units) * self._parameters.age_rate_increment
        value_rate = value_units * self._parameters.value_rate_increment

        return age_rate + value_rate + geographic_adjustment
