from pyfend.tools.hashprobe.utils.detector import detect_hash


def test_detect_hash_identifies_base64_text() -> None:
    results = detect_hash("aGVsbG8=")

    assert results[0]["type"] == "Base64 Encoded"
    assert results[0]["decoded_preview"] == "hello"
    assert results[0]["decoded_type"] == "printable-text"
    assert results[0]["confidence"] == 1.0


def test_detect_hash_identifies_ntlm_above_md5_for_uppercase_hex() -> None:
    results = detect_hash("8846F7EAEE8FB117AD06BDD830B7586C")

    assert results[0]["type"] == "NTLM"
    assert results[0]["confidence"] >= 1.0
    assert any(result["type"] == "MD5" for result in results)


def test_detect_hash_returns_empty_for_unknown_value() -> None:
    assert detect_hash("not-a-hash!") == []
