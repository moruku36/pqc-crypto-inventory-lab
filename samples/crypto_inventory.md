# PQC Crypto Inventory Report

## Executive Summary

Scanned files: 2; findings: 5.
QUANTUM_VULNERABLE: 2; SAFE: 2; UNKNOWN: 1.
Counts describe static findings, not distinct deployed assets or a security verdict.
Partial result: NO.

## Cryptographic Inventory

| Evidence | Kind | Algorithm | Status | Confidence |
|---|---|---|---|---|
| crypto&&#35;95;example.py:13 | python&&#35;95;api&&#35;95;call | RSA | QUANTUM&&#35;95;VULNERABLE | MEDIUM |
| crypto&&#35;95;example.py:9 | python&&#35;95;api&&#35;95;call | SHA-1 | UNKNOWN | MEDIUM |
| security.json | configuration | AES-256 | SAFE | MEDIUM |
| security.json | configuration | X25519 | QUANTUM&&#35;95;VULNERABLE | MEDIUM |
| security.json | configuration | SHA-384 | SAFE | MEDIUM |

## Quantum Vulnerability

SAFE is a narrow algorithm-level label. It does not mean the system is quantum-safe.
- crypto&&#35;95;example.py: Classical factoring/discrete-log cryptography is vulnerable to Shor&&#35;x27;s algorithm on a sufficiently capable quantum computer.
- crypto&&#35;95;example.py: SHA-1 has classical collision weaknesses; replace collision-sensitive uses independently of the quantum assessment.
- security.json: No known efficient quantum break of this algorithm at the stated parameters. SAFE is an algorithm-level screening label; it does not validate implementation, mode, protocol, or key management.
- security.json: Classical factoring/discrete-log cryptography is vulnerable to Shor&&#35;x27;s algorithm on a sufficiently capable quantum computer.
- security.json: No known efficient quantum break of this algorithm at the stated parameters. SAFE is an algorithm-level screening label; it does not validate implementation, mode, protocol, or key management.

## Migration Priority

Triage categories are lab heuristics, not NIST deadlines. Confirm data retention, exposure, asset owner and protocol support before prioritizing production changes.
Long-lived confidentiality warrants harvest-now-decrypt-later review.
- crypto&&#35;95;example.py / RSA: P2: establish use, data lifetime and migration dependencies
- crypto&&#35;95;example.py / SHA-1: P1: review classical collision-sensitive use now
- security.json / AES-256: P3: confirm parameters, implementation and operational controls
- security.json / X25519: P2: establish use, data lifetime and migration dependencies
- security.json / SHA-384: P3: confirm parameters, implementation and operational controls

## Recommended PQC Replacement

- AES-256: Review parameters, mode and purpose; no automatic replacement by a PQC primitive.
- RSA: Confirm purpose first: key establishment may use ML-KEM or a supported hybrid; signatures may use ML-DSA or SLH-DSA. Not a drop-in replacement.
- SHA-1: Review SHA-256/384/512 for collision-sensitive uses; PQC KEMs do not replace hashes.
- SHA-384: Review parameters, mode and purpose; no automatic replacement by a PQC primitive.
- X25519: Consider ML-KEM or a protocol-supported hybrid for key establishment.

## Crypto Agility Assessment

Not scored in Phase 3. Inventory alone cannot establish operational agility.

## Findings

No read/parse exclusions were reported among selected files.

## Limitations

- Static evidence is not proof of runtime use or absence.
- Python AST calls and selected configuration keys only; other code languages/dependencies require review.
- Aliases may be rebound; API hits are medium-confidence evidence.
- Symlinks, generated/dependency directories and large files excluded.
- Scan a quiescent directory; concurrent directory replacement is unsupported.
- No source snippets; relative filenames themselves may be sensitive.
- No secret contents or code excerpts are included; filenames still require review.
- Report output is created exclusively and never overwrites an existing file.

## References

Reference status checked 2026-09-15.
- [FIPS 203 — ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- [FIPS 204 — ML-DSA](https://csrc.nist.gov/pubs/fips/204/final)
- [FIPS 205 — SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final)
- [SP 800-227 — KEM recommendations](https://csrc.nist.gov/pubs/sp/800/227/final)
- [IR 8547 — INITIAL PUBLIC DRAFT](https://csrc.nist.gov/pubs/ir/8547/ipd)
- [CSWP 39upd1 — Crypto Agility](https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final)
