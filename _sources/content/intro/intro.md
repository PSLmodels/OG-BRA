(Chap_Intro)=
# OG-BRA

| | |
| --- | --- |
| Org | [![United Nations DESA](https://img.shields.io/badge/United%20Nations%20DESA-blue)](https://www.un.org/en/desa) [![PSL cataloged](https://img.shields.io/badge/PSL-cataloged-a0a0a0.svg)](https://www.PSLmodels.org) [![OS License: CC0-1.0](https://img.shields.io/badge/OS%20License-CC0%201.0-yellow)](https://github.com/PSLmodels/OG-BRA/blob/main/LICENSE) |
| Package | [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31013/) [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3116/) [![PyPI Latest Release](https://img.shields.io/pypi/v/ogbra.svg)](https://pypi.org/project/ogbra/) [![PyPI Downloads](https://img.shields.io/pypi/dm/ogbra.svg?label=PyPI%20downloads)](https://pypi.org/project/ogbra/) |
| Testing | ![example event parameter](https://github.com/PSLmodels/OG-BRA/actions/workflows/build_and_test.yml/badge.svg?branch=main) ![example event parameter](https://github.com/PSLmodels/OG-BRA/actions/workflows/deploy_docs.yml/badge.svg?branch=main) ![example event parameter](https://github.com/PSLmodels/OG-BRA/actions/workflows/check_format.yml/badge.svg?branch=main) [![Codecov](https://codecov.io/gh/PSLmodels/OG-BRA/branch/main/graph/badge.svg)](https://codecov.io/gh/PSLmodels/OG-BRA) |

[`OG-BRA`](https://github.com/PSLmodels/OG-BRA) is a Python package that provides code and data to calibrate an overlapping-generations (OG) model to the economy of Brazil (BRA), the code of which is hosted on GitHub at https://github.com/PSLmodels/OG-BRA. `OG-BRA` uses as a dependency the [`OG-Core`](https://pslmodels.github.io/OG-Core/) package, which contains the core theory and logic of a general OG model. The `OG-BRA` calibration package and the `OG-Core` theory and logic make the model that allows for dynamic general equilibrium analysis of federal fiscal policy in the Republic of Brazil. The model output focuses on changes in macroeconomic aggregates (GDP, investment, consumption), wages, interest rates, and the stream of tax revenues over time. This documentation of the `OG-BRA` package contains the following major sections, which are regularly updated.

* Contributing to `OG-BRA`
* `OG-BRA` API
* Calibration
* References
* Citations of `OG-BRA`


(Sec_CoreMaintainers)=
## Core Maintainers

Marcelo LaFleur (GitHub handle [@SeaCelo](https://github.com/SeaCelo)),  [Jason DeBacker](https://jasondebacker.com) (GitHub handle [@jdebacker](https://github.com/jdebacker)), and [Richard W. Evans](https://sites.google.com/site/rickecon/) (GitHub handle [@rickecon](https://github.com/rickecon)) are the core maintainers of `OG-BRA`. If you have questions about or contributions to the model or repository, please submit a GitHub "Issue" described in the {ref}`Sec_GitHubIssue` subsection or "Pull Request" as described in the {ref}`Sec_GitHubPR` subsection of the {ref}`Sec_Workflow` section of the `OG-BRA` {ref}`Chap_ContribGuide`.


(Sec_Disclaimer)=
## Disclaimer

The model is continuously under development. Users will be notified through [closed PR threads](https://github.com/PSLmodels/OG-BRA/pulls?q=is%3Apr+is%3Aclosed) and through the [release notes](https://github.com/PSLmodels/OG-BRA/releases) what changes have been implemented. The package will have released versions, which will be checked against existing code prior to release. Stay tuned for an upcoming release!


(Sec_CitingOGBRA)=
## Citing OG-BRA

`OG-BRA` (Version #.#.#)[Source code], https://github.com/PSLmodels/OG-BRA
