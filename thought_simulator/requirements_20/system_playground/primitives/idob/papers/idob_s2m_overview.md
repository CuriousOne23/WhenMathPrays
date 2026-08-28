# IdOB structure-to-meaning — live overview

Merged purpose for the hop that `primitives/idob/idob.py` actually runs.  
Alphabet essays (`appxA`–`appxAB`) are not this document.

Canonical long form:  
`testbenches/idob_structure_to_meaning/idob_s2m_theory.md`  
`testbenches/idob_structure_to_meaning/idob_s2m_constructs.md`  
`testbenches/idob_structure_to_meaning/11_idob_core/idob_core.md`

---

## 1. Purpose

IdOB is a **research hop**, not a product mind. It opens a door onto speaker-projected meaning so the projection can be named, stored, differenced, and replayed.

- **Utterance** = carrier string. Not meaning.
- **Structure** = six integer IDs + `structural_key` (landscape / road).
- **Meaning** = six-axis stand-in \(M\) of the speaker’s **intended projection** (not listener uptake, not psycho-analysis of the speaker).
- **CIE** = identity/stance **pressure** on that stand-in: \(M' = M + \alpha I\).
- **Δh** = instrument motion \(\|M_i - M_{i-1}\|\) after CIE. First hop uses a zero before-vector.

Visibility test: duck test — does the packet let you see a key, a legal group set, a vector, a leftover? Not: “does this machine cognize?”

---

## 2. Two geometries (do not trade names)

| | Structure | Meaning |
|--|-----------|---------|
| Kind | Combinatorial landscape (IDs + key) | Vector in \([0,1]^6\) |
| Question | What road is this utterance on? | What intended-projection object is proposed? |
| Born from | 09 assignment or a hand card | Map + rank + group prototype + CIE |
| Illegal mix | Meaning floats on a structure card | Structure IDs inside \(M\) |

---

## 3. Hop (what idob.py does)

1. Resolve card or run 09 on the utterance + packs.  
2. Miss → `unassigned`, no \(M\), residue for Slide 10. Utterance still recorded.  
3. Key → map (legal `group_id`s only). Empty map → no birth.  
4. Rank orders **only** that set.  
5. Winner prototype → \(M\).  
6. CIE modulates \(M \to M'\). Key unchanged.  
7. Δh vs prior (or zeros).  
8. Flags: `ready_for_ouba`, `path_b_eligible`, `idob_complete`.  
9. No write to `process.routing_filter` or DCB `geometric_state`. Next IdOB is **RB**, not this hop.

---

## 4. I/O names (live)

**In:** `utterance`, `card_id` (optional), `packs_loaded`, `cie_id`, `prior_M` / last packet, TP with optional `process.routing_filter` (must survive).

**Out (`tp.idob` + root flags):**  
`utterance`, `card_id`, `assignment_status`, `structural_key`, six IDs, `residue_code`, `identity_residual`, `candidate_group_ids`, `final_rank_order`, `selected_group_id`, `meaning_semantics`, `meaning_semantics_prime`, `meaning_delta_h`, `meaning_cie_delta`, `first_meaning_cycle`, `hold_geometry`, `resolution_status`, three flags, `routing_filter_mutated`, `expand_target`.

Schema: `11_idob_core/packet.schema.yaml` and `primitives/idob/idob_s2m_packet.yaml`.

---

## 5. What this hop is not

Not listener meaning. Not a completeness proof of six axes. Not automatic recursive search (Slide 10 + RB). Not the 10-state identity walk.
