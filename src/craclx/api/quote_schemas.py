from decimal import Decimal

from pydantic import BaseModel, Field, field_serializer


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


class QuoteResponseSchema(BaseModel):
    applied_rate: Decimal
    calculated_premium: Decimal
    car: CarDetailsSchema
    deductible_value: Decimal
    policy_limit: Decimal

    @field_serializer(
        "applied_rate",
        "calculated_premium",
        "deductible_value",
        "policy_limit",
        when_used="json",
    )
    def serialize_decimal(self, value: Decimal) -> str:
        return str(value)
