# PQC discovery: from findings to accountable decisions

[English](pqc-discovery-governance.md) | [日本語](pqc-discovery-governance.ja.md)

## For people and PMO

An inventory becomes useful when each finding has evidence, an accountable owner and a next decision. This paper supports improving the lab's human review workflow before expanding scanning. The smallest next step is a manual exercise using the existing synthetic service: record unknowns, separate evidence gathering from migration decisions, and check whether another reviewer can trace every conclusion. This document proposes that exercise; it does not report its execution or reproduce the paper's study.

## Source and scope

- Jelena Zelenovic, Leila Taghizadeh, Edoardo Pena-Gonzalez, Jaime Gómez García and Bart Preneel, *Post-Quantum Discovery as a Governance Capability: Evidence-Based Cryptographic Visibility and Exposure Prioritisation in a Critical Service Provider*.
- [arXiv abstract](https://arxiv.org/abs/2605.16549v1), [full text, v1](https://arxiv.org/pdf/2605.16549v1), [DOI](https://doi.org/10.48550/arXiv.2605.16549).
- Version: v1, submitted 2026-05-15 18:46:15 UTC. Reviewed: 2026-10-12 UTC, all 17 PDF pages including tables and references. arXiv lists a Eurocrypt 2026 poster presentation; this is a case-study preprint, not a certification or scanner benchmark.
- The repository saves an original reading note and versioned source links, rather than redistributing the PDF. No correspondence addresses or nonpublic organizational records are included.

## Study conditions, claims and limitations

Sections 3–5 describe static discovery, runtime telemetry and dependency mapping feeding a Quantum Exposure Register (QER), enriched with ownership, confidence and planning assumptions. The anonymised European organization spans logistics, identity, finance and payments. Section 8 reports a 14-month discovery effort across 148 environments, 24,350 endpoints and 87,200 certificates; approximately 68% RSA and 32% ECC, unclear custodians for about 40% of cryptographic assets, and 12 time-exposed critical services, under 3% of the portfolio. These are author-reported observations. Certificate, endpoint, asset and portfolio counts have different denominators and cannot be treated as coverage or detection-accuracy measures.

The authors argue that discovery should recur as a governance control, with accountable actions and supplier dependencies, rather than remain a one-time list. Section 7 acknowledges a single regulated organization, anonymised data, vendor-neutral tooling and uncertain quantum timelines. Tool versions, raw estate data, detailed sampling, accuracy measurements and controlled comparisons are not supplied sufficiently to reproduce discovery performance or quantify causal improvements. The paper's statement that combining static and dynamic evidence reduces errors is not accompanied by a measured error-rate comparison.

## Model review before reuse

Equation (1), PDF p. 6, marks confidentiality exposure when `T_shelf + T_migration > T_threat`. The 8-year horizon on p. 9 is a planning scenario, not a prediction. Retention is only an input to establishing confidentiality requirements; signing and long-lived authentication need their own integrity/trust assessment.

Equation (2), p. 12, proposes `0.4 × criticality + 0.4 × time exposure + 0.2 × evidence penalty`, with criticality and exposure coded 1–3 and evidence penalty High=0, Medium=1, Low=2. Weak evidence raises priority to investigate; it does not establish exposure. Its weights and Table 2 wave thresholds are organization-specific. The lab's [0–100 agility score](scoring.md) and P1–P3 report triage are separate heuristics; neither converts to this model's 1–5 agility scale or Wave 1–4.

Reviewer observations requiring resolution before automation:

- Table 1, p. 11, calls QER-010 (8+3>8) Borderline and QER-006 (7+1=8) No; no numerical Borderline rule is specified. Equality and missing inputs need an explicit local policy.
- QER-007 has high criticality, Yes exposure and Low confidence: Eq. (2) yields 2.8 (Table 2 Wave 1), while Table 1 assigns Wave 2. Governance overrides may explain this, but an asset-level override reason is not provided.
- The C/I/A triple is reduced to a scalar without a general aggregation rule. The worked KYC example chooses 3. Section cross-references/numbering and some bibliography pointers are inconsistent; use PDF page and equation/table identifiers to locate claims.

## Mapping to this inventory lab

| Paper concept | Existing lab support | Gap / proposed manual treatment |
|---|---|---|
| Technical discovery evidence | Directory paths, lines, algorithms and confidence | Detection confidence is not runtime-use assurance; preserve the reason and scope |
| Runtime/dependency evidence | Separate TLS snapshot; reviewer `verification_source` | No automatic TLS-to-directory join, full estate telemetry or supplier dependency graph |
| Accountability and context | `owner`, `purpose`, `runtime_state` | Distinguish accountable business role and technical custodian in a companion note |
| Temporal exposure | `data_retention_years`, `exposure` | Add confidentiality justification, migration estimate and threat scenario manually; `exposure` currently describes reachability/context, not Eq. (1) |
| Confidence and action | `verification_source`, `next_action`; static/declared/unknown scoring | Keep source, observation date, uncertainty and decision separately; do not infer QER confidence from a label |
| Refreshable decisions | `compare` evidence changes | Evidence removal is not deployment success; record review date and decision rationale |

## Smallest next validation (proposed, offline)

Use the committed [review example](../samples/mini-service-review-example.csv) and [ground truth](../samples/mini-service-ground-truth.json). No new scan, crypto change or vendor contact is necessary. Select signing, transport, stored-data and retired-code cases. In a private companion worksheet record service ID, linked finding/path, evidence source/date/scope, observed versus declared versus unknown state, accountable role, technical role, C/I/A rationale, confidentiality and integrity lifetime rationale, migration estimate/range, supplier constraint, threat scenario/date, separate temporal result, next evidence action and next decision date. These are proposed manual fields, not implemented CSV columns.

1. Include the undetected transport/archive cases and keep multiple findings for one service traceable. The synthetic 12-year retention is a scenario declaration, not verified confidentiality or proof that AES itself needs PQC replacement; inspect public-key wrapping and transport dependencies separately.
2. Use explicit synthetic assumptions to check below/equal/above boundaries and missing values. Keep missing inputs Unknown; document any Borderline policy before using it. Vary a scenario horizon and migration estimate without claiming a CRQC arrival date.
3. Give weak evidence an investigation action even when no migration wave can be justified. Keep a retired SHA-1 finding as an unverified-use question, with classical collision risk distinct from PQC.
4. Have a second reviewer trace sources and explain each decision. Accept only if every decision is traceable, all manual/unknown entries remain visible, no static signal is presented as runtime proof and every override has a reason. Otherwise revise the worksheet before considering implementation.

PMO can then review open owner assignments, unresolved evidence and supplier blockers, with denominators defined for the exercise. Benefits and effort savings remain hypotheses until measured. This update changes documentation only; the QER, formulas and workflow extensions are not implemented.
