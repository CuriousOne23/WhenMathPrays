# pa_text_correction.md

**Document ID:** 20.XXX_pa_text_correction  
**Version:** 0.1  
**Date:** 2026-07-09  
**Status:** Draft — Realization Paper (Path A)  
**Purpose:** Define the Text Correction (TC) subsystem for Path A, including canonical correction rules, normalization operators, ambiguity-resolution heuristics, correction geometry, distortion repair, and stable manifold output for GS.

---

## 1. Overview

Text Correction (TC) in Path A is the bounded mechanism for detecting, classifying, and repairing textual distortions, mismatches, and ambiguities while preserving determinism, structural integrity, pre-/post-semantic separation, writer authority, and replay equivalence. TC operates primarily through the Interpretation Mismatch Resolver (IMR) framework and feeds corrected structures into downstream primitives.

TC ensures that the Thought Packet (TP) reaches a stable, coherent state suitable for Geometry Stabilizer (GS) input. All corrections are strictly bounded, deterministic, and respect the separation invariants defined in the Path A references.

---

## 2. Canonical Correction Rules

Correction rules govern when, how, and to what extent TC may intervene. They align with IMR Type A/B/C classifications and maintain all boundary conditions, field geometry hypotheses, and interpretation constraints.

- **Type A (Expression/Realization):** Purely structural or syntactic repairs. No meaning alteration. Limited to surface normalization.
- **Type B (Semantic Mismatch):** Bounded re-interpretation within identity-conditioned manifold charts. Uses correction context with explicit target fields.
- **Type C (Safety):** Immediate bounded containment or rejection. Highest priority.

**Core Rules (Future-HLR-001 to Future-HLR-005):**
- Future-HLR-001: Corrections preserve structural geometry invariants unless explicitly allowed in bounded SmOB scope.
- Future-HLR-002: Corrections do not modify committed meaning fields outside defined correction_context.
- Future-HLR-003: Corrections maintain monotonic accumulation of structural signals (with SmOB hashing exception).
- Future-HLR-004: Corrections enforce replay equivalence (correction artifacts stripped for baseline comparison). Replay equivalence requires that all correction artifacts be fully removable without altering committed structural or meaning fields. Replay-equivalent outputs must compare identically under CTP snapshot evaluation.
- Future-HLR-005: Depth limits, cooldowns, and caps apply to prevent unbounded recursion or drift.
- Writer authority and provenance are preserved at all boundaries.

---

## 3. Normalization Operators

Normalization operators transform raw or distorted inputs into canonical forms while respecting upstream boundary conditions (InB → IIInB → IE) and structure vector rules.

**Key Operators:**
- **Lexical/Surface Normalization:** Deterministic canonicalization of encoding, punctuation, shorthand expansions (with repair metadata attached). No semantic inference.
- **Structural Normalization:** Application of C1–C7 constraints via SOB/SROB/CnOB. Produces normalized structure vectors.
- **Vector Normalization:** L2-normalization of structure vectors:

$$
v_{\text{norm}} = \frac{v_{\text{struct}}}{\lVert v_{\text{struct}} \rVert_2}
$$

- **Residue Normalization:** Bounded compression and integration into structure vectors (SmOB only for hashing).
- **Meaning Normalization:** Identity-conditioned refinement within selected manifold chart (IdOB/RBU), preserving non-modification of structural fields.

All operators are deterministic, seed-free, and produce replay-equivalent outputs.

---

## 4. Ambiguity-Resolution Heuristics

Ambiguity-resolution heuristics operate within strict interpretation constraints: pre-semantic for structural stages, identity-conditioned for meaning stages. They prioritize structural coherence first, then meaning stability.

**Heuristics (in priority order):**
- **Structural Priority:** Resolve via C1–C7 constraints, missing-slot signals, and conflict geometry from CnOB/SmOB. Favor lowest distortion to structural graph G.
- **Entropy/Confidence Guidance:** Use ISc-derived distribution entropy and confidence fields to select lowest-ambiguity candidate.
- **Identity Anchoring:** For meaning-level ambiguities (post-structural), anchor to identity profile and selected IdOB manifold chart. Maintain path_b_eligible signaling.
- **Proximity Routing Bias:** Prefer resolutions that minimize distance in normalized structure vector space (σ, derived from normalized structure vectors per pa_structure_vectors.md) for stable routing.
- **Monotonicity Preservation:** Resolutions do not delete prior committed structural or meaning signals (Future-HLR-006).
- **Bounded Exploration:** Limit to finite candidate sets from CE; escalate via COP policy if unresolved.

Heuristics do not introduce new meaning into structural fields or vice versa (Future-HLR-007).

---

## 5. Correction Geometry and Distortion Repair

Correction geometry defines how TC repairs distortions while preserving overall field geometry hypotheses.

**Distortion Types:**
- Surface/lexical distortions (repaired upstream).
- Structural graph distortions (SOB → SmOB).
- Meaning-field inconsistencies (IdOB, within bounds).
- Routing signature mismatches (SSG/TR).

**Repair Principles:**
- **Geometric Projection:** Corrections apply deterministic projection operators within allowed basins:

$$
F^{(n+1)} = \Pi_{\text{corr}}(F^{(n)}, \text{CorrectionContext})
$$

- **Bounded Mutation:** Only modify fields explicitly targeted within correction_context; structural geometry changes limited to SmOB scope.
- **Distortion Repair Invariants:** Post-correction, structure vectors remain normalized and monotonic; meaning fields stable within identity manifold; envelopes maintain canonical shape. Meaning-field corrections never alter structural geometry outside SmOB scope. Structural geometry is immutable outside SmOB scope, enforcing strict pre-/post-semantic separation.
- **Residue Integration:** Accumulated repair signals feed into structure vectors (SmOB hashing only).
- **Clean vs. Corrected Geometry:** Corrected paths introduce explicit correction_context but preserve core invariants and replay equivalence when artifacts are stripped. Corrected geometry must still satisfy all Path A invariants.

IdOB and RBU do not alter structural geometry during repairs (Future-HLR-008).

---

## 6. TC Output to Stable Manifold for GS

TC culminates in producing a stable manifold state for the Geometry Stabilizer (GS):

- **Stability Criteria:** All required TP fields committed; structural signature σ stable, normalized, and monotonic (consistent with Future-HLR-003) and satisfies separation invariants defined in pa_structure_vectors.md; meaning fields refined and consistent with identity profile; path_b_eligible properly set; no unresolved high-entropy ambiguities within bounds.
- **Manifold Output:** A coherent, low-distortion manifold chart embedding the refined structure vectors, meaning fields, and routing metadata.
- **Handoff Guarantees:** Output satisfies terminal boundary conditions (OuBA), with immutable TP snapshot via CTP. Envelope is canonical and provenance-complete.
- **GS Readiness:** Provides deterministic input geometry for GS to further stabilize trajectories, basins, and relational mappings without violating any Path A invariants.

The output manifold is replay-deterministic and supports clean Path B integration.

---

## 7. Consistency with Path A References

- **Boundary Conditions:** All TC actions respect input/output envelopes, guards, postconditions, and clean/corrected distinctions.
- **Structure Vectors:** TC maintains normalization, monotonicity, separation, and SmOB-only hashing.
- **Field Geometry Hypotheses:** Enforces structural precedence, non-modification rules (IdOB/RBU), and deterministic evolution.
- **Interpretation Constraints:** Strict pre-/post-semantic separation; bounded, non-inferential operations.
- **Meaning Rules:** Identity-conditioned construction; no structural mutation; stable monotonic fields.

---

## 8. Summary

pa_text_correction.md defines a bounded, deterministic Text Correction subsystem for Path A that applies canonical rules, normalization operators, and heuristics to repair distortions while preserving all core invariants. It ensures a stable manifold output for GS, maintaining strict separation of concerns and enabling reliable meaning construction and Path B handoff.

**End of pa_text_correction.md**
