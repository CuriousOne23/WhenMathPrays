# pa_boundary_conditions.md

**Document ID:** 20.XXX_pa_boundary_conditions  
**Version:** 0.2  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (Path A)  
**Purpose:** Define all boundary conditions for deterministic realization of Path A.

---

## 1. Overview

Path A is the deterministic meaning-construction pipeline of the Thought Simulator. It transforms external signals through bounded pre-semantic normalization, structural refinement, identity-conditioned interpretation, and routing preparation for truth evaluation and Path B handoff.

**Boundary conditions** are the required input states, postcondition invariants, transition guards, residue propagation rules, and error envelopes at every primitive interface. These conditions ensure replay determinism, writer-authority isolation, pre-/post-semantic separation, and safe Path B integration. They are directly realizable as validation assertions, guards, and test fixtures.

Path A maintains strict separation: upstream/midstream stages are pre-semantic/structural; downstream OB-family stages add identity-conditioned meaning only after structural processing.

---

## 2. Upstream Boundary Conditions (InB → IIInB → IE)

**InB:**  
- Required input: Raw external signal (transport metadata + payload).  
- Required envelope: Bounded size, schema-valid surface form.  
- Normalization: Deterministic canonicalization, encoding, lexical rules.  
- Forbidden: Semantic inference or reordering.  
- Postconditions: Canonical form + provenance (HLR-20.100 series).  
- Error boundaries: Fixed reject/degrade with audit codes.  
- Serialization: Deterministic, replayable.

**IIInB:**  
- Preconditions: Valid InB output.  
- Postconditions: Surface-normalized form with deterministic repairs (shorthand, punctuation).  
- SHALL: Preserve meaning and order.  
- MUST NOT: Context-dependent or semantic repair.  
- Repair metadata attached.

**IE:**  
- Preconditions: IIInB output.  
- Postconditions: Structured envelope with tokens, repairs, structural tags (no semantics).  
- Invariants: Bounded, deterministic, replayable (HLR-20.109 series).

---

## 3. Midstream Boundary Conditions (CEx → CE → ISc → TPU → IMR → RB)

**CEx/CE:** Extract explicit bounded fields from CIL only. No inference. CE is the sole context object for ISc. Deterministic, allowlisted output.

**ISc:** Finite candidate set from CE. Produces normalized distribution, entropy/confidence, rationale. Escalates to COP per policy. No meaning generation.

**TPU:** Sole TP writer. Enforces authority matrix, canonical ordering, atomicity, 1-cycle lag. Validates Merge requests.

**IMR:** Classifies mismatches (Type A/B/C). Emits bounded CorrectionTriggers with caps, cooldowns, depth limits. Preserves replay equivalence on trace strip.

**RB:** Relational routing. Consumes committed `TP.TR`. Produces routing filter. Enforces bounds, multi-core isolation, deterministic transitions.

---

## 4. Downstream Boundary Conditions (OB-family primitives)

**SOB:** Structural segmentation + hint extraction (modality/domain/tone/constraint). Produces residue for SROB. No semantics.

**SROB:** Normalizes/refines structure. Sharpens hints. Prepares for CnOB.

**CnOB:** Monotonic structural constraints (C1–C7), missing-slot signals, conflicts. Purely structural.

**SmOB:** Two distinct jobs: (1) pre-semantic cue extraction into TP; (2) bounded residue compression (including possible hashing per 20.40.040) for SSG/TR-input. Path A uses hashing only here; no other primitive performs hashing.

**IdOB:** Identity-conditioned meaning refinement in selected manifold chart. Updates meaning fields and `path_b_eligible`.

**SSG:** Maps SmOB graph to normalized signature vector. Computes bitmap and reason code.  
$$
\sigma = \frac{\varphi(G)}{\lVert \varphi(G) \rVert_2}
$$  
(Gloss: L2-normalized structural-invariant vector for proximity routing.)

**RBU:** Commits local identity, TPTB, TPSF, stance/register/tone into TP (meaning side only).

**CTP:** Collects OB outputs into immutable TP snapshot for next RB. No semantic merge.

**RTU:** Constructs routing_update (activation/suppression, reasons, confidence). Pure routing signals.

---

## 5. Terminal Boundary Conditions (OuBA)

- Terminal invariants: All required TP fields committed; `path_b_eligible` set; final `TP.TR` and `tp.ssg_signature` stable.  
- Final envelope: Canonical TP ready for Path B.  
- Post-termination: Immutability until new input/correction.  
- Provenance/audit: Complete trail required.

---

## 6. Clean vs. Corrected Path A Boundary Differences

**Clean:** Normal forward pass, no IMR CorrectionTrigger. Primary flow invariants.  

**Corrected:** IMR-triggered (Type B semantic mismatch primarily). Bounded re-interpretation with `correction_context`/`target_field_ids[]`. Type A is realization-only.  

**IMR differences:** Type A (expression) vs. Type B (semantic) vs. Type C (safety). Caps, cooldowns, depth limits apply.  

**Preserved:** Replay equivalence (trace stripped), writer authority, determinism, pre-/post-semantic separation.  

**May differ:** Scope of revisited basins (restricted in corrections); additional audit fields.

---

## 7. Determinism Guarantees

**Envelope evolution:**
$$
\text{Envelope}_{n+1} = f_{\text{det}}(\text{Envelope}_n, \text{Input}, \text{Profile})
$$
(Gloss: deterministic envelope evolution based on bounded functions.)

**Scoring evolution:**
$$
\text{Distribution}_{n+1} = \text{Score}(\text{Candidates from CE})
$$
(Gloss: deterministic scoring over finite candidate set.)

**Residue evolution:**
$$
\text{Residue}_{n+1} = \text{Residue}_n \cup \text{NewStructuralSignals}
$$
(Gloss: monotonic accumulation; SmOB MAY apply bounded residue compression (hash) per 20.40.040, but no other primitive performs hashing.)

**Transition condition:**
$$
\text{TransitionAllowed} \iff \text{PreconditionsHold} \land \text{PostconditionsSatisfiable} \land \text{Guard}(TP.TR, \text{routing\_filter})
$$
(Gloss: transitions occur only when all guards and invariants are satisfied.)

---

## 8. Realization Notes

- **Implementation:** Use runtime assertions/guards per primitive. Canonical serialization for handoffs. Declare envelope shapes explicitly.  
- **Validation:** Per-boundary unit tests (valid/edge/malformed).  
- **Testing:** Replay fixtures, clean/corrected paths, multi-core, overflow modes.  
- **Replay determinism:** Strip correction artifacts for baseline equivalence.  
- **Path B integration:** OuBA ensures clean `path_b_eligible` and TP snapshot. Path B consumes committed semantic fields only.  
- **New primitives:** Must declare input/output envelopes and satisfy existing invariants at boundaries.

---

## 9. Summary

Path A boundary conditions enforce a strictly deterministic, auditable meaning-construction pipeline with clear pre-/post-semantic separation. Structural processing precedes identity-conditioned meaning. All interfaces are guarded for replay safety, writer authority, and bounded behavior. SmOB residue compression (hashing) is the sole exception to the general no-hashing rule. These conditions enable safe, predictable integration with Path B while supporting both clean and corrected flows.

**End of pa_boundary_conditions.md**
