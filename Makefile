.SILENT:
.PHONY: all fmt build test lint ci proto

PY := python
PIP := pip
VENV_CMD := $(PY) -m venv .venv
ACTIVATE := . .venv/bin/activate

all: ci

fmt:
	@echo "Formatting project with black..."
	@$(PY) -m pip install --upgrade pip >/dev/null 2>&1 || true
	@$(PY) -m pip install black >/dev/null 2>&1 || true
	@$(PY) -m black .

lint:
	@echo "Running linters (flake8)..."
	@$(PY) -m pip install flake8 >/dev/null 2>&1 || true
	@$(PY) -m flake8 .

test:
	@echo "Running tests (pytest)..."
	@$(PY) -m pip install pytest >/dev/null 2>&1 || true
	@$(PY) -m pytest -q

build:
	@echo "Packaging (if applicable)..."
	@# Ejemplo: python -m build (requeriría pyproject.toml/setup.cfg)
	@echo "No packaging steps configured. Add build commands to Makefile if needed."

proto:
	@echo "No proto generation configured. Edit this target to run protoc if you use proto files."

ci: fmt lint test
	@echo "CI pipeline finished successfully."
