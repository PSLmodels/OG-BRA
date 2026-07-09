# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Upgraded `ogcore` to 0.16.3 in `uv.lock` (includes the OG-Core time-path
  pre-population restructuring and `g_n` boundary-convention change from
  PSLmodels/OG-Core#1073).
- Dropped Python 3.11 support to follow `ogcore` (>=0.16.2 requires Python
  >=3.12). On 3.11, dependency resolution silently fell back to `ogcore`
  0.16.1. `requires-python` is now `>=3.12, <3.14`; the CI matrix tests
  3.12 and 3.13; ruff targets py312.

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


