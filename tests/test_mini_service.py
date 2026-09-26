"""Check the exercise's expected observations without claiming runtime use."""

import json
from collections import Counter
from pathlib import Path

from pqc_inventory.directory_scanner import scan_directory


def test_mini_service_matches_ground_truth() -> None:
    root = Path(__file__).resolve().parents[1] / "samples" / "mini-service"
    truth = json.loads((root.parent / "mini-service-ground-truth.json").read_text(encoding="utf-8"))
    result = scan_directory(root)
    observed = Counter((item["path"], item["value"]) for item in result["findings"])
    expected = Counter({
        (case["path"], case["algorithm"]): case.get("expected_count", 1)
        for case in truth["cases"] if case["detected"]
    })

    assert result["issues"] == []
    assert result["truncated"] is False
    assert observed == expected
    assert not any(item["path"].endswith("ground-truth.json") for item in result["findings"])
