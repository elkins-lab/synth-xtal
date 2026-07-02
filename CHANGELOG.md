# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-07-02

### Fixed
- Untracked `synth_xtal.egg-info` to fix PyPI release failures caused by `setuptools_scm` identifying the build as dirty.

## [0.2.0] - 2026-07-02

### Added
- Bulk solvent modeling for more accurate low-resolution $F_{calc}$ simulation.
- Multi-model ensemble averaging for structure factors (NMR ensembles, MD trajectories).
- Virtual crystallography lab interactive tutorial.
- PyPI Trove classifiers in `pyproject.toml` to support the Python version badge.
- Added `FUTURE_ENHANCEMENTS.md` for local planning of future features (noise injection, missing wedges, anomalous scattering).

### Fixed
- Fixed a bug where bulk solvent masking for multiple models would overwrite instead of accumulate, applying only the final model's mask.
- Fixed `mypy` typing errors related to `gemmi.Model` string initialization and missing return type hints.
- Fixed `synth-pdb` syntax in tutorials and updated installation instructions.
- Suppressed `scipy` pearson correlation overflow warnings during experimental validation tests.

## [0.1.0] - 2026-06-18

### Added
- Initial release of `synth-xtal` (extracted from the `synth-pdb` ecosystem).
- Direct generation of complex structure factors from atomic coordinates using `gemmi.DensityCalculatorX`.
- Automated $P 1$ unit cell generation for missing periodic symmetries.
- Experimental validation suite against peer-reviewed data (4LZT, 0.95 Å resolution).
- Google Colab integration and interactive tutorials (Crystallography Basics, Experimental Validation).
- Pythonic data outputs via `reciprocalspaceship.DataSet` objects.
