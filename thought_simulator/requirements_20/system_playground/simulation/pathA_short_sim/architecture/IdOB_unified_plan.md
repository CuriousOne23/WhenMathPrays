# IdOB — Path-A meaning contract and unified plan
## Theory · Architecture · Engine · Debugger · Log contract
### Path-A short simulator
### 2026-09-23; meaning lock 2026-09-28

Status: consolidated plan. R1–R3 and D1–D3 landed. R4a catalog next.
Scope: short sim only. Meaning Composition Block (MCB) omitted (R5).
Seam: [idob_seam.md](idob_seam.md)
Object space: [idob_object_space.md](../notes/idob_object_space/idob_object_space.md)
Meaning-as-packet teaching contract: [idob_meaning_lock.md](idob_meaning_lock.md)
Observer: [user_guide.md](../user_guide.md)  
Charter: [path_a_realization_charter.md](path_a_realization_charter.md)  
Reserve (IdOB-S2M / CIE / `meaning_delta_h` remain in 20.40.050): `20.700.010`

Construct: **Identity Observation Block (IdOB) space $\mathcal{I}$ is a frozen registry of IdOB objects (IdOBObjects);
IdOB is the deterministic overlap-sum of their contributions;
the packet on the Thought Packet (TP) is that sum; the debugger observes that packet;
`run_examples.py` is the emitter that makes the space visible.**

Meaning on this path is the packet. Teaching contract and instrument aliases: [idob_meaning_lock.md](idob_meaning_lock.md). Do not import Meaning Signal Layer (MSL), Cognitive Identity Envelope (CIE), or Structure-to-Meaning (S2M) $M$ here. R5 is not their parking lot.

Path-A-short realizes the **IdOB-sum** face of 20.40.050. The S2M / CIE face stays in 20.40.050 as reserved capability. This file does not add HLRs.

**Phase pointer (2026-10-08):** [../notes/program/pathA_program.md](../notes/program/pathA_program.md). The reserved S2M face is the unrealized job of this block, not a separate component and not a ban. This plan still describes the sum. It does not implement the mapping. The helper-family sentence in §3.1 that files `agent_action` as `residual_identity` is superseded by live YAML `family: agent_action`; empty activation remains true.


---

## 0. Four layers, one fog

| Layer | Owner files | Current reality |
|---|---|
| Theory | seam, meaning lock, this plan | Meaning($U$)=IdOB($U$) as packet; space = eight YAML files |
| Architecture | PSC / object schema | Catalog exists; apply still bound to `idob.legacy` |
| Engine | `idob/sum.py`, `idob/packets.py`, `idob/registry.py` | Split objects write the packet; `semantic_core` merged as dict |
| Observer | `run_examples.py` → log → `pathA_dbug.py` | Teaching cards updated 2026-09-28; debugger must not re-sum |

Hard rule: **the debugger does not move until the engine has one writer and the log emits a space.**

---

## 1. Naming lock (all four layers)

| Token | Meaning |
|---|---|
| IdOB | Summation operator / primitive. Not an object. |
| IdOB space $\mathcal{I}$ | Frozen registry snapshot |
| IdOBObject | One bounded extractor |
| family | YAML `family` field. Helpers may share another family. |
| activation / activation_set | Objects with act=1 |
| inactive_objects | $\mathcal{I}\setminus A(U)$ |
| contribution / contributions | Per-object packet fragments |
| contributors | Activated ids, `(priority, name)` order |
| idob_packet | Sum written to `tp.idob` |
| semantic_core | **dict only** after IdOB |
| selected_ops | list[str], stable unique |
| identity_geometry | structural_identity \| referential_identity \| semantic_identity |
| truth_relation | mood: declarative \| interrogative \| unknown |
| truth_relation_family | descriptive_state \| descriptive_locative \| descriptive_mixed \| interrogative_wh \| interrogative_polar \| unknown |
| tru_hint | TRU mood hint on TP / log |
| tru_alignment | tru_hint vs summed mood |
| overlap_near / overlap_far | Declared edges |
| overlap_mode | merge \| suppress \| blend \| coexist |
| overlap_events | Executed resolutions `{a,b,mode,fields}` |
| meaning_delta | Legacy vs split claimed fields |
| PSC / psc_violations | Contract + logged breaks |
| registry_digest | Hash of object YAML |
| residual_activated | residual_identity in $A(U)$ |
| R0–R6 | Engine gates |
| D0–D4 | Debugger gates |

Forbidden: “IdOB object” as the primitive; list `semantic_core` as canonical; six linguistic types as the catalog; importing MSL / CIE / S2M $M$ into this packet.

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
- The debugger observes the IdOB sum, $\oplus$; it never performs a second $\oplus$.

---

## 3. Architecture

### 3.1 IdOBObject catalog frame (YAML)

Validated against `support/idob_schemas/idob_object.v1.schema.json`. Live apply symbols still look like `idob.legacy:_locative_apply`. Empty `activation: {}` is legal in v1. Two helpers do not set `family = name` (`agent_action` → `residual_identity`; `modifier_resolution` → `mixed_descriptive`).

Locks: `contribution_schema` is the write bound; activation is data; apply is code; I8/I10 live in `support/idob_psc_defaults.yaml`; `family` is the algebra axis.

### 3.2 Invariants

I1 Pure activation. I2 Unique names. I3 Sum order `(priority, name)`.
I4 Mood/family rules. I5 `idob_complete == packet.complete`.
I6 `path_b_eligible == idob_complete`. I7 Replay + digest.
I8 Objects do not mutate OB-set. I9 Contested keys → overlap_events.
I10 `semantic_core` is a dict after IdOB.

### 3.3 Observed packet schema

`identity_geometry`, `truth_relation`, `truth_relation_family`, `semantic_core` (dict), `selected_ops`, `claimed_fields`, `contributors`, `contributions`, `activation_set`, `inactive_objects`, `residual_activated`, `overlap_events`, `meaning_delta`, `psc_violations`, `registry_digest`, `complete`, `tru_hint`.

This is `tp.idob` after R3/D3. Frozen. No fourth schema.

### 3.4 Flow

`… CTP → IdOB → OuBA`. TRU writes `tru_hint` and must not clobber a completed IdOB mood.

---

## 4. Engine software

`idob/sum.py` is the writer. `registry.py` loads `support/idob_objects/*.yaml`. Eight live files: copular_state, locative, mixed_descriptive, interrogative_wh, interrogative_polar, agent_action, modifier_resolution, residual_identity.

---

## 5. Log contract (`run_examples.py`)

One `--- IdOB ---` block per run. `semantic_core=` is always a dict. Values after `=` are `ast.literal_eval` safe. Also print `--- TRU ---` with `tru_hint=`.

---

## 6. Debugger contract (`pathA_dbug.py`)

Observer only. Does not import IdOB. Does not re-sum. Teaching card: `debug/primitives/IdOB.md`.

---

## 7. Synchronized roadmap

R0–R3 / D0–D3 landed. R4a catalog lift (apply may stay on legacy). R4b PSC. D4 labels. D5 optional catalog appendix. R5 MCB copies only — no MSL/CIE/S2M move. R6 new object = YAML + closed overlap.

### Gate proofs

| Gate | Proof |
|---|---|
| R2 | *Where is the book that is on the table?* ≥2 contributors, overlap_events ≠ [] |
| R3 | One IdOB writer; `semantic_core` dict |
| D3 | *The sky is blue.* one descriptive contributor, empty overlap, declarative, dict core |
| R4a | Eight YAML load; digest stable |
| R5 | MCB copies only |

---

## 8–9. File map and open items

R1–R3: `idob/*`. D1–D3: log + space summary. R4a: YAML catalog. R4b: `idob/psc.py`.

Open: mood vs family vocab; helper-vs-family lock; TRU hint-before vs confirm-after; empty activation trees; line log vs JSON sidecar.

---

## 10. One-sentence plan

**R1–R3 made the sum real; D1–D3 observe the packet; R4a names $\mathcal{I}$ as a hashed YAML catalog; the packet stays still; meaning here stays the packet.**
