from pathlib import Path

import pytest

from pqc_inventory.directory_scanner import scan_directory
from pqc_inventory.report import cell, create_report, render_report, replacement
from pqc_inventory.tls_scanner import ScanError


def test_sections_and_empty_inventory(tmp_path: Path) -> None:
    report = render_report(scan_directory(tmp_path))
    for section in ["Executive Summary", "Cryptographic Inventory", "Quantum Vulnerability",
                    "Migration Priority", "Recommended PQC Replacement",
                    "Crypto Agility Assessment",
                    "Findings", "Limitations", "References"]:
        assert f"## {section}" in report
    assert "does not establish absence" in report
    assert "INITIAL PUBLIC DRAFT" in report


def test_report_never_overwrites(tmp_path: Path) -> None:
    output = tmp_path / "report.md"
    output.write_text("DO NOT OVERWRITE", encoding="utf-8")
    with pytest.raises(ScanError):
        create_report(tmp_path, output)
    assert output.read_text() == "DO NOT OVERWRITE"


def test_markdown_escape() -> None:
    escaped = cell('<img src=x> | [click](https://bad.invalid)\n# title')
    assert "<img" not in escaped
    assert "[click]" not in escaped
    assert "|" not in escaped
    assert "\n" not in escaped


def test_conditional_replacements() -> None:
    assert "Confirm purpose first" in replacement("RSA")
    assert "key establishment" in replacement("ECDH")
    assert "signatures" in replacement("ECDSA")
    assert "no automatic replacement" in replacement("AES-256")


def test_incomplete_report(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("bad syntax!", encoding="utf-8")
    report = render_report(scan_directory(tmp_path))
    assert "Partial result: YES" in report
    assert "bad syntax!" not in report
