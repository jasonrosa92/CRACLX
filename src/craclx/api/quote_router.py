from fastapi import APIRouter

from craclx.api.quote_schemas import (
    CarDetailsSchema,
    QuoteRequestSchema,
    QuoteResponseSchema,
)
from craclx.application.calculate_quote import (
    CalculateQuoteInput,
    CalculateQuoteUseCase,
    CarDetails,
)
from craclx.application.gis_adjustment import Address


def create_quote_router(use_case: CalculateQuoteUseCase) -> APIRouter:
    router = APIRouter(prefix="/quotes", tags=["quotes"])

    @router.post("", response_model=QuoteResponseSchema)
    async def calculate_quote(request: QuoteRequestSchema) -> QuoteResponseSchema:
        result = use_case.execute(
            CalculateQuoteInput(
                broker_fee=request.broker_fee,
                car=CarDetails(
                    make=request.car.make,
                    model=request.car.model,
                    value=request.car.value,
                    year=request.car.year,
                ),
                deductible_percentage=request.deductible_percentage,
                registration_location=_to_address(request=request),
            )
        )

        return QuoteResponseSchema(
            applied_rate=result.applied_rate,
            calculated_premium=result.calculated_premium,
            car=CarDetailsSchema(
                make=result.car.make,
                model=result.car.model,
                value=result.car.value,
                year=result.car.year,
            ),
            deductible_value=result.deductible_value,
            policy_limit=result.policy_limit,
        )

    return router


def _to_address(request: QuoteRequestSchema) -> Address | None:
    if request.registration_location is None:
        return None

    return Address(
        city=request.registration_location.city,
        country=request.registration_location.country,
        postal_code=request.registration_location.postal_code,
        state=request.registration_location.state,
        street=request.registration_location.street,
    )
