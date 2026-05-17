from datetime import UTC, datetime

from craclx.application.calculate_quote import CalculateQuoteUseCase
from craclx.domain.quote_calculator import QuoteCalculator
from craclx.infrastructure.settings import Settings


def create_calculate_quote_use_case(settings: Settings) -> CalculateQuoteUseCase:
    reference_year = settings.reference_year or datetime.now(tz=UTC).year

    return CalculateQuoteUseCase(
        calculator=QuoteCalculator(parameters=settings.to_calculation_parameters()),
        reference_year=reference_year,
    )
