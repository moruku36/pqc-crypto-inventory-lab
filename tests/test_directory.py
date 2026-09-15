import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from pqc_inventory.directory_scanner import MAX_BYTES, inspect_file, scan_directory


def test_ast_not_comments_or_strings(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text(
        '# RSA SHA-1\ns = "AES"\nimport hashlib as h\nh.sha256(b"x")\n', encoding="utf-8")
    result = scan_directory(tmp_path)
    assert [f["value"] for f in result["findings"]] == ["SHA-256"]


def test_private_body_never_output(tmp_path: Path) -> None:
    secret = "CANARY_DO_NOT_EMIT"
    (tmp_path / "secret.pem").write_text(
        f"-----BEGIN PRIVATE KEY-----\n{secret}\n-----END PRIVATE KEY-----", encoding="utf-8")
    result = scan_directory(tmp_path)
    assert result["findings"][0]["kind"] == "private_key_present"
    assert secret not in json.dumps(result)


def test_public_ssh_key_parsed_without_comment() -> None:
    key = ed25519.Ed25519PrivateKey.generate().public_key()
    data = key.public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
    result = inspect_file(data + b" private-comment-canary", "key.pub")
    assert result[0]["value"] == "Ed25519"
    assert result[0]["status"] == "QUANTUM_VULNERABLE"
    assert "private-comment-canary" not in json.dumps(result)


def test_scope_limits_and_failures(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "x.json").write_text('{"algorithm":"RSA"}', encoding="utf-8")
    root = tmp_path / "root"
    root.mkdir()
    (root / "link.json").symlink_to(outside / "x.json")
    (root / "linked_dir").symlink_to(outside, target_is_directory=True)
    (root / "large.txt").write_bytes(b"x" * (MAX_BYTES + 1))
    (root / "bad.py").write_text("not valid python!!!", encoding="utf-8")
    (root / ".env").write_text("TOKEN=CANARY", encoding="utf-8")
    result = scan_directory(root)
    assert result["findings"] == []
    assert len(result["issues"]) == 4
    assert "CANARY" not in json.dumps(result)
    assert scan_directory(root, max_files=1)["truncated"] is True


def test_config_context_and_malformed_input(tmp_path: Path) -> None:
    (tmp_path / "config.json").write_text(
        '{"description":"RSA", "crypto":{"algorithm":"ECDSA"}}', encoding="utf-8")
    result = scan_directory(tmp_path)
    assert len(result["findings"]) == 1
    assert result["findings"][0]["value"] == "ECDSA"
