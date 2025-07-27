.PHONY: help install install-dev test test-cov lint format type-check check clean build docs serve-docs

# Default target
help:
	@echo "VimGym Development Commands"
	@echo "=========================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  install         Install production dependencies"
	@echo "  install-dev     Install development dependencies"
	@echo ""
	@echo "Development Commands:"
	@echo "  test           Run tests"
	@echo "  test-cov       Run tests with coverage report"
	@echo "  lint           Run linting (flake8)"
	@echo "  format         Format code (black)"
	@echo "  type-check     Run type checking (mypy)"
	@echo "  check          Run all quality checks (lint, format, type-check, test)"
	@echo ""
	@echo "Build Commands:"
	@echo "  clean          Clean build artifacts"
	@echo "  build          Build package"
	@echo ""
	@echo "Documentation:"
	@echo "  docs           Build documentation"
	@echo "  serve-docs     Serve documentation locally"
	@echo ""

# Setup commands
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install --upgrade pip
	pip install -r requirements-dev.txt
	pip install -e .

# Development commands
test:
	pytest

test-cov:
	pytest --cov=vimgym --cov-report=html --cov-report=term

lint:
	flake8 vimgym/ tests/

format:
	black vimgym/ tests/

format-check:
	black --check vimgym/ tests/

type-check:
	mypy vimgym/

check: format-check lint type-check test
	@echo "✅ All quality checks passed!"

# Build commands
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

# Documentation commands (placeholder for future use)
docs:
	@echo "📖 Documentation building not yet implemented"
	@echo "Current docs are in markdown format in docs/"

serve-docs:
	@echo "📖 Documentation serving not yet implemented"
	@echo "Current docs are in markdown format in docs/"

# CLI shortcuts
hello:
	vimgym hello

status:
	vimgym status

cli-help:
	vimgym --help