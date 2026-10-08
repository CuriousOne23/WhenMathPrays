# Six-ID falsification pass

**Date:** 2026-10-08
**Status:** evaluation. No ID is written. Not an implementation of the six fields.

Door: [../../../README.md](../../../README.md). Status: [../status.md](../status.md). Shell: [README.md](README.md).

## Why this page exists

The six structure IDs are names in the shell. The requirement claims they locate a structure card. This pass asks whether the realized floor backs that claim, and whether the floor already makes a distinction the six do not name. It does not fill an ID.

## Verdicts

| Verdict | Meaning |
|---|---|
| `unsupported` | A question is stated. No floor field may supply the ID. |
| `missing_dimension` | No question is stated. The name does not yet measure anything in this sim. |
| `unplaced` | The floor separates two utterances. None of the six questions names that difference. |
| `separated` | Not legal in this pass. A later pass may use it only after a source is named. |
| `lacking` | Not legal in this pass. A source exists and the pair still matches. |

A null ID is not `separated`. An invented ID, an invented source, or a structural key fails the run.

## Rows

| ID | Question | Source | Verdict |
|---|---|---|---|
| `semantic_field_id` | different field? | none | `unsupported` |
| `semantic_role_id` | different hat? | none | `unsupported` |
| `semantic_object_id` | different object? | none | `unsupported` |
| `gradient_id` | none stated | none | `missing_dimension` |
| `universe_id` | none stated | none | `missing_dimension` |
| `subfield_id` | none stated | none | `missing_dimension` |

## Unplaced pairs

- *She said the book is on the table.* against *The book is on the table.* Speaker against theme. The floor has a speaker hat on the first only.
- *Where is the book?* against *The book is on the table.* Query against statement. The floor has a query focus on the first only.

If no ID question names those differences, they are `unplaced`. That challenges the six-ID set. It does not break the cut.

## Programs

- `support/tools/structure_id_eval.py` prints the six verdicts and the unplaced list. It writes no ID.
- `support/tools/structure_id_check_replay.py` fails if an ID is non-null, a key is formed, or a verdict is missing.

Replay: `PYTHONPATH=. python3 support/tools/structure_id_check_replay.py`

## First result

The guardrail passed. Field, role, and object are `unsupported`. Gradient, universe, and subfield are `missing_dimension`. Speaker against theme, and query against statement, are `unplaced`. No key was formed. No ID was written. The requirement is ahead of the cut on those two differences.
