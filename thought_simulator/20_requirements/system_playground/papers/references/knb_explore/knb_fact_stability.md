# knb_fact_stability.md

**Document ID:** 20.XXX_knb_fact_stability  
**Version:** 0.1  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (KnB)  
**Purpose:** Define fact-stability rules for the Knowing-by-Binding (KnB) primitive in Path A.

---

## 1. Overview

KnB fact stability governs the stabilization of identity-conditioned facts after candidate selection. It prevents semantic drift, enforces bounded corrections, and ensures replay-deterministic fact evolution while supporting meaning construction and Path B handoff.

Fact stability is required to maintain coherence across cycles, preserve invariants, and provide stable anchors for identity resolution and realization.

---

## 2. Fact Foundations

- **Fact envelopes:** Structured, bounded collections of stabilized facts.  
- **Fact fields:** identity_fact[], relation_fact[], domain_anchor_fact[], qualifier_fact[], truth_validation_fact[], KnDt_keywords[], KnDt_addresses[].  
- **Fact geometry:** Stable, monotonic sets with provenance.  
- **Fact provenance:** Traceable to selected candidates and identity profile.  
- **Fact monotonicity and stability invariants:** Once committed, facts do not disappear.

**Finite fact set:**  

$$
F = \{f_1, f_2, \dots, f_m\}
$$  

(Gloss: finite fact set.)

**Fact derivation:**  

$$
f_i = \Lambda(c^\ast, \text{IdentityProfile})
$$  

(Gloss: each fact is derived deterministically from the selected candidate and identity profile.)

---

## 3. Fact Stability Rules

Rules govern deterministic fact formation, refinement, monotonicity (facts do not disappear once committed), field stability, geometry stability, and replay-deterministic evolution.

- Fact stability SHALL NOT modify structural fields.  
- Fact stability SHALL NOT generate new candidates.  
- Fact stability SHALL NOT depend on routing signals.

---

## 4. Fact–Structure Interaction Rules

Facts depend on structural geometry but never mutate it.  

$$
F = g(F_{\text{struct}}, c^\ast, \text{IdentityProfile})
$$  

(Gloss: facts are a function of structural geometry, selected candidate, and identity profile.)

Fact stability enforces pre-/post-semantic separation.

---

## 5. Fact–Meaning Interaction Rules

Facts constrain meaning refinement and contribute to `path_b_eligible`. Meaning refinement depends on stable facts.  

- Fact stability SHALL NOT modify meaning fields directly.  
- Meaning refinement SHALL NOT modify fact geometry.  
- Fact stability prevents semantic drift.

---

## 6. Fact Correction Rules (IMR Type A/B/C)

Rules govern correction boundaries, depth limits, cooldowns, invariants, and replay equivalence.  

$$
F^{(n+1)} = \Psi_{\text{corr}}(F^{(n)}, \text{CorrectionContext})
$$  

(Gloss: fact corrections are bounded and deterministic.)

- Type A: realization-only.  
- Type B: bounded semantic.  
- Type C: safety.  

Corrections SHALL NOT introduce new structural fields, alter structural geometry, or generate meaning.

---

## 7. Fact Serialization Rules

- Canonical ordering, naming, and grouping.  
- Canonical fact envelope shape.  
- Replay-deterministic serialization.

$$
\text{Serialize}(F) = \text{CanonicalForm}(F)
$$  

(Gloss: fact sets must serialize deterministically.)

---

## 8. Deterministic Fact Guarantees

$$
\text{FactDeterministic} \iff f(x) = f(y) \;\text{whenever}\; x = y
$$  

(Gloss: identical inputs yield identical fact sets.)

All fact-stability operators are deterministic, seed-free, and replay-equivalent.

---

## 9. Realization Notes

- **Implementation:** Implement fact derivation, stabilization, and correction as deterministic operators with monotonicity guards.  
- **Validation:** Assert stability, monotonicity, separation, and provenance invariants.  
- **Testing:** Replay tests, clean/corrected fact paths, drift-prevention cases.  
- **Serialization:** Enforce canonical form for fact envelopes.  
- **Integration:** Stable facts support meaning construction, candidate selection, OB-family primitives, and Path B eligibility.  
- **New primitives:** Declare fact interactions and satisfy existing stability/monotonicity invariants.

---

## 10. Summary

KnB fact stability provides monotonic, deterministic anchors for identity-conditioned facts after candidate selection. Facts evolve in a bounded, replay-safe manner without mutating structure or generating meaning. Corrections are strictly limited by type and invariants. This system prevents semantic drift and ensures clean preparation for Path B handoff.

**End of knb_fact_stability.md**
