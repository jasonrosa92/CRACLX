# ADR-0001: Backend Architecture

## Status

Accepted

## Date

2026-05-16

## Context

The project must provide a backend API for car insurance quote calculation using Python and FastAPI.

The backend must support configurable business rules, automated tests, a stable API contract, and a future extension point for GIS-based geographic risk adjustment.

The frontend will be developed separately. This repository must therefore focus on backend responsibilities, API contracts, domain behavior, and delivery documentation.

The core business capabilities include:

- dynamic rate calculation based on vehicle age and vehicle value
- premium calculation using applied rate, deductible percentage, and broker fee
- policy limit calculation using coverage percentage and deductible percentage
- optional geographic risk adjustment using a replaceable GIS provider

The implementation must avoid coupling business rules to HTTP, frameworks, environment variables, or external services.

## Decision

We will implement the backend as a modular monolith using FastAPI, Domain-Driven Design, Clean Architecture, and Ports and Adapters.

Domain-Driven Design will guide the business model and language used in the code. Clean Architecture will define the dependency direction between layers. Ports and Adapters will isolate external concerns such as configuration sources and GIS providers.

FastAPI will be used only as the HTTP delivery mechanism. It must not own business calculation rules.

## Architecture Style

The backend will be organized around these layers:

- `domain`
- `application`
- `infrastructure`
- `api`
- `bootstrap`

The dependency direction must be:

```text
api -> application -> domain
infrastructure -> application/domain
bootstrap -> api/application/infrastructure
```

The domain layer sits at the center. Outer layers may depend on inner layers, but inner layers must not depend on outer layers.

## Domain Layer

The domain layer owns the business model and calculation rules.

Expected responsibilities:

- vehicle and quote concepts
- value objects for money, rate, deductible, and address when needed
- dynamic rate calculation rules
- premium calculation rules
- policy limit calculation rules
- domain services for quote calculation
- domain exceptions and invariants

Rules:

- must not import FastAPI
- must not import HTTP request or response schemas
- must not read environment variables directly
- must not call external GIS services directly
- must be testable without starting the application

## Application Layer

The application layer owns use cases and orchestration.

Expected responsibilities:

- quote calculation use case
- input and output application DTOs when needed
- ports for external capabilities
- coordination between domain services and infrastructure adapters

Rules:

- may depend on the domain layer
- must not depend on FastAPI route handlers
- must not implement technical infrastructure details
- should define ports for external integrations such as GIS risk adjustment

## Infrastructure Layer

The infrastructure layer owns technical implementations.

Expected responsibilities:

- configuration loading
- configuration validation
- GIS provider adapters
- logging setup
- external service clients when needed

Rules:

- must implement ports defined by the application layer
- must not move business calculation rules out of the domain layer
- must keep configuration details outside domain logic

## API Layer

The API layer owns HTTP delivery.

Expected responsibilities:

- FastAPI routers
- request schemas
- response schemas
- HTTP validation behavior
- exception mapping
- OpenAPI documentation

Rules:

- must call application use cases
- must not calculate premiums directly
- must not calculate policy limits directly
- must not implement GIS risk logic directly

## Bootstrap Layer

The bootstrap layer owns dependency wiring.

Expected responsibilities:

- create the FastAPI application
- load settings
- instantiate use cases
- connect infrastructure adapters to application ports
- include API routers

Rules:

- must keep object construction explicit
- must avoid hiding business behavior in dependency wiring

## Configuration Strategy

All business parameters must be configurable outside the calculation code.

Examples:

- rate increment per vehicle age unit
- vehicle age unit
- rate increment per value band
- value band size
- default coverage percentage
- minimum GIS adjustment
- maximum GIS adjustment
- reference year strategy for deterministic tests

The code must avoid hard-coded business numbers in calculation logic.

## Testing Strategy

The architecture must support a TDD-oriented workflow.

Expected test boundaries:

- domain unit tests for calculation rules
- application tests using fake ports
- API integration tests for HTTP contracts
- configuration tests for parameter loading and validation

The domain calculation engine must be testable independently from FastAPI.

## Consequences

Positive consequences:

- business rules remain isolated from framework concerns
- calculation rules can be tested quickly and deterministically
- API contracts can evolve without rewriting the domain
- GIS integration can start as a fake adapter and later become a real provider
- backend and frontend can evolve independently

Trade-offs:

- the project starts with more structure than a single-file FastAPI application
- dependency wiring must be explicit
- developers must respect the layer boundaries to preserve the architecture

## Alternatives Considered

### Single-layer FastAPI application

Rejected because it would mix HTTP handling, configuration, and business rules, making the project harder to test and evolve.

### Full microservices architecture

Rejected because the current scope is a focused backend service. A modular monolith provides strong internal boundaries without unnecessary operational complexity.

### Script-style calculator

Rejected because the requirements call for configurability, future changes, API exposure, automated tests, and optional GIS integration.
