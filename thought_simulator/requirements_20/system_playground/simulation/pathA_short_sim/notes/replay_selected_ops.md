# Replay — selected ops only

**Date:** 2026-10-01  
**Meter:** 40% used when this note was written.  
**Scope:** `_build_selected_ops` on a stand-in packet. Not a full runner pass. Not Structure-to-Meaning (S2M).

Plain stand-in, no cues and no rules, printed `[]`.

| Stand-in | Cue or rule present | Ops printed |
|---|---|---|
| *The sky is blue.* | none | none |
| *The sky is not blue.* | `negated_state`, `negation_scope_rule` | `negated_state`, `modifier_resolution` |
| coordination | `coordinated_clauses`, `coordination_composition_rule` | `coordinated_clauses`, `modifier_resolution` |
| conditional | `conditional_clauses`, `conditional_composition_rule` | `conditional_clauses`, `modifier_resolution` |
| fragment | `fragment_ellipsis`, `fragment_ellipsis_rule` | `fragment_ellipsis`, `modifier_resolution` |
| speaker | `first_person_speaker`, `first_person_state_rule` | `first_person_speaker`, `modifier_resolution` |
| passive | `passive_voice_clause`, `passive_voice_rule` | `passive_voice`, `modifier_resolution` |
| quantifier | `quantified_np`, `quantifier_scope_rule` | `quantified_np`, `modifier_resolution` |

`modifier_resolution` prints whenever any cue list is non-empty. That is existing behavior, not a new claim.

This does not prove the full pipeline writes those cues. It proves the stamp side prints the op once the cue is already there, and does not print it when the cue is absent.
