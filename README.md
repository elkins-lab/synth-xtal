# synth-xtal

[![codecov](https://codecov.io/gh/elkins-lab/synth-xtal/branch/main/graph/badge.svg)](https://codecov.io/gh/elkins-lab/synth-xtal)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/13300/badge)](https://www.bestpractices.dev/projects/13300)
[![PyPI version](https://img.shields.io/pypi/v/synth-xtal.svg)](https://pypi.org/project/synth-xtal/)
[![Python](https://img.shields.io/pypi/pyversions/synth-xtal.svg)](https://pypi.org/project/synth-xtal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/elkins-lab/synth-xtal/actions/workflows/test.yml/badge.svg)](https://github.com/elkins-lab/synth-xtal/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/type%20checked-mypy-blue)](https://mypy-lang.org/)

**synth-xtal** is a lightweight Python library for simulating X-ray Crystallography diffraction data (structure factors and MTZ files) from input atomic models (PDB/mmCIF files).

Extracted from the [synth-pdb](https://github.com/elkins/synth-pdb) ecosystem, it provides a physically grounded, education-focused engine for reciprocal space simulation.

---

### 🧪 For Structural Biologists
*   **Virtual Crystallography:** Generate ideal $F_{calc}$ and $\phi_{calc}$ structure factors from structural models.
*   **Automated Cell Generation:** Transparently computes optimal bounding unit cells in $P 1$ for standalone peptides/proteins lacking periodic symmetry constraints.

### 🤖 For Machine Learning Researchers
*   **Standard Integrations:** Built directly on top of `gemmi` and `reciprocalspaceship` for native FFT acceleration and robust MTZ writing.
*   **Multi-Model Support:** Seamlessly handles NMR ensembles or MD trajectories by accurately averaging grid densities to simulate alternative conformations.
*   **Educational Clarity:** Simple, well-commented implementation of crystallographic density mapping — easy to audit and extend.

---

## Features
- **Diffraction Simulation:** Direct generation of complex structure factors from atomic coordinates using `gemmi.DensityCalculatorX`.
- **Ensemble Averaging:** Calculates coherent scattering intensities over an ensemble of structural models.
- **Pythonic Data Structures:** Outputs are formatted to `reciprocalspaceship.DataSet` objects for seamless downstream integration with standard ML/data-science tools (Pandas).

## Installation
```bash
# Basic installation
pip install synth-xtal

# Installation for contributors/developers
pip install "synth-xtal[dev,test,docs]"
```

## Command-Line Interface (CLI)

`synth-xtal` provides a simple CLI for rapid simulation:

```bash
# Basic simulation (outputs to MTZ format)
synth-xtal input.pdb -o simulated.mtz

# Simulation at a specific high-resolution limit (e.g., 1.5 Å)
synth-xtal input.pdb -o simulated.mtz --resolution 1.5

# Simulation with a custom padding margin for automatically generated unit cells
synth-xtal input.pdb -o simulated.mtz --margin 15.0
```

### CLI Arguments
- `input`: Path to PDB or mmCIF file.
- `-o`, `--output`: Save structure factor data to an `.mtz` file (Required).
- `-d`, `--resolution`: High resolution limit in Ångströms (default: 2.0).
- `--margin`: Margin in Ångströms for the unit cell bounding box if the input lacks a defined unit cell (default: 10.0).

## Quick Start

### Python API
```python
from synth_xtal.simulator import simulate_diffraction

# Calculate MTZ from a PDB or mmCIF file
simulate_diffraction(
    input_pdb="protein.cif",
    output_mtz="simulated_data.mtz",
    d_min=2.0
)
```

## Tutorials

Try out `synth-xtal` interactively in Google Colab:

- **01. Crystallography Basics:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/elkins-lab/synth-xtal/blob/main/examples/interactive_tutorials/01_crystallography_basics.ipynb)
- **02. Experimental Validation (4LZT):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/elkins-lab/synth-xtal/blob/main/examples/interactive_tutorials/02_experimental_validation.ipynb)
- **03. Virtual Crystallography Lab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/elkins-lab/synth-xtal/blob/main/examples/interactive_tutorials/03_virtual_crystallography_lab.ipynb)

## Acknowledgements
`synth-xtal` was heavily inspired by the educational goals of the larger [synth-pdb](https://github.com/elkins/synth-pdb) ecosystem and relies critically on:
- [gemmi](https://gemmi.readthedocs.io/) - for core density calculations and FFT operations.
- [reciprocalspaceship](https://rs-station.github.io/reciprocalspaceship/) - for MTZ manipulation and Pandas integration.
