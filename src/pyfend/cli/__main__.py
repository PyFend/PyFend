import argparse
import os
from datetime import datetime

from questionary import prompt

from pyfend.tools.hashprobe.hash_probe import crack


def parse_args():
    parser = argparse.ArgumentParser(
        prog="hashprobe",
        description="Hash analysis and dictionary-based testing tool",
    )

    parser.add_argument(
        "-H",
        "--hash",
        dest="hash_value",
        required=True,
        help="Hash value to analyze",
    )

    parser.add_argument(
        "-b",
        "--bruteforce",
        default=None,
        metavar="WORDLIST",
        help="Enable dictionary-based testing (default: rockyou.txt)",
    )

    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Interactive info input to generate additional wordlist",
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=os.cpu_count(),
        help="Number of threads for dictionary testing",
    )

    parser.add_argument("--limit", type=int, help="Limit number of attempts")

    return parser.parse_args()


def _valid_date(birth_str: str):
    try:
        datetime.strptime(birth_str, "%Y-%m-%d")
        return True
    except ValueError:
        return "Invalid date format, use YYYY-MM-DD"


def main():
    args = parse_args()
    info_input = None

    if args.info:
        # Info Input
        info_input = prompt(
            [
                {
                    "type": "text",
                    "name": "name",
                    "message": "Name:",
                },
                {
                    "type": "text",
                    "name": "nickname",
                    "message": "Nickname:",
                },
                {
                    "type": "text",
                    "name": "birth",
                    "message": "Birth date (YYYY-MM-DD):",
                    "validate": lambda x: True if x == "" else _valid_date(x),
                    "filter": lambda x: (
                        datetime.strptime(x, "%Y-%m-%d") if x else None
                    ),
                },
                {
                    "type": "text",
                    "name": "extra",
                    "message": "Extra info:",
                },
            ]
        )

    crack(
        hash_value=args.hash_value,
        bruteforce=args.bruteforce,
        info=info_input,
        threads=args.threads,
        limit=args.limit,
    )
