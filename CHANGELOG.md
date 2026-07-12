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

- `debt_ratio_ss` updated from 1.0 to 0.99, the IMF 2025 Article IV
  projection of Brazil's general government gross debt stabilizing at
  about 99% of GDP in 2030.
- Turned on public capital: `alpha_I` 0.0 -> 0.02 (general-government
  public investment, IMF Article IV) and `gamma_g` 0.0 -> 0.05 (public
  capital share in production, carved out of the capital share following
  OG-PHL, so private `gamma` falls 0.40719 -> 0.35719). Previously
  infrastructure spending and public capital played no role in the model.
- Calibrated the public capital stock side to IMF PIMA/ICSD data:
  `initial_Kg_ratio` 0.2 -> 0.35 (Brazil's measured general government
  capital stock, 2015) and `delta_g_annual` 0.02 -> 0.047, the depreciation
  implied by the steady-state identity Kg/Y = alpha_I/(g + delta_g) at the
  observed stock and investment. With the ogcore defaults the model would
  have built public capital to 66% of GDP, twice the measured level.
  `tests/test_public_capital.py` enforces the identity.
- `eta` (distribution of aggregate transfers across households) rebuilt to
  reflect Brazilian transfer targeting instead of the population-proportional
  default: Bolsa Família, BPC, and unemployment insurance/abono incidence
  (World Bank and CEQ sources) blended by expenditure weight gives the
  bottom lifetime-earnings quartile 58% of transfers (was 25%) and the top
  1% essentially none. Age profiles within groups unchanged.
- Personal income tax rates recalibrated from the Receita Federal Grandes
  Números DIRPF tables for calendar 2024 (41.7 million declarations):
  `etr_params` 0.12 -> 0.07 (total income tax over total declared income,
  including exclusive-taxation withholding and exempt income),
  `mtrx_params` 0.18 -> 0.22 (taxable-income-weighted statutory marginal),
  `mtry_params` 0.18 -> 0.12 (composition-weighted marginal on capital
  income under the 2026 dividend-tax law). The old values were stylized;
  the taxes chapter documents the arithmetic and the alternative concepts.
- `frac_tax_payroll` updated from 0.0 to 0.57, computed from Receita
  Federal collection data (social contributions over social contributions
  plus personal income taxes, 2022–2025 average). With 0.0, all household
  income and payroll tax revenue was reported as income tax.
- Switched the pension system from the inert "US-Style Social Security"
  placeholder (USA AIME/PIA parameters with `PIA_rate_bkt_1 = 0`, i.e.
  essentially no public pensions) to OG-Core's "Defined Benefits" system
  calibrated to the post-2019-reform RGPS: `retirement_age = 65`,
  `avg_earn_num_years = 45` (full-career averaging), `yr_contrib = 35`, and
  `alpha_db = 0.0289` anchored so steady-state pension outlays equal 12.5%
  of GDP (Brazil's total public pension spending is 12–13.2% of GDP; the
  statutory accrual implies 11.1% in the model). Requires the OG-Core
  Defined Benefits bug fix (see the pensions section of the government
  calibration chapter).
- Regenerated the packaged baseline demographics and earnings profile under
  ogcore 0.16.3 (mirrors OG-PHL#67 / OG-ZAF#134 / OG-IDN#52 / OG-ETH#63).
  ogcore 0.16.3 reworked the pre-time-path population handling
  (PSLmodels/OG-Core#1073): the transition arrays (`omega`, `g_n`,
  `imm_rates`) shift by one period and three new period-0 seeds
  (`g_n_preTP`, `imm_rates_preTP`, `rho_preTP`) feed the aggregation of
  investment, wealth, and bequests. A baseline baked under older ogcore is
  silently inconsistent under 0.16.3 — the baseline time path converged but
  failed the resource-constraint check (max error 0.024); with the
  regenerated demographics it passes (max error 0.0009). Macro, tax, and
  industry parameters are untouched. Updated the stale README runtime note
  (runs take roughly 7–9 minutes per scenario, not "35 minutes to two
  hours").

- `zeta_K` updated from 0.9 to 0.16, the normalized Chinn-Ito
  capital-account openness index for Brazil (2022 update), following the
  approach used in the OG-ZAF single-industry refresh. The old value implied
  near-total foreign absorption of excess capital demand.

- `tau_bq` updated from 0.2 to 0.04 to reflect Brazil's ITCMD (state
  inheritance/gift tax, Senate-capped at 8%, state schedules 2–8%). The old
  value had no Brazilian basis. Also fixed the taxes chapter, which
  incorrectly stated that bequest taxes are set to zero.

- `tau_c` updated from 0.09 to 0.13. The old value covered only the federal
  PIS + COFINS rate; the new value is the effective indirect tax rate on
  household consumption (taxes on products net of subsidies / pre-tax
  consumption) computed from the Alves-Passoni & Freitas (2023) annual
  input-output tables for Brazil (stable at 0.124–0.133 over 2015–2021).

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


