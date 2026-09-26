"""Synthetic signing call; this file is never run by the exercise."""

from cryptography.hazmat.primitives.asymmetric import rsa


def create_signing_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)
