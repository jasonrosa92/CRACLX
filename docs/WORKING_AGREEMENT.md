# Backend Working Agreement

## Purpose

This document defines how the backend project will be planned, implemented, reviewed, and delivered.

The goal is to keep the work incremental, auditable, and aligned with the roadmap before implementation starts.

## Repository Flow

The repository must follow this branch flow:

```text
main -> develop -> task branch
```

Branch responsibilities:

- `main`: stable branch for completed releases
- `develop`: integration branch for the next release
- task branches: short-lived branches created from `develop`

Task branches must be merged back into `develop`. The `develop` branch must be merged into `main` only when a release is complete.

## Branch Naming

Task branches must follow this format:

```text
<type>/r<release-number>/<task-number>/<short-description>
```

Rules:

- `type` must describe the nature of the work
- `r<release-number>` must identify the target release
- `task-number` must match the roadmap task number
- `short-description` must use kebab-case

Allowed branch types:

- `docs`
- `feat`
- `fix`
- `test`
- `refactor`
- `chore`
- `ci`

Examples:

```text
docs/r1/002/define-backend-working-agreement
docs/r1/003/define-backend-architecture
feat/r2/002/implement-dynamic-rate-calculation
test/r3/004/add-api-integration-tests
```

## Commit Message Format

Commits must follow Conventional Commits and include the task id in the title:

```text
<type>(<scope>): <description> #<task-number>
```

The commit body must use bullet points:

```text
docs(repo): define backend working agreement #002

- document branch and commit conventions
- define delivery workflow and merge rules
- register TDD and definition of done practices
```

Allowed commit types:

- `docs`
- `feat`
- `fix`
- `test`
- `refactor`
- `chore`
- `ci`

Allowed commit scopes:

- `repo`
- `roadmap`
- `adr`
- `sdr`
- `domain`
- `application`
- `api`
- `config`
- `test`
- `ci`

## Delivery Rules

Each task branch should focus on one roadmap task.

Rules:

- do not mix unrelated tasks in the same branch
- do not mix frontend work into the backend repository
- do not introduce implementation code before the related documentation task is clear
- keep commits small enough to review
- keep task numbers consistent across branch names and commit titles

## Architecture Principles

The backend will follow a modular monolith approach with Domain-Driven Design, Clean Architecture, and Ports and Adapters.

Layer responsibilities:

- domain owns business rules
- application owns use cases and ports
- infrastructure owns technical adapters
- api owns HTTP delivery
- bootstrap owns dependency wiring

Dependency direction:

```text
api -> application -> domain
infrastructure -> application/domain
bootstrap -> api/application/infrastructure
```

Rules:

- domain must not depend on FastAPI
- domain must not depend on Pydantic HTTP schemas
- domain must not read environment variables directly
- domain must not call external services directly
- api must not implement business calculations
- infrastructure must implement ports defined by the application layer

## Configuration Rules

Business parameters must be externally configurable.

Examples:

- rate increment by vehicle age
- vehicle age unit
- rate increment by value band
- value band size
- default coverage percentage
- minimum GIS adjustment
- maximum GIS adjustment

The calculation code must avoid hard-coded business numbers.

## TDD Rules

Development should follow a TDD-oriented workflow whenever practical.

Expected flow:

```text
write failing test -> implement minimum behavior -> refactor -> validate
```

Test expectations:

- domain rules must have unit tests
- application use cases must be testable with fake ports
- API contracts must have integration tests
- configuration behavior must be covered when it affects business rules

## Definition Of Done

A task is done when:

- the implementation or documentation matches the roadmap task
- tests were added or updated when behavior changed
- relevant checks pass locally
- business rules remain outside the API layer
- configurable values remain outside calculation logic
- commit messages follow the agreed format
- the branch is ready to merge into `develop`

## Merge Rules

Task branches must target `develop`.

Merge expectations:

- the branch should have a clear task scope
- the working tree must be clean before merge
- the task branch should be pushed to the remote before merge
- merge into `develop` should happen after review or explicit approval
- `develop` should merge into `main` only at release completion

## Release Rules

Release work must follow the roadmap.

Expected release flow:

```text
task branches -> develop -> main
```

The `main` branch should represent completed and stable releases. The `develop` branch may contain completed tasks for the next release.

## Backend And Frontend Boundary

This repository is dedicated to the backend.

Rules:

- frontend implementation must live in a separate project or repository
- backend must expose stable API contracts for frontend consumption
- backend documentation may mention frontend integration only as an external consumer
- backend tasks must not include frontend UI implementation
