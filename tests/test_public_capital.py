"""The public capital calibration must be internally consistent.

The steady-state public capital stock in OG-Core is
K_g/Y = alpha_I / (growth + delta_g) with growth = (1+g_y)(1+g_n) - 1
(see ogcore.fiscal.get_K_g). The calibration anchors this to Brazil's
measured general government capital stock of 35% of GDP (IMF PIMA / ICSD,
2015) with public investment of 2% of GDP, which requires the implied
depreciation rate delta_g of about 4.7% rather than the ogcore default of
2%. This test enforces the identity so the four parameters cannot be
edited independently into an inconsistent state.
"""

import json
import importlib.resources


def test_public_capital_steady_state_consistency():
    with importlib.resources.open_text(
        "ogbra", "ogbra_default_parameters.json"
    ) as f:
        p = json.load(f)
    growth = (1 + p["g_y_annual"]) * (1 + p["g_n_ss"]) - 1
    ss_kg_ratio = p["alpha_I"][0] / (growth + p["delta_g_annual"])
    # the steady-state ratio must match the initial (measured) ratio, so the
    # model does not build in a large artificial public-capital transition
    assert abs(ss_kg_ratio - p["initial_Kg_ratio"]) < 0.01, (
        f"SS Kg/Y = {ss_kg_ratio:.4f} but initial_Kg_ratio = "
        f"{p['initial_Kg_ratio']} — alpha_I, delta_g_annual, and "
        "initial_Kg_ratio are mutually inconsistent"
    )
    # and the private + public capital shares must not exceed one
    assert p["gamma"][0] + p["gamma_g"][0] < 1.0
