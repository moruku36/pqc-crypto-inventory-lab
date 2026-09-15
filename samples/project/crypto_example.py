"""Synthetic inventory fixture; this module is not executed by the scanner."""

import hashlib

from cryptography.hazmat.primitives.asymmetric import rsa


def legacy_digest(data: bytes) -> bytes:
    return hashlib.sha1(data).digest()


def make_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)
