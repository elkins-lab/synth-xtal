# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.7] - 2026-06-18

### Added
- Added `preprocess_structure` utility with `keep_nucleic_acids=True` support to explicitly preserve DNA/RNA chains during Crystallography buffer subtraction.
- Added interactive tutorial on detecting allosteric hinge motions using HIV-1 Reverse Transcriptase as a model system.
- Added interactive tutorial bridging `synth-pdb` and `synth-xtal`.

### Fixed
- Fixed Jupyter Notebook `ModuleNotFoundError` issues in Colab by isolating package installations into separate execution cells.
- Fixed codecov badge path mapping by adding `codecov.yml` configuration.

## [0.1.4] - 2026-06-18

### Added
- OpenSSF Best Practices badge support, issue templates, security policy, and contributing guidelines.
- Community and security files (`CODE_OF_CONDUCT.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`).
- Reached 100% test coverage in CLI, engine, and visualization modules.
- Peer-reviewed validation suite against SASBDB datasets.
- Interactive hydration shell tutorial and Google Colab integration.

### Fixed
- Resolved Windows CI build issues (TclError and UnicodeDecodeError).
- Fixed missing `hypothesis` dependency for property-based testing.
- Standardized Google Colab setup blocks across all notebooks.
- Restructured tutorials and updated documentation links to the elkins-lab organization.
- Improved `docs/index.md` landing page.

## [0.1.3] - 2026-06-07

### Changed
- Maintenance release: General updates, dependency pins, and CI/CD workflow improvements.
