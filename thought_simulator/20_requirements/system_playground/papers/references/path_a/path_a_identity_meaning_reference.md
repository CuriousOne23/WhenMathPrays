# path_a_identity_meaning_reference.md

**Document ID:** 20.XXX_path_a_identity_meaning_reference  
**Version:** 0.1  
**Date:** 2026-07-09  
**Status:** Draft — Reference Paper (Path A)  
**Purpose:** Define the Path A identity and meaning reference for the IdOB and RBU primitives, including identity-conditioned refinement, referential stability, object binding, stance/tone integration, meaning manifold geometry, and field rules.

---

## 1. Purpose & Scope

This document establishes the canonical identity and meaning geometry specifications for the IdOB and RBU primitives. It defines identity profiles, referential stability, object binding, meaning refinement, and field rules that ensure deterministic, replay-safe processing.

---

## 2. Identity & Meaning Domain Overview

The identity and meaning domain applies identity profiles to refined structural outputs for object binding and meaning refinement. All operations are post-structural and identity-conditioned. The identity and meaning domain may consume cue_envelope as a non-semantic structural signal.

---

## 3. Canonical Meaning Geometry

Meaning geometry evolves within identity-selected manifold charts. Refinement follows deterministic operators.

$$
F_{\text{meaning}}^{(n+1)} = \Phi_{\text{id}}(F_{\text{meaning}}^{(n)}, \text{IdentityProfile})
$$

## 3.1 STPX Non‑Semantic Input Layer (Informative)

STPX (20.49) produces the cue_envelope, a non-semantic structural/lexical/constraint cue layer consumed by IdOB and RBU. Cue_envelope does not modify meaning geometry or identity profiles. It provides bounded, replay-safe surface cues that support referential stability, stance/tone integration, and identity-conditioned refinement without semantic inference.

---

## 4. Identity Profile Construction

Identity profile construction aggregates committed identity fields and prior context.

**HLR-PA-IDM-001:** Identity profile construction produces deterministic profiles from committed fields.  
**HLR-PA-IDM-002:** Identity profiles guide object binding and meaning refinement.

---

## 5. Referential Stability & Object Binding

Referential stability maintains consistent identity across sentences. Object binding links structural entities to meaning entries.

**HLR-PA-IDM-003:** Referential stability enforces consistent identity mappings.  
**HLR-PA-IDM-004:** Object binding operates within identity-conditioned manifolds.

---

## 6. Meaning Manifold Refinement Rules

Meaning manifold refinement applies identity-conditioned updates.

**HLR-PA-IDM-005:** Meaning manifold refinement is strictly identity-conditioned.  
**HLR-PA-IDM-006:** Refinement preserves monotonicity for committed meaning fields.

---

## 7. Field Allowance Table

| Primitive | Allowed Fields |
|-----------|----------------|
| IdOB | identity_profile, structural_cues, **cue_envelope**, meaning_fields, referential_stability_markers |
| RBU | identity_profile, stance_tone_fields, refined_meaning_fields, **cue_envelope**, provenance |

---

## 8. Forbidden Field Table

| Primitive | Forbidden Fields |
|-----------|------------------|
| IdOB | structural_geometry_modification, routing_decision_fields |
| RBU | structural_geometry_modification, routing_decision_fields |

---

## 9. Meaning Expansion & Refinement Rules

Expansion and refinement operate on finite candidate sets within identity manifolds.

**HLR-PA-IDM-007:** Meaning expansion produces deterministic candidates within identity bounds.  
**HLR-PA-IDM-008:** Refinement maintains referential stability and monotonicity.

---

## 10. Testing Requirements

Testing includes replay fixtures, identity profile consistency tests, referential stability verification, manifold refinement tests, and field invariant assertions.

**HLR-PA-IDM-009:** Identity and meaning tests verify determinism and replay equivalence.  
**HLR-PA-IDM-010:** Field allowance and forbidden field tests are mandatory.

---

## 11. Canonical Starter Identity & Meaning Reference File

```markdown
# Canonical Path A Identity & Meaning Starter
identity_version: "1.0"
identity_profile: {...}
referential_stability: {...}
meaning_fields: [...]
stance_tone: {...}
provenance: {timestamp, source_id, ...}
```

---

## 12. HLR Traceability Matrix

| HLR ID | Section | Description |
|--------|---------|-------------|
| HLR-PA-IDM-001 | 4 | Identity profile construction produces deterministic profiles |
| HLR-PA-IDM-002 | 4 | Identity profiles guide object binding and refinement |
| HLR-PA-IDM-003 | 5 | Referential stability enforces consistent mappings |
| HLR-PA-IDM-004 | 5 | Object binding operates within identity manifolds |
| HLR-PA-IDM-005 | 6 | Meaning manifold refinement is identity-conditioned |
| HLR-PA-IDM-006 | 6 | Refinement preserves monotonicity |
| HLR-PA-IDM-007 | 9 | Meaning expansion produces deterministic candidates |
| HLR-PA-IDM-008 | 9 | Refinement maintains referential stability |
| HLR-PA-IDM-009 | 10 | Identity tests verify determinism and replay |
| HLR-PA-IDM-010 | 10 | Field allowance tests are mandatory |

**End of path_a_identity_meaning_reference.md**
