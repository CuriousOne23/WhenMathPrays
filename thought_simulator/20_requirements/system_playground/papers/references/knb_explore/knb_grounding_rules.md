# knb_grounding_rules.md

**Document ID:** 20.XXX_knb_grounding_rules  
**Version:** 0.2  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (KnB)  
**Purpose:** Define grounding rules for the Knowing‑by‑Binding (KnB) primitive operating over SSR and the manifold, producing stable knowledge anchors consumed by Path B.

---

## 1. Overview

KnB grounding transforms selected candidates and stabilized facts into stable, identity‑conditioned anchors over **SSR(t−1)** and produces deterministic grounded entries for **SSR(t)**. Grounding differs from candidate selection (generation/filtering) and fact stability (monotonic commitment) by producing **grounded anchors** that serve as reliable, manifold‑projectable references.

Grounding MUST guarantee SSR determinism, manifold compatibility, and Path‑B consumption safety. It operates **outside Path A**, consuming SSR‑exposed fields and producing SSR‑visible grounded anchors.

---

## 2. Grounding Foundations

- **Grounding envelopes:** Structured, bounded collections of grounded entries.  
- **Grounded fields:** `identity_ground[]`, `relation_ground[]`, `domain_anchor_ground[]`, `qualifier_ground[]`, `truth_validation_ground[]`, `KnDt_keywords_ground[]`, `KnDt_addresses_ground[]`.  
- **Grounding geometry:** Stable, monotonic anchors with provenance.  
- **Grounding provenance:** Traceable to candidates, facts, and SSR(t−1).  
- **Grounding monotonicity:** Once committed, grounded entries do not disappear.

**Finite set of grounded entries:**  
```
G_KnB = { g₁, g₂, …, g_k }
```

**Grounded entry derivation:**  
```
gᵢ = Ω(c*, F, SSR(t−1), IdentityProfile)
```

(Gloss: each grounded entry is derived deterministically from the selected candidate, stabilized facts, SSR(t−1), and identity profile.)

---

## 3. Grounding Rules

Rules govern deterministic grounding, refinement, monotonicity, geometry stability, and replay‑deterministic evolution.

- Grounding SHALL NOT modify SSR(t−1).  
- Grounding SHALL NOT generate new candidates.  
- Grounding SHALL NOT depend on Path‑B routing signals.  
- Grounding SHALL read only SSR‑exposed fields.

---

## 4. Grounding–Structure Interaction Rules

Grounding depends on structural geometry but never mutates it.

```
G_KnB = h(F_struct, c*, F, SSR(t−1), IdentityProfile)
```

Grounding enforces pre‑/post‑semantic separation and SSR freeze compliance.

---

## 5. Grounding–Meaning Interaction Rules

Grounding constrains meaning refinement and contributes to `path_b_eligible`. Meaning refinement depends on grounded entries.

- Grounding SHALL NOT modify meaning fields directly.  
- Meaning refinement SHALL NOT modify grounding geometry.  
- Grounding prevents semantic drift and supports SSR determinism.

---

## 6. Grounding Correction Rules (IMR Type A/B/C)

Rules govern correction boundaries, depth limits, cooldowns, invariants, and replay equivalence.

```
G_KnB^(n+1) = Ψ_corr(G_KnB^(n), CorrectionContext)
```

- **Type A:** realization‑only.  
- **Type B:** bounded semantic.  
- **Type C:** safety.  

Corrections SHALL NOT introduce new structural fields, alter structural geometry, or generate meaning.  
Corrections MUST preserve SSR determinism and manifold compatibility.

---

## 7. Grounding Serialization Rules

- Canonical ordering, naming, and grouping.  
- Canonical grounding envelope shape.  
- Replay‑deterministic serialization.

```
Serialize(G_KnB) = CanonicalForm(G_KnB)
```

Serialization MUST produce SSR‑visible canonical forms and satisfy manifold projection requirements.

---

## 8. Deterministic Grounding Guarantees

```
GroundDeterministic ⇔ f(x) = f(y) whenever x = y
```

All grounding operators are deterministic, seed‑free, replay‑equivalent, and SSR‑consistent.

---

## 9. SSR Integration Requirements

- Grounding operates over **SSR(t−1)** and produces grounded anchors for **SSR(t)**.  
- All grounded fields MUST serialize into SSR using canonical SSR field names.  
- Grounding MUST satisfy SSRGn rules (freeze, sanitization, provenance).  
- Grounding SHALL NOT read raw Path‑A fields; it SHALL read only SSR‑exposed fields.  
- Grounded anchors MUST be visible to manifold operators Π and Π⁻¹.

---

## 10. Manifold Compatibility Requirements

- Grounded anchors MUST map to manifold shapes defined in `manifold_geometry_shapes_spec.md`.  
- Each grounded entry MUST expose a meaning‑signature‑compatible structure (finite, typed, stable).  
- Grounded identity, relations, anchors, qualifiers MUST be geometrically projectable.  
- Grounded anchors MUST satisfy manifold routing constraints (curvature, locality, basin rules).  
- Grounded anchors MUST NOT introduce non‑projectable structures (infinite sets, unstable fields).  
- Grounding provenance MUST be preserved for manifold → OuBB reverse projection (Π⁻¹).

---

## 11. Path‑B Consumption Guarantees

- Grounded anchors MUST be consumable by LI (20.112) as stable meaning‑layer inputs.  
- Grounded anchors MUST support continuity_fields computed by CoHI.  
- Grounded anchors MUST satisfy OuBB truth/safety expression rules.  
- Grounded anchors MUST be compatible with RG/RSG surface‑form generation rules.  
- Grounded anchors MUST NOT require Path‑B to perform grounding or stability work.  
- Grounded anchors MUST remain unchanged after SSR freeze (SSR(t) is immutable to Path‑B).

---

## 12. Realization Notes

- **Implementation:** Implement grounding as deterministic operators that produce stable anchors with monotonicity guards.  
- **Validation:** Assert monotonicity, SSR compliance, manifold compatibility, separation, and provenance invariants.  
- **Testing:** Replay tests, manifold projection tests, Path‑B consumption tests, drift‑prevention cases.  
- **Serialization:** Enforce canonical SSR form for grounding envelopes.  
- **Integration:** Grounded entries support fact stability, candidate selection, SSRGn, manifold projection, and Path‑B primitives.  
- **New primitives:** Declare grounding interactions and satisfy SSR/manifold/Path‑B invariants.

---

## 13. Summary

KnB grounding operates over SSR(t−1) to produce deterministic, monotonic, manifold‑compatible grounded anchors for SSR(t). Grounding enforces strict non‑mutation of structure, prevents semantic drift, and supports bounded corrections. These rules ensure replay safety and clean preparation for manifold projection and Path‑B consumption.

**End of knb_grounding_rules.md**
