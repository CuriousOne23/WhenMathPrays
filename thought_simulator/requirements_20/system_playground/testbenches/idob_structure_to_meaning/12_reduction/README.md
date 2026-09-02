# 12_reduction — Summation (Goal v2)

**Location (repo):** `thought_simulator/requirements_20/system_playground/testbenches/idob_structure_to_meaning/12_reduction/`  
**Status:** Agreement locked 2026-08-31. Harness landed (`run_12_reduction.py`, `fixtures.yaml`, `score_sheet.yaml`, `rivals/*` including `one_space.py`).  
**Does not claim:** world primitives, six-axis completeness, Path A as cognition, or a finished necessity theorem.

---

## Why this code exists

IdOB is defined as a structure→meaning hop. Saying “IdOB needs a mapping” is architectural identity, not a test.

**Goal v2:** On shared fixtures, show whether any *cheaper* operator (frame-fill, embedding nearest-prototype, dictionary lookup, plus contrast rival `one_space`) can satisfy the **five-wall package** using only its native theory and the same raw inputs.

If a cheap rival passes all walls without contamination, IdOB shrinks toward naming.  
If all three original cheap rivals fail at least one wall, uncontaminated, we have a **first conviction**: those styles cannot do the package’s work. That is not “the package is necessary in nature.” `one_space.py` is a fourth cheap rival (contrast probe) in the harness; it is not a fourth member of that first-conviction sentence.

Coverage of ordinary speech is **out of scope** for this folder.

---

## What this code is

A comparison harness, not a new meaning theory.

| Piece | Job |
|---|---|
| `idob_native` | Reference hop (`run_hop` / `process`). Allowed to use the live map. |
| `frame_fill` | Style: valid structure ⇒ licensed meaning. Always births if a card exists. |
| `embed_nn` | Style: string → nearest prototype. Always births. |
| `dict_lookup` | Style: utterance → fixed M. No structure. |
| `one_space` | Fourth cheap rival (contrast): one-space probe; see `rivals/one_space.py`. |
| `run_12_reduction.py` | Runs singles, pairs, and one cross case; scores walls; prints the verdict table. |

Cheap rivals **must not** read:

- `struct_to_meaning_map.slide.yaml`
- ranking weight tables
- meaning-group / dimensions tables
- `11_idob_core/idob.py` internals

If they do, the run is **contaminated**: not a pass, not a fail, discard.

`idob_native` is **not** a rival for the contamination rule. Map use is required for the reference.

---

## How it runs

1. Load `fixtures.yaml` (singles / pairs / cross) and `score_sheet.yaml`.
2. For each rival `run(case)`:
   - singles → W2, W3, W5, and I2 where marked
   - pairs → W1, W3, W4, W5, I1 where marked
   - `R_prior` → sanity only (native should not be first-cycle)
3. Static-check cheap modules for forbidden imports.
4. Print per-rival failed walls and the locked verdict table.
5. Stop the whole comparison if `idob_native` fails any wall (bench broken).

---

## Important constructs

**Talk-shape structure (current fact)**  
Six IDs on a card: `semantic_field_id`, `semantic_role_id`, `semantic_object_id`, `gradient_id`, `universe_id`, `subfield_id`.  
`structural_key` fingerprints those six IDs only. CIE must not enter the key.

**World primitives**  
Named revision target. Not a current claim. Do not put this phrase in runner output.

**Two geometries**  
- Structure: discrete admissibility (IDs + key).  
- Meaning: six-axis stand-in \(M \in [0,1]^6\): physicality, sociality, temporality, intentionality, materiality, spatiality.

**Map / rank / birth**  
- Map: key or card → set of legal `group_id`s. Empty set is legal.  
- Rank: order inside that set only.  
- Birth: `selected_group_id` and `meaning_semantics` both non-null.

**CIE**  
After birth: \(M' = \mathrm{clip}(M + \alpha I)\). Moves \(M\), never the key.

**Five-wall package (the novelty under test)**

1. Two-space invariant (key frozen under CIE).  
2. Empty legal birth (`S_unmapped` births nothing).  
3. Rank ⊆ map.  
4. CIE may move \(M\); must not move the key.  
5. Residue is tension, not a next six-tuple (`next_key` is always null here).

**Instruments**

- I1 Replay: identical inputs → identical scored fields.  
- I2 No routing write: `process()` leaves `routing_filter` unchanged.

---

## Variables (packet_subset)

Every `run(case)` returns exactly these keys. Nulls are legal. Do not coerce missing \(M\) to zeros except native first-cycle `before` inside the real hop (that field is **not** required on the subset).

| Key | Type | Meaning |
|---|---|---|
| `structural_key` | str or null | Fingerprint of six IDs, or null if no structure |
| `candidate_group_ids` | list[int] | Claimed legal set (may be empty) |
| `final_rank_order` | list[int] | Order inside that set |
| `selected_group_id` | int or null | Winner; null = no birth |
| `meaning_semantics` | dict[6 floats] or null | \(M\) before CIE |
| `meaning_semantics_prime` | dict[6 floats] or null | \(M'\) after CIE |
| `meaning_delta_h` | float or null | Motion instrument; may be ignored by cheap rivals |
| `residue_code` | str or null | Leftover tension flag |
| `next_key` | null | Must stay null |
| `routing_filter_mutated` | bool | True only if filter was written |
| `contaminated` | bool | See rule below |

**Case input keys** (subset per fixture):  
`case_id`, `card_id`, `cie_id`, `utterance`, `packs_loaded`, `prior_M`, `routing_filter`, `call` (`run_hop` or `process`).

---

## Fixtures (eight situations)

### Singles

| case_id | Input | Scored |
|---|---|---|
| `R_empty` | `card_id=S_unmapped`, `cie_id=neutral` | W2, W3, W5 |
| `R_deadline` | `S_deadline_friday`, `neutral` | W3, W5 |
| `R_miss` | utterance `zzzzq no cue at all`, packs `[base_en]`, no card | W5 only |
| `R_routing` | `S_sleepy`, `neutral`, `routing_filter={keep:true}`, `call=process` | I2 |

### Pairs

| pair_id | Left / right | Scored |
|---|---|---|
| `P_rock_cie` | `S_rock_burst` + `physical_stance` vs `scientific_stance` | W1, W3, W4, W5 |
| `P_replay` | `S_rock_burst` + `neutral` twice | I1 (also W3, W5 per side if convenient) |

### Cross

| case_id | Input | Scored |
|---|---|---|
| `R_prior` | `S_deadline_friday`, `neutral`, `prior_M` from native `R_rock_phys` \(M'\) | Sanity: native must not claim first-cycle. No extra wall. Cheap rivals may ignore `prior_M`. |

`R_miss` is **not** a W1 case. Absence of structure is not a failed invariant.

---

## Predicates (if this, then that)

### Contamination

- **If** module is `idob_native` → `contaminated = False` always. Map use allowed.  
- **If** cheap module imports/opens map, ranking, meaning-group tables, or `idob.py` → `contaminated = True`.  
- **If** `contaminated` is True on any call → discard that rival. Do not count pass or fail.  
- **If** self-report is False but static check finds a forbidden import → treat as contaminated anyway.

### W1 two-space invariant (`P_rock_cie`)

- **If** `structural_key_left != structural_key_right` → FAIL.  
- **If** both keys are null → FAIL (no structure to hold on a card-present pair).  
- **If** keys are equal and non-null → PASS.

### W2 empty legal birth (`R_empty`)

- **If** `selected_group_id is None` **and** `meaning_semantics is None` → PASS.  
- **If** either is non-null → FAIL (invented birth).

### W3 rank ⊆ map (every scored packet that has lists)

- **If** `set(final_rank_order) ⊆ set(candidate_group_ids)` → PASS.  
- **If** candidates empty and rank empty → PASS.  
- **If** rank contains an id not in candidates → FAIL.  
- **If** candidates empty and a winner exists → FAIL (also a W2-class invention).

### W4 CIE-only motion (`P_rock_cie`)

- **If** either side did not birth (`selected_group_id` or `meaning_semantics` null) → W4 = `n/a`. W2 owns empty birth. Do not pass or fail W4.  
- **If** both birthed and keys differ → FAIL W4 (and W1).  
- **If** both birthed, keys equal, CIE ids identical or both `neutral` → PASS even if \(M'\) equal.  
- **If** both birthed, keys equal, CIE differs, and native CIE table has \(\alpha \neq 0\) for at least one side:  
  - native: **If** \(\|M'_L - M'_R\|_2 > 0\) → PASS; else FAIL.  
  - cheap rival: **If** \(M'\) does not move → FAIL W4 (allowed; they may ignore CIE). Moving \(M\) is optional for rivals only in the sense that we do not require a good CIE model — but on this pair a frozen \(M'\) under two named stances fails W4.  
- CIE changing six IDs or the key is always FAIL.

Clarification for implementers: cheap rivals will typically fail W4 on `P_rock_cie`. That is expected. Do not “help” them by skipping W4.

### W5 residue is not a next-tuple

- **If** `next_key is None` → PASS.  
- **If** `next_key` is any string or six-tuple → FAIL.  
- `residue_code` may be non-null. That is not a fail.

### I1 replay (`P_replay`)

- **If** scored fields of left packet == scored fields of right packet → PASS.  
- Else FAIL.

### I2 no routing write (`R_routing`)

- Native: call `process()` with `routing_filter={keep:true}`.  
- **If** returned filter still `{keep:true}` and `routing_filter_mutated is False` → PASS.  
- Cheap rivals: if they do not implement `process`, they must echo `routing_filter_mutated=False` and not invent a write. Then I2 PASS (they did not touch routing).  
- **If** any rival sets `routing_filter_mutated=True` → FAIL I2.

### Native-broken stop

- **If** `idob_native` fails any W or I, uncontaminated → print `BENCH BROKEN` and exit non-zero. Do not interpret cheap-rival results.

---

## Locked verdict table (print this, nothing stronger)

| Result | What we may say |
|---|---|
| IdOB-native fails any wall | Bench broken. Stop. Fix `idob.py` / fixtures first. |
| Rival fails ≥1 wall, `contaminated: false` | That theory is not a sufficient cheaper operator. |
| Rival passes all walls, `contaminated: false` | Goal v2 fails for that rival. IdOB shrinks toward naming. |
| Rival passes only after reading our map | Contaminated. Not a pass. Not a fail. Discard. |
| All three cheap rivals fail ≥1 wall, uncontaminated | Package does work those styles do not. First conviction. Still not a completed necessity theorem. |

Forbidden sentences in code comments and README:

- “The package is necessary.”  
- “World primitives are the six IDs.”  
- “IdOB is better.”  
- “This proves cognition.”

---

## Expected first run (if stubs stay cheap)

| Rival | Expected |
|---|---|
| `idob_native` | All walls pass. Else stop. |
| `frame_fill` | Fail W2 (`S_unmapped` births). May fail W4. |
| `embed_nn` | Fail W2. Fail W1 if CIE is folded into the embed string. |
| `dict_lookup` | Fail W1 on `P_rock_cie` (both keys null). |
| `one_space` | Contrast fourth cheap rival; may fail W1/W4 on `P_rock_cie` when stance is live. |

Do not tune cheap rivals until they pass. That would contaminate the comparison by another route.

---

## File list (harness landed)

```
12_reduction/
  README.md
  fixtures.yaml
  score_sheet.yaml
  rivals/idob_native.py
  rivals/frame_fill.py
  rivals/embed_nn.py
  rivals/dict_lookup.py
  rivals/one_space.py       # fourth cheap rival (contrast)
  run_12_reduction.py
```

`run(case) -> packet_subset` is the only required function on each rival module.

From this directory:

    python run_12_reduction.py

---

## What this folder will not do

- Audit talk-shape IDs into a world ontology.  
- Count utterance coverage.  
- Invent `next_key` or call RB.  
- Declare six axes complete.  
- Expand the rival set mid-run.

Those are later named revisions.
