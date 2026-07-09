# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Consistency guard tests (`tests/test_consistency.py`): the packaged
  baseline must validate against the installed ogcore; every pre-time-path
  demographic seed the installed ogcore defines must be baked into the
  baseline (fails with a "regenerate demographics" message when ogcore
  changes its demographics interface); a feature canary and a wheel-RECORD
  integrity check that fail on stale or corrupted ogcore installs
  masquerading under a release version number. `pyproject.toml` now floors
  `ogcore>=0.16.3` so the packaged baseline and installed ogcore cannot
  silently drift apart.

### Changed

- Regenerated the packaged baseline demographics and earnings profile under
  ogcore 0.16.3 (mirrors OG-PHL#67 / OG-ZAF#134 / OG-IDN#52 / OG-ETH#63).
  ogcore 0.16.3 reworked the pre-time-path population handling
  (PSLmodels/OG-Core#1073): the transition arrays (`omega`, `g_n`,
  `imm_rates`) shift by one period and three new period-0 seeds
  (`g_n_preTP`, `imm_rates_preTP`, `rho_preTP`) feed the aggregation of
  investment, wealth, and bequests. A baseline baked under older ogcore is
  silently inconsistent under 0.16.3 — the baseline time path converged but
  failed the resource-constraint check (max error 0.024); with the
  regenerated demographics it passes (max error 0.0009). Updated the stale
  README runtime note (runs take roughly 7–9 minutes per scenario, not "35
  minutes to two hours").
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


