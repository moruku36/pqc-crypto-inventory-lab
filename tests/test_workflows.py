"""Exercise the review and before/after workflows on synthetic evidence."""

import csv
import json
from pathlib import Path

import pytest

from pqc_inventory.compare import compare_directories
from pqc_inventory.directory_scanner import scan_directory
from pqc_inventory.review import create_review, csv_cell, review_rows
from pqc_inventory.tls_scanner import ScanError


SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_review_exports_blank_fields_and_preserves_existing_file(tmp_path: Path) -> None:
    output = tmp_path / "review.csv"
    create_review(SAMPLES / "mini-service", output)
    with output.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 6
    assert [row["finding_id"] for row in rows] == [f"F{n:03d}" for n in range(1, 7)]
    assert all(row["owner"] == row["purpose"] == row["verification_source"] == ""
               for row in rows)
    with pytest.raises(ScanError, match="REVIEW_WRITE_FAILED"):
        create_review(SAMPLES / "mini-service", output)
    assert csv_cell("=HYPERLINK(\"https://invalid\")").startswith("'")


def test_review_rejects_partial_inventory(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("invalid syntax !", encoding="utf-8")
    with pytest.raises(ScanError, match="INCOMPLETE_INVENTORY"):
        create_review(tmp_path, tmp_path / "review.csv")


def test_migration_comparison_retains_unresolved_evidence() -> None:
    result = compare_directories(SAMPLES / "mini-service", SAMPLES / "migration-after")
    removed = {(item["path"], item["algorithm"]) for item in result["removed_evidence"]}
    added = {(item["path"], item["algorithm"]) for item in result["added_evidence"]}
    unchanged = {(item["path"], item["algorithm"]) for item in result["unchanged_evidence"]}
    assert ("app/signing.py", "RSA") in removed
    assert ("config/transport.json", "X25519") in removed
    assert ("config/transport.json", "ML-KEM") in added
    assert ("config/transport.json", "ML-DSA") in added
    assert ("certs/service.crt", "RSA") in unchanged
    assert ("retired/old_signing.py", "SHA-1") in unchanged
    assert result["before"]["issues"] == result["after"]["issues"] == []


def test_review_example_marks_manual_and_unverified_rows() -> None:
    with (SAMPLES / "mini-service-review-example.csv").open(encoding="utf-8-sig",
                                                       newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 8
    current = review_rows(scan_directory(SAMPLES / "mini-service"))
    assert [(row["finding_id"], row["path"], row["algorithm"]) for row in rows[:6]] == [
        (row["finding_id"], row["path"], row["algorithm"]) for row in current]
    assert {row["finding_id"] for row in rows if row["scanner_status"] == "NOT_DETECTED"} == {
        "M001", "M002"}
    assert all("exercise scenario" in row["verification_source"] or
               row["verification_source"] == "configuration only" for row in rows)


def test_synthetic_compatibility_exposes_legacy_gap() -> None:
    matrix = json.loads((SAMPLES / "migration-compatibility.json").read_text(encoding="utf-8"))
    assert matrix["synthetic_assumptions_only"] is True
    legacy, pilot = matrix["clients"]
    for scheme, capability in (("proposed_key_exchange", "key_exchange_supported"),
                               ("proposed_signature", "signatures_supported")):
        assert matrix[scheme] not in legacy[capability]
        assert matrix[scheme] in pilot[capability]
