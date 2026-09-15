"""Bounded inventory: no source snippets, key material, or secret values in output."""

import ast
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

from cryptography import x509
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives import serialization

from pqc_inventory.classification import assess
from pqc_inventory.tls_scanner import ScanError, public_key_info

MAX_BYTES = 1_048_576
MAX_FILES = 10_000
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache",
             ".pytest_cache", ".ruff_cache", "reports"}
TEXT_SUFFIXES = {".py", ".json", ".toml", ".yaml", ".yml", ".ini", ".conf", ".cfg",
                 ".js", ".ts", ".java", ".go", ".rs", ".c", ".h", ".txt", ".pem",
                 ".crt", ".cer", ".pub", ".key"}
ALIASES = {"rsa": "RSA", "ecdsa": "ECDSA", "ecdh": "ECDH", "ed25519": "Ed25519",
           "x25519": "X25519", "sha1": "SHA-1", "sha256": "SHA-256",
           "sha384": "SHA-384", "sha512": "SHA-512", "aes": "AES", "aes256": "AES-256"}
PRIVATE_HEADER = re.compile(rb"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
CONFIG_ALGORITHM = re.compile(
    r"^\s*[\"']?(?:algorithm|cipher|hash|signature_algorithm|key_exchange)[\"']?\s*[:=]\s*"
    r"[\"']?([a-zA-Z0-9_-]+)[\"']?\s*[,;]?(?:\s*[#;].*)?$", re.IGNORECASE)


def canonical(value: str) -> str | None:
    return ALIASES.get(value.lower().replace("-", "").replace("_", ""))


def finding(path: str, algorithm: str, kind: str, line: int | None = None,
            confidence: str = "MEDIUM") -> dict[str, Any]:
    assessment = assess("ECDH/ECDSA" if algorithm == "ECC" else algorithm).to_dict()
    assessment["value"] = algorithm
    return {"path": path, "line": line, "kind": kind, "confidence": confidence,
            **assessment}


def read_bounded(path: Path) -> bytes:
    """Reject links/special files and detect replacement between lstat and open."""
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_BYTES:
        raise ValueError("excluded file")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                 | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as stream:
        after = os.fstat(stream.fileno())
        if not stat.S_ISREG(after.st_mode) or (before.st_dev, before.st_ino) != (
                after.st_dev, after.st_ino):
            raise ValueError("changed file")
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("oversized file")
    return data


def python_findings(text: str, path: str) -> list[dict[str, Any]]:
    tree = ast.parse(text)
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name.split(".")[0]] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                aliases[alias.asname or alias.name] = f"{node.module}.{alias.name}"

    def qualified(node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return aliases.get(node.id, "")
        if isinstance(node, ast.Attribute):
            prefix = qualified(node.value)
            return f"{prefix}.{node.attr}" if prefix else ""
        return ""

    results = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = qualified(node.func)
        if not name.startswith(("hashlib.", "cryptography.", "Crypto.", "Cryptodome.")):
            continue
        algorithms = {canonical(part) for part in name.split(".")} - {None}
        if name == "hashlib.new" and node.args and isinstance(node.args[0], ast.Constant):
            value = node.args[0].value
            if isinstance(value, str) and canonical(value):
                algorithms.add(canonical(value))
        for algorithm in sorted(x for x in algorithms if x is not None):
            results.append(finding(path, algorithm, "python_api_call", node.lineno))
    return results


def inspect_file(data: bytes, path: str) -> list[dict[str, Any]]:
    if PRIVATE_HEADER.search(data):
        return [finding(path, "UNKNOWN", "private_key_present", confidence="HIGH")]
    if b"-----BEGIN CERTIFICATE-----" in data:
        results = []
        for cert in x509.load_pem_x509_certificates(data):
            algorithm, _ = public_key_info(cert.public_key())
            results.append(finding(path, algorithm, "x509_public_key", confidence="HIGH"))
        return results
    if b"-----BEGIN PUBLIC KEY-----" in data or b"-----BEGIN RSA PUBLIC KEY-----" in data:
        key = serialization.load_pem_public_key(data)
        algorithm, _ = public_key_info(key)
        return [finding(path, algorithm, "pem_public_key", confidence="HIGH")]
    if data.startswith((b"ssh-rsa ", b"ssh-ed25519 ", b"ecdsa-sha2-")):
        key = serialization.load_ssh_public_key(data)
        algorithm, _ = public_key_info(key)
        return [finding(path, algorithm, "ssh_public_key", confidence="HIGH")]
    if Path(path).suffix.lower() in {".der", ".cer", ".crt"} and data.startswith(b"0"):
        cert = x509.load_der_x509_certificate(data)
        algorithm, _ = public_key_info(cert.public_key())
        return [finding(path, algorithm, "x509_public_key", confidence="HIGH")]
    if b"\0" in data:
        return []
    text = data.decode("utf-8")
    if path.endswith(".py"):
        return python_findings(text, path)
    if path.endswith(".json"):
        obj = json.loads(text)
        results = []

        def visit(value: Any) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in {"algorithm", "cipher", "hash", "signature_algorithm",
                               "key_exchange"} and isinstance(child, str):
                        algorithm = canonical(child)
                        if algorithm:
                            results.append(finding(path, algorithm, "configuration"))
                    elif isinstance(child, (dict, list)):
                        visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(obj)
        return results
    results = []
    for number, line in enumerate(text.splitlines(), 1):
        match = CONFIG_ALGORITHM.fullmatch(line)
        if match and (config_algorithm := canonical(match[1])):
            results.append(finding(path, config_algorithm, "configuration", number))
    return results


def scan_directory(root: Path, max_files: int = MAX_FILES) -> dict[str, Any]:
    if root.is_symlink() or not root.is_dir():
        raise ScanError("INVALID_DIRECTORY: specify an existing non-symlink directory")
    if not 1 <= max_files <= MAX_FILES:
        raise ScanError("INVALID_LIMIT: max-files must be 1..10000")
    root = root.resolve()
    findings: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    scanned: list[str] = []
    examined = 0
    truncated = False

    def walk_error(error: OSError) -> None:
        issues.append({"path": ".", "reason": "directory_unreadable"})

    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS
                         and not Path(directory, d).is_symlink())
        for filename in sorted(files):
            examined += 1
            if examined > max_files:
                truncated = True
                break
            path = Path(directory, filename)
            relative = path.relative_to(root).as_posix()
            if filename.startswith(".env") or filename in {"credentials", "id_rsa", "id_ed25519"}:
                if filename.startswith("id_"):
                    # Presence is recorded without opening conventional private key files.
                    findings.append(finding(relative, "UNKNOWN", "possible_private_key_file"))
                issues.append({"path": relative, "reason": "sensitive_filename_excluded"})
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES | {".der"}:
                continue
            try:
                if path.is_symlink() or not path.resolve().is_relative_to(root):
                    raise ValueError("outside scope")
                data = read_bounded(path)
                results = inspect_file(data, relative)
                scanned.append(relative)
                findings.extend(results)
            except (OSError, ValueError, SyntaxError, UnsupportedAlgorithm, RecursionError):
                issues.append({"path": relative, "reason": "unreadable_unsupported_or_excluded"})
        if truncated:
            break
    return {"schema_version": 1, "scope": "explicit directory; paths are relative",
            "files_scanned": len(scanned), "scanned_paths": scanned,
            "truncated": truncated, "findings": findings, "issues": issues,
            "limitations": ["Static evidence is not proof of runtime use or absence.",
                            "Python AST calls and selected configuration keys only; other code "
                            "languages/dependencies require review.",
                            "Aliases may be rebound; API hits are medium-confidence evidence.",
                            "Symlinks, generated/dependency directories and large files excluded.",
                            "Scan a quiescent directory; concurrent directory replacement "
                            "is unsupported.",
                            "No source snippets; relative filenames themselves may be sensitive."]}
