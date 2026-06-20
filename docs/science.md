# Scientific Background

**synth-xtal** is built on a robust set of fundamental biophysical equations for simulating Small-Angle X-ray Scattering (Crystallography) from atomic coordinates. This document outlines the physical models and their limits of validity.

## 1. The Debye Formula
The total scattering intensity $I(q)$ of a molecule in a vacuum is computed by summing the interference between all pairs of atoms $i$ and $j$:

$$I_{vac}(q) = \sum_i \sum_j f_i(q) f_j(q) \frac{\sin(q r_{ij})}{q r_{ij}}$$

Where:
- $q$ is the momentum transfer magnitude ($q = \frac{4\pi \sin(\theta)}{\lambda}$).
- $r_{ij}$ is the Euclidean distance between atom $i$ and atom $j$.
- $f_i(q)$ is the atomic scattering factor for atom $i$.

### Atomic Form Factors (Cromer-Mann)
To accurately represent how individual atoms scatter X-rays, we use the Cromer-Mann parameterization, which models the atomic scattering factor as a sum of Gaussians:

$$f_i(q) = c_i + \sum_{k=1}^4 a_{i,k} \exp\left(-b_{i,k} \left(\frac{q}{4\pi}\right)^2\right)$$

The constants $a$, $b$, and $c$ are element-specific and derived from quantum mechanical calculations of electron density.

---

## 2. Solvent Displacement
In solution, scattering is driven by the **contrast** between the protein and the bulk solvent. A protein displaces a volume of water, creating a "hole" in the solvent that also scatters X-rays.

We use the established **Pavlov & Svergun (1997)** model for solvent subtraction. The effective scattering factor of an atom in solution becomes:

$$f_{eff}(q) = f_{vac}(q) - \rho_{sol} V_i \exp\left(-\frac{q^2 V_i^{2/3}}{10}\right)$$

Where:
- $\rho_{sol}$ is the electron density of the bulk solvent (e.g., $334 e nm^{-3}$ for water).
- $V_i$ is the excluded volume of atom $i$.

This approach computationally subtracts the "dummy atom" solvent displacement without requiring an explicit simulation box of water molecules, significantly speeding up calculation.

---

## 3. Analytical Tools: Guinier and Kratky Plots

`synth-xtal` provides built-in visualization tools to analyze the overall shape and flexibility of the simulated structure.

### The Guinier Approximation
At very low angles ($q \cdot R_g < 1.3$), the scattering curve can be approximated by a Gaussian:

$$I(q) \approx I(0) \exp\left(-\frac{q^2 R_g^2}{3}\right)$$

By plotting $\ln(I(q))$ against $q^2$ (a **Guinier Plot**), the $y$-intercept gives the forward scattering $I(0)$ (proportional to molecular weight), and the slope gives the Radius of Gyration ($R_g$), a measure of the protein's overall size.

### The Kratky Plot
A **Kratky Plot** displays $q^2 \cdot I(q)$ versus $q$.
- **Folded proteins** exhibit a distinct bell-shaped peak, as the intensity falls off rapidly according to Porod's Law ($I(q) \propto q^{-4}$).
- **Unfolded or highly flexible proteins** lack a well-defined boundary, causing the curve to plateau or rise at higher $q$ values.

---

## 4. Limits of Validity
While `synth-xtal` provides a highly accurate O(N²) calculation, users should be aware of the underlying physical assumptions:

1. **High $q$ Deviations ($q > 0.5 \AA^{-1}$):** The Pavlov & Svergun implicit solvent model assumes a uniform bulk hydration shell. At wide angles (high $q$), the scattering becomes sensitive to the *explicit* structured water molecules bound to the protein surface. For atomic-resolution wide-angle scattering (WAXS), explicit molecular dynamics simulations of the hydration shell are required.
2. **Missing Hydrogens:** The simulation accuracy is dependent on the completeness of the input structure. If hydrogens are missing, the total electron density is under-represented, which will severely skew $I(0)$ and slightly alter the overall curve shape. Ensure your structures are fully protonated before calculation.
3. **Static Representation:** A single PDB file is a static snapshot. Real Crystallography data is an ensemble average over all conformational states in solution. For flexible proteins, calculating the profile of a single structure will fail to capture the solution reality. We recommend integrating `synth-xtal` with ensemble generators for these cases.
