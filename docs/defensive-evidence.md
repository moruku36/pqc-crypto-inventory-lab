# Defensive inventory evidence ledger

Educational inventory lab. These local regressions test existing defensive behavior; production scanner code is unchanged. They do not establish runtime use, discovery completeness, interoperability, or a quantum-safe system.

| Claim | Test or source | Command | Observed result | Limit |
| --- | --- | --- | --- | --- |
| Synthetic content canary is absent from JSON, Markdown, CSV and captured stdout/stderr | `tests/test_defensive_boundaries.py::test_cli_content_canary_absent_from_all_exports` | `PYTHONPATH=src python -m pytest -q tests/test_defensive_boundaries.py` | Pass as part of the final 59-test suite | JSON/Python secret-like fields and synthetic PEM private-key body only; filenames remain visible and must not contain secrets |
| Malformed JSON/Python/UTF-8, oversized input and truncation are visible as partial | `test_partial_inventory_is_visible_and_csv_is_not_published` (5 cases) | Same targeted command | JSON issue/truncation marker and Markdown Partial result YES; CSV exit 1, no new file and existing output preserved | Directory/report exit 0 is not completeness or security success |
| MAX_BYTES boundary and growth after lstat fail safely | `test_read_exact_max_and_over_max`, `test_growth_after_lstat_is_bounded` | Same targeted command | Exact 1048576 bytes accepted; over-limit and post-stat growth refused | Size boundary tests, not a complete concurrency proof |
| File identity changes are refused | `test_fstat_identity_change_is_rejected`, `test_real_replacement_between_stat_and_open` | Same targeted command | Simulated device/inode mismatch and actual temporary-file replacement refused | One controlled interleaving; does not prove snapshot consistency against same-inode writes |
| Formula prefixes are escaped and manual assessment fields stay blank | `test_formula_prefix_survives_csv_roundtrip_as_text`; export-canary test | Same targeted command | = + - @ filenames prefixed with apostrophe after CSV roundtrip; whitespace variants covered by csv_cell; manual fields empty | String/CSV validation, not execution in spreadsheet software |
| All existing and new tests and static checks pass | `evidence/defensive-local-verification.json` | `PYTHONPATH=src python -m pytest -q tests`; `python -m ruff check src tests`; `python -m mypy src tests` | 59 passed; lint exit 0; mypy exit 0 over 17 source files | WSL local environment; Windows CI not run |

All fixtures are synthetic and temporary. The new regression module blocks socket.create_connection; existing TLS tests use invalid arguments or mocks. No external target was probed. Fifteen new regression cases supplement existing coverage. The canary assertions cover selected content paths, not arbitrary secrets, names or all encodings. Static algorithm labels and blank review columns cannot certify deployment properties.

## Reproduction and revision

Base commit: `b5f3b71c2ea528e68341e9cd595abc0794cb1660`. Implementation and test evidence commit: `51a8563fa102847fa2a129f183cf2a3672c78eca` (local only). The documentation commit follows it. CI for these changes has not run; earlier green CI is not evidence for this revision. Nothing was pushed or merged.

Commands run from the repository root with declared dependencies in an isolated WSL Ubuntu 24.04 Python 3.12 environment. Exact command output, UTC time and SHA-256 hashes of tested Python files are in [the local verification record](../evidence/defensive-local-verification.json). Use `git log -2 --oneline` to identify both local commits. Model/effort selection could not be independently inspected; Astra medium execution is not claimed.
