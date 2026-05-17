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

The `Makefile` uses `.venv/bin` by default. If a different virtual environment is needed, override `BIN`:

```bash
make test BIN=/path/to/venv/bin
```
