# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-08-31 9:00:00

### Changed

- Calibration now works with OG-Core > 0.18.0, which has demographic parameters varying by income goup.
- Rewrote the installation instructions. The README now documents two install paths — the OG family universal installer (`bash install.sh --repo og-bra`, from OG-Core's `scripts/`) and a manual uv install — with complete, copy-pasteable per-platform blocks for macOS, Linux, and Windows, and a "what happens" note for the  example run (runtime, output locations, and the UN Data Portal token prompt fallback). Removed the PyPI install section and badges: the  `ogbra` package has never been published to PyPI, so `pip install ogbra` fails for everyone who tries it.
- Updated the contributor guide to the uv workflow: `uv sync --extra dev` and `uv run` replace the conda environment steps, which have  been broken since `environment.yml` was removed in 0.1.0. Fixed the test command to this repo's real marker set (`pytest -m "not local"`; the old text cited OG-USA's `needs_puf`/`regression` markers and 24-hour suite) and replaced stale `master`-branch references with `main`.

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


[0.2.0]: https://github.com/PSLmodels/OG-BRA/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/PSLmodels/OG-BRA/compare/v0.0.0...v0.1.0