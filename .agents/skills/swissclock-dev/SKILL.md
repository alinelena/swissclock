---
name: swissclock-dev
description: >-
  Use this skill to understand the software engineering stack, project setup, and standard workflows for the Swissclock repository. Activate when you need to run tests, add dependencies, or lint code.
---

# Swissclock Development Guide

This skill outlines the software engineering practices, tooling stack, and local development setup for the `swissclock` project.

## 1. Environment & Dependency Management
- **Environment**: Always run commands within the `janus` micromamba environment. Prefix your commands with: `micromamba run -n janus <command>`
- **Dependencies**: The project uses `uv` for blazing-fast package management instead of standard `pip`. 
  - To install packages: `micromamba run -n janus uv pip install <package>`

## 2. Linting and Formatting
- **Ruff**: The project uses Ruff as its primary linter and formatter.
  - Run linter: `micromamba run -n janus uv run ruff check src tests`
  - Run formatter: `micromamba run -n janus uv run ruff format src tests`
  - Auto-fix issues (e.g. import sorting): `micromamba run -n janus uv run ruff check --fix src tests`
- **Pre-commit**: The repository uses `pre-commit` to enforce Ruff checks automatically on `git commit`. The configuration is in `.pre-commit-config.yaml`.

## 3. Testing
- **Framework**: `pytest` is used for unit testing, in combination with `pytest-qt` to handle the `PySide6` UI widgets.
- **Coverage**: Handled by `pytest-cov`. To run tests and see the coverage report:
  `micromamba run -n janus uv run pytest --cov=swissclock --cov-report=term-missing`
- **Headless UI Testing**: If running in a headless environment (like GitHub Actions or a background agent task), tests must be wrapped in `xvfb-run` to mock an X11 display:
  `xvfb-run micromamba run -n janus uv run pytest`
- **Matrix Testing**: `tox` is configured (`tox.ini`) to test against Python 3.11, 3.12, 3.13, and 3.14. Run the full suite with:
  `micromamba run -n janus tox`

## 4. CI/CD (GitHub Actions)
- **Tests**: `.github/workflows/test.yml` runs the Tox matrix on `ubuntu-latest` using `xvfb-run`, and uploads coverage to Coveralls.
- **Releases**: `.github/workflows/publish.yml` is configured for PyPI Trusted Publishing (OIDC) when a new release is cut.
