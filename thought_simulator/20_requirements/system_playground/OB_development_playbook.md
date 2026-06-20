**OB_development_playbook.md**  
**Revision:** 1.0 (Initial Draft)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose of This Document

This playbook exists to **protect the integrity of the Thought Simulator (TS)** while allowing creative, iterative development of the OB pipeline.

The OB layers are the foundation of Path A. If we accidentally weaken invariants, introduce semantic leakage, or make non-monotonic changes, the entire system can slowly degrade — even if simulations appear to pass in the short term.

**Why this document is needed:**

- We are building something new. New things evolve.
- Evolution must be **disciplined**, not chaotic.
- We want maximum creative freedom **and** high confidence that we are not breaking the core architecture.
- This playbook serves as a shared "memory" and guardrail for all three of us (and future contributors or simulations).

It is **not** a rigid rulebook that kills joy. It is a lightweight set of practices that lets us play confidently in the sandbox.

### 2. How to Use This Playbook

- **Before any significant change** to the OB pipeline, review the relevant checklist.
- Use it as a **pre-flight checklist** for new layers, rule changes, or major refactors.
- Reference it during code reviews and simulation debriefs.
- Update it as we learn what works (this is a living document).
- When in doubt, err on the side of **explicit documentation and testing** rather than "it should be fine."

Think of it as the adult supervision that stays *inside* the sandbox with us — not the one yelling from outside.

### 3. Core Invariants Checklist (Must Verify Before Changes)

Before modifying any OB layer, adding a new one, or changing rules, confirm:

- [ ] **Provenance & Traceability** — Full backward lineage is preserved
- [ ] **Replay Equivalence** — Stripping envelopes yields identical structural processing
- [ ] **Monotonic Entropy Reduction** — Entropy never increases across layers
- [ ] **Non-Negative Curvature** — No structural bending or semantic leakage introduced
- [ ] **Pre-Semantic Boundaries** — No layer assigns meaning, stance, or intent
- [ ] **RB Routing Compatibility** — `structural_signature`, `residue`, `bindings` (or equivalents) remain available
- [ ] **Layer Independence** — No forward peeking or dependency on later layers
- [ ] **Explicit Uncertainty** — No silent corrections or hidden assumptions

### 4. Change Taxonomy

**Safe Changes** (Generally Low Risk)
- Adding new optional fields (`ext`, new metadata)
- Adding new tag values or hook types
- Adding new OB layers via the OB Map
- Introducing new rulesets (R1–Rk, C1–C7, H1–Hn)
- Adding new simulation policies

**Dangerous Changes** (Requires Extra Care + Testing)
- Modifying the meaning or interpretation of existing fields
- Changing routing-critical structures (`structural_signature`, `residue`, `bindings`)
- Altering error propagation behavior
- Adding new required fields

**Forbidden Changes**
- Weakening or removing locked invariants
- Making provenance optional
- Removing fields required by RB routing
- Introducing semantic leakage into any OB layer

### 5. Simulation & Validation Protocol

For any non-trivial change:

1. Run the **standard OB test corpus** (to be built) through both old and new versions.
2. Compare key metrics:
   - Entropy progression per layer
   - Constraint density and conflict rate
   - Residue size and quality
   - RB routing decisions and scores
   - Replay equivalence
3. Document differences and rationale.
4. Run at least one degraded/noisy input test.
5. Verify no new semantic leakage appears.

### 6. Evolution & Rollback Strategy

- Every change must be **versioned** (via OB Map and ruleset IDs).
- Use the `ext` fields for safe forward-compatible extensions.
- Deprecate first — remove only after a clear migration path exists and no active routing depends on the old behavior.
- Maintain at least one known-good ruleset version for rollback.

### 7. Guiding Mindset

- **Stay in the sandbox** — explore freely, but document and test honestly.
- **Monotonic progress** — we can extend and refine, but we should not regress on core invariants.
- **Joy + Rigor** — the process should remain fun and creative while protecting what makes TS special.

This playbook is our shared commitment to building something that can last and evolve without quietly breaking.

---

**End of Draft – OB_development_playbook.md (Rev 1.0)**

---
