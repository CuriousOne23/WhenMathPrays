# IdOB core — what `idob.py` is

**Slide:** `11_idob_core/`  
**Module:** `idob.py`  
**Status:** Realization revision + keepers from `primitives/idob/idob.py` (first-pass Δh, write-boundary, complete vs eligible, identity residual, `process(tp)` adapter). Still not Path A product IdOB.  
**Read this file** to implement, review, or extend `idob.py` in a new conversation. You do not need the 20.xx routing stack or the 7-feature identity table.

---

## 1. Purpose

Path A / IdOB is an unproven theory of structure → speaker **intended-projection** stand-in. This module runs **one hop** so that theory is visible and expandable by YAML.

`idob.py` is an **orchestrator**. It does not tokenize English (Slide 09). It does not invent groups. It does not route the next IdOB (RB / Slide 10). It does not walk the primitive's formation…closure table as meaning.

Duck test: does one run make the crossing **visible and replayable**?

Two entries:

| Function | Use |
|----------|-----|
| `run_hop(...)` | Bench / learning. Returns `idob_packet`. |
| `process(tp, ...)` | Path A-shaped adapter. Calls `run_hop`, writes packet under `tp["idob"]`, **must not** mutate `process.routing_filter`. |

---

## 2. Risk vs Slide 07 and vs primitive `idob.py`

| Slide 07 | Slide 11 | `primitives/idob/idob.py` |
|----------|----------|---------------------------|
| Teaching wire of 01–06 | Realization kernel of the **crossing** | Identity-basin operator on a TP |
| Feel the print | `run_hop` + `process` | 7 categorical features, L1/Κ |

**Risk:** 11 grows into full Path A, or copies the 7-axis table over physicality…spatiality.  
**Rule:** six consequence axes stay meaning. Primitive keepers are **flags and boundaries**, not a second meaning geometry. 07 teaches. Neither folder implements TR / CTP / RB / OuBA.

---

## 3. What was absorbed from the primitive (and what was not)

| Keeper | How 11 uses it |
|--------|----------------|
| First-pass Δh | `first_meaning_cycle`; `meaning_semantics_before` = zeros if no `prior_M` |
| Write-boundary | `routing_filter_mutated` must stay false; `process` restores routing_filter if touched |
| Two flags | `ready_for_ouba` = birth; `path_b_eligible` = birth and no card residue; `idob_complete` = eligible and meaning_stable |
| Identity residual | `identity_residual.{magnitude,pattern}` — hold messiness, **not** `residue_code` |
| Hold lifecycle | `hold_geometry` default `formation` on birth. Not a meaning axis. No 10-state machine this revision. |
| `process(tp)` | Adapter only. Crossing stays in `run_hop`. |

**Not absorbed:** GEOMETRY_MAP … BASIN_MAP as meaning; L1/Κ=27; hardcoded `_apply_transition`; `idob_next_ob_candidates: ["idob"]` as routing.

---

## 4. Algorithm (`run_hop`)

1. **Card or utterance** — as before (01 card or 09 assign). Miss → null M, status unassigned/partial. No invented IDs.
2. **Key** — six IDs, meaning-blind. CIE must not change it.
3. **Map** — 03 set. Empty → `empty_map`, no M.
4. **Rank** — only mapped ids.
5. **Birth M0** — 02 `group_dimensions`.
6. **CIE** — \(M' = M + \alpha I\). Clip default True.
7. **Before-vector (primitive keeper)**  
   - If caller passed `prior_M`: `first_meaning_cycle=False`, before = that vector.  
   - Else: `first_meaning_cycle=True`, before = zeros (six axes).  
   `meaning_delta_h = ||M' − before||_2`  
   `meaning_cie_delta = ||M' − M0||_2`  
   `identity_delta = ||α I||_2`
8. **Freeze label** — `meaning_stable` if Δh < ε else `one_pass_complete`.
9. **Card residue** stays. **Identity residual** filled from miss/leftover (see §6). `hold_geometry='formation'` on birth.
10. **Flags** — see §7.
11. **Slide 10 hint** — `expand_target`; `next_key` never invented.
12. Return packet. Replay: same inputs → same packet.

Utterance-only path this revision: 09 can assign IDs; map is still keyed by `card_id`, so status is `empty_map` until a map row exists. That is a miss, not a silent birth.

---

## 5. What `idob.py` must not do

- Parse English except via 09.  
- Write physicality from the utterance.  
- Add a group the map forbade.  
- Change `structural_key` when CIE changes.  
- Invent `next_key` or write RB / `routing_filter`.  
- Treat `ready_for_ouba` as truth/OuBA work.  
- Replace six axes with the primitive 7-feature layout.  
- Load TR / CTP / RTU.

---

## 6. `identity_residual` vs `residue_code`

| Field | What |
|-------|------|
| `residue_code` | Talk-shape leftover on the **card** (Slide 10 / next key). |
| `identity_residual` | How messy the **hold** still is after this hop. |

This revision (hand, named):

| Situation | magnitude | pattern |
|-----------|-----------|---------|
| unassigned / partial | small | unassigned |
| empty_map | medium | empty_map |
| `residue_code` set after birth | medium | leftover |
| birth and no `residue_code` | small | collapsed |
| no birth other | none | none |

Do not derive next six IDs from these strings.

---

## 7. Flags

| Flag | True when |
|------|-----------|
| `ready_for_ouba` | `selected_group_id` is set (birth). |
| `path_b_eligible` | birth **and** `residue_code` is null. |
| `idob_complete` | `path_b_eligible` **and** `resolution_status == meaning_stable`. |
| `routing_filter_mutated` | must stay false. |

`ready_for_ouba` is **not** complete. Complete is not RB.

---

## 8. Fields read

| Source | Fields |
|--------|--------|
| Caller `run_hop` | `card_id` xor `utterance`; `packs_loaded`; `cie_id`; `clip_to_unit`; `epsilon`; optional `prior_M` |
| Caller `process` | a TP dict; optional same kwargs; must not require routing writes |
| `01_structure/structure_card.examples.yaml` | six IDs, `residue_code`, tags, `card_id` |
| `09_structure_assignment/assign.py` | six IDs, assignment_status, packs, residue |
| `03_map_lookup/struct_to_meaning_map.slide.yaml` | candidates by `card_id` |
| `02_meaning_groups/meaning_groups.slide.yaml` | `group_dimensions` |
| `04_ranking/ranking_weights.slide.yaml` | toy scores |
| `05_cie/cie.examples.yaml` + `modulate.py` | α, I, \(M'=M+α I\) |
| `lib/hash_toy.py`, `lib/vector6.py` | key, L2 |
| `10_residue_expand/expand.py` | hint only |

---

## 9. Fields written (`idob_packet`)

See `packet.schema.yaml`. Always emit every key.

Six-axis order: physicality, sociality, temporality, intentionality, materiality, spatiality.

`meaning_delta_h` is instrument motion from **before** (zeros on first cycle, or `prior_M`) to **M'**. That is the primitive first-pass rule on the bench geometry. `meaning_cie_delta` is CIE-only motion so the shove stays visible when first-pass Δh is large.

`process(tp)` additionally writes:

- `tp["idob"]` ← packet  
- `tp["semantic"]["meaning_delta_h"]` ← packet delta  
- never a new `process.routing_filter`

---

## 10. How it is structured / supportable / extensible

- Crossing logic lives in `run_hop`.  
- Tables live in slides 01–05 / 09 / 10. Do not fork `idob.py` to add English or groups.  
- New first-pass / flag / residual rule = named revision + this md + `packet.schema.yaml` + `tests_walls.py`.  
- Laptop: dict lookup. Working set = loaded YAML.  
- Hold-geometry state machine, if added later, is a CIE-adjacent table — not new meaning axes.

---

## 11. Tests (`tests_walls.py`)

Previous walls, plus:

- First pass: `first_meaning_cycle` True, `meaning_semantics_before` is zeros.  
- With `prior_M`: first_meaning_cycle False.  
- Birth + residue_code → `path_b_eligible` False.  
- Birth + no residue + small Δh → may be complete (neutral CIE vs zeros is **not** small; complete may be false on first pass — that is correct).  
- `process` does not change an existing `process.routing_filter`.  
- `routing_filter_mutated` is False.  
- `identity_residual` present; not equal to `residue_code`.

---

## 12. Run

    python run_11_idob_core.py
    python tests_walls.py

Driver: `RUN_11_IDOB_CORE` in `run_ts_struc2mn.py`.
