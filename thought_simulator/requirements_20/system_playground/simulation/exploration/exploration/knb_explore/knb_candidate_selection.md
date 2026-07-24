# knb_candidate_selection.md  
**Document ID:** 20.XXX_knb_candidate_selection  
**Version:** 0.2  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (KnB)  
**Purpose:** Define candidate selection for the Knowing-by-Binding (KnB) primitive operating over SSR and the manifold, producing knowledge anchors consumed by Path B.

---

## 1. Overview

KnB (Knowing-by-Binding) is the primitive responsible for generating, filtering, validating, and selecting candidates for knowledge anchoring over **SSR(t−1)** and producing stable, deterministic anchors for **SSR(t)**. Candidate selection bridges CE, ISc, SSR, and manifold geometry while preserving determinism, replay equivalence, and projection compatibility.

KnB operates **outside Path A**. It consumes SSR-exposed fields and produces SSR-visible knowledge anchors that the manifold and Path B (CoHI, LI, REx, RPlan, RPU, ReB, OuBB) rely on. Candidate selection MUST guarantee manifold projectability and Path‑B consumption safety.

---

## 2. Candidate Foundations

- **Candidate envelopes:** Structured, bounded collections of candidates.  
- **Candidate fields:** identity_candidate[], relation_candidate[], domain_anchor_candidate[], qualifier_candidate[], truth_validation_candidate[], KnDt_keywords[], KnDt_addresses[].  
- **Candidate geometry:** Finite sets with provenance.  
- **Candidate provenance:** Traceable origin from CE/ISc/SSR(t−1).  
- **Candidate monotonicity and stability:** Once selected, candidates are stable for the cycle and frozen into SSR(t).

**Finite candidate set:** 

$$
C = \{c_1, c_2, \dots, c_n\}
$$

**Candidate generation:**  

$$
c_i = \Gamma(\text{CE}, \text{ISc}, \text{SSR}(t-1))
$$

---

## 3. Candidate Generation Rules

Rules govern deterministic extraction from CE, expansion from ISc, and binding from SSR(t−1) fields.

- Candidate generation SHALL NOT infer new meaning.  
- Candidate generation SHALL NOT modify SSR(t−1).  
- Candidate generation SHALL NOT depend on Path‑B routing signals.  
- Candidate generation SHALL read only SSR-exposed fields, never raw Path‑A fields.

---

## 4. Candidate Normalization Rules

$$
c_i^{\text{norm}} = N(c_i)
$$

Normalization ensures canonical field ordering, grouping, envelope shape, and replay-deterministic normalization.

---

## 5. Candidate Filtering Rules

$$
C_{\text{filtered}} = \\{c_i \in C \mid F(c_i) = \text{true}\\}
$$

Filtering governs allowlist/denylist, structural-compatibility, identity-compatibility, domain-compatibility, and truth-validation filters.

- Filtering SHALL NOT introduce new candidates.  
- Filtering SHALL NOT modify candidate geometry.  
- Filtering SHALL NOT violate SSR freeze rules.

---

## 6. Candidate Scoring Rules

$$
S(c_i) = \text{Score}(c_i, \text{CE}, \text{ISc}, \text{SSR}(t-1))
$$

$$
\text{Distribution} = \frac{e^{S(c_i)}}{\sum_j e^{S(c_j)}}
$$

- Scoring SHALL NOT generate meaning.  
- Scoring SHALL NOT modify SSR(t−1).  
- Scoring MUST remain deterministic and seed-free.

---

## 7. Candidate Selection Rules

$$
c^\ast = \arg\max_{c_i \in C_{\text{filtered}}} S(c_i)
$$

Rules govern top-candidate selection, threshold selection, multi-candidate selection, deterministic tie-breaking, and replay-deterministic selection.

- Selection SHALL NOT modify candidate geometry.  
- Selection SHALL NOT generate new candidates.  
- Selection MUST produce SSR‑compatible anchors.

---

## 8. Candidate Correction Rules (IMR Type B)

$$
C^{(n+1)} = \Psi_{\text{corr}}(C^{(n)}, \text{CorrectionContext})
$$

Corrections govern boundaries, depth limits, cooldowns, invariants, and replay equivalence.

- Corrections SHALL NOT introduce new structural fields.  
- Corrections SHALL NOT alter candidate geometry.  
- Corrections SHALL NOT generate meaning.  
- Corrections MUST preserve SSR determinism.

---

## 9. Candidate Serialization Rules

$$
\text{Serialize}(C) = \text{CanonicalForm}(C)
$$

Serialization governs canonical ordering, naming, grouping, envelope shape, and replay-deterministic serialization.

- Serialization MUST produce SSR‑visible canonical forms.  
- Serialization MUST satisfy manifold projection requirements.

---

## 10. Deterministic Candidate Guarantees

$$
\text{CandidateDeterministic} \iff f(x) = f(y) \;\text{whenever}\; x = y
$$

All candidate operators are deterministic, seed-free, replay-equivalent, and SSR-consistent.

---

## 11. SSR Integration Requirements

- Candidate selection operates over **SSR(t−1)** and produces anchors for **SSR(t)**.  
- All candidate fields MUST serialize into SSR using canonical SSR field names.  
- Candidate ranking MUST be finite, deterministic, replay-stable, and seed-independent.  
- Candidate outputs MUST satisfy SSRGn projection rules (freeze, sanitization, provenance).  
- Candidate selection SHALL NOT read raw Path‑A fields; it SHALL read only SSR-exposed fields.  
- Candidate outputs MUST be visible to manifold operators Π and Π⁻¹.

---

## 12. Manifold Compatibility Requirements

- Candidate outputs MUST map to manifold shapes defined in `manifold_geometry_shapes_spec.md`.  
- Each candidate MUST expose a meaning‑signature‑compatible structure (finite, typed, stable).  
- Candidate identity, relations, anchors, qualifiers MUST be geometrically projectable.  
- Candidate outputs MUST satisfy manifold routing constraints (curvature, locality, basin rules).  
- Candidate outputs MUST NOT introduce non‑projectable structures (infinite sets, unstable fields).  
- Candidate provenance MUST be preserved for manifold → OuBB reverse projection (Π⁻¹).

---

## 13. Path‑B Consumption Guarantees

- Candidate outputs MUST be consumable by LI (20.112) as stable meaning‑layer inputs.  
- Candidate ranking MUST support continuity_fields computed by CoHI.  
- Candidate outputs MUST satisfy OuBB requirements for truth/safety expression.  
- Candidate outputs MUST be compatible with RG/RSG surface‑form generation rules.  
- Candidate outputs MUST NOT require Path‑B to perform grounding or fact‑stability work.  
- Candidate outputs MUST remain unchanged after SSR freeze (SSR(t) is immutable to Path‑B).

---

## 14. Realization Notes

- **Implementation:** Implement generation, normalization, filtering, scoring, and selection as deterministic functions with bounded sets and guards.  
- **Validation:** Assert finiteness, provenance, separation, SSR compliance, and normalization invariants.  
- **Testing:** Replay tests, clean/corrected candidate paths, manifold projection tests, Path‑B consumption tests.  
- **Serialization:** Enforce canonical SSR form for candidate envelopes.  
- **Integration:** Candidates feed grounding (KnC/KnM/KnF), SSRGn, manifold projection, and Path‑B primitives.  
- **New primitives:** Declare candidate interactions and satisfy SSR/manifold/Path‑B invariants.

---

## 15. Summary

KnB candidate selection operates over SSR(t−1) to produce deterministic, bounded, manifold‑compatible knowledge anchors for SSR(t). It maintains strict separation from meaning generation and structural mutation while enabling stable identity resolution, manifold projection, and safe Path‑B consumption. All operations are replay-equivalent, seed-free, and SSR-consistent.

**End of knb_candidate_selection.md**

---
