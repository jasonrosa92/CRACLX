from fastapi import APIRouter

from craclx.application.calculate_quote import CalculateQuoteUseCase


def create_quote_router(use_case: CalculateQuoteUseCase) -> APIRouter:
    return APIRouter(prefix="/quotes", tags=["quotes"])
