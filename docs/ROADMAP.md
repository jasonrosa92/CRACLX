# Backend Roadmap

## Vision

Build a backend API for car insurance quote calculation using Python and FastAPI.

The backend must expose a clear and stable contract for future frontend integration while keeping business rules isolated, configurable, and covered by automated tests.

The project will be delivered incrementally through release-based branches and numbered tasks. Each release must leave the repository in a reviewable and working state.

## Delivery Scope

The backend will provide the following capabilities:

- calculate a dynamic insurance rate based on vehicle age and vehicle value
- calculate the base premium, deductible discount, and final premium
- calculate the base policy limit, deductible value, and final policy limit
- return the input car details together with calculated quote values
- keep all business parameters configurable through environment variables or configuration files
- expose the calculation through a FastAPI endpoint
- document architecture decisions, software design, and development workflow
- support automated tests following a TDD-oriented workflow
- prepare an extension point for optional GIS-based geographic risk adjustment

## Out Of Scope

The following items are intentionally outside the initial backend scope:

- frontend application
- user authentication and authorization
- quote persistence in a database
- payment processing
- policy issuance workflow
- production GIS provider contract
- asynchronous job processing
- multi-tenant support
- production deployment automation before a deployment target is defined

These items may be revisited after the core backend contract and calculation engine are complete.

## Release Plan

### r1: Backend Foundation And Documentation

Goal: define how the backend will be planned, documented, structured, and delivered.

Expected outcomes:

- roadmap documented
- branch, commit, and release conventions documented
- initial architecture decision documented
- initial software design documented
- backend-only scope explicitly defined
- project execution plan ready before code implementation starts

### r2: Domain Calculation Engine

Goal: implement the core quote calculation rules without coupling them to FastAPI or infrastructure.

Expected outcomes:

- domain model defined
- dynamic rate calculation implemented
- premium calculation implemented
- policy limit calculation implemented
- configurable calculation parameters introduced
- unit tests covering the main business scenarios

### r3: Application And API Contract

Goal: expose the calculation engine through a stable FastAPI contract.

Expected outcomes:

- quote calculation use case implemented
- request and response schemas implemented
- FastAPI route implemented
- validation behavior documented and tested
- API integration tests added
- OpenAPI contract available through FastAPI

### r4: Quality, Tooling, And Developer Experience

Goal: make the backend easier to run, test, review, and maintain.

Expected outcomes:

- linting configured
- formatting configured
- type checking configured
- test commands documented
- local developer workflow documented
- GitHub Actions CI pipeline configured to run the same local validation gates
- CD kept intentionally pending until the production deployment target is defined

### r5: GIS Risk Adjustment

Goal: add a replaceable extension point for geographic risk adjustment.

Expected outcomes:

- geographic risk provider port defined
- fake or configurable GIS adapter implemented
- rate adjustment constrained by configuration
- tests covering the optional adjustment behavior
- design prepared for a future real GIS integration

## Initial Task Breakdown

### r1 Tasks

- `#001`: Define backend roadmap
- `#002`: Define backend working agreement
- `#003`: Define initial architecture decision
- `#004`: Define initial software design record
- `#005`: Define project bootstrap plan

### r2 Tasks

- `#001`: Add domain calculation test cases
- `#002`: Implement dynamic rate calculation
- `#003`: Implement premium calculation
- `#004`: Implement policy limit calculation
- `#005`: Add configurable calculation parameters

### r3 Tasks

- `#001`: Implement quote calculation use case
- `#002`: Add API request and response schemas
- `#003`: Add FastAPI quote endpoint
- `#004`: Add API integration tests
- `#005`: Document API contract

### r4 Tasks

- `#001`: Configure formatting and linting
- `#002`: Configure type checking
- `#003`: Add developer command documentation
- `#004`: Add GitHub Actions CI pipeline

### r5 Tasks

- `#001`: Define GIS adjustment port
- `#002`: Implement configurable GIS adjustment adapter
- `#003`: Add GIS adjustment tests
- `#004`: Document future GIS integration path

## Acceptance Criteria

The backend delivery will be considered complete when:

- all required quote calculation rules are implemented
- all business parameters can be changed without modifying calculation code
- the API returns the required input echo and calculated output fields
- automated tests cover the main calculation scenarios
- the domain calculation logic can be tested without starting FastAPI
- documentation explains the roadmap, architecture, design, and workflow
- branch names follow the release and task pattern
- commit messages include the task id in the title and bullet points in the body

## Branch Strategy

The repository will follow this flow:

```text
main -> develop -> task branch
```

Task branches must follow this format:

```text
<type>/r<release-number>/<task-number>/<short-description>
```

Examples:

```text
docs/r1/001/define-backend-roadmap
docs/r1/002/define-backend-working-agreement
feat/r2/002/implement-dynamic-rate-calculation
test/r3/004/add-api-integration-tests
```

## Commit Strategy

Commits must follow Conventional Commits and include the task id in the title:

```text
<type>(<scope>): <description> #<task-number>
```

Commit bodies must use bullet points:

```text
docs(roadmap): define backend roadmap #001

- describe backend vision and delivery scope
- define release plan and initial task breakdown
- document acceptance criteria and out-of-scope items
```
