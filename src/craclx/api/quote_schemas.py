from decimal import Decimal

from pydantic import BaseModel, Field


class CarDetailsSchema(BaseModel):
    make: str
    model: str
    value: Decimal = Field(ge=Decimal("0"))
    year: int = Field(gt=0)
