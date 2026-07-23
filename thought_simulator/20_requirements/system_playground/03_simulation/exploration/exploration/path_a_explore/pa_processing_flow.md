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
InB → SOB → SROB → CnOB → SmOB → SSG → RBU → TR → CTP → ISc → RTU → RB → IdOB → RBU → TR → CTP → ISc → RTU → RB → IdOB → RBU → ... 
OR
→ TR → CTP → ISc → RTU → RB → OuBA
```

---

## 3. Corrected Path A Flow Diagram (Conceptual)

```
InB → IIInB → IE → ISc → CEx → CE → TPU → IMR → 
SOB → SROB → CnOB → SmOB → SSG → RBU → 
TR → CTP → ISc → RTU → RB → IdOB → RBU → 
TR → CTP → ISc → RTU → RB → IdOB → RBU → ...
OR
TR → CTP → ISc → RTU → RB → OuBA
```

---

## 4. Path A Primitive Inventory

| Primitive | Governing Reference Manuals | Description | TP Fields Read | TP Fields Written | Notes |
|-----------|-----------------------------|-------------|----------------|-------------------|-------|
| InB | pa_boundary_conditions.md | Raw external signal intake and canonicalization | None | Raw payload + provenance | Enforces input envelope |
| IIInB | pa_boundary_conditions.md | Surface normalization with deterministic repairs | Raw payload | Normalized surface form | Corrected Path A |
| IE | pa_boundary_conditions.md | Structured envelope with tokens and tags | Normalized form | Structured envelope | Corrected Path A |
| ISc | pa_boundary_conditions.md, pa_interpretation_constraints.md | Candidate set scoring and entropy calculation | Envelope / TP snapshot | tp_entropy_score | Dual role: front-end + routing loop |
| CEx | pa_boundary_conditions.md | Explicit context expansion | Envelope | Correction hypotheses | Corrected Path A |
| CE | pa_boundary_conditions.md | Context envelope selection | Hypotheses | Selected context | Corrected Path A |
| TPU | pa_boundary_conditions.md | Truth Primitive writer with authority matrix | Context | Committed TP | Corrected Path A |
| IMR | pa_text_correction.md, pa_boundary_conditions.md, pa_error_manifolds.md | Mismatch classification and bounded correction | TP snapshot | correction_context | Governs correction_context |
| SOB | pa_structure_vectors.md, pa_grammatical_structure.md | Structural segmentation and hint extraction | Committed TP | Structural hints | Pre-semantic |
| SROB | pa_structure_vectors.md, pa_grammatical_structure.md | Structure normalization and refinement | Structural hints | Refined structure | - |
| CnOB | pa_structure_vectors.md, pa_grammatical_structure.md | Monotonic structural constraints (C1–C7) | Refined structure | Constraints + conflicts | - |
| SmOB | pa_structure_vectors.md, pa_grammatical_structure.md | Residue compression (hashing only here) and cue extraction | Constraints | Residue-compressed structure | Sole hashing primitive |
| SSG | pa_ssg.md | Semantic structure geometry and normalized routing signatures | Refined structure | σ + semantic geometry | - |
| RBU | pa_meaning_rules.md | Registers identity, stance, tone into meaning fields | Identity profile + meaning fields | Refined meaning fields | Dual role: after SSG (init) + after IdOB (refine) |
| TR | pa_boundary_conditions.md | Relational routing preparation | Committed TP | Routing-prep fields | Precedes every CTP |
| CTP | pa_boundary_conditions.md | Immutable TP snapshot collection | Committed fields | TP snapshot | Requires preceding TR |
| RTU | pa_boundary_conditions.md, 20.30.005_rtu_prim.md | Routing update construction from TP snapshot and entropy | TP snapshot + tp_entropy_score + routing_metadata | routing_update | Pure routing-signal constructor; no arbitration |
| RB  | pa_boundary_conditions.md, 20.50_rb_requirements.md | Relational routing filter and lane decision from routing_update | routing_update + routing_metadata | routing_filter | Sole routing decision primitive (IdOB / OuBA); entropy-informed via upstream ISc |
| IdOB | pa_idob.md | Identity profiles, object binding, referential stability, meaning refinement | σ + meaning fields | Identity-conditioned meaning | Post-structural |
| OuBA | pa_boundary_conditions.md | Terminal output with path_b_eligible | Final TP snapshot | path_b_eligible + final envelope | End of Path A |

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
