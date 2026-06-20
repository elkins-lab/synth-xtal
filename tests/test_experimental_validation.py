import os
import tempfile
import urllib.request
import pytest
import numpy as np
import reciprocalspaceship as rs
from scipy.stats import pearsonr
from synth_xtal.simulator import simulate_diffraction


def test_experimental_validation():
    """
    Validate synthetic structure factors against peer-reviewed experimental data.
    Uses 4LZT (Lysozyme, 0.95 Å resolution).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        pdb_path = os.path.join(tmpdir, "4LZT.pdb")
        sf_path = os.path.join(tmpdir, "4LZT-sf.cif")
        mtz_path = os.path.join(tmpdir, "4LZT_calc.mtz")

        # 1. Download peer-reviewed experimental data
        try:
            urllib.request.urlretrieve("https://files.rcsb.org/download/4LZT.pdb", pdb_path)
            urllib.request.urlretrieve("https://files.rcsb.org/download/4LZT-sf.cif", sf_path)
        except Exception as e:
            pytest.skip(f"Failed to download test data from RCSB: {e}")

        import gemmi

        # Strip ANISOU records since 4LZT has a non-positive definite tensor that causes NaNs in simulation
        st = gemmi.read_structure(pdb_path)
        for model in st:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        atom.aniso = gemmi.SMat33f(0, 0, 0, 0, 0, 0)
        st.write_pdb(pdb_path)

        # 2. Simulate structure factors at 1.5A resolution
        simulate_diffraction(pdb_path, mtz_path, d_min=1.5, use_bulk_solvent=True)

        # 3. Read the calculated and experimental data
        calc_ds = rs.read_mtz(mtz_path)
        exp_ds = rs.read_cif(sf_path)

        # In our simulation, columns are 'FC' and 'PHIC'
        # In experimental data for 4LZT, we have 'IMEAN'
        # Let's filter out negative intensities and approximate F_obs = sqrt(I)
        exp_ds = exp_ds[exp_ds["IMEAN"] > 0]
        exp_ds["F_obs"] = np.sqrt(exp_ds["IMEAN"])

        # Rename calculated FC so it doesn't clash with experimental FC if present
        calc_ds.rename(columns={"FC": "F_calc"}, inplace=True)

        # Merge datasets on Miller indices
        merged = exp_ds.merge(calc_ds, left_index=True, right_index=True, how="inner")
        assert len(merged) > 1000, "Should have many overlapping reflections"

        # Calculate Pearson correlation between simulated F_calc and experimental F_obs
        f_calc = merged["F_calc"].to_numpy(dtype=np.float64)
        f_obs = merged["F_obs"].to_numpy(dtype=np.float64)

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mask = ~np.isnan(f_calc) & ~np.isnan(f_obs)
            corr, _ = pearsonr(f_calc[mask], f_obs[mask])

        # For a raw, unscaled simulation without B-factor/solvent tuning,
        # a Pearson correlation > 0.8 is extremely strong evidence of physical validity.
        assert corr > 0.80, f"Correlation with experimental data is too low: {corr:.3f}"

        # Also check correlation with deposited FC (should be even higher, ~0.99)
        if "FC" in merged.columns:
            fc_deposited = merged["FC"].to_numpy(dtype=np.float64)
            mask_fc = ~np.isnan(f_calc) & ~np.isnan(fc_deposited)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                corr_fc, _ = pearsonr(f_calc[mask_fc], fc_deposited[mask_fc])
            assert corr_fc > 0.90, f"Correlation with deposited FC is too low: {corr_fc:.3f}"
