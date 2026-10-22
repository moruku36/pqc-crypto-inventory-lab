# Evidence-linked PQC briefing / 根拠付き説明テンプレート

Copy this two-layer template for a **separately authorized** review. The filled example below uses only the [synthetic mini-service ground truth](../samples/mini-service-ground-truth.json) and [example review CSV](../samples/mini-service-review-example.csv). It is a draft for a second reviewer, not a live asset decision or evidence that a migration occurred. Replace every synthetic statement with a dated source before using it elsewhere.

## CISO and PMO page (synthetic example)

| Briefing field | Evidence-linked statement or open item |
|---|---|
| Why now | [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final) specifies ML-KEM for key establishment; [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) and [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final) specify signature algorithms. Those standards do not validate this sample service or set its migration date. |
| Scope | Only the committed [mini-service fixture](../samples/mini-service/README.md) and its [review rows F001–F006, M001–M002](../samples/mini-service-review-example.csv). `M001` and `M002` are manual additions; the [ground truth](../samples/mini-service-ground-truth.json) explains why the static scanner misses them. No runtime or supplier evidence is present. |
| Accountable owner | The example CSV labels an **exercise service team**; an accountable business owner and technical custodian remain **unknown**. [Source: example review CSV](../samples/mini-service-review-example.csv). |
| Priority questions | Confirm whether the RSA signing call `F001` runs, whether certificate `F002` is deployed, what transport group is negotiated for `F003/M001`, and how archive `M002` is wrapped. The [CSV](../samples/mini-service-review-example.csv) and [ground truth](../samples/mini-service-ground-truth.json) provide scenario context, not operational proof. |
| Open unknowns | Real use, data confidentiality lifetime, migration lead time, supplier and client compatibility, ownership, and threat scenario remain **unknown**. The [offline walkthrough](offline-review-exercise.md) records why the P1–P3 heuristic cannot resolve these. |
| Next decision and date | **Decision pending; date unknown.** A real owner would first assign evidence gathering and a review date. Do not replace this unknown with a claimed NIST deadline; [NIST standards](references.md) and [project triage](../README.md#read-results-safely) serve different purposes. |
| Review | **Second reviewer pending.** Ask the reviewer to follow each linked source, challenge scenario declarations, and record corrections before distribution. |

## Engineer checklist (same synthetic example)

| Existing review field | Check and record | Linked example |
|---|---|---|
| `finding_id`, `path`, `algorithm`, `scanner_status` | Match each claim to a row. Preserve `NOT_DETECTED` manual rows; do not turn a configuration hit into runtime proof. | [F003 and M001](../samples/mini-service-review-example.csv) |
| `owner`, `purpose` | Ask who is accountable and what the crypto actually does; keep unconfirmed roles marked declared or unknown. | [F001 purpose](../samples/mini-service-review-example.csv) |
| `runtime_state`, `verification_source` | Identify a dated runtime or deployment source before changing a scenario declaration to observed. | [F002 certificate](../samples/mini-service-review-example.csv) |
| `data_retention_years`, `exposure` | Check data lifetime and public reachability separately; inspect public-key wrapping before making a PQC claim about AES. | [M002 and F004/F005](../samples/mini-service-review-example.csv), [ground truth](../samples/mini-service-ground-truth.json) |
| `next_action` | Record a testable next evidence action, owner and review date in the private working copy. Keep migration decisions separate from evidence gathering. | [Review workflow](review-workflow.md) |

The CSV schema and scanner are unchanged. A private working copy may contain sensitive paths or operational details; review it before sharing. The template's use classes and lead times are manual notes in the [offline walkthrough](offline-review-exercise.md), not new CSV fields.

## 日本語の使い方

上段は意思決定者向けに「理由・範囲・責任者・不明点・次の判断日」をまとめ、下段は現行 CSV の列から根拠を追う技術者向け確認表です。例は合成データだけで、第二評価者の確認も実環境の証拠も未実施です。実案件では根拠の日付・範囲・責任者を確認し、不明を推測で埋めないでください。
