# Packet sync, phase 1 — names and absence

**Date:** 2026-10-08 (updated 2026-11-19)
**Status:** name map. Teaching packet written to `tp.idob`. Constructable shell available. Not \(M\).

Program: [../README.md](../README.md). Door: [../../../README.md](../../../README.md). Requirement: `20.40.050` section 3A and `20.105`. Geometry note, not imported: [../../conjectures/meaning_geometry_conjecture.md](../../conjectures/meaning_geometry_conjecture.md).

## Why this page exists

The short sim agrees with Path A in concept. It does not agree in packet shape. This page maps the teaching names to the requirement names and writes the absences.

## Alias

`idob_packet` is a pedagogical view of the sum that IdOB writes into `tp.idob`. It is not a second packet. It does not disappear in this pass. A later requirement may retire the teaching name. Until then, both names refer to the same sum.

A later copy must be mechanical. A field may move to a requirement name only when it is the same value. No field is inferred. A connection is not \(M\). An empty list is not a rank. Zero is not `meaning_delta_h`.

## Name map

| Short sim now | Requirement name | This phase |
|---|---|---|
| teaching packet written to `tp.idob` | `tp.idob` | same sum, not a second packet |
| segments, roles, constraints, smoothing | SOB, SROB, CnOB, SmOB | floor, already named |
| connection record | not `meaning_semantics` | links and holes, not \(M\) |
| no six structure IDs | six structure IDs | absent |
| no key | `structural_key` | absent until six IDs exist |
| no rank | `final_rank_order` | absent |
| no \(M\) | `meaning_semantics` | absent, not zero, not born |
| no CIE | CIE identifiers | absent, not applied |
| no delta | `meaning_delta_h` | absent, not zero |

Null, when the constructable shell is formed, means absent. It does not mean born and empty.

## What this phase does not do

It does not invent an ID. It does not birth \(M\). It does not apply CIE. It does not rank. The teaching sum is not the crossing packet. The main simulator does not write the shell into `tp.idob`.

## Constructable shell

`idob/crossing.py` (`crossing_from_packet`) builds a shell view that copies the sum and sets the crossing fields (six IDs, key, rank, \(M\), CIE, `meaning_delta_h`, etc.) explicitly to null. Replay: [../../../support/tools/tp_idob_shell_replay.py](../../../support/tools/tp_idob_shell_replay.py). This view is available; it is not the value IdOB writes in a normal run.

Related packet-sync evaluation and replay programs (none of these write a structure ID):

- [../../../support/tools/structure_id_eval.py](../../../support/tools/structure_id_eval.py) — falsify the six structure IDs against the floor; write no ID value. Record: [id_eval.md](id_eval.md).
- [../../../support/tools/structure_id_check_replay.py](../../../support/tools/structure_id_check_replay.py) — guardrail: no invented ID, no key, no missing verdict.
- [../../../support/tools/unplaced_source_replay.py](../../../support/tools/unplaced_source_replay.py) — unplaced differences have floor sources; they are not structure IDs. Record: [unplaced.md](unplaced.md).
- [../../../support/tools/smob_residue_field_replay.py](../../../support/tools/smob_residue_field_replay.py) — SmOB residue field wiring on the short-simulator TP (`smoothing_residue`).
- [../../../support/tools/tp_idob_shell_replay.py](../../../support/tools/tp_idob_shell_replay.py) — the constructable shell copies the sum and leaves crossing fields null.

## Next

Phase 3 is the six IDs, and only if the floor already emits them.

Phase 3: the six IDs are named and absent. No key is formed. [structure_ids.md](structure_ids.md).

Falsification pass, no ID written: [id_eval.md](id_eval.md).
