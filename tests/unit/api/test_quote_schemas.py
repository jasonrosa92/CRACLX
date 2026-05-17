from decimal import Decimal

import pytest
from pydantic import ValidationError

from craclx.api.quote_schemas import (
    AddressSchema,
    CarDetailsSchema,
    QuoteRequestSchema,
    QuoteResponseSchema,
)


def test_quote_request_schema_accepts_required_car_details() -> None:
    request = QuoteRequestSchema.model_validate(
        {
            "broker_fee": "50.00",
            "car": {
                "make": "Toyota",
                "model": "Corolla",
                "value": "100000.00",
                "year": 2016,
            },
            "deductible_percentage": "0.10",
        }
    )

    assert request.broker_fee == Decimal("50.00")
    assert request.car == CarDetailsSchema(
        make="Toyota",
        model="Corolla",
        value=Decimal("100000.00"),
        year=2016,
    )
    assert request.deductible_percentage == Decimal("0.10")
    assert request.registration_location is None


def test_quote_request_schema_accepts_optional_registration_location() -> None:
    request = QuoteRequestSchema.model_validate(
        {
            "broker_fee": "50.00",
            "car": {
                "make": "Toyota",
                "model": "Corolla",
                "value": "100000.00",
                "year": 2016,
            },
            "deductible_percentage": "0.10",
            "registration_location": {
                "city": "Sao Paulo",
                "country": "BR",
                "postal_code": "01000-000",
                "state": "SP",
                "street": "Avenida Paulista",
            },
        }
    )

    assert request.registration_location == AddressSchema(
        city="Sao Paulo",
        country="BR",
        postal_code="01000-000",
        state="SP",
        street="Avenida Paulista",
    )


def test_quote_request_schema_rejects_negative_values() -> None:
    with pytest.raises(ValidationError):
        QuoteRequestSchema.model_validate(
            {
                "broker_fee": "50.00",
                "car": {
                    "make": "Toyota",
                    "model": "Corolla",
                    "value": "-1.00",
                    "year": 2016,
                },
                "deductible_percentage": "0.10",
            }
        )


def test_quote_response_schema_serializes_required_contract() -> None:
    response = QuoteResponseSchema(
        applied_rate=Decimal("0.100"),
        calculated_premium=Decimal("9050.00000"),
        car=CarDetailsSchema(
            make="Toyota",
            model="Corolla",
            value=Decimal("100000.00"),
            year=2016,
        ),
        deductible_value=Decimal("10000.0000"),
        policy_limit=Decimal("90000.0000"),
    )

    assert response.model_dump(mode="json") == {
        "applied_rate": "0.100",
        "calculated_premium": "9050.00000",
        "car": {
            "make": "Toyota",
            "model": "Corolla",
            "value": "100000.00",
            "year": 2016,
        },
        "deductible_value": "10000.0000",
        "policy_limit": "90000.0000",
    }
