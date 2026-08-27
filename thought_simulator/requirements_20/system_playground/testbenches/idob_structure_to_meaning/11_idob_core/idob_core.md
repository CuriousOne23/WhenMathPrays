# IdOB core — what `idob.py` is

**Slide:** `11_idob_core/`  
**Module:** `idob.py`  
**Status:** First realization revision. Laptop tables. Not Path A product IdOB.  
**Read this file** to implement, review, or extend `idob.py` in a new conversation. You do not need the 20.xx routing stack.

---

## 1. Why this file exists

Path A / IdOB is an unproven theory of structure → speaker intended-projection. The bench slides (00–10) name the parts. This slide is the **thin kernel that runs one hop** so the theory can be expanded by YAML, not by rewriting architecture.

`idob.py` is an **orchestrator**. It does not tokenize English (Slide 09 does). It does not invent groups. It does not route the next IdOB (RB / Slide 10).

Duck test: does one run make the crossing **visible and replayable**?

---

## 2. Risk vs Slide 07 (do not merge jobs)

| Slide 07 `07_idob_slide/` | Slide 11 `11_idob_core/` |
|---------------------------|--------------------------|
| Teaching wire of lessons 01–06 | Realization kernel |
| Feel the full print | Same hop as a callable `run_hop` |
| Stay a slide | Stay small; consumers (TR/CTP/RB) sit **outside** |

**Risk:** 11 grows into “full Path A.” Then 07 is redundant and the kernel is no longer supportable.  
**Rule:** 07 teaches. 11 realizes one hop. Neither implements RTU / TR / CTP / RB / OuBA.

---

## 3. What `idob.py` does (algorithm)

One function: `run_hop(...)` → `idob_packet` dict.

1. **Obtain a structure card**  
   - `card_id` given → load Slide 01 card. `assignment_status = card_given`.  
   - else `utterance` given → Slide 09 `assign(utterance, packs_loaded)`.  
   - If not six IDs (`unassigned` / `partial`) → packet with null key, null M, `resolution_status` = that miss. Stop. No invented IDs.

2. **Key** — `toy_structural_key` on the six IDs. Meaning-blind. CIE must not change it later.

3. **Map** — Slide 03: `card_id` → `candidate_group_ids` (set). Empty list is legal.  
   If empty → packet with key, empty candidates, no winner, no M. `resolution_status = empty_map`. Stop.

4. **Rank** — Slide 04 toys: score **only** mapped ids. `final_rank_order` winner first. `selected_group_id` = first. Must not add an id.

5. **Birth M0** — Slide 02 `group_dimensions` of `selected_group_id`.

6. **CIE** — `05_cie/modulate.py`:  
   \(M' = M + \alpha I\)  
   `clip_to_unit` default True. Key unchanged. Neutral envelope → \(M'=M\).

7. **Deltas (this revision: one CIE step, `refinement_cycles = 1`)**  
   `meaning_delta_h = ||M' − M||` (L2 on six axes)  
   `identity_delta = ||α I||` (L2 of the shove; 0 if α=0)  
   Full 06 cycle loop is **not** required in this kernel. Adding it is a named revision.

8. **Freeze label**  
   - `meaning_stable` if `meaning_delta_h < epsilon` (default 0.05)  
   - else `one_pass_complete`  
   Budget/time statuses are reserved for a cycle revision.

9. **Residue stays visible** — copy `residue_code` from the card. Do not clear it because M was born.

10. **Expand hint (optional, read-only)** — Slide 10 classifier may fill `expand_target`. `next_key` stays null unless already in the 10 table (never generated here).

11. **Return the packet.** Same inputs → same packet (replay).

---

## 4. What `idob.py` must not do

- Parse English except by calling Slide 09.  
- Write physicality from the utterance.  
- Add a group the map forbade.  
- Change `structural_key` when CIE changes.  
- Invent `next_key` or call RB.  
- Commit OuBA / truth / belief. `ready_for_ouba` is a **flag** that a birth happened, not a truth claim.  
- Load Path A TR / CTP / RTU.

---

## 5. Fields it reads

| Source | Fields |
|--------|--------|
| Caller | `card_id` xor `utterance`; `packs_loaded`; `cie_id`; `clip_to_unit`; `epsilon` |
| `01_structure/structure_card.examples.yaml` | six IDs, `residue_code`, `feature_tags`, `card_id` |
| `09_structure_assignment/assign.py` | same six + `assignment_status`, `packs_loaded`, `residue_code` |
| `03_map_lookup/struct_to_meaning_map.slide.yaml` | `meaning_group_candidates` by `card_id` |
| `02_meaning_groups/meaning_groups.slide.yaml` | `group_id`, `group_dimensions` |
| `04_ranking/ranking_weights.slide.yaml` | `ranking_weights`, `group_toy_scores` |
| `05_cie/cie.examples.yaml` | `cie_id`, `identity_importance` (α), `identity_vector` |
| `05_cie/modulate.py` | `modulate(M, alpha, I, clip)` |
| `lib/hash_toy.py` | `toy_structural_key` |
| `lib/vector6.py` | `from_mapping`, `delta_l2`, `add_scaled` |
| `10_residue_expand/expand.py` | optional hint only |

Working-set note: this revision **points at those YAML files**. A later pack tree under `11_idob_core/packs/` may copy them; architecture stays the same.

---

## 6. Fields it outputs (`idob_packet`)

See `packet.schema.yaml`. Always emit every key. Use null / `[]` / false rather than omitting.

Meaning of the important ones:

| Field | Role |
|-------|------|
| six IDs + `structural_key` | Structure geometry fingerprint |
| `candidate_group_ids` | Map door (set) |
| `final_rank_order` / `selected_group_id` | First birth |
| `meaning_semantics` | M0 |
| `meaning_semantics_prime` | M' after CIE |
| `meaning_delta_h` | \(\|M'-M\|\) instrument motion |
| `resolution_status` | Why this hop stopped |
| `residue_code` | Leftover tension still on the card |
| `packs_loaded` | Replay of 09 |
| `expand_target` | Human file hint (Slide 10) |
| `next_key` | Always null unless 10 table already had a hand suggestion |
| `ready_for_ouba` | True iff a group was selected (handoff *possible*, not OuBA work) |

Axis order of both M vectors: physicality, sociality, temporality, intentionality, materiality, spatiality. Each in [0,1] when clipped.

---

## 7. `resolution_status` this revision

| Value | When |
|-------|------|
| `unassigned` | 09 produced no six IDs |
| `partial` | 09 filled some slots only |
| `empty_map` | Key exists, candidates `[]` |
| `meaning_stable` | Birth happened and Δh < ε |
| `one_pass_complete` | Birth happened and Δh ≥ ε (one CIE step, no cycle budget) |

Reserved later: `identity_stable`, `budget_exhausted`, `time_exhausted` (Slide 06).

---

## 8. How to expand (do not fork `idob.py`)

| Need | Touch |
|------|--------|
| More English → IDs | 09 packs |
| New prototype | 02 YAML |
| New legal door | 03 map row |
| Different first winner | 04 weights |
| New hold | 05 envelope |
| Leftover named / next suggestion | 10 table |
| Different ε or CIE formula | **named machine revision** + this md |

Collision / miss stay visible. Unloaded packs do not fire.

---

## 9. Path A around this packet (not in this folder)

TR writes `TP.TR` only. CTP freezes a TP copy + history. RB reads this view + residue addresses and proposes next OBs. RTU masks lanes.  
Those modules **consume** `idob_packet`. They do not live in `idob.py`.

---

## 10. Tests (`tests_walls.py`)

- Empty map → no `selected_group_id`, no M.  
- Rank order ⊆ map set.  
- CIE swap does not change `structural_key`.  
- 09 miss utterance → `unassigned`, no key.  
- `next_key` is null unless table provided it.  
- Replay: two `run_hop` on same card+cie equal.

---

## 11. Run

    python run_11_idob_core.py
    python tests_walls.py

Driver: `RUN_11_IDOB_CORE` in `run_ts_struc2mn.py`.
