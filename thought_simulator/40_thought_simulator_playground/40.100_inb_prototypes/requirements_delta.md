# Requirements Delta

## Scaffold Status
- scaffold_status: implemented (initial Phase B pass, 2026-06-08)
- Phase A: **approved** (CP final review, 2026-06-08)

## Anchors
- 20-anchor: thought_simulator/20_requirements/20.100_inb_requirements.md (full 26 HLRs reproduced in software_description.md for exploratory clarity in the playground)
- 10.10-anchors:
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md (InB role, input stage, MTP/TP state, module-local buffers)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.20_interprocess_communication_and_channels.md (immutable channels, snapshots, no shared mutable memory)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md (InB visibility and non-mutation boundaries)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.60_coprocessor_offload_and_portability_rules.md (deterministic offload for normalization)

## Exploratory Note
The complete set of HLR-20.100-001 through HLR-20.100-026 (plus supporting 10-series contracts) is made visible in the accompanying software_description.md for playground exploration and insight. 20.xx remains the authoritative source of truth. 30.xx remains the coverage audit layer. 40.100 is non-canonical.

## Part B Evidence (Executed)
- Harness run: 2026-06-08 (Phase 1 handoff extension)
- Artifact: artifacts/inb_verification_run_2026-06-08.json
- Status: PASS (8/8 scenarios)
- Core invariants demonstrated via scenarios:
  - non_semantic_canonicalization (HLR-20.100-002, 003, 005)
  - bounded_reject_with_audit (HLR-20.100-007, 008, 016)
  - deterministic_replay (HLR-20.100-003, 018)
  - fifo_order_preservation (HLR-20.100-006)
  - provenance_emission (HLR-20.100-011, 012)
  - isolation (no MTP/other module mutation) (HLR-20.100-019)
  - explicit handoff contract (HLR-20.100-020)
- Scenarios executed:
  - positive_clean_canonicalization
  - positive_equivalent_surface_forms
  - negative_oversize_payload
  - negative_malformed_input
  - negative_unsupported_profile
  - positive_fifo_batch_order
  - positive_deterministic_replay

## Phase 1 delta (40.510-103)
- Added `handoff` contract on accepted output: `next_stage=input_semantic_repair`, ordering InB→IIInB→RB (HLR-20.100-020, 20.101-003)
- Scenario: `positive_iiinb_handoff_contract` — PASS

## Open Work (next iteration)
- Expand negative-path coverage for more HLRs (e.g. zero-event windows HLR-023, diagnostic exports HLR-022)
- Add explicit tick-cycle boundary enforcement tests
- Integrate with upstream snapshot/MTP state for more realistic handoff
- Generate richer evidence for 30-series verification capsule

## Proposed Focus Areas (satisfied in this run)
- Deterministic acceptance/rejection equivalence for identical input/signature/profile state
- Deterministic canonicalization across equivalent noisy surface forms
- Deterministic FIFO-preserving sequence metadata continuity at handoff
- Deterministic reject-with-audit behavior for malformed/oversized/unsupported states
- Deterministic provenance and append-only intake audit evidence
- Strict isolation (no MTP mutation, no downstream state reads)