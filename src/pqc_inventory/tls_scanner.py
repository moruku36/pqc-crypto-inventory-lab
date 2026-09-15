"""A single verified public TLS handshake; no probing or downgrade attempts."""

import re
import socket
import ssl
from typing import Any

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import (
    dh,
    dsa,
    ec,
    ed448,
    ed25519,
    rsa,
    x448,
    x25519,
)

from pqc_inventory.classification import assess


class ScanError(Exception):
    """Public error with a fixed, non-secret message."""


def public_key_info(key: Any) -> tuple[str, int | str]:
    if isinstance(key, rsa.RSAPublicKey):
        return "RSA", key.key_size
    if isinstance(key, ec.EllipticCurvePublicKey):
        return "ECC", key.key_size
    if isinstance(key, dsa.DSAPublicKey):
        return "DSA", key.key_size
    if isinstance(key, dh.DHPublicKey):
        return "DH", key.key_size
    for kind, name, size in ((ed25519.Ed25519PublicKey, "Ed25519", 256),
                             (ed448.Ed448PublicKey, "Ed448", 456),
                             (x25519.X25519PublicKey, "X25519", 256),
                             (x448.X448PublicKey, "X448", 448)):
        if isinstance(key, kind):
            return name, size
    return "UNKNOWN", "UNKNOWN"


def certificate_info(der: bytes) -> dict[str, Any]:
    cert = x509.load_der_x509_certificate(der)
    algorithm, size = public_key_info(cert.public_key())
    # EC key encoding alone does not prove signature versus agreement usage.
    key_assessment = assess("ECDH/ECDSA" if algorithm == "ECC" else algorithm).to_dict()
    key_assessment["value"] = algorithm
    signature = cert.signature_algorithm_oid.dotted_string
    known = {
        "1.2.840.113549.1.1.5": "RSA-SHA-1", "1.2.840.113549.1.1.11": "RSA-SHA-256",
        "1.2.840.113549.1.1.12": "RSA-SHA-384", "1.2.840.113549.1.1.13": "RSA-SHA-512",
        "1.2.840.113549.1.1.10": "RSA-PSS", "1.2.840.10045.4.3.2": "ECDSA-SHA-256",
        "1.2.840.10045.4.3.3": "ECDSA-SHA-384", "1.2.840.10045.4.3.4": "ECDSA-SHA-512",
        "1.3.101.112": "Ed25519", "1.3.101.113": "Ed448",
    }
    return {
        "public_key": key_assessment, "public_key_size_bits": size,
        "signature": assess(known.get(signature, "UNKNOWN")).to_dict(),
        "signature_oid": signature, "expiration": cert.not_valid_after_utc.isoformat(),
    }


def key_exchange(version: str, cipher: str) -> str:
    if version == "TLSv1.3":
        return "UNKNOWN"  # TLS 1.3 cipher suite does not identify the negotiated group.
    if cipher.startswith("ECDHE-"):
        return "ECDHE"
    if cipher.startswith("DHE-"):
        return "DHE"
    return "UNKNOWN"


def scan_tls(host: str, port: int = 443, timeout: float = 5.0) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z0-9.:-]{1,253}", host) or host.startswith("-"):
        raise ScanError("INVALID_HOST: specify a hostname or IP address, not a URL")
    if not 1 <= port <= 65535 or not 0 < timeout <= 60:
        raise ScanError("INVALID_OPTIONS: port 1..65535 and timeout (0,60] required")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with context.wrap_socket(raw, server_hostname=host) as connection:
                cipher_tuple = connection.cipher()
                cipher = cipher_tuple[0] if cipher_tuple else "UNKNOWN"
                version = connection.version() or "UNKNOWN"
                der = connection.getpeercert(binary_form=True)
        if not der:
            raise ScanError("CERTIFICATE_UNAVAILABLE")
        certificate = certificate_info(der)
    except ssl.SSLCertVerificationError:
        raise ScanError("CERTIFICATE_VERIFICATION_FAILED: trust, name, or validity") from None
    except (OSError, ssl.SSLError, ValueError):
        raise ScanError("TLS_CONNECTION_FAILED: DNS, network, timeout, or TLS error") from None
    encryption = "AES-256" if "AES_256" in cipher or "AES256" in cipher else "UNKNOWN"
    return {
        "schema_version": 1, "target": host, "port": port,
        "tls_version": assess(version).to_dict(), "cipher_suite": cipher,
        "symmetric_cipher": assess(encryption).to_dict(), "certificate": certificate,
        "key_exchange": assess(key_exchange(version, cipher)).to_dict(),
        "limitations": ["One handshake and leaf certificate only; not all server capabilities.",
                        "No CRL/OCSP check or complete chain inventory.",
                        "Negotiated group unavailable from Python ssl; TLS 1.3 KEX is UNKNOWN.",
                        "Socket timeout excludes platform DNS resolver delays."],
    }
