# Independent evidence review worksheet

Use this separate manual worksheet for a scoped, synthetic review. It is not input to `pqc-scan`, does not change the review CSV, and does not produce a security certification, CAMM maturity level, or migration decision. The requirements below are local exercise checks, not official CAMM requirements. See the [filled example](../samples/mini-service-evidence-review.md) and [CAMM evaluation note](camm-practical-evaluation.ja.md).

Copy the template once per reviewer. Record independent judgments before discussion; retain both original versions and any later reconciliation separately. A second reviewer and agreement measurement have not been performed for the example. Do not enter real secrets, personal information, or unapproved deployment data.

## Scope and identity template

- Target commit and exact included paths:
- Excluded paths and activities:
- Reviewer identifier and review date:
- Scenario and limitations:

## Requirement row template

| Field | Record |
|---|---|
| Requirement ID and criterion | A stable local ID and a reviewable question; define what evidence would satisfy it. |
| Procedure and expected result | What to inspect and what would be expected. |
| Evidence reference | Exact path and finding ID where available, and date or revision. |
| Evidence type and observation | `observed` (directly inspected), `declared` (scenario claim), or `unknown`; explain what the evidence actually establishes. Multiple types can coexist. |
| Applicability and reason | `applicable`, `not applicable`, or `undetermined`; give a reason. Missing evidence alone is not `not applicable`. |
| Judgment and reason | `supported`, `not supported`, `unknown`, or `not assessed`; explain the relationship to the criterion. `supported` is scoped evidence for the criterion, not a security verdict. Use `not assessed` for a justified exclusion. |
| Next evidence action | Concrete follow-up or `none within scope`. |

Do not award points for `not applicable`, treat a declaration as an observation, or treat missing evidence as failure. Record disagreement and its reasons rather than overwriting an independent judgment. Reconciliation and any agreement statistic require at least two independently completed reviews with a defined denominator and method; neither is supplied here.
