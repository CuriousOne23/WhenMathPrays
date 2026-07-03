# OB SMOB RB Handoff Guidelines
**ob_smob_rb_handoff_guidelines.md**  
**Revision:** 1.0 (Initial Draft)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose

Please see [OB_development_playbook.md](OB_development_playbook.md) for complete list of documents which pertain to the OB system playground papers.

This document defines the **critical handoff guidelines** between the structural OB pipeline (SOB → SROB → CnOB → SmOB) and the semantic stages (RB / TB / MTP).

Its goal is to protect the strict separation between **structure** and **meaning** while ensuring RB has everything it needs to perform reliable, content-addressable routing.

This is the primary seam where semantic leakage or structural drift is most likely to occur during implementation.

### 2. Semantic Readiness Contract (What SmOB Must Provide)

SmOB output (`SEMANTIC_SKELETON`) must contain exactly these elements for RB to function correctly:

- `structural_signature` – Canonical fingerprint of the refined structure
- `residue` – Unresolved structural material that still needs semantic attention
- `bindings` – Neutral attachment points between hooks and anchors
- `slots` – Open structural positions ready for potential semantic filling
- `referents` – Anchor points for future referent binding
- `hooks` – Neutral relation-ready attachment points
- Full `carry_forward` (constraints, uncertainty markers, gaps)

**SmOB Must Not Provide:**
- Any resolved meaning, stance, truth value, or interpretation
- Any suggestion about what should fill a slot or gap
- Any preference for one interpretation over another

### 3. Semantic Neutrality Test (Runtime Guardrail)

Before RB consumes any SmOB output, the following checks must pass:

- No hook or slot implies a semantic role, category, or intent
- No hook suggests what content belongs in a slot
- No boundary marker implies topic, scope, or segmentation
- No uncertainty marker has been silently resolved or minimized
- No gap marker proposes a repair or filler
- All provenance and structural_signature remain intact

If any check fails, the handoff must be rejected or flagged for review.

### 4. Residue Integrity Check (Protecting Structural Work)

RB must treat SmOB’s `residue` as **authoritative and immutable**:

- RB must not re-tokenize, re-segment, re-order, or re-group the residue
- RB must not reinterpret or “clean up” structural decisions made by the OB pipeline
- Any structural modification by RB is forbidden — only semantic attachment is allowed
- All `structural_signature`, `bindings`, and `entailment_edges` must be respected

This rule prevents RB from undoing OB’s structural work under the guise of “semantic reasoning.”

### 5. Key Invariants at the Handoff Seam (Locked)

- Strict pre-semantic boundary: SmOB produces scaffolding only — never meaning
- Monotonic flow: Structure may only be refined, never weakened or re-interpreted
- Traceability: Full provenance must survive the handoff
- RB responsibility: Semantic interpretation happens only in RB/TB, never retroactively in OB

### 6. Usage During Implementation

- All OB → RB handoff code must explicitly reference and enforce this document.
- Any violation must be logged as a high-severity architectural issue.
- During testing, run the Semantic Neutrality Test and Residue Integrity Check on every example.

---

**End of Draft – ob_smob_rb_handoff_guidelines.md (Rev 1.0)**

---
