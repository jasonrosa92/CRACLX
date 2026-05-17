# Developer Commands

This document describes the local commands used to develop, validate, and run the backend.

The same commands should be used by CI/CD so local feedback and remote validation stay aligned.

## Environment Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project with development dependencies:

```bash
make install
```

The `Makefile` runs tools through the active Python interpreter. If a different Python executable is needed, override `PYTHON`:

```bash
make test PYTHON=/path/to/venv/bin/python
```

## Local Validation

Run the full local validation suite before opening or merging a branch:

```bash
make format-check
make lint
make typecheck
make test
```

Command responsibilities:

- `make format-check`: verifies code formatting with Ruff without changing files
- `make lint`: checks code quality rules with Ruff
- `make typecheck`: validates static typing with `mypy` in strict mode
- `make test`: runs the automated test suite with `pytest`

Run coverage when changing business behavior or API contracts:

```bash
make test-cov
```

## Automatic Fixes

Apply formatting:

```bash
make format
```

Apply safe lint fixes:

```bash
make lint-fix
```

After running automatic fixes, run the full local validation suite again before committing.

## Run The API

Start the FastAPI application locally:

```bash
uvicorn craclx.bootstrap.app:create_app --factory --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Quote endpoint:

```text
POST /quotes
```

The request and response contract is documented in [API Contract](API_CONTRACT.md).

## Continuous Integration

GitHub Actions runs the backend validation pipeline on pull requests and pushes to `develop` and `main`.

The CI pipeline intentionally mirrors the local validation commands:

```bash
make install
make format-check
make lint
make typecheck
make test
```

If a command fails in CI, reproduce it locally with the same `make` target before changing the workflow.
