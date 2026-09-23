# IdOB Object Space — Unified Plan
## Theory · Architecture · Engine · Debugger · Log contract
### Path-A short simulator
### 2026-09-23

Status: consolidated plan. R1–R3 and D1–D3 landed. R4a catalog next.
Scope: short sim only. MCB omitted (R5).
Construct: **IdOB space $\mathcal{I}$ is a frozen registry of IdOBObjects;
IdOB is the deterministic overlap-sum of their contributions;
the packet on TP is that sum; the debugger observes that packet;
`run_examples.py` is the emitter that makes the space visible.**

---

## 0. Four layers, one fog

| Layer | Owner files | Current reality |
|---|---|---|
| Theory | routing note, this plan | Meaning(U)=IdOB(U) named; space not defined |
| Architecture | PSC / schema (missing) | No object spec, no overlap algebra |
| Engine | `primitives_pathA_short.py`, `pathA_short_simulator.py`, `tp_substrate.py` | Function + second writer + list/dict wobble |
| Observer | `run_examples.py` → `run.log` → `pathA_dbug.py` | Log collapses core to list-or-empty; debugger is faithful to the collapse |

Hard rule: **the debugger does not move until the engine has one writer and the log emits a space.**

---

## 1. Naming lock (all four layers)

| Token | Meaning |
|---|---|
| IdOB | Summation operator / primitive. Not an object. |
| IdOB space $\mathcal{I}$ | Frozen registry snapshot |
| IdOBObject | One bounded extractor |
| family | copular_state \| locative \| mixed_descriptive \| interrogative_wh \| interrogative_polar \| residual_identity |
| activation / activation_set | Objects with act=1 |
| inactive_objects | $\mathcal{I}\setminus A(U)$ |
| contribution / contributions | Per-object packet fragments |
| contributors | Activated ids, `(priority, name)` order |
| idob_packet | Sum written to `tp.idob` |
| semantic_core | **dict only** after IdOB |
| selected_ops | list[str], stable unique |
| identity_geometry | structural_identity \| referential_identity \| semantic_identity |
| truth_relation | mood: declarative \| interrogative \| unknown |
| truth_relation_family | note vocab: descriptive_state \| descriptive_locative \| descriptive_mixed \| interrogative_wh \| interrogative_polar \| unknown |
| tru_hint | TRU mood hint on TP / log |
| tru_alignment | tru_hint vs summed mood |
| overlap_near / overlap_far | Declared edges |
| overlap_mode | merge \| suppress \| blend \| coexist |
| overlap_events | Executed resolutions `{a,b,mode,fields}` |
| meaning_delta | Pre-IdOB vs packet claimed fields |
| PSC / psc_violations | Contract + logged breaks |
| registry_digest | Hash of object YAML |
| residual_activated | residual_identity in A(U) |
| R0–R6 | Engine gates |
| D0–D4 | Debugger gates |

Forbidden: “IdOB object” as the primitive; list `semantic_core` as canonical; `_minimal_idob_selection` after R3; debugger-only synonyms.

---

## 2. Theory

$$
\mathcal{I}=\{o_k\},\quad
A(U)=\{o\in\mathcal{I}:\mathrm{act}_o(\mathrm{freeze}(U))=1\},\quad
\mathrm{IdOB}(U)=\bigoplus_{o\in A(U)}c_o
$$

- Mixed interrogative is **overlap**, not a seventh family.
- Mood sum: any interrogative → interrogative; else any declarative → declarative; else unknown.
- Family sum: one family wins; descriptive+interrogative → `descriptive_mixed` + interrogative mood.
- Overlap default: near+same key merge; near+different coexist; far+same suppress by priority; far+different coexist.
- Residual never suppresses a non-residual object.
- Geometry = indicator of $A(U)$ plus claimed roles. No embeddings.
- The Debugger observes the IdOB sum, $\oplus$; it never performs a second $\oplus$.
    - It does not re-run IdOB logic.
    - It does not re-sum contributions.
    - It does not apply overlap rules.
    - It does not merge or suppress fields.
    - It does not produce its own packet.
    - $\oplus$, implies a structured, multi‑object combination, not necessarily numeric but structure

---

## 3. Architecture

### 3.1 IdOBObject catalog frame (YAML)

An IdOBObject is a catalog document plus a tiny apply stub. It is not a
closure in `legacy.py`.

```yaml
schema_ref: idob_object.v1
psc_id: PSC-IdOB-<name>-v1          # per-object id
name: locative
family: locative                     # for the eight live objects, family = name
priority: 20

identity:
  label: "Locative descriptive"
  description: "..."
  tags: ["descriptive", "locative"]

association:
  geometries:
    - [NP, CP, LOC]                  # claimed segment shapes, not a second SOB
  roles: [theme, state, location]    # TP roles, not SOB labels

contribution_schema:
  semantic_core:
    type: dict
    keys: [theme, state, location, complement, ...]   # live core keys only
  selected_ops:
    type: list
    items: [state_location]          # live op strings only
  truth_relation_family:
    type: str
    default: descriptive_locative    # locked enum

overlap:
  near: [copular_state, mixed_descriptive]
  far: [agent_action]

psc_invariants:                      # extras only; I8/I10 live in defaults
  - id: I8
    field: contribution_schema
    rule: writes_only_declared_fields

behavior:
  apply: idob.behaviors.locative:apply
```

Locks:

- **No `claimed_fields`.** `contribution_schema` is the bound. Any key
  written that is not listed there is a run-time PSC violation.
- **Activation is data** (predicate tree in the catalog / engine
  predicates). **Apply is code** (`idob/behaviors/`).
- Shared invariants I8 and I10 live in `support/idob_psc_defaults.yaml`.
  Object YAML only adds extras. Digest hashes specs + `schema_ref` +
  defaults file.
- `family` is the algebra axis. Human category goes in `identity.tags`.
- R4a copies **live** `semantic_core` keys and `selected_ops` strings.
  New names are a different gate.

Activation language remains
`all|any|not|has_role|has_constraint|has_cue|text_endswith|role_text_in`.
No Python in YAML.

### 3.2 Invariants

I1 Pure activation. I2 Unique names. I3 Sum order `(priority, name)`.
I4 Mood/family rules. I5 `idob_complete == packet.complete`.
I6 `path_b_eligible == idob_complete`. I7 Replay + digest.
I8 Objects do not mutate OB-set. I9 Contested keys → overlap_events.
I10 `semantic_core` is a dict after IdOB.

### 3.3 Observed packet schema (engine write = log emit = debugger parse)

```text
identity_geometry: str
truth_relation: str
truth_relation_family: str
semantic_core: dict
selected_ops: list
claimed_fields: list
contributors: list
contributions: list[dict]
activation_set: list
inactive_objects: list
residual_activated: bool
overlap_events: list
meaning_delta: dict
psc_violations: list     # [] required when clean
registry_digest: str
complete: bool
tru_hint: str            # copied from TRU for alignment
```

This **is** `tp.idob` after R3/D3. Frozen. `run_examples` prints these
keys. `pathA_dbug` scrapes these keys. No fourth schema.

R4 does **not** add spec/YAML blobs to the packet. The catalog lives
off-packet. PSC uses existing `psc_violations` and `registry_digest`.
D4 joins `contributors` to `identity.label` from YAML.

### 3.4 Flow

`… CTP → IdOB → OuBA`. TRU stays earlier; after R3 it writes `tru_hint` and must not clobber a completed IdOB mood.

---

## 4. Engine software

```text
idob/object.py registry.py predicates.py sum.py packets.py
idob/behaviors/          # apply stubs (R4a)
idob/psc.py              # checker (R4b)
idob/legacy.py           # migration leftover until apply moves
support/idob_objects/*.yaml
support/idob_psc_defaults.yaml
support/idob_object.v1.schema.json
support/idob_packet.v1.schema.json
```

`IdOB(tp)` = `sum_idob` + writeback.

`registry.py` loads `support/idob_objects/*.yaml`, binds
`behavior.apply`, builds the overlap graph from catalog `overlap`
blocks, and computes `registry_digest` from canonical specs +
`schema_ref` + hash of `support/idob_psc_defaults.yaml`. It does not
hash Python.

Eight live objects (family = name): copular_state, locative,
mixed_descriptive, interrogative_wh, interrogative_polar, agent_action,
modifier_resolution, residual_identity. No `overlap_identity` object.

---

## 5. Log contract (`run_examples.py`)

Today IdOB prints:

```text
idob_packet={...}
semantic_core=[]          # list or forced empty
truth_relation=...
```

After D1 (which is after R3), one block:

```text
--- IdOB ---
registry_digest='...'
activation_set=[...]
inactive_objects=[...]
residual_activated=False
contributors=[...]
contributions=[...]
overlap_events=[...]
meaning_delta={...}
psc_violations=[]
semantic_core={...}
truth_relation='...'
truth_relation_family='...'
tru_hint='...'
idob_packet={...}
```

Rules:

- Values after `=` are `ast.literal_eval` safe (`pathA_dbug` already uses that).
- `semantic_core=` is always a dict. Delete the `else []` branch.
- Exactly one `--- IdOB ---` per run. No second “[Semantic]” writer.
- R1 may emit `contributors=['legacy_monolith']` and `overlap_events=[]`. That is a true one-object space.

Also print `--- TRU ---` with `tru_hint=` (or current `truth_relation=`) so alignment has two sources.

---

## 6. Debugger contract (`pathA_dbug.py`)

Observer only. Does not import IdOB. Does not re-sum.

**Stop:** list-core as canonical; wrapping lists as `{"values":…}`; printing empty core when packet holds a dict; glossary “IdOB builds the packet”; omitting TRU; merging two IdOB blocks as legal.

**Start (D3):** IdOB Space Summary with the §3.3 keys; dict `_append_dict_block` for core; `tru_alignment`; contributions as records; list-core → parser `psc_violations` `_log`/`I10`, core `{}`.

Glossary rewrite:

```text
IdOB: Summation operator over IdOB space I; not an object.
idob_packet: Sum of activated IdOBObjects.
semantic_core: Dict payload of the sum; never a list.
truth_relation: Mood of the sum.
contributors / contributions / overlap_events / meaning_delta /
registry_digest / psc_violations / tru_alignment / residual_identity
```

`debug_setup.yaml` / `links.yaml` gain dimension `idob_space` at D3, not before.

---

## 7. Synchronized roadmap

```text
R0  Freeze engine oracle (packets / selected_ops / mood)
D0  Freeze collapsed-era debug_out.md fixtures (do not beautify)

R1  legacy_monolith behind sum_idob — bit-identical to R0
R2  Split objects + overlap graph — same selected_ops oracle
R3  Single writer; dict-only semantic_core; TRU cannot clobber
D1  run_examples log contract (§5)
D2  pathA_dbug parser accepts new keys
D3  IdOB Space Summary + glossary + TRU compare
    ── landed ─────────────────────────────────

R4a Catalog lift
    Eight YAML files; live core keys and selected_ops strings only.
    Registry loads YAML; apply still points at existing functions.
    Overlap graph closed (all live edges appear in some YAML).
    Load fails if a name does not resolve.
    Exit: eight files load; registry_digest stable;
    packet oracles bit-identical to R3.
    New core key or op string = a different gate, not R4a.
    Do not land psc.py in the same commit.

R4b PSC
    idob/psc.py: spec + contribution + TP.
    Load-time: unique names, closed graph, known behavior symbols.
    Run-time: unlisted keys, I8, I10, extras from object YAML.
    Violations: {object_id, invariant, field, detail}.
    Eval-order permutation remains a test.

D4  Debugger prints psc_violations (even []), |I|, |A(U)|,
    inactive_objects; joins contributors → identity.label.
    No spec dumps.

D5  Optional catalog appendix (space listing: name, family,
    priority, overlap). Not per-run YAML.

R5  MCB seam copies only. No catalog/PSC work moves here.
R6  New object = YAML + optional apply stub; closed overlap.
```

**Forbidden:** debugger printer changes in the same commit as R4a.
**Forbidden:** changing live op/core strings inside R4a.

### Gate proofs

| Gate | Proof utterance / check |
|---|---|
| R0/D0 | Current examples frozen |
| R1 | Bit-identical to R0 |
| R2 | *Where is the book that is on the table?* ≥2 contributors, overlap_events ≠ [] |
| R3 | One IdOB writer; `semantic_core` dict on TP |
| D1 | Log lines literal-eval; no `semantic_core=[]` for dict cores |
| D3 | *The sky is blue.* one descriptive contributor, empty overlap, declarative, dict core |
| R4a | Eight YAML load; digest stable; R3 packet oracle holds |
| R4b | Unlisted key → psc_violation; I8/I10 from defaults |
| D4 | `psc_violations: []` visible; contributor labels from catalog |
| R5 | MCB copies only |

---

## 8. File change map by gate

| Gate | Files |
|---|---|
| R1–R3 | `idob/*` landed; single writer |
| D1–D3 | log contract + IdOB Space Summary landed |
| R4a | `support/idob_objects/*.yaml`, defaults, registry YAML load |
| R4b | `idob/psc.py` |
| D4 | `pathA_dbug.py` join to `identity.label` |
| D5 | optional catalog appendix |
| R5 | MCB seam only |

---

## 9. Open items

1. Mood vs family: keep two fields, or rewrite note+code to one vocab.
2. `agent_action`: family or helper object.
3. TRU: hint-before vs confirm-after (plan assumes hint-before).
4. Candidate group ids 1001…: packet field or delete.
5. Residual may set `complete=True`.
6. Line log vs JSON sidecar when contributions get fat (line through D3).
7. Always print `inactive_objects` (yes, compact).

---

## 10. One-sentence plan

**R1–R3 made the sum real; D1–D3 observe the packet; R4a names $\mathcal{I}$ as a hashed YAML catalog with live keys; R4b checks spec against contribution; D4 joins names to `identity.label`; the packet stays still; R5 is still MCB.**

