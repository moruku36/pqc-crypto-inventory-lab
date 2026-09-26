"""Export static findings as an unverified human review worksheet."""

import csv
from pathlib import Path
from typing import Any

from pqc_inventory.directory_scanner import scan_directory
from pqc_inventory.tls_scanner import ScanError

HEADERS = (
    "finding_id", "path", "line", "kind", "algorithm", "scanner_status",
    "owner", "purpose", "runtime_state", "data_retention_years", "exposure",
    "verification_source", "next_action",
)


def csv_cell(value: object) -> str:
    text = str(value)
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) else text


def review_rows(inventory: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for number, item in enumerate(inventory["findings"], 1):
        rows.append({
            "finding_id": f"F{number:03d}",
            "path": csv_cell(item["path"]),
            "line": str(item["line"] or ""),
            "kind": str(item["kind"]),
            "algorithm": csv_cell(item["value"]),
            "scanner_status": str(item["status"]),
            "owner": "", "purpose": "", "runtime_state": "",
            "data_retention_years": "", "exposure": "",
            "verification_source": "", "next_action": "",
        })
    return rows


def create_review(root: Path, output: Path, max_files: int = 10000) -> Path:
    inventory = scan_directory(root, max_files)
    if inventory["issues"] or inventory["truncated"]:
        raise ScanError("INCOMPLETE_INVENTORY: resolve scan issues before exporting review")
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(review_rows(inventory))
    except OSError:
        raise ScanError("REVIEW_WRITE_FAILED: output exists or unavailable destination") from None
    return output
