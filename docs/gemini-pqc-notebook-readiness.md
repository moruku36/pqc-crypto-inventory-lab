# Google's PQC Gemini Notebook: what it means for crypto inventory and migration priorities

[English](gemini-pqc-notebook-readiness.md) | [日本語](gemini-pqc-notebook-readiness.ja.md)

## For CISOs and PMO

Google Cloud has published a public, AI-assisted primer for post-quantum cryptography (PQC). It helps leaders get up to speed; it does not find cryptography in your systems. This lab does the second job. The smallest useful step is to put the two side by side: use the primer to explain *why* to start, and use an evidence-based inventory to show *where* and *in what order*. This note records what the official sources state, then proposes how the lab could use them. The proposals are not implemented.

## Source and scope

- Stephanie Kiel (Head of Cloud Security Policy, Government Affairs and Public Policy, Google Cloud), [*Cloud CISO Perspectives: New Gemini Notebook can help CISOs and policymakers prepare for PQC*](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-new-gemini-notebook-can-help-cisos-policymakers-prepare-for-pqc), Google Cloud Blog.
- Published: 2026-10-14 (date shown on the page). Reviewed: 2026-10-18 (JST). The article is a newsletter-style post; the notebook itself is a separate resource.
- **Not verified:** the notebook page ([link from the article](https://notebook.google.com/notebook/68849586-67c5-4165-8f72-64a61991f1dd)) could not be retrieved by the automated reader used for this review. Its actual source list, answers, flashcards, audio overview and diagram were **not inspected**. Everything below about the notebook comes from the article's description only. Nothing is inferred from the notebook's name.
- This note is an original summary and analysis, not a reproduction of the article.

### Linked primary sources checked

| Source | What was checked | Date / version |
|---|---|---|
| [Google, *Quantum frontiers may be closer than they appear*](https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/) (Heather Adkins, Sophie Schmieg) | Google's 2029 migration timeline; threat framing for encryption versus signatures | Published 2026-03-25; reviewed 2026-10-18 |
| [Gidney, *How to factor 2048 bit RSA integers with less than a million noisy qubits*](https://arxiv.org/abs/2505.15917) | Abstract: RSA-2048 estimate and its assumptions | arXiv v1, submitted 2025-05-21; reviewed 2026-10-18 |
| [Babbush et al., *Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities*](https://arxiv.org/abs/2603.28846) | Abstract: 256-bit ECDLP estimate and its assumptions | arXiv v2 (2026-04-15; v1 submitted 2026-03-30); reviewed 2026-10-18 |
| [Google Cloud, *Why PQC is the next Y2K, and what you can do about it*](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-prepare-early-for-PQC-resilient-cryptographic-threats) (Christiane Peters) | Four preparation steps that the 2026 article refers back to | Published 2025-02-28; reviewed 2026-10-18 |

Only abstracts and article text were read for the two arXiv papers; their full text, circuits and proofs were not reviewed. The other links in the article (Chrome, Android, Cloud KMS, the Wiz scanner, the PQC Alliance and so on) were not followed.

## What the official sources state

**About the notebook (article's description).**

- It is a public Gemini Notebook named *Prepare for Post-Quantum Cryptography*, bringing together Google's PQC research, engineering blogs and migration guidance.
- Listed features: answers grounded in Google's sources, a podcast-style audio overview, flashcards, an interactive visual diagram of the quantum threat, and a concise briefing document.
- The article offers sample prompts for CISOs, newcomers and developers, and warns that, like all generative AI, the notebook can make mistakes, so answers should be checked against the linked sources.
- It also gives four steps for building a similar notebook for your own team: curate trusted sources, write neutral prompts, add AI disclaimers and a welcome note, and have experts review all output before sharing.

**About the threat and timeline (article, with the cross-checks above).**

- The article says Google research puts the cost of breaking ECDLP-256 and RSA-2048 at around 500,000 and 1 million noisy qubits respectively. The abstracts of the two linked papers are consistent in order of magnitude, but they state specific assumptions (for RSA-2048: a square qubit grid, 0.1% gate error, 1 µs surface-code cycle, 10 µs control reaction time, runtime under a week; for ECDLP-256: superconducting-type hardware with 10⁻³ physical error and planar connectivity, under half a million physical qubits). These are estimates, not statements that such a machine exists or when it will.
- The article describes store-now-decrypt-later attacks as a reason to act on data that must stay confidential for a long time, and says Google plans to transition to PQC by 2029 and urges others to consider the same. The March 2026 Google post adds that the threat to encryption is relevant today, while the signature threat requires transition *before* a cryptographically relevant quantum computer (CRQC), and that Google adjusted its threat model to prioritize migration of authentication services.
- The 2029 date is Google's own plan, not a standard or regulatory deadline.

**About CISO actions (article).** Start by understanding where vulnerable cryptography lives; identify and prioritize the data and systems most at risk and make a plan; anticipate system-wide effects of migration; build crypto-agility using lessons from earlier incidents. The article points to the 2025 post for detail. That post also lists the systems to examine (asymmetric encryption and key exchange, PKI and other signatures, software and firmware signing, authentication) and notes that, for most organizations, the longer-run risk is how long migration takes. The 2025 post also says that, unless an organization holds very long-lived sensitive data or has an architecture where a few keys unlock past traffic, neither harvest-now-decrypt-later nor signature forgery is as serious as some claim. The 2026 article puts more emphasis on data already being at risk. Both are Google's positions; read them together rather than picking one.

## Mapping to this lab (proposals, not official claims)

Everything in this section and below is **our proposal** for the lab. The sources above do not mention this project.

| Google's CISO step (article) | Existing lab support | Gap / proposed treatment |
|---|---|---|
| Understand where vulnerable cryptography lives | `directory` and `tls` inventory; reviewer `owner`, `purpose`, `runtime_state` | Coverage is limited (see README scope). Zero findings is not proof of absence |
| Identify and prioritize data and systems at risk | P1–P3 triage; `data_retention_years`, `exposure` | Add a manual "use class" note (below) so long-lived confidentiality and signature or authentication uses are not mixed |
| Anticipate system-wide effects | Not covered | Record manually: larger keys or signatures, protocol limits, supplier support, storage formats |
| Build crypto-agility | 0–100 agility score (heuristic) | Keep separate; the score is neither NIST's nor Google's measure |

### Proposed prioritization lens (manual, offline)

For each finding, a reviewer could add two notes in a private companion worksheet. These are not implemented CSV columns.

1. **Use class:** *confidentiality of data that must stay secret for years*, versus *signature or authentication use* (for example code signing, certificates, firmware). The sources above treat these differently: the first is exposed to store-now-decrypt-later, while the second must be migrated before a CRQC exists.
2. **Migration lead time:** an estimate or range with its basis (supplier support, release cycle, device update path), marked as measured, declared, inferred or unknown.

These notes would inform *investigation order*. They would not change the existing P1–P3 triage or the agility score, and they do not predict a CRQC date.

## Where this helps, and where it does not

**Possible uses.**

- *CISO and PMO briefings:* the article's four steps give a recognizable framing, and the notebook (if it behaves as described) may help non-specialists ask questions before a first meeting.
- *Engineer onboarding:* the same framing can be tied to the lab's sample output so readers see what an inventory finding looks like.
- *Making the lab's own primer:* the article's four-step recipe is compatible with this repository's habit of keeping source links and human review.

**Limits.**

- The notebook is a reading aid grounded in Google's chosen sources. It does not scan, measure or know anything about your environment, and it cannot replace an evidence-based inventory.
- Its source set is described as Google-curated. Treat it as one perspective alongside NIST publications ([references](references.md)) and your own suppliers' statements.
- Generative answers can be wrong; the article says so. How accurate this notebook is has not been tested here.
- Resource estimates depend on stated hardware assumptions and can change as research advances. They do not establish a date.
- Using or citing the notebook is not a certification, compliance or quantum-safety claim for this lab or for any system.

## Concrete next steps (proposed, not implemented)

| Priority | Proposal | Acceptance criterion |
|---|---|---|
| P1 | Add a short, docs-only **briefing template** with two layers: a CISO page (why, scope, owners, open unknowns, next decision date) and an engineer checklist mapped to existing review fields. | Every statement links to a source or a finding; unknowns stay visible; a second reviewer can trace each line. No new scanner feature or score. |
| P1 | Run an **offline exercise** on the existing synthetic mini-service: have a reviewer tag each finding with a use class and a lead-time note, then compare the resulting order with the current P1–P3 triage. | Differences are recorded with reasons. The exercise is accepted only if all manual and unknown entries stay visible and no static detection is presented as proof of runtime use. |
| P2 | Prepare a **curated source pack** for a private notebook (or any grounded Q&A tool): the sources listed in [references](references.md) plus this note's linked sources, with neutral prompts and an AI disclaimer, following the article's own four steps. | The pack lists versions and dates. Outputs are reviewed by a person before sharing. Nothing confidential is uploaded; no result is described as authoritative. |
| P2 | Hand-test the public notebook with about ten neutral questions (for example, store-now-decrypt-later, hybrid key exchange, first-90-day priorities) and compare each answer with its linked source. | Record question, answer summary, cited source and verdict. Report this as a small manual spot check, not an accuracy benchmark. Requires someone who can open the notebook. |
| P3 | Revisit whether a "use class" field belongs in the review CSV, after the exercise above. | Decide only with exercise evidence; any code change is a separate, reviewed task. |

**Status of this note at its original review:** documentation only; no scanner, scoring, CSV or CI change, and no exercise or notebook test. A later [two-layer synthetic briefing template](briefing-template.md) and [partial offline walkthrough](offline-review-exercise.md) now exist. The full each-finding exercise, independent second review, CSV-field decision and notebook test remain unperformed. See also the [human review workflow](review-workflow.md) and [source index](references.md).
