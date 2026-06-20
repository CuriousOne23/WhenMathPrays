# OB Developemnt Playbook
**OB_development_playbook.md**  
**Revision:** 1.1 (Two-Phase Development Rules Added)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose of This Document

This playbook exists to **protect the integrity of the Thought Simulator (TS)** while allowing creative, iterative development of the OB pipeline and future components.

It provides lightweight guardrails so we can explore freely in the early stages without quietly breaking core invariants.

### 2. How to Use This Playbook

- Review the relevant sections before making significant changes.
- Use it as a shared reference during discussions and code reviews.
- Update it as we learn what works best.
- When in doubt, favor explicit documentation and testing.

### 3. Development Phases

We operate under a **Two-Phase** model to balance flexibility during discovery with stability later.

#### Phase 1 – Active Development / Exploration (Current Phase)
**Goal:** Maximum learning speed and design flexibility.

**Allowed:**
- Delete, rename, or replace fields and objects
- Make major structural changes
- Experiment with new approaches
- Fix mistakes quickly

**Recommended:**
- Record major design decisions or breaking changes when practical
- Minor fixes do not require formal documentation

**Transition Trigger to Phase 2:**
When the core OB objects and pipeline feel reasonably stable and we are mostly tuning rather than redesigning.

#### Phase 2 – Stabilization / Production
**Goal:** Protect reliability, provenance, and backward compatibility.

**Rules:**
- No free deletion or replacement of core fields/objects
- Major changes require proper versioning (`_v1` → `_v2`)
- Deprecation process must be followed
- Occasional breaking changes are allowed but treated as **major version releases**

**Breaking Changes in Phase 2:**
- Must be clearly documented
- Should include a migration path when possible
- Users/environments needing strict repeatability can pin to specific versions

### 4. Core Invariants Checklist (Must Verify Before Changes)

- [ ] Provenance & Traceability preserved
- [ ] Replay Equivalence maintained
- [ ] Monotonic Entropy Reduction
- [ ] Non-Negative Curvature
- [ ] Pre-Semantic Boundaries
- [ ] RB Routing Compatibility
- [ ] Layer Independence

### 5. Change Taxonomy

**Safe Changes** (Low Risk)
- Adding optional fields or new tags/hooks/rules
- Adding new OB layers via OB Map

**Dangerous Changes** (Requires Care)
- Modifying meaning of existing fields
- Changing routing-critical structures

**Forbidden in Phase 2**
- Weakening locked invariants
- Making provenance optional

### 6. Simulation & Validation Protocol

For any non-trivial change:
- Run the standard test corpus
- Compare key metrics (entropy, residue quality, routing behavior)
- Document differences

### 7. Guiding Mindset

- Stay in the sandbox — explore freely, but honestly.
- Value the process and each coherent step.
- Protect what makes TS special while allowing it to evolve.

---

**End of Revision 1.1 — OB_development_playbook.md**

---
