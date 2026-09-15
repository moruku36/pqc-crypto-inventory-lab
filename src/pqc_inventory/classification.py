"""Conservative algorithm-level quantum assessment, not a security certification."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Assessment:
    value: str
    status: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def assess(value: str) -> Assessment:
    name = value.upper().replace("_", "-")
    if any(x in name for x in ("RSA", "ECDSA", "ECDH", "ED25519", "ED448", "X25519",
                                "X448", "DSA", "DHE")) and not name.startswith(
                                    ("ML-DSA", "SLH-DSA")):
        return Assessment(value, "QUANTUM_VULNERABLE",
                          "Classical factoring/discrete-log cryptography is vulnerable to "
                          "Shor's algorithm on a sufficiently capable quantum computer.")
    if name in {"ML-KEM", "ML-DSA", "SLH-DSA", "AES-256", "SHA-384", "SHA-512"}:
        return Assessment(value, "SAFE", "No known efficient quantum break of this algorithm "
                          "at the stated parameters. SAFE is an algorithm-level screening label; "
                          "it does not validate implementation, mode, protocol, or key management.")
    if name == "SHA-1":
        return Assessment(value, "UNKNOWN", "SHA-1 has classical collision weaknesses; replace "
                          "collision-sensitive uses independently of the quantum assessment.")
    return Assessment(value, "UNKNOWN", "Insufficient evidence about parameters, usage, or "
                      "negotiated algorithms; no system-level security inference is made.")
