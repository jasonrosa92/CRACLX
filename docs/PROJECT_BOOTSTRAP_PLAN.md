# Project Bootstrap Plan

## Purpose

This document defines the initial backend bootstrap plan before implementation code is created.

The goal is to create a predictable project structure that supports the roadmap, architecture decision, system design, TDD workflow, and release-based branch strategy.

## Bootstrap Scope

The bootstrap task must prepare the backend repository for implementation.

Expected outcomes:

- Python project metadata configured
- source package structure created
- test structure created
- FastAPI application entrypoint prepared
- configuration structure prepared
- tooling commands documented
- dependencies grouped by runtime and development usage
- initial quality gates prepared

The bootstrap must not implement business calculation behavior. Business rules start in `r2`.

## Proposed Project Layout

The backend should use a `src` layout:

```text
src/
  craclx/
    __init__.py
    api/
      __init__.py
    application/
      __init__.py
    bootstrap/
      __init__.py
    domain/
      __init__.py
    infrastructure/
      __init__.py
tests/
  integration/
  unit/
docs/
  adr/
  sdr/
```

The `src` layout keeps package imports explicit and helps tests exercise the installed package instead of accidentally importing local files by path.

## Initial Files

The bootstrap should introduce these initial files:

- `.env.example`
- `.gitignore`
- `README.md`
- `pyproject.toml`
- `src/craclx/__init__.py`
- `src/craclx/bootstrap/__init__.py`
- `src/craclx/bootstrap/app.py`
- `tests/__init__.py`
- `tests/integration/__init__.py`
- `tests/unit/__init__.py`

Optional files may be added if they directly support local development:

- `Makefile`
- `pytest.ini`
- `.python-version`

## Dependency Plan

Runtime dependencies:

- `fastapi`
- `pydantic`
- `pydantic-settings`
- `uvicorn`

Development dependencies:

- `httpx`
- `mypy`
- `pytest`
- `pytest-cov`
- `ruff`

Dependency versions should be pinned or constrained in `pyproject.toml` to make the test environment reproducible.

## Tooling Plan

The project should use:

- `ruff` for linting and formatting
- `mypy` for static type checking
- `pytest` for automated tests
- `pytest-cov` for coverage reporting

The initial tooling should support these commands:

```text
lint
format
typecheck
test
test-cov
```

The exact command runner may be either `Makefile` targets or documented commands in `README.md`.

## Package Design

The root Python package should be:

```text
craclx
```

Initial package responsibilities:

- `craclx.api`: HTTP routes and schemas
- `craclx.application`: use cases and ports
- `craclx.bootstrap`: application factory and dependency wiring
- `craclx.domain`: business model and calculation rules
- `craclx.infrastructure`: settings, adapters, and technical integrations

The bootstrap phase should create the package boundaries without implementing domain behavior.

## FastAPI Bootstrap

The initial FastAPI bootstrap should expose an app factory:

```text
create_app() -> FastAPI
```

The app factory may include:

- application title
- application version
- health endpoint if useful for smoke testing
- router inclusion points

Business quote endpoints should be implemented later in `r3`.

## Configuration Bootstrap

Configuration should be prepared for future calculation parameters.

Initial configuration should support:

- environment variables
- `.env` usage for local development
- validation through `pydantic-settings`
- deterministic overrides for tests

The bootstrap may create a settings object, but calculation parameters should be implemented when the domain engine is introduced in `r2`.

## Test Bootstrap

The test structure should support:

- unit tests for domain and application logic
- integration tests for FastAPI behavior
- deterministic configuration overrides

The bootstrap may include a simple smoke test only if needed to validate the app factory.

Business calculation tests belong to `r2`.

## Quality Gates

The bootstrap should prepare local quality gates:

- formatting passes
- linting passes
- type checking passes
- tests pass

These gates will become stronger as implementation grows.

## Implementation Order

Recommended bootstrap order:

- create the project metadata
- create the package directory structure
- create initial config and app factory placeholders
- create test directory structure
- add basic tooling configuration
- add README instructions
- run local quality commands

This order keeps the project reviewable at each step.

## Commit Plan

The bootstrap implementation should use task branches from `develop`.

Suggested first implementation branch:

```text
chore/r1/006/bootstrap-python-project
```

Suggested commit:

```text
chore(repo): bootstrap python backend project #006

- add python project metadata and package layout
- configure test and quality tooling
- prepare FastAPI app factory entrypoint
```

## Acceptance Criteria

The bootstrap is complete when:

- the repository has a valid Python project structure
- package boundaries match the documented architecture
- tooling commands are documented and runnable
- tests can be discovered by `pytest`
- no business calculation logic is introduced before `r2`
- the working tree is clean after commit
- the branch is published and merged into `develop`

## Follow-up Work

After bootstrap, the project should move to `r2`.

Next expected release focus:

- write domain calculation tests
- implement dynamic rate calculation
- implement premium calculation
- implement policy limit calculation
- introduce configurable calculation parameters
