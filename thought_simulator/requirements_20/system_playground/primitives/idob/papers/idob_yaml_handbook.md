# IdOB YAML handbook

How to read, change, and extend the tables IdOB depends on.  
If a change is not listed as OK, treat it as a **new machine revision** (requirements + code), not a silent edit.

Live copies of structure dictionaries: **`primitives/idob/semantic_*.yaml`**.  
`papers/semantic_*.yaml` are snapshots. Edit the primitives copies.

11 currently loads **slide** YAML under `testbenches/idob_structure_to_meaning/` (01–05, 09–10). Promoting production tables means pointing those loaders at the files in this handbook without renaming fields.

---

## 1. Structure dictionaries (six IDs)

These assign **integers that become the structural key**. They do not hold meaning scores.

| File | Field on the card | Why it exists |
|------|-------------------|---------------|
| `semantic_field_definitions.yaml` | `semantic_field_id` | Coarse topic basin |
| `semantic_roles_dictionary.yaml` | `semantic_role_id` | Role in the talk-shape |
| `semantic_objects.yaml` | `semantic_object_id` | Object slot |
| `semantic_gradients.yaml` | `gradient_id` | Dynamic vs static (etc.) |
| `semantic_universe_dictionary.yaml` | `universe_id` | Which inventory |
| `semantic_subfields.yaml` | `subfield_id` | Fine bin; `0` = none |

**Note:** the checked-in `semantic_field_definitions.yaml` still *names* lifecycle envelope keys (identity, stance, geometry…). That is **legacy naming inside a structure file**. Slide 01 cards use numeric field ids (`12`, `101`, `401`, `999`). When you extend for 09, add **numeric ids + gloss + example phrases**. Do not put `physicality` floats here.

### Record shape (target)

```yaml
entries:
  - id: 12
    gloss: physical-event basin (toy)
    examples: ["The rock burst open."]
```

### OK
- New unused integer id + gloss + examples.
- New pack file that *uses* these ids (`09_structure_assignment/packs/*.yaml`).
- Marking an id deprecated (keep the number; do not reuse).

### Not OK
- Reuse an id for a different gloss.
- Six-axis scores in these files.
- Deleting an id that any card or map still cites.
- Changing an id that already minted keys without a named revision.

---

## 2. Slide / production meaning tables

| File | Role |
|------|------|
| `02_meaning_groups/meaning_groups.slide.yaml` and `papers/structure_to_meaning/meaning_groups.yaml` | Prototypes: `group_id` + six floats + optional nested score bags |
| `03_map_lookup/struct_to_meaning_map.slide.yaml` and `structure_to_meaning/struct_to_meaning_map.yaml` | Door: key or `card_id` → legal `group_id` set |
| `04_ranking/ranking_weights.slide.yaml` | Order among **legal** candidates only |
| `05_cie/cie.examples.yaml` | Stance vectors \(I\) and \(\alpha\) |
| `09_structure_assignment/assignment.schema.yaml` + `packs/` | Utterance → six IDs |
| `10_residue_expand/residue_next.examples.yaml` | Leftover → human expand hint (not auto next six-tuple) |
| `11_idob_core/packet.schema.yaml` | Hop I/O |
| `structure_to_meaning/idob_meaning_dictionary.yaml` | Nested unit lexicon (optional; 11 may ignore units) |
| `structure_to_meaning/idob_object.yaml` | Example object blob |

### OK
- New `group_id` + six floats in range + gloss; add the id only to map rows that should see it.
- New map row: `card_id` or `structural_key` + list of existing group ids (empty list legal).
- New CIE row: `cie_id`, `I` length 6 in \([0,1]\), `alpha`.
- New pack cue that writes existing structure ids.
- New residue code + expand hint row.

### Not OK
- Rank mentioning a `group_id` absent from that key’s map.
- Map pointing at a missing group.
- CIE that rewrites the structural key.
- Pack cue that writes meaning floats.
- Treating list order in the map as rank.

---

## 3. Lifecycle YAML (sibling, not hop tables)

| File | Role |
|------|------|
| `primitives/idob/idob_schema.yaml` | formation…closure enums |
| `path_a/identity/idob_lifecycle_archive.yaml` | Ten utterances |
| `idob_s2m_packet.yaml` | Pointer at the live packet |

Do not add lifecycle geometry enums to `packet.schema.yaml` as if they were axes of \(M\).

---

## 4. How to know a change is OK

1. Structure file still has **no** meaning floats.  
2. Every `group_id` on a map row exists in meaning_groups.  
3. Rank ⊆ map for every key you care about.  
4. A replay of the same utterance + packs + CIE + prior_M yields the same packet.  
5. `routing_filter` on a fixture TP is unchanged after `process`.  
6. Miss still stores the utterance.

If (4) or (5) break, you changed the machine — bump the revision, do not hide it in a dictionary.

---

## 5. Packs and “all English”

Horizon is architectural: SSD can hold packs; RAM holds the loaded subset. Triggers may later load a dialect pack. Today: list packs in `packs_loaded`. Handbook change for a new dialect is a new YAML file in `09/.../packs/`, not a new IdOB class.
