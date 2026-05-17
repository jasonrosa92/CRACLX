from datetime import UTC, datetime

from craclx.application.calculate_quote import CalculateQuoteUseCase
from craclx.domain.quote_calculator import QuoteCalculator
from craclx.infrastructure.configurable_gis_adjustment_provider import (
    ConfigurableGeographicRiskAdjustmentProvider,
)
from craclx.infrastructure.settings import Settings


def create_calculate_quote_use_case(settings: Settings) -> CalculateQuoteUseCase:
    reference_year = settings.reference_year or datetime.now(tz=UTC).year

    return CalculateQuoteUseCase(
        calculator=QuoteCalculator(parameters=settings.to_calculation_parameters()),
        geographic_risk_adjustment_provider=ConfigurableGeographicRiskAdjustmentProvider(
            adjustment_max=settings.gis_adjustment_max,
            adjustment_min=settings.gis_adjustment_min,
            high_risk_locations=settings.gis_high_risk_locations,
            low_risk_locations=settings.gis_low_risk_locations,
        ),
        reference_year=reference_year,
    )
