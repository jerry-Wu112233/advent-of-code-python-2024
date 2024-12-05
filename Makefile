.PHONY: install dev lint format

# Install the main dependencies
install:
	poetry install --no-root

# Install development dependencies (linting and formatting tools)
dev:
	pip install poetry
	poetry install --with dev

# Lint the code with flake8
lint:
	poetry run flake8 .

# Format the code with black and sort imports with isort
format:
	poetry run black .
	poetry run isort .