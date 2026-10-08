# Path A conversational coverage map

**Date:** 2026-10-08
**Status:** roadmap. Not a proof that Path A is complete.

Door: [../../README.md](../../README.md). Status: [status.md](status.md).

## Why this page exists

Path A will be criticized because this work has no settled outside result. The answer is not that the theory is finished. The answer is a map. A critic can point at a hole. The hole is already named.

Human conversation space is the territory. Path A coverage space is the owner and the evidence. Roadmap completeness means every currently recognized conversational form has a named row and an explicit status. It does not mean human conversation space is exhaustively known.

The rows form a proposed and extensible inventory. They are informed by established conversational classifications, but they are not a closed or universally accepted ontology. A newly recognized conversational form is added as a named row rather than silently absorbed into an existing row.

## Status words

| Status | Meaning |
|---|---|
| `covered` | A short-sim replay already accounts for this form. |
| `absent` | Present-only, and not tested. |
| `unsupported` | Tested, and the packet could not account for it without invention. |
| `unknown` | No realization yet. Historical rows stay here until a later owner is exercised. |

A check without a replay is not `covered`. Every covered row must identify the replay or ledger row that demonstrates its coverage.

## Present-only

These forms use the current utterance only. History is not an input.

| Form | Realization path | Status | Evidence |
|---|---|---|---|
| Assertion / state | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *The sky is blue.* |
| Location | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *The book is on the table.* |
| Action | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *The cat chased the mouse.* |
| Transfer | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *Give me the book.* |
| Question | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *Where is the book?* Query against statement is unplaced, not an ID. |
| Command | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *Close the door.* |
| Request | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *Please close the door.* |
| Reporting | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *She said the book is on the table.* Speaker against theme is unplaced, not an ID. |
| Relative clause | SOB, SROB, CnOB, SmOB, IdOB | covered | `claim_ledger_replay.py`: *The book that John bought.* |
| Negation | unassigned | absent | not tested |
| Modality | unassigned | absent | not tested |
| Comparison | unassigned | absent | not tested |
| Causation | unassigned | absent | not tested |
| Conditional | unassigned | absent | not tested |
| Commitment | unassigned | absent | not tested |
| Expressive | unassigned | absent | not tested |

## Historical

History is on the map and out of the present sim. Owners are COB, CST, CIL, and CEx. IE and CE may feed them. The short sim does not import these rows.

| Form | Pipeline | Status |
|---|---|---|
| Historical reference | COB, CST, CIL, CEx | unknown |
| Answer to an earlier question | COB, CST, CIL, CEx | unknown |
| Multi-turn correction | COB, CST, CIL, CEx | unknown |
| Accumulated common ground | COB, CST, CIL, CEx | unknown |

## How a row changes

An extension is a new row, or a status change after a replay. `absent` becomes `covered` only when a replay exists. One absent form is the next development, chosen explicitly. This page does not add that sentence.

Realization path means the form passes through those writers. It is not a claim that each writer owns the distinctive capability. The decisive writer is unassigned. A later pass may name it. Partial support is not a status. A narrower form, such as simple predicate negation, gets its own row.
