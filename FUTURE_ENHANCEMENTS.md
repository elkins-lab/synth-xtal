# Future Enhancements for synth-xtal

These are potential feature enhancements to consider for future sprints, aimed at improving `synth-xtal` for Machine Learning Researchers and Educators.

## 1. Simulating Experimental Noise & Errors
Right now, `synth-xtal` produces mathematically "perfect" $F_{calc}$ amplitudes. Since one of the target audiences is **Machine Learning Researchers**, adding the ability to inject realistic experimental noise would be highly valuable.
- Consider adding a `--noise` parameter that applies Gaussian or Poisson-distributed noise to the structure factors based on resolution, simulating counting statistics and detector noise.
- This would allow ML models to train on realistic $F_{obs}$-like datasets rather than idealized data.

## 2. Simulating Data Incompleteness
Real crystallographic datasets are rarely 100% complete, especially in the highest resolution shells or if there is radiation damage.
- A feature to randomly drop a percentage of reflections, or simulate a "missing wedge" of data, would be excellent for training ML models focused on reflection imputation or map density completion.

## 3. Anomalous Scattering (SAD/MAD)
For the educational side of the project ("Virtual Crystallography Lab"), teaching students about experimental phasing (SAD/MAD) is a critical topic.
- You could add support for simulating anomalous pairs ($F^+$ and $F^-$) by passing custom anomalous scattering factors ($f'$ and $f''$) for heavy atoms like Selenium or anomalous metals.
- `gemmi` already supports these calculations under the hood, but exposing them via a simple API/CLI flag would make `synth-xtal` an incredible teaching tool for phasing.

## 4. Overall Anisotropic B-factor Scaling
The simulator currently applies an overall exponential scaling for bulk solvent. It might be beneficial to allow users to specify an overall anisotropic B-factor (a $3 \times 3$ tensor) for the entire crystal, which is commonly refined in real datasets, rather than relying solely on the individual atomic B-factors in the input PDB.
