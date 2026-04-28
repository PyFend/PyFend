import base64
import math
import re
import string

from .hashes import HASH_SIGNATURES

# Pre-compile regex
HEX_PATTERN = re.compile(r"^[0-9a-fA-F]+$")
BASE64_STRICT_PATTERN = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")


def is_hex(s):
    return bool(HEX_PATTERN.fullmatch(s))


def is_base64_charset(s):
    if len(s) % 4 != 0:
        return False
    return bool(BASE64_STRICT_PATTERN.fullmatch(s))


def shannon_entropy(s):
    if not s:
        return 0.0
    from collections import Counter

    counts = Counter(s)
    entropy = 0.0
    length = len(s)
    for c in counts.values():
        p = c / length
        entropy -= p * math.log2(p)
    return entropy


def is_printable_ratio(data, threshold=0.90):
    if not data:
        return False
    printable = sum(
        chr(b) in string.printable and chr(b) not in "\x0b\x0c" for b in data
    )
    return printable / len(data) >= threshold


def detect_base64(value):
    if not is_base64_charset(value):
        return None

    looks_like_hex = is_hex(value)

    try:
        decoded = base64.b64decode(value, validate=True)
    except Exception:
        return None

    if not decoded:
        return None

    looks_like_text = is_printable_ratio(decoded)

    if looks_like_hex and not looks_like_text:
        return None

    result = {
        "type": "Base64 Encoded",
        "confidence": 1.0 if looks_like_text else 0.5,
        "decoded_preview": None,
        "decoded_type": "binary",
    }

    if looks_like_text:
        result["decoded_preview"] = decoded.decode(errors="replace")[:50]
        result["decoded_type"] = "printable-text"
    else:
        result["decoded_preview"] = decoded[:10].hex() + "..."

    return result


def detect_hash(hash_value):
    hash_value = hash_value.strip()
    results = []

    length = len(hash_value)
    base64_result = detect_base64(hash_value)
    if base64_result:
        results.append(base64_result)

    for sig in HASH_SIGNATURES:
        score = 0.0

        if "prefix" in sig:
            if any(hash_value.startswith(p) for p in sig["prefix"]):
                score += 0.8  # Naikkan bobot prefix
            else:
                continue
        if sig["name"] == "MD5" and hash_value.isupper():
            score -= 0.3

        if sig["name"] == "NTLM":
            if hash_value.isupper():
                score += 0.6
            else:
                score -= 0.4

        length_match = sig.get("length") == length
        if length_match:
            score += 0.5

        charset = sig.get("charset")
        if (
            charset == "hex"
            and is_hex(hash_value)
            or charset == "base64"
            and is_base64_charset(hash_value)
        ):
            score += 0.3

        if length_match and charset == "hex" and is_hex(hash_value):
            if sig["name"] not in ("MD5", "NTLM"):
                score += 0.2

        if score > 0.4:
            results.append(
                {"type": sig["name"], "confidence": round(min(score, 1.0), 2)}
            )

    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results
