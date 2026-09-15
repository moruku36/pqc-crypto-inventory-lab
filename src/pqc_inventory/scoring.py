"""Transparent evidence score; declared operational maturity is not independently verified."""

import json
from pathlib import Path
from typing import Any

from pqc_inventory.directory_scanner import read_bounded
from pqc_inventory.tls_scanner import ScanError

CRITERIA = {
    "hard_coded_algorithms": "Move algorithm selection behind configuration or an interface.",
    "algorithm_abstraction": "Document and test an interchangeable crypto provider interface.",
    "centralized_key_management": "Document key ownership, access control and KMS/HSM integration.",
    "certificate_automation": "Document and test automated certificate issuance/deployment.",
    "key_rotation": "Test rotation, overlap, retirement and rollback of keys.",
    "cryptographic_library_dependency": "Track supported library versions and update procedures.",
    "protocol_negotiation": "Test authenticated negotiation and downgrade resistance.",
    "configuration_driven_selection": "Validate configurable choices against an approved policy.",
    "certificate_lifecycle_automation": "Test renewal, expiry monitoring and revocation workflows.",
    "upgradeability": "Test a crypto migration with compatibility checks and rollback.",
}
LEVELS = {"unknown": 0, "absent": 0, "documented": 5, "tested": 10}


def declarations(root: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    manifest = root / ".pqc-agility.json"
    if not manifest.exists() and not manifest.is_symlink():
        return {}
    try:
        if manifest.is_symlink() or ".pqc-agility.json" not in inventory["scanned_paths"]:
            raise ValueError("excluded manifest")
        data = json.loads(read_bounded(manifest))
        if not isinstance(data, dict) or set(data) != {"version", "criteria"}:
            raise ValueError("schema")
        if type(data["version"]) is not int or data["version"] != 1:
            raise ValueError("version")
        entries = data["criteria"]
        if not isinstance(entries, dict) or not set(entries) <= CRITERIA.keys():
            raise ValueError("criteria")
        forbidden = {f["path"] for f in inventory["findings"] if "private_key" in f["kind"]}
        for entry in entries.values():
            if not isinstance(entry, dict) or set(entry) != {"level", "evidence"}:
                raise ValueError("entry")
            if not isinstance(entry["level"], str) or entry["level"] not in LEVELS:
                raise ValueError("level")
            evidence = entry["evidence"]
            if not isinstance(evidence, list) or len(evidence) > 20:
                raise ValueError("evidence")
            if entry["level"] in {"documented", "tested"} and not evidence:
                raise ValueError("missing evidence")
            for path in evidence:
                if (not isinstance(path, str) or path not in inventory["scanned_paths"]
                        or path in forbidden or path == ".pqc-agility.json"):
                    raise ValueError("out of scope evidence")
        return dict(entries)
    except (OSError, ValueError, RecursionError):
        raise ScanError("AGILITY_MANIFEST_INVALID: check schema and evidence paths") from None


def score_inventory(root: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    declared = declarations(root, inventory)
    findings = inventory["findings"]
    api = sorted({f["path"] for f in findings if f["kind"] == "python_api_call"})
    config = sorted({f["path"] for f in findings if f["kind"] == "configuration"})
    items = []
    for name, recommendation in CRITERIA.items():
        item: dict[str, Any] = {
            "criterion": name, "score": 0, "max_score": 10, "status": "UNKNOWN",
            "reason": "Insufficient evidence. Zero unawarded points do not prove poor agility.",
            "evidence": [], "recommendation": recommendation,
        }
        if name in declared:
            entry = declared[name]
            item.update(score=LEVELS[entry["level"]], evidence=entry["evidence"],
                        status="UNKNOWN" if entry["level"] == "unknown" else "DECLARED",
                        reason=f"Operator declares {entry['level']}; evidence files exist. "
                        "Content and operational claims are not independently verified.")
        if name == "hard_coded_algorithms" and api:
            item.update(score=0, status="STATIC_EVIDENCE", evidence=api,
                        reason="Explicit crypto API calls found; conservative hard-coding flag. "
                        "This overrides positive declarations; review possible wrapper use.")
        elif name not in declared:
            paths = (config if name == "configuration_driven_selection" else
                     api if name == "cryptographic_library_dependency" else [])
            if paths:
                item.update(score=5, status="STATIC_EVIDENCE", evidence=paths,
                            reason="Configuration or crypto library API evidence found. "
                            "Runtime selection, support status and migration tests are unverified.")
        items.append(item)
    return {
        "score": sum(item["score"] for item in items), "max_score": 100,
        "assessed_items": sum(item["status"] != "UNKNOWN" for item in items),
        "total_items": 10,
        "declared_items": sum(item["status"] == "DECLARED" for item in items),
        "partial_inventory": bool(inventory["truncated"] or inventory["issues"]),
        "items": items,
        "interpretation": "Evidence/declared-maturity points, not a measured probability or "
        "NIST score. Unknowns receive no points and are shown separately. Declared tests are "
        "not executed or validated by this tool. Compare only equivalent scope and evidence.",
    }
