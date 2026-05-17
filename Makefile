.PHONY: format format-check install lint lint-fix test test-cov typecheck

PYTHON ?= python
BIN ?= .venv/bin

format:
	$(BIN)/ruff format .

format-check:
	$(BIN)/ruff format --check .

install:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	$(BIN)/ruff check .

lint-fix:
	$(BIN)/ruff check --fix .

test:
	$(BIN)/pytest

test-cov:
	$(BIN)/pytest --cov=craclx --cov-report=term-missing

typecheck:
	$(BIN)/mypy src tests
