import hashlib

from Crypto.Hash import MD4

HASH_SIGNATURES = [
    {
        "name": "MD5",
        "length": 32,
        "charset": "hex",
    },
    {
        "name": "SHA1",
        "length": 40,
        "charset": "hex",
    },
    {
        "name": "SHA256",
        "length": 64,
        "charset": "hex",
    },
    {
        "name": "SHA512",
        "length": 128,
        "charset": "hex",
    },
    {
        "name": "SHA224",
        "length": 56,
        "charset": "hex",
    },
    {
        "name": "SHA384",
        "length": 96,
        "charset": "hex",
    },
    {
        "name": "SHA3-224",
        "length": 56,
        "charset": "hex",
    },
    {
        "name": "SHA3-256",
        "length": 64,
        "charset": "hex",
    },
    {
        "name": "SHA3-384",
        "length": 96,
        "charset": "hex",
    },
    {
        "name": "SHA3-512",
        "length": 128,
        "charset": "hex",
    },
    {
        "name": "BLAKE2b",
        "length": 128,
        "charset": "hex",
    },
    {
        "name": "BLAKE2s",
        "length": 64,
        "charset": "hex",
    },
    {"name": "NTLM", "length": 32, "charset": "hex", "uppercase": True},
]


class HashProbeHashes:
    """
    Class with list of hashes used in HashProbe Tool
    """

    @staticmethod
    def md5(s):
        return hashlib.md5(s.encode()).hexdigest()

    @staticmethod
    def sha1(s):
        return hashlib.sha1(s.encode()).hexdigest()

    @staticmethod
    def sha224(s):
        return hashlib.sha224(s.encode()).hexdigest()

    @staticmethod
    def sha256(s):
        return hashlib.sha256(s.encode()).hexdigest()

    @staticmethod
    def sha384(s):
        return hashlib.sha384(s.encode()).hexdigest()

    @staticmethod
    def sha512(s):
        return hashlib.sha512(s.encode()).hexdigest()

    @staticmethod
    def sha3_224(s):
        return hashlib.sha3_224(s.encode()).hexdigest()

    @staticmethod
    def sha3_256(s):
        return hashlib.sha3_256(s.encode()).hexdigest()

    @staticmethod
    def sha3_384(s):
        return hashlib.sha3_384(s.encode()).hexdigest()

    @staticmethod
    def sha3_512(s):
        return hashlib.sha3_512(s.encode()).hexdigest()

    @staticmethod
    def blake2b(s):
        return hashlib.blake2b(s.encode()).hexdigest()

    @staticmethod
    def blake2s(s):
        return hashlib.blake2s(s.encode()).hexdigest()

    @staticmethod
    def ntlm(s):
        return MD4.new(s.encode("utf-16le")).hexdigest().upper()


HASH_FUNCTIONS = {
    "MD5": HashProbeHashes.md5,
    "SHA1": HashProbeHashes.sha1,
    "SHA224": HashProbeHashes.sha224,
    "SHA256": HashProbeHashes.sha256,
    "SHA384": HashProbeHashes.sha384,
    "SHA512": HashProbeHashes.sha512,
    "SHA3-224": HashProbeHashes.sha3_224,
    "SHA3-256": HashProbeHashes.sha3_256,
    "SHA3-384": HashProbeHashes.sha3_384,
    "SHA3-512": HashProbeHashes.sha3_512,
    "BLAKE2b": HashProbeHashes.blake2b,
    "BLAKE2s": HashProbeHashes.blake2s,
    "NTLM": HashProbeHashes.ntlm,
}
