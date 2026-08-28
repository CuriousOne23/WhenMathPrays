# idob_py_struc_pgm.md — IdOB structural program

**Document ID:** idob_py_struc_pgm  
**Version:** 1.1  
**Scope:** Path A IdOB hop as realized by `primitives/idob/idob.py`  
**Tests:** `testbenches/path_a/identity/`

An implementer should be able to run, extend, and judge the hop from this file plus the YAML listed in §6.

Derivation is Path A structure-to-meaning (two geometries, door, rank, CIE, Δh). This program does not name another directory as the test oracle.

---

## 0. Intent

IdOB is a research hop: utterance and/or card → six-ID structure → map → rank → six-axis stand-in \(M\) → CIE → Δh + flags.  
Meaning = speaker **intended projection**. The utterance is the carrier.

Feel: `papers/idob_s2m_overview.md`.  
YAML law: `papers/idob_yaml_handbook.md` (edit the tables in **this** directory).

---

## 1. Module (`primitives/idob/idob.py`)

```
get_primitive_name() -> "idob"
process(tp, mode="general", **kwargs) -> tp
IdOB(tp).process(mode, **kwargs) -> tp
run_hop(...) -> packet dict
```

`idob.py` loads YAML **only** from `primitives/idob/`. It does not import testbench slide code.

kwargs (also accepted on the TP):

| Name | Role |
|------|------|
| `utterance` | Carrier; always stored when present |
| `card_id` | Load `structure_card.examples.yaml` |
| `packs_loaded` | e.g. `[base_en]` → `pack_base_en.yaml` |
| `cie_id` | Row in `cie.examples.yaml` |
| `prior_M` | Absent → first-pass zeros |

`mode` is `testbench` \| `general` (runner convention). The hop algorithm does not change with mode.

---

## 2. Test structure (`testbenches/path_a/identity/`)

The runner may import **only** this folder and `primitives/idob`.

| File | Role |
|------|------|
| `idob_testbench.py` | Runner. Prints utterance + input + `tp.idob` per test. |
| `idob_tests_to_run.yaml` | Enable list |
| `idob_testbench.yaml` | Cases: `utterance`, `input`, `expected` packet fields |
| `idob_input.yaml` | General-mode single TP |
| `idob_rules.yaml` | Rule ids |
| `idob_rulechecker.py` | Walls: packet present, utterance, rank ⊆ map, write-boundary, flags |
| `idob_lifecycle_archive.yaml` | Ten formation…closure utterances — **not** enabled |

Import: `from …primitives.idob.idob import IdOB, get_primitive_name`.

### Enabled cases (`idob_tests_to_run.yaml`)

| id | What it proves |
|----|----------------|
| `idob_s2m_01_rock` | Card `S_rock_burst` births group 1001; leftover `residue_code`; `path_b_eligible` false |
| `idob_s2m_02_deadline` | Card `S_deadline_friday` births 3001; no residue; Path B door open |
| `idob_s2m_03_sleepy` | Card `S_sleepy` births 4001 |
| `idob_s2m_04_unmapped` | Card `S_unmapped` empty map; no \(M\) |
| `idob_s2m_05_miss` | Utterance with no pack cue; `unassigned`; string still stored |
| `idob_s2m_06_write_boundary` | `process.routing_filter` unchanged |

### Dual mode

| mode | Input | Pass |
|------|--------|------|
| `testbench` | enabled rows in `idob_testbench.yaml` | `expected` fields match **and** rulechecker clean |
| `general` | `idob_input.yaml` | rulechecker only |

Every enabled test must keep the utterance on the trace (or `utterance_source: card`).

---

## 3. Owned writes vs write-boundary

**May write:** `tp["idob"]` (packet), root flags `idob_complete` / `path_b_eligible` / `ready_for_ouba`, `tp["semantic"]["meaning_delta_h"]`.

**Must not write:** `process.routing_filter`, DCB `geometric_state`, SSG / structural_graph, next six-tuple as if it were RB.

Guard: snapshot `routing_filter` before the hop; restore if it moved.

---

## 4. Packet

Contract file: `idob_s2m_packet.yaml` (loaded by `idob.py`).

Always: `utterance`, `resolution_status`, three flags, `routing_filter_mutated`.

On birth: six IDs, `structural_key`, candidates, rank, `selected_group_id`, \(M\), \(M'\), Δh, CIE fields, `first_meaning_cycle`, `hold_geometry`.

On miss / empty map: meaning fields null; utterance still present.

Flags:

- `ready_for_ouba` — a vector was born  
- `path_b_eligible` — born and no `residue_code`  
- `idob_complete` — eligible **and** `resolution_status == meaning_stable`

---

## 5. One hop

1. Card from `structure_card.examples.yaml`, or assign utterance via `pack_*.yaml` + `semantic_*.yaml`.  
2. Miss / partial → stop birth; keep string.  
3. Key `SK|f|r|o|g|u|s`.  
4. Map by `card_id` or `structural_key`. Empty → `empty_map`.  
5. Rank ⊆ legal set.  
6. Prototype → \(M\).  
7. CIE: \(M'=\mathrm{clip}(M+\alpha I)\). Key unchanged.  
8. Δh vs `prior_M` or zeros.  
9. Flags + `identity_residual` + expand hint from `residue_next.examples.yaml`.  
10. Write packet; enforce write-boundary.

RB is outside this module.

---

## 6. YAML `idob.py` must open (this directory only)

| File | Role |
|------|------|
| `structure_card.examples.yaml` | Cards |
| `meaning_groups.yaml` | Prototypes |
| `struct_to_meaning_map.yaml` | Door |
| `ranking_weights.yaml` | Rank |
| `cie.examples.yaml` | Stance |
| `residue_next.examples.yaml` | Expand hint |
| `pack_base_en.yaml` | Phrase → six IDs |
| `semantic_field_definitions.yaml` … `semantic_subfields.yaml` | Structure id inventories |
| `idob_s2m_packet.yaml` | Packet contract |

A YAML that the hop never opens does not belong here. Lifecycle enums: `papers/lifecycle/idob_schema.yaml`.

---

## 7. What the testbench must keep proving

1. Same utterance/card + packs + CIE + prior_M + YAML revision → same packet.  
2. Utterance visible on every enabled case.  
3. Rank never invents a `group_id` off the map.  
4. CIE does not change `structural_key`.  
5. First hop uses zero before-vector (`first_meaning_cycle`).  
6. `routing_filter` unchanged when present.  
7. Miss stores the string and births no \(M\).  
8. `get_primitive_name() == "idob"`.

---

## 8. Lifecycle sibling (not this runner)

Ten conversation cases: `papers/lifecycle/idob_10_conversation_cases.md` and `idob_lifecycle_archive.yaml`. Do not compare `metadata.identity.geometry` to `tp.idob.meaning_semantics`.
