# Optional performance evidence / 任意の性能証拠台帳

This manual companion template does not alter scanner output or the agility score. A small offline ML-KEM experiment is recorded in [the experiment](../experiments/mlkem/README.md); it is not a deployment measurement. Never infer CPU cost or migration risk from an algorithm name alone.

| Field | Synthetic/blank example | Rule |
|---|---|---|
| Linked finding and purpose | `F001`, synthetic document signing | Trace to [review example](../samples/mini-service-review-example.csv); confirm real use separately |
| Baseline / candidate operation | RSA sign / proposed ML-DSA sign | Candidate only; interoperability and parameter set unknown |
| Library/version, CPU/runtime, build flags, concurrency | Unknown | Record exact versions and host only when authorized and measured |
| Latency distribution, throughput, CPU, memory, failures | Unknown | Never fill from static detections or kernel-only results |
| Application SLO, supplier constraints, evidence source/date | Unknown | Distinguish measured, declared, inferred and unknown for each value |
| Reviewer and decision | Pending | Keep performance, correctness, constant-time and side-channel evidence separate |

For a later authorized offline CPU experiment, fix the library version, operation and parameter set, CPU/runtime, build flags, concurrency and workload. Warm up, repeat runs, report distributions and failures, and compare with the application's own requirement. Measure key generation, signing, verification and key establishment separately when supported. Kernel time alone does not predict end-to-end TLS latency. No external TLS load test or hardware purchase is part of this plan.

## Research background and later decisions

[Liao, Adegbija and Lysecky, *Accelerating Post-Quantum Cryptography via LLM-Driven Hardware-Software Co-Design*](https://arxiv.org/html/2602.09410v1), reviewed 2026-10-13, compares individual FALCON reference-code kernels, including Cortex-A53 profiling and ZCU104/Vitis HLS 2023.2 work. Its reported up-to-2.6× comparison is kernel-level, not end-to-end TLS acceleration. Source-only hotspot rankings diverged from profiling; constant-time and leakage verification remain open. These paper observations do not establish a hardware requirement for all PQC deployments or prove that Nitro Enclaves or CloudHSM are PQC accelerators.

| Priority | Proposed investigation | Condition before claiming progress |
|---|---|---|
| P1 | Manual CPU benchmark using a maintained library on the actual target CPU | Fixed workload, versions and build; warm-up, repeated runs, distributions and failures. No external TLS load test starts automatically |
| P2 | Join inventory ownership and use to benchmark evidence, application SLOs and supplier constraints | Measured headroom and unknowns shown separately; consider software optimization and capacity before offload |
| P2 | Optionally compare source-only with profile-guided hotspot suggestions from a local model | Held-out measurements and function references; disclose model, quantization and prompt. Advice remains unverified |
| P3 | Explore one FPGA kernel only after an application limit has been measured | Compare latency, throughput, area/power, transfer and integration overhead; functional, constant-time and side-channel checks remain separate |

Actual target hardware, provider support, performance and leakage properties remain unverified in this lab. No production cryptographic implementation follows from this plan.

## 日本語

これは手入力の記録様式で、数値はすべて未測定です。方式名から CPU 負荷や性能上の危険を推測しません。実測・申告・推論・不明を各項目で区別し、アプリの要件と供給者の制約を確認した後に判断します。
