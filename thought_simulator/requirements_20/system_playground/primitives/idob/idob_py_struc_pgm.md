# idob_py_struc_pgm.md — IdOB structural program (S2M / 11)

**Document ID:** idob_py_struc_pgm  
**Version:** 1.0 (structure-to-meaning)  
**Scope:** Path A IdOB hop as realized by `primitives/idob/idob.py`  
**Kernel:** `testbenches/idob_structure_to_meaning/11_idob_core/`  
**v0.1** (formation…closure transition table) is lifecycle history — git of this file; not how `idob.py` runs.

An implementer or another AI should be able to wire, test, and extend IdOB from this document plus `11_idob_core/idob_core.md`.

---

## 0. Intent

IdOB is a **research hop**: utterance/card → six-ID structure → map → rank → six-axis stand-in \(M\) → CIE → Δh + flags.  
It is not a cognition verdict and not listener uptake. Meaning = speaker **intended projection**.

Feel / theory: `papers/idob_s2m_overview.md`, bench `idob_s2m_theory.md`.  
YAML law: `papers/idob_yaml_handbook.md`.

---

## 1. Module shape (`idob.py`)

```
primitives/idob/idob.py
  get_primitive_name() -> "idob"
  process(tp, mode="general", **kwargs) -> tp
  class IdOB(tp).process(mode, **kwargs) -> tp
```

`process` loads `11_idob_core/idob.py` and calls its `process`. It copies `idob_complete`, `path_b_eligible`, `ready_for_ouba` onto the TP root and `meaning_delta_h` under `tp["semantic"]`.

kwargs (also accepted on the TP):

| Name | Role |
|------|------|
| `utterance` | Carrier string (always store when present) |
| `card_id` | Skip 09; load 01 card |
| `packs_loaded` | 09 pack list |
| `cie_id` | Stance table row (default `neutral` or `physical_stance`) |
| `prior_M` | Previous \(M'\); absent → first-pass zeros |

`mode` is `testbench` | `general` (runner convention). The kernel does not change algorithm by mode.

Do not re-implement `_apply_transition` geometry tables in this module.

---

## 2. Testbench architecture

Root: `testbenches/path_a/identity/`

| File | Role |
|------|------|
| `idob_testbench.py` | Runner. Prints utterance + input + `tp.idob` every test. |
| `idob_tests_to_run.yaml` | Enable list (`idob_s2m_*`) |
| `idob_testbench.yaml` | Cases: `utterance`, `input`, `expected` packet fields |
| `idob_input.yaml` | General-mode single TP |
| `idob_rules.yaml` + `idob_rulechecker.py` | Write-boundary, packet keys, rank ⊆ map, utterance present |
| `idob_lifecycle_archive.yaml` | Ten formation…closure utterances — **not** run against 11 |

Import: `from ...primitives.idob.idob import IdOB, get_primitive_name`.

Learning bench (same kernel): `testbenches/idob_structure_to_meaning/` slides 01–11 + `run_ts_struc2mn.py`.

### Dual mode

| mode | Input | Pass criterion |
|------|--------|----------------|
| `testbench` | `idob_testbench.yaml` row | expected fields match **and** rulechecker clean |
| `general` | `idob_input.yaml` | rulechecker only |

Every enabled test **must** keep the utterance on the trace (or `utterance_source: card` with a card note).

---

## 3. Owned writes vs write-boundary

**IdOB may write**

- `tp["idob"]` — full packet (`11_idob_core/packet.schema.yaml`, `idob_s2m_packet.yaml`)
- root flags `idob_complete`, `path_b_eligible`, `ready_for_ouba`
- `tp["semantic"]["meaning_delta_h"]`
- diagnostic `tp["_idob_diagnostics"]["routing_filter_mutated"]` if a leak was detected and rolled back

**IdOB must not write**

- `process.routing_filter` (RB)
- `metadata.geometric_state` / DCB history
- SSG / structural_graph / structural residue
- next six-tuple as if it were RB

Guard: snapshot `routing_filter` before `run_hop`; restore if changed.

---

## 4. Packet (output contract)

Always: `utterance`, `resolution_status`, three flags, `routing_filter_mutated`.

On birth: `structural_key`, six IDs, `candidate_group_ids`, `final_rank_order`, `selected_group_id`, `meaning_semantics`, `meaning_semantics_prime`, `meaning_delta_h`, `meaning_cie_delta`, `first_meaning_cycle`, `cie_id`, `hold_geometry`.

On miss / empty map: meaning fields null; `expand_target` may be set; utterance still present.

Flags (split on purpose):

- `ready_for_ouba` — a vector was born  
- `path_b_eligible` — born and no `residue_code`  
- `idob_complete` — same as eligible in this revision (not `geometry=closure`)

---

## 5. Algorithm (one hop)

1. Resolve card or 09-assign utterance + packs.  
2. Miss → `unassigned`, stop birth.  
3. Key from six IDs (`SK|f|r|o|g|u|s`).  
4. Map → legal `group_id` set. Empty → `empty_map`.  
5. Rank ⊆ that set → winner.  
6. Group prototype → \(M\).  
7. CIE: \(M'=\mathrm{clip}(M+\alpha I)\). Key unchanged.  
8. Δh vs `prior_M` or zeros.  
9. Flags + residue/`identity_residual` + expand hint.  
10. Write packet; enforce write-boundary.

RB / Slide 10 / CvThP are **outside** this module.

---

## 6. Support files this primitive must see

| Need | Where |
|------|--------|
| Structure IDs | `semantic_*.yaml` (this directory) + 09 packs |
| Cards | `01_structure/structure_card.examples.yaml` |
| Groups / map / rank / CIE | slides 02–05 (or `papers/structure_to_meaning/*.yaml` when promoted) |
| Residue expand | Slide 10 |
| Packet schema | `11_idob_core/packet.schema.yaml` |
| Lifecycle enums | `idob_schema.yaml` (hold_geometry / archive only) |

Loaders look **here first**, then the slide tree. Do not hard-code `papers/semantic_*` (deleted).

---

## 7. Requirements the testbench must keep proving

1. Deterministic: same utterance/card + packs + CIE + prior_M + YAML revision → same packet.  
2. Utterance visible on every case.  
3. Rank never invents a `group_id` off the map.  
4. CIE does not change `structural_key`.  
5. First hop uses zero before-vector (`first_meaning_cycle`).  
6. `routing_filter` unchanged when present.  
7. Miss stores the string and births no \(M\).  
8. `get_primitive_name() == "idob"`.

---

## 8. Implementation order (if touching code)

1. Keep wrapper + `process(tp)` surface.  
2. Point map lookup at `structural_key` as well as `card_id` when promoting tables.  
3. Load `semantic_*.yaml` numeric ids from 09 packs.  
4. Do not port v0.1 `GEOMETRY_MAP` into meaning.

---

## 9. Lifecycle sibling (not this program)

Ten conversation cases and the formation…closure table live in `papers/lifecycle/` and `idob_lifecycle_archive.yaml`. `idob_schema.yaml` remains their enum file. Do not compare `metadata.identity.geometry` to `tp.idob.meaning_semantics`.
