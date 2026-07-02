import os
import tempfile
import gemmi

from synth_xtal.simulator import simulate_diffraction


def create_dummy_pdb(path):
    st = gemmi.Structure()
    st.cell = gemmi.UnitCell(20, 20, 20, 90, 90, 90)
    st.spacegroup_hm = "P 1"

    model = gemmi.Model("1")  # type: ignore[arg-type]
    chain = gemmi.Chain("A")
    res = gemmi.Residue()
    res.name = "ALA"
    res.seqid = gemmi.SeqId("1")

    atom = gemmi.Atom()
    atom.name = "CA"
    atom.element = gemmi.Element("C")
    atom.pos = gemmi.Position(10.0, 10.0, 10.0)
    atom.b_iso = 20.0
    res.add_atom(atom)
    chain.add_residue(res)
    model.add_chain(chain)
    st.add_model(model)
    st.write_pdb(path)


def create_cell_less_pdb(path):
    st = gemmi.Structure()

    model = gemmi.Model("1")  # type: ignore[arg-type]
    chain = gemmi.Chain("A")
    res = gemmi.Residue()
    res.name = "ALA"
    res.seqid = gemmi.SeqId("1")

    atom = gemmi.Atom()
    atom.name = "CA"
    atom.element = gemmi.Element("C")
    atom.pos = gemmi.Position(5.0, 5.0, 5.0)
    atom.b_iso = 20.0
    res.add_atom(atom)
    chain.add_residue(res)
    model.add_chain(chain)
    st.add_model(model)
    st.write_pdb(path)


def test_simulate_diffraction_with_cell():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdb_path = os.path.join(tmpdir, "test.pdb")
        mtz_path = os.path.join(tmpdir, "test.mtz")

        create_dummy_pdb(pdb_path)

        simulate_diffraction(pdb_path, mtz_path, d_min=3.0)

        assert os.path.exists(mtz_path)

        # Verify MTZ contents
        mtz = gemmi.read_mtz_file(mtz_path)
        assert mtz.resolution_high() <= 3.1
        assert mtz.spacegroup.hm == "P 1"
        assert len(mtz.columns) > 3  # H, K, L and some data columns like FC, PHIC


def test_simulate_diffraction_multi_model():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdb_path = os.path.join(tmpdir, "multi.pdb")
        mtz_path = os.path.join(tmpdir, "multi.mtz")

        # Create a dummy structure with 2 models
        st = gemmi.Structure()
        st.cell = gemmi.UnitCell(10.0, 10.0, 10.0, 90.0, 90.0, 90.0)
        st.spacegroup_hm = "P 1"
        for i in range(2):
            model = gemmi.Model(str(i + 1))  # type: ignore[arg-type]
            chain = gemmi.Chain("A")
            res = gemmi.Residue()
            res.name = "ALA"
            atom = gemmi.Atom()
            atom.name = "CA"
            atom.element = gemmi.Element("C")
            # Shift the atom in the second model
            atom.pos = gemmi.Position(5.0 + i, 5.0, 5.0)
            atom.occ = 1.0
            atom.b_iso = 20.0
            res.add_atom(atom)
            chain.add_residue(res)
            model.add_chain(chain)
            st.add_model(model)
        st.write_pdb(pdb_path)

        simulate_diffraction(pdb_path, mtz_path, d_min=3.0)

        assert os.path.exists(mtz_path)
        mtz = gemmi.read_mtz_file(mtz_path)
        assert len(mtz.columns) > 3


def test_simulate_diffraction_multi_model_bulk_solvent():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdb_path = os.path.join(tmpdir, "multi_bulk.pdb")
        mtz_path = os.path.join(tmpdir, "multi_bulk.mtz")

        # Create a dummy structure with 2 models
        st = gemmi.Structure()
        st.cell = gemmi.UnitCell(10.0, 10.0, 10.0, 90.0, 90.0, 90.0)
        st.spacegroup_hm = "P 1"
        for i in range(2):
            model = gemmi.Model(str(i + 1))  # type: ignore[arg-type]
            chain = gemmi.Chain("A")
            res = gemmi.Residue()
            res.name = "ALA"
            atom = gemmi.Atom()
            atom.name = "CA"
            atom.element = gemmi.Element("C")
            atom.pos = gemmi.Position(5.0 + i, 5.0, 5.0)
            atom.occ = 1.0
            atom.b_iso = 20.0
            res.add_atom(atom)
            chain.add_residue(res)
            model.add_chain(chain)
            st.add_model(model)
        st.write_pdb(pdb_path)

        simulate_diffraction(pdb_path, mtz_path, d_min=3.0, use_bulk_solvent=True)

        assert os.path.exists(mtz_path)
        mtz = gemmi.read_mtz_file(mtz_path)
        assert len(mtz.columns) > 3
        assert mtz.spacegroup.hm == "P 1"
        assert len(mtz.columns) > 3  # H, K, L and some data columns like FC, PHIC


def test_simulate_diffraction_without_cell():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdb_path = os.path.join(tmpdir, "nocell.pdb")
        mtz_path = os.path.join(tmpdir, "nocell.mtz")

        create_cell_less_pdb(pdb_path)

        simulate_diffraction(pdb_path, mtz_path, d_min=3.0, margin=5.0)

        assert os.path.exists(mtz_path)
        mtz = gemmi.read_mtz_file(mtz_path)

        # A single atom bounding box is point-like, margin=5 -> dims = 10x10x10
        assert abs(mtz.cell.a - 10.0) < 1e-4
        assert abs(mtz.cell.b - 10.0) < 1e-4
        assert abs(mtz.cell.c - 10.0) < 1e-4


def test_simulate_diffraction_with_invalid_anisou():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdb_path = os.path.join(tmpdir, "aniso.pdb")
        mtz_path = os.path.join(tmpdir, "aniso.mtz")

        # Create a dummy structure with ANISOU records
        st = gemmi.Structure()
        st.cell = gemmi.UnitCell(20, 20, 20, 90, 90, 90)
        st.spacegroup_hm = "P 1"

        model = gemmi.Model("1")  # type: ignore[arg-type]
        chain = gemmi.Chain("A")
        res = gemmi.Residue()
        res.name = "ALA"
        res.seqid = gemmi.SeqId("1")

        atom = gemmi.Atom()
        atom.name = "CA"
        atom.element = gemmi.Element("C")
        atom.pos = gemmi.Position(10.0, 10.0, 10.0)
        atom.b_iso = 20.0

        # Add a bizarre/invalid anisotropic B-factor tensor
        atom.aniso = gemmi.SMat33f(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

        res.add_atom(atom)
        chain.add_residue(res)
        model.add_chain(chain)
        st.add_model(model)
        st.write_pdb(pdb_path)

        # Ensure simulate_diffraction runs successfully and produces valid numbers
        simulate_diffraction(pdb_path, mtz_path, d_min=3.0)

        import numpy as np

        assert os.path.exists(mtz_path)
        mtz = gemmi.read_mtz_file(mtz_path)

        # Verify that the structure factors FC do not contain NaNs
        fc_array = np.array(mtz.column_with_label("FC"))
        assert not np.isnan(fc_array).any()
