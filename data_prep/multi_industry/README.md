# Multi-industry calibration — data collection (preliminary)

Staging area for the data needed to build OG-BRA's multi-industry calibration
(the agreed **M=10** sector list) and the OG-CLEWS energy linkage. This is
exploratory: raw source files as downloaded, plus provenance and status notes.
Nothing here is wired into the `ogbra` package yet.

**Collected 2026-07-09.** Branch: `multi-industry-data`.

## Agreed 10-sector target (for reference)
1 Agriculture, forestry & fishing · 2 Mining & extractives · 3 Manufacturing ·
4 Electricity & gas (CLEWS) · 5 Water, sewage & waste (CLEWS) · 6 Construction ·
7 Trade, transport & accommodation · 8 Info/financial/business services ·
9 Real estate & dwellings · 10 Public, social & other services.

---

## Status summary

| Source | What it provides | Coverage | Status |
|---|---|---|---|
| **IPEA/UFRJ annual MIP** (`io_ipea_ufrj/`) | Full IO tables: supply/make, use, taxes, margins, technical coeffs, market-share `D`, value added, final demand | 42-sector **2000–2021**; 67-sector **2010–2021** | ✅ **collected + parsed end-to-end** |
| **EPE BEN energy balances** (`energy_epe/`) | Electricity generation by source, transformation, consumption by sector (physical, tep) | annual **1970–2024** | ✅ **collected** |
| **IBGE official benchmark MIP** (`io_ibge/`) | Official reference IO to validate IPEA estimates | 2015 Nível 67 downloaded (2000/2005/2010 also available) | ✅ **collected (2015)** |
| **Receita Federal — tax by CNAE section** (`tax_rfb/arrecadacao-cnae.csv`) | IRPJ/CSLL (+ IPI, Cofins, …) monthly by CNAE section → effective `cit_rate` numerator | **2016–2026** | ✅ **collected** |
| SNIS / ANA — water sector (`water_snis/`) | Sector-5 operational/financial detail | annual | ⬜ optional, low priority |

**Working parts (committed):**
- `concordances/concordance.py` — Nível-67 → 10-sector map, all 67 activities /
  126 products covered (products map by 4-digit code prefix). Judgment calls
  flagged inline.
- `extract_10sectors_draft.py` — verified extractor: VA shares, `gamma_m`,
  `alpha_c`, draft `Pi^I` from any MIP year (tested 2015/2018/2021; all
  internal asserts pass; shares sum to 100%).
- `CODE_ASSESSMENT.md` — where `ogbra/` needs modification (no changes made),
  incl. the `update_from_api` gating issue in `calibrate.py`.

**Headline 2018 results (IPEA, 10 sectors):** VA shares — trade/transport 19.8%,
info/fin/business 18.4%, public/social 25.0%, manufacturing 12.3%, real estate
9.8%, agriculture 5.2%, construction 4.0%, **mining 2.7%** (vs 0.8% in the IFPRI
SAM — petroleum properly resolved), electricity+gas 2.0%, water 0.8%. Gamma runs
0.16 (public) to 0.99 (real estate). Caveat: gamma treats all mixed income as
capital — see CODE_ASSESSMENT.md §6.

---

## 1. IPEA/UFRJ annual MIP — PRIMARY source (production + consumer side)

**Path:** `io_ipea_ufrj/PPE_apendice_eletronico/`
**Origin:** Electronic appendix to Alves-Passoni & Freitas (2023), *Estimação de
Matrizes Insumo-Produto anuais para o Brasil no SCN Referência 2010*, PPE v.53 n.1.
**URL:** https://repositorio.ipea.gov.br/bitstream/11058/13345/2/PPE_v53_n1_Artigo4_apendice_eletronico.zip
(archived as `concordances/PPE_v53_n1_Artigo4_apendice.zip`)

**Contents:** one `.xlsx` per year, two resolutions:
- `MIP_42_PCR_PPE/MIP_YYYY_42_PCR.xlsx` — 42 activities, **2000–2021**
- `MIP_67_PCR_PPE/MIP_YYYY_67_PCR.xlsx` — 67 activities / 126 products, **2010–2021**
- `PCR` = *preços correntes* (current prices).

**Each workbook has these sheets** (everything the calibration needs):
- `Recursos` — supply/make table (production by activity)
- `Usos`, `Usos Nacional`, `Usos Importado` — use tables; final-demand cols incl.
  `Consumo das famílias` (→ `alpha_c`), `Consumo do governo`, exports; and VA rows
  incl. `Excedente operacional bruto e rendimento misto bruto` (→ capital for `γ_m`)
- `Impostos`, `Comércio`, `Transporte` — taxes & margins
- `D` — **market-share matrix** → builds the Leontief consumption bridge `Π^I` (`io_matrix`)
- `Bn`, `Bm`, `An` — technical-coefficient matrices (not needed by OG-Core, but present)
- Concordance keys built in: `Código/Descrição da Atividade Nível 67`, `Produto Nível 126`

**Key verified facts:**
- **Electricity is bundled**: activity `Energia elétrica, gás natural e outras utilidades`
  (product `Eletricidade, gás e outras utilidades`) = Sector 4. Pure-power split needs EPE (below).
- **Water is separate**: `Água, esgoto e gestão de resíduos` = Sector 5.
- **Mining/petroleum well resolved** (iron ore, non-ferrous, coal, `Extração de petróleo e gás`
  as distinct activities) — fixes IFPRI's understated single mining sector.
- Fuels resolved as *products* (refino, etanol/biocombustíveis, diesel, óleo combustível, gasoálcool)
  even though the electricity *utility* is bundled — useful for CLEWS energy-demand mapping.

## 2. EPE BEN — energy detail for electricity split & CLEWS

**Path:** `energy_epe/`
**Origin:** EPE, *Balanço Energético Nacional 2025* (base year 2024), open data.
**Files:**
- `BEN2025_AnexoIX_Balancos_Consolidados_tep_1970-2024.xlsx` — consolidated energy
  balance, **one sheet per year 1970–2024**, in tep (toe). Rows = energy sources
  (hydro, natural gas, electricity, biomass, etc.), cols = transformation & consumption
  sectors. This is the long series for the electricity split and demand-by-sector coupling.
- `BEN2025_Matriz_ab2024.xlsx` — single-year (2024) energy matrix.
- **Not downloaded (53 MB):** `Anexo X - Matriz aberta e Comercial 1970 a 2024.xlsx`
  (full open+commercial matrix). URL under EPE publicacao-885/topico-766 if needed.

**Use:** BEN is *physical* (tep/GWh). To carve monetary pure-electricity value added out
of the Section-D bundle, combine BEN physical shares with ANEEL (electricity revenue) +
ABEGÁS/ANP (piped-gas revenue); steam/district-heating ≈ 0 in Brazil. For a first pass the
Section-D bundle ≈ electricity (~90%+).

## 3. IBGE official benchmark MIP — verified available, not yet pulled

**Path:** `io_ibge/` (empty)
**URL:** https://ftp.ibge.gov.br/Contas_Nacionais/Matriz_de_Insumo_Produto/
(browsable with a browser User-Agent; folders 2000, 2005, 2010, 2015 confirmed present).
Also `Sistema_de_Contas_Nacionais/` holds the annual TRUs. Purpose: cross-check the IPEA
estimated years against the official benchmarks (2010, 2015). Pull when validating.

## 4. Receita Federal — corporate tax by industry (`cit_rate`) — to collect

"Grandes Números IRPJ/CSLL" by CNAE at gov.br/receitafederal (dados abertos). Statutory
IRPJ+CSLL ≈ 34% as baseline; watch Simples Nacional / Lucro Presumido / Manaus Free Zone.

## 5. SNIS / ANA — water sector detail (Sector 5) — to collect

SNIS (Sistema Nacional de Informações sobre Saneamento) for operational/financial data;
monetary VA already comes from the IPEA MIP. Low priority (small sector).

---

## Notes
- Downloads require a browser `User-Agent`; bare curl gets HTTP 403 from IBGE/EPE.
- xlsx files not yet parsed into tidy form — no `.venv`/pandas set up yet. Next step when
  the real work starts: `uv sync` then a loader that reads `Recursos`/`Usos`/`D` and applies
  the 126-product / 67-activity → 10-sector concordance.
