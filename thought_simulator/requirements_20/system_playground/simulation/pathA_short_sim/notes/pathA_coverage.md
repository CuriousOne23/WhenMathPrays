# Path A coverage map

**Document:** `notes/pathA_coverage.md`  
**Date:** 2026-10-01  
**Status:** claim backlog prints on the runner. Form holes remain.

**Program (2026-10-08):** [program/README.md](program/README.md) is the status account. The action row below that says *The cat chased the mouse.* already prints `agent_action` on `main` is superseded by [action_row_runner.md](action_row_runner.md): that verb circle was seen locally and was not uploaded. Do not treat that row as landed. Next structural write remains the three form holes, then the ready line, not S2M.
  
**Does not define tokens.** Authorities: [idob_seam.md](../architecture/idob_seam.md), [idob_object_space.md](idob_object_space/idob_object_space.md), [IdOB_unified_plan.md](../architecture/IdOB_unified_plan.md), [idob_meaning_lock.md](../architecture/idob_meaning_lock.md).

## Purpose

This page is the current development-target map for Path A short sim. Open it to say printed, hole, or shut.

## What this page covers

Structural Observation Block through Identity Observation Block, then Output Binding / Assemble as the lock on the card. That span is the IdOB meaning hop. It is not Structure-to-Meaning (S2M).

## What this page does not cover

Intake, correction, and routing are not scored. Meaning Composition Block is omitted. S2M is recorded and not scored.

## Status words

| Word | Means |
|---|---|
| printed | A runner pass writes the cue and `selected_ops` shows the line. `pathA_dbug.py` can render that log. |
| form hole | The signed form has no circle or hat for the shape. |
| shut | Named, empty, not a hole in the four lists. |

## Family list

Five shapes, printed: copular, locative, mixed descriptive, interrogative, mixed interrogative. Authority: [pathA_supported_sentences.md](pathA_supported_sentences.md).

## Form list

Cues for negation, command, request, coordination, conditional, fragment, speaker, passive, quantifier, exclamative, and action are printed as cues. Three form holes remain: reporting circle (*She said the book is on the table.*), recipient hat (*Give me the book.*), relative subject that is not the head (*The book that John bought*).

## Stamp list

Eight original cards, plus `imperative` and `exclamative`. Those two are filed `residual_identity` because the family enum has no force family yet. `agent_action` is still filed residual. On-switches are still empty in YAML.

## Claim backlog

Printed on `run_pathA_short`. *The sky is blue.* prints no extra op.

| Row | Sentence | Line |
|---|---|---|
| Negation | *The sky is not blue.* | `negated_state` |
| Coordination | *The book is on the table and the lamp is on the desk.* | `coordinated_clauses` |
| Conditional | *If the book is on the table, the lamp is in the hall.* | `conditional_clauses` |
| Fragment | *On the table.* | `fragment_ellipsis` |
| Speaker | *I am tired.* | `first_person_speaker` |
| Passive | *The book was written.* | `passive_voice` |
| Quantifier | *Every sky is blue.* | `quantified_np` |
| Bare command | *Close the door.* | `bare_command` |
| Request | *Please close the door.* | `polite_request` |
| Exclamative | *What a beautiful day!* | `exclamative_force` |
| Action | *The cat chased the mouse.* | `agent_action` |

Action circles are `NP VP NP`. The verb set is `chased`, `chase`, `chases`, `bought`, `buy`, `wrote`, `write`. `pathA_dbug.py` rendered `action_clause` and `agent_action` from a runner log for that sentence. Exit was clean.

`modifier_resolution` still prints beside any non-empty cue list. Old helper.

## Shut door

\(M\), the envelope \(M' = M + \alpha I\), and \(\Delta h\) are shut. A surface is implied and not drawn. A dictionary is not required and not forbidden. Path A short sim does not compute \(M\).

## Next

The three form holes. Not a new stamp. Not the shut door.
