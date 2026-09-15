import json
from pathlib import Path

import pytest

from pqc_inventory.directory_scanner import scan_directory
from pqc_inventory.scoring import CRITERIA, score_inventory
from pqc_inventory.tls_scanner import ScanError


def manifest(root: Path, criteria: dict[str, object]) -> None:
    (root / ".pqc-agility.json").write_text(
        json.dumps({"version": 1, "criteria": criteria}), encoding="utf-8")


def test_unknown_is_not_an_asserted_failure(tmp_path: Path) -> None:
    result = score_inventory(tmp_path, scan_directory(tmp_path))
    assert result["score"] == 0
    assert result["assessed_items"] == 0
    assert all(i["status"] == "UNKNOWN" for i in result["items"])


def test_declared_full_scale_and_provenance(tmp_path: Path) -> None:
    (tmp_path / "evidence.txt").write_text("operator test record", encoding="utf-8")
    manifest(tmp_path, {k: {"level": "tested", "evidence": ["evidence.txt"]} for k in CRITERIA})
    result = score_inventory(tmp_path, scan_directory(tmp_path))
    assert result["score"] == 100
    assert result["declared_items"] == 10
    assert "not executed" in result["interpretation"]


def test_contradictory_hardcoding_overrides_declaration(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text('import hashlib\nhashlib.sha256(b"x")', encoding="utf-8")
    manifest(tmp_path, {"hard_coded_algorithms": {"level": "tested", "evidence": ["code.py"]}})
    result = score_inventory(tmp_path, scan_directory(tmp_path))
    assert result["items"][0]["score"] == 0
    assert result["items"][0]["status"] == "STATIC_EVIDENCE"
    assert result["score"] == 5


@pytest.mark.parametrize("evidence", [[], ["../outside.txt"], ["missing.txt"], [".env"],
                                     [".pqc-agility.json"]])
def test_bad_evidence_rejected(tmp_path: Path, evidence: list[str]) -> None:
    manifest(tmp_path, {"key_rotation": {"level": "tested", "evidence": evidence}})
    with pytest.raises(ScanError):
        score_inventory(tmp_path, scan_directory(tmp_path))


def test_static_configuration_points(tmp_path: Path) -> None:
    (tmp_path / "policy.json").write_text('{"cipher":"AES-256"}', encoding="utf-8")
    result = score_inventory(tmp_path, scan_directory(tmp_path))
    assert result["score"] == 5
    assert result["assessed_items"] == 1
