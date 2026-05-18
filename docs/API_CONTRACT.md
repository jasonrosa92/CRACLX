# API Contract

## Purpose

This document describes the public backend API contract exposed by CRACLX.

The contract is intended for frontend integration and external API consumers. It documents request payloads, response payloads, validation behavior, and examples for the quote calculation endpoint.

## Base API

The current backend exposes:

```text
GET /health
POST /quotes
```

## Health Endpoint

### `GET /health`

Returns application status information.

Successful response:

```json
{
  "app": "CRACLX",
  "environment": "local",
  "status": "ok",
  "version": "0.1.0"
}
```

## Quote Endpoint

### `POST /quotes`

Calculates a car insurance quote from car details, deductible percentage, broker fee, and optional registration location.

The endpoint delegates business behavior to the application and domain layers. The API layer is responsible only for HTTP validation, schema conversion, and response serialization.

## Quote Request Body

Required fields:

- `car`: car details used by the quote calculation
- `deductible_percentage`: deductible percentage as a decimal value
- `broker_fee`: broker fee added after deductible discount

Optional fields:

- `registration_location`: address used by future GIS risk adjustment

### Car Details

```json
{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2016,
  "value": "100000.00"
}
```

Rules:

- `make` must be a string
- `model` must be a string
- `year` must be a positive integer
- `value` must be a non-negative decimal-compatible value

### Registration Location

```json
{
  "city": "Sao Paulo",
  "country": "BR",
  "postal_code": "01000-000",
  "state": "SP",
  "street": "Avenida Paulista"
}
```

The field is accepted by the current API but does not change the rate until the GIS adjustment task is implemented.

### Request Example

```json
{
  "broker_fee": "50.00",
  "car": {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2016,
    "value": "100000.00"
  },
  "deductible_percentage": "0.10",
  "registration_location": {
    "city": "Sao Paulo",
    "country": "BR",
    "postal_code": "01000-000",
    "state": "SP",
    "street": "Avenida Paulista"
  }
}
```

## Quote Response Body

Successful responses include the echoed car details and calculated quote fields.

Response fields:

- `car`: car details echoed from the request
- `applied_rate`: final calculated rate after rate components and adjustments
- `policy_limit`: final policy limit after deductible application
- `calculated_premium`: final premium after deductible discount and broker fee
- `deductible_value`: monetary deductible value calculated from the original policy limit

### Response Example

```json
{
  "applied_rate": "0.100",
  "calculated_premium": "9050.0000000",
  "car": {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2016,
    "value": "100000.00"
  },
  "deductible_value": "10000.000000",
  "policy_limit": "90000.000000"
}
```

Decimal values are serialized as strings to preserve precision in JSON responses.

## Validation And Error Behavior

### Success

Successful quote calculation returns:

```text
200 OK
```

### Invalid Request Payload

Invalid request payloads return FastAPI/Pydantic validation errors:

```text
422 Unprocessable Entity
```

Examples of invalid payloads:

- negative `car.value`
- negative `broker_fee`
- negative `deductible_percentage`
- missing required `car` fields
- invalid field types

Example invalid request:

```json
{
  "broker_fee": "50.00",
  "car": {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2016,
    "value": "-1.00"
  },
  "deductible_percentage": "0.10"
}
```

The exact validation error body follows FastAPI's default validation response format.

### Domain Validation Error

Requests that pass HTTP schema validation but violate business rules return:

```text
400 Bad Request
```

Example response:

```json
{
  "error": {
    "code": "domain_validation_error",
    "message": "vehicle_year must be less than or equal to reference_year"
  }
}
```

Examples of domain validation failures:

- vehicle year greater than the configured reference year
- business values that are structurally valid but invalid for quote calculation

## Configuration Impact

The quote endpoint uses backend configuration values when calculating the response.

Configuration values that affect quote results:

- `AGE_RATE_INCREMENT`
- `AGE_UNIT_YEARS`
- `COVERAGE_PERCENTAGE`
- `REFERENCE_YEAR`
- `VALUE_RATE_INCREMENT`
- `VALUE_RATE_UNIT`

GIS configuration values are already available for future geographic risk adjustment:

- `GIS_ADJUSTMENT_MAX`
- `GIS_ADJUSTMENT_MIN`

Changing these values changes the calculated quote without changing the API request or response shape.
