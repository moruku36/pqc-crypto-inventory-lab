# Offline review exercise / オフライン確認演習

This worked walkthrough uses only the committed [synthetic ground truth](../samples/mini-service-ground-truth.json) and [example review CSV](../samples/mini-service-review-example.csv). It is an author walkthrough, not a second independent review or a runtime test. The proposed review fields stay outside the CSV schema.

| Service question | Existing evidence | Use class / lead time | Investigation order versus report heuristic |
|---|---|---|---|
| Document signatures | `F001`, RSA call in `app/signing.py`; scenario declares active use | Signature/authentication; lead time **unknown** | Report would flag quantum-vulnerable RSA for P2. Confirm callers, verifier compatibility and supplier support before scheduling migration. |
| Transport key establishment | `F003`, X25519 config; `M001`, undetected Python dictionary | Confidentiality in transit; retention and lead time **unknown** | P2 on the detected X25519, while `M001` is absent from automatic triage. Resolve runtime negotiation and data lifetime; do not claim TLS group from the config. |
| Stored archive | `M002`, synthetic 12-year retention declaration; AES settings `F004`/`F005` cannot be mapped to data | Long-lived confidentiality is a **scenario hypothesis**; lead time **unknown** | The heuristic gives AES P3 and misses `M002`. Investigate wrapping keys and access paths; AES itself is not thereby a PQC replacement target. |
| Retired signer | `F006`, SHA-1 call; scenario declares unused | Signature/authentication; lead time **unknown** | Heuristic P1 for classical collision review. Confirm reachability before a retirement decision; this is separate from quantum exposure. |

**Observed difference:** static P1–P3 order does not represent undetected cases, real runtime use, retention needs or supplier lead time. The manual notes add questions, not a new risk score or a CRQC date. All scenario declarations and unknowns remain visible. A second reviewer and real operational evidence are still needed before a migration decision. [Review workflow](review-workflow.md) and [PQC discovery note](pqc-discovery-governance.md) explain the unresolved QER model choices.

## 日本語

上表は合成シナリオの申告とスキャナーの静的検出を分けた記入例です。`M001`・`M002` は自動検出されず、保持期間 12 年も演習上の申告です。用途分類と移行期間は手作業の補足で、現在の CSV 列・P1～P3・採点を変更しません。第二評価者による独立判断、実際の稼働状況、供給者対応は未確認です。
