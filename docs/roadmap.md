# Status and roadmap / 実装状況と計画

[English README](../README.md) | [日本語 README](../README.ja.md)

This is a status index, not a promise that every research proposal will become a feature. The source of truth for behavior is the code and tests; dated observations in [Implementation Summary](../IMPLEMENTATION_SUMMARY.md) are historical.

| Status | Item | Evidence or next condition |
|---|---|---|
| Implemented | One verified TLS handshake, bounded directory scan, algorithm classification, report, agility score, review CSV and static comparison | `src/pqc_inventory/`, `tests/`; limitations in both READMEs |
| Implemented | Recognize exact ML-KEM-512/768/1024 and ML-DSA-44/65/87 names in selected configuration fields | [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final); regression test in `tests/test_directory.py`. No implementation validation |
| Available documentation | Synthetic offline review walkthrough, two-layer briefing template and manual performance template | [Exercise](offline-review-exercise.md), [briefing](briefing-template.md), [performance evidence](performance-evidence.md); no production measurements or second review |
| Proposed | Independent reviewer comparison and operational migration evidence | Requires a second human review and a scoped test environment. [CAMM note](camm-practical-evaluation.ja.md) |
| Decision pending | QER weights, equality/borderline policy, criticality aggregation and possible extra review CSV fields | Resolve [paper/model inconsistencies](pqc-discovery-governance.md) using an agreed local policy before automation |
| Decision pending | Automated performance risk, notebook use, supplier integration and broader language/dependency scanning | Define data sources, consent, coverage and acceptance tests; [Notebook note](gemini-pqc-notebook-readiness.md) |
| Out of scope now | Live estate scanning, key-store collection, production deployment, security certification | Needs separate authorization, data handling and operational validation |

## 日本語の要約

TLS の 1 回の観測、指定ディレクトリの静的棚卸し、分類、レポート、採点、確認票、差分比較は実装済みです。今回の変更は既知の NIST パラメータ名の認識と、合成サンプルで追える手作業資料です。QER の重み、等号の扱い、CSV の列追加、性能リスクの自動判定は根拠と運用方針が未確定です。実環境への走査・収集・配備は行いません。

## Decisions needed before changing QER or the CSV

| Decision | Why the existing material does not choose it | Evidence needed before code |
|---|---|---|
| QER temporal outcome | The reviewed paper has a strict `T_shelf + T_migration > T_threat` equation, but calls one greater-than example “Borderline” without a numeric rule. Equality and missing inputs need a local policy. | Define a scenario horizon and below/equal/above/unknown behavior; keep a reason for any manual override. [Model review](pqc-discovery-governance.md) |
| QER wave or score | The C/I/A-to-scalar aggregation is unspecified, and QER-007's worked wave conflicts with the obvious high-value calculation. The paper's weights and wave cutoffs are organization-specific. | Agree on aggregation, weights, cutoffs and review authority; test synthetic boundary cases and keep this separate from the existing 0–100 agility score. [Model review](pqc-discovery-governance.md) |
| `use class` in review CSV | The [Notebook note](gemini-pqc-notebook-readiness.md) explicitly defers the column decision until an exercise. The current [walkthrough](offline-review-exercise.md) covers selected cases only; a separate [briefing template](briefing-template.md) can carry manual notes without changing the schema. | Complete each-finding review, compare usefulness with a companion worksheet, then define vocabulary, optional/unknown values, provenance and CSV compatibility. Never infer this field from the static scanner. |

These are concrete product and evidence choices, not missing code branches with one predetermined answer. A later change can remain small once those choices are recorded and a second reviewer can trace them. No real asset data is needed to design the synthetic boundary tests.
