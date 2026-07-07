# pb_local_inference.md

**Title:** Path B Local Inference — Expression-Side Micro-Inference Rules  
**Document ID:** Future-HLR  
**Version:** 1.0 (Playground White Paper)  
**Date:** 2026-07-07  
**Status:** Complete — Playground Reference  
**Location:** thought_simulator/system_playground/  
**Purpose:** Define how Path B performs strictly expression-side local inference without altering meaning, identity, or SSR commitments.

---

## 1. Introduction — Local Inference in Path B

Path B is the realization layer of the Thought Simulator. It converts the immutable SSR produced at the Path A boundary into surface-form expression.

Local inference in Path B consists of minimal, expression-side micro-inference operations used to select phrasing, maintain coherence, preserve continuity, satisfy discourse-act constraints, and apply safety-driven patterns.

Local inference shall never construct meaning, resolve identity, alter the SSR, perform truth evaluation, modify continuity_fields, or navigate the manifold.

---

## 2. Definition of Local Inference (Expression-Side)

Local inference is the set of deterministic, surface-form operations that map committed SSR meaning and metadata into coherent linguistic realizations.

It operates entirely downstream of LI meaning commitment and is limited to choices among equivalent expressions that preserve the underlying semantics.

**Rule future-HLR:** Local inference shall be expression-neutral with respect to meaning, identity, and manifold geometry.

---

## 3. Upstream Inputs Used for Local Inference (SSR, CoHI, LI, KnB, Manifold)

Path B local inference consumes only the following read-only inputs:

- SSR continuity_fields (from CoHI)
- LI meaning-layer commitments
- KnB grounding tiers (identity/relation/qualifier fields)
- TPTB and TPSF metadata
- Manifold projections embedded in the SSR

No other structures shall be accessed.

---

## 4. Deterministic Local Inference Rules (future-HLR placeholders)

**Rule future-HLR:** Local inference shall select phrasing and structural variants using only SSR metadata, KnB grounding, and discourse-act constraints.

**Rule future-HLR:** All local inference decisions shall be deterministic for a fixed SSR and fixed seed.

**Rule future-HLR:** Local inference shall respect entropy tiers from KnB when choosing level of detail in expression.

---

## 5. Seed-Bounded Variation and Local Inference Neutrality

The response-generator seed shall influence only surface-form choices (lexical, syntactic, stylistic).

**Rule future-HLR:** Seed-bounded variation shall be local-inference neutral: it shall not change the underlying propositional content, referents, or required qualifications derived from the SSR.

---

## 6. Forbidden Local Inference Operations

Path B local inference shall not:
- Introduce new propositions or inferences.
- Resolve or alter identity (beyond projecting grounded referents).
- Modify SSR fields, continuity_fields, or lineage.
- Override TPTB or TPSF metadata except for explicit safety-driven expression adjustments.
- Perform manifold navigation or basin transformation.

---

## 7. Manifold → Local Inference Mapping (Projection-Only)

Local inference operates exclusively on the manifold projection already present in the SSR.

**Rule future-HLR:** Path B shall perform projection-only mapping of manifold structures into linear expression, preserving basin assignments without navigation or modification.

---

## 8. KnB Grounding and Local Inference Stability

Local inference shall use KnB grounding tiers to ensure stable and coherent expression.

**Rule future-HLR:** When selecting among variants, local inference shall respect the lowest sufficient KnB tier and shall not invent detail that would lower entropy beyond what is grounded in the SSR.

---

## 9. OuBB Commit Boundary and Local Inference Guarantees

OuBB is the final commit boundary for Path B.

**Rule future-HLR:** At OuBB commit, all local inference decisions shall be fully captured such that the expressed artifact remains reversible to the originating SSR.

Local inference shall not introduce any state that prevents exact replay or identity/meaning recovery.

---

## 10. Runtime Contract for Local Inference

Local inference shall execute only after:
- SSR is frozen by SSRGn.
- CoHI and LI have completed their writes.
- ReB has validated invariants.

All operations shall remain read-only on upstream artifacts.

---

## 11. Replay Contract (Local Inference Across Turns)

Replay fixtures shall verify that local inference choices are fully recoverable.

**Rule future-HLR:** Stripping stylistic and local-inference variation from OuBB artifacts shall recover the exact originating SSR meaning, identity, and continuity structures.

Replay shall be seed-aware and shall confirm collapse to a single canonical representation.

---

## 12. Examples (Minimal, Precise)

**Example 1 — Phrasing Selection**  
SSR contains a resolved proposition. Local inference selects among equivalent phrasings ("The value is 42", "We observe 42") while preserving exact meaning.

**Example 2 — Continuity Maintenance**  
CoHI continuity_fields link a referent. Local inference maintains consistent reference across sentences without re-resolving identity.

**Example 3 — Safety Pattern**  
TPSF requires qualification. Local inference applies a safety-aware phrasing template without altering propositional content.

---

## 13. Appendix: Relationship to Path A Inference and Manifold Geometry

Path A (with KnB) performs all meaning construction and identity resolution. Path B performs only local, expression-side inference on the committed SSR projection.

Manifold geometry is projected into the SSR; Path B consumes this projection for coherence but does not navigate or transform basins.

This design maintains strict separation while enabling coherent, reversible expression. It is fully consistent with pb_expression_rules.md, pb_identity_continuity.md, 20.705, SSRGn, CoHI, LI, ReB invariants, and all manifold papers.

---

*End of pb_local_inference.md*
