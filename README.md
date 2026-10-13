# PQC Crypto Inventory Lab

[English](README.md) | [日本語](README.ja.md)

An educational tool for inventorying cryptography in source code, configuration, and supported TLS endpoints, then producing findings and migration-planning reports for post-quantum readiness.

## Research into practice

The [PQC discovery paper review](docs/pqc-discovery-governance.md) ([日本語](docs/pqc-discovery-governance.ja.md), arXiv:2605.16549v1, reviewed 2026-10-12) explains how evidence, accountable owners and supplier constraints can turn findings into decisions. It starts with a short PMO overview and proposes an offline exercise using existing samples. The case study has not been reproduced here; QER scoring and register extensions are not implemented. Continue through the [human review workflow](docs/review-workflow.md) and [source index](docs/references.md).

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

---

## Future Research — measured PQC performance impact (2026-10-13)

**Status: proposed; no scanner, scoring or accelerator feature added.**

### Paper reviewed

[Accelerating Post-Quantum Cryptography via LLM-Driven Hardware-Software Co-Design](https://arxiv.org/html/2602.09410v1) — Yuchao Liao, Tosiron Adegbija and Roman Lysecky; arXiv:2602.09410v1. Reviewed Sections III–V and Table III. The study uses ChatGPT-4o, gprof, FALCON reference C, Cortex-A53 and ZCU104/Vitis HLS 2023.2. Its up-to-2.6× result concerns individual kernels versus HLS, not end-to-end TLS. Source-only hotspot rankings diverged from profiling; constant-time and leakage verification remain future work.

The following are **our migration-planning proposals**. The paper does not establish a hardware requirement for all PQC deployments, or validate Nitro Enclaves/CloudHSM as PQC accelerators. Provider support and actual offload capability require separate evidence.

| Priority | Planned investigation | Acceptance criterion |
|---|---|---|
| P1 | Draft an optional performance evidence register alongside inventory findings: workload/operation, algorithm and parameter set, library/version, CPU/runtime, build flags, concurrency, baseline and candidate latency/throughput, CPU/memory, timestamp and evidence reference. | Distinguish measured, declared, inferred and unknown values. Static detections never fabricate CPU load or performance estimates. Missing benchmark evidence stays unknown and does not silently change the existing agility score. |
| P1 | Start with a manual offline benchmark of a maintained library on the actual target CPU; measure key generation, signing, verification and key establishment separately where supported. | Fix build/workload conditions, use warm-up and repeated runs, report distributions and failures. Compare against application requirements; kernel timing alone cannot predict TLS latency. No external TLS load test is started automatically. |
| P2 | Produce a migration-impact report that joins inventory ownership/use with benchmark evidence, application SLOs and supplier constraints. | Report measured headroom, uncertainties and owner review. Consider software optimization, library choice and capacity before declaring offload necessary; no performance-risk classification from algorithm name alone. |
| P2 | Evaluate source-only versus profile-guided hotspot suggestions with a local model as an optional assistant, linked to the Sidekick research plan. | Validate suggestions against held-out measurements and function references; disclose model, quantization and prompt. Local-model suitability is unverified, and LLM rankings are advisory. |
| P3 | Explore one FPGA kernel only if measured application limits justify it; use AI Governance Control for separately scoped independent reference checking. | Compare latency, throughput, area/power and data-transfer/integration overhead. Functional, constant-time and side-channel checks are separate. Unsupported or unperformed checks remain unknown; no self-generated production crypto is adopted. |

**Next milestone:** a manually populated performance-register example and reproducible CPU benchmark plan. This extends migration evidence, not the current scanner's language support or a claim of quantum-safe certification. See [source references](docs/references.md), [human review](docs/review-workflow.md), and [AI Governance Control research](https://github.com/moruku36/ai-governance-control#future-research--agent-runtime-and-hwsw-verification-2026-10-13).
