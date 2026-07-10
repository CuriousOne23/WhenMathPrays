# ✅ **REVISED `path_a.md` — Path A with Parallel OB‑Regions + CTP**

## Path A — Meaning Construction Pipeline (Revised)

Path A is the meaning‑construction pipeline of the TS system. It is the only pipeline that:

- constructs meaning  
- updates TP and MTP  
- performs ΔH% accounting  
- executes semantic merge  
- produces meaning‑aligned outputs  

This revision incorporates:

- **Parallel OB‑Regions**  
- **CTP (Combine‑TP)** as the join primitive  
- **TS‑orchestrated scheduling**  
- **Removal of TE‑prm** (no more split/merge)  
- **New canonical Path A execution model**

All flows begin and end with **primitives**.

---

# 1. Notation Guide

**Primitive sets**

- Single primitive: `primA`  
- Multiple primitives: `{primA, primB, primC}`  

**Processes**

- Serial processes: `proc1‑prc → proc2‑prc`  
- Parallel processes: `[proc1‑prc, proc2‑prc]`  

**Flow structure**

```text
{primitive inputs} → [parallel processes] → serial processes → {primitive outputs}
```

---

# 2. Path A Primitive Flows (Revised)

Primitive flows describe the **actual execution order** of primitives.

The new Path A removes TE‑prm and introduces:

- **OB‑Regions** (parallel OB sets)  
- **CTP‑prm** (Combine‑TP join primitive)  

---

## 2.1 PthA‑cor — Full corrected primitive flow (Revised)

### **Flow diagram**

```text
InB → IIInB → IE → CEx → CE → ISc → TPU → OB0 → RB → {OB1 … OBn} → CTP → RB → {OB1a … OBna} → CTP → RB → OB-final
```

### **Formal boundary**

```text
{InB‑prm} → IIInB‑prm → IE‑prm → CEx‑prm → CE‑prm → ISc‑prm → TPU‑prm → OB‑prm 
→ RB‑prm → {OB‑prm} → CTP‑prm → RB‑prm → {OB‑prm} → CTP‑prm → RB‑prm → {OB‑prm}
```

### **Key changes**

- **OB0** is the only serial OB.  
- **All subsequent OBs run in parallel OB‑Regions.**  
- **CTP‑prm** merges OB‑Region outputs into a single TP.  
- **TS orchestrates all scheduling, fan‑out, and join behavior.**  
- **TE‑prm is removed** (no more split/merge).

---

## 2.2 PthA‑ncor — Minimal primitive flow (Revised)

### **Flow diagram**

```text
InB → OB0 → RB → {OB1 … OBn} → CTP → RB → OB-final
```

### **Notes**

- Even the minimal path uses OB‑Regions and CTP.  
- No TE‑prm.  
- No structural merge.  
- No semantic branching.

---

# 3. OB‑Regions (Revised)

OB‑Regions are **parallelizable clusters** of OB‑prm instances that operate on the **same TP** to extract **orthogonal semantic slices**.

### 3.1 Execution semantics

- TS fans out the TP to all OBs in the region.  
- OBs run **in parallel**.  
- OBs do **not** modify the TP.  
- OBs write **OB‑deltas** (their observations).  
- TS waits until **all OBs complete**.  
- TS invokes **CTP‑prm** to combine outputs.

### 3.2 No TP splitting

OB‑Regions do **not**:

- split TPs  
- create new TPs  
- require semantic merging  
- resolve conflicts  

They are pure extraction.

---

# 4. CTP‑prm — Combine‑TP Primitive

### 4.1 Purpose

CTP‑prm is the **join primitive** that:

- collects all OB outputs from an OB‑Region  
- packages them into a single TP update  
- performs **no semantic resolution**  
- performs **no conflict resolution**  
- preserves OB provenance  
- preserves determinism  

### 4.2 Responsibilities

CTP‑prm:

- merges OB‑deltas into a single TP container  
- tags each delta with OB identity  
- ensures order‑independence  
- ensures replayability  
- hands the merged TP to the next RB  

### 4.3 What CTP does **not** do

CTP does **not**:

- interpret  
- resolve conflicts  
- prioritize  
- choose winners  
- apply formulas  
- modify meaning  

All semantic resolution happens in **Path B**.

---

# 5. Revised Path A Process Flow

The new canonical Path A loop is:

```text
OB0 → RB → {OB1 … OBn} → CTP → RB → {OB1a … OBna} → CTP → RB → …
```

### 5.1 TS orchestration

TS is responsible for:

- scheduling OB0  
- routing to OB‑Regions  
- parallel execution of OBs  
- waiting for completion  
- invoking CTP  
- advancing to the next RB  
- maintaining determinism  
- maintaining invariants  

No primitive self‑schedules.

---

# 6. MTP (v1) — Turn Semantic Package (Revised)

MTP is now simply:

- the **final TP** after the last CTP  
- containing all OB‑deltas from all OB‑Regions  
- ready for Path B  

No merging.  
No conflict resolution.  
No inference.

---

# 7. Summary of Changes

### ✔ Added  
- OB‑Regions  
- CTP‑prm  
- TS‑orchestrated parallelism  
- New canonical Path A loop  

### ✔ Removed  
- TE‑prm  
- Split/merge semantics  
- TP branching  

### ✔ Updated  
- Primitive flows  
- Process flows  
- Execution semantics  
- MTP definition  

---
