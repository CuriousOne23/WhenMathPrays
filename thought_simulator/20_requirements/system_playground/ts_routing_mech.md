# ts_routing_mech.md  
**Title:** TS Routing Mechanics  
**Scope:** Architectural description of TP→OB→RB routing, pre‑semantic OB layers, geometric requirements, and applicability to Path A and Path B.  
**Status:** Playground (non‑normative, no HLRs).

---

## 1. Purpose and role of routing in TS

TS separates **interpretation** and **realization** into two paths:

- **Path A:** interpretation (meaning, structure, operators, constraints)  
- **Path B:** realization (reasoning, planning, execution, formatting)

Routing lives entirely in **Path A**.

The purpose of routing is to:

- **select the right OBs** for a given TP and residue  
- do so in a **deterministic, geometric, monotonic** way  
- ensure **no guessing, no drift, no hallucination**  
- keep Path B free of any interpretive work

This document describes:

- the **TP→SOB→RB→OB** routing loop  
- the **four pre‑semantic OB layers** (SOB, PrSOB, CrOB, FsOB)  
- the **geometric requirements** of the OB address space  
- how this applies to **Path A**  
- why **Path B has no OB/RB layer and must never have one**

---

## 2. Core routing loop: TP → SOB → RB → OB

### 2.1 High‑level flow

At the highest level, Path A routing is:

```text
TP_in → SOB (structural OBs) → RB (routing block) → OB (selected OB or OB set) → RB (again, with new residue) → OB (next OB) → ...→ TP_out (fully interpreted, ready for Path B)
```

The loop is:

1. **TP_in:** a thought packet (TP) enters Path A.  
2. **SOB:** structural OBs extract structure and initial hints.  
3. **RB:** the routing block takes residue and computes an address query.  
4. **OB:** the best‑matching OB(s) are selected based on geometric similarity.  
5. **OB execution:** the OB transforms the TP and leaves new residue.  
6. **RB:** routing repeats until no meaningful residue remains.  
7. **TP_out:** a fully interpreted, structured, constrained representation is produced.

Path B receives **TP_out**, not raw user text.

---

### 2.2 Residue and address fragments

Routing is driven by **residue**.

- **TP:** the current structured representation.  
- **Residue:** what is *not yet resolved*—uninterpreted structure, unresolved operators, missing constraints, etc.

The RB:

1. **Extracts fragments** from residue (structure, operators, domain hints, constraints, tone, etc.).  
2. **Hashes fragments** into address fragments.  
3. **Combines fragments** (e.g., via XOR) into a **query address**.  
4. **Compares** the query address to OB addresses in the OB space.  
5. **Applies a geometric similarity function** to select OBs.

The key idea:  
> Routing is **address‑based**, not token‑based.

---

### 2.3 OB addresses and XOR‑based combination

Each OB has a **fixed address** in the OB space.

- OB addresses are **sparse**, **stable**, and **semantically meaningful**.  
- Residue fragments are hashed into **address fragments**.  
- The RB combines fragments (e.g., via XOR) into a **query address**.

Conceptually:

```text
fragment_1_hash ⊕ fragment_2_hash ⊕ ... ⊕ fragment_n_hash = query_address
```

Then:

```text
similarity(query_address, OB_address_i) → score_i
```

Routing selects OBs based on these scores, subject to geometric constraints (Section 4).

---

### 2.4 Routing thresholds and partial matches

Routing is not binary; it is **thresholded**:

- **route:** similarity ≥ high_threshold  
- **maybe:** low_threshold ≤ similarity < high_threshold  
- **no:** similarity < low_threshold  

This allows:

- **strong matches** → direct routing  
- **partial matches** → cautious routing or fallback  
- **no matches** → safe failure or generic handling

Partial matches are still governed by the **same geometric rules** (monotonic, smooth, curvature‑invariant).

---

## 3. The four pre‑semantic OB layers

Before deep semantic OBs, Path A passes through four foundational OB layers:

1. **SOB — Structural OBs**  
2. **PrSOB — Pre‑Semantic OBs**  
3. **CrOB — Constraint OBs**  
4. **FsOB — First‑Semantic OBs**

These layers progressively:

- extract structure  
- refine hints  
- make constraints explicit  
- begin semantic extraction  

They ensure that **deep semantic OBs never guess**.

---

### 3.1 SOB — Structural OBs

**Role:** Extract **structure before meaning**.

**What SOBs do:**

- **Segmentation:**  
  - sentences, clauses, lists, tables, code blocks  
- **Grammar and modality hints:**  
  - questions, commands, conditionals, hypotheticals  
- **Operator hints:**  
  - summarize, derive, classify, plan, compare, explain  
- **Domain hints:**  
  - math‑like, narrative‑like, code‑like, legal‑like, etc.  
- **Tone/subculture hints:**  
  - formal, casual, technical, supportive, etc.  
- **Constraint hints:**  
  - precision, safety, conciseness, politeness, etc.

**Trip level:**  
- **Always first.** Every message goes through SOBs.  

**Output:**  
- A structured TP + residue that is now **addressable**.

SOBs do **not** interpret meaning; they prepare the message for interpretation.

---

### 3.2 PrSOB — Pre‑Semantic OBs

**Role:** Refine the coarse hints from SOBs without yet extracting meaning.

**What PrSOBs do:**

- **Sharpen domain classification**  
  - e.g., “math‑like” → “symbolic algebra” vs “probability”  
- **Sharpen operator classification**  
  - e.g., “explain” vs “derive” vs “compare”  
- **Refine tone/subculture**  
  - e.g., “technical‑supportive” vs “formal‑academic”  
- **Normalize structure**  
  - clean up segmentation, remove noise, standardize forms  
- **Detect contradictions**  
- **Detect missing metadata**  
- **Detect implicit operators and constraints**  
- **Reduce entropy** in the residue

**Trip level:**  
- Triggered when SOBs leave **non‑trivial residue** with ambiguous or incomplete metadata.

**Output:**  
- A **cleaner, sharper, lower‑entropy residue**.

PrSOBs are the **semantic staging area**.

---

### 3.3 CrOB — Constraint OBs

**Role:** Extract and enforce **constraints** that shape downstream semantic interpretation.

**What CrOBs do:**

- **Precision level**  
  - informal intuition vs rigorous derivation  
- **Determinism level**  
  - exploratory vs definitive  
- **Safety constraints**  
  - content boundaries, risk levels  
- **Politeness and tone constraints**  
- **Conciseness and verbosity constraints**  
- **Formatting constraints**  
  - bullet lists, tables, code, proofs, etc.  
- **Domain‑specific constraints**  
  - legal formality, medical caution, mathematical rigor, etc.

**Trip level:**  
- Triggered when residue contains **explicit or implicit constraints**.

**Output:**  
- A residue with **explicit constraints and no hidden assumptions**.

CrOBs ensure that semantic OBs operate within **clear, stable boundaries**.

---

### 3.4 FsOB — First‑Semantic OBs

**Role:** Perform the **first layer of true semantic extraction**.

FsOBs are not deep semantic OBs; they are the **first interpreters**.

**What FsOBs do:**

- Extract **high‑level meaning**  
- Identify **semantic roles**  
- Identify **entities**  
- Identify **relationships**  
- Identify **intent**  
- Identify **semantic operators**  
- Produce **structured semantic fragments**

**Trip level:**  
- Triggered when structure, domain, operators, and constraints are **sufficiently refined**.

**Output:**  
- A **partially interpreted semantic structure** + remaining residue.

After FsOBs, the system can safely route into **domain‑specific semantic OBs** and **fine‑semantic OBs**.

---

## 4. Geometric requirements of the OB address space

Routing in TS is not heuristic; it is **geometric**.

For routing to be:

- stable  
- deterministic  
- drift‑free  
- replayable  

…the OB address space and similarity function must satisfy strict geometric properties.

---

### 4.1 Monotonicity

If similarity increases, routing confidence must **never decrease**.  
If similarity decreases, routing confidence must **never increase**.

Formally:

- Let $ d $ be a distance (or dissimilarity) measure.  
- Let $ f(d) $ be the routing confidence (or similarity score).  

Then:

- If $ d_1 < d_2 $, then $ f(d_1) \ge f(d_2) $.  

This prevents:

- routing chaos  
- oscillation  
- non‑deterministic jumps  
- “why did it pick that OB?” behavior

Monotonicity is the **stability guarantee**.

---

### 4.2 Smoothness

The similarity gradient must be **smooth**:

- no sharp kinks  
- no discontinuities  
- no sudden jumps in routing confidence  

Small changes in residue → **small changes** in routing behavior.

This ensures:

- graceful partial matches  
- predictable threshold behavior  
- no “cliff effects” where tiny changes cause huge routing shifts

---

### 4.3 Curvature invariance (predictable geometry)

This is the deeper requirement:

> **Same distance → same slope → same curvature → same routing behavior.**

For any OB (including FsOB1, FsOB2, etc.):

- If a random message is at distance $ d $ from OB1  
- And another random message is at distance $ d $ from OB1  

Then:

- the **value** of the similarity  
- the **first derivative** (slope)  
- the **second derivative** (curvature)  

must all be **identical**.

This must hold:

- for all OBs  
- for all layers (SOB, PrSOB, CrOB, FsOB, semantic OBs)  
- for all directions in the address space

This is what makes the routing space a **true metric space** with consistent meaning.

---

### 4.4 OB‑invariant geometry

The similarity function and its derivatives must be **OB‑invariant**:

- FsOB1 and FsOB2 must behave identically at the same distance.  
- No OB is “more sensitive” or “less sensitive” than another at the same similarity score.  
- The shape of the gradient is **universal**.

This guarantees:

- deterministic routing  
- stable partial matches  
- predictable fallback  
- zero drift  
- perfect replay

---

### 4.5 Why this makes TS efficient

Because TS is **not** searching all possible meanings.

It is searching a **small, structured, geometric address space** that is:

- monotonic  
- smooth  
- curvature‑invariant  
- OB‑invariant  

Transformers operate in:

- dense  
- entangled  
- non‑monotonic  
- non‑geometric  

vector spaces.

TS operates in:

- sparse  
- structured  
- geometric  

address spaces.

This is why TS can be:

- smaller  
- cheaper  
- deterministic  
- hallucination‑free  
- CPU‑friendly

---

## 5. Applicability to Path A and Path B

### 5.1 Path A: where routing lives

Path A is the **only** place where:

- OBs exist  
- RBs exist  
- routing happens  
- residue is extracted  
- addresses are computed  
- geometric similarity is applied  

Path A is the **semantic front‑end**:

```text
User Input
  → TP_in
  → SOB → PrSOB → CrOB → FsOB → semantic OBs
  → TP_out (fully interpreted)
  → Path B
```

All interpretation, classification, and disambiguation **must** happen in Path A.

---

### 5.2 Path B: deterministic realization, no OBs, no routing

Path B is a **deterministic realization path**.

Current primitive flow (horizontal):

```text
LI‑prm → REx‑prm → RPlan‑prm → RPU‑prm → ReB‑prm → [Sty‑prm / Vo‑prm / Ti‑prm / Ch‑prm] → CE → ISc
```

**Key properties:**

- no OBs  
- no RBs  
- no routing  
- no residue  
- no addressing  
- no geometric similarity  

Path B:

- executes reasoning  
- applies operators  
- follows a plan  
- bundles results  
- formats output  
- validates against instructions

Path B **does not interpret meaning**.

---

### 5.3 Architectural invariant: Path B must never have OBs or routing

This is a core architectural rule:

> **Invariant:** Path B must never contain OBs, RBs, routing, residue, addressing, or any semantic interpretation mechanism.  
> If Path B appears to need interpretation, that logic must be moved into Path A.

Rationale:

- Interpretation is **non‑deterministic, branching, semantic**.  
- Path B must be **deterministic, linear, execution‑only**.  
- If Path B starts interpreting, you get:  
  - semantic drift  
  - double interpretation  
  - inconsistent meaning  
  - circular dependencies  
  - loss of replay and correctness

Therefore:

- **All OB/RB work belongs in Path A.**  
- **Path B must remain OB‑free and routing‑free.**

---

## 6. Summary

- TS separates **interpretation (Path A)** from **realization (Path B)**.  
- Routing is a **Path A‑only** concern.  
- The core loop is **TP → SOB → RB → OB → … → TP_out**.  
- Routing is driven by **residue**, **address fragments**, and **XOR‑based addressing**.  
- The OB address space must be **monotonic, smooth, curvature‑invariant, and OB‑invariant**.  
- The four pre‑semantic OB layers (SOB, PrSOB, CrOB, FsOB) prepare the TP so deep semantic OBs never guess.  
- Path B is a **deterministic reasoning pipeline** with **no OBs and no routing**.  
- If Path B ever appears to need OBs or routing, that is a design error—**the work must be pushed back into Path A**.

This document is the **playground‑level architectural description** of TS routing mechanics and the separation of concerns between Path A and Path B.
```
