import shutil
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pyfend.hash_probe.hash_probe as hash_probe_module
import pytest

ROOT_DIR = Path(__file__).resolve().parents[3]
TEMP_DIR = ROOT_DIR / ".tmp-test-hash-probe"


@pytest.fixture
def workspace_tmp_path():
    TEMP_DIR.mkdir(exist_ok=True)
    path = TEMP_DIR / uuid4().hex
    path.mkdir()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
        with suppress(OSError):
            TEMP_DIR.rmdir()


def test_crack_reports_detected_hashes_without_dictionary_attack(
    monkeypatch, capsys
) -> None:
    crack_calls = []

    monkeypatch.setattr(
        hash_probe_module,
        "detect_hash",
        lambda _: [
            {
                "type": "Base64 Encoded",
                "confidence": 1.0,
                "decoded_preview": "hello",
                "decoded_type": "printable-text",
            },
            {
                "type": "MD5",
                "confidence": 0.8,
            },
        ],
    )

    def fake_crack_hash(**kwargs):
        crack_calls.append(kwargs)
        return {"found": False, "attempts": 0}

    monkeypatch.setattr(hash_probe_module, "crack_hash", fake_crack_hash)

    hash_probe_module.crack("aGVsbG8=")

    output = capsys.readouterr().out

    assert "[+] Possible hash types:" in output
    assert "Base64 Encoded (confidence: 1.0)" in output
    assert "MD5 (confidence: 0.8)" in output
    assert "decoded (printable-text): hello" in output
    assert "[*] Starting dictionary attack" not in output
    assert crack_calls == []


def test_crack_generates_wordlist_and_passes_it_to_crack_hash(
    monkeypatch, workspace_tmp_path, capsys
) -> None:
    wordlist = workspace_tmp_path / "words.txt"
    wordlist.write_text("secret\n", encoding="utf-8")
    additional_file = workspace_tmp_path / "additional.txt"
    info = {
        "name": "John Doe",
        "nickname": "JD",
        "birth": datetime(2000, 1, 2),
        "extra": "admin",
    }
    generated = []
    crack_calls = []

    monkeypatch.setattr(
        hash_probe_module,
        "detect_hash",
        lambda _: [{"type": "MD5", "confidence": 0.8}],
    )
    monkeypatch.setattr(hash_probe_module, "ADDITIONAL_FILE", additional_file)

    def fake_generate_smart_wordlist(data) -> None:
        generated.append(data)

    def fake_crack_hash(**kwargs):
        crack_calls.append(kwargs)
        return {
            "found": True,
            "password": "secret",
            "attempts": 2,
            "source": "additional",
        }

    monkeypatch.setattr(
        hash_probe_module,
        "generate_smart_wordlist",
        fake_generate_smart_wordlist,
    )
    monkeypatch.setattr(hash_probe_module, "crack_hash", fake_crack_hash)

    hash_probe_module.crack(
        "5ebe2294ecd0e0f08eab7690d2a6ee69",
        bruteforce=str(wordlist),
        info=info,
        threads=4,
        limit=7,
    )

    output = capsys.readouterr().out

    assert generated == [info]
    assert crack_calls == [
        {
            "target_hash": "5ebe2294ecd0e0f08eab7690d2a6ee69",
            "hash_type": "MD5",
            "wordlist_path": str(wordlist),
            "limit": 7,
            "additional_file": additional_file,
            "threads": 4,
        }
    ]
    assert "[*] Starting dictionary attack using 4 threads..." in output
    assert "[+] PASSWORD FOUND! (MD5)" in output
    assert "password : secret" in output
    assert "source   : additional" in output


def test_crack_skips_unsupported_hash_types_and_reports_not_found(
    monkeypatch, workspace_tmp_path, capsys
) -> None:
    wordlist = workspace_tmp_path / "words.txt"
    wordlist.write_text("secret\n", encoding="utf-8")
    hash_types = []

    monkeypatch.setattr(
        hash_probe_module,
        "detect_hash",
        lambda _: [
            {"type": "UNKNOWN", "confidence": 0.9},
            {"type": "MD5", "confidence": 0.8},
        ],
    )

    def fake_crack_hash(**kwargs):
        hash_types.append(kwargs["hash_type"])
        if kwargs["hash_type"] == "UNKNOWN":
            raise ValueError("Unsupported hash type")
        return {"found": False, "attempts": 1}

    monkeypatch.setattr(hash_probe_module, "crack_hash", fake_crack_hash)

    hash_probe_module.crack(
        "5ebe2294ecd0e0f08eab7690d2a6ee69", bruteforce=str(wordlist)
    )

    output = capsys.readouterr().out

    assert hash_types == ["UNKNOWN", "MD5"]
    assert "[*] Starting dictionary attack using" in output
    assert "[-] Password not found" in output


def test_crack_stops_after_first_successful_match(
    monkeypatch, workspace_tmp_path, capsys
) -> None:
    wordlist = workspace_tmp_path / "words.txt"
    wordlist.write_text("secret\n", encoding="utf-8")
    hash_types = []

    monkeypatch.setattr(
        hash_probe_module,
        "detect_hash",
        lambda _: [
            {"type": "MD5", "confidence": 0.8},
            {"type": "SHA1", "confidence": 0.7},
        ],
    )

    def fake_crack_hash(**kwargs):
        hash_types.append(kwargs["hash_type"])
        return {
            "found": True,
            "password": "secret",
            "attempts": 1,
            "source": "wordlist",
        }

    monkeypatch.setattr(hash_probe_module, "crack_hash", fake_crack_hash)

    hash_probe_module.crack(
        "5ebe2294ecd0e0f08eab7690d2a6ee69", bruteforce=str(wordlist)
    )

    output = capsys.readouterr().out

    assert hash_types == ["MD5"]
    assert "[+] PASSWORD FOUND! (MD5)" in output
    assert "source   : wordlist" in output
