# Offline ML-KEM-768 experiment

This is a small first step toward the P1 manual CPU measurement in [performance evidence](../../docs/performance-evidence.md). The inventory scanner remains unchanged. It uses Go's maintained [crypto/mlkem](https://pkg.go.dev/crypto/mlkem) implementation of [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), not a new cryptographic implementation. Only ephemeral in-memory keys and synthetic inputs are used; no key material is printed or saved.

The lab's stored [performance note](../../docs/performance-evidence.md) discusses [Liao et al.](https://arxiv.org/html/2602.09410v1), which reports FALCON kernel experiments on different hardware. This ML-KEM measurement is neither a reproduction nor a confirmation of that paper's results. It provides a local starting point for the roadmap, not a performance risk decision.

## Reproduce

Requires Go 1.24 or later for `crypto/mlkem`. The library test names below were checked with Go 1.27.0; they may differ in other releases. Run offline in this directory, limiting Go execution to one logical processor (PowerShell example):

```powershell
$env:GOMAXPROCS = '1'
$env:GOPROXY = 'off'
go test -short -run 'TestAccumulated|TestRoundTrip|TestBadLengths|TestConstantSizes' crypto/mlkem
go test ./...
go run .
```

The standard library's `TestAccumulated` short mode checks the aggregate hash of 100 deterministic vectors, including encapsulation and decapsulation; this is Go's existing regression test, not a NIST validation or claim of formal validation. The experiment checks a round trip and lengths, then uses two warm-up batches and 20 measured batches of 100 operations each: 2,000 measured operations per type. Each operation type is timed separately. Encapsulation and decapsulation reuse the same ephemeral key, and decapsulation repeats the last ciphertext; this is a microbenchmark, not a realistic protocol workload. The reported median is the upper middle sorted batch mean and p95 is the nearest-rank value, both across **batch means**, not individual operations. Key generation and encapsulation include randomness; results include Go and timing overhead. An initial single-operation run produced zero medians due to clock resolution and was discarded.

## One observed run, 2026-10-28 UTC

Windows amd64, Go 1.27.0, `GOMAXPROCS=1`, default Go build flags, no network access in the experiment. Hardware identifiers are omitted from this public record. This computer was shared with other work; no CPU pinning or load isolation was used. Power state, memory and CPU utilization were not measured. These numbers are illustrative only and lack enough hardware detail for a direct performance comparison.

| Operation | Median batch mean | p95 batch mean |
|---|---:|---:|
| Key generation | 50.017 µs | 57.732 µs |
| Encapsulation | 39.999 µs | 48.029 µs |
| Decapsulation | 55.125 µs | 63.529 µs |

The run completed without reported errors or mismatches. Encapsulation key, ciphertext and shared-key sizes were 1,184, 1,088 and 32 bytes respectively. These are wire/data sizes, not memory usage; Go's private-key seed representation must not be confused with expanded key size. No application SLO, throughput under load, CPU consumption, memory, interoperability, side-channel behavior or end-to-end TLS latency was measured. Results do not demonstrate safety, certification, suitability for production, or a migration decision.

Next, repeat on the actual target with controlled load, a workload and SLO, record build/runtime and resource use, and separately assess interoperability. Retain unknowns until measured; do not join this result to a real inventory finding without a reviewed use case.

## Small follow-up candidates

| Order | Candidate and incremental value | Evidence and boundary |
|---|---|---|
| 1 | Add a separate structured evidence worksheet for the existing synthetic mini-service, with scope, requirement, evidence, applicability and judgment recorded separately; then request an independent human comparison. This makes the existing walkthrough independently traceable rather than adding an automatic score. | The [CAMM evaluation note](../../docs/camm-practical-evaluation.ja.md) and [saved survey](https://github.com/moruku36/independent-tech-research-notes/blob/main/surveys/security-governance/2026-camm-practical-evaluation.md) support this proposed first step. A second human is needed for actual agreement results; do not infer them or convert the lab score to CAMM. |
| 2 | Build a small synthetic temporal-scenario worksheet and boundary fixtures for below/equal/above/missing inputs, retaining alternative policy outcomes and reasons. This makes the QER ambiguity reviewable without adopting an automated priority. | The [discovery governance note](../../docs/pqc-discovery-governance.md) records the paper's inconsistent borderline example and missing aggregation policy. Explicitly agree a local policy before any operational QER automation; fixtures are not real asset risk evidence. |

The first candidate now has a [manual worksheet and author example](../../samples/mini-service-evidence-review.md), separate from this benchmark; a second reviewer is still needed. The second remains a proposal supporting the pending QER decision. Their source studies are not reproduced by either exercise.
