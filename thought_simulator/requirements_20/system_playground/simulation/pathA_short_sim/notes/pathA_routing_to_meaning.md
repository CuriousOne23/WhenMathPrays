# pathA_routing_to_meaning.md

## 1. Purpose

This document captures our current thinking about **routing to meaning in Path A**:

- how **addressing** works (structural coordinates),
- how **routing** works (the ladder from tokens to identity),
- how **residue** is split (constraint vs basin),
- how **smoothing** is split (operations vs cues),
- how **meaning** is defined (IdOB bundle),
- and how this all connects to **TS**.

It is a **snapshot** of the present conceptual state, intended to be refined and polished later.

---

## 2. Structural basis (geometry recap)

Path A is built on **factored, independent structural spaces**:

- **SOB** → segment geometry  
- **SROB** → role geometry  
- **CnOB** → constraint geometry  
- **SmOB** → basin geometry  
- **IdOB** → identity geometry  

Let:

- $\mathcal{S}$ = SOB space (segments, struct_segments, segment_tokens)  
- $\mathcal{R}$ = SROB space (struct_roles, role_geometry)  
- $\mathcal{C}$ = CnOB space (constraints_matched, constraint_residue)  
- $\mathcal{B}$ = SmOB space (smoothing_operations, semantic_adjacent_cues, basin_residue)  
- $\mathcal{I}$ = IdOB space (identity_geometry, truth_relation, semantic_core, idob_packet)

Then the **Path A structured state space** is:  

$$
\mathcal{X}\\_\mathrm{PathA} =
\mathcal{S}
\times
\mathcal{R}
\times
\mathcal{C}
\times
\mathcal{B}
\times
\mathcal{I}
$$

This factorization and independence are demonstrated in:

- `path_ab_tst_run_cp_6-19-2026.md`  
  (Path‑A / Path‑AB test‑run logic simulation)

---

## 3. Addressing

### 3.1. What “addressing” means

**Addressing** is the act of locating a state in the Path A structured world using **coordinates across primitives**.

A Path A state for an utterance $U$ can be addressed by:

- **utterance_id** (or window id),
- **segment_id** (SOB),
- **role_id** (SROB),
- **constraint_id** (CnOB),
- **basin_id** (SmOB),
- **identity_id** (IdOB).

Conceptually:

$$
\text{Addr}(U) =
(u\_{id},
s\_{id},
r\_{id},
c\_{id},
b\_{id},
i\_{id})
$$


Each component of this address lives in its own structural space:

- $s\_{id} \in \mathcal{S}$  
- $r\_{id} \in \mathcal{R}$  
- $c\_{id} \in \mathcal{C}$  
- $b\_{id} \in \mathcal{B}$  
- $i\_{id} \in \mathcal{I}$

Addressing is **structural**: it does not depend on pipeline order, only on the factored geometry.

---

## 4. Routing (the ladder to meaning)

### 4.1. Canonical routing ladder

Routing is the **deterministic movement up a ladder** from raw tokens to identity/meaning.

For an utterance $U$:

1. **Tokens → Segments**  
   - Primitive: **SOB**  
   - Output: `struct_segments`, `segment_tokens`  
   - Operation: segmentation of the token stream into structured segments.

2. **Segments → Roles**  
   - Primitive: **SROB**  
   - Output: `struct_roles`, `role_geometry`  
   - Operation: assign roles (speaker, addressee, proposition, modifier, etc.) to segments.

3. **Roles → Constraints + constraint_residue**  
   - Primitive: **CnOB**  
   - Output: `constraints_matched`, `constraint_residue`  
   - Operation: apply structural/semantic constraints to roles and segments, leaving unresolved rule‑level mismatches as `constraint_residue`.

4. **Constraints + Cues → Basin + basin_residue**  
   - Primitive: **SmOB**  
   - Output: `smoothing_operations`, `semantic_adjacent_cues`, `basin_residue`  
   - Operation: apply named smoothing operations to semantic adjacency cues, stabilizing a basin geometry and leaving unresolved adjacency/basin signals as `basin_residue`.

5. **Basin → Identity / Meaning**  
   - Primitive: **IdOB**  
   - Output: `identity_geometry`, `truth_relation`, `semantic_core`, `idob_packet`  
   - Operation: form identity and meaning from the stabilized basin plus residues.

This ladder is the **canonical routing description**:

> **Routing to meaning = tokens → segments → roles → constraints/cues → basin → identity.**

---

## 5. Residue types (clean split)

### 5.1. Constraint residue (CnOB)

**constraint_residue** is the residue produced by **CnOB**:

- unresolved **rule‑level** mismatches,
- things that constraints could not fully resolve.

Examples (conceptual):

- interrogative_scope not fully resolved,
- modifier_chain ambiguity,
- locative_mismatch,
- tense/aspect mismatch,
- incomplete argument structure.

Constraint residue lives in **constraint geometry**:

- it is part of $\mathcal{C}$,
- it is **upstream** of basin,
- it is **rule‑centric**.

### 5.2. Basin residue (SmOB)

**basin_residue** is the residue produced by **SmOB**:

- unresolved **adjacency / basin‑level** signals,
- things that smoothing operations could not fully stabilize.

Examples (conceptual):

- underspecification_adjacent,
- conflict_adjacent,
- unstable_modality_cue,
- unresolved continuity cue.

Basin residue lives in **basin geometry**:

- it is part of $\mathcal{B}$,
- it is **downstream** of constraints,
- it is **adjacency‑centric**.

### 5.3. IdOB and residue

IdOB consumes both:

- `constraint_residue`,
- `basin_residue`,

as part of identity formation and meaning construction.

---

## 6. Smoothing (clean split)

### 6.1. Smoothing operations

**smoothing_operations** are the **named transforms** applied in SmOB.

Examples (conceptual):

- `adjacency_smoothing`,
- `continuity_smoothing`,
- `role_alignment_smoothing`,
- `segment_alignment_smoothing`,
- `basin_compression_smoothing`.

These operations:

- take semantic adjacency cues as input,
- modify basin geometry,
- attempt to stabilize the basin.

They live in **basin geometry** ($\mathcal{B}$).

### 6.2. Semantic adjacent cues

**semantic_adjacent_cues** are the **inputs** to smoothing.

Examples (conceptual):

- `locative_adjacent`,
- `state_adjacent`,
- `modality_cue`,
- `conflict_adjacent`,
- `continuity_cue`.

These cues:

- describe how segments/roles/constraints are **adjacent** in semantic space,
- guide smoothing operations,
- are part of the basin’s input structure.

### 6.3. Basin residue

After smoothing operations act on semantic adjacency cues:

- stabilized basin geometry is formed,
- unresolved signals become `basin_residue`.

So:

> **SmOB = (smoothing_operations applied to semantic_adjacent_cues) → basin geometry + basin_residue.**

---

## 7. Meaning (IdOB bundle)

### 7.1. Meaning as identity bundle

In Path A, **meaning** is defined as the **IdOB bundle**:

- `identity_geometry`,
- `truth_relation`,
- `semantic_core`,
- `idob_packet`.

This bundle is the **final product** of routing:

- it is **downstream** of SOB, SROB, CnOB, SmOB,
- it consumes `constraint_residue` and `basin_residue`,
- it lives in $\mathcal{I}$ (identity geometry).

### 7.2. Formal routing to meaning

For an utterance $U$:



$$
G(U) =
(\text{SOB}(U),
\text{SROB}(U),
\text{CnOB}(U),
\text{SmOB}(U),
\text{IdOB}(U))
$$


$$
\text{Meaning}(U) = \text{IdOB}(U) =
(\text{identity\_geometry},
\text{truth\_relation},
\text{semantic\_core},
\text{idob\_packet})
$$

Routing to meaning is:

$$
\text{RouteToMeaning}(U)
:
U
\rightarrow
G(U)
\rightarrow
\text{IdOB}(U)
$$

---

## 8. TS and windowed meaning

### 8.1. TS sees the structured world, not the pipeline

TS does not care about the **order** in which primitives ran.  
TS cares about the **structured state** $G(U)$ and its mapping into TS space.

Let:

- $\phi(G(U))$ = TS‑compatible embedding of the Path A structured state,
- $W(\phi(G(U)), t)$ = windowing over time $t$.

Then:



$$
\text{TSMeaningRoute}(U) =
W(\phi(G(U)), t)
$$



TS sees:

- independent activation tracks corresponding to $\mathcal{S}, \mathcal{R}, \mathcal{C}, \mathcal{B}, \mathcal{I}$,
- a stable manifold built on the factored geometry,
- meaning as the **windowed embedding** of the IdOB bundle plus upstream structure.

### 8.2. Independence and TS

Because:



$$
\mathcal{X}\\_\text{PathA} =
\mathcal{S}
\times
\mathcal{R}
\times
\mathcal{C}
\times
\mathcal{B}
\times
\mathcal{I}
$$



TS can:

- treat each primitive’s geometry as an independent axis,
- build windowed embeddings on a **factored manifold**,
- maintain replay determinism and window invariance.

This is why **structural independence** is key to TS.

---

## 9. Summary (current snapshot)

- The **geometry** of Path A is clean, factored, and independent.
- The **routing ladder** is: tokens → segments → roles → constraints/cues → basin → identity.
- **Residue** is split into:
  - `constraint_residue` (CnOB),
  - `basin_residue` (SmOB).
- **Smoothing** is split into:
  - `smoothing_operations` (transforms),
  - `semantic_adjacent_cues` (inputs).
- **Meaning** is defined as the **IdOB bundle**.
- **Addressing** is done via coordinates across SOB, SROB, CnOB, SmOB, IdOB.
- **TS** sees the structured world via $\phi(G(U))$ and windowing $W(\cdot, t)$.

This document is a **working capture** of our present thinking.  
We expect to refine terminology, tighten definitions, and align field names and code (e.g., `run_examples.py`) to this routing picture in subsequent revisions.
