# Prework

**Date:** 2026-10-08
**Status:** the legal input to the S2M structure pass. Not the mapping.

Front door: [README.md](README.md).

Prework is the cut and the sum that already exist. SOB, SROB, CnOB, and SmOB cut the utterance. IdOB sums the packet. This pass does not redo that work and does not repair it.


## Dictionary sources

The dictionaries are not in `idob/`. The Python there calls them.

- Card dictionaries: `support/idob_objects/*.yaml`. `idob/registry.py` loads them and checks `support/idob_schemas/idob_object.v1.schema.json`. A fired card is the activation set on the packet.
- Relation names: `support/s2m/relations.yaml`. This is the closed list the connection writer may use. It is not a meaning dictionary.
- Known words: [../known_words.md](../known_words.md). A word not on that list is not invented into a card.

`idob/claim.py`, `idob/connections.py`, and `idob/crossing.py` are functions over the finished packet. They do not look up a meaning entry. A dictionary mapping would be a later card from a sourced structure key to a meaning entry. That card does not exist.

## Legal input

- `struct_segments` and `segment_tokens`
- `struct_roles` and `role_segments`
- `selected_ops`
- `semantic_core` fields already written: theme, state, location, copula, action, patient, speaker, recipient, relative_subject, query_focus, adverb
- the activation set, as a witness of which cards fired, not as a new relation

## Not legal input

- an earlier utterance
- a likelihood
- the geometry conjecture
- \(M\), the envelope, or \(\Delta h\)
- a word that is not on the known-word list

## A missing hat is prework

If the sentence has an object and the packet has no hat for it, the mapping does not invent the hat. *She* had to become `speaker` before a reporting connection could name her. That addition is a structure change, with a replay, before this pass may use it.

The known-word boundary remains in force: [../known_words.md](../known_words.md).
