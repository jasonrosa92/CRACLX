from decimal import Decimal

from pydantic import BaseModel, Field


class AddressSchema(BaseModel):
    city: str
    country: str
    postal_code: str
    state: str
    street: str


class CarDetailsSchema(BaseModel):
    make: str
    model: str
    value: Decimal = Field(ge=Decimal("0"))
    year: int = Field(gt=0)


class QuoteRequestSchema(BaseModel):
    broker_fee: Decimal = Field(ge=Decimal("0"))
    car: CarDetailsSchema
    deductible_percentage: Decimal = Field(ge=Decimal("0"))
    registration_location: AddressSchema | None = None
