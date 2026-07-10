**kn_dt_partitioning.md**

# **kn_dt_partitioning — KnDt Architectural Partitioning Rules**

## **1. Title and Purpose**

This document defines the architectural boundaries and responsibilities of KnDt within the TS pipeline.

kn_dt_partitioning.md establishes the strict separation of KnDt as the declarative meaning source and prevents leakage into grounding, mapping, or realization stages.

---

## **2. Architectural Context**

The pipeline is:  
**KnDt → KnC/KnM/KnF → SSR → Pre‑Manifold → Manifold → RSG → RG**

- KnDt is the declarative meaning source for Path A.  
- KnDt never participates in Path B operations.  
- KnC, KnM, and KnF are the only components that read KnDt.  
- All downstream stages operate exclusively on SSR fields derived from KnDt.

---

## **3. KnDt Responsibilities**

- KnDt provides declarative meaning only.  
- KnDt defines identity, relations, manifold region, coordinates, and expression surfaces.  
- KnDt provides schema‑level constraints and validation anchors.  
- KnDt supplies stable symbolic entries for grounding extraction.

---

## **4. KnDt Non‑Responsibilities**

- KnDt must not perform grounding.  
- KnDt must not compute SSR fields.  
- KnDt must not define basin identity, mismatch, manifold placement, clause‑shape selection, surface‑form selection, or connective logic.  
- KnDt must not encode meaning construction or realization rules.  
- KnDt must not participate in inference, timing, priority, or projection.

---

## **5. Partitioning Rules**

- All grounding is performed by KnC/KnM/KnF.  
- All mismatch and basin evaluation is performed in Pre‑Manifold.  
- All manifold placement is symbolic and performed outside KnDt.  
- All clause‑shape and surface‑form grounding is performed by RSG.  
- All assembly is performed by RG.  
- KnDt is read‑only for all downstream components.  
- KnC/KnM/KnF perform symbolic extraction only; no modification of KnDt occurs.

---

## **6. Stability Requirements**

- KnDt entries must remain declarative across routing epochs.  
- KnDt schema must remain stable and non‑inferential.  
- No KnDt field may encode dynamic or procedural meaning.

---

## **7. Constraints to Avoid Drift**

- KnDt must not expand into grounding, projection, or assembly domains.  
- KnDt must not encode implicit meaning or hidden logic.  
- KnDt must remain strictly declarative and symbolic.

This specification enforces architectural separation and prevents semantic drift.
