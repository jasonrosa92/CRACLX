from dataclasses import dataclass
from decimal import Decimal

from craclx.application.gis_adjustment import (
    Address,
    GeographicRiskAdjustmentProvider,
    NoGeographicRiskAdjustmentProvider,
)
from craclx.domain.quote_calculator import QuoteCalculator


@dataclass(frozen=True, slots=True)
class CarDetails:
    make: str
    model: str
    value: Decimal
    year: int


@dataclass(frozen=True, slots=True)
class CalculateQuoteInput:
    broker_fee: Decimal
    car: CarDetails
    deductible_percentage: Decimal
    geographic_adjustment: Decimal = Decimal("0.00")
    registration_location: Address | None = None


@dataclass(frozen=True, slots=True)
class CalculateQuoteOutput:
    applied_rate: Decimal
    calculated_premium: Decimal
    car: CarDetails
    deductible_value: Decimal
    policy_limit: Decimal


class CalculateQuoteUseCase:
    def __init__(
        self,
        calculator: QuoteCalculator,
        geographic_risk_adjustment_provider: GeographicRiskAdjustmentProvider | None,
        reference_year: int,
    ) -> None:
        self._calculator = calculator
        self._geographic_risk_adjustment_provider = (
            geographic_risk_adjustment_provider or NoGeographicRiskAdjustmentProvider()
        )
        self._reference_year = reference_year

    def execute(self, data: CalculateQuoteInput) -> CalculateQuoteOutput:
        geographic_adjustment = self._calculate_geographic_adjustment(data=data)
        quote = self._calculator.calculate(
            broker_fee=data.broker_fee,
            car_value=data.car.value,
            deductible_percentage=data.deductible_percentage,
            geographic_adjustment=geographic_adjustment,
            reference_year=self._reference_year,
            vehicle_year=data.car.year,
        )

        return CalculateQuoteOutput(
            applied_rate=quote.applied_rate,
            calculated_premium=quote.calculated_premium,
            car=data.car,
            deductible_value=quote.deductible_value,
            policy_limit=quote.policy_limit,
        )

    def _calculate_geographic_adjustment(self, data: CalculateQuoteInput) -> Decimal:
        if data.registration_location is None:
            return data.geographic_adjustment

        return self._geographic_risk_adjustment_provider.calculate_adjustment(
            address=data.registration_location
        )
