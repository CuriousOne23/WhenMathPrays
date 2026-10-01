# Path A coverage map

**Document:** `notes/pathA_coverage.md`  
**Date:** 2026-10-01  
**Status:** base, with an account of the claim pass. May gain rows. The cuts below stay.  
**Meter:** 43% used when this account was written.  
**Does not define tokens.** Authorities: [idob_seam.md](../architecture/idob_seam.md), [idob_object_space.md](idob_object_space/idob_object_space.md), [IdOB_unified_plan.md](../architecture/IdOB_unified_plan.md), [idob_meaning_lock.md](../architecture/idob_meaning_lock.md).

## Purpose

This page is the current development-target map for Path A short sim. Open it to say developed, wired, hole, or shut. Other files define the tokens. This page does not copy those catalogs.

## What this page covers

Structural Observation Block through Identity Observation Block, then Output Binding / Assemble as the lock on the card. That span is the IdOB meaning hop. It is not Structure-to-Meaning (S2M).

## What this page does not cover

Intake, correction, and routing are not scored. Meaning Composition Block is omitted. S2M is recorded and not scored.

## Status words

| Word | Means |
|---|---|
| developed | The row exists and a full runner replay can show it. |
| wired | The stamp prints the op when the cue is already on a stand-in packet. Full runner replay not run. |
| stamp hole | The form has the cue. No honest card may print the force. |
| form hole | The signed form has no circle or hat for the shape. |
| shut | Named, empty, not a hole in the four lists. |

## Family list

Five shapes, developed: copular, locative, mixed descriptive, interrogative, mixed interrogative. Authority: [pathA_supported_sentences.md](pathA_supported_sentences.md).

## Form list

Cues for negation, command, request, coordination, conditional, fragment, speaker, passive, quantifier, and exclamative are developed as cues. Three form holes remain: reporting circle (*She said the book is on the table.*), recipient hat (*Give me the book.*), relative subject that is not the head (*The book that John bought*).

## Stamp list

Eight cards, plus a proposed `imperative` card not on `main` at this writing. On-switches are still empty in YAML. Apply still lives in code.

| Card | Status |
|---|---|
| `copular_state` | developed as a card; negation, speaker, quantifier wired |
| `locative` | developed as a card; coordination, conditional, fragment wired |
| `mixed_descriptive` | developed as a card |
| `interrogative_wh` | developed as a card; must not own exclamative |
| `interrogative_polar` | developed as a card |
| `agent_action` | weak row; passive wired; family still `residual_identity` |
| `modifier_resolution` | helper |
| `residual_identity` | leftover card |
| `imperative` | not on `main`; proposed for command and request |

## Claim backlog

| Row | Sentence | Status | Where |
|---|---|---|---|
| Negation | *The sky is not blue.* | wired | `negated_state` on `copular_state` |
| Coordination | *The book is on the table and the lamp is on the desk.* | wired | `coordinated_clauses` on `locative` |
| Conditional | *If the book is on the table, the lamp is in the hall.* | wired | `conditional_clauses` on `locative` |
| Fragment | *On the table.* | wired | `fragment_ellipsis` on `locative` |
| Speaker | *I am tired.* | wired | `first_person_speaker` on `copular_state` |
| Passive | *The book was written.* | wired | `passive_voice` on `agent_action`; by-phrase still open |
| Quantifier | *Every sky is blue.* | wired | `quantified_np` on `copular_state` |
| Action | *The cat chased the mouse.* | wired as an op | `agent_action` already prints; family still residual |
| Bare command | *Close the door.* | stamp hole | no honest card on `main` |
| Request | *Please close the door.* | stamp hole | distinct from bare command |
| Exclamative | *What a beautiful day!* | stamp hole | not a question card |

Wired means a stand-in replay of `_build_selected_ops`: the op prints when the cue is present, and *The sky is blue.* does not gain it. `modifier_resolution` also prints whenever any cue list is non-empty. That is old behavior.

## Shut door

\(M\), the envelope \(M' = M + \alpha I\), and \(\Delta h\) are shut. A surface is implied and not drawn. A dictionary is not required and not forbidden. Path A short sim does not compute \(M\).

## Next

Full runner replay of the wired rows. Then one imperative card with two lines, if pull request 97 is accepted. Then the three form holes. Not the shut door.
