# **`path_a.md`**  
## **Path A — Meaning Construction Pipeline**

Path A is the **only** pipeline that constructs meaning, updates TP/MTP, performs ΔH% accounting, and executes the semantic merge.  
This document defines:

- Path A **primitive flows** (actual execution order of primitives)  
- Path A **process flows** (conceptual flows using reference objects)  
- Path A **reference‑object flows**  
- Path A **governance flows**  
- Path A **TS‑concept flows**  
- Clear **WHERE / WHEN / WHY** separation rules  

Primitive flows and process flows must never be mixed.

---

# **1. Path A Primitive Flows**

Primitive flows describe the **actual execution order** of primitives.  
They define determinism, replay equivalence, and stage boundaries.

---

## **1.1 PthA‑cor — Full Corrected Primitive Flow**

### **Flow Diagram**
```
InB → IIInB → IE → CEx → CE → ISc → TPU(Merg) → OB → TE → RB → TR → OB
```

### **Primitive Flow Table**

| Order | TS Object | Description | Notes |
|------|-----------|-------------|-------|
| 1 | **InB‑prm** | Input buffer; receives raw input | Entry point for Path A |
| 2 | **IIInB‑prm** | Initial inspection; structural sanity check | May trigger USP‑Flow |
| 3 | **IE‑prm** | Input enrichment; normalization/expansion | Optional; no‑op if not needed |
| 4 | **CEx‑prm** | Context extraction | Consumes USP‑ref if present |
| 5 | **CE‑prm** | Concept extraction | Produces CE‑ref |
| 6 | **ISc‑prm** | Intermediate scoring | Computes ΔH% contributions |
| 7 | **TPU‑prm** | Semantic merge | Only writer to TP |
| 8 | **OB‑prm** | Output buffer | Holds post‑merge TP snapshot |
| 9 | **TE‑prm** | Structural merge | No semantic interpretation |
| 10 | **RB‑prm** | Router; arbitration | Appears twice in Path A |
| 11 | **TR‑prm** | Interpretation | Applies post‑TE interpretation |
| 12 | **OB‑prm** | Final output buffer | End of Path A |

---

## **1.2 PthA‑ncor — Minimal Primitive Flow (No Correction)**

### **Flow Diagram**
```
InB → OB → TE → RB → TR → OB
```

### **Primitive Flow Table**

| Order | TS Object | Description | Notes |
|------|-----------|-------------|-------|
| 1 | **InB‑prm** | Input buffer | Entry point |
| 2 | **OB‑prm** | Output buffer | Direct pass‑through |
| 3 | **TE‑prm** | Structural merge | No semantic work |
| 4 | **RB‑prm** | Router | Arbitration |
| 5 | **TR‑prm** | Interpretation | Minimal interpretation |
| 6 | **OB‑prm** | Final output buffer | End of fast path |

---

# **2. Path A Process Flows**

Processes describe **conceptual flows** that may span multiple primitives and reference objects.  
They explain *what* the system is doing, not *how primitives are ordered*.

---

## **2.1 USP‑Flow — Understanding Support Process**

### **Flow Diagram**
```
IIInB → USP-ref → CEx
```

| Step | Object | Description | Notes |
|------|--------|-------------|-------|
| 1 | **IIInB‑prm** | Initial inspection | Detects need for USP |
| 2 | **USP‑ref** | Understanding support reference | Provides contextual scaffolding |
| 3 | **CEx‑prm** | Context extraction | Consumes USP‑ref |

---

## **2.2 MTP‑Loop — MTP Maintenance Process**

### **Flow Diagram**
```
OuB → MTP-Process → MTP-ref
MTP-ref → MTP-Process → OuB
```

| Step | Object | Description | Notes |
|------|--------|-------------|-------|
| 1 | **OuB‑prm** | Output buffer | Source of MTP updates |
| 2 | **MTP‑Process‑prc** | MTP maintenance | Reads/writes MTP‑ref |
| 3 | **MTP‑ref** | MTP reference object | Persistent meaning memory |

> **Note:** TPU does *not* perform MTP maintenance.

---

## **2.3 IB‑Flow — Interpretation Bridge Process**

### **Flow Diagram**
```
OuB → IB → TB-ref → GPIB-gov → GB-gov
```

| Step | Object | Description | Notes |
|------|--------|-------------|-------|
| 1 | **OuB‑prm** | Output buffer | Source of interpretation |
| 2 | **IB‑prc** | Interpretation bridge | Prepares TB‑ref |
| 3 | **TB‑ref** | Trace behavior reference | Input to governance |
| 4 | **GPIB‑gov** | Governance pre‑interpretation | Applies governance rules |
| 5 | **GB‑gov** | Governance behavior | Final governance output |

---

# **3. Path A Reference‑Object Flows**

Reference objects are **data**, not execution units.  
They appear inside processes, not primitive flows.

| Flow Name | Diagram | Description |
|-----------|---------|-------------|
| **CE‑RefGen** | `CE → CE-ref` | Concept extraction reference generation |
| **ISc‑Delta** | `ISc → ΔH%` | Scoring and entropy contribution |
| **TPU‑Req** | `TPU → tp_update_request` | Semantic merge request envelope |

---

# **4. Path A Governance Flows**

| Flow Name | Diagram | Description |
|-----------|---------|-------------|
| **Gov‑Interp** | `TB-ref → GPIB-gov → GB-gov` | Governance interpretation chain |

---

# **5. Path A TS‑Concept Flows**

TS‑level concepts are invariants, not primitives or processes.

| Concept | Short Name | Description |
|---------|------------|-------------|
| Meaning Commitment | **MC‑tsc** | Meaning commitment invariant |
| Semantic Span | **SS‑tsc** | Span of semantic coverage |
| Structural Validity | **SV‑tsc** | Structural correctness invariant |
| Semantic Density | **SD‑tsc** | Density of meaning per unit |

---

# **6. Separation Rules (WHERE / WHEN / WHY)**

## **6.1 Primitive Flow Rules**
- **WHERE:** Define actual execution order  
- **WHEN:** Determinism, replay equivalence, stage boundaries  
- **WHY:** Primitives are mechanical execution units  

## **6.2 Process Flow Rules**
- **WHERE:** Conceptual operations spanning primitives  
- **WHEN:** Meaning construction, context expansion, governance  
- **WHY:** Processes explain *what*, not *how*  

## **6.3 Reference Object Flow Rules**
- **WHERE:** Inside processes  
- **WHEN:** Plans, graphs, mappings, envelopes  
- **WHY:** Reference objects are data, not execution units  

---

# **7. Summary**

Path A is the meaning‑construction pipeline.  
It consists of:

- **Primitive flows** (PthA‑cor, PthA‑ncor)  
- **Process flows** (USP‑Flow, MTP‑Loop, IB‑Flow)  
- **Reference‑object flows**  
- **Governance flows**  
- **TS‑concept flows**  
- **Strict separation rules**  

This document is the **canonical reference** for all Path A behavior in the TS architecture.

---
