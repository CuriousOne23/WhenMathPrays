# path_a_structure_reference.md

**Document ID:** 20.XXX_path_a_structure_reference  
**Version:** 0.1  
**Date:** 2026-07-09  
**Status:** Draft — Reference Paper (Path A)  
**Purpose:** Define the Path A structural geometry reference, including segmentation, normalization, monotonic constraints, residue compression, structural tags, field allowances, and testing requirements for the covered primitives.

---

## 1. Purpose & Scope

This document establishes the canonical structural geometry specifications for the Path A primitives SOB, SROB, CnOB, and SmOB. It defines segmentation, normalization, monotonic constraints, residue handling, and field rules that ensure deterministic, replay-safe structural processing.

---

## 2. Structural Domain Overview

The structural domain encompasses segmentation, refinement, constraint application, and residue management. All operations maintain monotonic accumulation, bounded behavior, and pre-semantic separation. STPX consumes structural geometry but does not modify it.

---

## 3. Canonical Structural Geometry

Structural geometry consists of graphs with nodes, edges, and labels. Evolution follows deterministic projection operators. Structure vectors are produced via normalization.

$$
v_{\text{struct}} = h(G)
$$

$$
v_{\text{norm}} = \frac{v_{\text{struct}}}{\lVert v_{\text{struct}} \rVert_2}
$$

## 3.1 STPX Structural Inputs (Informative)

STPX (20.49) consumes cleaned structural geometry and canonical tokens produced by SOB, SROB, CnOB, and SmOB. STPX does not modify structural geometry. It extracts lexical, structural, and constraint cues from the structural domain for downstream routing-adjacent processing. STPX operates strictly post-SSG and pre-RBU in Path A.

---

## 4. Structural Segmentation Rules

Segmentation divides input into bounded structural units and extracts hints.

**HLR-PA-STR-001:** Segmentation produces deterministic structural units and hints.  
**HLR-PA-STR-002:** Segmentation attaches structural tags without semantic inference.

---

## 5. Structure Normalization & Refinement

Normalization applies canonical ordering and deterministic repairs to structural representations.

**HLR-PA-STR-003:** Normalization preserves structural invariants and monotonicity.  
**HLR-PA-STR-004:** Refinement sharpens hints while maintaining replay equivalence.

---

## 6. Monotonic Constraint Set C1–C7

The C1–C7 constraint set enforces structural consistency.

**HLR-PA-STR-005:** Monotonic constraints detect missing slots and conflicts.  
**HLR-PA-STR-006:** Constraint application produces bounded signals for downstream processing.

---

## 7. Residue Compression Geometry

Residue accumulates monotonically. Compression occurs only in SmOB via bounded hashing.

**HLR-PA-STR-007:** Residue accumulation is monotonic.  
**HLR-PA-STR-008:** Residue compression is restricted to SmOB and preserves replay equivalence.

---

## 8. Field Allowance Table

| Primitive | Allowed Fields |
|-----------|----------------|
| SOB | raw_structure, segmentation_hints, structural_tags |
| SROB | refined_structure, normalized_hints, repair_metadata |
| CnOB | constraint_signals, missing_slot_flags, conflict_flags |
| SmOB | residue_accumulation, compressed_residue, structural_cues |
| STPX | structural_geometry, canonical_tokens |

---

## 9. Forbidden Field Table

| Primitive | Forbidden Fields |
|-----------|------------------|
| SOB | meaning_fields, semantic_tags |
| SROB | meaning_fields, semantic_inference |
| CnOB | meaning_fields, structural_geometry_modification |
| SmOB | meaning_fields, non_bounded_hashing |
| STPX | semantic_fields, identity_fields, routing_fields, entropy_fields, TPU_fields |

---

## 10. Structural Expansion & Refinement Rules

Expansion and refinement operate on finite candidate sets within bounded envelopes.

**HLR-PA-STR-009:** Expansion produces deterministic structural candidates.  
**HLR-PA-STR-010:** Refinement maintains structural geometry invariants.

---

## 11. Testing Requirements

Testing includes replay fixtures, boundary cases, constraint violation tests, residue accumulation tests, and envelope invariant assertions.

**HLR-PA-STR-011:** Structural tests verify monotonicity and replay equivalence.  
**HLR-PA-STR-012:** Field allowance and forbidden field tests are mandatory at each handoff.

---

## 12. Canonical Starter Structural Reference File

```markdown
# Canonical Path A Structural Starter
structural_version: "1.0"
nodes: [...]
edges: [...]
labels: {...}
residue: []
provenance: {timestamp, source_id, ...}
```

---

## 13. HLR Traceability Matrix

| HLR ID | Section | Description |
|--------|---------|-------------|
| HLR-PA-STR-001 | 4 | Segmentation produces deterministic units and hints |
| HLR-PA-STR-002 | 4 | Segmentation attaches structural tags |
| HLR-PA-STR-003 | 5 | Normalization preserves invariants and monotonicity |
| HLR-PA-STR-004 | 5 | Refinement sharpens hints with replay equivalence |
| HLR-PA-STR-005 | 6 | Monotonic constraints detect missing slots and conflicts |
| HLR-PA-STR-006 | 6 | Constraint application produces bounded signals |
| HLR-PA-STR-007 | 7 | Residue accumulation is monotonic |
| HLR-PA-STR-008 | 7 | Residue compression restricted to SmOB |
| HLR-PA-STR-009 | 10 | Expansion produces deterministic candidates |
| HLR-PA-STR-010 | 10 | Refinement maintains structural invariants |
| HLR-PA-STR-011 | 11 | Structural tests verify monotonicity and replay |
| HLR-PA-STR-012 | 11 | Field allowance tests are mandatory |
|HLR-PA-STR-013 | 3.1 | STPX produces deterministic cue_envelope |
|HLR-PA-STR-014 | 3.1 | STPX operates only on cleaned structural geometry |
|HLR-PA-STR-015 | 3.1 | STPX emits lexical surface cues |
|HLR-PA-STR-016 | 3.1 | STPX emits structural cues |
|HLR-PA-STR-017 | 3.1 | STPX emits constraint cues |
|HLR-PA-STR-018 | 3.1 | STPX emits repair-region markers when present |
|HLR-PA-STR-019 | 3.1 | STPX does not perform semantic interpretation |
|HLR-PA-STR-020 | 3.1 | STPX does not modify TPU, meaning, identity, routing, or truth fields |
|HLR-PA-STR-021 | 3.1 | STPX cue_envelope is bounded and replay-safe |
|HLR-PA-STR-022 | 3.1 | STPX cue_envelope schema is deterministic |

---

