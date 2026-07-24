# OG-BRA

| | |
| --- | --- |
| Org | [![PSL cataloged](https://img.shields.io/badge/PSL-cataloged-a0a0a0.svg)](https://www.PSLmodels.org) [![OS License: CC0-1.0](https://img.shields.io/badge/OS%20License-CC0%201.0-yellow)](https://github.com/PSLmodels/OG-BRA/blob/main/LICENSE) |
| Package | [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3129/) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Testing | ![example event parameter](https://github.com/PSLmodels/OG-BRA/actions/workflows/build_and_test.yml/badge.svg?branch=main) ![example event parameter](https://github.com/PSLmodels/OG-BRA/actions/workflows/deploy_docs.yml/badge.svg?branch=main) ![example event parameter](https://github.com/PSLmodels/OG-BRA/actions/workflows/check_ruff.yml/badge.svg?branch=main) [![Codecov](https://codecov.io/gh/PSLmodels/OG-BRA/branch/main/graph/badge.svg)](https://codecov.io/gh/PSLmodels/OG-BRA) |

OG-BRA is an overlapping-generations (OG) model that allows for dynamic general equilibrium analysis of fiscal policy for Brazil. OG-BRA is built on the OG-Core framework. The model output includes changes in macroeconomic aggregates (GDP, investment, consumption), wages, interest rates, and the stream of tax revenues over time. Regularly updated documentation of the model theory--its output, and solution method--and the Python API is available at https://pslmodels.github.io/OG-Core and documentation of the specific Brazil calibration of the model will be available soon.


## Installation

OG-BRA is installed from this GitHub repository. (There is no `pip install ogbra` from PyPI: a PyPI install would not pin the version of OG-Core the model is tested with, and on older Pythons `pip` silently resolves years-old releases. Installing from the repository uses `uv.lock`, which pins the exact tested versions.)

There are two ways to install. The easy way is the OG family's universal installer, which sets up everything in one step. The manual way does the same steps one at a time.

### The easy way: the universal installer

The installer needs only [Git](https://git-scm.com/). It installs [`uv`](https://docs.astral.sh/uv/) if needed, clones OG-BRA into a folder named `OG-BRA` inside your current directory, creates a Python environment in `OG-BRA/.venv` with everything the model needs (downloading a compatible Python if necessary), and verifies the installation.

**macOS** — open Terminal and run each line:

```
xcode-select --install
```

(That installs Git and Apple's command line tools; it is only needed once, and it is fine if it says the tools are already installed.) Then:

```
curl -fsSL https://raw.githubusercontent.com/PSLmodels/OG-Core/master/scripts/install.sh -o install.sh
bash install.sh --repo og-bra --yes
```

**Linux** — Git is usually preinstalled (if not, install it with your distribution's package manager, e.g. `sudo apt install git`). Then:

```
curl -fsSL https://raw.githubusercontent.com/PSLmodels/OG-Core/master/scripts/install.sh -o install.sh
bash install.sh --repo og-bra --yes
```

**Windows** — open PowerShell and run each line:

```
winget install --id Git.Git -e --source winget
```

Close and reopen PowerShell (so Git is on your PATH), then:

```
Invoke-WebRequest -UseBasicParsing -Uri https://raw.githubusercontent.com/PSLmodels/OG-Core/master/scripts/install.ps1 -OutFile install.ps1
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Repo og-bra -Yes
```

More installer options (choosing a destination folder, installing other OG country models) are documented in [OG-Core's quick-install guide](https://github.com/PSLmodels/OG-Core/blob/master/scripts/QUICK_INSTALL.md).

### Manual install

**macOS** — open Terminal and run each line:

```
xcode-select --install
```

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```
source $HOME/.local/bin/env
```

(That last line puts the just-installed `uv` on the current shell's PATH; new terminal windows will have it automatically.) Then:

```
git clone https://github.com/PSLmodels/OG-BRA.git
```

```
cd OG-BRA
```

```
uv sync --extra dev
```

**Linux** — same idea, run each line (install Git first with your package manager if it is missing):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```
source $HOME/.local/bin/env
```

```
git clone https://github.com/PSLmodels/OG-BRA.git
```

```
cd OG-BRA
```

```
uv sync --extra dev
```

**Windows** — open PowerShell and run each line:

```
winget install --id Git.Git -e --source winget
```

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen PowerShell (so Git and `uv` are on your PATH), then:

```
git clone https://github.com/PSLmodels/OG-BRA.git
```

```
cd OG-BRA
```

```
uv sync --extra dev
```

On every platform this leaves you with an `OG-BRA` folder inside the directory where you ran `git clone`, containing the model code and a ready-to-use Python environment in `OG-BRA/.venv`. `uv sync` downloads a compatible Python interpreter if you don't already have one. For docs/Jupyter Book work, also run `uv sync --extra dev --extra docs`.

If you want to contribute changes rather than just run the model, fork this repository on GitHub first and clone your fork instead; the [contributor guide](docs/book/content/contributing/contributor_guide.md) walks through the whole workflow.

### Run an example of the model

From the `OG-BRA` folder:

```
cd examples
```

```
uv run python run_og_bra.py
```

(`uv run` uses the project's `.venv` automatically. If you prefer to activate the environment first: `source .venv/bin/activate` on macOS/Linux, or `.\.venv\Scripts\Activate.ps1` on Windows, then `python run_og_bra.py`.)

**What happens when you run it:**

* If you are connected to the internet, the model refreshes its calibration inputs, including United Nations demographic data. If you are asked for a UN Data Portal API token, just press return — the model falls back to a public data mirror.
* A full run (solving the baseline and reform time paths) takes from about 35 minutes to more than two hours, depending on your machine.
* You can adjust the `./examples/run_og_bra.py` by modifying model parameters specified in the dictionary passed to the `p.update_specifications()` calls.
* Model outputs will be saved in the following files:
  * `./examples/OG-BRA_example_plots`
    * This folder will contain a number of plots generated from OG-Core to help you visualize the output from your run
  * `./examples/ogbra_example_output.csv`
    * This is a summary of the percentage changes in macro variables over the first ten years and in the steady-state.
  * `./examples/OG-BRA-Example/OUTPUT_BASELINE/model_params.pkl`
    * Model parameters used in the baseline run
    * See [`ogcore.execute.py`](https://github.com/PSLmodels/OG-Core/blob/master/ogcore/execute.py) for items in the dictionary object in this pickle file
  * `./examples/OG-BRA-Example/OUTPUT_BASELINE/SS/SS_vars.pkl`
    * Outputs from the model steady state solution under the baseline policy
    * See [`ogcore.SS.py`](https://github.com/PSLmodels/OG-Core/blob/master/ogcore/SS.py) for what is in the dictionary object in this pickle file
  * `./examples/OG-BRA-Example/OUTPUT_BASELINE/TPI/TPI_vars.pkl`
    * Outputs from the model timepath solution under the baseline policy
    * See [`ogcore.TPI.py`](https://github.com/PSLmodels/OG-Core/blob/master/ogcore/TPI.py) for what is in the dictionary object in this pickle file
  * An analogous set of files in the `./examples/OUTPUT_REFORM` directory, which represent objects from the simulation of the reform policy

If you run into errors running the example script, please open a new issue in the OG-BRA repo with a description of the issue and any relevant tracebacks you receive.

Once the package is installed, one can adjust parameters in the OG-Core `Specifications` object using the `Calibration` class as follows:

```
from ogcore.parameters import Specifications
from ogbra.calibrate import Calibration
p = Specifications()
c = Calibration(p)
updated_params = c.get_dict()
p.update_specifications({'initial_debt_ratio': updated_params['initial_debt_ratio']})
```

## Disclaimer
The organization of this repository will be changing rapidly, but the `OG-BRA/examples/run_og_bra.py` script will be kept up to date to run with the main branch of this repo.

## Core Maintainers

The core maintainers of the OG-BRA repository are:

* Marcelo LaFleur (GitHub handle: [@SeaCelo](https://github.com/SeaCelo)), Senior Economist, Department of Economic and Social Affairs (DESA), United Nations
* [Richard W. Evans](https://sites.google.com/site/rickecon/) (GitHub handle: [@rickecon](https://github.com/rickecon)), Senior Research Fellow and Director of Open Policy, Center for Growth and Opportunity at Utah State University; President, Open Research Group, Inc.
* [Jason DeBacker](https://jasondebacker.com) (GitHub handle: [@jdebacker](https://github.com/jdebacker)), Associate Professor, University of South Carolina; Vice President of Research, Open Research Group, Inc.

## Citing OG-BRA

OG-BRA (Version #.#.#)[Source code], https://github.com/PSLmodels/OG-BRA
