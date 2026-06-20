# synth-xtal

**synth-xtal** is a lightweight Python library for simulating X-ray Crystallography profiles and structure factors from protein coordinates.

Extracted from the [synth-pdb](https://github.com/elkins/synth-pdb) ecosystem, it provides a physically grounded, education-focused engine for reciprocal space simulation.

---

## 🧪 Key Features

*   **Diffraction Simulation:** Direct generation of Structure Factors ($F_{calc}$ and $\phi_{calc}$) from atomic coordinates.
*   **Gemmi & Reciprocalspaceship:** Leverages standard crystallographic libraries for native FFT integration and MTZ writing.
*   **Automated Unit Cells:** Transparently computes optimal bounding unit cells for standalone peptides/proteins lacking periodic symmetry constraints.

## 🚀 Quick Start

### Installation
```bash
pip install synth-xtal
```

### Basic Usage
```python
from synth_xtal.simulator import simulate_diffraction

# Calculate MTZ from PDB
simulate_diffraction("input.pdb", "output.mtz", d_min=2.0)
```

## 📚 Documentation Sections
*   [API Reference](api.md): Detailed function and class signatures.
*   [Scientific Rationale](science.md): The physics and mathematics behind the engine.
*   [Validation Report](validation.md): Comparison against experimental datasets.
