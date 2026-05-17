.PHONY: format format-check install lint lint-fix test test-cov typecheck

PYTHON ?= python

format:
	$(PYTHON) -m ruff format .

format-check:
	$(PYTHON) -m ruff format --check .

install:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	$(PYTHON) -m ruff check .

lint-fix:
	$(PYTHON) -m ruff check --fix .

test:
	$(PYTHON) -m pytest

test-cov:
	$(PYTHON) -m pytest --cov=craclx --cov-report=term-missing

typecheck:
	$(PYTHON) -m mypy src tests
