# Requirements Delta

## Scaffold Status
- scaffold_status: implemented (Phase B complete, 2026-06-08)
- Phase A: **approved** (CP final review, 2026-06-08)
- Phase B: **approved** (16/16 PASS; CP review, 2026-06-08; 40.510-103)

## Anchors
- 20-anchor: thought_simulator/20_requirements/20.100_inb_requirements.md (full 26 HLRs reproduced in software_description.md for exploratory clarity in the playground)
- 10.10-anchors:
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md (InB role, input stage, MTP/TP state, module-local buffers)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.20_interprocess_communication_and_channels.md (immutable channels, snapshots, no shared mutable memory)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md (InB visibility and non-mutation boundaries)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.60_coprocessor_offload_and_portability_rules.md (deterministic offload for normalization)

## Exploratory Note
The complete set of HLR-20.100-001 through HLR-20.100-026 (plus supporting 10-series contracts) is made visible in the accompanying software_description.md for playground exploration and insight. 20.xx remains the authoritative source of truth. 30.xx remains the coverage audit layer. 40.50 is non-canonical.

## Part B Evidence (Executed)
- Harness run: 2026-06-08 (Phase B complete)
- Artifact: artifacts/inb_verification_run_2026-06-08.json
- Status: PASS (16/16 scenarios)
- Evidence types: behavioral, structural, negative, replay, golden diff

### Implemented / demonstrated
| HLR | Implementation | Scenario |
|-----|----------------|----------|
| 001 | Bounded intake via `normalize()` | `positive_clean_canonicalization` |
| 002 | No inference in `_normalize_text` | all positive canonicalization |
| 003 | `state_digest` replay contract | `positive_deterministic_replay` |
| 004 | `_validate_schema()` | `negative_unsupported_schema` |
| 005 | Profile-bound canonicalization | equivalent forms, unicode |
| 006 | `batch_normalize()` FIFO | `positive_fifo_batch_order` |
| 007 | `_make_reject()` fixed codes | `negative_malformed_input` |
| 008 | `_check_bounds()` | `negative_oversize_payload` |
| 009 | Transport fields in provenance only | `positive_transport_metadata_isolation` |
| 010 | NFKC + surface rules | `positive_unicode_normalization` |
| 011 | Provenance block on all paths | all scenarios |
| 012 | Reproducible outcomes + digest | replay + rejects |
| 014 | `request_profile_activation()` deferral | `profile_activation_boundary` |
| 015 | `apply_safe_boundary()` + retain prior | `profile_activation_boundary` |
| 016 | Schema/wire/profile rejects | negative schema/profile |
| 018 | Platform-independent JSON digest | `positive_deterministic_replay` |
| 019 | `run_first_stage()` no MTP mutation | `positive_tick_boundary_first_stage` |
| 020 | `handoff` object on accept | `positive_iiinb_handoff_contract` |
| 021 | `timestamp` in provenance only | `positive_timestamp_metadata_only` |
| 022 | `export_intake_diagnostics()` | `positive_diagnostic_export_ordering` |
| 023 | `process_tick_intake([])` | `positive_zero_event_window` |
| 025 | Fixture matrix valid/malformed/oversized | full harness |
| 026 | Handoff without semantic interpretation | `positive_iiinb_handoff_contract` |

HLR-013, 017, and 024 are intentionally excluded here and tracked in the Open / partial table below.

### Open / partial
| HLR | Gap | Notes |
|-----|-----|-------|
| 013 | Signature-bound profile precedence | Per-input profile reject demonstrated; execution-signature model not wired |
| 017 | Full immutable reason-code registry | `REASON_CODES` frozenset defined; versioned dictionary mapping not exported |
| 024 | Parent 20.10/20.30 cross-check | Deferred to 30-series coverage audit |

## Phase 1 delta (40.510-103)
- Added `handoff` contract: `next_stage=input_semantic_repair`, ordering InB→IIInB→RB
- Scenario: `positive_iiinb_handoff_contract` — PASS

## Phase B delta (40.05)
- Added schema validation (`INTAKE_SCHEMA_VERSION`, `WIRE_MAP_VERSION`)
- Added `process_tick_intake`, `request_profile_activation`, `apply_safe_boundary`, `export_intake_diagnostics`, `run_first_stage`
- Expanded harness from 8 → 16 scenarios; full test matrix PASS

## Flows Alignment Statement

- **Forward Flow (20-series)**: [20.100](../../20_requirements/20.100_inb_requirements.md) drives all implemented obligations; [20.101](../../20_requirements/20.101_iiinb_requirements.md) informs handoff ordering.
- **Backward Flow (40-series evidence)**: 16/16 PASS artifact proves deterministic intake skeleton; residuals named above.
- **Iterative Design Flow (50-series influence)**: None yet.

**Agreement Statement**: Aligned for Phase B closure. Promotion to 30-series requires closing HLR-013, 017, 024 gaps.