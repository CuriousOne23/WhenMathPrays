# pb_identity_continuity.md

**Title:** Path B Identity Continuity — Expression-Side Preservation Across Turns and Variants  
**Document ID:** future-HLR  
**Version:** 1.0 (Playground White Paper)  
**Date:** 2026-07-07  
**Status:** Complete — Playground Reference  
**Location:** thought_simulator/system_playground/  
**Purpose:** Define how Path B maintains identity continuity during expression generation while respecting all architectural boundaries.

---

## 1. Introduction — Identity Continuity in Path B

Path B is the realization layer of the Thought Simulator. It converts the immutable SSR produced at the Path A boundary into surface-form expression.

Identity continuity in Path B is strictly expression-side. It ensures that expressed identity (referents, discourse participants, core continuity) remains stable across turns, stylistic variants, and seeds, without Path B performing identity evaluation or meaning construction.

Path B derives continuity exclusively from SSR continuity_fields (produced by CoHI), LI meaning-layer commitments, manifold projections, and KnB grounding tiers.

---

## 2. Definition of Identity Continuity (Expression-Side)

Identity continuity in Path B means that all surface expressions preserve the identity structures committed in the SSR.

It guarantees that referents, core identifiers, relational bindings, and discourse continuity remain consistent in expression even when stylistic variation is applied.

**Path B shall not** evaluate, resolve, or modify identity. It shall only project and preserve the identity already stabilized in the SSR.

---

## 3. Upstream Identity Inputs (SSR, CoHI, LI, Manifold)

Path B receives identity-related inputs exclusively from:

- **SSR continuity_fields** (structural_history, referential_history, conversation_objects, topic_threads, continuity_markers) produced by CoHI.
- **LI meaning-layer commitments** (resolved meaning with associated referents and bindings).
- **Manifold basin projections** embedded in the SSR (object/relational basins, identity anchors).
- **KnB grounding tiers** (identity_coarse / identity_medium / identity_fine).

These inputs are read-only.

---

## 4. Deterministic Continuity Rules

**Rule future-HLR-001:** Path B shall map SSR identity structures to surface expressions using only the provided continuity_fields and grounded referents.

**Rule future-HLR-002:** All expression primitives (RG, RSG, OuBB) shall treat continuity_fields as immutable for the duration of the turn.

**Rule future-HLR-003:** The continuity transfer function shall be:

$$
\text{Expressed}\_{Identity} = \text{Project}\left( \text{SSR.continuity}\_{fields} \cup \text{KnB.identity}\_{tiers} \cup \text{LI.meaning} \right)
$$

where Project preserves all identity anchors and relational bindings.

---

## 5. Seed-Bounded Variation and Identity Preservation

Stylistic variation controlled by the response-generator seed shall affect only surface phrasing and shall never alter identity referents, core identifiers, or relational bindings.

**Rule future-HLR-004:** Seed variation shall be identity-neutral. Any expressed output with identical SSR shall collapse to the same identity representation when stylistic variation is stripped.

---

## 6. Forbidden Identity Transformations

Path B shall not:
- Introduce new referents or bindings not present in the SSR.
- Resolve ambiguous identity (this belongs to Path A and KnB).
- Modify continuity_fields or lineage.
- Allow stylistic variation to change pronoun resolution or core identity anchors.
- Drift identity across turns outside the continuity_fields provided by CoHI.

---

## 7. Manifold → Identity Continuity Mapping

Path B consumes the manifold projection present in the SSR.

**Rule future-HLR-005:** Manifold identity structures (basin assignments, relational geometry) shall be preserved in expression through consistent grounding tier selection and referent anchoring. Path B performs basin-preserving linearization of identity but does not navigate or modify manifold geometry.

---

## 8. KnB Grounding and Identity Stability

KnB provides tiered identity grounding (coarse → medium → fine) that Path B uses for expression.

**Rule future-HLR-006:** Path B shall select the lowest sufficient KnB identity tier consistent with total entropy. Higher-precision tiers (KnF) shall respect constraints from lower tiers (KnM/KnC) when ambiguity persists.

This ensures stable identity expression without invention of detail.

---

## 9. OuBB Commit Boundary and Continuity Guarantees

OuBB is the final commit boundary for Path B expression.

**Rule future-HLR-007:** At OuBB commit, identity continuity shall be fully captured in the expressed artifact such that replay can recover the originating SSR identity structures exactly.

Incomplete-meaning or continuity faults shall be routed via IMR without mutating SSR identity fields.

---

## 10. Runtime Contract for Identity Continuity

Runtime execution of identity continuity shall begin only after:
- SSR is frozen.
- CoHI has written continuity_fields.
- LI has committed meaning-layer identity.
- ReB has validated invariants.

All Path B primitives shall operate read-only on identity inputs.

---

## 11. Replay Contract (Identity Continuity Across Turns)

Replay shall verify that identity continuity is preserved across turns.

**Rule future-HLR-008:** Replay fixtures shall confirm that stripping stylistic variation from any sequence of OuBB artifacts recovers the exact sequence of SSR identity structures and continuity_fields.

Replay shall be seed-aware and shall validate collapse to a single canonical identity representation per SSR.

---

## 12. Examples (Minimal, Precise)

**Example 1 — Stable Referent**  
SSR continuity_fields contain a persistent conversation_object ("the dataset").  
Path B expressions across turns consistently refer to it as "the dataset" or equivalent grounded terms, regardless of stylistic variation.

**Example 2 — Pronoun Continuity**  
CoHI provides referential_history linking "it" to a prior referent.  
Path B maintains correct pronoun resolution in expression without re-resolving identity.

**Example 3 — Cross-Turn Stability**  
Manifold basin projection remains stable.  
Path B expressions preserve the same core identity anchors across multiple turns despite seed variation.

---

## 13. Appendix: Relationship to Path A Identity and Manifold Basins

Path A (with KnB support) is responsible for identity construction, resolution, and commitment into the SSR. Path B only projects and preserves this committed identity during expression.

Manifold basins provide the underlying relational geometry. Path B consumes the SSR projection of these basins to maintain expression-side continuity without performing basin navigation or modification.

This design ensures strict separation while guaranteeing identity stability across the full TS pipeline. It aligns with pb_expression_rules.md, 20.705 Path A/Path B flow, SSRGn, CoHI, LI, and all manifold papers.

---

*End of pb_identity_continuity.md*
