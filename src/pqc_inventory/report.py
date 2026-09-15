"""Evidence-first Markdown reports with escaped filenames and no raw source."""

import html
from collections import Counter
from pathlib import Path
from typing import Any

from pqc_inventory.directory_scanner import scan_directory
from pqc_inventory.scoring import score_inventory
from pqc_inventory.tls_scanner import ScanError

REFERENCES = [
    ("FIPS 203 — ML-KEM", "https://csrc.nist.gov/pubs/fips/203/final"),
    ("FIPS 204 — ML-DSA", "https://csrc.nist.gov/pubs/fips/204/final"),
    ("FIPS 205 — SLH-DSA", "https://csrc.nist.gov/pubs/fips/205/final"),
    ("SP 800-227 — KEM recommendations", "https://csrc.nist.gov/pubs/sp/800/227/final"),
    ("IR 8547 — INITIAL PUBLIC DRAFT", "https://csrc.nist.gov/pubs/ir/8547/ipd"),
    ("CSWP 39upd1 — Crypto Agility", "https://csrc.nist.gov/pubs/cswp/39/upd1/"
     "considerations-for-achieving-crypto-agility/final"),
]


def cell(value: object) -> str:
    text = html.escape(str(value), quote=True)
    for character in ("\\", "|", "`", "[", "]", "*", "_", "!", "#"):
        text = text.replace(character, f"&#{ord(character)};")
    return "".join(c if ord(c) >= 32 and ord(c) != 127 else " " for c in text)


def priority(item: dict[str, Any]) -> str:
    if item["value"] == "SHA-1":
        return "P1: review classical collision-sensitive use now"
    if item["kind"] in {"private_key_present", "possible_private_key_file"}:
        return "P1: review private-key storage and access; exposure is not established"
    if item["status"] == "QUANTUM_VULNERABLE":
        return "P2: establish use, data lifetime and migration dependencies"
    return "P3: confirm parameters, implementation and operational controls"


def replacement(algorithm: str) -> str:
    if algorithm in {"RSA", "ECC"}:
        return ("Confirm purpose first: key establishment may use ML-KEM or a supported hybrid; "
                "signatures may use ML-DSA or SLH-DSA. Not a drop-in replacement.")
    if algorithm in {"ECDH", "X25519"}:
        return "Consider ML-KEM or a protocol-supported hybrid for key establishment."
    if algorithm in {"ECDSA", "Ed25519", "DSA"}:
        return "Consider ML-DSA or SLH-DSA signatures; validate PKI/protocol and size constraints."
    if algorithm == "SHA-1":
        return ("Review SHA-256/384/512 for collision-sensitive uses; "
                "PQC KEMs do not replace hashes.")
    if algorithm.startswith(("AES", "SHA-")):
        return "Review parameters, mode and purpose; no automatic replacement by a PQC primitive."
    return "UNKNOWN: confirm algorithm and purpose before selecting a migration candidate."


def render_report(inventory: dict[str, Any]) -> str:
    findings = inventory["findings"]
    counts = Counter(item["status"] for item in findings)
    lines = ["# PQC Crypto Inventory Report", "", "## Executive Summary", "",
             f"Scanned files: {inventory['files_scanned']}; findings: {len(findings)}.",
             f"QUANTUM_VULNERABLE: {counts['QUANTUM_VULNERABLE']}; "
             f"SAFE: {counts['SAFE']}; UNKNOWN: {counts['UNKNOWN']}.",
             "Counts describe static findings, not distinct deployed assets or a security verdict.",
             f"Partial result: {'YES' if inventory['truncated'] or inventory['issues'] else 'NO'}.",
             "", "## Cryptographic Inventory", "",
             "| Evidence | Kind | Algorithm | Status | Confidence |",
             "|---|---|---|---|---|"]
    for item in findings:
        evidence = item["path"] + (f":{item['line']}" if item["line"] else "")
        lines.append("| " + " | ".join(cell(x) for x in (
            evidence, item["kind"], item["value"], item["status"], item["confidence"])) + " |")
    if not findings:
        lines += ["", "No supported evidence found. "
                  "This does not establish absence of cryptography."]
    lines += ["", "## Quantum Vulnerability", "",
              "SAFE is a narrow algorithm-level label. "
              "It does not mean the system is quantum-safe."]
    for item in findings:
        lines.append(f"- {cell(item['path'])}: {cell(item['reason'])}")
    lines += ["", "## Migration Priority", "",
              "Triage categories are lab heuristics, not NIST deadlines. Confirm data retention, "
              "exposure, asset owner and protocol support before prioritizing production changes.",
              "Long-lived confidentiality warrants harvest-now-decrypt-later review."]
    for item in findings:
        lines.append(f"- {cell(item['path'])} / {cell(item['value'])}: {priority(item)}")
    lines += ["", "## Recommended PQC Replacement", ""]
    for algorithm in sorted({str(item["value"]) for item in findings}):
        lines.append(f"- {cell(algorithm)}: {replacement(algorithm)}")
    lines += ["", "## Crypto Agility Assessment", ""]
    agility = inventory.get("agility")
    if agility:
        lines += [f"Crypto Agility Score: {agility['score']} / 100 (evidence points).",
                  f"Assessed: {agility['assessed_items']} / 10; "
                  f"declared: {agility['declared_items']}; "
                  f"partial inventory: {agility['partial_inventory']}.",
                  agility["interpretation"], "",
                  "| Criterion | Score | Status | Reason | Evidence | Recommendation |",
                  "|---|---|---|---|---|---|"]
        for item in agility["items"]:
            lines.append("| " + " | ".join(cell(x) for x in (
                item["criterion"], f"{item['score']}/10", item["status"], item["reason"],
                ", ".join(item["evidence"]), item["recommendation"])) + " |")
    else:
        lines.append("Not scored. Inventory alone cannot establish operational agility.")
    lines += ["", "## Findings", ""]
    for issue in inventory["issues"]:
        lines.append(f"- {cell(issue['path'])}: {cell(issue['reason'])}")
    if inventory["truncated"]:
        lines.append("- File limit reached; the inventory is incomplete.")
    if not inventory["issues"] and not inventory["truncated"]:
        lines.append("No read/parse exclusions were reported among selected files.")
    lines += ["", "## Limitations", ""]
    lines.extend(f"- {cell(limit)}" for limit in inventory["limitations"])
    lines += ["- No secret contents or code excerpts are included; filenames still require review.",
              "- Report output is created exclusively and never overwrites an existing file.",
              "", "## References", "", "Reference status checked 2026-09-15."]
    lines.extend(f"- [{title}]({url})" for title, url in REFERENCES)
    return "\n".join(lines) + "\n"


def create_report(root: Path, output: Path, max_files: int = 10000) -> Path:
    inventory = scan_directory(root, max_files)
    inventory["agility"] = score_inventory(root, inventory)
    content = render_report(inventory)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as stream:
            stream.write(content)
    except OSError:
        raise ScanError("REPORT_WRITE_FAILED: output exists or unavailable destination") from None
    return output
