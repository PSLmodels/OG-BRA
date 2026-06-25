# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-25 12:00:00

### Changed

- Migrated the project from conda to uv. Install with `uv sync --extra dev`; `pyproject.toml` is the single source of truth for dependencies and `uv.lock` pins exact versions.
- CI uses `astral-sh/setup-uv`, and ruff replaces black for formatting and linting (`check_format.yml` -> `check_ruff.yml`).
- Updated the README, `AGENTS.md`, and the Makefile to the uv workflow.

### Removed

- `setup.py`, `environment.yml`, `pytest.ini`, and `MANIFEST.in` (their settings moved into `pyproject.toml`).

## [0.0.0] - 2026-06-24 18:00:00

### Added

- This version is a pre-release alpha. The example run script OG-BRA/examples/run_og_bra.py runs, but the model is not currently calibrated to represent the Brazilan economy and population.


