from argparse import ArgumentParser
from convert_to_json_uv import convert


def main():
    parser = ArgumentParser(description="Convert Gilson CSV to JSON file")
    parser.add_argument(
        "filenames",
        help="convert given filename(s) to json",
        nargs="+",
    )

    args = parser.parse_args()
    convert(args.filenames)


if __name__ == "__main__":
    main()
