# Claim backlog status

**Date:** 2026-10-01

**Pointer (2026-10-08):** this table matches the closer branch account. Action has no cue on `main`. Comprehensive status: [program/ready_line.md](program/ready_line.md).
  
**Call:** `run_pathA_short` on current `main`. Debugger `pathA_dbug.py` also rendered the request line from a runner log.

The table is not fully implemented. Ten rows print an op. One does not.

| Row | Sentence | Runner result |
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
| Action | *The cat chased the mouse.* | no cue, no op |

*The sky is blue.* prints no op.

Action is not a missing stamp. The form writes one noun circle and no action cue, so no card can claim it. That row leaves the backlog only when the Structural Observation Block writes the verb circle. `modifier_resolution` still prints beside any non-empty cue list.
