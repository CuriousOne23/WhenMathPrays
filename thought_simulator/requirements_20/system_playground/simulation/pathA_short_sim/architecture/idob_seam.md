# IdOB seam — names, layers, and the walk from this world

**Path‑A short simulator**  
**Date:** 2026-09-28  
**Status:** lock. Read this before `idob_object_space.md`, `IdOB_unified_plan.md`, or the Identity Observation Block (IdOB) sections of `user_guide.md`.

This page is the join. It does not define the catalog and it does not define the packet writer. It stops names from trading places.

**Official expansions** (20.700.010 / 20.40): Structural Observation Block (SOB); Structural Refinement Observation Block (SROB); Constraint Observation Block (CnOB); Semantic Observation Block (SmOB); Identity Observation Block (IdOB).  
Charter: [path_a_realization_charter.md](path_a_realization_charter.md). Realization notes: `20.40.010`–`20.40.050`.

Teaching row below used older expansions (Segment / Segment Role / Smoothing). Those words remain as **aliases** after the official name. They do not replace 20.40 jobs.

---

## 1. This world, then Path A

In ordinary talk a sentence is already “about something.” *The sky is blue.* You hear words, you know the sky is the thing, blue is how it is, and the speaker is telling, not asking.

The Path‑A Thought Simulator (TS) short simulator does **not** start there. It builds a **Thought Packet (TP)** in a fixed lineup. Structure is written first. Meaning on this path is written last, as one packet. Nothing in the lineup stores a dictionary definition of “sky.”

| This world | Path A |
|---|---|
| A sentence you can say | An **utterance** (carrier string). Not meaning. |
| Words in order | Tokens / normalized text — Intake Engine (IE) |
| Chunks you can point at (*the sky*, *on the table*) | **Segment geometry** — Structural Observation Block (SOB) |
| The job of a chunk (thing talked about, place, question word) | **Structural labels** — Structural Refinement Observation Block (SROB) |
| “Does this combination hold?” | **Constraint geometry** — Constraint Observation Block (CnOB) |
| “Which pieces belong in the same picture?” | **Basin / smoothing** — Semantic Observation Block (SmOB) |
| “What claim is this, and what do we emit?” | **IdOB space + sum** — Identity Observation Block (IdOB) |
| Telling vs asking | **Truth relation** — Truth-Relation Update (TRU) hint + IdOB sum |

**IdOB does not segment, assign roles, or invent constraints.** SOB, SROB, CnOB, and SmOB already wrote those fields. An IdOB object may *claim* keys such as `theme` or `location` in its contribution. That is not the same as discovering that the sky is a noun phrase.

---

## 2. Reader roadmap

1. [README.md](../README.md) — what this folder is; five sentence families.  
2. [notes/bench_walk/00_how_to_walk.md](../notes/bench_walk/00_how_to_walk.md) — false image, stamp card, empty hook, shut Structure-to-Meaning (S2M) door. Teaching track. Does not define tokens.  
3. **This seam** — names and do-not-mix table.  
4. [user_guide.md](../user_guide.md) — run two utterances; structure column vs packet column.  
5. [idob_object_space.md](../notes/idob_object_space/idob_object_space.md) — the eight catalog families (structure of the space).  
6. [IdOB_unified_plan.md](IdOB_unified_plan.md) — meaning as the packet the sum writes; engine and debugger gates.  
7. [path_a_realization_charter.md](path_a_realization_charter.md) — lineup vs reserved 20.40 capability.

Older snapshot of the ladder (tokens → segments → roles → constraints → basin → identity): [pathA_routing_to_meaning.md](../notes/pathA_routing_to_meaning.md). Treat it as teaching voice. It must not override the packet schema in the unified plan or in `idob/sum.py`.

Canonical utterances live in [pathA_supported_sentences.md](../notes/pathA_supported_sentences.md). Examples in the IdOB docs use that set only.

---

## 3. Do not trade names

| Token | This layer | Not this |
|---|---|---|
| **Identity Observation Block (IdOB)** | Summation operator over a frozen registry. A primitive. | An object. A person. A meaning. |
| **IdOB space** $\mathcal{I}$ | Frozen registry snapshot of IdOB objects (eight YAML files under `support/idob_objects/`). | A room of meanings. The S2M six-ID landscape. |
| **IdOB object (IdOBObject)** | One catalog entry: name, family, priority, declared overlap, contribution schema, apply stub. | The book, the sky, an Actor type. |
| **idob_packet** | The one dict the sum writes onto the Thought Packet (TP). | A second packet built by the debugger. |
| **semantic_core** | A **dict** after IdOB (`theme`, `state`, `location`, …). | A list. A glossary definition. |
| **meaning_delta** | Path‑A field: legacy-writer vs split-writer diff on a few packet fields. | Structure-to-Meaning (S2M) $\Delta h$. Entropy $\Delta H\%$. Meaning Signal Layer (MSL) stance. |
| **meaning_delta_h** / $\Delta h$ | S2M instrument: $\|M_i - M_{i-1}\|$ after Cognitive Identity Envelope (CIE). Other hop. | Path‑A `meaning_delta`. |
| **Meaning Signal Layer (MSL)** | Thought Packet (TP) metadata packaging (qualifiers, stance as a cue). Other layer. | An IdOB operator. CIE. |
| **Cognitive Identity Envelope (CIE)** | S2M hop pressure $M' = M + \alpha I$. Other hop. | MSL stance. Path‑A `identity_geometry`. |
| **Meaning Composition Block (MCB)** | Full Path‑A primitive after IdOB. **Omitted** in the short sim (unified plan R5 = copy-only). | The parking lot for S2M, CIE, or MSL. |
| **Observation Block set (OB-set)** | SOB + SROB + CnOB + SmOB (+ SSG). Structure. | IdOB. |
| **Primitive Specification Contract (PSC)** | Load-time and run-time checks on catalog + contributions (`psc_violations`, `registry_digest`). | A second meaning theory. |

There is no Meaning Observation Block (MnOB) in the short-sim lineup. Meaning on this path is the mapping that **is** the packet, not a sixth Observation Block (OB).

---

## 4. Acronyms (first use in every IdOB doc)

Expand on first use in **each** document, then use the short form.

| First use | Then |
|---|---|
| Thought Simulator (TS) | TS |
| Thought Packet (TP) | TP |
| Identity Observation Block (IdOB) | IdOB |
| IdOB object (IdOBObject) | IdOBObject |
| Structural Observation Block (SOB) | SOB |
| Structural Refinement Observation Block (SROB) | SROB |
| Constraint Observation Block (CnOB) | CnOB |
| Semantic Observation Block (SmOB) | SmOB |
| Observation Block set (OB-set) | OB-set |
| Primitive Specification Contract (PSC) | PSC |
| Truth-Relation Update (TRU) | TRU |
| Output Binding / Assemble (OuBA) | OuBA |
| Meaning Signal Layer (MSL) | MSL |
| Meaning Composition Block (MCB) | MCB |
| Structure-to-Meaning (S2M) | S2M |
| Cognitive Identity Envelope (CIE) | CIE |
| Intake Engine (IE) | IE |
| YAML catalog / JSON Schema | write in full at first mention of the file |

Teaching aliases after first official use: segments (`struct_segments`), structural labels (`struct_roles`), smoothing (Job 1 operation of SmOB).

---

## 5. Hard words (three beats)

Each heading below is **this world → Path A cut → example that can be false**. If a later page says one of these words without marking the cut, the page is not done.

### Object

- This world: a thing you can point at (book, sky).  
- Path A: an **IdOBObject** — a named catalog entry that may write a fragment. The book is a *referent*, usually a `semantic_core` key such as `theme`, not an object type.  
- False friend: calling *the book* an IdOB object.

### Space

- This world: a room.  
- Path A: a frozen registry $\mathcal{I}$ or a factored geometry written by a primitive. Not a warehouse of stored meanings.  
- False friend: “IdOB space contains the meaning of the sentence.” The space contains **extractors**. The packet contains the sum.

### Adjacency (three different Path‑A uses)

Say which one, every time.

1. **String / segment adjacency** — SOB, CnOB. Chunks that sit next to each other. *book* next to *that is on the table*.  
2. **Cue / basin adjacency** — SmOB. Pieces that belong in one picture even if they are not neighbors. *the rain* and *in the plain*.  
3. **Object adjacency** — IdOB catalog `overlap.near` / `overlap.far`. Declared edges between **families**. Locative is near mixed_descriptive in YAML. That does not mean the words are neighbors. It means: if both objects fire, the sum has a named pair to record.

Worked utterance: *Where is the book that is on the table?*  
- (1) `book` touches the relative clause.  
- (2) book + table stay one locative picture.  
- (3) more than one IdOB family can fire; `overlap_events` may be nonempty.

### Packet

- This world: a parcel in the mail.  
- Path A: the one dict IdOB writes (`idob_packet` on the Thought Packet (TP)). The debugger observes it. It does not wrap a second parcel.  
- False friend: list `semantic_core` as the parcel.

### Identity

- This world: who someone is.  
- Path A: `identity_geometry` on the sum — `structural_identity` \| `referential_identity` \| `semantic_identity`. An indicator of what fired plus claimed roles. Not a biography.  
- False friend: CIE = this field.

### Meaning

- This world: what the sentence “really means.”  
- Path A short sim: the **idob_packet**. Not MSL stance, not S2M’s vector $M$, not a dictionary entry.  
- False friend: “IdOB retrieved the meaning of blue.”

### Overlap

- This world: two circles sharing area.  
- Path A: executed `overlap_events` `{a, b, mode, fields}` with mode merge \| suppress \| blend \| coexist.  
- False friend: treating declared `overlap.near` as if the event already ran. Declaration is object-space. Execution is the sum.

### Residue

- This world: leftovers.  
- Path A: named leftovers. `constraint_residue` is CnOB (rules that did not close). `basin_residue` is SmOB (picture that did not stabilize). Different primitives.  
- False friend: one pile called “residue.”

### Family

- This world: relatives.  
- Path A: catalog field `family`. For five of the eight files, `family` equals `name`. Two helper files share another family’s name (see object-space).  
- False friend: “family” = “sentence family” except where they happen to match.

### Activation

- This world: turning something on.  
- Path A: `act=1` for an IdOBObject given frozen TP structure. Live YAML currently has `activation: {}`; apply still lives in `idob.legacy`. Docs may name the slot. They must not pretend each object already carries a filled predicate tree.

---

## 6. Who writes which column

| Primitive | Writes (structure) | Does not write |
|---|---|---|
| SOB | `struct_segments`, `segment_tokens` | packet, structural labels |
| SROB | `struct_roles` | packet, constraints |
| CnOB | `constraints_matched`, `constraints_unmatched`, `constraint_residue` | packet |
| SmOB | `smoothing_operations`, `semantic_adjacent_cues`, `basin_residue` | packet |
| TRU | `tru_hint` (must not clobber a completed IdOB mood) | IdOB space |
| IdOB | `idob_packet` and the packet keys listed in the unified plan | OB-set fields (PSC: objects do not mutate the OB-set) |
| OuBA | commit / freeze of the TP | a second IdOB sum |

---

## 7. Acceptance checks for later pages

A draft of object-space, unified plan, user guide, or the debugger IdOB card **fails** if it:

- uses adjacency / object / meaning / identity without the cut above,  
- never says which primitive wrote the field,  
- teaches six object types (Actor, Action, Relation, Modifier, Constraint, Context) as the catalog,  
- shows list `semantic_core` as canonical after IdOB,  
- parks MSL, CIE, or S2M $M$ inside IdOB or inside MCB as if the short sim ran them.

A draft **passes** if a reader who only knows English sentences can point at *The sky is blue.*, say what SOB vs SROB vs IdOB each did, and not call the sky an IdOBObject.
