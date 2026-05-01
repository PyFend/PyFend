from datetime import datetime
from pathlib import Path

from pyfend.tools.hashprobe.types import Info

BASE_DIR = Path.cwd()
ADDITIONAL_FILE = BASE_DIR / "wordlists" / "additional.txt"


def create_smart_wordlist_data(
    name: str = "", nickname: str = "", birth: datetime = "", extra: str = ""
) -> list[str]:
    """
    Core logic to generate a list of potential passwords based on personal info.
    Returns a list of unique strings.
    """
    base_words = []
    modifiers = []

    # Process Name
    if name:
        parts = name.replace(",", " ").split()
        for p in parts:
            base_words.append(p)
            base_words.append(p.lower())
        if len(parts) > 1:
            base_words.append("".join(parts))
            base_words.append("".join(parts).lower())

    # Process Nickname
    if nickname:
        parts = nickname.replace(",", " ").split()
        for p in parts:
            base_words.append(p)
            base_words.append(p.lower())
        if len(parts) > 1:
            base_words.append("".join(parts))
            base_words.append("".join(parts).lower())

    # Process Extra Keywords
    if extra:
        for e in extra.replace(",", " ").split():
            base_words.append(e)
            base_words.append(e.lower())

    base_words = list(set(base_words))
    modifiers = list(set(modifiers))

    final = []
    # 1. Base words only
    final.extend(base_words)

    # 2. Permutations: word + modifier and modifier + word
    for w in base_words:
        for m in modifiers:
            final.append(w + m)
            final.append(m + w)

    # 3. Common additions
    common_suffixes = ["123", "!", "@", "2024", "2025"]
    for w in base_words:
        for s in common_suffixes:
            final.append(w + s)

    return list(set(final))


def generate_smart_wordlist(info: Info) -> None:
    """CLI version that uses input()"""
    print("[*] Smart wordlist generator")

    final_list = create_smart_wordlist_data(**info)

    # Write to file for CLI usage
    path = Path(ADDITIONAL_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)

    with Path.open(path, "w", encoding="utf-8") as f:
        for w in final_list:
            f.write(w + "\n")

    print(f"[+] Additional wordlist generated: {path}")
    print(f"[+] Total words: {len(final_list)}")
