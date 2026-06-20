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

    args = parser.parse_args()

    try:
        simulate_diffraction(
            input_pdb=args.input, output_mtz=args.output, d_min=args.resolution, margin=args.margin
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
