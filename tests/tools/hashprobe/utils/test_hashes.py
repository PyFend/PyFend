import hashlib

from pyfend.tools.hashprobe.utils.hashes import HASH_FUNCTIONS, ntlm


def test_hash_functions_return_expected_digests() -> None:
    sample = "password"

    expected = {
        "MD5": hashlib.md5(sample.encode()).hexdigest(),
        "SHA1": hashlib.sha1(sample.encode()).hexdigest(),
        "SHA224": hashlib.sha224(sample.encode()).hexdigest(),
        "SHA256": hashlib.sha256(sample.encode()).hexdigest(),
        "SHA384": hashlib.sha384(sample.encode()).hexdigest(),
        "SHA512": hashlib.sha512(sample.encode()).hexdigest(),
        "SHA3-224": hashlib.sha3_224(sample.encode()).hexdigest(),
        "SHA3-256": hashlib.sha3_256(sample.encode()).hexdigest(),
        "SHA3-384": hashlib.sha3_384(sample.encode()).hexdigest(),
        "SHA3-512": hashlib.sha3_512(sample.encode()).hexdigest(),
        "BLAKE2b": hashlib.blake2b(sample.encode()).hexdigest(),
        "BLAKE2s": hashlib.blake2s(sample.encode()).hexdigest(),
        "NTLM": ntlm(sample),
    }

    for name, func in HASH_FUNCTIONS.items():
        assert func(sample) == expected[name]


def test_hash_functions_mapping_exposes_supported_hashes() -> None:
    assert set(HASH_FUNCTIONS) == {
        "MD5",
        "SHA1",
        "SHA224",
        "SHA256",
        "SHA384",
        "SHA512",
        "SHA3-224",
        "SHA3-256",
        "SHA3-384",
        "SHA3-512",
        "BLAKE2b",
        "BLAKE2s",
        "NTLM",
    }
