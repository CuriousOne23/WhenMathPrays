# Residue expand — leftover tension after one IdOB hop

**Slide:** `10_residue_expand/`  
**Status:** First revision. Hand table. Not RB. Not automatic next-key.  
**Read this file for this subject.** Path A routing specs (20.50 RB, 20.37 TR, 20.145 CTP, 20.30.005 RTU, 20.40 OB lineup, 20.105 TP) are background. You do not need them to run or extend this slide.

---

## 1. Purpose

One IdOB crossing can birth a meaning-object **and still leave talk-shape tension**. That leftover is **residue**. This slide makes the leftover visible and names **which file a person expands** so the next hop can digest it.

Goals:

- See undigested residue instead of pretending the hop finished meaning.
- Expand by **hand** from leftover + a toy history of this hop (key, empty map or not, residue code).
- Keep recursion **controlled**: serial next hop is a human-written row or a stop; parallel multi-IdOB is not implemented here.
- If we cannot digest, replay of these fields tells us **what to touch**, not a new geometry.

This is a research-vehicle protocol, not a product router.

---

## 2. What this slide is / is not

| This slide is | This slide is not |
|---------------|-------------------|
| A leftover ledger + expand recipe | Automatic `residue →` six IDs |
| Manual digestion support | RB (`firing_order`, fan-out) |
| Pointer to 02 / 03 / 04 / 05 / 09 / this YAML | TR, CTP, RTU implementation |
| Visibility into why search should continue or stop | A claim that meaning was fully digested |

IdOB (slides 02–07) instantiates **this** projection.  
Residue marks **unfinished tension**.  
RB (Path A, not this folder) would later choose the **next** IdOB.  
Until that table exists in Path A, **you** write the next row here.

---

## 3. Feel (short)

Map opened legal doors for **this** key. Rank birthed one M. CIE may have shoved M. Cycle may have frozen.

If a residue code is still on the card, or the map was empty, or assignment never produced six IDs — the hop did not eat that leftover. Looking at the leftover + hop facts tells you which **book** to add a line to.

---

## 4. Algorithm (this revision)

1. Take a structure card (Slide 01) and its map row (Slide 03). Optional: assignment status from Slide 09.
2. Classify **after_status** (see §6). Do not invent IDs.
3. Look up `residue_next.examples.yaml` by `(residue_code, after_status)` when possible; else by `after_status` with `residue_code: null`; else `unknown_residue`.
4. Print: digested or not, `expand_target`, `next_key` (null unless a human already wrote a suggestion), note.
5. Stop. Do not run map, rank, CIE, or hasher. Do not write packs.

Same inputs → same print (replay).

---

## 5. Fields this slide creates / prints

These are **lesson packet** fields (toy TP slice). They are not a full 20.105 TP.

| Field | Meaning |
|-------|--------|
| `card_id` | Which structure card this hop used |
| `structural_key` | Fingerprint of six IDs (from Slide 01 hasher). Unchanged here. |
| `residue_code` | Named leftover on the card, or null |
| `map_empty` | True if Slide 03 candidates are `[]` |
| `after_status` | Classifier: `unassigned` \| `empty_map` \| `leftover_after_map` \| `digested_stop` \| `unknown_residue` |
| `digested` | Boolean: this hop has no leftover this slide cares about |
| `expand_target` | Which folder/file a human should edit, or `stop` |
| `next_key` | Optional suggested next `SK|…`. **null unless written by hand.** Never generated. |
| `note` | Why |

**Not created here:** physicality…spatiality, `final_rank_order`, `M'`, `meaning_delta_h`, RB filter, CTP history row. Those stay on their slides. A full Path A CTP row would *copy* residue and RB proposal; this slide only teaches the copy-worthy leftover.

---

## 6. How after_status is decided

| after_status | When |
|--------------|------|
| `unassigned` | No six IDs / no key (Slide 09 miss). |
| `empty_map` | Key exists, candidate list empty (`S_unmapped`). |
| `leftover_after_map` | Key exists, map may be non-empty, `residue_code` is set (rock burst). |
| `digested_stop` | Key exists, map non-empty, `residue_code` is null. |
| `unknown_residue` | A residue_code not in the hand table. |

Priority if several could apply: `unassigned` > `unknown_residue` (if code present but not tabled) > `empty_map` > `leftover_after_map` > `digested_stop`.

---

## 7. What to expand (manual digestion)

| You see | Touch |
|---------|--------|
| `unassigned` | `09_structure_assignment/packs/` (cues) |
| `empty_map` | `03_map_lookup` map row; maybe `02_meaning_groups` new prototype |
| Rank always wrong but map right | `04_ranking` weights |
| Hold wrong, key unchanged | `05_cie` envelope |
| Leftover code, map already legal | **this** `residue_next.examples.yaml` — name leftover; optionally write `next_key` by hand |
| Pack on disk not loaded | assignment / pack list (09), not IdOB |
| `digested_stop` | nothing; hop is done for this slide |

You may also add a map row **and** a residue row. Smallest legal edit first. Named revision if the machine rule changes, not if you add a teaching row.

---

## 8. How to expand *this* table

Add a YAML row:

```yaml
- residue_code: my_new_leftover
  after_status: leftover_after_map
  digested: false
  expand_target: 10_residue_expand/residue_next.examples.yaml
  next_key: null   # or SK|a|b|c|d|e|f if you already chose the next road by hand
  note: "why this leftover still lives"
```

Rules:

- Do not invent `next_key` in code.
- Do not put meaning floats in this file.
- Do not treat `next_key` as executed IdOB.
- Unknown leftover → new row here first, then maybe 03/09.

---

## 9. Serial and parallel (controlled search)

**Serial (this revision supports the *idea*):**  
one hop → leftover visible → human row → next run with that card/key.  
Path A would insert TR → CTP → RB between hops. This slide does not.

**Parallel:** not implemented. Several leftovers at once would be several rows / several keys. Do not blend M vectors. Path A CTP v1 also does not collect multi-IdOB outputs.

**Stop conditions this slide understands:** digested_stop; or undigested + you choose not to add a row (named halt: leftover logged, search not continued).

---

## 10. Do / don't

**Do:** keep miss visible; log residue; expand the smallest file; replay.

**Don't:** auto-fill six IDs from residue; add a group the map forbade from this slide; let rank leftovers mean RB next; write CIE into the key; load Path A routing primitives into this folder.

---

## 11. Tests

| Case | Expect |
|------|--------|
| S_rock_burst | leftover_after_map, undigested, target this YAML, next_key null |
| S_unmapped | empty_map, undigested, target 03 |
| S_deadline_friday | digested_stop, target stop |
| S_sleepy | digested_stop (no residue_code on card) |
| Fake residue `unknown_code` | unknown_residue, target this YAML |
| Replay | same print |
| Output | no six meaning floats |

---

## 12. Relation to other slides (captions only)

- 01: card may carry `residue_code`.  
- 02–05: this hop's inventory, door, winner, hold. They do not choose the next IdOB.  
- 06–07: freeze / packet; leftover should still be visible on the packet.  
- 08: witness — can you say which file to expand?  
- 09: miss → expand packs, not this table first.

---

## 13. Run

    python run_10_residue_expand.py
