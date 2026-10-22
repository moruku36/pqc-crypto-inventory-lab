# Status and roadmap / 実装状況と計画

[English README](../README.md) | [日本語 README](../README.ja.md)

This is a status index, not a promise that every research proposal will become a feature. The source of truth for behavior is the code and tests; dated observations in [Implementation Summary](../IMPLEMENTATION_SUMMARY.md) are historical.

| Status | Item | Evidence or next condition |
|---|---|---|
| Implemented | One verified TLS handshake, bounded directory scan, algorithm classification, report, agility score, review CSV and static comparison | `src/pqc_inventory/`, `tests/`; limitations in both READMEs |
| This revision | Recognize exact ML-KEM-512/768/1024 and ML-DSA-44/65/87 names in selected configuration fields | [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final); regression test in `tests/test_directory.py`. No implementation validation |
| This revision | Synthetic offline review walkthrough and manual briefing/performance templates | [Exercise](offline-review-exercise.md), [performance evidence](performance-evidence.md); no production measurements |
| Proposed | Independent reviewer comparison and operational migration evidence | Requires a second human review and a scoped test environment. [CAMM note](camm-practical-evaluation.ja.md) |
| Decision pending | QER weights, equality/borderline policy, criticality aggregation and possible extra review CSV fields | Resolve [paper/model inconsistencies](pqc-discovery-governance.md) using an agreed local policy before automation |
| Decision pending | Automated performance risk, notebook use, supplier integration and broader language/dependency scanning | Define data sources, consent, coverage and acceptance tests; [Notebook note](gemini-pqc-notebook-readiness.md) |
| Out of scope now | Live estate scanning, key-store collection, production deployment, security certification | Needs separate authorization, data handling and operational validation |

## 日本語の要約

TLS の 1 回の観測、指定ディレクトリの静的棚卸し、分類、レポート、採点、確認票、差分比較は実装済みです。今回の変更は既知の NIST パラメータ名の認識と、合成サンプルで追える手作業資料です。QER の重み、等号の扱い、CSV の列追加、性能リスクの自動判定は根拠と運用方針が未確定です。実環境への走査・収集・配備は行いません。
