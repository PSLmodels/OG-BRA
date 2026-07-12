"""
Same-economy equivalence test for the multi-industry configuration.

With identical technology in every industry, the M = 9, I = 7 model with
the chi_b/chi_n composite-units rescale must reproduce the M = 1 economy
exactly: the io_matrix bookkeeping and the utility-weight conversion are
supposed to be neutral, and this test proves they are (OG-PHL's
acceptance criterion for its multi-industry calibration).

The test sets ``gamma_g = 0``. That is not a shortcut: with nonrival
public capital the production function has decreasing returns to private
factors, so marginal cost rises with industry scale and identical
industries of different sizes price differently -- disaggregation then
changes the equilibrium through the common K_g, as a matter of model
structure. Exact M-invariance is only defined at gamma_g = 0.

Marked local: three steady-state solves (~1 minute).
"""

import json
import os

import numpy as np
import pytest

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
PKG = os.path.join(CUR_DIR, "..", "ogbra")
FLAT_GAMMA = 0.428  # economy-wide capital share (TOTAL_CAPITAL_SHARE)


def _solve(M, n_cons, tmp_path, base, overlay):
    from ogcore import SS
    from ogcore.parameters import Specifications

    out = os.path.join(tmp_path, f"m{M}i{n_cons}")
    p = Specifications(
        baseline=True, num_workers=2, baseline_dir=out, output_base=out
    )
    p.update_specifications(base)
    upd = {
        "M": M,
        "I": n_cons,
        "gamma": [FLAT_GAMMA] * M,
        "gamma_g": [0.0] * M,
        "epsilon": [1.0] * M,
        "Z": [[1.0] * M],
        "c_min": [0.0] * n_cons,
    }
    if n_cons == 1:
        upd.update({"alpha_c": [1.0], "io_matrix": [[1.0 / M] * M]})
    else:
        alpha = np.array(overlay["alpha_c"])
        k_units = float(np.prod(alpha**-alpha))
        chi_scale = k_units ** (base["sigma"] - 1.0)
        upd.update(
            {
                "alpha_c": overlay["alpha_c"],
                "io_matrix": overlay["io_matrix"],
                "chi_b": [c * chi_scale for c in base["chi_b"]],
                "chi_n": [c * chi_scale for c in base["chi_n"]],
            }
        )
    p.update_specifications(upd)
    return SS.run_SS(p, client=None)


@pytest.mark.local
def test_multisector_describes_same_economy(tmp_path):
    with open(os.path.join(PKG, "ogbra_default_parameters.json")) as f:
        base = json.load(f)
    with open(
        os.path.join(PKG, "ogbra_multisector_default_parameters.json")
    ) as f:
        overlay = json.load(f)

    single = _solve(1, 1, str(tmp_path), base, overlay)
    multi = _solve(9, 7, str(tmp_path), base, overlay)

    assert float(multi["r"]) == pytest.approx(float(single["r"]), rel=1e-8)
    assert float(multi["w"]) == pytest.approx(float(single["w"]), rel=1e-8)
    assert float(np.sum(multi["K"])) == pytest.approx(
        float(np.sum(single["K"])), rel=1e-8
    )
    assert float(np.sum(multi["L"])) == pytest.approx(
        float(np.sum(single["L"])), rel=1e-8
    )
    # nominal consumption (composite units differ; p_tilde converts back)
    nom_c_multi = float(np.mean(np.atleast_1d(multi["p_tilde"]))) * float(
        np.sum(multi["C"])
    )
    nom_c_single = float(np.mean(np.atleast_1d(single["p_tilde"]))) * float(
        np.sum(single["C"])
    )
    assert nom_c_multi == pytest.approx(nom_c_single, rel=1e-8)
    # identical industries must price identically
    assert np.allclose(np.atleast_1d(multi["p_m"]), 1.0, atol=1e-8)
