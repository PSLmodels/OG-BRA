"""
Build the OG-BRA multi-industry (M=9, I=7) calibration and write it to
the packaged ``ogbra_multisector_default_parameters.json``.

Calibration is a rare event. Run this ONLY to (re)generate the packaged
multi-industry parameter overlay from the packaged input-output extracts
(the 2018 IPEA/IBGE table; see ``ogbra.input_output``):

    uv run python -m ogbra.create_multisector_calibration

The model itself loads the JSON; it does not call these functions at run
time. This module assembles the output of ``ogbra.input_output``
(``get_alpha_c``, ``get_io_matrix``, ``get_gamma``, ``get_Z``) into an
OG-Core parameter overlay, following the structure of OG-PHL's
multisector calibration.

Values written (an overlay on top of ``ogbra_default_parameters.json``):
  * ``M``, ``I``   -  9 production industries, 7 consumption goods
                     (electricity and water are their own goods for the
                     OG-CLEWS energy and water linkages)
  * ``alpha_c``    - household expenditure shares (use table)
  * ``io_matrix``  - 7x9 domestic value-added content of each good
  * ``gamma``      - per-industry private capital share: the input-output
                     capital shares with mixed income split between labor
                     and capital by Gollin's second adjustment (see
                     get_gamma), rescaled so their weighted mean is
                     TOTAL_CAPITAL_SHARE, then PUBLIC_CAPITAL_SHARE carved
                     out of capital, not labor
  * ``Z``          - per-industry TFP, the Solow residual (see get_Z)
  * ``epsilon``    - 1.0 (Cobb-Douglas; OG-Core default)
  * ``gamma_g``    - PUBLIC_CAPITAL_SHARE for every industry
  * ``c_min``      - 0.0 (no subsistence floor)
  * ``chi_b``, ``chi_n`` - the base utility weights converted for the
                     multi-good composite-consumption units: scaled by
                     k**(sigma-1) with k = prod(alpha_c**-alpha_c), the
                     units constant OG-Core's unnormalized composite
                     price index picks up when I > 1 (see OG-PHL's
                     create_multisector_calibration for the derivation)
  * ``nu``         - 0.2 TPI dampening (0.4 was marginally unstable in
                     the analogous OG-PHL configuration)

  * ``tau_c``      - per-good effective consumption tax rates (taxes on
                     products over net-of-tax consumption, from the use
                     table); their weighted average equals the
                     single-industry effective rate, but electricity
                     (heavy ICMS, 0.34) and fuels (0.29) now stand apart
                     from services (0.06)
  * ``cit_rate``   - per-industry effective corporate tax rates (IRPJ +
                     CSLL collections by CNAE section over gross
                     operating surplus). Effective rates average about
                     0.09 -- far below the 34% statutory rate -- and
                     range from ~0.01 (agriculture's special regimes) up
                     to ~0.14 (manufacturing)
"""

import json
import os

import numpy as np

from ogbra import input_output as io
from ogbra.constants import PUBLIC_CAPITAL_SHARE, TOTAL_CAPITAL_SHARE

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
MULTISECTOR_PARAMS_PATH = os.path.join(
    CUR_DIR, "ogbra_multisector_default_parameters.json"
)

TPI_NU = 0.2


def build_multisector_params():
    """Compute the multi-industry parameter overlay from the packaged data.

    Returns:
        params (dict): an OG-Core ``update_specifications``-format overlay.
    """
    alpha_c = [float(v) for v in io.get_alpha_c().values()]
    io_df = io.get_io_matrix()
    n_cons, n_ind = io_df.shape
    # Per-industry capital shares: rescale to the economy-wide total, then
    # subtract public capital's share to leave the private share gamma_m.
    gamma_total = io.get_gamma(target_avg=TOTAL_CAPITAL_SHARE)
    gamma = {k: v - PUBLIC_CAPITAL_SHARE for k, v in gamma_total.items()}
    Z = io.get_Z(gamma=gamma, gamma_g=PUBLIC_CAPITAL_SHARE)
    # Composite-consumption units change for I > 1; rescale the utility
    # weights so multi-industry households are behaviorally identical to
    # the single-industry baseline (see module docstring).
    alpha_arr = np.array(alpha_c)
    k_units = float(np.prod(alpha_arr**-alpha_arr))
    with open(os.path.join(CUR_DIR, "ogbra_default_parameters.json")) as f:
        base = json.load(f)
    chi_scale = k_units ** (base["sigma"] - 1.0)
    chi_b = [float(v) * chi_scale for v in base["chi_b"]]
    chi_n = [float(v) * chi_scale for v in base["chi_n"]]
    return {
        "M": int(n_ind),
        "I": int(n_cons),
        # Public capital must be funded for gamma_g > 0 to be coherent:
        # with the base calibration's alpha_I = 0 the steady-state public
        # capital stock is zero and production is inconsistent. This block
        # is the IMF PIMA-anchored set from the single-industry refresh
        # (public investment 2% of GDP; measured stock 35% of GDP; the
        # depreciation rate implied by the steady-state identity).
        "alpha_I": [0.02],
        "delta_g_annual": 0.047,
        "initial_Kg_ratio": 0.35,
        "alpha_c": alpha_c,
        "io_matrix": io_df.values.tolist(),
        "c_min": [0.0] * n_cons,
        "gamma": [float(v) for v in gamma.values()],
        "epsilon": [1.0] * n_ind,
        "gamma_g": [PUBLIC_CAPITAL_SHARE] * n_ind,
        "Z": [[float(v) for v in Z.values()]],
        "tau_c": [[float(v) for v in io.get_tau_c().values()]],
        "cit_rate": [[float(v) for v in io.get_cit_rate().values()]],
        "chi_b": chi_b,
        "chi_n": chi_n,
        "nu": TPI_NU,
    }


def main():
    params = build_multisector_params()
    with open(MULTISECTOR_PARAMS_PATH, "w") as f:
        json.dump(params, f, indent=2)
        f.write("\n")
    print(f"Wrote {MULTISECTOR_PARAMS_PATH}")
    print(f"  M = {params['M']}, I = {params['I']}")
    print(f"  alpha_c = {np.round(params['alpha_c'], 4).tolist()}")
    print(f"  gamma   = {np.round(params['gamma'], 4).tolist()}")
    print(f"  Z       = {np.round(params['Z'][0], 4).tolist()}")
    return params


if __name__ == "__main__":
    main()
