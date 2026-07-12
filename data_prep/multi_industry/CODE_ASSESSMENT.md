# Code assessment: what changes for the multi-industry calibration

> **STATUS (2026-07-10): IMPLEMENTED.** The changes mapped below now exist
> on this branch: `ogbra/constants.py` carries the concordances,
> `ogbra/input_output.py` reads the packaged MIP extracts (VA-content
> io_matrix, alpha_c, gamma with the Gollin-target rescale, employment,
> Solow-residual Z), `ogbra/create_multisector_calibration.py` writes the
> packaged M=10/I=7 overlay, `Calibration` fills the I/O objects offline,
> and the example loads the overlay. Tests re-derive the overlay from the
> packaged data. Not yet done: a multisector model solve, and per-industry
> cit_rate/tau_c from the staged Receita data.

Assessment only — **no code has been changed**. File:line references are to the
`multi-industry-data` branch as of 2026-07-09. Companion to `README.md` (data)
and `concordances/concordance.py` + `extract_10sectors_draft.py` (verified draft
extraction logic).

## 1. `ogbra/input_output.py` — full rewrite (the core change)

Currently hardwired to the IFPRI SAM: reads
`data/002_IFPRI_SAM_BRA_2018_SAM.csv` **at import time** (module level, lines
7–16), and `get_alpha_c`/`get_io_matrix` are keyed to `CONS_DICT`/`PROD_DICT`
IFPRI codes and `hhd-r*/u*` household columns.

Needs to become: read the IPEA MIP xlsx (`Usos` sheet for alpha_c + value
added; `D` sheet for the Pi^I bridge), aggregate via the Nível-67 concordance.
The verified parsing logic lives in `extract_10sectors_draft.py`:
- activity columns: `Usos` row 3 codes, cols 2–68
- household consumption: `Usos` col 73 ("Consumo das famílias")
- VA block: rows 141 (VAB), 142 (Remunerações), 148 (EOB+rendimento misto) —
  layout confirmed identical across year files (tested 2015/2018/2021)
- `D` sheet: 67 activities × 126 products, market shares

New function needed: **`get_gamma()`** (per-industry capital share from the VA
block) — does not exist today; the placeholder example guesses gamma.

Also fix in passing: move the module-level file read into a function (OG-PHL
already did this with `read_SAM()`).

## 2. `ogbra/constants.py:299–397` — replace the sector dictionaries

`CONS_DICT` (5 IFPRI consumption cats) and `PROD_DICT` (7 IFPRI production
cats) are replaced by the Nível-67 → 10-sector concordance
(`concordances/concordance.py`, verified: covers all 67 activities and all
126 products via 4-digit prefix).

**I-dimension: follow OG-PHL's multi-sector pattern (resolved 2026-07-09).**
The reference implementation is OG-PHL's m8-compat worktree
(`ogphl/create_multisector_calibration.py` + `ogphl/input_output.py`):
**I = 5 COICOP-style consumption goods ≠ M = 8 industries**, with the
io_matrix built by `get_io_matrix_value_added()` — the Leontief
**value-added-content** method (domestic technical coefficients,
`L = (I−A_d)^{-1}`, VA embodied per unit of final consumption), *not* the
direct SAM-block method. The IPEA MIP ships the needed pieces precomputed
(`An` = domestic tech coefficients, `Z` = Leontief inverse, `Usos Nacional` =
domestic-only use table — better than PHL's import-proportionality
approximation). Demo on 2018 data (`validate_and_i_demo.py`): I=5 gives
alpha_c = (food .196, energy/utilities .094, nondur .120, dur .101, services
.489) with genuinely mixed Pi^I rows (food = .31 agri + .28 mfg + .22 trade).
An I=6 variant splitting network utilities from fuels puts household utility
demand 50.5% on electricity_gas + 21.0% on water_waste. **I=7 (electricity as
its own consumption good, 2018 numbers):** alpha_c = (food .196, electricity
.027, water .009, fuels .057, nondur .120, dur .101, services .490); the
electricity row of Pi^I is 72.1% electricity_gas sector (rest = supply chain:
12.2% info/fin, 6.4% trade margins); the water row is 66.7% water_waste.
Household electricity = R$121bn vs water R$39bn (2018, consumer prices).
Data nuance: product 35001 is "Eletricidade, gás e outras utilidades" — one
product; piped gas can't be split off natively (bottled cooking gas/GLP is a
refino product, already in fuels), so the "electricity" good is the
elec-dominated network-utility bundle; a pure-power refinement would apply
ANEEL/ABEGÁS revenue shares to that one row/column later.

**DECIDED (user, 2026-07-09): I = 7** — Food & beverages, Electricity, Water,
Fuels, Non-durables, Durables, Services. Final design: **M = 10, I = 7**,
PHL-m8 machinery (VA-content io_matrix, gamma target-rescale to 0.428 with
public capital carved out, chi_b/chi_n units rescale, Solow-residual Z).
Also transplant from PHL m8: `get_Z` (Solow-residual TFP), the chi_b/chi_n
composite-consumption units rescale for I>1, and nu=0.2 TPI dampening.

## 3. `ogbra/calibrate.py` — the `update_from_api` semantics issue

- **Lines 48–49:** `alpha_c`/`io_matrix` are initialized only for the
  single-industry case (`p.I == 1` / `p.M == 1`); otherwise `None`.
- **Lines 51–52 + 66–80:** *all* I/O calibration is gated behind
  `update_from_api=True`. But the MIP is a **packaged file, not an API** — in
  the default offline path a multi-industry run gets `alpha_c=None`,
  `io_matrix=None` and no gamma. **The I/O block should move out of the
  API-gated section** so multi-industry calibration works offline (this is
  the main finding of the update-code review).
- **Lines 70–77:** asserts `p.I == len(alpha_c_dict)` and
  `p.M == len(io_df.keys())` — will hold with the 10-sector concordance once
  the I-dimension decision (above) is made.
- **`get_dict()` (126–136):** add `gamma` (and possibly per-industry
  `cit_rate`) to the returned dict.

`macro_params.py` itself needs **no changes** for multi-industry: World
Bank/IMF/UN ILO pulls are all economy-wide. (Note for later: its `requests`
calls send no User-Agent; IBGE/EPE endpoints reject bare clients with 403,
so any future direct IBGE/EPE fetch must send a browser UA — see
`fetch_data.sh`.)

## 4. `ogbra/update_baseline.py` — runs at default (single-industry) spec

Lines 14–26: builds `Specifications()` + packaged defaults, then
`Calibration(p, update_from_api=True)`. Since default `I = M = 1`, the
multi-industry branches never fire. Recommendation: keep the packaged
baseline single-industry (as today) and treat multi-industry as opt-in via
the example script; if a multi-industry baseline JSON is ever wanted,
`p.update_specifications({"M": 10, "I": ...})` must run *before* the
`Calibration` call.

## 5. Packaging & tests

- `pyproject.toml:80–84` (`[tool.setuptools.package-data]`): decide what ships
  in the wheel. One MIP year is ~0.7 MB xlsx; better to extract the needed
  arrays once and package small CSVs (like the current SAM csv, 20 KB).
- `tests/test_input_output.py` is keyed to the SAM structure — rewrite
  alongside `input_output.py`. `tests/test_calibrate.py` asserts the
  single-industry defaults — extend for M=10.
- `examples/run_og_bra_multi_industry.py` — replace the 2×2 placeholder
  (`io_matrix=np.eye(2)`, guessed gammas) with the M=10 calibration.

## 6. Known methodological caveats (from the verified 2018 run)

- **gamma & mixed income (approach decided 2026-07-09):** use the family
  standard — OG-PHL's `get_gamma(target_avg=...)`: raw sector capital shares
  rescaled multiplicatively so the VA-weighted mean hits an economy-wide
  target, then `PUBLIC_CAPITAL_SHARE` carved out of capital. Brazil
  improvement: IBGE separates EOB from rendimento misto (Usos rows 150/149),
  so the target is computable from Brazil's own accounts instead of an
  external number. 2018 totals: Rem 3,055,773 / EOB 2,287,642 / misto
  583,568 → raw capital share 0.484; **Gollin target (misto split like the
  rest of the economy) = EOB/(Rem+EOB) = 0.428** (PHL's was 0.588).
- **Pi^I and imports:** use `Usos Nacional` (domestic-only) for the bridge —
  exact, no import-proportionality assumption needed.
- **Benchmark validation DONE (2026-07-09):** IPEA 2015 household consumption
  matches the official IBGE 2015 MIP almost exactly — totals ratio 1.0023,
  124/125 common products within 1% (single outlier: product 50001, water
  transport, IPEA 10,407 vs IBGE 1,910 — flag to investigate, ~0.2% of total).
  See `validate_and_i_demo.py`.
