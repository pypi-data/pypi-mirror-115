from argparse import ArgumentParser
from . import convert_to_json_uv

"""Convert a UV File to JSON."""


if __name__ == "__main__":
    parser = ArgumentParser(description="Convert Gilson CSV to JSON file")
    parser.add_argument(
        "filenames",
        help="convert given filename(s) to json",
        nargs="+",
    )

    args = parser.parse_args()

    convert_to_json_uv.convert(args.filenames)
