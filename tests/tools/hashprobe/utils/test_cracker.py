import gzip

import pytest

from pyfend.tools.hashprobe.utils.cracker import crack_hash
from pyfend.tools.hashprobe.utils.hashes import md5, ntlm


def test_crack_hash_finds_match_in_additional_words_before_wordlist(
    tmp_path,
) -> None:
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    result = crack_hash(
        target_hash=md5("secret"),
        hash_type="MD5",
        wordlist_path=str(wordlist),
        additional_words=["guest", "secret", "admin"],
    )

    assert result == {
        "found": True,
        "password": "secret",
        "attempts": 3,
        "source": "smart-generator",
    }


def test_crack_hash_finds_match_in_additional_file(tmp_path) -> None:
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
    additional = tmp_path / "additional.txt"
    additional.write_text("guest\nsecret\n", encoding="utf-8")

    result = crack_hash(
        target_hash=md5("secret"),
        hash_type="MD5",
        wordlist_path=str(wordlist),
        additional_file=str(additional),
    )

    assert result == {
        "found": True,
        "password": "secret",
        "attempts": 2,
        "source": "additional",
    }


def test_crack_hash_supports_gzipped_wordlists_and_limit(tmp_path) -> None:
    wordlist = tmp_path / "words.txt.gz"
    with gzip.open(wordlist, "wt", encoding="latin-1") as handle:
        handle.write("alpha\nbeta\nsecret\n")

    found = crack_hash(
        target_hash=md5("secret"),
        hash_type="MD5",
        wordlist_path=str(wordlist),
        threads=2,
    )
    not_found = crack_hash(
        target_hash=md5("secret"),
        hash_type="MD5",
        wordlist_path=str(wordlist),
        limit=2,
    )

    assert found["found"] is True
    assert found["password"] == "secret"
    assert found["source"] == "wordlist"
    assert not_found == {"found": False, "attempts": 3}


def test_crack_hash_normalizes_ntlm_target_hash(tmp_path) -> None:
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("password\n", encoding="utf-8")

    result = crack_hash(
        target_hash=ntlm("password").lower(),
        hash_type="NTLM",
        wordlist_path=str(wordlist),
    )

    assert result["found"] is True
    assert result["password"] == "password"


def test_crack_hash_rejects_unsupported_hash_type(tmp_path) -> None:
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("password\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported hash type"):
        crack_hash(
            target_hash="abc",
            hash_type="UNKNOWN",
            wordlist_path=str(wordlist),
        )


def test_crack_hash_requires_existing_wordlist(tmp_path) -> None:
    missing = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="Wordlist not found"):
        crack_hash(
            target_hash=md5("secret"),
            hash_type="MD5",
            wordlist_path=str(missing),
        )
