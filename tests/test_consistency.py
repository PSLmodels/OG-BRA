"""Guards against calibration/ogcore drift and corrupted ogcore installs.

Two real incidents motivate these tests (July 2026):

1. ogcore 0.16.3 reworked the pre-time-path demographics
   (PSLmodels/OG-Core#1073), adding period-0 seed parameters. The packaged
   ``ogbra_default_parameters.json``, baked under an older ogcore, was
   silently inconsistent: the baseline time path converged but violated the
   resource constraint. The schema-coverage tests below fail loudly when the
   installed ogcore defines demographic parameters the packaged baseline
   does not carry (fix: regenerate the demographics, see CHANGELOG).

2. A locally-built development wheel of ogcore, cached by the package
   manager under the release version number, shadowed the real PyPI 0.16.3
   (its parameter schema lacked the new fields). The feature-canary and
   wheel-RECORD tests below fail on such an install.
"""

import base64
import csv
import hashlib
import json
from pathlib import Path

import pytest
from ogcore.parameters import Specifications
import importlib.resources


def _load_ogbra_defaults():
    with importlib.resources.open_text(
        "ogbra", "ogbra_default_parameters.json"
    ) as f:
        return json.load(f)


def _load_ogcore_schema():
    with importlib.resources.open_text(
        "ogcore", "default_parameters.json"
    ) as f:
        return json.load(f)


def test_defaults_json_loads_into_specifications():
    """The packaged baseline must validate against the installed ogcore.

    Catches fields the installed ogcore does not know (baseline regenerated
    under a newer ogcore than the one installed).
    """
    p = Specifications()
    p.update_specifications(_load_ogbra_defaults())


def test_demographic_schema_coverage():
    """Every pre-time-path seed the installed ogcore defines must be baked
    into the packaged baseline.

    If this fails, ogcore changed its demographics interface and the
    packaged demographics must be regenerated under the installed ogcore
    (see the ogcore 0.16.3 entry in CHANGELOG.md).
    """
    schema = _load_ogcore_schema()
    defaults = _load_ogbra_defaults()
    seeds = {k for k in schema if k.endswith("_preTP")}
    assert seeds, "ogcore schema defines no *_preTP seeds — interface changed?"
    missing = sorted(seeds - set(defaults))
    assert not missing, (
        f"Packaged baseline lacks demographic seed(s) {missing} defined by "
        "the installed ogcore. Regenerate the packaged demographics under "
        "this ogcore version."
    )


def test_ogcore_has_expected_feature_set():
    """Feature canary: the installed ogcore must expose the 0.16.3
    demographics fields its version claims.

    ogbra requires ogcore>=0.16.3, which introduced the period-0 seeds. A
    stale or locally-built ogcore masquerading under the release version
    fails here even when ``ogcore.__version__`` looks right.
    """
    schema = _load_ogcore_schema()
    expected = {"g_n_preTP", "imm_rates_preTP", "rho_preTP", "omega_S_preTP"}
    missing = sorted(expected - set(schema))
    assert not missing, (
        f"Installed ogcore lacks {missing} despite ogbra requiring "
        ">=0.16.3 — the install does not match the release it claims. "
        "Purge the package cache and reinstall ogcore from PyPI."
    )


def test_ogcore_install_matches_wheel_record():
    """Installed ogcore files must match the per-file hashes in the wheel's
    RECORD — catches installs whose files were mixed or overwritten.
    """
    import ogcore

    site = Path(ogcore.__file__).parent.parent
    dist_infos = list(site.glob("ogcore-*.dist-info"))
    if not dist_infos:
        pytest.skip("ogcore not installed from a wheel (no dist-info)")
    record = dist_infos[0] / "RECORD"
    if not record.exists():
        pytest.skip("no RECORD file for ogcore install")

    bad = []
    with record.open(newline="") as f:
        for row in csv.reader(f):
            if len(row) < 2:
                continue
            path, hash_spec = row[0], row[1]
            if not path.startswith("ogcore/") or not hash_spec:
                continue
            algo, _, expected = hash_spec.partition("=")
            target = site / path
            if not target.exists():
                bad.append(path + " (missing)")
                continue
            digest = hashlib.new(algo, target.read_bytes()).digest()
            actual = (
                base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
            )
            if actual != expected:
                bad.append(path)
    assert not bad, (
        "Installed ogcore files differ from the wheel RECORD (corrupted or "
        f"mixed install): {bad}. Purge the package cache and reinstall."
    )
