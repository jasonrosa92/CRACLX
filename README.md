# CRACLX

Backend API for car insurance quote calculation.

## Overview

This repository contains the backend service for CRACLX. The project is planned as a Python and FastAPI backend using Domain-Driven Design, Clean Architecture, and Ports and Adapters.

The frontend is outside this repository.

## Documentation

- [Roadmap](docs/ROADMAP.md)
- [Working Agreement](docs/WORKING_AGREEMENT.md)
- [Project Bootstrap Plan](docs/PROJECT_BOOTSTRAP_PLAN.md)
- [ADR-0001: Backend Architecture](docs/adr/ADR-0001-backend-architecture.md)
- [SDR-0001: Backend System Design](docs/sdr/SDR-0001-backend-system-design.md)

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
make install
```

Run checks:

```bash
make format
make lint
make typecheck
make test
```

Run the API locally:

```bash
uvicorn craclx.bootstrap.app:create_app --factory --reload
```

Health check:

```text
GET /health
```

## Configuration

Business calculation parameters are loaded from environment variables or `.env`.

Available variables:

- `AGE_RATE_INCREMENT`: rate added for each vehicle age unit
- `AGE_UNIT_YEARS`: number of years represented by one age unit
- `COVERAGE_PERCENTAGE`: policy coverage percentage, defaulting to `1.00`
- `GIS_ADJUSTMENT_MAX`: maximum geographic risk adjustment
- `GIS_ADJUSTMENT_MIN`: minimum geographic risk adjustment
- `REFERENCE_YEAR`: optional year override for deterministic calculations
- `VALUE_RATE_INCREMENT`: rate added for each vehicle value unit
- `VALUE_RATE_UNIT`: monetary value represented by one value unit
