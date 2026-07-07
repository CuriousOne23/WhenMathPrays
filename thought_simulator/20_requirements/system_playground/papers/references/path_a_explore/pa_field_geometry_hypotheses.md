# pa_field_geometry_hypotheses.md

**Document ID:** 20.XXX_pa_field_geometry_hypotheses  
**Version:** 0.2  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (Path A)  
**Purpose:** Define field-geometry hypotheses for Path A.

---

## 1. Overview

“Field geometry” in the Thought Simulator refers to the structural, relational, and evolutionary properties of fields within the Thought Packet (TP) and associated envelopes as they traverse Path A. These hypotheses formalize how structural fields, meaning fields, routing fields, and envelopes evolve, interact, and maintain invariants.

Path A requires these geometric hypotheses to guarantee deterministic meaning construction, replay equivalence, bounded behavior, and safe handoff to Path B. Structural fields precede and constrain meaning fields; routing fields operate on signatures derived from structural geometry; envelopes provide the canonical container.

The separation between structural/pre-semantic processing (early OB layers + SSG) and identity-conditioned meaning (IdOB + RBU) is geometrically enforced via manifold charts and projection operators. **IdOB and RBU SHALL NOT modify structural geometry or structural fields.**

---

## 2. Field Geometry Foundations

- **Structural field geometry:** Governed by SOB → SROB → CnOB → SmOB. Describes segmentation, constraints (C1–C7), residue, and graph structure.  
- **Meaning field geometry:** Governed by IdOB → RBU. Refines meaning within identity-selected manifold charts. **Meaning geometry SHALL NOT modify structural fields.**  
- **Routing field geometry:** Governed by SSG → TR → RB → RTU. Uses signatures and relational topology.  
- **Envelope geometry:** Governed by InB → ... → CTP → OuBA. Maintains canonical shape and serialization.

**Key operators:**  

$$
F_{\text{struct}}^{(n+1)} = \Pi_{\text{struct}}(F_{\text{struct}}^{(n)}, \text{Signals})
$$  

(Gloss: structural field evolution via deterministic projection operator.)

$$
F_{\text{meaning}}^{(n+1)} = \Phi_{\text{id}}(F_{\text{meaning}}^{(n)}, \text{IdentityProfile})
$$  

(Gloss: meaning field evolution conditioned on identity manifold.)

---

## 3. Structural Field Geometry Hypotheses

Hypotheses govern segmentation, constraint families (C1–C7), missing-slot and conflict geometry, residue accumulation, and the structural graph feeding SSG. Residue is monotonically accumulated; SmOB MAY apply bounded compression (hashing) — hashing occurs ONLY here in Path A.

Structural graph $G = (V, E, \lambda)$ is the canonical input to SSG. Structural geometry SHALL NOT be modified by IdOB or RBU.

---

## 4. Meaning Field Geometry Hypotheses

Hypotheses govern identity-conditioned refinement, meaning-field stability, constraints, and `path_b_eligible` signaling. Meaning geometry operates within the manifold chart selected by prior routing. **Meaning geometry SHALL NOT modify structural fields.**

---

## 5. Routing Field Geometry Hypotheses

- SSG produces normalized structural signature.
  
$$
\sigma = \frac{\varphi(G)}{\lVert \varphi(G) \rVert_2}
$$  

(Gloss: normalized structural signature vector used for routing geometry.)  

- TR and RB operate on relational topology derived from $\sigma$, `TP.TR`, and routing metadata.  
- RTU constructs lane activation/suppression geometry.

---

## 6. Envelope Geometry Hypotheses

Envelopes maintain canonical shape across primitives.  

$$
E_{n+1} = f_{\text{env}}(E_n, F_{\text{struct}}, F_{\text{meaning}}, F_{\text{routing}})
$$  

(Gloss: envelope evolution as a deterministic function of all field geometries.)

Correction-context envelopes (IMR Type B) are bounded and carry explicit `target_field_ids[]`.

---

## 7. Clean vs. Corrected Geometry Hypotheses

**Clean geometry:** Uninterrupted forward flow; invariants hold without mutation.  

**Corrected geometry:** IMR Type B introduces bounded re-interpretation geometry with `correction_context`. Type A remains realization-only.  

**Preservation rules:** Core structural geometry invariants preserved; mutations limited to allowed basins and fields. Replay equivalence holds when correction artifacts are stripped. Correction geometry is strictly bounded.

---

## 8. Deterministic Geometry Guarantees

$$
\text{GeometryDeterministic} \iff f(x) = f(y) \ \text{whenever}\ x = y
$$  

(Gloss: identical inputs yield identical geometric outputs.)

All field projections, normalizations, and transitions are deterministic, seed-free, and replay-equivalent.

---

## 9. Realization Notes

- **Implementation:** Encode geometric operators as deterministic functions; validate invariants at each handoff. Use canonical serialization for fields and envelopes.  
- **Validation:** Assert field shapes, monotonicity, projection properties, and the structural/meaning separation per primitive.  
- **Testing:** Replay tests, clean/corrected path geometry diffs, boundary cases.  
- **Serialization:** All geometric fields must use canonical ordering.  
- **Path B integration:** Final envelope and `path_b_eligible` must satisfy terminal geometric invariants.  
- **New primitives:** Declare field geometry contributions and satisfy existing projection/normalization invariants.

---

## 10. Summary

Path A field-geometry hypotheses provide a rigorous foundation for deterministic evolution of structural, meaning, and routing fields. Structural geometry precedes and constrains meaning geometry (with explicit non-modification rules for IdOB/RBU); routing operates on derived signatures. SmOB residue compression (hashing) is the sole hashing operation. These hypotheses ensure replay safety, invariant propagation, bounded corrections, and clean handoff to Path B.

**End of pa_field_geometry_hypotheses.md**
