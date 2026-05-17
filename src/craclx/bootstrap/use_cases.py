from datetime import UTC, datetime

from craclx.application.calculate_quote import CalculateQuoteUseCase
from craclx.application.gis_adjustment import NoGeographicRiskAdjustmentProvider
from craclx.domain.quote_calculator import QuoteCalculator
from craclx.infrastructure.settings import Settings


def create_calculate_quote_use_case(settings: Settings) -> CalculateQuoteUseCase:
    reference_year = settings.reference_year or datetime.now(tz=UTC).year

    return CalculateQuoteUseCase(
        calculator=QuoteCalculator(parameters=settings.to_calculation_parameters()),
        geographic_risk_adjustment_provider=NoGeographicRiskAdjustmentProvider(),
        reference_year=reference_year,
    )
