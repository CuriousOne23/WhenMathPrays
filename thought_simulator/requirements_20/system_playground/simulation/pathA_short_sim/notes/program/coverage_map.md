# Path A conversational coverage map

**Date:** 2026-10-08
**Status:** roadmap. Not a proof that Path A is complete.

Door: [../../README.md](../../README.md). Status: [status.md](status.md).

## Why this page exists

Path A will be criticized because this work has no settled outside result. The answer is not that the theory is finished. The answer is a map. A critic can point at a hole. The hole is already named.

Human conversation space is the territory. Path A coverage space is the owner and the evidence. Completeness here means the map is known.

## Status words

| Status | Meaning |
|---|---|
| `covered` | A short-sim replay already accounts for this form. |
| `absent` | Present-only, and not tested. |
| `unsupported` | Tested, and the packet could not account for it without invention. |
| `unknown` | No realization yet. Historical rows stay here until a later owner is exercised. |

A check without a replay is not `covered`.

## Present-only

These forms use the current utterance only. History is not an input.

| Form | Owner | Status | Evidence |
|---|---|---|---|
| Assertion / state | SOB, SROB, CnOB, SmOB, IdOB | covered | claim ledger |
| Location | SOB, SROB, CnOB, SmOB, IdOB | covered | claim ledger |
| Action | SOB, SROB, CnOB, SmOB, IdOB | covered | claim ledger |
| Transfer | SOB, SROB, CnOB, SmOB, IdOB | covered | *Give me the book.* |
| Question | SOB, SROB, CnOB, SmOB, IdOB | covered | *Where is the book?* Query against statement is unplaced, not an ID. |
| Command | SOB, SROB, CnOB, SmOB, IdOB | covered | *Close the door.* |
| Request | SOB, SROB, CnOB, SmOB, IdOB | covered | *Please close the door.* |
| Reporting | SOB, SROB, CnOB, SmOB, IdOB | covered | *She said the book is on the table.* Speaker against theme is unplaced, not an ID. |
| Relative clause | SOB, SROB, CnOB, SmOB, IdOB | covered | *The book that John bought.* |
| Negation | unassigned | absent | not tested |
| Modality | unassigned | absent | not tested |
| Comparison | unassigned | absent | not tested |
| Causation | unassigned | absent | not tested |
| Conditional | unassigned | absent | not tested |
| Commitment | unassigned | absent | not tested |
| Expressive | unassigned | absent | not tested |

## Historical

History is on the map and out of the present sim. Owners are COB, CST, CIL, and CEx. IE and CE may feed them. The short sim does not import these rows.

| Form | Owner | Status |
|---|---|---|
| Historical reference | COB, CST, CIL, CEx | unknown |
| Answer to an earlier question | COB, CST, CIL, CEx | unknown |
| Multi-turn correction | COB, CST, CIL, CEx | unknown |
| Accumulated common ground | COB, CST, CIL, CEx | unknown |

## How a row changes

An extension is a new row, or a status change after a replay. `absent` becomes `covered` only when a replay exists. One absent form is the next development, chosen explicitly. This page does not add that sentence.
