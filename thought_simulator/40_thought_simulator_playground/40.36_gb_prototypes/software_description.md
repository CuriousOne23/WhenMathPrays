# 40.36_gb_prototypes / software_description.md

## Approval State
**Phase A draft complete.** Pending explicit human approval before Phase B execution.

## Two-Phase Execution Model
- **Phase A:** Define and review `software_description.md` only.
- **Mandatory stop** after Phase A until explicit human approval.
- **Phase B (after approval):** Implement `prototype.py`, `harness.py`, verification artifacts, etc.

---

## Role in the Development Flow
This document defines the **desired behavior** for the Global Brain (GB) prototype in the 40-series. It is guided by the updated 20-series documents (especially 20.10, 20.16, 20.17, 20.18, and 20.80). Insights and challenges discovered during implementation will inform refinements to the 10-series.

---

## 1. Purpose

Define a deterministic Global Brain (GB) prototype that acts as a **non-mutating supervisory subsystem**.

The GB SHALL:
- Monitor global semantic stability and coherence
- Detect drift, oscillation, and instability
- Enforce cross-cycle and cross-basin coherence
- Govern IB lifecycle (creation, evolution, merge/split, promotion, retirement)
- Supervise OB decomposition
- Gate COP proposals
- Apply safe-boundary supervisory actions
- Maintain deterministic supervisory logging
- Operate within bounded TCU envelopes

**Core Principle (from 20.10 & 20.16):**  
The GB **MUST NOT** perform direct meaning construction or mutate TP/MTP semantic state. It operates only at explicit safe boundaries.

---

## 2. Scope

### In Scope
- Deterministic TS → GB → TS supervisory evaluation loop
- Implementation of responsibilities defined in **20.16 GB Responsibility Matrix**
- Handling of messy / contradictory input per **20.17**
- Failure detection and graceful degradation per **20.18**
- Deterministic supervisory action selection and application
- Bounded resource usage and overflow handling

### Out of Scope
- Direct mutation of TP/MTP meaning state
- Internal implementation details of basins, TP execution, or learned modules
- Full production-grade performance optimizations
- User interface or external integration

---

## 3. Key Requirements from 20-series

**HLR Alignment:**
- **20.10** – Architectural principles, supervisory separation, determinism
- **20.16** – GB Responsibility Matrix (core reference)
- **20.17** – Messy real-world input handling
- **20.18** – Failure modes and success criteria
- **20.80** – GB component requirements

The prototype SHALL demonstrate clear adherence to the **supervisory-only** role of the GB.

---

## 4. Success Criteria (Phase B)

- GB correctly identifies and logs supervisory concerns without mutating core state.
- All actions are deterministic and replayable.
- Clear evidence of safe-boundary enforcement.
- Graceful handling of edge cases (high volatility, contradictory input, overflow).

---