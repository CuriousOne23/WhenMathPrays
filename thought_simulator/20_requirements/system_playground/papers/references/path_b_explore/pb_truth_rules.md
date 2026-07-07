# pb_truth_rules.md

**Title:** Path B Truth Rules — Expression-Side Truth Metadata Handling  
**Document ID:** Future-HLR  
**Version:** 1.0 (Playground White Paper)  
**Date:** 2026-07-07  
**Status:** Complete — Playground Reference  
**Location:** thought_simulator/system_playground/  
**Purpose:** Define how Path B consumes and applies truth metadata during expression without performing truth evaluation or meaning mutation.

---

## 1. Introduction — Truth Rules in Path B

Path B is the realization layer of the Thought Simulator. It converts the immutable SSR produced at the Path A boundary into surface-form expression.

Truth rules in Path B are the deterministic, expression-side rules that govern how TPTB (and related TPSF truth fields) metadata is used to shape output — ensuring conflicts, uncertainty, alignment, and qualifications are properly surfaced while preserving committed meaning.

Path B performs no truth evaluation, comparison, or reinterpretation.

---

## 2. Definition of Truth Rules (Expression-Side)

Truth rules in Path B define how expression primitives map TPTB metadata into surface patterns such as qualification, clarification, hedging, or explicit conflict acknowledgment.

They ensure truth stance is expressed faithfully without altering the underlying propositional content or stance committed in the SSR.

**Rule future-HLR:** Path B shall treat TPTB metadata as authoritative and immutable for the purpose of expression pattern selection.

---

## 3. Upstream Truth Inputs (TPTB, TPSF truth fields, SSR, CoHI, LI, KnB)

Path B truth rules operate exclusively on the following read-only inputs:

- TPTB (truth_conflict, conflict_type, alignment, explanation, hypothesis_band)
- Related TPSF truth-linked fields
- SSR semantic_core and continuity_fields (from CoHI and LI)
- KnB grounding tiers
- Manifold projections embedded in the SSR

No other structures shall be accessed for truth-related decisions.

---

## 4. Deterministic Truth Rule Set (future-HLR placeholders)

**Rule future-HLR:** Path B shall map TPTB fields to deterministic expression patterns (qualification markers, conflict acknowledgment, alignment tone).

**Rule future-HLR:** Truth-aware adjustments shall affect only surface form and discourse framing; they shall never modify propositional content or referents.

**Rule future-HLR:** When TPTB indicates conflict, Path B shall include appropriate qualification or clarification phrasing without resolving the conflict.

---

## 5. Truth Conflict Expression Patterns

Path B shall select patterns that surface detected conflicts as specified by TPTB.

**Rule future-HLR:** Conflict expression shall use hedging language, explicit acknowledgment, or clarification requests consistent with the conflict_type and hypothesis_band, while preserving the original meaning.

---

## 6. Truth Alignment, Uncertainty, and Qualification

Path B shall apply alignment tone, uncertainty markers, and qualification based on TPTB.

**Rule future-HLR:** Uncertainty and qualification shall be expressed proportionally to the metadata (e.g., hypothesis_band) without inventing new evidence or altering stance.

---

## 7. Forbidden Truth Transformations

Path B shall not:
- Perform truth evaluation or comparison.
- Resolve or suppress conflicts present in TPTB.
- Override TPTB metadata to enable stronger claims.
- Modify SSR, continuity_fields, or lineage under truth rules.
- Use truth metadata as justification for meaning or identity changes.

---

## 8. Manifold → Truth Mapping (Projection-Only)

Truth rules operate on the manifold projection already present in the SSR.

**Rule future-HLR:** Path B shall apply truth-aware patterns to the projected manifold structures without performing navigation or transformation of basins.

---

## 9. KnB Grounding and Truth Stability

KnB grounding tiers shall support stable truth-aware expression.

**Rule future-HLR:** Local inference under truth constraints shall respect KnB tiers and shall not invent detail that would bypass qualification or conflict acknowledgment requirements.

---

## 10. OuBB Commit Boundary and Truth Guarantees

OuBB is the final commit boundary for Path B.

**Rule future-HLR:** At OuBB commit, all truth rules shall be fully applied such that the expressed artifact respects TPTB metadata exactly.

Truth-related issues shall trigger appropriate IMR routing without mutating the SSR.

---

## 11. Runtime Contract for Truth Rules

Truth rule enforcement shall begin only after:
- SSR is frozen by SSRGn.
- CoHI and LI have completed their writes.
- ReB has validated invariants.

All truth operations shall remain read-only on upstream metadata.

---

## 12. Replay Contract (Truth Rules Across Turns)

Replay fixtures shall verify truth rule preservation.

**Rule future-HLR:** Stripping stylistic variation from OuBB artifacts shall recover exact compliance with the originating TPTB metadata and SSR commitments.

Replay shall confirm that truth-aware patterns remain consistent and reversible across turns.

---

## 13. Examples (Minimal, Precise)

**Example 1 — Conflict Acknowledgment**  
TPTB indicates conflict. Path B produces: "The value appears to be 42, although this conflicts with prior data." (preserving original propositions).

**Example 2 — Uncertainty Qualification**  
TPTB hypothesis_band is medium. Path B applies moderate hedging: "It is likely that..." without stronger claims.

**Example 3 — Alignment**  
TPTB shows misalignment. Path B selects neutral or distancing phrasing while maintaining factual content.

---

## 14. Appendix: Relationship to Path A Truth Evaluation and Manifold Geometry

Path A performs all truth evaluation and produces TPTB metadata. Path B only consumes and applies this metadata during expression.

Manifold geometry is projected into the SSR; Path B applies truth rules to this projection without navigation or modification.

This design maintains strict A/B separation while ensuring truthful, reversible expression. It is fully consistent with pb_expression_rules.md, pb_identity_continuity.md, pb_local_inference.md, pb_safety_constraints.md, 20.705, SSRGn, CoHI, LI, ReB invariants, KnB grounding, and all manifold and TPTB/TPSF papers.

---

*End of pb_truth_rules.md*
