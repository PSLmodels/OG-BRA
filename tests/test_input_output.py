"""
Tests of the multi-industry input-output calibration.

The functions read the packaged MIP extracts (``ogbra/data/mip_2018_*``),
so these tests exercise the real interface. The multisector overlay test
re-derives the packaged json from the same functions so the two cannot
silently drift apart.
"""

import json
import os

import numpy as np
import pytest

from ogbra import input_output as io
from ogbra.constants import (
    ACTIVITY_TO_SECTOR,
    CONS_CATEGORIES,
    PREFIX_TO_CONS_CATEGORY,
    PUBLIC_CAPITAL_SHARE,
    SECTORS,
    TOTAL_CAPITAL_SHARE,
)

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
OVERLAY = os.path.join(
    CUR_DIR, "..", "ogbra", "ogbra_multisector_default_parameters.json"
)


def test_concordances_cover_everything():
    assert len(ACTIVITY_TO_SECTOR) == 67
    assert set(ACTIVITY_TO_SECTOR.values()) == set(SECTORS)
    assert len(PREFIX_TO_CONS_CATEGORY) == 67
    assert set(PREFIX_TO_CONS_CATEGORY.values()) == set(CONS_CATEGORIES)
    # every product in the packaged data maps to a category
    cons = io._read("consumption")
    unmapped = [
        c for c in cons["product_code"] if c[:4] not in PREFIX_TO_CONS_CATEGORY
    ]
    assert unmapped == []


def test_alpha_c_sums_to_one_and_is_positive():
    a = io.get_alpha_c()
    assert list(a) == list(CONS_CATEGORIES)
    vals = np.array(list(a.values()))
    assert abs(vals.sum() - 1.0) < 1e-9
    assert (vals > 0).all()


def test_io_matrix_rows_sum_to_one():
    m = io.get_io_matrix()
    assert m.shape == (len(CONS_CATEGORIES), len(SECTORS))
    assert np.allclose(m.sum(axis=1), 1.0)
    # electricity consumption is produced mostly by the electricity
    # industry; services mostly outside manufacturing
    assert m.loc["electricity", "electricity_gas"] > 0.5
    assert m.loc["services", "manufacturing"] < 0.1


def test_gamma_rescale_hits_target():
    g = io.get_gamma(target_avg=TOTAL_CAPITAL_SHARE)
    act = io._read("activity")
    sector = act["activity_code"].map(ACTIVITY_TO_SECTOR)
    cap = (
        (act["operating_surplus"] + act["mixed_income"])
        .groupby(sector)
        .sum()
        .reindex(list(SECTORS))
    )
    lab = act["compensation"].groupby(sector).sum().reindex(list(SECTORS))
    w = (cap + lab).to_numpy()
    avg = np.average(np.array(list(g.values())), weights=w)
    assert abs(avg - TOTAL_CAPITAL_SHARE) < 1e-9
    # private share plus public capital share stays inside the unit box
    assert all(
        0 < v - PUBLIC_CAPITAL_SHARE < 1 - PUBLIC_CAPITAL_SHARE
        for v in g.values()
    )


def test_gamma_mixed_income_split():
    """The Gollin split must move smallholder self-employment income to the
    labor side, so agriculture (nearly half mixed income) lands well below
    the capital-heavy, low-self-employment industries -- not above them, as
    booking all mixed income to capital would put it."""
    g = io.get_gamma(target_avg=TOTAL_CAPITAL_SHARE)
    # booking all mixed income to capital put agriculture on par with the
    # capital-heavy industries; the split drops it well below them (it
    # keeps a genuine, land-rent-driven premium over the economy average,
    # but no longer rivals the capital-intensive extractives and utilities)
    assert g["agriculture"] < g["mining"] - 0.15
    assert g["agriculture"] < g["electricity_gas"] - 0.15


def test_Z_normalized_to_manufacturing():
    g = io.get_gamma(target_avg=TOTAL_CAPITAL_SHARE)
    gamma = {k: v - PUBLIC_CAPITAL_SHARE for k, v in g.items()}
    Z = io.get_Z(gamma=gamma, gamma_g=PUBLIC_CAPITAL_SHARE)
    assert Z["manufacturing"] == pytest.approx(1.0)
    assert all(v > 0 for v in Z.values())


def test_tau_c_rates():
    tau = io.get_tau_c()
    assert list(tau) == list(CONS_CATEGORIES)
    assert all(0 <= v < 0.5 for v in tau.values())
    # electricity (ICMS) and fuels are the heavily taxed goods; services light
    assert tau["electricity"] > 0.25
    assert tau["fuels"] > 0.2
    assert tau["services"] < 0.1
    # consumption-weighted average reproduces the single effective rate
    alpha = io.get_alpha_c()
    avg = sum(alpha[c] * tau[c] for c in tau)
    assert 0.10 < avg < 0.15


def test_cit_effective_rates():
    cit = io.get_cit_rate()
    assert list(cit) == list(SECTORS)
    # effective rates sit below the 34% statutory rate for every industry
    assert all(0 < v < 0.34 for v in cit.values())
    # agriculture pays the least (special regimes on a sector whose surplus
    # includes land rents); the effective aggregate is far below statutory
    assert min(cit, key=cit.get) == "agriculture"
    assert cit["agriculture"] < 0.05


def test_overlay_reproducible_from_packaged_data():
    """The packaged multisector overlay must equal a fresh rebuild."""
    from ogbra.create_multisector_calibration import build_multisector_params

    with open(OVERLAY) as f:
        packaged = json.load(f)
    rebuilt = build_multisector_params()
    assert packaged.keys() == rebuilt.keys()
    for k in rebuilt:
        assert np.allclose(
            np.array(packaged[k], dtype=float),
            np.array(rebuilt[k], dtype=float),
        ), f"overlay field {k} does not match a rebuild from packaged data"
