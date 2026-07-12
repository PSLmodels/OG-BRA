# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Multi-industry calibration (M = 9 industries, I = 7 consumption
  goods) from the Brazilian input-output tables (Alves-Passoni & Freitas
  2023, built on the IBGE Supply and Use Tables; the packaged extracts
  and their provenance live in `ogbra/data` and
  `data_prep/multi_industry`). Electricity and water are broken out as
  their own industries and consumption goods so energy and water are
  tracked separately; real estate (imputed dwelling rent) is grouped with
  finance and business services, the standard FIRE aggregation.
  `ogbra.input_output` now provides `get_alpha_c`,
  `get_io_matrix` (domestic value-added content, Leontief), `get_gamma`
  (capital shares with mixed income split between labor and capital by
  Gollin's second adjustment, then anchored to the economy-wide capital
  share), `get_employment`, and `get_Z` (Solow-residual TFP);
  `ogbra.create_multisector_calibration` assembles them into the
  packaged `ogbra_multisector_default_parameters.json` overlay, and the
  multi-industry example loads that overlay instead of the previous
  two-sector placeholder. The IFPRI SAM-based functions and dictionaries
  are replaced. The Calibration class fills `alpha_c` and `io_matrix`
  from the packaged data in offline mode (they are not API-dependent).
- Per-good effective consumption tax rates (`get_tau_c`, from the use
  table's taxes-on-products column; electricity 0.34, services 0.06,
  weighted average equal to the single rate) and per-industry effective
  corporate tax rates (`get_cit_rate`, Receita Federal IRPJ + CSLL
  collections by CNAE section over gross operating surplus, packaged as
  `ogbra/data/rfb_cit_by_section.csv`) in the multi-industry overlay.
- A continuation (homotopy) steady-state solver for the multi-industry
  model in `examples/run_og_bra_multi_industry.py`, following OG-PHL:
  flat-gamma anchor, adaptive morph to the calibrated economy, the
  baseline transition path off the converged steady state, and a small
  illustrative reform (a corporate income tax cut) for comparison. The
  overlay funds public capital (`alpha_I = 0.02`,
  `delta_g_annual = 0.047`, `initial_Kg_ratio = 0.35`) because
  `gamma_g > 0` with zero public investment leaves the production side
  inconsistent, and keeps manufacturing last as the numeraire.
- A same-economy equivalence test
  (`tests/test_multisector_equivalence.py`): at `gamma_g = 0` the
  M = 9, I = 7 configuration with the utility-weight units conversion
  reproduces the M = 1 economy to machine precision. (With
  `gamma_g > 0`, disaggregation itself changes the equilibrium because
  public capital is common and nonrival — documented in the firms
  chapter.)
- A multi-industry section in the firms calibration chapter
  (`docs/book/content/calibration/firms.md`): industries, capital
  shares, the value-added-content input-output matrix (with a direct-use
  comparison), Solow-residual sector TFP, the per-good and per-industry
  tax rates, the units conversion, and how to interpret the solved
  steady state.

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


