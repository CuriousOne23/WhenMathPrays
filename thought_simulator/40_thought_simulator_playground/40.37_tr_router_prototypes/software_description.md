# 40.37_tr_router_prototypes / software_description.md

## Approval State
**Phase A draft complete.** Phase B implementation executed on 2026-06-03 (prototype + harness + verification artifacts). Awaiting explicit human / CP review before further promotion steps.

## Two-Phase Execution Model (Global 40.* Rule)
- **Phase A:** Define and review this `software_description.md` only.
- **Mandatory stop** after Phase A until explicit human approval is given.
- **Phase B (after approval):** Implement `prototype.py`, `harness.py`, verification artifacts, `requirements_delta.md`, etc.

---

## Role in the Development Flow
This document defines the **desired / explored behavior** for the Thought Router (TR) prototype in the 40-series. It is guided by the 20-series and 10-series documents listed below. Insights, challenges, and evidence generated here (including the executed minimal basin router) inform refinements to the 10-series and alignment with full TR semantics in 20.37.

This module was executed as a minimal deterministic router to validate core routing + ΔH% assignment principles before full TP.TR / tr_needs_update lifecycle integration.

---

## Phase A Deliverables
- High-level routing behavior description
- Mapping of 20/10-series intent to prototype responsibilities (simplified basin selection as proxy)
- Identification of unknowns, ambiguities, and missing definitions (e.g., full semantic fields vs. early routing proxy)
- Definition of what Phase B must / did explore
- No final algorithms or thresholds for production TR (those remain in 20.37 / 10.10.50)

---

## Phase B Deliverables (Executed)
- Minimal deterministic content-based router (keyword proxy for semantic cues)
- Consistent ΔH% assignment per route decision
- Explicit error route for invalid input, no side effects
- Harness with deterministic pass/fail + ΔH% validation
- JSON artifact for replay evidence
- Feedback for 10.50.37 canonical requirements and 30-layer promotion

---

## 1. Purpose

Define a deterministic Thought Router (TR) prototype that performs **initial basin selection** and **ΔH% tagging** as an exploratory validation of routing concepts.

The TR prototype **SHALL**:
- deterministically map input characteristics to a basin route (`math_basin`, `thought_basin`, `general_basin`)
- assign fixed, consistent ΔH% values based on the chosen route
- return explicit `{"route": "error", "reason": "invalid_input"}` for malformed/empty input with no side effects
- remain strictly deterministic: identical input always yields identical route + delta_h
- respect separation of concerns (routing decision only; no meaning construction, no TP/MTP mutation in this proxy)

**Core Principle (from 20.10, 20.30, 10.10):**  
Routing decisions in the TS core **MUST** be deterministic. The (full) TR routine is the *exclusive writer* of TP.TR and may only execute when RB detects `tr_needs_update = true`. GB supervises read-only and may never perform or bypass routing.

---

## 2. Guidance from Specified Sources

This prototype was developed under guidance from (and must be traceable to):

- **20.10_ts_architectural_principles.md** — Core determinism (HLR-20.010-001), meaning construction explicit/auditable, variability isolated to output layer, basin locality, GB as supervisor only (HLR-20.010-018..026), no unbounded work, all state transitions replayable. Risks around trace explosion and need for explicit boundaries (1.14).

- **20.16_gb_responsibility_matrix.md** — GB responsibility matrix: GB **must** do supervisory flow control, coherence/stability, arbitration, population control; **must not** perform meaning construction or mutate core state. Routing logic must remain in the deterministic core (pushed downward per HLR-20.016-015); GB reads TR/metadata for gating only (read-only per 10.50.36).

- **20.30_ts_functional_model.md** — Pipeline: RB routing → OB extraction (may set `tr_needs_update`) → TR gate (RB routes to TR *iff* `tr_needs_update = true`) → ... → merge (may set dirty) → GB review at safe boundary. Explicit HLRs: 20.030-311 (tr_needs_update boolean), 20.030-313 (RB routes iff true), 20.030-314 (TR clears *only* on success), 20.030-315 (TR SHALL NOT execute when false). RB determines OB firing and lane projections. All end-to-end stages deterministic.

- **20.38_ts_implementation_guidelines.md** — Prototypes SHOULD demonstrate modularity, clear deterministic-core vs. non-det separation, explicit typed contracts, strong typing, structured logging with reason codes, deterministic replay capability early, auditability/debuggability. Surface conflicts between guidance and implementation for 10-series resolution. Prioritize clarity over premature optimization.

- **10.10 (10.10.10_system_architecture.md + 10.10.50_module_contracts_and_visibility_rules.md)** — TR (Thought Router routine) in decomposition: "Computes and refreshes the TP semantic routing block (TP.TR) when TP.tr_needs_update = true." Execution model explicitly gates TR after semantic-write phase. TR contract: Does = compute/refresh TP.TR on RB route when dirty + produce auditable status/provenance; Does Not = execute when false, clear dirty on failure, bypass RB gating. Visibility limited to routing-relevant fields. TR forbidden from coprocessor offload (any semantic interpretation). Architectural invariants include the RB→TR iff dirty rule. Strict module contracts and no cross-module mutation.

- **10.50.36_gb_requirements.md (and 20.80)** — GB is non-mutating, asynchronous, deterministic supervisory subsystem. GB SHALL read only lane-local TP snapshots and MPs; SHALL NOT access internal basin state or mutate TP/MTP meaning-construction state (HLR-36-001..003). GB actions only at deterministic safe boundaries (HLR-36-010). GB supervises COP/IB/OB but TR routine (as core semantic writer) must remain inside TS arbitration rules; GB may read TR for supervisory gating without mutation (HLR-36-061). TCU envelope and deterministic fallback apply to all supervised work.

Additional primary anchor:
- `20.37_thought_router_tr_specification.md` — Full TP.TR field set, lifecycle, producer/consumer authority (TR routine exclusive writer), dirty-flag protocol, OB→TR input fields, RB consumption, safety/determinism constraints, and 41 HLR-20.037-* items. (This 40.37 prototype explores *only* a minimal routing+ΔH% proxy; full field population and dirty-flag integration are out of scope for this iteration.)

---

## 3. What Phase B Explored (and Must Explore in Future Iterations)

Phase B produced concrete evidence for:
- Deterministic routing decisions from input content (keyword proxy for semantic cues from OB input_fields)
- Monotonic / consistent ΔH% assignment as direct function of route (math=0.15, thought=0.08, general=0.05)
- Strict input validation and error-path handling without state mutation or nondeterminism
- 100% same-input → same-output behavior across repeated harness runs
- Separation of concerns: this router performs *routing selection only*

Future iterations of 40.37 (or sibling modules) **SHALL** explore:
- Full TP.TR block population (stance, intent, affect, epistemic_shading, tension, politeness, commitment, reservation, logical_structure, semantic_deltaH, lineage_additions, routing_semantics) per 20.37 §6
- Correct `tr_needs_update` dirty-flag lifecycle integrated with RB, OB, Merge, IB, Delta-H% writers
- MTP snapshot (read-only) consumption by TR routine
- Atomic write of TP.TR + clear of dirty flag only on success
- Read-only consumption by IB/Merge/Truth/Done/GB (per 20.37 and 10.10.50)
- Integration with safe-boundary GB supervisory signals
- Handling of split/merge lineage additions in TR

**Note:** Phase B prototypes explore feasibility and surface limitations; they do not define final system behavior.

---

## 4. What the 10-series Must Eventually Define

The prototype surfaced (and the 10-series **SHALL** codify):
- Final TR routine contract and exact field computation rules (full 20.37)
- Canonical dirty-flag protocol enforcement points (RB, semantic writers, TR success/failure paths) — see 10.10.50 and 20.30 HLR-20.030-311..315
- How TR semantics interact with GB read-only supervisory paths and COP proposals at safe boundaries (cross-ref 10.50.36, 20.16)
- Versioning / serialization rules for TP.TR block and deterministic ordering
- Compatibility with 20.95 numeric policy and 20.39 core data structures
- Full module visibility and IPC channel contracts for TR (10.10.20 + 10.10.50)
- Promotion path from this minimal router evidence into the normative 10.50.37 (already partially populated from this prototype) and eventual full TR design in 50.37

All Phase B findings **SHALL** be fed into the 50-series for design decisions and into the 10-series for specification refinement.

---

## 5. Non-Goals (This Iteration)

This 40.37 prototype and its software_description deliberately **do not** define or implement:
- The complete 12-field TP.TR semantic block or its derivation logic
- tr_needs_update flag management or RB gating inside the prototype (standalone for isolation)
- MTP snapshot reading or full pipeline integration
- GB/COP interaction or safe-boundary signaling (GB reads TR; this proto does not emit supervisory events)
- Any stochastic elements or wall-clock behavior
- Performance / TCU budgeting for full TR (minimal here)
- Full IB/OB/Merge/Truth consumer contracts

These are reserved for subsequent iterations or the 50.37 design layer once 20.37 + 10.10.50 anchors stabilize.

---

## 6. Risks & Unknowns to Investigate (Aligned with 20.10 §1.14)

- Scaling of simple routing rules to full semantic TR field derivation under messy/contradictory input (20.17)
- Correct interaction of TR dirty-flag with parallel traces, split/merge, and GB arbitration
- Whether early ΔH% assignment in router remains stable once full semantic_deltaH and lineage rules are added
- GB overload if TR-related supervisory events become too frequent (mitigation: push as much as possible to RB + basin-local rules per 20.16)
- Traceability of TR provenance through to commitments and human-oversight gates

---

## 7. Deterministic Invariants (Observed in Executed Prototype)

- Identical input → identical `{"route", "priority", "delta_h"}` (and error form)
- No randomness, no global mutable state, no wall-clock dependence
- Error paths produce no side effects on successful-path state
- ΔH% values are fixed per route class (monotonic, auditable)
- Harness results are fully replayable from the JSON artifact

---

## 8. IO Contract (Current Prototype)

Inbound (harness → router):
- `{"content": string}` (free text; lowercased + keyword scan for routing)

Outbound (router → caller):
- Success: `{"route": "math_basin"|"thought_basin"|"general_basin", "priority": "high"|"medium"|"low", "delta_h": float}`
- Error: `{"route": "error", "reason": "invalid_input"}`

Future full TR will expand this to structured TP.TR + tr_needs_update write under RB dispatch contract.

---

## 9. Promotion Readiness Conditions

Before promotion / release coupling:
- Executed harness with deterministic pass/fail (achieved: 4/4)
- Artifact evidence covering routing + ΔH% + error paths
- Explicit mapping in `requirements_delta.md` to 20.10 / 20.30 / 20.37 / 10.10 anchors
- Completed `verification_capsule.md` with three-flow statements
- This `software_description.md` human-approved
- Alignment check against 10.50.37 canonical (already seeded from this prototype)

---

## Flows Alignment Note
- **Forward Flow (20/10-series)**: Routing determinism, tr_needs_update protocol, RB gating, GB read-only supervision, and module contracts drawn directly from 20.10, 20.16, 20.30, 20.38, 10.10.10, 10.10.50, 10.50.36.
- **Backward Flow (40-series evidence)**: Executed prototype demonstrated minimal viable deterministic routing + ΔH% tagging; surfaced that full TP.TR semantics (20.37) require additional iteration beyond this basin-proxy.
- **Iterative Design Flow**: 10.50.37 was created/populated from this 40.37 evidence; further 50.37 design will drive additional 40.x exploration.

**Agreement Statement**: The three flows are in agreement for the *minimal routing proxy* scope. Full semantic TR integration remains an open forward-flow item to be addressed in subsequent cycles.

---

## Traceability

All Phase B evidence and this description **SHALL** be traceable to:
- 20.10 (architectural principles + GB separation)
- 20.16 (GB responsibility matrix)
- 20.30 (functional model + TR dirty-flag HLRs 20.030-311..315)
- 20.37 (TR specification)
- 20.38 (implementation guidelines)
- 10.10.10 (system architecture)
- 10.10.50 (module contracts for TR routine)
- 10.50.36 (GB requirements, read-only, safe boundaries)
- 10.50.37 (canonical TR requirements seeded by this prototype)
- 30.37 / 40.37 verification artifacts

---

## Scaffold / Execution Metadata (Retained for History)
- intended_20_anchor: thought_simulator/20_requirements/20.37_thought_router_tr_specification.md
- intended_10_10_anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md
- executed_as: minimal basin-selection router (proxy); full TP.TR deferred
- disposition_target: promote (achieved partial promotion to 10.50.37 + 30.37)
