import concurrent.futures
import gzip
from pathlib import Path

from .hashes import HASH_FUNCTIONS


class HashProbeCracker:
    """
    Class that contain method to crack tje hash
    """

    @staticmethod
    def __check_words(words, hash_func, target_hash):
        for word in words:
            if hash_func(word) == target_hash:
                return word
        return None

    @staticmethod
    def crack_hash(
        target_hash: str,
        hash_type: str,
        wordlist_path: str,
        limit: int | None = None,
        additional_file: str | None = None,
        additional_words: list[str] | None = None,
        threads: int = 1,
    ):
        if hash_type not in HASH_FUNCTIONS:
            raise ValueError(f"Unsupported hash type: {hash_type}")

        hash_func = HASH_FUNCTIONS[hash_type]
        attempts = 0

        if hash_type == "NTLM":
            target_hash = target_hash.upper()

        wordlist = (
            Path(wordlist_path).expanduser().resolve()
            if wordlist_path
            else None
        )
        additional = (
            Path(additional_file).expanduser().resolve()
            if additional_file
            else None
        )

        # 1. TRY ADDITIONAL WORDS (Direct list) FIRST
        if additional_words:
            found = HashProbeCracker.__check_words(
                additional_words, hash_func, target_hash
            )
            if found:
                return {
                    "found": True,
                    "password": found,
                    "attempts": len(additional_words),
                    "source": "smart-generator",
                }
            attempts += len(additional_words)

        # 2. TRY ADDITIONAL FILE
        if additional and additional.exists():
            with Path.open(additional, encoding="utf-8", errors="ignore") as f:
                words = [line.strip() for line in f if line.strip()]
                found = HashProbeCracker.__check_words(
                    words, hash_func, target_hash
                )
                if found:
                    return {
                        "found": True,
                        "password": found,
                        "attempts": len(words),
                        "source": "additional",
                    }
                attempts += len(words)

        # 2. MAIN WORDLIST
        if wordlist:
            if not wordlist.exists():
                raise FileNotFoundError(f"Wordlist not found: {wordlist}")

            # Choose open function based on extension
            is_gz = wordlist.suffix == ".gz"
            open_func = gzip.open if is_gz else open
            mode = "rt" if is_gz else "r"

            with open_func(
                wordlist, mode, encoding="latin-1", errors="ignore"
            ) as f:
                if threads <= 1:
                    # Sequential mode
                    for line in f:
                        word = line.strip()
                        if not word:
                            continue

                        attempts += 1
                        if limit and attempts > limit:
                            break

                        if hash_func(word) == target_hash:
                            return {
                                "found": True,
                                "password": word,
                                "attempts": attempts,
                                "source": "wordlist",
                            }
                else:
                    # Multithreaded mode
                    chunk_size = 50000
                    with concurrent.futures.ThreadPoolExecutor(
                        max_workers=threads
                    ) as executor:
                        while True:
                            lines = []
                            for _ in range(chunk_size):
                                line = f.readline()
                                if not line:
                                    break
                                w = line.strip()
                                if w:
                                    lines.append(w)

                            if not lines:
                                break

                            # Split lines into sub-chunks for threads
                            sub_chunk_size = max(1, len(lines) // threads)
                            sub_chunks = [
                                lines[i : i + sub_chunk_size]
                                for i in range(0, len(lines), sub_chunk_size)
                            ]

                            futures = [
                                executor.submit(
                                    HashProbeCracker.__check_words,
                                    sc,
                                    hash_func,
                                    target_hash,
                                )
                                for sc in sub_chunks
                            ]
                            for future in concurrent.futures.as_completed(
                                futures
                            ):
                                found = future.result()
                                if found:
                                    return {
                                        "found": True,
                                        "password": found,
                                        "attempts": attempts
                                        + lines.index(found)
                                        + 1,
                                        "source": "wordlist",
                                    }

                            attempts += len(lines)
                            if limit and attempts >= limit:
                                break

        return {"found": False, "attempts": attempts}
