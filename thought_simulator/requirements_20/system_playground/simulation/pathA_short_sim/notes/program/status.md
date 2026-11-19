# Path A short-sim status

**Date:** 2026-11-19  
**Door:** [../../README.md](../../README.md). This page is the account. The door points here and does not carry it.

## Current goal

Controlled category selection (sentence-internal cue or prior-CEx cue) so a non-default category can be chosen without mutating the floor.

Detail and constraints: [category_selection_proposal.md](category_selection_proposal.md).

The bots ShortSim Status and ShortSim Docs hold the account accountable to this goal. They report distance from it; they do not invent the next path or fill fields.

## Historical / accomplished

**Narrow S2M seed (accomplished 2026-11-19)**  
One minimum S2M path that makes the structure-to-meaning transition visible was realized. IdOB attaches an accountability trail (`tp.s2m_seed`) and an interpretive transfer (`tp.s2m_meaning`). Both are additive, non-mutating, and CLI-controlled. Crossing fields remain null. The seed is visible and re-runnable.

Prior wording (kept for trace):
- One existing floor distinction written from a real floor source (or explicitly left outside and recorded as such).
- The connection/hole record surfaced as a limited, still-not-\(M\) signal so a run shows which floor fields participated and which holes stayed holes.
- Every other crossing field (six IDs, structural key, rank, CIE, `meaning_delta_h`) remains null unless a floor source for that exact field already exists and the write is mechanical.

That goal is closed. Further expansion of S2M paths is not the current aim; category selection is.

## Independent views (not definitive)

Two additional views exist. Both are independent and speculative or summary; neither is a definitive conclusion and neither updates this account or the requirements.

- **ShortSim Trajectory** — speculative trajectory quality relative to the goal above (advances / neutral / drifts, with reason). Emitted to Helm. Does not replace the ShortSim Status distance report.
- **Path A Account** — larger Path A status door at [../../../../path_a_status.md](../../../../path_a_status.md). Readable summary of where Path A is, what is locked, next step, and why. Kept from drifting by its bot; does not author requirements.

Read them as second views, not as the account.

## Coverage map

Human conversation space against Path A owners. Present forms are covered or absent. History is on the map and out of the sim. [coverage_map.md](coverage_map.md).

## Current effort

Bring the short-sim packet into name and shape agreement with `20.40.050` and `20.105`. The concept already agreed. The packet did not.

IdOB writes the teaching packet into `tp.idob`. Crossing fields (six structure IDs, `structural_key`, rank, \(M\), CIE, `meaning_delta_h`) are absent from that packet. Null means absent, not born. A constructable shell that copies the sum and sets those fields to null is available via `idob/crossing.py` (`crossing_from_packet`); it is not the value the main simulator writes. Detail: [packet_sync/README.md](packet_sync/README.md) and [packet_sync/structure_ids.md](packet_sync/structure_ids.md).

This effort does not birth \(M\) and does not apply CIE.

## Six-ID falsification

The six IDs are not filled. The first run found three `unsupported`, three `missing_dimension`, and two `unplaced` floor differences: speaker against theme, and query against statement. The six-ID set does not account for distinctions the floor already makes. Detail: [packet_sync/id_eval.md](packet_sync/id_eval.md). Candidates, not new IDs: [packet_sync/unplaced.md](packet_sync/unplaced.md). Both already have floor sources. They stay outside the six.

## Narrow S2M realization

A finished packet can support accountable connections and holes. That is evidence for the Path A claim that structure can be mapped without inventing links. It is not \(M\), not history, and not the geometry conjecture.

- Definition and bounds: [s2m_structure/README.md](s2m_structure/README.md)
- What the writer showed: [s2m_structure/result.md](s2m_structure/result.md)
- Claims that print: [claim_ledger.md](claim_ledger.md)
- Words not invented: [known_words.md](known_words.md)
- Geometry note, not imported: [../conjectures/meaning_geometry_conjecture.md](../conjectures/meaning_geometry_conjecture.md)

## What is implemented

- Structure floor: SOB, SROB, CnOB, SmOB.
- IdOB sum. Teaching packet written into `tp.idob`. `idob_packet` is that same sum, not a second packet.
- Readable claim and connection record. No ranking.
- Constructable shell view (`crossing_from_packet`) that sets crossing fields to null. Not the default `tp.idob` value.
- Narrow S2M seed (accountability + interpretive transfer) attached by IdOB (see Historical / accomplished).

## What is absent

- Six structure IDs, structural key, rank, selected group.
- \(M\), CIE, `meaning_delta_h`.
- Force ops as relations. Polar, command, request, and exclamative stay holes.
- Controlled category selection (next realization).

## Requirement account

| Requirement | Implemented | Not implemented |
|---|---|---|
| `20.705` section 2 lineup | floor order and routing beside the floor | full intake through OuBA stretch |
| `20.105` TP envelope | teaching packet written to `tp.idob` | full canonical TP field catalog |
| `20.40.010`–`040` | cut writers in the short sim | full primitive contracts |
| `20.40.050` 3A | teaching packet (utterance + sum); constructable shell with null crossing fields | six IDs, key, rank, \(M\), CIE, delta on the written packet |
| `20.40.050` 3B | CIE not applied | CIE after \(M\) |
| `20.107`, `20.109` | not this sim's intake | CEx packet and IE normalization |

## Log

A short dated log. Detail stays in the linked pages. This list does not grow into a field table.

- 2026-10-08 — Structure floor and claim ledger locked. [claim_ledger.md](claim_ledger.md)
- 2026-10-08 — Narrow S2M record: connections and holes. [s2m_structure/result.md](s2m_structure/result.md)
- 2026-10-08 — Packet shell. Six IDs absent. No key. [packet_sync/structure_ids.md](packet_sync/structure_ids.md)
- 2026-10-08 — Six-ID falsification. No ID written. Two floor differences unplaced. [packet_sync/id_eval.md](packet_sync/id_eval.md)
- 2026-10-08 — Unplaced differences have floor sources and are not IDs. [packet_sync/unplaced.md](packet_sync/unplaced.md)
- 2026-10-08 — Coverage map. Present forms covered or absent. History owned by COB, CST, CIL, CEx. [coverage_map.md](coverage_map.md)
- 2026-11-19 — tp.idob description aligned with code: main run writes teaching packet; shell is constructable view via crossing_from_packet.
- 2026-11-19 — Current goal stated: one minimum visible S2M path. ShortSim Status and ShortSim Docs hold the account accountable to it.
- 2026-11-19 — Independent views added: ShortSim Trajectory (speculative quality) and Path A Account (larger door). Both labeled non-definitive.
- 2026-11-19 — Narrow S2M seed marked accomplished (historical). Current goal moved to controlled category selection. [category_selection_proposal.md](category_selection_proposal.md)
