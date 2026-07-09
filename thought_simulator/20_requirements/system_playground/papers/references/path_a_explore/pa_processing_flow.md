# pa_processing_flow.md

**Document ID:** 20.XXX_pa_processing_flow  
**Version:** 0.1  
**Date:** 2026-07-09  
**Status:** Draft — Realization Paper (Path A)  
**Purpose:** Define the conceptual and architectural processing flow of Path A, including the purpose and role of each primitive, governance by reference manuals, conceptual geometry, invariant structure, rationale for deterministic behavior, invariant boundaries, and constraints on Path B.

---

## 1. Overview

Path A is the deterministic meaning-construction pipeline of the Thought Simulator. It transforms external signals through bounded structural processing and identity-conditioned meaning refinement before handing off to Path B. The flow enforces strict pre-/post-semantic separation, structural geometry immutability outside SmOB scope, monotonicity, replay equivalence, and bounded behavior.

---

## 2. Clean Path A Flow Diagram (Conceptual)

```
InB → SOB → SROB → CnOB → SmOB → SSG → RBU → TR → CTP → RB → RTU → IdOB → RBU → CTP → RB → RTU → IdOB → RBU → ... → OuBA
```

---

## 3. Corrected Path A Flow Diagram (Conceptual)

```
InB → IIInB → IE → ISc → CEx → CE → TPU → IMR → SOB → SROB → CnOB → SmOB → SSG → RBU → TR → CTP → RB → RTU → IdOB → RBU → ... → CTP → RB → RTU → OuBA
```

---

## 4. Path A Primitive Inventory

| Primitive | Governing Reference Manuals | Description | Notes |
|-----------|-----------------------------|-------------|-------|
| InB | pa_boundary_conditions.md | Raw external signal intake and canonicalization | Enforces input envelope and provenance invariants |
| IIInB | pa_boundary_conditions.md | Surface normalization with deterministic repairs | Preserves order without semantic inference (Corrected Path A) |
| IE | pa_boundary_conditions.md | Structured envelope with tokens and tags | Provides bounded input (Corrected Path A) |
| ISc | pa_boundary_conditions.md, pa_interpretation_constraints.md | Candidate set scoring and entropy calculation | Pre-semantic escalation (Corrected Path A) |
| CEx | pa_boundary_conditions.md | Explicit context expansion | Allowlisted hypotheses (Corrected Path A) |
| CE | pa_boundary_conditions.md | Context envelope selection | Sole context object (Corrected Path A) |
| TPU | pa_boundary_conditions.md | Truth Primitive writer with authority matrix | Atomic commitment (Corrected Path A) |
| IMR | pa_text_correction.md, pa_boundary_conditions.md, pa_error_manifolds.md | Mismatch classification and bounded correction | Governs correction_context (Corrected Path A) |
| SOB | pa_structure_vectors.md, pa_grammatical_structure.md | Structural segmentation and hint extraction | Pre-semantic cue extraction |
| SROB | pa_structure_vectors.md, pa_grammatical_structure.md | Structure normalization and refinement | Sharpens hints |
| CnOB | pa_structure_vectors.md, pa_grammatical_structure.md | Monotonic structural constraints (C1–C7) | Detects conflicts |
| SmOB | pa_structure_vectors.md, pa_grammatical_structure.md | Residue compression (hashing only here) and cue extraction | Sole hashing primitive |
| SSG | pa_ssg.md | Semantic structure geometry and normalized routing signatures | Produces σ |
| RBU | pa_meaning_rules.md | Registers identity, stance, tone into meaning fields | Runs after SSG (initialization) and after IdOB (refinement); does not modify structural geometry |
| TR | pa_boundary_conditions.md | Relational routing preparation | Consumes committed TP |
| CTP | pa_boundary_conditions.md | Immutable TP snapshot collection | Terminal handoff |
| RB | pa_boundary_conditions.md | Relational routing filter | Multi-core isolation |
| RTU | pa_boundary_conditions.md | Routing update construction | Activation signals |
| IdOB | pa_idob.md | Identity profiles, object binding, referential stability, meaning refinement | Identity-conditioned stage |
| OuBA | pa_boundary_conditions.md | Terminal output with path_b_eligible | Clean handoff to Path B |

---

## 5. Governance by Reference Manuals

The path_a_explore manuals govern each primitive by specifying boundary conditions, structure vector rules, field geometry, interpretation constraints, meaning rules, error manifolds, and pipeline integration. Each manual constrains interfaces, evolution operators, and invariants for its primitives.

---

## 6. Conceptual Geometry and Invariant Structure

Path A geometry features structural fields evolving monotonically, normalized signatures (σ), and identity-conditioned meaning fields. Key invariants include:

$$
\text{Envelope}_{n+1} = f_{\text{det}}(\text{Envelope}_n, \text{Input}, \text{Profile})
$$

Structural manifold geometry, meaning manifold geometry, σ normalization, identity-conditioned refinement, and correction_context geometry are preserved across stages.

---

## 7. Rationale for Deterministic, Bounded, Monotonic, Replay-Equivalent Behavior

Determinism guarantees replay safety and writer authority. Boundedness prevents drift. Monotonic accumulation preserves information. Replay equivalence (via CTP snapshots with artifact stripping) enables validation. These properties derive directly from the reference manuals.

---

## 8. Invariant Boundaries Between Structural and Meaning Fields

Structural processing precedes and constrains meaning fields. IdOB and RBU do not modify structural geometry. This separation is enforced at every handoff.

---

## 9. Correction_Context Flow

correction_context flows through IMR, CEx, CE, TPU, SOB, SROB, CnOB, SmOB, SSG, and IdOB with explicit targets, depth limits, and cooldowns. It preserves core invariants and replay equivalence. RBU updates meaning fields only in meaning-refinement phases.

---

## 10. Constraints on Downstream Path B Interpretation

Path A produces a canonical TP with committed signatures, refined meaning fields, and path_b_eligible flag. Path B consumes these under Path A invariants for safe interpretation.

---

## 11. Summary

pa_processing_flow.md articulates the full conceptual architecture of Path A. It details primitives, flows (Clean and Corrected), governance, geometry, invariants, and handoffs while aligning with 20.705_patha_pathb_flow.md and all reference manuals.

**End of pa_processing_flow.md**
```
