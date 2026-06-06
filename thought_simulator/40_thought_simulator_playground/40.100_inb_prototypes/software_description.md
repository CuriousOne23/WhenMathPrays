# 40.100_inb_prototypes / software_description.md

## Approval State
- Phase A (software_description): scaffold with exploratory HLR visibility (per alignment)
- Phase B (prototype + harness + evidence): planned

## Phase B Deliverables (Planned)
- Once implemented, the harness will execute scenarios covering the full set of 20.100 HLRs for exploratory evidence generation.
- Expected coverage: all 26 HLR-20.100-001 through 026 (ingest, no inference, determinism/replayability, schema validation, canonicalization, FIFO, bounded limits, provenance/audit, isolation, handoff contracts, platform independence, testability).
- Additional invariants to demonstrate: non-semantic canonicalization only, tick-cycle boundary compliance (first stage, no MTP mutation, no downstream state reads), deterministic intake evidence emission.
- Note: The full HLR list from 20.100_inb_requirements.md is included in this document for exploratory clarity and to make the complete requirement space visible during playground exploration. 20.xx remains the sole source of truth; 30.xx remains the authoritative coverage audit layer. 40.100 is a playground and not authoritative.

## Scaffold Metadata
- scaffold_status: planned
- intended_20_anchor: thought_simulator/20_requirements/20.100_inb_requirements.md (primary)
- intended_10_10_anchors:
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md (InB role, input normalization stage, MTP/TP state model, module-local buffers, deterministic cycles)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.20_interprocess_communication_and_channels.md (immutable messages, structured snapshots, no shared mutable memory, bounded channels)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md (InB visibility: read intake-bound fields and MTP snapshots read-only; no mutation of other modules; explicit does/does-not boundaries)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.60_coprocessor_offload_and_portability_rules.md (normalization/canonicalization eligible for deterministic offload; platform-independent determinism)
- applicability: planned exploratory module for InB as the memory buffer / input normalization skeleton. Focus on deterministic surface-form canonicalization into conceptual basins, bounded intake, provenance/audit, FIFO preservation, no semantic inference, and clean handoff contract.
- disposition_target: promote

## Purpose
This scaffold reserves the module slot for exploratory implementation of the Input Basin (InB) as the deterministic memory buffer for external input.

It corresponds to the input normalization stage in 10.10.10_system_architecture.md (first stage of the deterministic cycle) and the complete obligations defined in 20.100_inb_requirements.md.

The InB memory buffer is responsible for:
- Ingesting external/noisy signals into bounded TP input fields
- Deterministic, replayable transformations and canonicalization of equivalent surface forms under versioned parser/profile rules
- Schema validation of input mappings
- Preserving FIFO ordering metadata from intake through handoff (no reordering, skipping, or speculation)
- Deterministic malformed-input handling with fixed audit reason codes (reject-or-canonicalize policy)
- Enforcing explicit bounds on payload size, token count, and field cardinality with bounded reject/degrade
- Isolating transport/session metadata from semantic payload fields
- Emitting deterministic provenance for intake source, normalization profile, schema version, and acceptance/rejection outcome
- Applying execution-signature-bound profile precedence
- Operating only on intake-bound fields and approved interfaces (no reading or mutating OB, RB, TB, IB, GB, CIL, COB, COP, or MTP internal state)
- Producing explicit, versioned, testable, and auditable handoff contracts to downstream pathways
- Preserving platform-independent deterministic behavior
- Remaining fully testable via deterministic fixtures

The InB memory buffer **does not**:
- Perform inference or truth arbitration
- Mutate or interpret semantic content
- Reorder or speculate on sequence state
- Bypass GB supervisory control
- Introduce nondeterminism

## Scope
- placeholder module for requirements-driven exploration of InB as memory buffer
- no executable behavior is asserted yet (pure scaffold)
- will explore (via future prototype/harness): all behaviors and invariants defined in the 20.100 HLRs below, plus supporting 10-series contracts and boundaries

All exploration **SHALL** remain strictly deterministic, non-inferential, bounded, provenance-rich, and replayable. The full HLR list is reproduced here for exploratory visibility in the playground.

## Flows Alignment Statement

- **Forward Flow (10/20-series)**: Driven by the input normalization role and cycle position in 10.10.10_system_architecture.md (InB as first stage), channel and snapshot rules in 10.10.20, visibility and non-mutation contracts in 10.10.50, offload/portability constraints in 10.10.60, and the complete normative requirements in 20.100_inb_requirements.md (all 26 HLRs). Also informed by 20.30_ts_functional_model.md (determinism for input handling, no nondeterminism from variability, explicit contracts), 20.170_safety_requirements.md (InB protected from unsafe pathways), and 20.90_interfaces_and_io.md (handoff contracts).

- **Backward Flow (40-series evidence)**: Currently scaffold only. Once implemented, evidence will be generated via prototype and harness to demonstrate the core invariants and handoff contract under the full HLR load from 20.100.

- **Iterative Design Flow (playground exploration)**: This document includes the full HLR list from 20.100 for exploratory clarity so the complete requirement space can be felt against the skeleton's invariants, boundaries, and handoff. This helps surface practical questions about bounded buffers, provenance richness, non-inference enforcement, and FIFO preservation before upstream refinement. 40.20_master_program_guide.md provides the workflow guidance for this exploration (not treated as requirements).

**Agreement Statement**: The three flows are provisionally aligned on InB as the deterministic, non-inferential memory buffer for external input normalization. The full 20.100 HLR set is made visible here in the 40.xx playground for insight purposes only. Authoritative requirements remain in 20.xx; coverage audit remains in 30.xx. Full alignment statements will be refreshed as the skeleton evolves through future phases.

## Phase A Deliverables (this document)
- High-level description of InB as memory buffer for exploratory prototyping
- Mapping of 10/20-series intent to skeleton responsibilities
- Full reproduction of the 20.100 HLR set for exploratory visibility (see "What Phase B Must Explore")
- Identification of core invariants, boundaries, and handoff contract
- Clear definition of what the future Phase B must explore
- Tentative data structures / handoff interface
- No algorithms or final numeric thresholds asserted (governed by 20-series)

## What Phase B Must Explore
Phase B **SHALL** explore and produce concrete (deterministic, replayable) evidence against the complete set of obligations. The full list from 20.100_inb_requirements.md is reproduced here for exploratory clarity in the playground:

1. HLR-20.100-001: InB SHALL ingest external signals into bounded TP input fields.
2. HLR-20.100-002: InB SHALL NOT perform inference or truth arbitration.
3. HLR-20.100-003: InB transformations SHALL be deterministic and replayable.
4. HLR-20.100-004: InB input mappings SHALL be schema-validated.
5. HLR-20.100-005: InB canonicalization SHALL normalize equivalent surface forms deterministically under versioned parser/profile rules.
6. HLR-20.100-006: InB SHALL preserve FIFO ordering metadata from intake through handoff and SHALL NOT reorder, skip, or speculate on sequence state.
7. HLR-20.100-007: InB malformed-input handling SHALL follow deterministic reject-or-canonicalize policy with fixed audit reason codes.
8. HLR-20.100-008: InB SHALL enforce deterministic limits on payload size, token count, and field cardinality using bounded reject/degrade behavior.
9. HLR-20.100-009: InB SHALL isolate transport/session metadata from semantic payload fields and SHALL prevent implicit meaning mutation by transport attributes.
10. HLR-20.100-010: InB SHALL map source encodings to canonical internal representation deterministically, including Unicode and escape normalization rules.
11. HLR-20.100-011: InB SHALL emit deterministic provenance entries for intake source, normalization profile, schema version, and acceptance/rejection outcome.
12. HLR-20.100-012: InB acceptance/rejection outcomes SHALL be auditable, append-only, and reproducible for identical input/signature state.
13. HLR-20.100-013: InB SHALL apply execution-signature-bound profile precedence over environment defaults.
14. HLR-20.100-014: InB profile/policy activation changes SHALL activate only at deterministic safe boundaries.
15. HLR-20.100-015: On profile/policy activation validation failure, InB SHALL retain prior valid signature state and emit fixed audit reason codes.
16. HLR-20.100-016: InB SHALL reject unsupported enum, schema, or wire-map states deterministically with fixed audit reason codes.
17. HLR-20.100-017: InB reason-code dictionaries SHALL use immutable identifiers and versioned deterministic mapping behavior.
18. HLR-20.100-018: InB SHALL preserve platform-independent deterministic behavior under equivalent input/signature/profile state.
19. HLR-20.100-019: InB SHALL NOT read or mutate OB, RB, TB, IB, GB, CIL, COB, COP, or MTP internal state and SHALL operate only on intake-bound fields and approved interfaces.
20. HLR-20.100-020: InB handoff contracts to downstream intake/integration pathways SHALL be explicit, versioned, testable, and auditable.
21. HLR-20.100-021: InB SHALL treat timestamps as evidence metadata only; ordering-critical behavior SHALL derive from deterministic sequence/token state.
22. HLR-20.100-022: InB diagnostic exports for intake events SHALL use deterministic flush boundaries, canonical field ordering, and canonical serialization.
23. HLR-20.100-023: InB zero-event windows SHALL follow deterministic empty-artifact semantics (canonical empty artifact or no artifact with fixed reason code).
24. HLR-20.100-024: InB requirements in this module SHALL satisfy and SHALL NOT weaken parent invariants defined by 20.10 and 20.30.
25. HLR-20.100-025: InB behavior SHALL remain fully testable through deterministic fixtures covering valid, malformed, oversized, and unsupported-profile/schema inputs.
26. HLR-20.100-026: InB SHALL hand off accepted canonicalized input without introducing semantic interpretation, leaving inference, routing, and truth decisions to downstream TS/GB-governed components.

Additional exploratory items (drawn from 10-series contracts):
- Strict tick-cycle boundary compliance (first stage completion before downstream stages; no MTP mutation; read-only upstream snapshots only).
- Explicit handoff contract definition (schema, provenance, audit codes, FIFO metadata, bounds).
- Evidence model sufficient for replay and audit (intake provenance, acceptance/rejection outcomes).

## Non-Goals (Scaffold and Initial Phase B)
This module **SHALL NOT**:
- Perform semantic inference, stance/intent classification, or truth-related work.
- Mutate MTP, TP (beyond handoff fields), or any downstream module state.
- Define final canonical schemas or parser rules (those are governed by 20-series and 10.10.60 profiles).
- Implement full scheduler, regulator, or GB logic.
- Provide production-grade logging or MB telemetry (only the minimal deterministic intake evidence for the skeleton).
- Bypass safe boundaries or GB approval for any global behavior changes.

## Risks & Unknowns to Investigate
- Core non-inference invariant enforcement under noisy, malformed, or oversized inputs.
- Practical mechanics of bounded buffers and reject/degrade without losing FIFO or provenance.
- Exact shape of the handoff contract to RB/CIL (what fields, metadata, and guarantees are sufficient and minimal).
- Interaction with execution signatures, profiles, and safe boundaries for profile activation.
- How much internal buffer state (if any) InB may maintain locally without violating visibility rules or introducing hidden coupling.
- Evidence richness needed for higher-level audit while staying minimal and replay-safe.
- Edge cases around zero-event windows, unsupported states, and deterministic empty-artifact semantics.
- Ensuring the skeleton remains strictly non-semantic even when exploring full HLR load.

## Required Next Step
Advance from pure scaffold to implemented prototype + harness that exercises the core invariants and handoff contract against the full HLR list reproduced above. Populate verification_capsule.md and requirements_delta.md with executed evidence once available. The full HLR visibility in this document supports exploratory thinking in the playground; authoritative requirements remain in 20.100_inb_requirements.md and related 20.xx documents.

## Traceability
- 10.10.10_system_architecture.md (InB as input normalization stage, MTP/TP state model, module-local temporary buffers, deterministic cycles)
- 10.10.20_interprocess_communication_and_channels.md (immutable messages, structured snapshots, bounded channels, no shared mutable memory)
- 10.10.50_module_contracts_and_visibility_rules.md (InB visibility and non-mutation boundaries)
- 10.10.60_coprocessor_offload_and_portability_rules.md (deterministic offload eligibility for normalization)
- 20.100_inb_requirements.md (complete source of the 26 HLRs reproduced above for exploratory visibility)
- 20.30_ts_functional_model.md (determinism, no nondeterminism from variability, explicit contracts)
- 20.170_safety_requirements.md (InB protection from unsafe pathways)
- 20.90_ib_requirements.md and 20.200_traceability_matrix.md (interfaces and traceability)
- 40.20_master_program_guide.md (workflow guidance for playground exploration — not treated as requirements)
- 40.100_inb_prototypes/prototype.py (current stub)
- 40.100_inb_prototypes/harness.py (current stub)
- 40.100_inb_prototypes/requirements_delta.md (current scaffold delta)

**Note on authority**: The full HLR list from 20.100 is included in this 40.xx playground document solely for exploratory clarity and to make the complete requirement space visible during design thinking. 20.xx documents remain the authoritative source of truth. 30.xx provides the coverage audit. This document makes no claim to canonical status.

All future Phase B evidence **SHALL** be traceable to the 20.100 HLRs and supporting 10/20 sources above.