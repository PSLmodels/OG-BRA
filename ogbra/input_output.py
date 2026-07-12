"""
Multi-industry calibration objects from the Brazilian input-output tables.

The data source is the annual input-output series for Brazil estimated by
Alves-Passoni and Freitas (2023) from the IBGE Supply and Use Tables
(67 activities, 126 products; the 2015 benchmark year reproduces the
official IBGE matrix). Compact extracts of the 2018 table ship with the
package in ``ogbra/data`` (see ``data_prep/multi_industry`` for the
extraction script and provenance); the functions here aggregate them to
the model's M = 9 industries and I = 7 consumption goods using the
concordances in ``ogbra.constants``.
"""

import os

import numpy as np
import pandas as pd

from ogbra.constants import (
    ACTIVITY_TO_SECTOR,
    CAPITAL_OUTPUT_RATIO,
    CONS_CATEGORIES,
    PREFIX_TO_CONS_CATEGORY,
    SECTORS,
)

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CUR_DIR, "data")
MIP_YEAR = 2018


def _read(name):
    path = os.path.join(DATA_DIR, f"mip_{MIP_YEAR}_{name}.csv")
    kwargs = {"dtype": {"activity_code": str, "product_code": str}}
    if name in ("market_share", "leontief"):
        kwargs = {"index_col": 0}
    try:
        df = pd.read_csv(path, **kwargs)
    except Exception as exc:
        raise RuntimeError(
            f"Packaged MIP extract {path} is unavailable: {exc}"
        )
    if name in ("market_share", "leontief"):
        df.index = [str(i).zfill(4) for i in df.index]
        width = 5 if name == "market_share" else 4
        df.columns = [str(c).zfill(width) for c in df.columns]
    return df


def get_alpha_c(cats=CONS_CATEGORIES):
    """
    Calibrate ``alpha_c``, the shares of household expenditure on each of
    the I consumption goods, from household final consumption at consumer
    prices in the use table.

    Args:
        cats (dict): consumption categories (order sets the I dimension)

    Returns:
        alpha_c (dict): expenditure shares, keyed by consumption category
    """
    cons = _read("consumption")
    group = cons["product_code"].str[:4].map(PREFIX_TO_CONS_CATEGORY)
    totals = (
        cons["hh_consumption_consumer_prices"]
        .groupby(group)
        .sum()
        .reindex(list(cats))
    )
    shares = totals / totals.sum()
    return {cat: float(shares[cat]) for cat in cats}


def get_io_matrix(cats=CONS_CATEGORIES, sectors=SECTORS):
    """
    Calibrate the ``io_matrix``: the domestic value-added content of each
    consumption good, by producing industry (rows sum to one).

    OG-Core's production side has no intermediate inputs, so the object it
    needs is the value added embodied in final consumption: of one real
    spent on consumption good i, how much is value added by each industry
    once the whole domestic supply chain is traced. The input-output table
    provides the pieces directly: the market-share matrix D allocates each
    product's domestic supply to producing activities, the domestic
    Leontief inverse traces the supply chain, and value added per unit of
    gross output converts activity output into value added. Household
    consumption of domestic production (basic prices) weights the products
    within each consumption good; imported content is outside the domestic
    matrices and is excluded by the row normalization.

    Args:
        cats (dict): consumption categories (order sets the I dimension)
        sectors (dict): production industries (order sets the M dimension)

    Returns:
        io_df (pd.DataFrame): I x M ``io_matrix`` (rows sum to one)
    """
    act = _read("activity")
    cons = _read("consumption")
    D = _read("market_share")
    L = _read("leontief")

    acts = act["activity_code"].tolist()
    assert list(D.index) == acts and list(L.index) == acts
    prods = cons["product_code"].tolist()
    assert list(D.columns) == prods

    v = (act["value_added"] / act["gross_output"]).to_numpy()
    D_np, L_np = D.to_numpy(), L.to_numpy()
    group = cons["product_code"].str[:4].map(PREFIX_TO_CONS_CATEGORY)
    hh_dom = cons["hh_consumption_domestic_basic"].to_numpy()

    slugs = list(sectors)
    io = np.zeros((len(cats), len(slugs)))
    for ci, cat in enumerate(cats):
        f = np.where(group.to_numpy() == cat, hh_dom, 0.0)
        va_by_activity = v * (L_np @ (D_np @ f))
        for ai, a in enumerate(acts):
            io[ci, slugs.index(ACTIVITY_TO_SECTOR[a])] += va_by_activity[ai]
    io = io / io.sum(axis=1, keepdims=True)
    return pd.DataFrame(io, index=list(cats), columns=slugs)


def get_gamma(sectors=SECTORS, target_avg=None):
    """
    Calibrate ``gamma``, the capital share of factor income by industry.

    The input-output table reports three factor rows: compensation of
    employees (labor), gross operating surplus (capital, including land
    rents), and gross mixed income -- the earnings of the self-employed,
    which are part labor and part capital and cannot be booked wholesale
    to either. Assigning all mixed income to capital badly overstates the
    capital share in self-employment-heavy industries (Brazilian
    agriculture is nearly half mixed income, against a tenth economy-wide).

    We therefore split mixed income by Gollin's second adjustment: the
    self-employed earn capital and labor in the same proportion as the
    incorporated part of the economy, where the split is observed. With
    ``phi`` the economy-wide capital share of the non-mixed factor income
    (operating surplus over compensation plus operating surplus), each
    industry's capital income is operating surplus plus ``phi`` of its
    mixed income, and its labor income is compensation plus the rest.
    Because ``phi`` is the economy's own capital share, the industry
    shares already average (factor-income-weighted) to it; ``target_avg``,
    when given, applies a final multiplicative rescale so the average
    equals the calibration target exactly (``constants.TOTAL_CAPITAL_SHARE``
    -- the same measure, so the rescale is a rounding-level adjustment)
    while preserving the cross-industry pattern.

    Args:
        sectors (dict): production industries
        target_avg (float | None): rescale so the weighted mean equals this

    Returns:
        gamma (dict): capital share of factor income, keyed by industry
    """
    act = _read("activity")
    sector = act["activity_code"].map(ACTIVITY_TO_SECTOR)
    os_ = act["operating_surplus"].groupby(sector).sum().reindex(list(sectors))
    mixed = act["mixed_income"].groupby(sector).sum().reindex(list(sectors))
    comp = act["compensation"].groupby(sector).sum().reindex(list(sectors))

    # Gollin adjustment 2: split mixed income at the economy-wide capital
    # share of the non-mixed factor income.
    phi = float(os_.sum() / (comp.sum() + os_.sum()))
    cap = os_ + phi * mixed
    lab = comp + (1.0 - phi) * mixed
    factor_income = cap + lab
    gamma = cap / factor_income

    if target_avg is not None:
        current = float(np.average(gamma, weights=factor_income))
        gamma = gamma * (target_avg / current)

    return {s: float(gamma[s]) for s in sectors}


def get_employment(sectors=SECTORS):
    """
    Employment (occupations) by industry from the input-output table's
    labor-factor row.

    Args:
        sectors (dict): production industries

    Returns:
        employment (dict): occupations, keyed by industry
    """
    act = _read("activity")
    sector = act["activity_code"].map(ACTIVITY_TO_SECTOR)
    emp = act["occupations"].groupby(sector).sum().reindex(list(sectors))
    return {s: float(emp[s]) for s in sectors}


def get_Z(
    sectors=SECTORS,
    gamma=None,
    gamma_g=0.0,
    employment=None,
    capital_output_ratio=CAPITAL_OUTPUT_RATIO,
):
    """
    Construct industry total factor productivity ``Z_m`` as the Solow
    residual of OG-Core's per-industry production function,

        Z_m = Y_m / (K_m**gamma_m * K_g**gamma_g * L_m**(1-gamma_m-gamma_g)),

    normalized so Manufacturing has Z = 1 (following OG-PHL, whose
    documentation explains the construction in detail). Y_m is industry
    value added from the input-output table; L_m is the table's
    occupations row, a physical head count measured separately from the
    factor payments; K_m allocates the national capital stock
    (``capital_output_ratio`` times total value added; Penn World Table
    for Brazil) across industries by their share of capital income, the
    distribution implied by capital mobility at a common return. Public
    capital is one common stock, so with the Manufacturing normalization
    only ``gamma_g``'s effect on the labor exponent survives and the
    stock itself is never needed.

    Args:
        sectors (dict): production industries
        gamma (dict | None): capital share by industry; pass the same
            (rescaled) gamma the model uses
        gamma_g (float): public capital's output share
        employment (dict | None): occupations by industry; read from the
            packaged table when None
        capital_output_ratio (float): national K/Y anchoring capital

    Returns:
        Z (dict): TFP by industry (Manufacturing = 1.0)
    """
    act = _read("activity")
    sector = act["activity_code"].map(ACTIVITY_TO_SECTOR)
    slugs = list(sectors)
    Y = act["value_added"].groupby(sector).sum().reindex(slugs).to_numpy()
    cap_income = (
        (act["operating_surplus"] + act["mixed_income"])
        .groupby(sector)
        .sum()
        .reindex(slugs)
        .to_numpy()
    )
    if employment is None:
        employment = get_employment(sectors)
    L = np.array([employment[s] for s in slugs])
    if gamma is None:
        gamma = get_gamma(sectors)
    g = np.array([gamma[s] for s in slugs])

    K = capital_output_ratio * Y.sum() * (cap_income / cap_income.sum())
    with np.errstate(divide="ignore", invalid="ignore"):
        Z = Y / (K**g * L ** (1.0 - g - gamma_g))
    numeraire = Z[slugs.index("manufacturing")]
    Z = Z / numeraire
    return {s: float(z) for s, z in zip(slugs, Z)}


# Receita Federal CNAE section -> production industry, for the corporate
# tax collections data (sections G/H/I combine into trade & transport;
# J/K/M/N into information, financial & business services; O-U into
# public, social & other services).
CNAE_SECTION_TO_SECTOR = {
    "A": "agriculture",
    "B": "mining",
    "C": "manufacturing",
    "D": "electricity_gas",
    "E": "water_waste",
    "F": "construction",
    "G": "trade_transport",
    "H": "trade_transport",
    "I": "trade_transport",
    "J": "info_fin_business",
    "K": "info_fin_business",
    "L": "info_fin_business",
    "M": "info_fin_business",
    "N": "info_fin_business",
    "O": "public_social_other",
    "P": "public_social_other",
    "Q": "public_social_other",
    "R": "public_social_other",
    "S": "public_social_other",
    "T": "public_social_other",
    "U": "public_social_other",
}


def get_tau_c(cats=CONS_CATEGORIES):
    """
    Calibrate per-good consumption tax rates: taxes on products embedded
    in household consumption over consumption net of those taxes, by
    consumption good. This is the same effective-rate concept as the
    single-industry ``tau_c`` (whose 0.13 is the weighted average of
    these), disaggregated: it makes the heavy indirect taxation of
    electricity (ICMS) and fuels visible against lightly taxed services.

    Args:
        cats (dict): consumption categories

    Returns:
        tau_c (dict): effective consumption tax rate by category
    """
    cons = _read("consumption")
    group = cons["product_code"].str[:4].map(PREFIX_TO_CONS_CATEGORY)
    agg = (
        cons.groupby(group)[
            ["hh_consumption_consumer_prices", "hh_taxes_on_products"]
        ]
        .sum()
        .reindex(list(cats))
    )
    tau = agg["hh_taxes_on_products"] / (
        agg["hh_consumption_consumer_prices"] - agg["hh_taxes_on_products"]
    )
    return {cat: float(tau[cat]) for cat in cats}


def get_cit_rate(sectors=SECTORS, years=(2017, 2018, 2019)):
    """
    Calibrate per-industry effective corporate income tax rates: IRPJ plus
    CSLL collections by CNAE section (Receita Federal, averaged over
    ``years``) over gross operating surplus by industry from the
    input-output table. Effective rates are far below the 34% statutory
    rate and differ by industry: agriculture pays the least (special
    regimes, and a surplus that is largely land rent rather than taxable
    corporate profit), and manufacturing the most. Note that the finance,
    real estate & business services aggregate carries a low effective rate
    because its operating surplus includes imputed owner-occupier dwelling
    rent, which is not corporate profit and dilutes the denominator.

    Args:
        sectors (dict): production industries
        years (tuple): collection years to average (centered on the
            input-output table's year)

    Returns:
        cit_rate (dict): effective corporate tax rate by industry
    """
    path = os.path.join(DATA_DIR, "rfb_cit_by_section.csv")
    rfb = pd.read_csv(path)
    rfb = rfb[rfb["year"].isin(years)]
    rfb["sector"] = rfb["cnae_section"].map(CNAE_SECTION_TO_SECTOR)
    collections = (
        rfb.dropna(subset=["sector"])
        .groupby("sector")[["irpj", "csll"]]
        .sum()
        .sum(axis=1)
        / len(years)
        / 1e6  # RFB data in R$; MIP in R$ millions
    )
    act = _read("activity")
    sector = act["activity_code"].map(ACTIVITY_TO_SECTOR)
    eob = act["operating_surplus"].groupby(sector).sum()
    return {s: float(collections.get(s, 0.0) / eob[s]) for s in sectors}
