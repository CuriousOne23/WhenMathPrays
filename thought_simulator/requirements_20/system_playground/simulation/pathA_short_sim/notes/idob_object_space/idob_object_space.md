# Path A — IdOB object space

**Document:** `idob_object_space.md`  
**Layer:** structure of Identity Observation Block (IdOB) space $\mathcal{I}$ only  
**Date:** 2026-09-28  
**Oracle:** `support/idob_objects/*.yaml` + `support/idob_schemas/idob_object.v1.schema.json`  
**Seam:** [idob_seam.md](../../architecture/idob_seam.md)  
**Meaning / packet:** [IdOB_unified_plan.md](../../architecture/IdOB_unified_plan.md)  
**How to look:** [user_guide.md](../../user_guide.md)

This page starts in ordinary hearing, then stays in the **catalog**. It does not define meaning. It does not define $\Delta h$. It does not import the Meaning Signal Layer (MSL), the Cognitive Identity Envelope (CIE), or Structure-to-Meaning (S2M).

Official expansions: Structural Observation Block (SOB), Structural Refinement Observation Block (SROB), Constraint Observation Block (CnOB), Semantic Observation Block (SmOB), Identity Observation Block (IdOB).

---

## 0. Why “structure” is hard to see

You already do structure. You just never have to look at it. In a human listener it finishes before you notice you started.

Someone says: *The book is on the table.*  
You do not experience four jobs. You experience one picture: a book, a table, the book located there, told not asked. That picture arriving whole is why “structure” can feel fake. The work is real; it is silent.

If you slow the same hearing down, the silent work is things like:

- these sounds are words, in this order  
- *the book* hangs together as one chunk, *on the table* as another  
- *book* is the thing being placed; *table* is the place  
- *is* + *on* can close as “location of a thing,” not as “the book *is* the table”  
- book and table belong in one picture, even though they are not the same word  

Path A calls that silent work **structure**. It is not the meaning “there is a book on a table.” It is the **shape that makes that meaning possible**.

Your mind does the shape and the “what it is about” in one motion. The simulator cannot. If it jumps from the raw string to “meaning,” there is no place to see where it went wrong and no replay. So Path A forces a pause: write the grouping and fitting down **before** IdOB is allowed to say what the sentence is about.

A usable sentence:

> Structure is the part of hearing a sentence that is already finished when I notice I understood — the grouping and fitting — written down before the simulator is allowed to say what the sentence is about.

Same words, different silent shape (you already feel this):

- *The book is on the table.* vs *Is the book on the table?* — telling vs asking.  
- *The book that is on the table is blue.* vs *The book is on the table that is blue.* — which clause sticks to which noun.

That difference is structure. Ordinary talk never hands it to you as an object. Path A **externalizes** a step that, in you, is implied and automatic.

---

## 0.1 Where the layers live (read this before §3 and §4)

Nothing in §3–§4 is a new kind of sentence. They are **different writings on the same walk**, in different places.

Imagine the utterance as a spoken line. Path A then makes three notebooks:

| Layer | Where it lives | What you can point at | This page? |
|---|---|---|---|
| **U — utterance** | Intake fields on the Thought Packet (TP): the carrier string / tokens | *The book is on the table.* as sounds or letters | Named only |
| **S — OB-set structure** | TP fields written by SOB, SROB, CnOB, SmOB | Chunks, structural labels, constraints, adjacent cues | Used in examples; owned by those primitives |
| **C — catalog (§3)** | Eight YAML files under `support/idob_objects/` | Named extractors (`locative`, `copular_state`, …) | **This file owns C** |
| **K — claim keys (§4)** | Keys an extractor is *allowed to speak* on the packet (`theme`, `location`, …) | Not objects. Not chunks. Vocabulary. | **This file translates K** |
| **P — packet** | `idob_packet` after IdOB sums whoever fired | Meaning on this path | Unified plan, not this file |

How to stand in the stack:

- You **hear** U.  
- The machine **writes** S onto the TP (the silent grouping, now visible).  
- §3 lists the **tools** that may read S and emit a fragment (§3 objects live in YAML, not in the sentence).  
- §4 lists **words we used to treat as types** and shows they are either keys on those tools (K) or they stay on layer S (Constraint, Context).  
- IdOB **sums** into P. This page does not describe P.

§3 and §4 are not two catalogs. §3 is the drawer of tools. §4 is the labels those tools may write — plus two old labels that never became tools.

---

## 1. This world → this page

In ordinary talk we name *who*, *what happens*, *where*, *how much*. Those are useful teaching words. They are **not** the objects in this simulator. They belong to layer K or to layer S (§4).

In the Path‑A Thought Simulator (TS) short sim, an **IdOB object (IdOBObject)** is a named catalog entry (layer C) that may write a **fragment** onto a packet. The book in *The book is on the table.* is a referent (usually a `theme` or similar core key on layer K). It is not an IdOBObject.

IdOB space $\mathcal{I}$ is the frozen set of those catalog entries. Eight YAML files. The Identity Observation Block (IdOB) primitive **sums** whatever subset activates. The sum is meaning-side (layer P). This file only says what may exist on C and how entries are allowed to sit next to each other **as declarations**.

---

## 2. What an IdOBObject is (structure of a catalog entry)

This section is still layer C: the shape of **one tool in the drawer**, not the shape of the sentence (that is layer S).

An IdOBObject is a YAML document validated by `idob_object.v1.schema.json`. Required slots:

| Slot | What it is in this world | What it is here |
|---|---|---|
| `name` | A label | Unique catalog id (`locative`, …) |
| `family` | Relatives | Algebra axis. Not always equal to `name` (see helpers below). |
| `priority` | Importance | Sum order key with `name` |
| `identity.label` / `tags` | Human nickname | Teaching tags only. Not a second type system. |
| `association.roles` | Jobs in the sentence | Claim-role vocabulary this object *may* speak (layer K) |
| `association.geometries` | Shape of chunks | Claimed segment-shape lists. Live files currently use `[]`. |
| `activation` | On-switch | Predicate tree language. Live files currently use `{}`. Apply still lives in `idob.legacy`. |
| `contribution_schema` | What it is allowed to write | Bound on `semantic_core` keys, `selected_ops` strings, default `truth_relation_family` |
| `overlap.near` / `overlap.far` | Neighbors | **Object adjacency (3)** — declared edges between catalog entries, not executed events |
| `behavior.apply` | What it does | Symbol `module:function`. Live apply is still `idob.legacy:_…_apply` |
| `psc_id` / `psc_invariants` | House rules | Primitive Specification Contract (PSC) id. Live objects list `psc_invariants: []`. Shared rules live in `support/idob_schemas/idob_psc_defaults.yaml`. |

**Boundary** of an object = the schema + that YAML. A key written at run time that is not in `contribution_schema` is a PSC matter (unified plan), not a new object type.

**Interface** = `contribution_schema` + `association.roles`. Objects compose only if declared overlap and schema allow it. Composition *eligibility* is this file. Composition *result* is the packet.

**Forbidden on this page:** semantic manifold, curvature, center of mass, meaning-refinement operator, MSL, CIE, S2M $M$, calling the six linguistic labels object types.

---

## 3. The eight catalog names (layer C — the tools)

These are the live files under `support/idob_objects/`. They do not live inside the utterance. They live in the registry. When an utterance arrives, some subset may *activate* and read layer S.

The JSON Schema `family` enum lists the same eight strings as *legal family values*. Two helper files **declare a shared family** instead of `family = name`. Document the YAML, not the wish.

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

`family` here is the catalog algebra axis (a field on a tool). It is not “sentence family” (copular / locative / interrogative as kinds of utterance).

---

## 4. Claim-role vocabulary (layer K — not a second drawer of tools)

**Bridge from §3.** Section 3 named eight extractors. Section 4 does not name eight more. It answers: *the old teaching words Actor, Action, Relation, Modifier, Constraint, Context — if they are not tools, what are they?*

They are **not** catalog types and **not** families. They map onto keys the schema already locks on `semantic_core` (layer K), except the last two, which never leave layer S:

| Teaching word | Path A home | Layer | Who writes the structure that feeds it |
|---|---|---|---|
| Actor / thing talked about | core keys `theme`, `agent`, `patient` | K (claimed by a §3 object) | SROB labels; IdOB may claim them |
| Action / what happens | core keys `action`, `predicate` | K | SROB; helper `agent_action` may contribute |
| Relation / how connected | `location`, `complement`, `relation_modifiers` | K | SROB + CnOB; `locative` may claim `location` |
| Modifier / quality or degree | `modifiers`, `relation_modifiers` | K | SROB; helper `modifier_resolution` |
| Constraint | **not an IdOBObject** | S (stays upstream) | Constraint Observation Block (CnOB) |
| Context / frame | **not an IdOBObject** | S (stays upstream) | SmOB cues + earlier metadata; not a catalog family |

Constraint and Context stay on the OB-set. They do not become IdOB families. You will not find a YAML file named `constraint` or `context` under `support/idob_objects/`.

Feeling for the cut on *The book is on the table.*:

- Layer S: SOB chunks *the book* and *on the table*; SROB marks theme / location jobs.  
- Layer C: tools that may wake — often `locative`, sometimes `copular_state` as a declared neighbor.  
- Layer K: those tools may claim keys such as `theme` and `location`. The book is a referent under `theme`, not a tool.

---

## 5. Adjacency here means object adjacency

See the seam for the three Path‑A uses of **adjacency**.

This file only owns **(3) object adjacency** (edges on layer C):

- Declared in YAML as `overlap.near` and `overlap.far`.  
- Not segment neighbors (layer S, string adjacency).  
- Not basin cues (layer S, SmOB).  
- Not `overlap_events`. Those are executed in `idob/packets.py` / `idob/sum.py` and belong to the unified plan (layer P).

Example: `locative.overlap.near` includes `mixed_descriptive`. If both fire on one utterance, the sum may record an event for that pair. The declaration does not by itself write the packet.

---

## 6. Structure-only examples

Utterances from [pathA_supported_sentences.md](../pathA_supported_sentences.md). This section says **which catalog names are in play as teaching**, not what `semantic_core` contains.

Walk each example as U → S → C. K and P are mentioned only so they are not mistaken for C.

### 6.1 *The sky is blue.*

This world: someone tells you the sky’s color.

| Primitive | Layer | What it did |
|---|---|---|
| Structural Observation Block (SOB) | S | Chunks such as a noun phrase and a state complement |
| Structural Refinement Observation Block (SROB) | S | Theme vs state jobs (structural labels) |
| Constraint Observation Block (CnOB) | S | Copular / state constraints can close |
| Semantic Observation Block (SmOB) | S | Little leftover picture-work |
| IdOB catalog | C | `copular_state` is the family this sentence family was built for |

Object adjacency: typically one descriptive contributor. Declared near-edges need not fire.

### 6.2 *The book is on the table.*

This world: someone tells you where the book is.

| Primitive | Layer | What it did |
|---|---|---|
| SOB | S | Entity chunk + locative chunk |
| SROB | S | Theme / location jobs |
| CnOB | S | Locative attachment |
| SmOB | S | Book and table in one picture |
| IdOB catalog | C | `locative` (and often `copular_state` as a near neighbor in the catalog) |

String adjacency: *on the table* sits on the entity (layer S).  
Object adjacency: `copular_state` declares near `locative` (layer C). That is catalog geometry, not word order.

### 6.3 *Where is the book that is on the table?*

This world: someone asks where the book is, and also pins the book with a relative clause.

| Primitive | Layer | What it did |
|---|---|---|
| SOB | S | Question word, entity, locative, relative material |
| SROB | S | Query focus + entity + location |
| CnOB | S | Interrogative scope + locative attachment |
| SmOB | S | Book + table remain one picture while the question wraps them |
| IdOB catalog | C | `interrogative_wh` plus locative / descriptive families may all be eligible |

Three adjacencies at once (seam §5):  
(1) *book* touches the clause (S).  
(2) book + table stay one picture (S).  
(3) more than one IdOB name can be active (C); executed overlap is a packet field (P), not this page.

---

## 7. Composition eligibility (not the packet)

Objects may compose when:

- each is in $\mathcal{I}$,  
- schemas list the keys they will write,  
- declared overlap covers the pair if both activate,  
- PSC shared defaults still hold (no OB-set mutation; `semantic_core` remains a dict after IdOB).

The composed **result** is `idob_packet` (layer P). That result is not specified here.

---

## 8. What this file will not grow into

- No MSL chapter.  
- No CIE / $M' = M + \alpha I$.  
- No S2M six-axis stand-in.  
- No six-type “foundational basis” that rivals the eight files.  
- No debugger second sum.

If a sentence on this page cannot be pointed at a YAML field or at SOB/SROB/CnOB/SmOB, it belongs somewhere else.
