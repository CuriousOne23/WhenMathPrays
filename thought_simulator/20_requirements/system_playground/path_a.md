# `path_a.md`  
## Path A — Meaning Construction Pipeline

Path A is the meaning‑construction pipeline of the TS system. It is the only pipeline that:

- constructs meaning  
- updates TP and MTP  
- performs ΔH% accounting  
- executes semantic merge  
- produces meaning‑aligned outputs  

This document defines:

- Path A **primitive flows**  
- Path A **process flows**  
- Path A **reference‑object flows**  
- Path A **governance flows**  
- Path A **TS‑concept flows**  
- A **notation guide** for reading all flows  

All flows begin and end with **primitives**.

---

## Notation guide

**Primitive sets**

- Single primitive: `primA`  
- Multiple primitives: `{primA, primB, primC}`  
- Used **only** for primitive boundaries.

**Processes**

- Serial processes: `proc1‑prc → proc2‑prc`  
- Parallel processes: `[proc1‑prc, proc2‑prc]`  
- Used **only** for conceptual units.

**Flow structure**

```text
{primitive inputs} → [parallel processes] → serial processes → {primitive outputs}
```

**Diagrams**

- Diagrams remain simple (no `{}` / `[]`).  
- Formal boundary notation appears only in tables.

---

## 1. Path A primitive flows

Primitive flows describe the **actual execution order** of primitives.

---

### 1.1 PthA‑cor — Full corrected primitive flow

**Flow diagram**

```text
InB → IIInB → IE → CEx → CE → ISc → TPU → OB → TE → TR → RB → OB
```

**Formal boundary**

```text
{InB‑prm} → IIInB‑prm → IE‑prm → CEx‑prm → CE‑prm → ISc‑prm → TPU‑prm → OB‑prm → TE‑prm → TR‑prm → RB‑prm  → {OB‑prm}
```

#### Primitive flow table (PthA‑cor)

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | InB‑prm | Input buffer; receives raw input | Entry point for Path A |
|   |           | **Example:** “User sends: *Explain entropy in simple terms*” | |
| 2 | IIInB‑prm | Initial inspection; structural sanity check | May trigger USP‑Flow |
|   |           | **Example:** Detects malformed JSON or missing context | |
| 3 | IE‑prm | Input enrichment; normalization/expansion | Optional; no‑op if not needed |
|   |        | **Example:** Expands pronouns: “it” → “the previous concept” | |
| 4 | CEx‑prm | Context extraction | Consumes USP‑ref if present |
|   |         | **Example:** Extracts: *topic=entropy, domain=physics* | |
| 5 | CE‑prm | Concept extraction | Produces CE‑ref |
|   |        | **Example:** Identifies: *entropy, disorder, information* | |
| 6 | ISc‑prm | Intermediate scoring | No meaning creation |
|   |         | **Example:** Computes ΔH% for concept alignment | |
| 7 | TPU‑prm | Semantic merge | Only writer to TP when correcting |
|   |         | **Example:** Writes new meaning to TP | |
| 8 | OB‑prm | Output buffer | Holds post‑merge TP snapshot |
|   |        | **Example:** Stores merged TP snapshot | |
| 9 | TE‑prm | Structural merge | No semantic interpretation |
|   |        | **Example:** Merges structure, not meaning | |
| 10 | TR‑prm | Interpretation | — |
|    |        | **Example:** Applies post‑TE interpretation | |
| 11 | RB‑prm | Router; arbitration | Appears twice in Path A |
|    |        | **Example:** Chooses next stage | |
| 12 | OB‑prm | Final output buffer | End of Path A |
|    |        | **Example:** Output ready for downstream use | |

---

### 1.2 PthA‑ncor — Minimal primitive flow (no correction)

**Flow diagram**

```text
InB → OB → TE → RB → TR → OB
```

**Formal boundary**

```text
{InB‑prm} → OB‑prm → TE‑prm → TR‑prm → RB‑prm → {OB‑prm}
```

#### Primitive flow table (PthA‑ncor)

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | InB‑prm | Input buffer | Entry point |
|   |         | **Example:** “User sends: *Hello*” | |
| 2 | OB‑prm | Output buffer | Direct pass‑through |
|   |        | **Example:** Input copied to OB without correction | |
| 3 | TE‑prm | Structural merge | No semantic work |
|   |        | **Example:** Merges trivial structure | |
| 4 | TR‑prm | Interpretation | Minimal interpretation |
|   |        | **Example:** Applies minimal interpretation to trivial output | |
| 5 | RB‑prm | Router | Arbitration |
|   |        | **Example:** Chooses next stage | |
| 6 | OB‑prm | Final output buffer | End of fast path |
|   |        | **Example:** Output ready | |

---

## 2. Path A process flows

Processes describe conceptual operations that may span multiple primitives.  
All flows begin and end with primitives.

---

### 2.1 USP‑Flow — Understanding Support Process

**Simple diagram**

```text
IIInB → USP-ref → CEx
```

**Formal flow**

```text
{IIInB‑prm} → USP‑prc → {CEx‑prm}
```

#### USP‑Flow table

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | USP‑prc | Understanding Support Process; enriches context between inspection and extraction | Provides contextual scaffolding for CEx |
|   |         | **Example:** Resolves “it” to “entropy” before CEx runs | |

---

### 2.2 MTP‑Loop — MTP maintenance process

**Simple diagram**

```text
OuB → MTP-Process → MTP-ref → MTP-Process → OuB
```

**Formal flow**

```text
{OuB‑prm} → MTP‑Process‑prc → MTP‑ref → MTP‑Process‑prc → {OuB‑prm}
```

#### MTP‑Loop table

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | MTP‑Process‑prc | MTP maintenance; reads/writes MTP‑ref based on OuB | TPU does not perform MTP maintenance |
|   |                 | **Example:** Updates long‑term meaning memory when a stable pattern is confirmed | |

---

### 2.3 IB‑Flow — Interpretation Bridge process

**Simple diagram**

```text
OuB → IB → TB-ref → GPIB-gov → GB-gov
```

**Formal flow (with parallel governance)**

```text
{OuB‑prm} → IB‑prc → TB‑ref → [GPIB‑gov, GB‑gov] → {OuB‑prm}
```

#### IB‑Flow table

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | IB‑prc | Interpretation bridge; prepares TB‑ref from OuB | Pre‑governance stage |
|   |        | **Example:** Converts a candidate response into a traceable behavior representation (TB‑ref) | |
| 2 | GPIB‑gov | Governance pre‑interpretation; applies governance rules to TB‑ref | Runs in parallel with GB‑gov |
|   |          | **Example:** Checks policy constraints before final behavior | |
| 3 | GB‑gov | Governance behavior; final governance decision | Runs in parallel with GPIB‑gov |
|   |        | **Example:** Approves, modifies, or rejects behavior based on TB‑ref | |

---

## 3. Reference‑object flows

Reference objects are **data**, not execution units.  
They appear inside processes; flows still begin and end with primitives.

---

### 3.1 CE‑RefGen

**Formal flow**

```text
{CE‑prm} → CE‑RefGen‑prc → {TPU‑prm}
```

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | CE‑RefGen‑prc | Generates CE‑ref from CE‑prm output | Feeds TPU‑prm |
|   |               | **Example:** Packages extracted concepts into a CE‑ref structure for semantic merge | |

---

### 3.2 ISc‑Delta

**Formal flow**

```text
{ISc‑prm} → ISc‑Delta‑prc → {TPU‑prm}
```

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | ISc‑Delta‑prc | Computes ΔH% contributions from ISc‑prm | Used by TPU‑prm |
|   |               | **Example:** Produces entropy deltas for each candidate meaning update | |

---

### 3.3 TPU‑Req

**Formal flow**

```text
{TPU‑prm} → TPU‑Req‑prc → {OB‑prm}
```

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | TPU‑Req‑prc | Builds semantic merge request envelope from TPU‑prm | Drives downstream OB‑prm behavior |
|   |             | **Example:** Encodes which TP segments are updated and why | |

---

## 4. Governance flows

---

### 4.1 Gov‑Interp

**Formal flow**

```text
{OuB‑prm} → IB‑prc → TB‑ref → [GPIB‑gov, GB‑gov] → {OuB‑prm}
```

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | Gov‑Interp‑prc | Governance interpretation chain over TB‑ref | Uses parallel governance stages |
|   |                | **Example:** Safety and behavior checks applied to a candidate response before finalization | |

*(You can keep Gov‑Interp‑prc as a named composite if you want, or just rely on the IB‑Flow table above.)*

---

## 5. TS‑concept flows

TS‑level concepts are invariants, not execution units, but we can still express where they bind between primitives.

---

### 5.1 MC‑tsc — Meaning commitment

**Formal flow**

```text
{TPU‑prm} → MC‑tsc → {OB‑prm}
```

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | MC‑tsc | Meaning commitment invariant; ensures TP updates are coherent | Binds between TPU‑prm and OB‑prm |
|   |       | **Example:** Prevents contradictory meaning updates from being committed to TP | |

---

### 5.2 SS‑tsc — Semantic span

**Formal flow**

```text
{CEx‑prm} → SS‑tsc → {CE‑prm}
```

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | SS‑tsc | Semantic span invariant; ensures extracted context is sufficiently broad | Binds between CEx‑prm and CE‑prm |
|   |       | **Example:** Ensures all relevant parts of the user query are represented in CE‑prm | |

---

### 5.3 SV‑tsc — Structural validity

**Formal flow**

```text
{IIInB‑prm} → SV‑tsc → {IE‑prm}
```

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | SV‑tsc | Structural validity invariant; ensures input is structurally sound | Binds between IIInB‑prm and IE‑prm |
|   |       | **Example:** Rejects or flags structurally invalid inputs before enrichment | |

---

### 5.4 SD‑tsc — Semantic density

**Formal flow**

```text
{ISc‑prm} → SD‑tsc → {TPU‑prm}
```

| Order | TS Object | Description | Notes |
|-------|-----------|-------------|-------|
| 1 | SD‑tsc | Semantic density invariant; ensures meaning density is sufficient for merge | Binds between ISc‑prm and TPU‑prm |
|   |       | **Example:** Prevents merges based on too‑sparse or noisy evidence | |

---

# **## 6. OB‑Regions (Orthogonal Extraction Regions)**

**OB‑Regions** are optional, parallelizable clusters of OB‑prm instances that operate on the **same TP** to extract **orthogonal semantic slices**.  
They provide safe parallelism inside Path A without introducing TP‑splitting, entropy fragmentation, or merge‑tree complexity.

### **6.1 Definition**

An **OB‑Region (OBR‑prc)** is a *parallel fan‑out stage* in Path A:

- The **same TP** is provided as input to each OB‑prm in the region.  
- Each OB‑prm extracts a **different, orthogonal semantic dimension**.  
- OB‑prms in a region **do not modify the TP**.  
- OB‑prms in a region **do not spawn new TPs**.  
- OB‑prms in a region **do not require semantic merging** with each other.

### **6.2 Purpose**

OB‑Regions allow Path A to:

- extract multiple semantic dimensions in parallel,  
- reduce latency,  
- maintain deterministic semantics,  
- avoid the complexity of TP splitting.

### **6.3 Examples of OB‑Region Lanes**

Typical OB‑prm lanes inside an OB‑Region include:

- **OB‑intent** — extracts user intent  
- **OB‑topic** — extracts topic domain  
- **OB‑constraints** — extracts explicit constraints  
- **OB‑tone** — extracts affective tone  
- **OB‑entities** — extracts named entities and referents  
- **OB‑temporal** — extracts temporal references  
- **OB‑spatial** — extracts spatial references  

These lanes are **orthogonal**: each extracts a different semantic slice and does not depend on the others.

### **6.4 Execution Semantics**

- TS fans out the TP to all OB‑prms in the region.  
- All OB‑prms run **in parallel** or **serially** depending on implementation.  
- TS waits until **all OB‑prms in the region complete**.  
- Their outputs are collected for MTP assembly.

### **6.5 No TP Splitting**

OB‑Regions **do not**:

- split TPs,  
- create new TPs,  
- modify the TP,  
- require conflict resolution.

They are strictly **parallel extraction**, not semantic branching.

---

# **## 7. MTP (v1) — Turn Semantic Package**

The **MTP (v1)** is the final output of Path A: a **structured bundle** of all OB outputs produced during the turn.  
It is intentionally simple, deterministic, and free of merge‑logic complexity.

### **7.1 Definition**

The **MTP (v1)** is:

> **A Turn Semantic Package containing all orthogonal semantic slices extracted by the OB‑Region.**

It is created **after all OB‑prms in the OB‑Region complete**.

### **7.2 Purpose**

The MTP (v1):

- provides a **single, coherent meaning object** for Path B,  
- bundles orthogonal semantic slices into a structured record,  
- performs **no semantic merging**,  
- performs **no conflict resolution**,  
- does **not** modify the TP,  
- does **not** maintain cross‑turn memory.

It is a **pure packaging step**, not a semantic engine.

### **7.3 Structure**

The MTP is a simple record:

```
MTP = {
  intent: <OB-intent output>,
  topic: <OB-topic output>,
  constraints: <OB-constraints output>,
  tone: <OB-tone output>,
  entities: <OB-entities output>,
  temporal: <OB-temporal output>,
  spatial: <OB-spatial output>,
  ...
}
```

Fields are populated directly from OB‑prm outputs.  
No merging, reconciliation, or inference occurs here.

### **7.4 Path A Completion Semantics**

Path A completes when:

1. All OB‑prms in the OB‑Region have finished, **and**  
2. The MTP (v1) has been assembled from their outputs.

The resulting MTP is then passed to Path B.

### **7.5 Notes for Future Versions**

Future versions of the system may expand the MTP to:

- merge multiple TPs,  
- reconcile conflicting slices,  
- maintain cross‑turn semantic memory,  
- integrate multi‑modal meaning fragments.

But **v1 intentionally avoids all of this** to preserve clarity, determinism, and simplicity.

---

## 6. Summary

Path A is the meaning‑construction pipeline. It consists of:

- **Primitive flows** (PthA‑cor, PthA‑ncor)  
- **Process flows** (USP‑Flow, MTP‑Loop, IB‑Flow)  
- **Reference‑object flows** (CE‑RefGen, ISc‑Delta, TPU‑Req)  
- **Governance flows** (Gov‑Interp / IB‑Flow with governance)  
- **TS‑concept flows** (MC‑tsc, SS‑tsc, SV‑tsc, SD‑tsc)  
- A **notation system** that keeps primitives, processes, references, governance, and invariants cleanly separated while still composable.

This file is the canonical reference for all Path A behavior in the TS architecture.

---
