"""The packaged eta must be reproducible from the packaged incidence data.

`ogbra/data/transfer_incidence.csv` holds the quintile incidence and 2024
spending of Brazil's main non-pension transfer programs (see the government
calibration chapter for sources and the market-income-ranking discussion).
This test re-derives the lifetime-income-group shares of `eta` from it —
blend the program distributions by spending weight, map quintiles to the
model's J groups assuming uniformity within quintiles — so the packaged
values and the packaged data cannot silently drift apart.
"""

import json
import os
import importlib.resources

import numpy as np
import pandas as pd

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CSV = os.path.join(CUR_DIR, "..", "ogbra", "data", "transfer_incidence.csv")


def test_eta_group_shares_reproducible_from_incidence_data():
    df = pd.read_csv(CSV)
    w = df["spending_2024_rbn"] / df["spending_2024_rbn"].sum()
    qcols = ["q1", "q2", "q3", "q4", "q5"]
    blend = (df[qcols].T * w.values).T.sum()

    with importlib.resources.open_text(
        "ogbra", "ogbra_default_parameters.json"
    ) as f:
        p = json.load(f)
    lambdas = p["lambdas"]
    edges = np.cumsum([0] + lambdas)
    qedges = np.arange(0, 1.01, 0.2)

    def mass(a, b):
        m = 0.0
        for qi in range(5):
            lo, hi = qedges[qi], qedges[qi + 1]
            ov = max(0.0, min(b, hi) - max(a, lo))
            m += blend.iloc[qi] * ov / 0.2
        return m

    etaJ = np.array(
        [mass(edges[j], edges[j + 1]) for j in range(len(lambdas))]
    )
    etaJ /= etaJ.sum()

    eta = np.array(p["eta"])  # (S, J)
    assert eta.shape[1] == len(lambdas)
    packaged_shares = eta.sum(axis=0)
    assert np.allclose(packaged_shares, etaJ, atol=1e-6), (
        f"packaged eta J-shares {np.round(packaged_shares, 4)} != "
        f"shares recomputed from incidence data {np.round(etaJ, 4)}"
    )
    # the whole matrix distributes exactly one unit of transfers
    assert abs(eta.sum() - 1.0) < 1e-6
