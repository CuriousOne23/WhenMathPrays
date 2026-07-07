# knb_candidate_selection.md

**Document ID:** 20.XXX_knb_candidate_selection  
**Version:** 0.1  
**Date:** 2026-07-07  
**Status:** Draft — Realization Paper (KnB)  
**Purpose:** Define candidate selection for the Knowing-by-Binding (KnB) primitive in Path A.

---

## 1. Overview

KnB (Knowing-by-Binding) is the primitive responsible for generating, filtering, validating, and selecting candidates for meaning construction and identity resolution. Candidate selection bridges CE, ISc, and the OB-family primitives while preserving determinism and replay equivalence.

Path A requires KnB candidate selection to enable bounded, deterministic candidate sets that support structural → meaning transitions and safe Path B handoff without introducing nondeterminism or semantic leakage.

---

## 2. Candidate Foundations

- **Candidate envelopes:** Structured, bounded collections of candidates.  
- **Candidate fields:** identity_candidate[], relation_candidate[], domain_anchor_candidate[], qualifier_candidate[], truth_validation_candidate[], KnDt_keywords[], KnDt_addresses[].  
- **Candidate geometry:** Finite sets with provenance.  
- **Candidate provenance:** Traceable origin from CE/ISc/structural cues.  
- **Candidate monotonicity and stability:** Once selected, candidates are stable for the cycle.

**Finite candidate set:**  

$$
C = \{c_1, c_2, \dots, c_n\}
$$  

(Gloss: finite candidate set.)

**Candidate generation:**  

$$
c_i = \Gamma(\text{CE}, \text{ISc}, \text{StructuralSignals})
$$  

(Gloss: each candidate is generated deterministically from CE, ISc, and structural cues.)

---

## 3. Candidate Generation Rules

Rules govern deterministic extraction from CE, expansion from ISc, binding from structural geometry, bounded candidate count, canonical ordering, and replay-deterministic generation.

- Candidate generation SHALL NOT infer new meaning.  
- Candidate generation SHALL NOT modify structural fields.  
- Candidate generation SHALL NOT depend on routing signals.

---

## 4. Candidate Normalization Rules

Rules govern normalization operators, canonical field ordering, grouping, envelope shape, and replay-deterministic normalization.

$$
c_i^{\text{norm}} = N(c_i)
$$  

(Gloss: normalized candidate.)

---

## 5. Candidate Filtering Rules

Rules govern allowlist/denylist, structural-compatibility, identity-compatibility, domain-compatibility, and truth-validation filters.

$$
C_{\text{filtered}} = \{c_i \in C \mid F(c_i) = \text{true}\}
$$  

(Gloss: filtered candidate set.)

- Filtering SHALL NOT introduce new candidates.  
- Filtering SHALL NOT modify candidate geometry.

---

## 6. Candidate Scoring Rules

Rules govern scoring distribution, entropy, confidence, rationale, and deterministic scoring function.

$$
S(c_i) = \text{Score}(c_i, \text{CE}, \text{ISc})
$$  

(Gloss: deterministic scoring.)

$$
\text{Distribution} = \frac{e^{S(c_i)}}{\sum_j e^{S(c_j)}}
$$  

(Gloss: normalized scoring distribution.)

- Scoring SHALL NOT generate meaning.  
- Scoring SHALL NOT modify structural geometry.

---

## 7. Candidate Selection Rules

Rules govern top-candidate selection, threshold selection, multi-candidate selection, deterministic tie-breaking, and replay-deterministic selection.

$$
c^\ast = \arg\max_{c_i \in C_{filtered}} S(c_i)
$$  

(Gloss: selected candidate.)

- Selection SHALL NOT modify candidate geometry.  
- Selection SHALL NOT generate new candidates.

---

## 8. Candidate Correction Rules (IMR Type B)

Rules govern correction boundaries, depth limits, cooldowns, invariants, and replay equivalence.

$$
C^{(n+1)} = \Psi_{\text{corr}}(C^{(n)}, \text{CorrectionContext})
$$  

(Gloss: bounded candidate correction.)

- Corrections SHALL NOT introduce new structural fields.  
- Corrections SHALL NOT alter structural geometry.  
- Corrections SHALL NOT generate meaning.

---

## 9. Candidate Serialization Rules

- Canonical ordering, naming, and grouping.  
- Canonical candidate envelope shape.  
- Replay-deterministic serialization.

$$
\text{Serialize}(C) = \text{CanonicalForm}(C)
$$  

(Gloss: candidate sets must serialize deterministically.)

---

## 10. Deterministic Candidate Guarantees

$$
\text{CandidateDeterministic} \iff f(x) = f(y) \;\text{whenever}\; x = y
$$  

(Gloss: identical inputs yield identical candidate sets.)

All candidate operators are deterministic, seed-free, and replay-equivalent.

---

## 11. Realization Notes

- **Implementation:** Implement generation, normalization, filtering, scoring, and selection as deterministic functions with bounded sets and guards.  
- **Validation:** Assert finiteness, provenance, separation, and normalization invariants.  
- **Testing:** Replay tests, clean/corrected candidate paths, edge cases.  
- **Serialization:** Enforce canonical form for candidate envelopes.  
- **Integration:** Candidates feed OB-family primitives, support ISc → TPU flow, and prepare for Path B eligibility.  
- **New primitives:** Declare candidate interactions and satisfy existing determinism/separation invariants.

---

## 12. Summary

KnB candidate selection provides a deterministic, bounded pipeline for generating, filtering, scoring, and selecting candidates from CE, ISc, and structural cues. It maintains strict separation from meaning and structural mutation while enabling identity resolution and Path B handoff. All operations are replay-equivalent and support clean correction boundaries.

**End of knb_candidate_selection.md**
