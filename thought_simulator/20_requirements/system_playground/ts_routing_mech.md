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
- the **four pre‑semantic OB layers** (SOB, SROB, CnOB, SmOB)  
- the **geometric requirements** of the OB address space  
- how this applies to **Path A**  
- why **Path B has no OB/RB layer and must never have one**

---

## 2. Core routing loop: TP → SOB → RB → OB

### 2.1 High‑level flow

At the highest level, Path A routing is:

```text
TP_in
  → SOB (structural OBs)
  → RB (routing block)
  → OB (selected OB or OB set)
  → RB (again, with new residue)
  → OB (next OB)
  → ...
  → TP_out (fully interpreted, ready for Path B)
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
2. **SROB — Structural‑Refinement OBs**  
3. **CnOB — Constraint OBs**  
4. **SmOB — Semantic OBs (entry layer)**

These layers progressively:

- extract structure  
- refine structure  
- make constraints explicit  
- begin semantic extraction  

They ensure that **deep semantic OBs never guess**.

---

## 3.1 SOB — Structural OBs

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

## 3.2 SROB — Structural‑Refinement OBs

**Role:** Refine the structural output of SOBs.

**What SROBs do:**

- sharpen segmentation  
- normalize structure  
- reduce structural ambiguity  
- identify implicit structural operators  
- detect missing structural metadata  
- reduce structural entropy  
- prepare residue for constraint extraction and semantic entry

**Trip level:**  
- Triggered when SOBs leave **non‑trivial structural residue**.

**Output:**  
- A **cleaner, sharper, lower‑entropy structural residue**.

SROBs are the **structural cleanup and sharpening layer**.

---

## 3.3 CnOB — Constraint OBs

**Role:** Extract and enforce **constraints** that shape downstream semantic interpretation.

**What CnOBs do:**

- **Precision level**  
- **Determinism level**  
- **Safety constraints**  
- **Politeness and tone constraints**  
- **Conciseness and verbosity constraints**  
- **Formatting constraints**  
- **Domain‑specific constraints**

**Trip level:**  
- Triggered when residue contains **explicit or implicit constraints**.

**Output:**  
- A residue with **explicit constraints and no hidden assumptions**.

CnOBs ensure that semantic OBs operate within **clear, stable boundaries**.

---

## 3.4 SmOB — Semantic OBs (entry layer)

**Role:** Perform the **first layer of semantic extraction**.

SmOBs are the **semantic entry point**, not the deep semantic OBs.

**What SmOBs do:**

- extract **high‑level meaning**  
- identify **semantic roles**  
- identify **entities**  
- identify **relationships**  
- identify **intent**  
- identify **semantic operators**  
- produce **structured semantic fragments**

**Trip level:**  
- Triggered when structure and constraints are sufficiently refined.

**Output:**  
- A **partially interpreted semantic structure** + remaining residue.

After SmOBs, the system can safely route into **domain‑specific semantic OBs** and **fine‑semantic OBs**.

---

## 4. Geometric requirements of the OB address space

Routing in TS is not heuristic; it is **geometric**.

For routing to be:

- stable  
- deterministic  
- drift‑free  
- replayable  
- predictable  

…the OB address space and similarity function must satisfy strict geometric properties.

---

### 4.1 Monotonicity

If similarity increases, routing confidence must **never decrease**.  
If similarity decreases, routing confidence must **never increase**.

This prevents:

- routing chaos  
- oscillation  
- non‑deterministic jumps  
- “why did it pick that OB?” behavior

---

### 4.2 Smoothness

The similarity gradient must be **smooth**:

- no sharp kinks  
- no discontinuities  
- no sudden jumps in routing confidence  

Small changes in residue → **small changes** in routing behavior.

---

### 4.3 Curvature invariance

> **Same distance → same slope → same curvature → same routing behavior.**

This must hold:

- for all OBs  
- for all layers  
- for all directions in the address space

This is what makes the routing space a **true metric space**.

---

### 4.4 Predictability

Predictability is the requirement that **routing behavior must be identical for identical geometric conditions**, regardless of:

- which OB is being approached  
- which residue fragments produced the query address  
- which direction the query address approached from  
- which TP produced the residue  

Formally:

If two query addresses \( q_1 \) and \( q_2 \) satisfy:

- \( d(q_1, OB_i) = d(q_2, OB_i) \)  
- and their local gradients and curvature match  

then the routing decision must be **identical**:

- same similarity value  
- same slope  
- same curvature  
- same threshold behavior  
- same OB selection outcome  

Predictability ensures:

- **replayability**  
- **no drift**  
- **no sensitivity explosions**  
- **no “chaotic zones” in the address space**  
- **consistent routing across all OBs**  

Predictability is the *operational guarantee* that the geometric rules (monotonicity, smoothness, curvature invariance, OB‑invariance) produce **identical routing behavior for identical geometric conditions**.

---

### 4.5 OB‑invariant geometry

The similarity function and its derivatives must be **OB‑invariant**:

- SmOB1 and SmOB2 must behave identically at the same distance.  
- No OB is “more sensitive” or “less sensitive” than another at the same similarity score.  

This guarantees:

- deterministic routing  
- stable partial matches  
- predictable fallback  
- zero drift  
- perfect replay

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
  → SOB → SROB → CnOB → SmOB → semantic OBs
  → TP_out (fully interpreted)
  → Path B
```

---

### 5.2 Path B: deterministic realization, no OBs, no routing

Path B is a **deterministic realization path**.

Horizontal primitive flow:

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

Path B **does not interpret meaning**.

---

### 5.3 Architectural invariant: Path B must never have OBs or routing

> **Invariant:** Path B must never contain OBs, RBs, routing, residue, addressing, or any semantic interpretation mechanism.  
> If Path B appears to need interpretation, that logic must be moved into Path A.

---

## 6. Summary

- TS separates **interpretation (Path A)** from **realization (Path B)**.  
- Routing is a **Path A‑only** concern.  
- The core loop is **TP → SOB → RB → OB → … → TP_out**.  
- Routing is driven by **residue**, **address fragments**, and **XOR‑based addressing**.  
- The OB address space must be **monotonic, smooth, curvature‑invariant, and OB‑invariant**.  
- The four pre‑semantic OB layers are now:  
  - **SOB** — Structural OB  
  - **SROB** — Structural‑Refinement OB  
  - **CnOB** — Constraint OB  
  - **SmOB** — Semantic OB (entry layer)  
- Path B is a **deterministic reasoning pipeline** with **no OBs and no routing**.  
- If Path B ever appears to need OBs or routing, that is a design error—**the work must be pushed back into Path A**.

This document is the **playground‑level architectural description** of TS routing mechanics and the separation of concerns between Path A and Path B.
```

---
