# synth-xtal

Simulates X-ray crystallography diffraction data (structure factors and MTZ files) from input atomic models (PDB/mmCIF files).

## Installation

```bash
pip install synth-xtal
```

## Usage

You can use the command-line interface to simulate an MTZ file from a PDB:

```bash
synth-xtal input.pdb -o simulated.mtz --resolution 2.0
```

If the input PDB lacks a unit cell (CRYST1 record), `synth-xtal` will automatically place the molecule in a P1 unit cell with a 10 Å margin around the bounding box.
