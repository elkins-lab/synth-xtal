import os
import tempfile
import pytest
import gemmi
from unittest.mock import patch
from synth_xtal.cli import main


def create_dummy_pdb(filepath: str):
    st = gemmi.Structure()
    st.cell = gemmi.UnitCell(10.0, 10.0, 10.0, 90.0, 90.0, 90.0)
    st.spacegroup_hm = "P 1"
    model = gemmi.Model("1")
    chain = gemmi.Chain("A")
    res = gemmi.Residue()
    res.name = "ALA"
    atom = gemmi.Atom()
    atom.name = "CA"
    atom.element = gemmi.Element("C")
    atom.pos = gemmi.Position(5.0, 5.0, 5.0)
    atom.occ = 1.0
    atom.b_iso = 20.0
    res.add_atom(atom)
    chain.add_residue(res)
    model.add_chain(chain)
    st.add_model(model)
    st.write_pdb(filepath)


def test_cli_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdb_path = os.path.join(tmpdir, "test.pdb")
        mtz_path = os.path.join(tmpdir, "test.mtz")

        create_dummy_pdb(pdb_path)

        test_args = [
            "synth-xtal",
            pdb_path,
            "-o",
            mtz_path,
            "--resolution",
            "3.0",
            "--margin",
            "5.0",
        ]

        with patch("sys.argv", test_args):
            main()

        assert os.path.exists(mtz_path)


def test_cli_failure(capsys):
    test_args = ["synth-xtal", "nonexistent.pdb", "-o", "out.mtz"]

    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 1

    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_cli_exception(capsys):
    test_args = ["synth-xtal", "bad.pdb", "-o", "out.mtz"]

    # Mock simulate_diffraction to raise a generic Exception
    with patch("synth_xtal.cli.simulate_diffraction", side_effect=Exception("Mocked failure")):
        with patch("sys.argv", test_args):
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 1

    captured = capsys.readouterr()
    assert "Error: Mocked failure" in captured.err
