# Path A — IdOB object space

**Document:** `idob_object_space.md`  
**Layer:** structure of Identity Observation Block (IdOB) space $\mathcal{I}$ only  
**Date:** 2026-09-28  
**Oracle:** `support/idob_objects/*.yaml` + `support/idob_schemas/idob_object.v1.schema.json`  
**Seam:** [idob_seam.md](../../architecture/idob_seam.md)  
**Meaning / packet:** [IdOB_unified_plan.md](../../architecture/IdOB_unified_plan.md)  
**How to look:** [user_guide.md](../../user_guide.md)

This page starts in ordinary talk, then stays in the **catalog**. It does not define meaning. It does not define $\Delta h$. It does not import the Meaning Signal Layer (MSL), the Cognitive Identity Envelope (CIE), or Structure-to-Meaning (S2M).

---

## 1. This world → this page

In ordinary talk we name *who*, *what happens*, *where*, *how much*. Those are useful teaching words. They are **not** the objects in this simulator.

In the Path‑A Thought Simulator (TS) short sim, an **IdOB object (IdOBObject)** is a named catalog entry that may write a **fragment** onto a packet. The book in *The book is on the table.* is a referent (usually a `theme` or similar core key). It is not an IdOBObject.

IdOB space $\mathcal{I}$ is the frozen set of those catalog entries. Eight YAML files. The Identity Observation Block (IdOB) primitive **sums** whatever subset activates. The sum is meaning-side. This file only says what may exist and how entries are allowed to sit next to each other **as declarations**.

---

## 2. What an IdOBObject is (structure)

An IdOBObject is a YAML document validated by `idob_object.v1.schema.json`. Required slots:

| Slot | What it is in this world | What it is here |
|---|---|---|
| `name` | A label | Unique catalog id (`locative`, …) |
| `family` | Relatives | Algebra axis. Not always equal to `name` (see helpers below). |
| `priority` | Importance | Sum order key with `name` |
| `identity.label` / `tags` | Human nickname | Teaching tags only. Not a second type system. |
| `association.roles` | Jobs in the sentence | Claim-role vocabulary this object *may* speak |
| `association.geometries` | Shape of chunks | Claimed segment-shape lists. Live files currently use `[]`. |
| `activation` | On-switch | Predicate tree language. Live files currently use `{}`. Apply still lives in `idob.legacy`. |
| `contribution_schema` | What it is allowed to write | Bound on `semantic_core` keys, `selected_ops` strings, default `truth_relation_family` |
| `overlap.near` / `overlap.far` | Neighbors | **Object adjacency (3)** — declared edges, not executed events |
| `behavior.apply` | What it does | Symbol `module:function`. Live apply is still `idob.legacy:_…_apply` |
| `psc_id` / `psc_invariants` | House rules | Primitive Specification Contract (PSC) id. Live objects list `psc_invariants: []`. Shared rules live in `support/idob_schemas/idob_psc_defaults.yaml`. |

**Boundary** of an object = the schema + that YAML. A key written at run time that is not in `contribution_schema` is a PSC matter (unified plan), not a new object type.

**Interface** = `contribution_schema` + `association.roles`. Objects compose only if declared overlap and schema allow it. Composition *eligibility* is this file. Composition *result* is the packet.

**Forbidden on this page:** semantic manifold, curvature, center of mass, meaning-refinement operator, MSL, CIE, S2M $M$, calling the six linguistic labels object types.

---

## 3. The eight catalog names

These are the live files under `support/idob_objects/`. The JSON Schema `family` enum lists the same eight strings as *legal family values*. Two helper files **declare a shared family** instead of `family = name`. Document the YAML, not the wish.

| `name` | YAML `family` | `priority` | Claimed `association.roles` | Declared `overlap.near` | Declared `overlap.far` | Default `truth_relation_family` |
|---|---|---|---|---|---|---|
| `interrogative_wh` | `interrogative_wh` | 10 | query_focus, predicate | interrogative_polar | copular_state | interrogative_wh |
| `interrogative_polar` | `interrogative_polar` | 11 | query_focus, predicate | — | copular_state | interrogative_polar |
| `copular_state` | `copular_state` | 20 | theme, state | locative | — | descriptive_state |
| `locative` | `locative` | 30 | location | mixed_descriptive | — | descriptive_locative |
| `mixed_descriptive` | `mixed_descriptive` | 40 | theme, state, location | modifier_resolution | — | descriptive_state |
| `agent_action` | `residual_identity` | 50 | agent, action, patient | — | — | residual_identity |
| `modifier_resolution` | `mixed_descriptive` | 60 | theme, state, location, relation, action, patient | — | — | descriptive_mixed |
| `residual_identity` | `residual_identity` | 90 | — | — | copular_state, locative | residual_identity |

`agent_action` and `modifier_resolution` are **helper objects**. They have their own `name`. They do not get a second object-type system. Their `family` field is what YAML says.

Activation trees are empty in v1 YAML. Which object *actually* fires on an utterance is still decided in legacy apply plus whatever the registry binds. This page may list **eligibility by sentence family** as teaching, not as a filled predicate tree.

---

## 4. Claim-role vocabulary (not types)

Actor, Action, Relation, Modifier, Constraint, Context were a first-draft taxonomy. They are **not** catalog types.

They map onto keys and roles the schema already locks on `semantic_core`:

| Teaching word | Path A home | Who writes the structure that feeds it |
|---|---|---|
| Actor / thing talked about | core keys `theme`, `agent`, `patient` | SROB roles; IdOB may claim them |
| Action / what happens | core keys `action`, `predicate` | SROB; helper `agent_action` may contribute |
| Relation / how connected | `location`, `complement`, `relation_modifiers` | SROB + CnOB; `locative` may claim `location` |
| Modifier / quality or degree | `modifiers`, `relation_modifiers` | SROB; helper `modifier_resolution` |
| Constraint | **not an IdOBObject** | Constraint Observation Block (CnOB) |
| Context / frame | **not an IdOBObject** | SmOB cues + earlier metadata; not a catalog family |

Constraint and Context stay upstream. They do not become IdOB families.

---

## 5. Adjacency here means object adjacency

See the seam for the three Path‑A uses of **adjacency**.

This file only owns **(3) object adjacency**:

- Declared in YAML as `overlap.near` and `overlap.far`.  
- Not segment neighbors.  
- Not basin cues.  
- Not `overlap_events`. Those are executed in `idob/packets.py` / `idob/sum.py` and belong to the unified plan.

Example: `locative.overlap.near` includes `mixed_descriptive`. If both fire on one utterance, the sum may record an event for that pair. The declaration does not by itself write the packet.

---

## 6. Structure-only examples

Utterances from [pathA_supported_sentences.md](../pathA_supported_sentences.md). This section says **which catalog names are in play as teaching**, not what `semantic_core` contains.

### 6.1 *The sky is blue.*

This world: someone tells you the sky’s color.

| Primitive | What it did (structure) |
|---|---|
| Segment Observation Block (SOB) | Chunks such as a noun phrase and a state complement |
| Segment Role Observation Block (SROB) | Theme vs state jobs |
| Constraint Observation Block (CnOB) | Copular / state constraints can close |
| Smoothing Observation Block (SmOB) | Little leftover picture-work |
| IdOB catalog | `copular_state` is the family this sentence family was built for |

Object adjacency: typically one descriptive contributor. Declared near-edges need not fire.

### 6.2 *The book is on the table.*

This world: someone tells you where the book is.

| Primitive | What it did |
|---|---|
| SOB | Entity chunk + locative chunk |
| SROB | Theme / location jobs |
| CnOB | Locative attachment |
| SmOB | Book and table in one picture |
| IdOB catalog | `locative` (and often `copular_state` as a near neighbor in the catalog) |

String adjacency: *on the table* sits on the entity.  
Object adjacency: `copular_state` declares near `locative`. That is catalog geometry, not word order.

### 6.3 *Where is the book that is on the table?*

This world: someone asks where the book is, and also pins the book with a relative clause.

| Primitive | What it did |
|---|---|
| SOB | Question word, entity, locative, relative material |
| SROB | Query focus + entity + location |
| CnOB | Interrogative scope + locative attachment |
| SmOB | Book + table remain one picture while the question wraps them |
| IdOB catalog | `interrogative_wh` plus locative / descriptive families may all be eligible |

Three adjacencies at once (seam §5):  
(1) *book* touches the clause.  
(2) book + table stay one picture.  
(3) more than one IdOB name can be active; executed overlap is a packet field, not this page.

---

## 7. Composition eligibility (not the packet)

Objects may compose when:

- each is in $\mathcal{I}$,  
- schemas list the keys they will write,  
- declared overlap covers the pair if both activate,  
- PSC shared defaults still hold (no OB-set mutation; `semantic_core` remains a dict after IdOB).

The composed **result** is `idob_packet`. That result is not specified here.

---

## 8. What this file will not grow into

- No MSL chapter.  
- No CIE / $M' = M + \alpha I$.  
- No S2M six-axis stand-in.  
- No six-type “foundational basis” that rivals the eight files.  
- No debugger second sum.

If a sentence on this page cannot be pointed at a YAML field or at SOB/SROB/CnOB/SmOB, it belongs somewhere else.
