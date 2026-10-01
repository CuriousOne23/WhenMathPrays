# Path A coverage map

**Document:** `notes/pathA_coverage.md`  
**Date:** 2026-10-01  
**Status:** base. May gain rows. The cuts below stay.  
**Does not define tokens.** Authorities: [idob_seam.md](../architecture/idob_seam.md), [idob_object_space.md](idob_object_space/idob_object_space.md), [IdOB_unified_plan.md](../architecture/IdOB_unified_plan.md), [idob_meaning_lock.md](../architecture/idob_meaning_lock.md).

## Purpose

This page is the current development-target map for Path A short sim. Open it to say developed, next, or hole. Other files define the tokens and hold the catalogs. This page names the lists, defines each row, and links out. It does not copy those catalogs.

A hole names a list and a row. "Path A does not cover *and*" is not a verdict. "Form list has coordination. Claim backlog still holds it" is a verdict.

## What this page covers

The desks that write the signed form and the card: Structural Observation Block (SOB), Structural Refinement Observation Block (SROB), Constraint Observation Block (CnOB), Semantic Observation Block (SmOB), Identity Observation Block (IdOB). Output Binding / Assemble (OuBA) is named only as the lock on the card. Truth-Relation Update (TRU) is named only where a mood hint must not clobber the card.

That span is the IdOB meaning hop: structure to `idob_packet`. It is not Structure-to-Meaning (S2M).

## What this page does not cover

Intake, correction, and routing are upstream. They are not scored. Meaning Composition Block (MCB) is omitted in the short sim. No second IdOB sum. No embeddings.

S2M is recorded and not scored. See the shut door. This page does not create a dictionary for \(M\).

## Status words

Used only here.

| Word | Means |
|---|---|
| developed | The row exists and a replay can show it. |
| unclaimed | The form already has the cue. No stamp prints the line. |
| form hole | The signed form has no circle, hat, fit, or cue for the shape. |
| shut | Named, empty, not a coverage hole in the four lists. |

"Coverage is good" means the family list replays and the claim-backlog row you care about is no longer unclaimed. "Not good" names the list and the row.

New facts get a row on the list that owns them. They do not become a sixth list because a sentence felt new. A new list requires a sentence on this page saying why the four could not hold it.

## Family list

**Definition.** Sentence shapes the short-sim pipeline already runs end to end: SOB through IdOB. Not the stretch list.

**Authority.** [pathA_supported_sentences.md](pathA_supported_sentences.md).

| Row | Definition | Status | Example |
|---|---|---|---|
| Copular / state | Property or identity of a theme. Hats: theme, state. | developed | *The sky is blue.* |
| Locative | Place of a theme. Hats: theme, location. | developed | *The book is on the table.* |
| Mixed descriptive | Nested modifier or place chain on a descriptive. | developed | *The rain in Spain stays mainly in the plain.* |
| Interrogative | Wh or yes/no question over a descriptive shape. | developed | *Where is the book?* |
| Mixed interrogative | Question scope over a nested descriptive. Overlap, not a seventh stamp family. | developed | *Where is the book that is on the table?* |

A hole on this list is a shape with no family at all. Coordination is not that hole.

## Form list

**Definition.** What the structure desks can write on the signed form before any stamp fires. Circles (SOB), hats (SROB), fits (CnOB), cues (SmOB and CnOB notes). A claim cannot own a note the form does not have.

**Authority.** Exerciser holes in [pathA_supported_sentences.md](pathA_supported_sentences.md). Primitive cards under `debug/primitives/`.

| Row | What is written | Status | Note |
|---|---|---|---|
| Entity and complement circles | *the book*, *on the table*, *blue* | developed | SOB |
| Hats | theme, state, location, query focus | developed | SROB. A hat is not a stamp. |
| Locative and copular fits | combination may close | developed | CnOB |
| Scene cue | pieces in one picture | developed | SmOB. Basin adjacency, not object adjacency. |
| Negation cue | denied state | developed as a cue | *The sky is not blue.* |
| Command cue | bare imperative | developed as a cue | *Close the door.* |
| Request cue | polite imperative, distinct from bare command | developed as a cue | *Please close the door.* |
| Coordination cue | two clauses joined | developed as a cue | *and the lamp is on the desk* |
| Conditional cue | one clause depends on another | developed as a cue | *If the book is on the table, ...* |
| Fragment cue | place or piece with a missing hat | developed as a cue | *On the table.* |
| Speaker cue | first person | developed as a cue | *I am tired.* |
| Passive cue | acted-on | developed as a cue | *The book was written.* |
| Quantifier cue | how much of the theme | developed as a cue | *Every sky is blue.* |
| Exclamative cue | force that is not a question | developed as a cue | *What a beautiful day!* |
| Reporting circle | "she said that..." | form hole | No circle yet. |
| Recipient hat | *Give me the book.* | form hole | No recipient hat yet. |
| Relative subject that is not the head | *The book that John bought* | form hole | Relative clause whose subject is not the book. |

A form-list row can be developed and still sit on the claim backlog. The cue is written. The line is not printed.

## Stamp list

**Definition.** The IdOBObject drawer. One card is a named spec that may wake and print claim lines. It is not the book, not the packet, not S2M. This is the dictionary Path A has.

**Authority.** [idob_object_space.md](idob_object_space/idob_object_space.md). Files under `support/idob_objects/`. On-switches are empty in YAML (`activation: {}`). Apply still lives in `idob.legacy`.

| Card | Family on the card | May print | Status |
|---|---|---|---|
| `copular_state` | `copular_state` | theme, state | developed as a card; switch not data |
| `locative` | `locative` | location | developed as a card; switch not data |
| `mixed_descriptive` | `mixed_descriptive` | theme, state, location | developed as a card; switch not data |
| `interrogative_wh` | `interrogative_wh` | query_focus, predicate | developed as a card; switch not data |
| `interrogative_polar` | `interrogative_polar` | query_focus, predicate | developed as a card; switch not data |
| `agent_action` | `residual_identity` | agent, action, patient | weak row: helper filed as residual |
| `modifier_resolution` | `mixed_descriptive` | theme, state, location, relation, action, patient | helper; not a second type system |
| `residual_identity` | `residual_identity` | none declared | developed as the leftover card |

A hole on this list is a force no current card may honestly print. Bare command is the clearest candidate. Do not pretend it into `copular_state`.

## Claim backlog

**Definition.** Cues on the form list that no stamp prints. The stretch list. A claim is one row: an on-switch for that cue, and the line the stamp may write. A row leaves only when the packet prints the line and the family list does not move.

Not a dictionary. Not more facts about the book. Not S2M.

| Row | Sentence | Cue present | Line the card drops | Card that should own it | Status |
|---|---|---|---|---|---|
| Negation | *The sky is not blue.* | negation | denied, not only blue | `copular_state` | unclaimed |
| Bare command | *Close the door.* | command | command force | no honest card yet | unclaimed |
| Request | *Please close the door.* | request | request, distinct from bare command | no honest card yet | unclaimed |
| Coordination | *The book is on the table and the lamp is on the desk.* | coordination | two place-claims, joined | `locative`, twice, with a join recorded | unclaimed |
| Conditional | *If the book is on the table, the lamp is in the hall.* | conditional | one claim depends on the other | `locative`, with a dependency line | unclaimed |
| Fragment | *On the table.* | fragment | place with the thing missing | `locative`, theme absent on purpose | unclaimed |
| Speaker | *I am tired.* | speaker | who the theme is | `copular_state` | unclaimed |
| Passive | *The book was written.* | passive | acted-on; by-phrase still open | `agent_action` | unclaimed |
| Quantifier | *Every sky is blue.* | quantifier | how much of the theme | `copular_state` | unclaimed |
| Exclamative | *What a beautiful day!* | exclamative | force that is not a question | no honest card yet; TRU must not call it a question by default | unclaimed |
| Action | *The cat chased the mouse.* | action shape, if the form has it | agent, action, patient | `agent_action`; stop calling the result residual if the packet is an action claim | unclaimed |

Current development targets, in order: negation (smallest stretch), then coordination (the *and* join), then bare command (clearest missing force). Do not open a new family for a row whose card already exists.

## Shut door

**Definition.** S2M. The later hop. Not a coverage list. Not a second name for the meaning hop.

**Authority.** [idob_meaning_lock.md](../architecture/idob_meaning_lock.md). Reserved packet shape, not written by the short sim: `primitives/idob/idob_s2m_packet.yaml`.

| Reading | What it is | Status |
|---|---|---|
| \(M\) | `meaning_semantics`: a six-axis coordinate, or null. A point, not a card. | shut |
| Envelope | \(M' = M + \alpha I\). `meaning_semantics_prime`, `meaning_cie_delta`. A shove, not a drawer. | shut |
| \(\Delta h\) | `meaning_delta_h`. Step size between coordinates. Not Path A `meaning_delta`. | shut |

Research note: a surface is implied and not drawn. A dictionary of named regions is not required and not forbidden. We do not know enough to say a drawer will follow or will not. Do not open a blank catalog that looks like the stamp list.

Product note: Path A short sim does not compute \(M\). Do not add a second YAML drawer in this folder. `identity_geometry` on the packet is not the envelope.

Next door, after this map: define the space those readings sit in, then ask whether any region is worth a name. Not a row on the stamp list.

## How a miss looks

No circle: form hole. Cue present, no line: claim backlog. No card may print the force: stamp-list hole. Shape with no family: family-list hole. Packet complete and you want a coordinate: shut door.
