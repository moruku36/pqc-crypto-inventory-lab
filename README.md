# PQC Crypto Inventory Lab

[English](README.md) | [日本語](README.ja.md)

An educational tool for inventorying cryptography in source code, configuration, and supported TLS endpoints, then producing findings and migration-planning reports for post-quantum readiness.

## Start learning

Use the supplied sample and reports to learn how crypto inventory findings become migration-planning inputs. The project includes TLS inspection, directory inventory, migration reports, a crypto-agility score, and security-specialist learning notes.

```bash
python -m venv .venv
# Activate the virtual environment for your shell.
python -m pip install -e ".[dev]"
pqc-scan --help
pqc-scan directory ./samples/project
```

[Getting started](docs/getting-started.md) · [Reading results](docs/reading-results.md) · [Scoring](docs/scoring.md) · [Architecture](docs/architecture.md) · [Glossary](docs/glossary.md).

Findings and scores are educational planning aids. They do not prove that all cryptography has been found or that a system is quantum-safe. Review the documented scanner scope and security boundaries.


## Contents

- [SECURITY.md](SECURITY.md)
- [docs/](docs)
- [reports/](reports)
- [samples/](samples)
- [src/](src)
- [tests/](tests)

## Detailed documentation

The [Japanese guide](README.ja.md) retains the complete original setup instructions, configuration, examples, project status, and limitations. Supporting documents keep their existing language.
