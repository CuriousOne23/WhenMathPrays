# path_a_semantic_geometry_reference.md

**Document ID:** 20.XXX_path_a_semantic_geometry_reference  
**Version:** 0.1  
**Date:** 2026-07-09  
**Status:** Draft — Reference Paper (Path A)  
**Purpose:** Define the Path A semantic geometry reference for the SSG primitive, including semantic structure geometry, σ-normalization, semantic manifold geometry, routing signatures, semantic tags, field rules, and testing requirements.

---

## 1. Purpose & Scope

This document establishes the canonical semantic geometry specifications for the SSG primitive. It defines semantic structure geometry, normalization, manifold construction, routing signatures, and field rules that ensure deterministic, replay-safe processing.

---

## 2. Semantic Geometry Domain Overview

The semantic geometry domain integrates grammatical and structural outputs into normalized signatures and manifold projections. All operations remain pre-routing and maintain structural invariants. STPX follows SSG in the Path A pipeline but does not consume semantic geometry.

---

## 3. Canonical Semantic Geometry

Semantic geometry consists of refined graphs and normalized vectors derived from prior structural outputs. Evolution follows deterministic projection.

$$
\sigma = \frac{\varphi(G)}{\lVert \varphi(G) \rVert_2}
$$

## 3.1 STPX Position in Path A (Informative)

After SSG produces semantic_structure_geometry, normalized_σ, and manifold_projections, STPX (20.49) runs next in the Path A pipeline. STPX does not consume semantic geometry. It operates strictly on cleaned structural geometry and canonical tokens and produces the cue_envelope for downstream routing-adjacent primitives. STPX maintains pre-routing separation and does not modify semantic fields.

---

## 4. σ-Normalization Rules

σ-normalization produces L2-normalized routing signatures from semantic structure geometry.

**HLR-PA-SEM-001:** σ-normalization applies deterministic L2 scaling to structure vectors.  
**HLR-PA-SEM-002:** Normalized signatures preserve structural invariants and replay equivalence.

---

## 5. Semantic Manifold Construction

Semantic manifold construction projects refined geometry onto bounded charts.

**HLR-PA-SEM-003:** Manifold construction produces deterministic projections.  
**HLR-PA-SEM-004:** Manifold charts maintain bounded geometry without semantic inference.

---

## 6. Routing Signature Geometry

Routing signatures encode pre-routing semantic geometry for downstream use.

**HLR-PA-SEM-005:** Routing signatures derive from normalized semantic geometry.  
**HLR-PA-SEM-006:** Routing signature geometry remains pre-routing and bounded.

---

## 7. Field Allowance Table

| Primitive | Allowed Fields |
|-----------|----------------|
| SSG | semantic_structure_geometry, normalized_σ, manifold_projections, semantic_cues, provenance |
|STPX | structural_geometry, canonical_tokens |

---

## 8. Forbidden Field Table

| Primitive | Forbidden Fields |
|-----------|------------------|
| SSG | meaning_fields, routing_decision_fields, identity_conditioned_fields |
| STPX | semantic_structure_geometry, normalized_σ, manifold_projections, semantic_cues |

---

## 9. Semantic Expansion & Refinement Rules

Expansion and refinement operate on finite candidate sets within bounded semantic geometry.

**HLR-PA-SEM-007:** Semantic expansion produces deterministic candidates from prior geometry.  
**HLR-PA-SEM-008:** Refinement maintains structural invariants and monotonicity.

---

## 10. Testing Requirements

Testing includes replay fixtures, normalization verification, manifold projection tests, signature consistency tests, and envelope invariant assertions.

**HLR-PA-SEM-009:** Semantic geometry tests verify normalization and replay equivalence.  
**HLR-PA-SEM-010:** Field allowance and forbidden field tests are mandatory.

---

## 11. Canonical Starter Semantic Reference File

```markdown
# Canonical Path A Semantic Geometry Starter
semantic_version: "1.0"
graph: {nodes: [...], edges: [...], labels: {...}}
normalized_sigma: [...]
manifold_projections: [...]
provenance: {timestamp, source_id, ...}
```

---

## 12. HLR Traceability Matrix

| HLR ID | Section | Description |
|--------|---------|-------------|
| HLR-PA-SEM-001 | 4 | σ-normalization applies deterministic L2 scaling |
| HLR-PA-SEM-002 | 4 | Normalized signatures preserve invariants |
| HLR-PA-SEM-003 | 5 | Manifold construction produces deterministic projections |
| HLR-PA-SEM-004 | 5 | Manifold charts maintain bounded geometry |
| HLR-PA-SEM-005 | 6 | Routing signatures derive from normalized geometry |
| HLR-PA-SEM-006 | 6 | Routing signature geometry remains pre-routing |
| HLR-PA-SEM-007 | 9 | Semantic expansion produces deterministic candidates |
| HLR-PA-SEM-008 | 9 | Refinement maintains structural invariants |
| HLR-PA-SEM-009 | 10 | Semantic geometry tests verify normalization |
| HLR-PA-SEM-010 | 10 | Field allowance tests are mandatory |

**End of path_a_semantic_geometry_reference.md**
```
