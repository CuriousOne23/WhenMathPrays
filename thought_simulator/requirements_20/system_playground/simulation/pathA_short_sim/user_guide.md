# PathA Short Simulation — User Guide

This guide starts with a sentence you already know, then shows how the Path‑A Thought Simulator (TS) short simulator writes **structure** first and an Identity Observation Block (IdOB) **packet** last.

Names and hard words (object, adjacency, meaning, packet): [architecture/idob_seam.md](architecture/idob_seam.md).  
Catalog (eight families only): [notes/idob_object_space/idob_object_space.md](notes/idob_object_space/idob_object_space.md).  
Packet contract: [architecture/IdOB_unified_plan.md](architecture/IdOB_unified_plan.md).

---

## 1. Run the simulator

From this directory:

```
python run_examples.py
```

Or log output:

```
python run_examples.py > run.log
```

Then, to read the log as a teaching document:

```
python pathA_dbug.py run.log --base-dir .
```

That writes `debug_out.md`.

Supported sentences: [notes/pathA_supported_sentences.md](notes/pathA_supported_sentences.md).

---

## 2. Modify the input sentence

Open `run_examples.py` and change the raw string passed into `run_pathA_short(...)`, then rerun. Stay inside the supported families unless you are extending dictionaries on purpose.

---

## 3. This world → two columns

Take *The sky is blue.*

This world: you are told the sky’s color.

Path A splits that into:

| Column A — structure (Observation Block set, OB-set) | Column B — meaning on this path (IdOB packet) |
|---|---|
| Chunks, roles, constraints, smoothing cues | Which catalog objects fired and what dict they summed |
| Written by Segment Observation Block (SOB), Segment Role Observation Block (SROB), Constraint Observation Block (CnOB), Smoothing Observation Block (SmOB) | Written by IdOB only |
| `struct_segments`, `struct_roles`, `constraints_matched`, `semantic_adjacent_cues`, residues | `activation_set`, `semantic_core` (**dict**), `truth_relation`, `overlap_events`, `meaning_delta`, `idob_packet` |

IdOB does not invent the chunks. If column A is empty or wrong, column B cannot “know the sky.”

### 3.1 *The sky is blue.*

| Structure (who wrote it) | Packet (IdOB) |
|---|---|
| SOB: noun-phrase + state material | Expect one descriptive contributor (`copular_state` family) |
| SROB: theme / state jobs | `semantic_core` is a dict (keys such as `theme`, `state`) — **not** a list |
| CnOB: copular constraints can close | `truth_relation` declarative; `tru_hint` from Truth-Relation Update (TRU) should align |
| SmOB: little basin leftover | `overlap_events` typically `[]` |

This is the unified-plan D3 proof utterance.

### 3.2 *Where is the book that is on the table?*

This world: you ask where the book is, and you pin which book with a clause.

| Structure | Packet |
|---|---|
| SOB: question word, entity, locative, relative clause | `activation_set` may list more than one name |
| SROB: query focus + entity + location | `semantic_core` dict may hold `query_focus` and `location` |
| CnOB: interrogative scope + locative attachment (`constraint_residue` if scope is messy) | `truth_relation` interrogative |
| SmOB: book + table in one picture (basin adjacency) | `overlap_events` may be nonempty — **object** adjacency executed, not word neighbors |

Three uses of adjacency (do not collapse them):

1. String: *book* touches the clause (SOB/CnOB).
2. Basin: book + table one picture (SmOB).
3. Object: more than one IdOB family eligible (catalog `overlap.*` → packet `overlap_events`).

This is the unified-plan R2 proof utterance.

### 3.3 *The book is on the table.*

Same two-column habit: SOB/SROB place the locative; IdOB `locative` (and possibly `copular_state`) are the catalog names in play. Do not call the book an IdOB object.

---

## 4. Interpret the final Thought Packet (TP)

The final TP is the end-state substrate after all primitives run.

**Intake**

- `tokens`, `normalized_text` — Intake Engine (IE) and intake blocks

**Structure (OB-set)**

- `struct_segments`, `segment_tokens` — SOB
- `struct_roles`, `role_segments` — SROB
- `constraints_matched`, `constraints_unmatched`, `constraint_residue` — CnOB
- `smoothing_operations`, `semantic_adjacent_cues`, `basin_residue` — SmOB

**Routing**

- `routing_metadata`, `routing_decision`, `tru_hint` — routing primitives including TRU

**Meaning on this path (IdOB)**

- `semantic_core` — **dict** payload of the sum
- `idob_packet` — full packet (see unified plan §3.3)
- `activation_set`, `contributors`, `contributions`, `overlap_events`, `meaning_delta`, `psc_violations`, `registry_digest`

**Commit**

- `commit_flags` — Output Binding / Assemble (OuBA) checkpoints

`meaning_delta` here is legacy-writer vs split-writer. It is not S2M `meaning_delta_h` and not entropy $\Delta H\%$. See the seam alias table.

---

## 5. Interpret the trace

Each trace item includes:

- **primitive** — name executed
- **input** — TP snapshot before the primitive
- **output** — TP snapshot after the primitive
- **notes** — human-readable observation

Read input/output deltas to see exactly what each primitive changed. IdOB should change packet fields, not rewrite `struct_segments`.

---

## 6. Follow TP evolution macro by macro

### Intake
`InB`, `IIInB`, `IE`

### Correction
`CEx`, `CE`, `ISc`, `TPU`

### Structural geometry (OB-set)
`SOB`, `SROB`, `CnOB`, `SmOB`, `SSG`

### Routing
`RBU`, `RB`, `TR`, `TRU`, `RTU`, `CTP`

### Semantic (meaning-as-packet)
`IdOB`

### Final commit
`OuBA`

Meaning Composition Block (MCB) is omitted in this short sim.

---

## 7. Debug odd outputs

- Confirm token normalization in **IE**
- Verify YAML dictionaries contain expected entries (OB-set rules under `support/dictionaries`)
- Check **SOB** segment alignment
- Check **SROB** role progression
- Confirm **CnOB** transition pairs in `constraint_rules.yaml`
- Confirm **IdOB** against the catalog and the packet, not against a six-type linguistic list
- If `semantic_core` prints as a list after IdOB, treat that as a contract break (Primitive Specification Contract (PSC) I10), not as “the meaning”

Debugger teaching cards live under `debug/`. The IdOB card is `debug/primitives/IdOB.md`.

---

## 8. Modify dictionaries

Edit files under `support/dictionaries` for **structure** rules:

- `token_classes.yaml`
- `segment_patterns.yaml`
- `role_patterns.yaml`
- `constraint_rules.yaml`

IdOB catalog objects live under `support/idob_objects/`. Do not add a ninth family by editing `semantic_rules.yaml` and calling it an object type.

Rerun `run_examples.py` and compare trace deltas.

---

## 9. Extend primitives

Edit `primitives_pathA_short.py` only when the lineup itself must change. IdOB sum logic lives in `idob/sum.py` and `idob/packets.py`. Keep mutations explicit and trace-visible.

---

## 10. Architecture overview — how files load

Neither `run_examples.py` nor `pathA_short_simulator.py` open YAML by hand. The engine import chain does.

### 10.1 Top-level Python

**`run_examples.py`**  
Entry point / driver. Defines example sentences. Calls `run_pathA_short`. Prints or logs the trace. Does not mutate the TP.

**`pathA_short_simulator.py`**  
Macro sequencer. Runs primitives in order. Captures snapshots. No dictionary loading of its own.

**`tp_substrate.py`**  
Defines the TP object, `init_tp`, `clone_tp`.

**`primitives_pathA_short.py`**  
Lineup implementations and imports. This is where support files get pulled in.

**`idob/`**  
Registry, sum, packets, PSC, legacy apply stubs.

### 10.2 Support files

**YAML dictionaries (OB-set)**  
`support/dictionaries/` — token classes, segments, roles, constraints.

**IdOB catalog**  
`support/idob_objects/*.yaml` — the eight families.  
`support/idob_schemas/idob_object.v1.schema.json` — object bound.  
`support/idob_schemas/idob_psc_defaults.yaml` — shared PSC defaults.

**JSON schemas**  
`support/contracts/` — TP / stream contracts.

**Prototypes**  
`support/prototypes/` when present — structural templates.

### 10.3 Execution flow

```
run_examples.py
    ↓
pathA_short_simulator.py
    ↓
tp_substrate.py
    ↓
primitives_pathA_short.py + idob/*
    ↓
support/dictionaries + support/idob_objects + schemas
    ↓
Primitive sequence (InB → … → IdOB → OuBA)
    ↓
Final TP + full trace
```

---

## 11. File roles (summary)

| File | Purpose |
|------|--------|
| `run_examples.py` | Runs examples; prints trace |
| `pathA_short_simulator.py` | Macro sequencer |
| `tp_substrate.py` | TP structure |
| `primitives_pathA_short.py` | Lineup; loads many support files |
| `idob/sum.py` | Writes the packet (meaning here) |
| `support/idob_objects/*.yaml` | IdOB space $\mathcal{I}$ |
| `support/dictionaries/*.yaml` | OB-set rule tables |
| `architecture/idob_seam.md` | Names and on-ramp |
| `debug/primitives/IdOB.md` | Observer card for IdOB |

---

## 12. Acceptance for this guide

This guide fails if it teaches six IdOB object types, shows list `semantic_core` as canonical, or calls the book an IdOBObject. It passes if the two-column examples in §3 can be walked without opening the engine.
