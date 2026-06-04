# 40.36_gb_prototypes / software_description.md

## Approval State
**Phase A draft complete.** Pending explicit human approval before proceeding to Phase B.

## Two-Phase Execution Model
- **Phase A:** Define and review this `software_description.md` only.
- **Mandatory stop** after Phase A until explicit human approval is given.
- **Phase B (after approval):** Implement `prototype.py`, `harness.py`, verification artifacts, etc.

---

## Role in the Development Flow
This document defines the **desired behavior** for the Governing Basin (GB) prototype in the 40-series. It is guided by the updated 20-series documents (especially 20.10, 20.16, 20.17, 20.18, and 20.80). Insights, challenges, and evidence generated here will inform refinements to the 10-series.

---

## Phase A Deliverables
- High-level supervisory behavior description
- Mapping of 20-series intent to prototype responsibilities
- Identification of unknowns, ambiguities, and missing definitions
- Definition of what Phase B must explore
- No algorithms, no data structures, no thresholds

---

## Phase B Deliverables
- Deterministic supervisory loop prototype
- Logging + reason-code scaffolding
- Harness for testing messy input, contradictions, and ΔH% volatility
- Evidence for 50-series design decisions
- Feedback for 10-series refinement

---

## 1. Purpose

Define a deterministic Governing Basin (GB) prototype that acts as a **non-mutating supervisory subsystem**.

The GB **SHALL**:
- Monitor global semantic stability and coherence
- Detect drift, oscillation, and instability
- Enforce cross-cycle and cross-basin coherence
- Govern IB lifecycle (creation, evolution, merge/split, promotion, retirement)
- Supervise OB decomposition
- Apply safe-boundary supervisory actions
- Maintain deterministic supervisory logging
- Operate within bounded TCU envelopes

**Core Principle (from 20.10 & 20.16):**  
The GB **MUST NOT** perform direct meaning construction or mutate TP/MTP semantic state. It operates only at explicit safe boundaries.

---

## 2. Guidance from 20-series

The 20-series provides development guidance, not final rules. This prototype **SHALL** explore, validate, and stress-test the mechanisms implied by:

- **20.10** – Architectural principles and supervisory separation
- **20.16** – GB Responsibility Matrix
- **20.17** – Messy real-world input handling
- **20.18** – Failure modes and success criteria
- **20.80** – GB component requirements

---

## 3. What Phase B Must Explore

Phase B **SHALL** explore and produce concrete evidence for:

- ΔH% drift and oscillation detection
- IB population stability under contradictory and messy input
- Supervisory load under parallel traces
- Safe-boundary enforcement correctness
- Overflow and bounded-resource behavior
- GB intervention frequency and thresholds
- Failure mode detection and graceful degradation (per 20.18)
- Deterministic fallback behavior
- Supervisory logging completeness and auditability

**Note:** Phase B prototypes **SHALL** explore feasibility and surface limitations; they do not define final system behavior.

---

## 4. What the 10-series Must Eventually Define

The prototype **SHALL** surface ambiguities and missing definitions. The 10-series **SHALL** eventually codify:

- Final GB supervisory boundaries
- Deterministic thresholds for ΔH% drift, oscillation, and stability
- Final IB lifecycle rules (creation, merge/split, retirement)
- Final supervisory reason-code taxonomy
- Final safe-boundary definitions
- Final overflow/degradation rules

All Phase B findings **SHALL** be fed into the 50-series for design decisions and into the 10-series for specification refinement.

---

## 5. Non-Goals (Phase A)

Phase A **SHALL NOT** define:

- Algorithms
- Data structures
- Thresholds or formulas (including ΔH%)
- Commitment decay rules
- Basin-transition logic
- GB internal state layout

---

## 6. Risks & Unknowns to Investigate

Phase B **SHALL** investigate the following risks (aligned with 20.10 Section 1.14):

- GB overload risk
- Supervisory bottlenecks
- ΔH% instability under messy input
- Trace explosion and IB population overflow
- Contradiction preservation correctness
- Emotional-content routing correctness
- Deterministic fallback behavior effectiveness

---

## Traceability
All Phase B evidence **SHALL** be traceable to the relevant 20-series guidance items.

---