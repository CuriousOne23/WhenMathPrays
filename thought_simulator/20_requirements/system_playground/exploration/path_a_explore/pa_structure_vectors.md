# pa_structure_vectors.md

**Document ID:** 20.XXX_pa_structure_vectors  
**Version:** 0.1  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (Path A)  
**Purpose:** Define the structure-vector system for Path A.

---

## 1. Overview

“Structure vectors” in the Thought Simulator are deterministic encodings of structural information extracted by the OB-family primitives. They represent, normalize, and evolve structural cues, graphs, and residue for downstream use in SSG, routing, and Path B preparation.

Path A requires structure-vector representations to enable deterministic routing, replay safety, and invariant propagation while maintaining strict separation from meaning and routing fields.

Structure vectors differ from raw structural fields (they are normalized encodings) and from meaning vectors (they contain no semantic content).

---

## 2. Structural Vector Foundations

- **Structural graph geometry:** Governed by SOB → SROB → CnOB → SmOB.  
- **Residue geometry and bounded compression:** Hashing occurs ONLY in SmOB.  
- **Structural cue families:** C1–C7.  
- **Structural segmentation and refinement.**  
- **Structural tags and envelopes.**

**Structural graph:**
  
$$
G = (V, E, \lambda)
$$  

(Gloss: structural graph with nodes, edges, and labels.)

**Structure vector:**  
  
$$
v_{\text{struct}} = h(G)
$$  

(Gloss: structure vector produced by deterministic graph-to-vector mapping.)

---

## 3. Structure Vector Construction Rules

Rules govern deterministic graph encoding, cue encoding, residue incorporation, bounded hashing (SmOB only), canonical ordering, and monotonic accumulation of structural signals.

- Structure vectors SHALL NOT include meaning fields.  
- Structure vectors SHALL NOT include routing fields.  
- Structure vectors SHALL NOT be modified by IdOB or RBU.

---

## 4. Structure Vector Normalization Rules

Rules govern normalization operators, canonical scaling, ordering, grouping, and replay-deterministic normalization.

$$
v_{\text{norm}} = \frac{v_{\text{struct}}}{\lVert v_{\text{struct}} \rVert_2}
$$  

(Gloss: normalized structure vector used for downstream routing.)

---

## 5. Structure Vector Interaction Rules

Rules govern how structure vectors feed SSG, constrain meaning, constrain routing, and interact with envelope geometry.

$$
\sigma = \varphi(v_{\text{norm}})
$$  

(Gloss: SSG signature derived from normalized structure vector.)

- Meaning rules SHALL NOT modify structure vectors.  
- Routing rules SHALL NOT modify structure vectors.  
- Envelope rules SHALL NOT introduce new structural vector components.

---

## 6. Structure Vector Correction Rules (IMR Type B)

Rules govern correction boundaries, depth limits, cooldowns, invariants, and replay equivalence.

$$
v_{\text{struct}}^{(n+1)} = \Psi_{\text{corr}}(v_{\text{struct}}^{(n)}, \text{CorrectionContext})
$$  

(Gloss: structural vector corrections are bounded and deterministic.)

Corrections SHALL NOT alter structural geometry outside allowed basins, introduce new structural fields, or modify structural vectors except within bounded SmOB correction scope.

---

## 7. Structure Vector Serialization Rules

- Canonical ordering, naming, and grouping.  
- Canonical vector envelope shape.  
- Replay-deterministic serialization.

$$
\text{Serialize}(v_{\text{struct}}) = \text{CanonicalForm}(v_{\text{struct}})
$$  

(Gloss: structure vectors must serialize deterministically.)

---

## 8. Deterministic Structure Vector Guarantees

$$
\text{StructDeterministic} \iff f(x) = f(y) \ \text{whenever}\ x = y
$$  

(Gloss: identical structural inputs yield identical structure vectors.)

All structure-vector operators are deterministic, seed-free, and replay-equivalent.

---

## 9. Realization Notes

- **Implementation:** Implement graph-to-vector mapping, normalization, and bounded compression as deterministic functions with guards.  
- **Validation:** Assert separation, monotonicity, normalization, and non-modification rules.  
- **Testing:** Replay tests, clean/corrected vector paths, boundary cases.  
- **Serialization:** Enforce canonical form for all structure vectors.  
- **Integration:** Structure vectors feed SSG → TR → RB → RTU and prepare clean TP for Path B.  
- **New primitives:** Declare vector contributions and satisfy existing invariants.

---

## 10. Summary

Path A structure vectors provide a deterministic, normalized encoding of structural information from the OB-family. They evolve monotonically with bounded compression only in SmOB, feed SSG for routing geometry, and maintain strict separation from meaning and routing fields. These vectors ensure replay safety, invariant propagation, and clean preparation for SSG, TR, RB, RTU, and Path B.

**End of pa_structure_vectors.md**
