# knb_grounding_rules.md

**Document ID:** 20.XXX_knb_grounding_rules  
**Version:** 0.1  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (KnB)  
**Purpose:** Define grounding rules for the Knowing-by-Binding (KnB) primitive in Path A.

---

## 1. Overview

KnB grounding transforms selected candidates and stabilized facts into stable, identity-conditioned anchors for meaning construction. It differs from candidate selection (generation/filtering) and fact stability (monotonic commitment) by producing grounded entries that serve as reliable references.

Grounding is required to prevent semantic drift, enforce deterministic anchors, and support safe Path B handoff while preserving replay equivalence and pre-/post-semantic separation.

---

## 2. Grounding Foundations

- **Grounding envelopes:** Structured, bounded collections of grounded entries.  
- **Grounded fields:** identity_ground[], relation_ground[], domain_anchor_ground[], qualifier_ground[], truth_validation_ground[], KnDt_keywords_ground[], KnDt_addresses_ground[].  
- **Grounding geometry:** Stable, monotonic anchors with provenance.  
- **Grounding provenance:** Traceable to candidates, facts, and identity profile.  
- **Grounding monotonicity and stability invariants:** Once committed, grounded entries do not disappear.

**Finite set of grounded entries:**  

$$
G_{\text{KnB}} = \{g_1, g_2, \dots, g_k\}
$$  

(Gloss: finite set of grounded entries.)

**Grounded entry derivation:**  

$$
g_i = \Omega(c^\ast, F, \text{IdentityProfile})
$$  

(Gloss: each grounded entry is derived deterministically from the selected candidate, stabilized facts, and identity profile.)

---

## 3. Grounding Rules

Rules govern deterministic grounding, refinement, monotonicity (grounded entries do not disappear once committed), field stability, geometry stability, and replay-deterministic evolution.

- Grounding SHALL NOT modify structural fields.  
- Grounding SHALL NOT generate new candidates.  
- Grounding SHALL NOT depend on routing signals.

---

## 4. Grounding–Structure Interaction Rules

Grounding depends on structural geometry but never mutates it.  

$$
G_{\text{KnB}} = h(F_{\text{struct}}, c^\ast, F, \text{IdentityProfile})
$$  

(Gloss: grounded entries are a function of structural geometry, selected candidate, stabilized facts, and identity profile.)

Grounding enforces pre-/post-semantic separation.

---

## 5. Grounding–Meaning Interaction Rules

Grounding constrains meaning refinement and contributes to `path_b_eligible`. Meaning depends on grounded entries.  

- Grounding SHALL NOT modify meaning fields directly.  
- Meaning refinement SHALL NOT modify grounding geometry.  
- Grounding prevents semantic drift.

---

## 6. Grounding Correction Rules (IMR Type A/B/C)

Rules govern correction boundaries, depth limits, cooldowns, invariants, and replay equivalence.  

$$
G_{\text{KnB}}^{(n+1)} = \Psi_{\text{corr}}(G_{\text{KnB}}^{(n)}, \text{CorrectionContext})
$$  

(Gloss: grounding corrections are bounded and deterministic.)

- Type A: realization-only.  
- Type B: bounded semantic.  
- Type C: safety.  

Corrections SHALL NOT introduce new structural fields, alter structural geometry, or generate meaning.

---

## 7. Grounding Serialization Rules

- Canonical ordering, naming, and grouping.  
- Canonical grounding envelope shape.  
- Replay-deterministic serialization.

$$
\text{Serialize}(G_{\text{KnB}}) = \text{CanonicalForm}(G_{\text{KnB}})
$$  

(Gloss: grounded entries must serialize deterministically.)

---

## 8. Deterministic Grounding Guarantees

$$
\text{GroundDeterministic} \iff f(x) = f(y) \;\text{whenever}\; x = y
$$ 

(Gloss: identical inputs yield identical grounded outputs.)

All grounding operators are deterministic, seed-free, and replay-equivalent.

---

## 9. Realization Notes

- **Implementation:** Implement grounding as deterministic operators that produce stable anchors with monotonicity guards.  
- **Validation:** Assert monotonicity, provenance, separation, and stability invariants.  
- **Testing:** Replay tests, clean/corrected grounding paths, drift-prevention cases.  
- **Serialization:** Enforce canonical form for grounding envelopes.  
- **Integration:** Grounded entries support meaning construction, fact stability, candidate selection, OB-family primitives, and Path B eligibility.  
- **New primitives:** Declare grounding interactions and satisfy existing stability/monotonicity invariants.

---

## 10. Summary

KnB grounding rules transform selected candidates and stabilized facts into monotonic, deterministic anchors for identity-conditioned meaning. Grounding enforces strict non-mutation of structure, prevents semantic drift, and supports bounded corrections. These rules ensure replay safety and clean preparation for Path B handoff.

**End of knb_grounding_rules.md**
