# pb_safety_constraints.md

**Title:** Path B Safety Constraints — Expression-Side Enforcement Rules  
**Document ID:** Future-HLR  
**Version:** 1.0 (Playground White Paper)  
**Date:** 2026-07-07  
**Status:** Complete — Playground Reference  
**Location:** thought_simulator/system_playground/  
**Purpose:** Define the safety constraints that govern Path B expression while preserving strict architectural separation from Path A.

---

## 1. Introduction — Safety Constraints in Path B

Path B is the realization layer of the Thought Simulator. It converts the immutable SSR produced at the Path A boundary into surface-form expression.

Safety constraints in Path B are the deterministic rules that ensure all expressed output respects TPSF and TPTB metadata, SSR commitments, continuity fields, and manifold projections — without performing any safety evaluation or meaning mutation.

Path B safety enforcement is strictly expression-side.

---

## 2. Definition of Safety Constraints (Expression-Side)

Safety constraints in Path B are the set of immutable rules that govern how expression primitives select patterns, apply qualifications, and enforce scoping based on TPSF and TPTB metadata.

They ensure safe, compliant surface output while preserving the committed meaning and identity from the SSR.

**Rule future-HLR:** Path B shall never perform safety evaluation; it shall only consume and apply safety metadata provided by Path A.

---

## 3. Upstream Safety Inputs (TPSF, TPTB, SSR, CoHI, LI, KnB)

Path B safety constraints operate exclusively on the following read-only inputs:

- TPSF (safety flags, severity, required qualification/refusal, allowed_scope)
- TPTB (truth conflict metadata, alignment)
- SSR continuity_fields and semantic_core (from CoHI and LI)
- KnB grounding tiers
- Manifold projections embedded in the SSR

No other structures shall be accessed for safety decisions.

---

## 4. Deterministic Safety Constraint Rules (future-HLR placeholders)

**Rule future-HLR:** Path B shall map TPSF and TPTB metadata to expression patterns (qualification, refusal, redirection, scoping) using deterministic lookup.

**Rule future-HLR:** Safety-driven adjustments shall modify only discourse act and surface phrasing; they shall never alter propositional content, stance, or referents.

**Rule future-HLR:** When TPSF indicates high severity or requires refusal, Path B shall select only allowed_scope patterns and shall suppress disallowed content.

---

## 5. Safety-Driven Discourse-Act Adjustments

Path B may adjust the discourse act when explicitly required by TPSF/TPTB.

**Rule future-HLR:** Any safety-driven discourse-act adjustment shall be limited to the envelope defined by TPSF and shall preserve the underlying SSR meaning and identity continuity.

---

## 6. Forbidden Safety Transformations

Path B shall not:
- Perform safety evaluation or reinterpret TPSF/TPTB.
- Introduce content outside the allowed_scope defined by TPSF.
- Override safety metadata to enable disallowed expression.
- Modify SSR, continuity_fields, or lineage under safety constraints.
- Use safety rules as justification for meaning or identity changes.

---

## 7. Manifold → Safety Mapping (Projection-Only)

Safety constraints operate on the manifold projection already present in the SSR.

**Rule future-HLR:** Path B shall apply safety rules to the projected manifold structures without performing navigation or transformation of basins.

---

## 8. KnB Grounding and Safety Stability

KnB grounding tiers shall inform safe expression choices.

**Rule future-HLR:** When applying safety constraints, Path B shall respect KnB grounding tiers and shall not invent detail that would bypass safety scoping or qualification requirements.

---

## 9. OuBB Commit Boundary and Safety Guarantees

OuBB is the final commit boundary for Path B.

**Rule future-HLR:** At OuBB commit, all safety constraints shall be fully enforced such that the expressed artifact is guaranteed to respect TPSF/TPTB metadata.

Safety violations at runtime shall trigger IMR routing without mutating the SSR.

---

## 10. Runtime Contract for Safety Constraints

Safety constraint enforcement shall begin only after:
- SSR is frozen by SSRGn.
- CoHI and LI have completed their writes.
- ReB has validated invariants.

All safety operations shall remain read-only on upstream metadata.

---

## 11. Replay Contract (Safety Constraints Across Turns)

Replay fixtures shall verify safety constraint preservation.

**Rule future-HLR:** Stripping stylistic variation from OuBB artifacts shall recover exact compliance with the originating TPSF/TPTB metadata and SSR commitments.

Replay shall confirm that safety-driven patterns remain consistent and reversible across turns.

---

## 12. Examples (Minimal, Precise)

**Example 1 — Qualification**  
TPSF requires qualification. Path B produces: "It appears that..." while preserving exact propositional content.

**Example 2 — Refusal**  
TPSF indicates high-severity refusal. Path B selects a safe redirection template within allowed_scope without providing disallowed content.

**Example 3 — Scoped Response**  
TPSF limits scope. Path B produces only high-level information consistent with the constraint.

---

## 13. Appendix: Relationship to Path A Safety Evaluation and Manifold Geometry

Path A performs all safety evaluation and produces TPSF/TPTB metadata. Path B only consumes and applies these metadata during expression.

Manifold geometry is projected into the SSR; Path B applies safety constraints to this projection without navigation or modification.

This design maintains strict A/B separation while ensuring safe, reversible expression. It is fully consistent with pb_expression_rules.md, pb_identity_continuity.md, pb_local_inference.md, 20.705, SSRGn, CoHI, LI, ReB invariants, KnB grounding, and all manifold papers.

---

*End of pb_safety_constraints.md*
