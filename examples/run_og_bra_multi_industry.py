"""
Run the calibrated multi-industry (M=9, I=7) version of OG-BRA.

This example loads the packaged multi-industry calibration overlay
``ogbra_multisector_default_parameters.json`` -- generated (rarely) by
``ogbra.create_multisector_calibration`` from the Brazilian input-output
tables -- solves and simulates the baseline, and runs a small
illustrative reform (a corporate income tax cut) for comparison, as the
sibling multi-industry examples do. The overlay contains ``alpha_c``
(7 consumption goods; electricity and water are their own goods), the
7x10 ``io_matrix`` (domestic value-added content),
per-industry ``gamma`` (capital shares, Gollin-rescaled) and ``Z``
(Solow-residual TFP, Manufacturing = 1), and the ``chi_b``/``chi_n``
composite-consumption units conversion that keeps multi-industry
households behaviorally identical to the single-industry baseline.

Solving the steady state directly fails to converge: OG-Core seeds the
industry-price guess at p_m = 1 for every industry, but with capital
shares spanning 0.08 (public services) to 0.77 (mining) the
equilibrium relative prices are far from one, and the built-in guess
sweep only varies r and TR (never p_m). Following OG-PHL's multi-industry
example, we solve by *continuation* (homotopy): first solve a flat-gamma
economy (where p_m = 1 is correct), then morph gamma and Z toward their
calibrated values in adaptive steps, each step reusing the previous
step's solution as its starting guess. The baseline transition path
reuses the continuation's converged steady state; the reform re-solves
warm-started off the baseline.

Run the full baseline + reform comparison (slow, tens of minutes):

    uv run python examples/run_og_bra_multi_industry.py

Quick steady-state-only check (continuation + validation, no transition
path):

    uv run python examples/run_og_bra_multi_industry.py --ss-only
"""

import os
import sys
import json
import time
import shutil
import pickle
import importlib.resources
import multiprocessing

import cloudpickle
import numpy as np
from distributed import Client

from ogcore.parameters import Specifications
from ogcore.execute import runner
from ogcore import TPI
from ogcore import output_tables as ot
from ogcore import output_plots as op
from ogcore.utils import safe_read_pickle

from ogbra.constants import SECTORS

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

# Flat capital share used as the continuation anchor (a solver device, not
# a calibrated value). It equals the private-capital aggregate the
# packaged gamma averages to (TOTAL_CAPITAL_SHARE - PUBLIC_CAPITAL_SHARE),
# so morphing from the anchor to the calibrated gamma holds the aggregate
# constant and only varies the cross-industry dispersion -- which is what
# makes the homotopy converge.
ANCHOR_GAMMA = 0.378


def _load_params(name):
    with importlib.resources.files("ogbra").joinpath(name).open() as f:
        return json.load(f)


def _load_defaults():
    return _load_params("ogbra_default_parameters.json")


def _load_multisector():
    """Load the packaged multi-industry calibration overlay."""
    return _load_params("ogbra_multisector_default_parameters.json")


def build_specifications(gamma, Z, baseline, output_base, baseline_dir=None):
    """
    Build a Specifications object from the packaged single-industry
    defaults, the packaged multi-industry overlay, and the supplied gamma
    and Z (which the continuation morphs toward the calibrated values).
    """
    p = Specifications(
        baseline=baseline,
        num_workers=1,
        baseline_dir=baseline_dir or output_base,
        output_base=output_base,
    )
    p.update_specifications(_load_defaults())
    p.update_specifications(_load_multisector())
    p.update_specifications({"gamma": list(gamma), "Z": [list(Z)]})
    return p


def solve_ss_by_continuation(work_dir, dt0=0.125, dt_min=0.01):
    """
    Solve the heterogeneous-gamma, heterogeneous-Z steady state by
    adaptive continuation (see the module docstring).

    Returns:
        (ss, p, out_dir): the final steady-state dict, its parameters,
            and the directory holding it
    """
    ms = _load_multisector()
    gamma_target = np.array(ms["gamma"])
    Z_target = np.array(ms["Z"][0])
    M = ms["M"]
    anchor = np.full(M, ANCHOR_GAMMA)
    Z_anchor = np.ones(M)
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)

    # Homogeneous anchor: flat gamma and Z = 1 (equilibrium prices all 1).
    base_dir = os.path.join(work_dir, "anchor")
    os.makedirs(os.path.join(base_dir, "SS"), exist_ok=True)
    p = build_specifications(
        anchor, Z_anchor, baseline=True, output_base=base_dir
    )
    print("  solving homogeneous anchor economy ...", flush=True)
    t0 = time.time()
    runner(p, time_path=False, client=None)
    print(f"    anchor solved in {time.time() - t0:.1f}s", flush=True)

    good_dir, good_p = base_dir, p
    t, dt, idx = 0.0, dt0, 0
    while t < 1.0 - 1e-9:
        t_try = min(t + dt, 1.0)
        gamma = (1 - t_try) * anchor + t_try * gamma_target
        Z = (1 - t_try) * Z_anchor + t_try * Z_target
        idx += 1
        out_dir = os.path.join(work_dir, f"t{idx}")
        os.makedirs(os.path.join(out_dir, "SS"), exist_ok=True)
        p = build_specifications(
            gamma,
            Z,
            baseline=False,
            output_base=out_dir,
            baseline_dir=good_dir,
        )
        t0 = time.time()
        try:
            runner(p, time_path=False, client=None)
            t, good_dir, good_p = t_try, out_dir, p
            print(
                f"  step to t={t:.3f} (dt={dt:.3f}) solved in "
                f"{time.time() - t0:.1f}s",
                flush=True,
            )
            dt = min(dt * 1.5, 0.25)
        except Exception:
            dt /= 2.0
            print(
                f"  step to t={t_try:.3f} failed; reducing dt -> {dt:.4f}",
                flush=True,
            )
            if dt < dt_min:
                raise RuntimeError(
                    f"continuation stalled at t={t:.3f} (dt below {dt_min})"
                )

    ss = safe_read_pickle(os.path.join(good_dir, "SS", "SS_vars.pkl"))
    return ss, good_p, good_dir


def validate_ss(p, ss):
    """Print and sanity-check key steady-state results."""
    s = lambda x: float(np.squeeze(x))  # noqa: E731
    industries = list(SECTORS.values())
    Y_m = np.atleast_1d(np.squeeze(ss["Y_m"]))
    K_m = np.atleast_1d(np.squeeze(ss["K_m"]))
    L_m = np.atleast_1d(np.squeeze(ss["L_m"]))
    p_m = np.atleast_1d(np.squeeze(ss["p_m"]))
    Y, K, C = s(ss["Y"]), s(ss["K"]), s(ss["C"])
    # C is composite consumption (price p_tilde); value it at p_tilde
    # before dividing by nominal Y, else C/Y is understated by a units
    # factor.
    p_tilde = float(np.squeeze(ss.get("p_tilde", 1.0)))
    C_share = p_tilde * C / Y
    print("\n================ STEADY-STATE VALIDATION ================")
    print(f"Aggregate Y = {Y:.4f}   K = {K:.4f}   L = {s(ss['L']):.4f}")
    print(
        f"K/Y = {K / Y:.3f}   C/Y = {C_share:.3f}   r = {s(ss['r']):.4f}   "
        f"w = {s(ss['w']):.4f}"
    )
    print(f"K_f/K (foreign-owned capital share) = {s(ss['K_f']) / K:.3f}")
    print("\nPer-industry steady state:")
    print(
        f"{'industry':38s}{'gamma':>8s}{'Z':>7s}{'p_m':>9s}"
        f"{'Y_m':>11s}{'Y share':>9s}"
    )
    nominal = p_m * Y_m
    Yshare = nominal / nominal.sum()
    Z_m = np.atleast_1d(np.squeeze(p.Z[-1]))
    for i, name in enumerate(industries):
        print(
            f"{name:38s}{p.gamma[i]:8.3f}{Z_m[i]:7.3f}{p_m[i]:9.3f}"
            f"{Y_m[i]:11.4f}{Yshare[i]:9.1%}"
        )

    checks = {
        "all Y_m > 0": bool((Y_m > 0).all()),
        "all K_m > 0": bool((K_m > 0).all()),
        "all L_m > 0": bool((L_m > 0).all()),
        "all p_m > 0": bool((p_m > 0).all()),
        "numeraire p_m[-1] == 1": bool(np.isclose(p_m[-1], 1.0)),
        "r in (0, 0.2)": bool(0.0 < s(ss["r"]) < 0.2),
        "K/Y in (1, 8)": bool(1.0 < K / Y < 8.0),
        "Y shares sum to 1": bool(np.isclose(Yshare.sum(), 1.0)),
    }
    print("\nChecks:")
    all_ok = True
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        all_ok = all_ok and ok
    print("=========================================================")
    return all_ok


# Example reform: a small illustrative policy change, following the
# sibling multi-industry calibrations, which demonstrate the model with a
# corporate income tax cut. Here we cut every industry's effective
# corporate rate by 10 percent -- small enough that the reform steady
# state solves warm-started off the baseline.
CIT_REFORM_CUT = 0.9


def run_baseline_tpi(p_base, ss_source_dir, client):
    """Run the baseline transition path, reusing the continuation's SS.

    The calibrated steady state cannot be re-solved from a cold start
    (OG-Core seeds industry prices at p_m = 1 and only the continuation
    warm-starts them), so rather than call ``runner`` -- which would
    re-solve the SS and diverge -- we place the continuation's converged
    SS as the baseline SS and run only the TPI off it.
    """
    ss_dir = os.path.join(p_base.output_base, "SS")
    os.makedirs(ss_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(ss_source_dir, "SS", "SS_vars.pkl"),
        os.path.join(ss_dir, "SS_vars.pkl"),
    )
    with open(os.path.join(p_base.output_base, "model_params.pkl"), "wb") as f:
        cloudpickle.dump(p_base, f)
    tpi_output = TPI.run_TPI(p_base, client=client)
    tpi_dir = os.path.join(p_base.output_base, "TPI")
    os.makedirs(tpi_dir, exist_ok=True)
    with open(os.path.join(tpi_dir, "TPI_vars.pkl"), "wb") as f:
        pickle.dump(tpi_output, f)


def main(time_path=True):
    save_dir = os.path.join(CUR_DIR, "OG-BRA-MultiIndustry")
    work_dir = os.path.join(save_dir, "continuation")
    base_dir = os.path.join(save_dir, "OUTPUT_BASELINE")
    reform_dir = os.path.join(save_dir, "OUTPUT_REFORM")

    ms = _load_multisector()
    gamma = np.array(ms["gamma"])
    Z = np.array(ms["Z"][0])
    print(f"M = {ms['M']} industries, I = {ms['I']} consumption goods")
    print(f"calibrated gamma (capital share) = {np.round(gamma, 4)}")
    print(f"calibrated sector TFP Z_m (Mfg=1) = {np.round(Z, 4)}")

    start = time.time()
    ss, _, good_dir = solve_ss_by_continuation(work_dir)
    print(f"\nTotal SS continuation time = {time.time() - start:.1f}s")
    p_base = build_specifications(
        gamma, Z, baseline=True, output_base=base_dir
    )
    ok = validate_ss(p_base, ss)

    if not time_path:
        sys.exit(0 if ok else 1)

    num_workers = min(multiprocessing.cpu_count(), 7)
    client = Client(n_workers=num_workers, threads_per_worker=1)
    try:
        start = time.time()
        run_baseline_tpi(p_base, good_dir, client)
        print(f"Baseline TPI run time = {time.time() - start:.1f}s")

        cit_reform = (np.array(ms["cit_rate"][0]) * CIT_REFORM_CUT).tolist()
        p_reform = build_specifications(
            gamma,
            Z,
            baseline=False,
            output_base=reform_dir,
            baseline_dir=base_dir,
        )
        p_reform.update_specifications({"cit_rate": [cit_reform]})
        start = time.time()
        runner(p_reform, time_path=True, client=client)
        print(f"Reform SS+TPI run time = {time.time() - start:.1f}s")
    finally:
        client.close()

    base_tpi = safe_read_pickle(os.path.join(base_dir, "TPI", "TPI_vars.pkl"))
    base_params = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))
    reform_tpi = safe_read_pickle(
        os.path.join(reform_dir, "TPI", "TPI_vars.pkl")
    )
    reform_params = safe_read_pickle(
        os.path.join(reform_dir, "model_params.pkl")
    )
    ans = ot.macro_table(
        base_tpi,
        base_params,
        reform_tpi=reform_tpi,
        reform_params=reform_params,
        var_list=["Y", "C", "K", "L", "r", "w"],
        output_type="pct_diff",
        num_years=10,
        start_year=base_params.start_year,
    )
    op.plot_all(base_dir, reform_dir, os.path.join(save_dir, "plots"))
    print("\nPercentage changes, reform vs baseline (first 10 years):")
    print(ans)
    ans.to_csv(os.path.join(save_dir, "OG-BRA_MultiIndustry_output.csv"))


if __name__ == "__main__":
    main(time_path="--ss-only" not in sys.argv)
