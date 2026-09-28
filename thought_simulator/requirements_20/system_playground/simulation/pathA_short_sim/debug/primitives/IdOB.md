# IdOB

### Identity Observation Block — Path‑A short simulator teaching card

**Seam:** [../../architecture/idob_seam.md](../../architecture/idob_seam.md)  
**Space:** [../../notes/idob_object_space/idob_object_space.md](../../notes/idob_object_space/idob_object_space.md)  
**Packet contract:** [../../architecture/IdOB_unified_plan.md](../../architecture/IdOB_unified_plan.md)

## 1. This world → this primitive

This world: after you have heard the chunks of a sentence, something in you settles *what is being claimed* and *whether it was told or asked*.

Path A: the Identity Observation Block (IdOB) does **not** hear the words first. Segment Observation Block (SOB), Segment Role Observation Block (SROB), Constraint Observation Block (CnOB), and Smoothing Observation Block (SmOB) already wrote structure onto the Thought Packet (TP). IdOB is the **summation operator** over a frozen catalog. It writes one `idob_packet`. It is not an object. The debugger must not sum again.

## 2. Inputs (structure someone else wrote)

Geometry sources:

- `identity_geometry` — [../dimensions/identity_geometry.md](../dimensions/identity_geometry.md)
- `semantic_core` — [../dimensions/semantic_core.md](../dimensions/semantic_core.md) (after IdOB this is a **dict**)
- `truth_relation` — [../dimensions/truth_relation.md](../dimensions/truth_relation.md)

Canonical fields consumed (not rewritten as OB-set):

- `struct_segments`, `segment_tokens` — SOB  
- `struct_roles` — SROB  
- `constraints_matched`, `constraints_unmatched`, `constraint_residue` — CnOB  
- `smoothing_operations`, `semantic_adjacent_cues`, `basin_residue` — SmOB  
- `tru_hint` — Truth-Relation Update (TRU)

## 3. Outputs (the packet)

- `idob_packet` — the sum  
- `identity_geometry` — structural_identity \| referential_identity \| semantic_identity  
- `truth_relation` — declarative \| interrogative \| unknown  
- `truth_relation_family`  
- `semantic_core` — **dict** (`theme`, `state`, `location`, …). Never a list as canonical.  
- `activation_set`, `contributors`, `contributions`  
- `inactive_objects`, `residual_activated`  
- `overlap_events` — executed object adjacency  
- `meaning_delta` — legacy vs split field diff (not Structure-to-Meaning $\Delta h$)  
- `psc_violations`, `registry_digest`, `complete`, `tru_hint`

Field card: [../fields/idob_packet.md](../fields/idob_packet.md).

## 4. Structural function

IdOB activates a subset $A(U)$ of the eight catalog files, merges fragments with dict-only `semantic_core`, applies declared overlap as `overlap_events`, and writes one packet. Primitive Specification Contract (PSC): objects do not mutate the Observation Block set (OB-set).

## 5. Minimal examples

### *The sky is blue.*

Structure already on the TP: theme + state segments and roles.

```text
activation_set includes a descriptive family (copular_state)
overlap_events = []
truth_relation = declarative
semantic_core = { ... dict, not a list ... }
```

### *Where is the book that is on the table?*

```text
activation_set may include interrogative_wh plus locative / descriptive names
overlap_events may be nonempty
truth_relation = interrogative
semantic_core is still a dict
```

Do not call the book an IdOB object. Adjacency in `overlap_events` is **object** adjacency (catalog), not word neighbors.

## 6. Cross-primitive interaction

- Preceding: SmOB (and TRU earlier for `tru_hint`).  
- Following in this short sim: Output Binding / Assemble (OuBA). Meaning Composition Block (MCB) omitted.  
- Pipeline: `SOB → SROB → CnOB → SmOB → IdOB`.

## 7. Notes for debugging

- Typical miss: treating list `semantic_core` as legal after IdOB. That is PSC I10.  
- Typical miss: debugger re-merging contributions.  
- Typical miss: six linguistic types (Actor, Action, …) as catalog names.  
- Validate: packet keys match `identity_geometry`, `truth_relation`, dict `semantic_core`, and `activation_set`.
