"""Convert a UV File to JSON.

Takes a CSV file output by Gilson GX machines and converts it into a JSON file containing sample information alongwith intensities and time for three different UV wavelengths.
"""

from argparse import ArgumentParser
from . import convert_to_json_uv


if __name__ == "__main__":
    parser = ArgumentParser(description="Convert Gilson CSV to JSON file")
    parser.add_argument(
        "filenames",
        help="convert given filename(s) to json",
        nargs="+",
    )

    args = parser.parse_args()

    convert_to_json_uv.convert(args.filenames)
