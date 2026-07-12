"""The packaged PIT rates must be reproducible from the packaged DIRPF data.

`ogbra/data/dirpf_ac2024_by_bracket.csv` holds the national aggregates of the
Receita Federal Grandes Números DIRPF tables for calendar year 2024 (Tabela 4,
summed over form type and UF, by annual tax-base bracket). The linear tax
rates in `ogbra_default_parameters.json` are computed from it as documented
in the taxes chapter; this test re-derives them so the packaged values and
the packaged data cannot silently drift apart.
"""

import json
import os
import importlib.resources

import pandas as pd

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CSV = os.path.join(
    CUR_DIR, "..", "ogbra", "data", "dirpf_ac2024_by_bracket.csv"
)

# statutory bracket rates for the 2024 annual table, aligned with the five
# faixa_base_calculo rows (isento, 7.5%, 15%, 22.5%, 27.5%)
BRACKET_ORDER = [
    "Até 26.963,20",
    "De 26.963,21 até 33.919,80",
    "De 33.919,81 até 45.012,60",
    "De 45.012,61 até 55.976,16",
    "Acima de 55.976,16",
]
STATUTORY_RATES = [0.0, 0.075, 0.15, 0.225, 0.275]
EXCLUSIVA_WITHHOLDING = 0.175  # midpoint of the 15-22.5% fixed-income schedule
DIVIDEND_RATE_2026 = 0.10  # Law No. 15,270/2025
RENTAL_MARGINAL = 0.275


def _params():
    with importlib.resources.open_text(
        "ogbra", "ogbra_default_parameters.json"
    ) as f:
        return json.load(f)


def test_pit_rates_reproducible_from_dirpf_data():
    df = (
        pd.read_csv(CSV).set_index("faixa_base_calculo").reindex(BRACKET_ORDER)
    )
    tot = df.sum()

    tributavel = tot["rendimento_tributavel_total"]
    exclusiva = tot["rend_sujeitos_a_tribut_exclusiva"]
    exclusiva_13 = tot["rend_tribut_exclusiva_decimo_terceiro"]
    isentos = tot["rend_isentos_e_nao_tributaveis"]
    devido = tot["imposto_devido_total"]

    # etr: total income tax (adjustment tax plus imputed exclusive-taxation
    # withholding) over total declared income
    exclusiva_ex13 = exclusiva - exclusiva_13
    etr = (devido + EXCLUSIVA_WITHHOLDING * exclusiva_ex13) / (
        tributavel + exclusiva + isentos
    )

    # mtrx: taxable-income-weighted statutory marginal rate
    w = df["rendimento_tributavel_total"] / tributavel
    mtrx = float((w * STATUTORY_RATES).sum())

    # mtry: composition-weighted marginal rate on declared capital income
    div = tot["rend_isentos_lucros_dividendos"]
    poup = tot["rend_isentos_poupanca"]
    alug = tot["rend_tributavel_alugueis"]
    cap = div + poup + alug + exclusiva_ex13
    mtry = (
        div * DIVIDEND_RATE_2026
        + poup * 0.0
        + alug * RENTAL_MARGINAL
        + exclusiva_ex13 * EXCLUSIVA_WITHHOLDING
    ) / cap

    p = _params()
    assert round(etr, 2) == p["etr_params"][0][0][0]
    assert round(mtrx, 2) == p["mtrx_params"][0][0][0]
    assert round(mtry, 2) == p["mtry_params"][0][0][0]
