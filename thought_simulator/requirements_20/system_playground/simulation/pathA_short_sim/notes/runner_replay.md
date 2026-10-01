# Runner replay

**Date:** 2026-10-01  
**Meter:** 44% used when this note was written.  
**Call:** `run_pathA_short` on the short-sim runner. Not Structure-to-Meaning (S2M).

| Sentence | Cues written | Rules written | `selected_ops` |
|---|---|---|---|
| *The sky is blue.* | none | `structural_rule` | none |
| *The sky is not blue.* | `negated_state` | `negation_scope_rule` | `negated_state`, `modifier_resolution` |
| *On the table.* | `fragment_ellipsis` | `fragment_ellipsis_rule` | `fragment_ellipsis`, `modifier_resolution` |
| *I am tired.* | `first_person_speaker` | `first_person_state_rule` | `first_person_speaker`, `modifier_resolution` |
| *Every sky is blue.* | `quantified_np` | `quantifier_scope_rule` | `quantified_np`, `modifier_resolution` |
| *The book was written.* | `passive_voice_clause` | `passive_voice_rule` | `passive_voice`, `modifier_resolution` |
| *Close the door.* | `imperative_voice_clause` | `imperative_voice_rule` | `modifier_resolution` only |
| *Please close the door.* | `request_imperative_clause` | `request_imperative_rule` | `modifier_resolution` only |

The form writes the command and request cues. No stamp prints those forces. That is the stamp hole, confirmed on the runner, not only on a stand-in.

`modifier_resolution` prints whenever a cue list is non-empty. Old behavior.
