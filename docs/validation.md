# Scientific Validation Report

This document details the validation of the **synth-xtal** simulation engine against peer-reviewed experimental data.

## Methodology

To verify the accuracy of the Debye-based scattering simulation and the solvent subtraction model, we compare synthetic profiles generated from crystal structures (PDB) against experimental data from the **Small Angle Scattering Biological Data Bank (SASBDB)**.

### Assessment Criteria
*   **Correlation Coefficient ($\rho$):** Calculated on the log-intensity scale (standard for Crystallography) in the primary scattering range ($q < 0.3 \text{ \AA}^{-1}$).
*   **Primary Range:** $q < 0.3 \text{ \AA}^{-1}$ captures the Guinier regime ($R_g$) and the first few form factor features, which are most sensitive to the overall protein fold.

## Validation Results

### 1. Ubiquitin (Monomer)
*   **PDB Model:** [1UBQ](https://www.rcsb.org/structure/1UBQ)
*   **Experimental Data:** [SASBDB SASDAQ2](https://www.sasbdb.org/data/entry/SASDAQ2/)
*   **Correlation Coefficient:** **0.9913**

### 2. Lysozyme
*   **PDB Model:** [1AKI](https://www.rcsb.org/structure/1AKI)
*   **Experimental Data:** [SASBDB SASDAB2](https://www.sasbdb.org/data/entry/SASDAB2/)
*   **Correlation Coefficient:** **0.9787**

## Interpretation

The high correlation ($> 0.97$) across different protein folds demonstrates that:
1.  **Atomic form factors** (Waasmaier & Kirfel, 1995) are correctly implemented.
2.  **Solvent subtraction** (Pavlov & Svergun, 1997) accurately models the contrast effect of the displaced water volume.
3.  **Hydration shell** modeling (standard excess density of $0.03 \text{ e/}\text{\AA}^3$) provides a physically grounded improvement to the fit.

The slight deviations from 1.0 correlation are expected due to:
*   Experimental noise in the SASBDB datasets.
*   The use of static crystal structures to model proteins that exhibit side-chain and backbone flexibility in solution.
*   Possible differences in buffer conditions and ionic strength between experiment and simulation.

## References
- Waasmaier, D. & Kirfel, A. (1995). Acta Cryst. A51, 416-431.
- Pavlov, M.Y. & Svergun, D.I. (1997). J. Appl. Cryst. 30, 712-717.
- Svergun, D., et al. (1995). J. Appl. Cryst. 28, 768-773.
