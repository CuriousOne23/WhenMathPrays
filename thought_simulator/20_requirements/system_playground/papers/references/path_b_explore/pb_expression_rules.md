# pb_expression_rules.md

**Title:** Path B Expression Rules — Deterministic Meaning-to-Surface Realization  
**Document ID:** 20.30.090  
**Version:** 1.0 (Playground White Paper — CP Reviewed)  
**Date:** 2026-07-07  
**Status:** Complete — Playground Reference  
**Location:** thought_simulator/system_playground/  
**Purpose:** Define how Path B converts committed SSR meaning into surface expression while preserving all architectural invariants.

---

## 1. Introduction — What Path B Is and Why It Exists

Path B is the realization layer of the Thought Simulator. It consumes the immutable Semantic Snapshot Reference (SSR) produced at the Path A commit boundary (via OuBA and SSRGn) and converts structured meaning into surface-form expression.

Path B is expression-only. It performs no meaning construction, inference, truth evaluation, or safety evaluation. Path B has no access to truth-evaluation primitives (TB, TPTB, TPSF) beyond reading their metadata; it cannot re-evaluate or reinterpret them.

The core regime is deterministic core + bounded stylistic freedom. Meaning must be preserved exactly.

---

## 2. Definition of Expression Primitives

The primary expression primitives in Path B are:

- **RG** (Response Generator): Performs realization planning and semantic-to-linguistic mapping as a read-only consumer of SSR and metadata.
- **RSG** (Response Surface Generator): Renders the final surface-form text from the realization plan and accumulated substrate.
- **OuBB** (Output Basin): Performs final expression commit, applies seed-bound variability, and routes incomplete-meaning cases to IMR. OuBB is the only commit boundary for Path B.

RG and RSG shall operate on isolated expression substrates and shall not write to continuity_fields, lineage, or any SSR-adjacent structure.

---

## 3. Deterministic Core Rules

The primary transfer function is:

$$
\text{Expression} = \text{RSG}\left( \text{RG}\left( \text{SSR}, \text{TPTB}, \text{TPSF}, \text{continuity}\_{fields}, \text{exec}\_{plan} \right), \text{seed} \right)
$$

Path B shall produce deterministic output for any fixed SSR and fixed response-generator seed (modulo allowed stylistic variation).

The seed influences only stylistic variation and shall never alter propositional content, stance, or required qualifications.

Path B shall consume TPTB and TPSF metadata to select expression patterns without re-performing evaluation.

---

## 4. Allowed Stylistic Variants (Bounded Freedom)

Path B may select among equivalent surface realizations inside a bounded envelope defined by the discourse act, OBG/register policy, and exec_plan.

Allowed variations include lexical choice (consistent with KnF), syntactic rephrasing of the same propositions, and bounded adjustments in conciseness or formality.

All stylistic variants shall remain SSR-recoverable (reversible by stripping variation).

---

## 5. Forbidden Transformations

Path B shall not:
- Add, remove, or alter referents, bindings, or constraints from the semantic_core.
- Introduce new propositions or perform inference.
- Override or reinterpret TPTB or TPSF metadata except for explicit safety-driven adjustments.
- Modify continuity_fields, lineage, or any Path A artifact.
- Change the meaning-layer commitment produced by LI.

Safety-driven adjustments shall modify only the discourse act and never the underlying propositional content or stance.

---

## 6. Meaning Preservation Guarantees

The mapping from SSR to expressed output shall preserve the exact propositional content, stance, required qualifications, and lineage metadata.

Replay with identical SSR and seed shall yield identical surface output. Stripping stylistic variation shall recover the original SSR meaning without loss.

---

## 7. Manifold → Expression Mapping Rules

Expression maps the relational manifold surface (as projected into the SSR) to linear linguistic form while respecting basin structure. This mapping follows basin-preserving linearization.

Path B shall respect object-basin and relational-basin distinctions present in the SSR when selecting grounding tiers and expression patterns. Path B does not perform manifold navigation — it only consumes the projection provided by Path A.

Manifold curvature or resonance signals encoded in SSR metadata shall influence emphasis and stylistic choices but shall not alter propositional content.

---

## 8. KnB Grounding Requirements

Path B consumes the tiered grounding produced by KnC, KnM, and KnF.

Path B shall select expression precision according to the lowest sufficient entropy tier ($H_{Kn}$) and total entropy relative to defined thresholds. Path B cannot lower entropy by inventing detail. KnF lexical grounding must respect KnM constraints when ambiguity remains high.

When total entropy exceeds coarse-expression thresholds, Path B shall favor clarification or surgical questioning patterns.

---

## 9. Safety, Governance, and Reversibility Constraints

Path B shall treat TPSF and TPTB fields as authoritative and immutable.

All expressed output shall remain fully reversible to the originating SSR by stripping stylistic variants.

Incomplete-meaning conditions detected at OuBB shall trigger audit events and IMR pathways (expression-side only) without mutating the SSR.

---

## 10. Runtime Contract for Expression Generation

Expression generation shall begin only after:
- The SSR is frozen by SSRGn.
- CoHI and LI have completed their writes.
- ReB has validated required invariants and SSR continuity fields are stable.

Primitives shall maintain strict ordering and read-only access to upstream artifacts.

---

## 11. Replay Contract (Expression → Meaning)

Replay fixtures shall support:
- Stripping stylistic variation from OuBB artifacts.
- Recovering the exact originating SSR meaning and metadata.
- Verifying equivalence to the committed state.

Replay shall verify that all surface-form variability collapses to a single canonical SSR-equivalent representation. Replay fixtures must be seed-aware.

---

## 12. Examples (Minimal, Precise)

**Example 1 — Clean Resolved Meaning**  
SSR contains a resolved proposition with no conflicts.  
Path B produces: "The measured value is 42." (or equivalent stylistic variant).  
Stripped form recovers the original proposition exactly.

**Example 2 — Truth Conflict**  
TPTB indicates a conflict.  
Path B produces: "The value appears to be 42, although this conflicts with prior data."  
No resolution of the conflict occurs in Path B.

**Example 3 — Safety Constraint**  
TPSF requires qualification or scoping.  
Path B produces a response that respects the allowed_scope without introducing disallowed content.

---

## 13. Appendix: Interaction with Path A and Manifold Shapes

Path A is responsible for meaning construction and commitment into the SSR. Path B consumes the frozen SSR without feedback mutation, preserving the strict A/B boundary.

Manifold shapes (basins, trajectories, relational geometry) are projected into SSR fields and guide Path B via KnB grounding tiers and stylistic selection (including register selection when appropriate). This maintains consistency with relational principles while producing linear linguistic output.

This white paper aligns with the broader TS architecture and existing 20-series documents.

---

*End of pb_expression_rules.md*
