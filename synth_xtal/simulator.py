import gemmi
import numpy as np


def calculate_bounding_box(structure: gemmi.Structure) -> tuple:
    """Calculate the bounding box of a gemmi Structure."""
    min_pos = np.array([float("inf"), float("inf"), float("inf")])
    max_pos = np.array([-float("inf"), -float("inf"), -float("inf")])

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    pos = atom.pos
                    arr = np.array([pos.x, pos.y, pos.z])
                    min_pos = np.minimum(min_pos, arr)
                    max_pos = np.maximum(max_pos, arr)

    return min_pos, max_pos


def simulate_diffraction(
    input_pdb: str,
    output_mtz: str,
    d_min: float = 2.0,
    margin: float = 10.0,
    use_bulk_solvent: bool = False,
    k_sol: float = 0.35,
    b_sol: float = 45.0,
):
    """
    Simulate an MTZ file containing structure factors from a PDB model.
    If the PDB lacks a CRYST1 record (unit cell), a P 1 unit cell is
    automatically generated with the specified margin.
    """
    st = gemmi.read_structure(input_pdb)

    # Check if we need to add a unit cell (gemmi defaults to 1x1x1 if missing)
    if st.cell.a == 1.0 and st.cell.b == 1.0 and st.cell.c == 1.0:
        print(f"No unit cell found in {input_pdb}. Creating a default P 1 unit cell.")
        st.spacegroup_hm = "P 1"

        min_pos, max_pos = calculate_bounding_box(st)
        dimensions = max_pos - min_pos + (2 * margin)

        # Move the structure to the center of the new cell
        # Calculate the shift required to move the min_pos to (margin, margin, margin)
        shift = np.array([margin, margin, margin]) - min_pos

        for model in st:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        atom.pos.x += shift[0]
                        atom.pos.y += shift[1]
                        atom.pos.z += shift[2]

        st.cell = gemmi.UnitCell(dimensions[0], dimensions[1], dimensions[2], 90.0, 90.0, 90.0)
        print(f"New unit cell: {st.cell.a:.2f}, {st.cell.b:.2f}, {st.cell.c:.2f}, 90, 90, 90")

    # We will use gemmi's DensityCalculatorX and reciprocalspaceship
    # to calculate and write structure factors.
    dc = gemmi.DensityCalculatorX()
    dc.d_min = d_min

    # Apply cell and spacegroup to density calculator
    dc.set_grid_cell_and_spacegroup(st)

    # Calculate density for all models in the ensemble
    # This correctly superimposes densities, equivalent to alternative conformations
    # To maintain scaling, we scale the entire grid by 1 / N_models if there are multiple models
    for model in st:
        dc.put_model_density_on_grid(model)

    num_models = len(st)
    if num_models > 1:
        # Scale grid by 1 / num_models to get the average density
        grid_array = np.array(dc.grid, copy=False)
        grid_array *= 1.0 / num_models

    # Perform FFT to reciprocal space
    f_phi = gemmi.transform_map_to_f_phi(dc.grid)

    # Get the asymmetric unit data
    asu_data = f_phi.prepare_asu_data(d_min)

    import reciprocalspaceship as rs

    # Extract Miller indices and complex structure factors
    hkl = np.array(asu_data.miller_array)
    values_p = np.array(asu_data.value_array, copy=False)

    if use_bulk_solvent:
        # Calculate bulk solvent mask
        masker = gemmi.SolventMasker(gemmi.AtomicRadiiSet.VanDerWaals, 0.0)
        mask_grid = gemmi.FloatGrid(dc.grid.nu, dc.grid.nv, dc.grid.nw)
        mask_grid.set_unit_cell(dc.grid.unit_cell)
        mask_grid.spacegroup = dc.grid.spacegroup

        for model in st:
            masker.put_mask_on_float_grid(mask_grid, model)

        if num_models > 1:
            mask_array = np.array(mask_grid, copy=False)
            mask_array *= 1.0 / num_models

        f_phi_m = gemmi.transform_map_to_f_phi(mask_grid)
        asu_data_m = f_phi_m.prepare_asu_data(d_min)
        values_m = np.array(asu_data_m.value_array, copy=False)
    else:
        values_m = np.zeros_like(values_p)

    sg = st.find_spacegroup()

    print(f"Spacegroup: {sg.hm}, Cell: {st.cell.a}, {st.cell.b}, {st.cell.c}")
    print(f"Generated {len(hkl)} reflections")

    if use_bulk_solvent:
        # Compute dHKL using a temporary DataSet
        ds_temp = rs.DataSet(
            {"H": hkl[:, 0], "K": hkl[:, 1], "L": hkl[:, 2]}, spacegroup=sg, cell=st.cell
        )
        ds_temp.compute_dHKL(inplace=True)
        d_star_sq = 1.0 / (ds_temp["dHKL"].to_numpy() ** 2)
        solvent_scale = k_sol * np.exp(-b_sol / 4.0 * d_star_sq)
        values_total = values_p + solvent_scale * values_m
    else:
        values_total = values_p

    # Create the final reciprocalspaceship DataSet
    ds = rs.DataSet(
        {
            "H": hkl[:, 0],
            "K": hkl[:, 1],
            "L": hkl[:, 2],
            "FC": np.abs(values_total),
            "PHIC": np.angle(values_total, deg=True),
        },
        spacegroup=sg,
        cell=st.cell,
    )

    # Assign appropriate MTZ datatypes (e.g. 'F' for amplitudes, 'P' for phases)
    ds.infer_mtz_dtypes(inplace=True)

    # Set the dataset as the index (H, K, L)
    ds.set_index(["H", "K", "L"], inplace=True)

    # Write to MTZ
    ds.write_mtz(output_mtz)
    print(f"Simulation successful. MTZ written to {output_mtz}")
