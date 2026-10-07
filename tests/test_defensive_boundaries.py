"""Local synthetic canaries and bounded-read/partial-export regressions."""

import csv
import json
import os
import socket
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from pqc_inventory import directory_scanner as scanner
from pqc_inventory.cli import main
from pqc_inventory.review import csv_cell

CANARY = "SYNTHETIC_CONTENT_CANARY_20261007"


@pytest.fixture(autouse=True)
def prohibit_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def refused(*args: object, **kwargs: object) -> None:
        raise AssertionError("These regressions must not use a network")
    monkeypatch.setattr(socket, "create_connection", refused)


def test_cli_content_canary_absent_from_all_exports(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    source = tmp_path / "input"
    source.mkdir()
    (source / "config.json").write_text(
        json.dumps({"algorithm": "RSA", "secret": CANARY}), encoding="utf-8")
    (source / "key.pem").write_text(
        f"-----BEGIN PRIVATE KEY-----\n{CANARY}\n-----END PRIVATE KEY-----\n",
        encoding="utf-8")
    (source / "usage.py").write_text(
        f'import hashlib\nsecret = "{CANARY}"\nhashlib.sha256(b"fixture")\n',
        encoding="utf-8")
    assert main(["directory", str(source)]) == 0
    captured = capsys.readouterr()
    inventory = json.loads(captured.out)
    assert inventory["findings"] and not inventory["issues"]
    assert CANARY not in captured.out + captured.err
    for command, suffix in (("report", ".md"), ("review", ".csv")):
        output = tmp_path / (command + suffix)
        assert main([command, str(source), "--output", str(output)]) == 0
        captured = capsys.readouterr()
        content = output.read_text(encoding="utf-8-sig")
        assert content and CANARY not in content + captured.out + captured.err
        if command == "review":
            with output.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.DictReader(stream))
            assert rows
            assert all(row[field] == "" for row in rows for field in (
                "owner", "purpose", "runtime_state", "verification_source", "next_action"))


@pytest.mark.parametrize("failure", ["json", "python", "utf8", "oversized", "truncated"])
def test_partial_inventory_is_visible_and_csv_is_not_published(
    failure: str, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    source = tmp_path / "input"
    source.mkdir()
    (source / "a.json").write_text('{"algorithm":"RSA"}', encoding="utf-8")
    payloads = {
        "json": ("bad.json", ('{"secret":"' + CANARY).encode()),
        "python": ("bad.py", ("invalid syntax ! " + CANARY).encode()),
        "utf8": ("bad.txt", b"\xff" + CANARY.encode()),
        "oversized": ("bad.txt", CANARY.encode().ljust(scanner.MAX_BYTES + 1, b"x")),
        "truncated": ("b.json", b'{"algorithm":"RSA"}'),
    }
    name, data = payloads[failure]
    (source / name).write_bytes(data)
    options = ["--max-files", "1"] if failure == "truncated" else []
    assert main(["directory", str(source), *options]) == 0
    captured = capsys.readouterr()
    inventory = json.loads(captured.out)
    assert inventory["truncated"] or inventory["issues"]
    assert CANARY not in captured.out + captured.err
    report = tmp_path / "report.md"
    assert main(["report", str(source), "--output", str(report), *options]) == 0
    captured = capsys.readouterr()
    content = report.read_text(encoding="utf-8")
    assert "Partial result: YES" in content
    assert CANARY not in content + captured.out + captured.err
    output = tmp_path / "review.csv"
    assert main(["review", str(source), "--output", str(output), *options]) == 1
    captured = capsys.readouterr()
    assert "INCOMPLETE_INVENTORY" in captured.err
    assert CANARY not in captured.out + captured.err
    assert not output.exists()
    output.write_text("existing evidence", encoding="utf-8")
    assert main(["review", str(source), "--output", str(output), *options]) == 1
    assert output.read_text(encoding="utf-8") == "existing evidence"


def test_read_exact_max_and_over_max(tmp_path: Path) -> None:
    source = tmp_path / "fixture.txt"
    data = b"x" * scanner.MAX_BYTES
    source.write_bytes(data)
    assert scanner.read_bounded(source) == data
    source.write_bytes(data + b"x")
    with pytest.raises(ValueError, match="excluded file"):
        scanner.read_bounded(source)


@pytest.mark.parametrize("field", ["st_ino", "st_dev"])
def test_fstat_identity_change_is_rejected(field: str, tmp_path: Path) -> None:
    source = tmp_path / "fixture.txt"
    source.write_bytes(b"fixture")
    original = source.stat()
    changed = SimpleNamespace(st_mode=original.st_mode, st_ino=original.st_ino,
                              st_dev=original.st_dev)
    setattr(changed, field, getattr(changed, field) + 1)
    with patch.object(os, "fstat", return_value=changed):
        with pytest.raises(ValueError, match="changed file"):
            scanner.read_bounded(source)


def test_growth_after_lstat_is_bounded(tmp_path: Path) -> None:
    source = tmp_path / "fixture.txt"
    source.write_bytes(b"small")
    real_open = os.open

    def grow_then_open(path: Path, flags: int) -> int:
        source.write_bytes(b"x" * (scanner.MAX_BYTES + 1))
        return real_open(path, flags)

    with patch.object(os, "open", side_effect=grow_then_open):
        with pytest.raises(ValueError, match="oversized file"):
            scanner.read_bounded(source)


@pytest.mark.parametrize("prefix", ["=", "+", "-", "@"])
def test_formula_prefix_survives_csv_roundtrip_as_text(prefix: str, tmp_path: Path) -> None:
    source = tmp_path / "input"
    source.mkdir()
    name = prefix + "fixture.json"
    (source / name).write_text('{"algorithm":"RSA"}', encoding="utf-8")
    output = tmp_path / "review.csv"
    assert main(["review", str(source), "--output", str(output)]) == 0
    with output.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert rows and rows[0]["path"] == "'" + name
    for whitespace in ("", " ", "\t", "\r\n"):
        value = whitespace + prefix + "fixture"
        assert csv_cell(value) == "'" + value


def test_real_replacement_between_stat_and_open(tmp_path: Path) -> None:
    source = tmp_path / "fixture.txt"
    replacement = tmp_path / "replacement.txt"
    source.write_bytes(b"original")
    replacement.write_bytes(b"replacement")
    assert source.stat().st_ino != replacement.stat().st_ino
    real_open = os.open

    def replace_then_open(path: Path, flags: int) -> int:
        replacement.replace(source)
        return real_open(path, flags)

    with patch.object(os, "open", side_effect=replace_then_open):
        with pytest.raises(ValueError, match="changed file"):
            scanner.read_bounded(source)
