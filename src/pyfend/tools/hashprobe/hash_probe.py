import os
from pathlib import Path

from .types import Info
from .utils.cracker import crack_hash
from .utils.detector import detect_hash
from .utils.word_list import ADDITIONAL_FILE, generate_smart_wordlist

# Path relative to this file
BASE_DIR = Path(__file__).parent
ROCKYOU_GZ = BASE_DIR / "wordlists" / "rockyou.txt.gz"
ROCKYOU_TXT = BASE_DIR / "wordlists" / "rockyou.txt"

# Default to .gz if it exists, otherwise .txt
DEFAULT_ROCKYOU = ROCKYOU_GZ if ROCKYOU_GZ.exists() else ROCKYOU_TXT


def crack(
    hash_value: str,
    bruteforce: str | None = None,
    info: Info | None = None,
    threads: int = os.cpu_count(),
    limit: int = 1,
):
    results = detect_hash(hash_value)

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
    if info:
        generate_smart_wordlist(info)  # overwrite additional.txt
        additional_file = ADDITIONAL_FILE

    # Start dictionary attack if -b
    if bruteforce and Path(bruteforce).exists():
        print(f"\n[*] Starting dictionary attack using {threads} threads...")

        for r in results:
            hash_type = r["type"]
            try:
                result = crack_hash(
                    target_hash=hash_value,
                    hash_type=hash_type,
                    wordlist_path=bruteforce,
                    limit=limit,
                    additional_file=additional_file,
                    threads=threads,
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
