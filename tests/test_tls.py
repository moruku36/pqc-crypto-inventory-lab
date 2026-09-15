import ssl
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from pqc_inventory.classification import assess
from pqc_inventory.cli import main
from pqc_inventory.tls_scanner import ScanError, certificate_info, key_exchange, scan_tls


def test_certificate() -> None:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "fixture.invalid")])
    now = datetime.now(UTC)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
            .public_key(key.public_key()).serial_number(1).not_valid_before(now)
            .not_valid_after(now + timedelta(days=1)).sign(key, hashes.SHA256()))
    result = certificate_info(cert.public_bytes(serialization.Encoding.DER))
    assert result["public_key_size_bits"] == 2048
    assert result["public_key"]["status"] == "QUANTUM_VULNERABLE"
    assert result["signature"]["value"] == "RSA-SHA-256"
    assert "+00:00" in result["expiration"]


def test_no_tls13_group_guess() -> None:
    assert key_exchange("TLSv1.3", "TLS_AES_256_GCM_SHA384") == "UNKNOWN"
    assert key_exchange("TLSv1.2", "ECDHE-RSA-AES256-GCM-SHA384") == "ECDHE"
    assert key_exchange("TLSv1.2", "AES256-GCM-SHA384") == "UNKNOWN"


@pytest.mark.parametrize("host,port,timeout", [("https://github.com", 443, 5),
                                              ("github.com", 0, 5),
                                              ("github.com", 443, 0),
                                              ("github.com", 443, float("nan"))])
def test_invalid_target(host: str, port: int, timeout: float) -> None:
    with pytest.raises(ScanError):
        scan_tls(host, port, timeout)


def test_cli_failure_is_structured(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["tls", "https://invalid"]) == 1
    assert '"event": "scan_failed"' in capsys.readouterr().err


@pytest.mark.parametrize("name,status", [("RSA", "QUANTUM_VULNERABLE"),
                                        ("X25519", "QUANTUM_VULNERABLE"),
                                        ("ML-DSA", "SAFE"), ("AES-256", "SAFE"),
                                        ("AES", "UNKNOWN"), ("SHA-1", "UNKNOWN")])
def test_quantum_assessment(name: str, status: str) -> None:
    assert assess(name).status == status


@pytest.mark.parametrize("error,code", [
    (ssl.SSLCertVerificationError("SECRET_CANARY"), "CERTIFICATE_VERIFICATION_FAILED"),
    (TimeoutError("SECRET_CANARY"), "TLS_CONNECTION_FAILED"),
])
def test_tls_errors_are_sanitized(error: OSError, code: str) -> None:
    with patch("pqc_inventory.tls_scanner.socket.create_connection", side_effect=error):
        with pytest.raises(ScanError) as failure:
            scan_tls("example.com")
    assert code in str(failure.value)
    assert "SECRET_CANARY" not in str(failure.value)
