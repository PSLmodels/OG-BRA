"""
Import smoke tests for installed package usage.
"""


def test_import_smoke():
    import ogbra
    from ogbra import macro_params
    from ogbra.calibrate import Calibration

    assert ogbra is not None
    assert macro_params is not None
    assert Calibration is not None
