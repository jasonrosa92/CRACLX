# SDR-0001: Backend System Design

## Status

Accepted

## Date

2026-05-16

## Purpose

This document describes the initial backend system design for the car insurance quote API.

It translates the roadmap and architecture decision into an implementation-oriented design that can guide the upcoming project bootstrap and domain development tasks.

## System Overview

The backend will expose an HTTP API that receives car details and returns a calculated insurance quote.

The system must calculate:

- applied rate
- calculated premium
- deductible value
- policy limit

The API must also echo the car details received from the client.

The frontend is outside this repository. It will consume the backend through the published API contract.

## Main Flow

The expected quote calculation flow is:

```text
HTTP request
-> API request schema validation
-> quote calculation use case
-> configuration-backed calculation parameters
-> optional geographic risk provider
-> domain quote calculator
-> application output
-> API response schema
-> HTTP response
```

Business calculation rules must live in the domain layer. Request validation and response serialization must live in the API layer.

## Proposed Module Layout

The initial backend implementation should follow this structure:

```text
src/
  craclx/
    api/
    application/
    bootstrap/
    domain/
    infrastructure/
tests/
  integration/
  unit/
docs/
  adr/
  sdr/
```

Expected responsibilities:

- `api`: FastAPI routes, HTTP schemas, and exception mapping
- `application`: use cases, application DTOs, and ports
- `bootstrap`: app factory and dependency wiring
- `domain`: business entities, value objects, and calculation services
- `infrastructure`: settings, config loading, logging, and adapters
- `tests/integration`: API and cross-layer behavior tests
- `tests/unit`: domain and application unit tests

## Domain Concepts

Initial domain concepts:

- `Address`: optional registration location data
- `Car`: make, model, year, and value
- `Coverage`: coverage percentage and deductible percentage
- `Money`: monetary amount representation
- `Rate`: percentage representation
- `Quote`: calculated insurance quote
- `QuoteCalculator`: domain service that applies the calculation rules

The exact class names may evolve during implementation, but the business language should remain aligned with these concepts.

## Input Contract

The API request must accept the following car details:

- `make`: string
- `model`: string
- `year`: integer
- `value`: float
- `deductible_percentage`: float
- `broker_fee`: float
- `registration_location`: optional address object

The address object will be optional and used by the GIS adjustment feature.

Initial address fields may include:

- `city`: string
- `country`: string
- `postal_code`: string
- `state`: string
- `street`: string

Address field requirements may be refined when the GIS provider design is implemented.

## Output Contract

The API response must include:

- echoed car details from the request
- `applied_rate`
- `policy_limit`
- `calculated_premium`
- `deductible_value`

The response should use explicit field names that match the challenge requirements.

## Calculation Design

### Dynamic Rate

The dynamic rate is composed of:

- age-based rate component
- value-based rate component
- optional GIS adjustment component

Required behavior:

```text
age_rate = vehicle_age_units * configured_age_rate_increment
value_rate = vehicle_value_bands * configured_value_rate_increment
applied_rate = age_rate + value_rate + geographic_adjustment
```

The challenge example expects:

```text
10-year-old car valued at 100000
age rate = 5%
value rate = 5%
applied rate = 10%
```

The implementation must make the age increment, value band size, and value increment configurable.

### Premium

Required behavior:

```text
base_premium = car_value * applied_rate
deductible_discount = base_premium * deductible_percentage
calculated_premium = base_premium - deductible_discount + broker_fee
```

### Policy Limit

Required behavior:

```text
base_policy_limit = car_value * coverage_percentage
deductible_value = base_policy_limit * deductible_percentage
policy_limit = base_policy_limit - deductible_value
```

The default coverage percentage must be configurable and default to 100%.

## Configuration Design

The backend must load calculation parameters from configuration.

Initial configuration keys:

- `AGE_RATE_INCREMENT`
- `AGE_UNIT_YEARS`
- `COVERAGE_PERCENTAGE`
- `GIS_ADJUSTMENT_MAX`
- `GIS_ADJUSTMENT_MIN`
- `REFERENCE_YEAR`
- `VALUE_RATE_INCREMENT`
- `VALUE_RATE_UNIT`

Configuration rules:

- business values must not be hard-coded inside calculation logic
- invalid configuration values must fail fast during application startup
- tests may override configuration to keep calculations deterministic
- `REFERENCE_YEAR` may be used in tests to avoid time-dependent failures

## GIS Adjustment Design

GIS adjustment will be implemented through a port defined by the application layer.

Current port behavior:

```text
calculate_adjustment(address) -> rate adjustment
```

Rules:

- the adjustment must stay within configured minimum and maximum bounds
- the domain must not call GIS providers directly
- initial implementation may use a fake or configurable adapter
- future implementation may use a real external GIS provider

The application layer owns the `Address` value object used by the port. The API layer maps its request schema into this value object before executing the use case.

When no `registration_location` is provided, the application uses a no-op provider that returns `0.00`. This keeps GIS optional while preserving the same quote calculation flow.

The current infrastructure adapter is configurable and pattern-based. A future real provider should be introduced as another infrastructure adapter behind the same port, keeping the API, application use case, and domain calculator stable.

See [GIS Integration Path](../GIS_INTEGRATION.md) for the future provider strategy.

## Error Handling Design

The backend should distinguish:

- validation errors from invalid API input
- domain errors from invalid business states
- configuration errors from invalid settings
- infrastructure errors from external provider failures

Expected API behavior:

- invalid request payloads return `422`
- invalid business input returns a mapped client error
- unexpected failures return a controlled server error response

The exact error response schema will be defined during the API contract task.

## Testing Design

Testing will follow the roadmap and working agreement.

Initial test groups:

- domain unit tests for rate, premium, and policy limit calculations
- application tests with fake GIS providers
- API integration tests for request and response contracts
- configuration tests for loading and validation behavior

High-priority scenarios:

- example calculation from the challenge
- zero deductible percentage
- non-zero deductible percentage
- default coverage percentage
- configured coverage percentage
- quote without registration location
- quote with GIS adjustment
- invalid vehicle year
- invalid negative monetary values

## Implementation Order

Recommended implementation order:

- create project bootstrap and tooling
- add domain calculation tests
- implement domain value objects and calculator
- add configuration model
- add application use case
- expose FastAPI endpoint
- add API integration tests
- add GIS adjustment adapter

This order keeps the business rules testable before adding HTTP delivery details.

## Open Questions

- Should monetary values use `Decimal` from the beginning instead of `float` internally?
- Should the API accept `float` for compatibility and convert to `Decimal` internally?
- Should `registration_location` require all address fields or allow partial location data?
- Should GIS failures block quote calculation or fall back to zero adjustment?
- Should `REFERENCE_YEAR` be required in production or optional with current year fallback?

These questions should be resolved through future ADRs or implementation tasks when the trade-offs become concrete.
