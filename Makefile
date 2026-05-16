.PHONY: format install lint test test-cov typecheck

format:
	ruff format .

install:
	python -m pip install -e ".[dev]"

lint:
	ruff check .

test:
	pytest

test-cov:
	pytest --cov=craclx --cov-report=term-missing

typecheck:
	mypy src tests
