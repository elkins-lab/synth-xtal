import argparse
import sys
from .simulator import simulate_diffraction


def main():
    parser = argparse.ArgumentParser(
        description="Simulate X-ray crystallography diffraction data from atomic models."
    )
    parser.add_argument("input", type=str, help="Input PDB or mmCIF file.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output MTZ file path.")
    parser.add_argument(
        "-d",
        "--resolution",
        type=float,
        default=2.0,
        help="High resolution limit in Ångströms (default: 2.0).",
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=10.0,
        help="Margin in Ångströms for the unit cell bounding box if PDB lacks cell (default: 10.0).",
    )
    parser.add_argument(
        "--bulk-solvent",
        action="store_true",
        help="Enable flat bulk solvent modeling.",
    )
    parser.add_argument(
        "--k-sol",
        type=float,
        default=0.35,
        help="Bulk solvent scale factor (default: 0.35).",
    )
    parser.add_argument(
        "--b-sol",
        type=float,
        default=45.0,
        help="Bulk solvent B-factor (default: 45.0).",
    )

    args = parser.parse_args()

    try:
        simulate_diffraction(
            input_pdb=args.input,
            output_mtz=args.output,
            d_min=args.resolution,
            margin=args.margin,
            use_bulk_solvent=args.bulk_solvent,
            k_sol=args.k_sol,
            b_sol=args.b_sol,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
