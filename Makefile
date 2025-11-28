.PHONY: help test lint format clean install test-docker

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests with coverage"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Clean cache and build files"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	@echo "Running Black..."
	@black --check app tests
	@echo "Running isort..."
	@isort --check app tests
	@echo "Running Flake8..."
	@flake8 app tests
	@echo "Running MyPy..."
	@mypy app

format:
	black app tests
	isort app tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage
