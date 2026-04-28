import argparse
import os
from pathlib import Path

from pyfend.core.cracker import crack_hash
from pyfend.core.detector import detect_hash
from pyfend.core.wordlist import ADDITIONAL_FILE, generate_smart_wordlist

# Path relative to this file
BASE_DIR = Path(__file__).parent
ROCKYOU_GZ = BASE_DIR / "wordlists" / "rockyou.txt.gz"
ROCKYOU_TXT = BASE_DIR / "wordlists" / "rockyou.txt"

# Default to .gz if it exists, otherwise .txt
DEFAULT_ROCKYOU = ROCKYOU_GZ if ROCKYOU_GZ.exists() else ROCKYOU_TXT


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
        nargs="?",
        const=str(DEFAULT_ROCKYOU),
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


def main():
    args = parse_args()
    print("HashProbe v0.1 Analysis tools")

    results = detect_hash(args.hash_value)

    print("[+] Possible hash types:")
    for r in results:
        print(f"  - {r['type']} (confidence: {r['confidence']})")

        if r["type"] == "Base64 Encoded":
            if r.get("decoded_preview"):
                print(
                    f"     ↳ decoded ({r['decoded_type']}): {r['decoded_preview']}"
                )
            else:
                print("      ↳ decoded: binary / non-printable")

    additional_file = None

    # Generate smart wordlist if -i
    if args.info:
        generate_smart_wordlist()  # overwrite additional.txt
        additional_file = ADDITIONAL_FILE

    # Start dictionary attack if -b
    if args.bruteforce:
        print(
            f"\n[*] Starting dictionary attack using {args.threads} threads..."
        )

        for r in results:
            hash_type = r["type"]
            try:
                result = crack_hash(
                    target_hash=args.hash_value,
                    hash_type=hash_type,
                    wordlist_path=args.bruteforce,
                    limit=args.limit,
                    additional_file=additional_file,
                    threads=args.threads,
                )
            except ValueError:
                continue

            if result["found"]:
                print(f"[+] PASSWORD FOUND! ({hash_type})")
                print(f"    password : {result['password']}")
                print(f"    attempts : ~{result['attempts']}")
                print(f"    source   : {result.get('source')}")
                return

        print("[-] Password not found")
