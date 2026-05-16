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
