from decimal import Decimal

import pytest
from pydantic import ValidationError

from craclx.api.quote_schemas import CarDetailsSchema


def test_car_details_schema_accepts_vehicle_payload() -> None:
    car = CarDetailsSchema.model_validate(
        {
            "make": "Toyota",
            "model": "Corolla",
            "value": "100000.00",
            "year": 2016,
        }
    )

    assert car.make == "Toyota"
    assert car.model == "Corolla"
    assert car.value == Decimal("100000.00")
    assert car.year == 2016


def test_car_details_schema_rejects_negative_value() -> None:
    with pytest.raises(ValidationError):
        CarDetailsSchema.model_validate(
            {
                "make": "Toyota",
                "model": "Corolla",
                "value": "-1.00",
                "year": 2016,
            }
        )
