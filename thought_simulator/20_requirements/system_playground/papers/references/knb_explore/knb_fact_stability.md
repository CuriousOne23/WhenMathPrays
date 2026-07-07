# knb_fact_stability.md

**Document ID:** 20.XXX_knb_fact_stability  
**Version:** 0.2  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (KnB)  
**Purpose:** Define fact-stability rules for the Knowing‑by‑Binding (KnB) primitive operating over SSR and the manifold, producing stable knowledge anchors consumed by Path B.

---

## 1. Overview

KnB fact stability governs the stabilization of identity‑conditioned facts after candidate selection. It prevents semantic drift, enforces bounded corrections, and ensures replay‑deterministic fact evolution while supporting SSR freeze, manifold projection, and Path‑B consumption.

KnB operates **outside Path A**, over **SSR(t−1)**, producing stable, deterministic fact anchors for **SSR(t)**. These anchors must be geometrically projectable, manifold‑compatible, and safe for Path‑B primitives (CoHI, LI, REx, RPlan, RPU, ReB, OuBB).

---

## 2. Fact Foundations

- **Fact envelopes:** Structured, bounded collections of stabilized facts.  
- **Fact fields:** `identity_fact[]`, `relation_fact[]`, `domain_anchor_fact[]`, `qualifier_fact[]`, `truth_validation_fact[]`, `KnDt_keywords[]`, `KnDt_addresses[]`.  
- **Fact geometry:** Stable, monotonic sets with provenance.  
- **Fact provenance:** Traceable to selected candidates and SSR(t−1).  
- **Fact monotonicity:** Once committed, facts do not disappear.

**Finite fact set:**  

$F\ =\ \\{ f_1, f_2, \dots , f_m \\}$


**Fact derivation:**  

$f_i = \Lambda(c^{\*}, \text{SSR}(t-1), \text{IdentityProfile})$


(Gloss: each fact is derived deterministically from the selected candidate, SSR(t−1), and identity profile.)

---

## 3. Fact Stability Rules

Rules govern deterministic fact formation, refinement, monotonicity, geometry stability, and replay‑deterministic evolution.

- Fact stability SHALL NOT modify SSR(t−1).  
- Fact stability SHALL NOT generate new candidates.  
- Fact stability SHALL NOT depend on Path‑B routing signals.  
- Fact stability SHALL read only SSR‑exposed fields.

---

## 4. Fact–Structure Interaction Rules

Facts depend on structural geometry but never mutate it.

$F\ =\ g(F\_{\text{struct}}, c^\*, \text{SSR(t−1)}, \text{IdentityProfile})$

Fact stability enforces pre‑/post‑semantic separation and SSR freeze compliance.

---

## 5. Fact–Meaning Interaction Rules

Facts constrain meaning refinement and contribute to `path_b_eligible`. Meaning refinement depends on stable facts.

- Fact stability SHALL NOT modify meaning fields directly.  
- Meaning refinement SHALL NOT modify fact geometry.  
- Fact stability prevents semantic drift and supports SSR determinism.

---

## 6. Fact Correction Rules (IMR Type A/B/C)

Rules govern correction boundaries, depth limits, cooldowns, invariants, and replay equivalence.

$F^{(n+1)} = \Psi_{\text{corr}}(F^{(n)}, \text{CorrectionContext})$


- **Type A:** realization‑only.  
- **Type B:** bounded semantic.  
- **Type C:** safety.  

Corrections SHALL NOT introduce new structural fields, alter structural geometry, or generate meaning.  
Corrections MUST preserve SSR determinism and manifold compatibility.

---

## 7. Fact Serialization Rules

- Canonical ordering, naming, and grouping.  
- Canonical fact envelope shape.  
- Replay‑deterministic serialization.

```
Serialize(F) = CanonicalForm(F)
```

Serialization MUST produce SSR‑visible canonical forms and satisfy manifold projection requirements.

---

## 8. Deterministic Fact Guarantees

```
FactDeterministic ⇔ f(x) = f(y) whenever x = y
```

All fact‑stability operators are deterministic, seed‑free, replay‑equivalent, and SSR‑consistent.

---

## 9. SSR Integration Requirements

- Fact stability operates over **SSR(t−1)** and produces stable anchors for **SSR(t)**.  
- All fact fields MUST serialize into SSR using canonical SSR field names.  
- Fact evolution MUST satisfy SSRGn rules (freeze, sanitization, provenance).  
- Fact stability SHALL NOT read raw Path‑A fields; it SHALL read only SSR‑exposed fields.  
- Facts MUST be visible to manifold operators Π and Π⁻¹.

---

## 10. Manifold Compatibility Requirements

- Facts MUST map to manifold shapes defined in `manifold_geometry_shapes_spec.md`.  
- Each fact MUST expose a meaning‑signature‑compatible structure (finite, typed, stable).  
- Fact identity, relations, anchors, qualifiers MUST be geometrically projectable.  
- Facts MUST satisfy manifold routing constraints (curvature, locality, basin rules).  
- Facts MUST NOT introduce non‑projectable structures (infinite sets, unstable fields).  
- Fact provenance MUST be preserved for manifold → OuBB reverse projection (Π⁻¹).

---

## 11. Path‑B Consumption Guarantees

- Facts MUST be consumable by LI (20.112) as stable meaning‑layer inputs.  
- Facts MUST support continuity_fields computed by CoHI.  
- Facts MUST satisfy OuBB truth/safety expression rules.  
- Facts MUST be compatible with RG/RSG surface‑form generation rules.  
- Facts MUST NOT require Path‑B to perform grounding or stability work.  
- Facts MUST remain unchanged after SSR freeze (SSR(t) is immutable to Path‑B).

---

## 12. Realization Notes

- **Implementation:** Implement fact derivation, stabilization, and correction as deterministic operators with monotonicity guards.  
- **Validation:** Assert stability, monotonicity, SSR compliance, manifold compatibility, and provenance invariants.  
- **Testing:** Replay tests, manifold projection tests, Path‑B consumption tests, drift‑prevention cases.  
- **Serialization:** Enforce canonical SSR form for fact envelopes.  
- **Integration:** Stable facts support grounding (KnC/KnM/KnF), SSRGn, manifold projection, and Path‑B primitives.  
- **New primitives:** Declare fact interactions and satisfy SSR/manifold/Path‑B invariants.

---

## 13. Summary

KnB fact stability operates over SSR(t−1) to produce deterministic, monotonic, manifold‑compatible fact anchors for SSR(t). Facts evolve in a bounded, replay‑safe manner without mutating structure or generating meaning. Corrections are strictly limited by type and invariants. This system prevents semantic drift and ensures clean preparation for manifold projection and Path‑B consumption.

**End of knb_fact_stability.md**

---
