# 40.100_inb_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP final review, 2026-06-08)
- Phase B (prototype + harness + evidence): **initial execution complete** (8/8 PASS, 2026-06-08); iterative expansion continues

## Phase B Deliverables (Executed — initial pass)
- Harness executed 8 scenarios; artifact: `artifacts/inb_verification_run_2026-06-08.json`
- Core invariants demonstrated: non-semantic canonicalization, bounded reject-with-audit, FIFO preservation, deterministic replay, provenance emission, isolation, explicit handoff contract (`InB → IIInB → RB`)
- HLR coverage (exploratory subset): 002, 003, 005, 006, 007, 008, 011, 012, 016, 018, 019, 020
- Remaining HLR exploration: 001, 004, 009–010, 013–015, 017, 021–026 (see Test Matrix below)
- Additional invariants still to demonstrate: tick-cycle boundary compliance, zero-event windows, diagnostic exports, profile activation boundaries
- Note: The full HLR list from 20.100_inb_requirements.md is included in this document for exploratory clarity and to make the complete requirement space visible during playground exploration. 20.xx remains the sole source of truth; 30.xx remains the authoritative coverage audit layer. 40.100 is a playground and not authoritative.

## Scaffold Metadata
- scaffold_status: implemented (initial Phase B pass)
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
- exploratory module for requirements-driven InB memory-buffer prototyping
- initial prototype + harness implemented (`prototype.py`, `harness.py`); evidence in `verification_capsule.md` and `requirements_delta.md`
- continues to explore all behaviors and invariants defined in the 20.100 HLRs below, plus supporting 10-series contracts and boundaries

All exploration **SHALL** remain strictly deterministic, non-inferential, bounded, provenance-rich, and replayable. The full HLR list is reproduced here for exploratory visibility in the playground.

## Flows Alignment Statement

- **Forward Flow (10/20-series)**: Driven by the input normalization role and cycle position in 10.10.10_system_architecture.md (InB as first stage), channel and snapshot rules in 10.10.20, visibility and non-mutation contracts in 10.10.50, offload/portability constraints in 10.10.60, and the complete normative requirements in 20.100_inb_requirements.md (all 26 HLRs). Also informed by 20.30_ts_functional_model.md (determinism for input handling, no nondeterminism from variability, explicit contracts), 20.170_safety_requirements.md (InB protected from unsafe pathways), and 20.90_interfaces_and_io.md (handoff contracts).

- **Backward Flow (40-series evidence)**: Initial evidence generated (2026-06-08): 8/8 harness PASS covering canonicalization, bounded reject, FIFO, replay, provenance, isolation, and `InB → IIInB` handoff contract. Artifact: `artifacts/inb_verification_run_2026-06-08.json`. Remaining HLRs tracked in Test Matrix and `requirements_delta.md`.

- **Iterative Design Flow (playground exploration)**: This document includes the full HLR list from 20.100 for exploratory clarity so the complete requirement space can be felt against the skeleton's invariants, boundaries, and handoff. This helps surface practical questions about bounded buffers, provenance richness, non-inference enforcement, and FIFO preservation before upstream refinement. 40.20_master_program_guide.md provides the workflow guidance for this exploration (not treated as requirements).

**Agreement Statement**: The three flows are provisionally aligned on InB as the deterministic, non-inferential memory buffer for external input normalization. The full 20.100 HLR set is made visible here in the 40.xx playground for insight purposes only. Authoritative requirements remain in 20.xx; coverage audit remains in 30.xx. Full alignment statements will be refreshed as the skeleton evolves through future phases.

## Phase A Deliverables (this document)
- High-level description of InB as memory buffer for exploratory prototyping
- Mapping of 10/20-series intent to skeleton responsibilities
- Full reproduction of the 20.100 HLR set for exploratory visibility (see "What Phase B Must Explore")
- Identification of core invariants, boundaries, and handoff contract
- Clear definition of what Phase B must explore (initial pass executed; expansion ongoing)
- Draft handoff contract skeleton, state digest definition, schema validation, unicode normalization, profile activation target semantics, transport/session isolation, tick-cycle boundary test placeholder, reject/degrade policy, minimal internal state, and test matrix (below)
- Prototype thresholds (e.g. `MAX_PAYLOAD_CHARS`, `MAX_TOKENS`) are playground fixtures only; governed by 20-series for authoritative values

## Handoff Contract (Draft Skeleton)
Accepted outputs include an explicit handoff object for downstream intake/integration pathways (HLR-20.100-020, 20.101-003):

```
handoff = {
  "contract_version": "inb_to_iiinb_v1",
  "next_stage": "input_semantic_repair",
  "downstream_after_repair": "routing",
  "ordering": ["inb_surface_norm", "input_semantic_repair", "routing"],
}
```

Accompanying payload fields on accepted output:

```
output = {
  "canonical_content": str,
  "provenance": {
    "source": str,
    "profile": str,
    "intake_order": int,
    "outcome": "accepted" | "rejected",
    "reason_code": str | null,
  },
  "metadata": {...},
  "state_digest": str,
  "handoff": {...},   # present on accepted path only
}
```

Rejected outputs omit `handoff`; provenance carries fixed `reason_code` and `outcome: "rejected"`.

## State Digest (Definition)
`state_digest` is the deterministic replay fingerprint for harness verification (HLR-20.100-003, 018). It is computed **before** `handoff` is attached on the accepted path, so `handoff` is outside the current replay contract.

- **Accepted path input:** `{content, provenance, metadata}` — canonical normalized text plus intake provenance and metadata only
- **Rejected path input:** `{outcome: "rejected", reason_code, provenance}`
- **Algorithm:** SHA-256 over canonical JSON (`sort_keys=True`, `separators=(",", ":")`), UTF-8 encoded
- **Stability:** platform-independent for equivalent input/profile state when the same serialization rules are used; harness asserts identical raw input → identical `state_digest`
- **Replay contract:** `state_digest` is the primary equivalence check in `positive_deterministic_replay`; downstream consumers should not treat it as a semantic hash

## Schema Validation (Draft)
Playground wire schema for intake mapping validation (HLR-20.100-004). Authoritative schemas remain in 20-series; this is a fixture for Phase B expansion.

- **Assumed schema version:** `inb_intake_v1` (playground fixture, not canonical)
- **Required fields:** `content` (str) — primary payload
- **Optional fields:** `source` (str, default `"unknown"`), `intake_order` (int, default `0`), `profile` (str, must match active profile if present)
- **Validation today:** input must be a `dict`; non-dict → `MALFORMED_INPUT`
- **Unsupported mapping (planned):** unknown required keys, wrong types, or unsupported wire-map version → fixed `reason_code` (e.g. `UNSUPPORTED_SCHEMA`, `INVALID_FIELD_TYPE`) — not yet harness-tested

## Unicode and Escape Normalization (Draft)
Surface-form canonicalization policy implemented in `prototype.py` (HLR-20.100-005, 010). Playground profile `v1.0` applies:

- **Unicode:** NFKC normalization (compatibility decomposition + canonical composition)
- **Case:** lowercase
- **Whitespace:** strip leading/trailing; collapse internal runs to single space
- **Punctuation:** collapse repeated `!`, `?`, `.` deterministically (non-semantic)
- **Escape normalization:** not yet implemented (e.g. `\n`, `\t`, `\uXXXX` unescaping) — planned harness scenario `positive_unicode_normalization`

Current harness coverage for HLR-010 is **partial** via `positive_equivalent_surface_forms` (case/whitespace/punctuation only).

## Profile Activation Boundary (Target Semantics — Not Yet Implemented)
Target behavior for HLR-20.100-014 and 015. **Current prototype** rejects per-input profile mismatch immediately (`UNSUPPORTED_PROFILE` in `negative_unsupported_profile`); deferred activation is not implemented.

Target semantics at deterministic safe boundaries:

```
active_profile = v1.0
incoming requests profile v1.1 at mid-tick
→ activation deferred until next safe boundary
→ prior profile (v1.0) retained for current tick
→ audit: reason_code PROFILE_ACTIVATION_DEFERRED
```

On validation failure at a safe boundary: retain prior valid signature/profile state; emit fixed audit reason code (e.g. `PROFILE_ACTIVATION_FAILED`). Harness scenario `profile_activation_boundary` is planned.

## Transport and Session Metadata Isolation (Draft)
Transport and session attributes must not alter semantic payload fields or `canonical_content` (HLR-20.100-009).

- **Semantic payload:** `content` — sole field driving canonicalization
- **Transport/session metadata (playground):** `source`, `intake_order` — recorded in provenance/metadata only; variations do not change normalized text for identical `content`
- **Profile:** execution-signature-bound configuration, not transport — mismatches handled per profile policy
- **Invariant:** identical `content` under same active profile → identical `canonical_content`, regardless of `source` or transport envelope variations
- **Planned scenario:** `positive_transport_metadata_isolation` — not yet harness-tested

## Tick-Cycle Boundary (Test Placeholder)
Per 40.510-103 and 10.10.10 (InB as first deterministic-cycle stage). Orchestration detail deferred to 20.36 / 40.60; this is playground-level test design.

- InB completes surface normalization and emits handoff before IIInB or RB stages run
- No mutation of MTP or downstream module internal state during InB processing
- No reads of OB, RB, TB, IB, GB, CIL, COB, COP internal state (HLR-019)
- Handoff is the sole outbound contract; downstream stages consume it at the next tick boundary
- **Planned scenario:** `positive_tick_boundary_first_stage` — not yet harness-tested

## Deterministic Reject/Degrade Policy (Draft)
- **Reject path**: malformed input, unsupported profile, oversize payload, too many tokens, unsupported enum/schema/wire-map states → `outcome: "rejected"`, `canonical_content: null`, fixed immutable `reason_code` (e.g. `MALFORMED_INPUT`, `UNSUPPORTED_PROFILE`, `OVERSIZE_PAYLOAD`, `TOO_MANY_TOKENS`)
- **Degrade path**: reserved for bounded-limit scenarios where partial retention is permitted under 20.100; current prototype uses reject-only for oversize/token limits
- **Reason codes**: immutable identifiers with versioned deterministic mapping (HLR-017); no free-text inference
- **Empty-artifact semantics** (HLR-023): zero-event windows emit canonical empty artifact or no artifact with fixed reason code — not yet exercised in harness

## Minimal Internal State
**May hold (per tick / per invocation):**
- Active normalization profile identifier (`profile`, default `v1.0`)
- Ephemeral working state during `normalize()` / `batch_normalize()` only (no cross-call mutation)

**Must not hold:**
- MTP, TP, OB, RB, TB, IB, GB, CIL, COB, COP internal state
- Cross-tick FIFO queue or speculative sequence buffers (FIFO metadata travels in provenance/intake_order, not hidden reordering state)
- Semantic interpretation caches or inference artifacts

**Persistence and reset:**
- No state persists across harness scenarios; each `InB()` instance starts clean
- Per-tick reset: profile-bound; profile activation changes only at deterministic safe boundaries (HLR-014 — not yet harness-tested)

## Test Matrix (Draft)
| Category | Scenario (harness) | HLR anchors | Status |
|----------|-------------------|-------------|--------|
| Valid canonicalizable input | `positive_clean_canonicalization` | 001, 003, 005 | PASS |
| Equivalent surface forms | `positive_equivalent_surface_forms` | 003, 005 | PASS |
| Unicode / escape normalization | `positive_unicode_normalization` *(planned)* | 010 | partial (impl only) |
| Malformed input | `negative_malformed_input` | 007, 016 | PASS |
| Oversized input | `negative_oversize_payload` | 008 | PASS |
| Unsupported profile | `negative_unsupported_profile` | 013, 016 | PASS |
| FIFO batch order | `positive_fifo_batch_order` | 006 | PASS |
| Deterministic replay | `positive_deterministic_replay` | 003, 018 | PASS |
| IIInB handoff contract | `positive_iiinb_handoff_contract` | 020, 026 | PASS |
| Zero-event window | *(planned)* | 023 | todo |
| Diagnostic export ordering | *(planned)* | 022 | todo |
| Profile activation boundary | `profile_activation_boundary` *(planned)* | 014, 015 | todo |
| Transport/session isolation | `positive_transport_metadata_isolation` *(planned)* | 009 | todo |
| Tick-cycle boundary (first stage) | `positive_tick_boundary_first_stage` *(planned)* | 019, 10.10.10 | todo |
| Schema validation | `negative_unsupported_schema` *(planned)* | 004 | todo |
| Timestamp-as-metadata only | *(planned)* | 021 | todo |

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
Expand harness coverage for remaining HLRs (see Test Matrix), add tick-cycle boundary tests, and enrich evidence for 30-series audit. `verification_capsule.md` and `requirements_delta.md` record the initial 8/8 PASS run. The full HLR visibility in this document supports exploratory thinking in the playground; authoritative requirements remain in 20.100_inb_requirements.md and related 20.xx documents.

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
- 40.100_inb_prototypes/prototype.py (implemented skeleton)
- 40.100_inb_prototypes/harness.py (8-scenario harness)
- 40.100_inb_prototypes/verification_capsule.md (Part B evidence summary)
- 40.100_inb_prototypes/requirements_delta.md (executed delta + open work)
- 40.100_inb_prototypes/artifacts/inb_verification_run_2026-06-08.json

**Note on authority**: The full HLR list from 20.100 is included in this 40.xx playground document solely for exploratory clarity and to make the complete requirement space visible during design thinking. 20.xx documents remain the authoritative source of truth. 30.xx provides the coverage audit. This document makes no claim to canonical status.

All future Phase B evidence **SHALL** be traceable to the 20.100 HLRs and supporting 10/20 sources above.