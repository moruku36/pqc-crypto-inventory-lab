"""Compare static inventory evidence without claiming a completed migration."""

from collections import Counter
from pathlib import Path
from typing import Any

from pqc_inventory.directory_scanner import scan_directory


def compare_directories(before: Path, after: Path, max_files: int = 10000) -> dict[str, Any]:
    old = scan_directory(before, max_files)
    new = scan_directory(after, max_files)

    def count(inventory: dict[str, Any]) -> Counter[tuple[str, str, str, str]]:
        return Counter((str(item["path"]), str(item["kind"]), str(item["value"]),
                        str(item["status"])) for item in inventory["findings"])

    old_counts, new_counts = count(old), count(new)

    def entries(counter: Counter[tuple[str, str, str, str]]) -> list[dict[str, Any]]:
        return [{"path": path, "kind": kind, "algorithm": algorithm, "status": status,
                 "count": amount}
                for (path, kind, algorithm, status), amount in sorted(counter.items())]

    return {
        "schema_version": 1,
        "before": {"files_scanned": old["files_scanned"], "findings": len(old["findings"]),
                   "issues": old["issues"], "truncated": old["truncated"]},
        "after": {"files_scanned": new["files_scanned"], "findings": len(new["findings"]),
                  "issues": new["issues"], "truncated": new["truncated"]},
        "removed_evidence": entries(old_counts - new_counts),
        "added_evidence": entries(new_counts - old_counts),
        "unchanged_evidence": entries(old_counts & new_counts),
        "limitations": [
            "Evidence changes do not prove deployment, runtime use, or migration success.",
            "Content changes with the same path, kind, algorithm and status are not shown.",
            "Review scan issues and truncation before interpreting missing evidence.",
            "Compare compatibility, certificate deployment, data lifetime, and owners manually.",
        ],
    }
