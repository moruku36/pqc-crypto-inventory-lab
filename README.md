# PQC Crypto Inventory Lab

[日本語](README.ja.md) | English

An educational, evidence-based inventory for cryptography in selected local files and one authorized TLS endpoint. It helps a person plan what to investigate for post-quantum migration. It does not certify a system as quantum-safe.

![Data flow from selected inputs to static findings and reports](docs/images/architecture-overview.svg)

## Try the bundled sample

Python 3.11 or later is required. From the repository root:

```sh
python -m venv .venv
# Activate .venv using your shell's normal command.
python -m pip install -e ".[dev]"
pqc-scan directory ./samples/project
pqc-scan score ./samples/project
pqc-scan report ./samples/project --output reports/first-review.md
```

The first command prints JSON findings. `path` and `line` locate evidence; `kind` describes detection; `value`, `status`, `confidence`, and `reason` describe a narrow algorithm-level assessment. The sample has five findings and scores 25/100 evidence points, not a security percentage. The report creates a new file and never overwrites one. See [reading results](docs/reading-results.md) and [the scoring rubric](docs/scoring.md).

## What works today

| Command | Input | Output and boundary |
|---|---|---|
| `directory PATH` | Explicit local directory | JSON: selected Python crypto API calls, selected configuration keys, public keys, X.509 certificates, and private-key presence. Static evidence only. |
| `score PATH` | Same directory and optional `.pqc-agility.json` | JSON: ten evidence/declaration criteria. Declarations are not independently verified. |
| `report PATH --output FILE` | Same directory | Markdown inventory and heuristic migration questions. Creates a new file. |
| `review PATH --output FILE` | Complete directory inventory | Blank CSV for human verification. Refuses partial scans. |
| `compare BEFORE AFTER` | Two selected directories | JSON change in static evidence; no deployment verification. |
| `tls HOST` | One explicitly authorized TLS host | One certificate-verified handshake and JSON snapshot. No broad network discovery. |

Run `pqc-scan --help` for options. [Architecture and data flow](docs/architecture.md) explain the implementation. [Getting started](docs/getting-started.md) gives a step-by-step Japanese walkthrough; [synthetic samples](samples/README.md) include expected misses and a human review example.

## Read results safely

`QUANTUM_VULNERABLE` identifies a classical public-key family to investigate. `SAFE` is a narrow algorithm-level screening label and does **not** validate parameters, implementation, protocol, key management, or deployment. `UNKNOWN` means the available evidence does not support a conclusion. Zero findings do not establish absence. The report's P1–P3 priorities and agility score are project heuristics, not NIST ratings or deadlines.

The scanner reads only an explicitly chosen directory, with file and count limits. It does not execute sample code or decode private keys, but may read file bytes to identify a private-key header; do not point it at real secrets without authorization. Paths in JSON, CSV and Markdown can themselves be sensitive. Generated `reports/` files are ignored by Git; review output before sharing. For safe learning, use `samples/project` or `samples/mini-service`. Do not use `tls` without permission for the target. Certificate-store collection, broad network scans and live migration are outside this tool.

## Plans and references

[Roadmap and status](docs/roadmap.md) separates implemented work, this revision and decisions still needed. The [offline review exercise](docs/offline-review-exercise.md) and [performance evidence template](docs/performance-evidence.md) use synthetic or unknown values; neither measures a real deployment. Research notes on [PQC discovery](docs/pqc-discovery-governance.md), [CAMM](docs/camm-practical-evaluation.ja.md), [Google's PQC Notebook](docs/gemini-pqc-notebook-readiness.md), and [other references](docs/references.md) remain background, not implemented features. Historical test and phase records are in [Implementation Summary](IMPLEMENTATION_SUMMARY.md).

NIST's finalized standards are [FIPS 203 (ML-KEM)](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204 (ML-DSA)](https://csrc.nist.gov/pubs/fips/204/final), and [FIPS 205 (SLH-DSA)](https://csrc.nist.gov/pubs/fips/205/final). This lab only recognizes selected names; it does not implement or validate those algorithms. See [security policy](SECURITY.md) and [contributing guide](CONTRIBUTING.md).
