# **oubb_surface_forms — Symbolic Surface-Form Primitives**

## **1. Title and Purpose**

This document defines the symbolic surface‑form primitives used by OuBB.

OuBB surface‑form primitives provide final connective and formatting templates for deterministic output text.

---

## **2. Architectural Context**

The pipeline is:  
**RSG → RG → OuBB**

OuBB surface‑form primitives are symbolic and deterministic.  
OuBB surface‑form primitives do not reinterpret SSR, manifold placement, RSG projection logic, or RG assembly logic.

---

## **3. Surface‑Form Primitive Definitions**

**oubb_connective_link**  
- Symbolic template for final linking.  
- Reflects RG connective primitives.

**oubb_connective_transition**  
- Symbolic template for transitional closure.  
- Reflects RG ordering metadata.

**oubb_connective_terminal**  
- Symbolic template for terminal punctuation and closure.  
- Reflects final RG structure.

**oubb_format_block**  
- Symbolic formatting template for block‑level output.  
- Reflects RG assembly structure.

**oubb_format_line**  
- Symbolic formatting template for line‑level output.  
- Reflects sequential RG ordering.

**oubb_format_sequence**  
- Symbolic formatting template for sequenced output.  
- Reflects full RG connective and ordering metadata.

**oubb_output_join**  
- Symbolic assembly primitive for final joining.  
- Reflects RG structure.

**oubb_output_finalize**  
- Symbolic assembly primitive for terminal output.  
- Reflects complete RG surface‑form identity.

Additional primitives follow the same pattern for all admissible combinations.  
Each primitive is symbolic and template‑based.  
Each primitive reflects RG connective logic and ordering metadata.  
No geometric or numeric interpretation.

---

## **4. Surface‑Form Structure Rules**

- OuBB surface‑form primitives must encode symbolic connective and formatting behavior only.  
- OuBB surface‑form primitives must not encode clause‑shape structure (resolved upstream).  
- OuBB surface‑form primitives must not encode descriptive content (provided by RG).  
- OuBB surface‑form primitives must remain stable across routing epochs.

---

## **5. Surface‑Form Admissibility Rules**

- Admissibility must depend on RG connective primitives.  
- Admissibility must depend on RG ordering metadata.  
- Admissibility must respect compatibility between RG structure and OuBB templates.  
- No inference, no dynamic meaning, no probabilistic selection.

---

## **6. Surface‑Form Compatibility Rules**

- OuBB surface‑form primitives must be compatible with RG-assembled structures.  
- OuBB surface‑form primitives must not override RG connective logic.  
- OuBB surface‑form primitives must not modify RG ordering.  
- OuBB surface‑form primitives must not reinterpret domain anchors, coordinates, or mismatch indicators.

---

## **7. Output Requirements**

- OuBB surface‑form primitives must be symbolic templates ready for OuBB assembly.  
- OuBB surface‑form primitives must be deterministic and stable across routing epochs.  
- OuBB surface‑form primitives must be directly consumable by oubb_assembly_rules.md.

---

## **8. Constraints to Avoid Drift**

- OuBB surface‑form primitives must remain symbolic.  
- OuBB surface‑form primitives must not expand into geometric or numeric domains.  
- OuBB surface‑form primitives must not encode hidden logic or implicit meaning.  
- OuBB surface‑form primitives must preserve strict Path A → Path B separation.

This specification defines the deterministic symbolic surface‑form primitives for OuBB.
