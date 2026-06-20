# OB Developemnt Playbook
**OB_development_playbook.md**  
**Revision:** 1.2 (Added list of all OB development documents)  
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

---

## **3. OB Document Index (Authoritative List)**  
This section provides a complete, centralized index of all OB‑related documents.  
It serves as the canonical reference for contributors, implementers, and reviewers.

**Core Architecture & Pipeline**  
- [OB_pipeline_spec.md](OB_pipeline_spec.md) 
- [OB_data_structures.md](OB_data_structures.md)  
- `OB_development_playbook.md` (this document)  

**Layer Specifications**  
- [sob_tag_set.md](sob_tag_set.md)  
- [srob_rewrite_rules.md](srob_rewrite_rules.md)  
- [cnob_constraint_families.md](cnob_constraint_families.md  )  
- [smob_mapping_hooks.md](smob_mapping_hooks.md)  

**Seam & Integration**  
- [ob_smob_rb_handoff_guidelines.md](ob_smob_rb_handoff_guidelines.md)  

**Validation & Examples**  
- [ob_pipeline_examples.md](ob_pipeline_examples.md)  
- [ob_validation_test_corpus.md](ob_validation_test_corpus.md)  

**Notes:**  
- This list is authoritative; all new OB documents must be added here.  
- Deprecated documents should be marked clearly and versioned appropriately.  
- This index ensures discoverability and prevents architectural drift.

---

### 4. Development Phases

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

### 5. Core Invariants Checklist (Must Verify Before Changes)

- [ ] Provenance & Traceability preserved
- [ ] Replay Equivalence maintained
- [ ] Monotonic Entropy Reduction
- [ ] Non-Negative Curvature
- [ ] Pre-Semantic Boundaries
- [ ] RB Routing Compatibility
- [ ] Layer Independence

### 6. Change Taxonomy

**Safe Changes** (Low Risk)
- Adding optional fields or new tags/hooks/rules
- Adding new OB layers via OB Map

**Dangerous Changes** (Requires Care)
- Modifying meaning of existing fields
- Changing routing-critical structures

**Forbidden in Phase 2**
- Weakening locked invariants
- Making provenance optional

### 7. Simulation & Validation Protocol

For any non-trivial change:
- Run the standard test corpus
- Compare key metrics (entropy, residue quality, routing behavior)
- Document differences

### 8. Guiding Mindset

- Stay in the sandbox — explore freely, but honestly.
- Value the process and each coherent step.
- Protect what makes TS special while allowing it to evolve.

---

**End of Revision 1.2 — OB_development_playbook.md**

---
